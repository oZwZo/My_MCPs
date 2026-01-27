# MCP 搜索服务器 - 功能改进说明

## 改进日期
2025-01-27 (v2.0)

## 改进概述

本次改进主要针对NCBI PubMed API的速率限制和Google Scholar搜索模式的扩展，大幅提升了文献搜索的灵活性和深度。

---

## 1. NCBI PubMed API 速率限制

### 问题描述
NCBI E-utilities API有严格的速率限制：
- **没有API密钥**: 每秒3次请求
- **有API密钥**: 每秒10次请求

### 实现方案

#### RateLimiter 类
```python
class RateLimiter:
    """令牌桶算法实现的速率限制器"""
```

**功能特性**:
- 使用异步锁（`asyncio.Lock`）确保线程安全
- 滑动时间窗口算法，精确控制请求频率
- 自动清理过期请求记录
- 当达到限制时，自动等待直到可以发送新请求

**使用方式**:
```python
NCBI_RATE_LIMITER = RateLimiter(max_calls=10, time_window=1.0)

# 在每次API调用前
await NCBI_RATE_LIMITER.acquire()
```

**应用位置**:
- PubMed搜索API (`esearch.fcgi`)
- PubMed摘要获取API (`esummary.fcgi`)

### 效果
- ✅ 完全符合NCBI使用政策
- ✅ 避免因超限被API封禁
- ✅ 自动处理并发请求的速率控制

---

## 2. Google Scholar 三种搜索模式

### 2.1 快速模式 (Quick Mode)

**特点**:
- 最快的搜索速度
- 直接返回前10篇文献
- 适合快速浏览和初步调研

**实现**:
```python
async def search_scholar_quick(query: str, num_results: int = 10)
```

**使用示例**:
```python
result = await search_scholar(
    "CRISPR gene editing",
    mode=ScholarSearchMode.QUICK,
    num_results=10
)
```

---

### 2.2 相关度优化模式 (Relevance Mode)

**特点**:
- 搜索前200篇文献
- 根据位置计算相关度分数
- 返回最相关的N篇文献

**实现细节**:
```python
async def search_scholar_relevance(query: str, num_results: int = 10)
```

**相关度计算**:
- 第1篇: 相关度分数 1.0
- 第200篇: 相关度分数 0.0
- 线性递减模型

**分页处理**:
- SerpApi每次最多返回20篇
- 需要多次调用以获取200篇
- 自动处理分页逻辑

**使用示例**:
```python
result = await search_scholar(
    "machine learning in biology",
    mode=ScholarSearchMode.RELEVANCE,
    num_results=20
)
```

---

### 2.3 深度查找模式 (Deep Mode)

#### 功能概述

这是最复杂的搜索模式，通过引文网络扩展搜索范围，并使用多指标综合排序。

#### 实现步骤

**步骤1: 初始文献获取**
- 使用相关度优化模式获取前50篇文献
- 作为后续分析的基础文献池

**步骤2: 筛选关键文献**
- 从50篇中选择相关度最高的20篇
- 用于引文分析和关键词提取

**步骤3: 引文扩展**
- 提取关键文献的标题关键词
- 生成扩展搜索查询
- 对每个关键词进行额外搜索
- 扩大文献池

**步骤4: 多维度评分**

对文献池中的每篇文献计算三个分数：

1. **引用分数** (Citation Score, 40%权重)
   ```
   citation_score = min(paper_citations / max_citations, 1.0)
   ```
   - 标准化到0-1范围
   - 引用次数越多分数越高

2. **相关度分数** (Relevance Score, 40%权重)
   ```
   relevance_score = 1.0 - (position / total_results)
   ```
   - 来自初始搜索的相关度
   - 扩展文献默认为0.5

3. **时效性分数** (Recency Score, 20%权重)
   ```
   recency_score = max(0, 1.0 - (years_old / 20.0))
   ```
   - 20年线性衰减
   - 越新的文献分数越高
   - 当前年份2025

**步骤5: 综合排序**
```python
total_score = (
    0.4 * citation_score +
    0.4 * relevance_score +
    0.2 * recency_score
)
```

#### 实现代码
```python
async def search_scholar_deep(query: str, num_results: int = 5)
    # 1. 获取初始文献
    initial_result = await search_scholar_relevance(query, num_results=50)

    # 2. 筛选关键文献
    top_papers = sorted(initial_papers, key=relevance)[:20]

    # 3. 引文扩展
    for term in extracted_keywords[:10]:
        expansion_query = f"{query} {term}"
        # 执行扩展搜索...

    # 4-5. 评分和排序
    for paper in all_papers:
        # 计算三个分数...
        # 综合排序...
```

#### 返回结果

每篇文献包含：
```json
{
  "title": "...",
  "summary": "...",
  "cited_by": 150,
  "year": 2023,
  "scores": {
    "citation": 0.850,
    "relevance": 0.920,
    "recency": 0.800,
    "total": 0.858
  }
}
```

#### 使用示例
```python
result = await search_scholar(
    "CRISPR gene editing",
    mode=ScholarSearchMode.DEEP,
    num_results=5
)

print(f"文献池大小: {result['pool_size']}")
print(f"扩展查询数: {result['expansion_queries']}")

for paper in result['results']:
    print(f"{paper['title']}")
    print(f"  总分: {paper['scores']['total']}")
    print(f"  引用度: {paper['scores']['citation']}")
    print(f"  相关度: {paper['scores']['relevance']}")
    print(f"  时效性: {paper['scores']['recency']}")
```

---

## 3. 工具接口改进

