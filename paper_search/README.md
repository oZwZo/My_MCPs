# MCP Research Workflow Server

本地 MCP 服务器，用于科研文献搜索（PubMed 和 Google Scholar）。

适用于 **Claude Code CLI** 和 **Claude Desktop**。

## 快速开始

### 1. 安装完成 ✓

已通过 uv 安装：
- Python 3.12.12
- MCP SDK 1.26.0
- httpx 0.28.1

### 2. 配置 API Keys

编辑 `api_key.json` 文件：

```bash
nano api_key.json
# 或使用任何文本编辑器
```

填入您的 API Keys：

```json
{
  "NCBI_API_KEY": "你的真实NCBI_API_KEY",
  "NCBI_EMAIL": "your_email@example.com",
  "SERPAPI_KEY": "你的真实SERPAPI_KEY"
}
```

**获取 API Keys：**
- **NCBI API Key**: https://www.ncbi.nlm.nih.gov/account/
  - 登录后 → Settings → API Key Management → Create API Key
- **SerpApi Key**: https://serpapi.com/users/sign_up
  - 注册后会在 Dashboard 显示

### 3. Claude Code CLI 配置 ✓

配置文件已创建：`~/.config/claude-code/config.json`

**重启您的终端或重新加载配置**

### 4. Claude Desktop 配置（可选）

如果您也使用 Claude Desktop，编辑配置文件：

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

添加以下配置：

```json
{
  "mcpServers": {
    "research-workflow": {
      "command": "/Users/wergilius/Documents/My_MCPs/.venv/bin/python",
      "args": ["/Users/wergilius/Documents/My_MCPs/mcp_server.py"]
    }
  }
}
```

## 使用方法

### 在 Claude Code 中

```
搜索 PubMed 关于 "hematopoietic stem cell heterogeneity" 的文献
```

```
使用 Google Scholar 搜索 "CRISPR gene editing" 的最新研究
```

### 工具说明

#### search_pubmed
搜索 PubMed 数据库，返回最相关的文献

**参数：**
- `query` (必需): 搜索查询词
- `max_results` (可选): 返回结果数量，默认 10，最大 100

**返回：**
- 标题
- PMID
- 作者
- 期刊
- 发表日期
- 引用信息

#### search_scholar
搜索 Google Scholar，支持三种搜索模式

**参数：**
- `query` (必需): 搜索查询词
- `mode` (可选): 搜索模式
  - `quick`: 快速模式，返回前10篇文献（默认）
  - `relevance`: 相关度优化模式，从前200篇文献中选择最相关的
  - `deep`: 深度查找模式，基于引文扩展搜索，并根据引用次数、相关度、发表时间综合排序，返回前5篇最优文献
- `num_results` (可选): 返回结果数量（默认: quick模式10篇，deep模式5篇）

**返回：**
- 标题
- 摘要
- 链接
- 作者
- 年份
- 期刊
- 引用次数
- deep模式下还会显示评分详情（引用度、相关度、时效性、总分）

**搜索模式详解：**

1. **快速模式 (quick)**
   - 最快的搜索方式
   - 直接返回前10篇文献
   - 适合快速浏览和初步调研

2. **相关度优化模式 (relevance)**
   - 搜索前200篇文献
   - 根据Google Scholar的相关性排序选择最相关的文献
   - 适合需要更全面相关文献的场景

3. **深度查找模式 (deep)**
   - 执行步骤：
     1. 使用相关度优化模式获取初始文献集
     2. 筛选最相关的文献用于引文分析
     3. 提取关键词进行引文扩展搜索
     4. 在扩大的文献池中根据三个指标评分：
        - **引用程度** (40%权重): 被引用次数越多分数越高
        - **相关度** (40%权重): 与查询的相关性
        - **发表时间** (20%权重): 越新的文献分数越高
   - 返回综合评分最高的5篇文献
   - 适合需要高质量、高影响力文献的深入研究

**特别说明：**
- NCBI PubMed API已添加速率限制（10次/秒），符合NCBI使用政策
- deep模式会进行多次API调用以获取更全面的结果，可能需要较长时间

## 手动测试

激活虚拟环境并运行服务器：

```bash
source activate.sh
python mcp_server.py
```

## 文件结构

```
My_MCPs/
├── mcp_server.py           # MCP 服务器主程序
├── api_key.json            # API Keys 配置（不提交到 git）
├── api_key.json.example    # API Keys 模板
├── requirements.txt        # Python 依赖
├── activate.sh             # 虚拟环境激活脚本
├── .gitignore              # Git 忽略规则
├── .venv/                  # Python 虚拟环境
└── README.md               # 本文档
```

## 安全注意事项

⚠️ **重要**: `api_key.json` 已在 `.gitignore` 中，不会被提交到 git

请勿：
- ❌ 将 `api_key.json` 提交到版本控制
- ❌ 在公开场合分享您的 API Keys

建议：
- ✅ 定期更换 API Keys
- ✅ 使用不同的邮箱用于开发和生产环境
- ✅ 监控 API 使用量，避免超额

## 配置优先级

API Keys 的加载优先级：

1. **环境变量** (最高优先级)
2. **api_key.json 配置文件**
3. **代码中的默认值** (最低优先级)

如果您在 `claude_desktop_config.json` 中设置了环境变量，会覆盖 `api_key.json` 中的值。

## 故障排除

### 1. Claude Code 找不到 MCP 服务器

检查配置文件路径：
```bash
cat ~/.config/claude-code/config.json
```

确认 Python 路径正确：
```bash
ls -la /Users/wergilius/Documents/My_MCPs/.venv/bin/python
```

### 2. API 调用失败

检查 API Keys 是否正确配置：
```bash
cat api_key.json
```

测试网络连接：
```bash
curl -I https://eutils.ncbi.nlm.nih.gov/
curl -I https://serpapi.com/
```

### 3. 依赖问题

重新安装依赖：
```bash
/Users/wergilius/.local/bin/uv pip install --reinstall mcp httpx
```

## 技术栈

- **Python**: 3.12.12（通过 uv 管理）
- **MCP SDK**: 1.26.0 (Model Context Protocol)
- **HTTP 客户端**: httpx 0.28.1
- **APIs**:
  - NCBI E-utilities (PubMed)
  - SerpApi (Google Scholar)

## 更新日志

### v2.0 (2025-01-27)
- ✅ 添加 NCBI API 速率限制（10次/秒），符合使用政策
- ✅ 实现 Google Scholar 三种搜索模式：
  - 快速模式：返回前10篇文献
  - 相关度优化模式：从前200篇中选择最相关的
  - 深度查找模式：基于引文扩展，多指标综合排序
- ✅ 深度模式支持三维度评分：引用度、相关度、时效性
- ✅ 改进错误处理和结果格式化

### v1.0 (2025-01-27)
- ✅ 实现 PubMed 搜索工具
- ✅ 实现 Google Scholar 搜索工具
- ✅ 支持从 `api_key.json` 读取配置
- ✅ 兼容 Claude Code CLI 和 Claude Desktop
- ✅ 添加配置文件模板和安全保护
