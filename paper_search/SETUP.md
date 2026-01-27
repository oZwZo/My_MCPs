# 快速设置指南

## ✅ 已完成

1. ✓ Python 3.12.12 虚拟环境已创建（`.venv/`）
2. ✓ MCP SDK 和依赖已安装
3. ✓ `api_key.json` 配置文件已创建
4. ✓ Claude Code CLI 配置已创建（`~/.config/claude-code/config.json`）
5. ✓ 服务器代码已修改，支持从 `api_key.json` 读取配置
6. ✓ `.gitignore` 已配置，保护 API Keys

## 🔧 您需要做的

### 步骤 1: 获取 API Keys

1. **NCBI API Key**:
   - 访问 https://www.ncbi.nlm.nih.gov/account/
   - 注册/登录账号
   - Settings → API Key Management → Create API Key

2. **SerpApi Key**:
   - 访问 https://serpapi.com/users/sign_up
   - 注册账号
   - 在 Dashboard 复制 API Key

### 步骤 2: 编辑 api_key.json

```bash
cd /Users/wergilius/Documents/My_MCPs
nano api_key.json
```

将以下内容替换为您的真实 keys：

```json
{
  "NCBI_API_KEY": "您的NCBI_API_KEY",
  "NCBI_EMAIL": "your_email@example.com",
  "SERPAPI_KEY": "您的SERPAPI_KEY"
}
```

保存并退出（Ctrl+O, Enter, Ctrl+X）

### 步骤 3: 测试服务器

```bash
source activate.sh
python mcp_server.py
```

如果看到服务器运行信息，说明配置成功！按 Ctrl+C 退出。

### 步骤 4: 重启 Claude Code

关闭并重新打开 Claude Code CLI

## 📝 测试命令

在 Claude Code 中尝试：

```
搜索 PubMed 关于 "CRISPR" 的文献
```

```
使用 Google Scholar 搜索 "machine learning in healthcare"
```

## 📂 文件位置

| 文件 | 路径 |
|------|------|
| 服务器代码 | `/Users/wergilius/Documents/My_MCPs/mcp_server.py` |
| API Keys | `/Users/wergilius/Documents/My_MCPs/api_key.json` |
| Claude Code 配置 | `~/.config/claude-code/config.json` |
| Python 虚拟环境 | `/Users/wergilius/Documents/My_MCPs/.venv/` |

## 🔐 安全提醒

- ⚠️ `api_key.json` 包含敏感信息，请勿分享
- ⚠️ `.gitignore` 已配置，不会提交到 git
- ✅ 定期检查 API 使用量，避免超额费用

## ❓ 需要帮助？

查看完整文档：`README.md`