### MCP工具定义更新

**search_scholar** 工具新增参数：

```json
{
  "name": "search_scholar",
  "description": "...",
  "inputSchema": {
    "properties": {
      "query": "搜索查询词",
      "mode": {
        "type": "string",
        "enum": ["quick", "relevance", "deep"],
        "default": "quick"
      },
      "num_results": {
        "type": "number",
        "default": 10,
        "maximum": 50
      }
    }
  }
}
```

### 输出格式化改进

**深度模式输出示例**：
```markdown
## Google Scholar Search Results (Deep Mode)

Query: CRISPR gene editing
Pool Size: 247 papers
Expansion Queries: 8
Returned: 5 papers

### 1. CRISPR-Cas9 gene editing for... (0.858)
**Cited by:** 1250 papers
**Scores:** Citation=0.850, Relevance=0.920, Recency=0.800, Total=0.858

...
```

---

## 4. 技术细节

### 新增数据结构

#### ScholarSearchMode (枚举)
```python
class ScholarSearchMode(str, Enum):
    QUICK = "quick"
    RELEVANCE = "relevance"
    DEEP = "deep"
```

#### PaperScore (数据类)
```python
@dataclass
class PaperScore:
    paper: dict
    citation_score: float
    relevance_score: float
    recency_score: float
    total_score: float
```

### 异步处理

所有搜索函数都是异步的，支持并发请求：
```python
async def search_scholar(...)
```

### 错误处理

- 网络错误捕获和友好提示
- API密钥验证
- 速率限制异常处理
- 空结果处理

---

## 5. 性能考虑

### 快速模式
- API调用: 1次
- 预计时间: < 2秒
- 适用场景: 快速查询

### 相关度优化模式
- API调用: 10次 (200篇 / 20每次)
- 预计时间: 5-10秒
- 适用场景: 全面搜索

### 深度查找模式
- API调用: 10-20次
- 预计时间: 15-30秒
- 适用场景: 高质量文献筛选

---

## 6. 使用建议

### 模式选择指南

1. **快速模式** - 适用于：
   - 初步了解一个主题
   - 快速验证想法
   - 测试搜索关键词

2. **相关度优化模式** - 适用于：
   - 需要更全面的文献覆盖
   - 寻找特定主题的核心文献
   - 文献综述的初步阶段

3. **深度查找模式** - 适用于：
   - 寻找高影响力的核心文献
   - 需要最新且高质量的研究
   - 深入研究某个具体方向
   - 论文写作前的文献调研

### 最佳实践

1. **从快速模式开始**，了解大概情况
2. **使用相关度优化模式**获取更全面的文献
3. **对关键查询使用深度模式**，获得最优文献推荐

### API成本考虑

- SerpApi按调用次数收费
- 深度模式会消耗更多API调用
- 建议对重要查询使用深度模式

---

## 7. 测试

提供了完整的测试脚本 `test_server.py`：

```bash
# 激活虚拟环境
source activate.sh

# 运行测试
python test_server.py
```

测试内容：
1. ✅ NCBI速率限制验证
2. ✅ PubMed搜索功能
3. ✅ Scholar快速模式
4. ✅ Scholar相关度优化模式
5. ✅ Scholar深度查找模式

---

## 8. 文件变更

### 修改的文件
- `mcp_server.py` - 主要功能实现
- `README.md` - 更新使用说明
- `requirements.txt` - 无需更新（使用标准库）

### 新增的文件
- `test_server.py` - 测试脚本
- `IMPROVEMENTS.md` - 本文档

---

## 9. 向后兼容性

✅ **完全向后兼容**

- 现有的`search_pubmed`调用不受影响
- `search_scholar`的默认行为保持不变（快速模式）
- 新增的`mode`参数是可选的

---

## 10. 未来改进方向

### 可能的增强功能

1. **缓存机制**
   - 缓存搜索结果避免重复API调用
   - 特别是深度模式的中间结果

2. **并行处理**
   - 并行执行多个扩展搜索
   - 减少深度模式的等待时间

3. **自定义权重**
   - 允许用户调整三个指标的权重
   - 例如更重视时效性或引用度

4. **导出功能**
   - 支持导出为BibTeX、EndNote格式
   - 生成文献引用

5. **交互式模式**
   - 允许用户筛选和重新排序
   - 基于用户反馈优化排序

---

## 11. 常见问题

### Q: 为什么深度模式需要这么长时间？
A: 深度模式需要执行10-20次API调用以获取全面的文献数据，包括初始搜索和引文扩展搜索。

### Q: 如何调整评分权重？
A: 目前权重是硬编码的（引用40%、相关度40%、时效性20%）。未来版本可能支持自定义权重。

### Q: 深度模式的文献池越大越好吗？
A: 不一定。文献池过大会引入不相关的文献，降低平均质量。当前设计（初始50篇，扩展到200-300篇）是平衡质量和效率的结果。

### Q: 速率限制会影响搜索速度吗？
A: 会，但影响很小。对于正常使用（<10次/秒），速率限制器几乎不会触发等待。只有在批量查询时才会生效。

---

## 总结

本次改进显著提升了MCP搜索服务器的功能：

1. ✅ **符合NCBI政策** - 实现速率限制保护
2. ✅ **三种搜索模式** - 适应不同使用场景
3. ✅ **智能排序** - 多维度评分系统
4. ✅ **向后兼容** - 不影响现有使用
5. ✅ **完整测试** - 验证所有功能

用户现在可以根据需求选择合适的搜索模式，从快速查询到深度研究，都能得到高质量的文献推荐。
