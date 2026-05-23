<div align="center">

# 🚀 APIForge-CLI

**轻量级终端HTTP API测试与智能文档生成引擎**

*Lightweight Terminal HTTP API Testing & Intelligent Documentation Generator*

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Zero-Dependencies-orange.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)]()

[简体中文](#简体中文) | [繁體中文](#繁體中文) | [English](#english)

</div>

---

## 简体中文

### 🎉 项目介绍

APIForge-CLI 是一款专为开发者打造的轻量级终端HTTP API测试工具，旨在解决日常API调试、测试和文档生成的痛点。它采用纯Python实现，**零依赖**，单文件即可运行，支持TUI交互界面和命令行双模式。

**灵感来源**：在日常开发中，我们经常需要使用Postman、Insomnia等重量级工具进行简单的API测试。APIForge-CLI提供了一个更轻量、更快速的替代方案，让API测试回归简单。

**自研差异化亮点**：
- ✅ 零依赖设计，单文件可运行
- ✅ 智能请求历史管理与复用
- ✅ 响应数据自动格式化与语法高亮
- ✅ 一键生成API文档（支持Markdown/OpenAPI 3.0）
- ✅ 兼容Postman/Insomnia集合导入导出

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🎯 **零依赖** | 纯Python标准库实现，无需安装任何第三方包 |
| 🖥️ **双模式** | 支持TUI交互界面和命令行模式 |
| 📚 **历史管理** | 自动保存请求历史，支持快速复用 |
| 🎨 **语法高亮** | JSON响应自动格式化与彩色显示 |
| 📝 **文档生成** | 一键生成Markdown/OpenAPI 3.0规范文档 |
| 📦 **集合导入** | 支持Postman/Insomnia集合导入 |
| 🌐 **多协议** | 支持HTTP/HTTPS，自动SSL处理 |
| ⚡ **轻量级** | 单文件<1000行代码，启动极速 |

### 🚀 快速开始

#### 环境要求

- Python 3.7 或更高版本
- 支持 Linux / macOS / Windows

#### 安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/apiforge-cli.git
cd apiforge-cli

# 直接运行（无需安装）
python apiforge.py

# 或添加到系统PATH
chmod +x apiforge.py
sudo cp apiforge.py /usr/local/bin/apiforge
```

#### 快速启动

```bash
# TUI交互模式
python apiforge.py tui

# 发送GET请求
python apiforge.py request https://api.github.com/users/gitstq

# 发送POST请求
python apiforge.py request -X POST \
  -H "Content-Type: application/json" \
  -d '{"name":"test"}' \
  https://httpbin.org/post

# 生成文档
python apiforge.py docs -f markdown -o api.md
```

### 📖 详细使用指南

#### TUI模式

启动TUI交互界面：

```bash
python apiforge.py tui
```

**菜单选项**：
1. **Send Request** - 发送HTTP请求
2. **View History** - 查看请求历史
3. **Manage Collections** - 管理集合（导入/导出）
4. **Environments** - 环境变量管理
5. **Generate Docs** - 生成API文档
6. **Settings** - 配置选项

#### 命令行模式

```bash
# 基本GET请求
apiforge request https://api.example.com/users

# 带Header的请求
apiforge request -H "Authorization: Bearer token" \
  https://api.example.com/profile

# POST请求
apiforge request -X POST \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com"}' \
  https://api.example.com/users

# 保存响应到文件
apiforge request -o response.json \
  https://api.example.com/data

# 查看历史记录
apiforge history

# 生成OpenAPI规范
apiforge docs -f openapi -o api.json
```

#### 支持的HTTP方法

- `GET` - 获取资源
- `POST` - 创建资源
- `PUT` - 更新资源
- `DELETE` - 删除资源
- `PATCH` - 部分更新
- `HEAD` - 获取响应头
- `OPTIONS` - 获取支持的方法

### 💡 设计思路与迭代规划

#### 设计理念

1. **极简主义**：去除不必要的功能，专注于核心API测试场景
2. **零依赖**：使用Python标准库，避免依赖地狱
3. **开发者优先**：命令行优先，TUI辅助，符合开发者使用习惯

#### 技术选型

- **Python 3.7+**：广泛兼容，标准库丰富
- **urllib**：标准库HTTP客户端，无需requests
- **json/curses**：标准库数据处理和终端控制

#### 后续迭代计划

- [ ] 环境变量模板支持
- [ ] 请求脚本化（支持预/后置处理）
- [ ] WebSocket支持
- [ ] 响应断言与测试套件
- [ ] CI/CD集成插件

### 📦 打包与部署

#### 打包为可执行文件

```bash
# 使用PyInstaller
pip install pyinstaller
pyinstaller --onefile apiforge.py

# 输出在 dist/apiforge
```

#### 作为Python包安装

```bash
# 创建setup.py后
pip install -e .
```

### 🤝 贡献指南

欢迎提交Issue和PR！请遵循以下规范：

1. **Issue**：描述问题、复现步骤、期望行为
2. **PR**：
   - 使用清晰的提交信息（遵循Conventional Commits）
   - 确保代码通过基础测试
   - 更新相关文档

### 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 繁體中文

### 🎉 專案介紹

APIForge-CLI 是一款專為開發者打造的輕量級終端HTTP API測試工具，旨在解決日常API除錯、測試和文件生成的痛點。它採用純Python實現，**零依賴**，單檔案即可執行，支援TUI互動介面和命令列雙模式。

**自研差異化亮點**：
- ✅ 零依賴設計，單檔案可執行
- ✅ 智慧請求歷史管理與復用
- ✅ 響應資料自動格式化與語法高亮
- ✅ 一鍵生成API文件（支援Markdown/OpenAPI 3.0）
- ✅ 相容Postman/Insomnia集合匯入匯出

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🎯 **零依賴** | 純Python標準庫實現，無需安裝任何第三方套件 |
| 🖥️ **雙模式** | 支援TUI互動介面和命令列模式 |
| 📚 **歷史管理** | 自動儲存請求歷史，支援快速復用 |
| 🎨 **語法高亮** | JSON響應自動格式化與彩色顯示 |
| 📝 **文件生成** | 一鍵生成Markdown/OpenAPI 3.0規範文件 |
| 📦 **集合匯入** | 支援Postman/Insomnia集合匯入 |

### 🚀 快速開始

#### 環境要求

- Python 3.7 或更高版本
- 支援 Linux / macOS / Windows

#### 安裝

```bash
# 克隆倉庫
git clone https://github.com/gitstq/apiforge-cli.git
cd apiforge-cli

# 直接執行（無需安裝）
python apiforge.py
```

#### 快速啟動

```bash
# TUI互動模式
python apiforge.py tui

# 傳送GET請求
python apiforge.py request https://api.github.com/users/gitstq

# 傳送POST請求
python apiforge.py request -X POST \
  -H "Content-Type: application/json" \
  -d '{"name":"test"}' \
  https://httpbin.org/post
```

### 📄 開源協議

本專案採用 [MIT License](LICENSE) 開源協議。

---

## English

### 🎉 Introduction

APIForge-CLI is a lightweight terminal HTTP API testing tool designed for developers to solve the pain points of daily API debugging, testing, and documentation generation. It is implemented in pure Python with **zero dependencies**, runs from a single file, and supports both TUI interactive interface and command-line modes.

**Differentiation Highlights**:
- ✅ Zero dependencies, single-file executable
- ✅ Smart request history management and reuse
- ✅ Automatic response formatting with syntax highlighting
- ✅ One-click API documentation generation (Markdown/OpenAPI 3.0)
- ✅ Compatible with Postman/Insomnia collection import/export

### ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🎯 **Zero Dependencies** | Pure Python standard library, no third-party packages |
| 🖥️ **Dual Mode** | TUI interactive interface and CLI mode |
| 📚 **History Management** | Auto-save request history with quick reuse |
| 🎨 **Syntax Highlighting** | JSON response auto-formatting with colors |
| 📝 **Doc Generation** | One-click Markdown/OpenAPI 3.0 spec generation |
| 📦 **Collection Import** | Import from Postman/Insomnia |

### 🚀 Quick Start

#### Requirements

- Python 3.7 or higher
- Supports Linux / macOS / Windows

#### Installation

```bash
# Clone repository
git clone https://github.com/gitstq/apiforge-cli.git
cd apiforge-cli

# Run directly (no installation needed)
python apiforge.py
```

#### Quick Launch

```bash
# TUI interactive mode
python apiforge.py tui

# Send GET request
python apiforge.py request https://api.github.com/users/gitstq

# Send POST request
python apiforge.py request -X POST \
  -H "Content-Type: application/json" \
  -d '{"name":"test"}' \
  https://httpbin.org/post
```

### 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

**Made with ❤️ by APIForge Team**

[Report Bug](https://github.com/gitstq/apiforge-cli/issues) · [Request Feature](https://github.com/gitstq/apiforge-cli/issues)

</div>
