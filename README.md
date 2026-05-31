<p align="center">
  <img src="https://img.shields.io/badge/version-v1.0.0-blue.svg" alt="Version" />
  <img src="https://img.shields.io/badge/python-3.9+-green.svg" alt="Python" />
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License" />
  <img src="https://img.shields.io/badge/tests-84%20passed-success.svg" alt="Tests" />
  <img src="https://img.shields.io/badge/templates-20%2B-purple.svg" alt="Templates" />
</p>

<p align="center">
  <strong>AgentForge Studio</strong> — 轻量级终端 AI Agent 技能工厂与团队编排引擎
</p>

<p align="center">
  <a href="#简体中文">简体中文</a> |
  <a href="#繁體中文">繁體中文</a> |
  <a href="#english">English</a> |
  <a href="#日本語">日本語</a> |
  <a href="#한국어">한국어</a> |
  <a href="#español">Español</a>
</p>

---

<a name="简体中文"></a>

# 🎉 AgentForge Studio

> 用终端打造你的 AI Agent 军团 —— 轻量、高效、开箱即用。

AgentForge Studio 是一个运行在终端中的 AI Agent 技能工厂与团队编排引擎。它让你能够像搭积木一样创建、管理和编排 AI Agent 技能，并通过 DAG 依赖图实现多 Agent 团队协作。无需复杂配置，一条命令即可启动你的 AI 工坊。

**GitHub:** [https://github.com/gitstq/AgentForge-Studio](https://github.com/gitstq/AgentForge-Studio)

---

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 🛠️ **技能管理** | 创建、编辑、测试、导出 AI Agent 技能，完整生命周期管理 |
| 🤖 **Agent 管理** | 创建 Agent 并灵活分配技能，打造专属 AI 助手 |
| 🔄 **团队编排** | 基于 DAG 依赖图编排多 Agent 团队协作，支持可视化 |
| 📋 **20+ 内置模板** | 代码审查、文档生成、安全扫描、数据分析等开箱即用 |
| 📤 **MCP 导出** | 技能一键导出为 MCP Server 格式，无缝对接 LLM 生态 |
| 🧪 **测试沙箱** | 独立测试每个技能，确保质量可靠 |
| 📊 **TUI 仪表盘** | Rich 终端交互界面，信息一目了然 |
| ✅ **84 个单元测试** | 全部通过，代码质量有保障 |

---

## 🚀 快速开始

### 📋 环境要求

- Python 3.9 或更高版本
- pip 包管理器
- 终端（推荐支持 256 色的终端以获得最佳体验）

### 🔧 安装步骤

```bash
# 克隆项目
git clone https://github.com/gitstq/AgentForge-Studio.git
cd AgentForge-Studio

# 安装依赖
pip install -r requirements.txt

# 安装项目（可选，注册 agentforge 命令）
pip install -e .
```

### 🎮 使用命令

```bash
# 查看版本
agentforge --version

# 初始化项目
agentforge init

# 启动 TUI 仪表盘
agentforge dashboard
```

---

## 📖 详细使用指南

### 🛠️ 技能管理

技能是 AgentForge 的核心构建单元。每个技能定义了 AI Agent 可以执行的具体能力。

```bash
# 创建新技能
agentforge skill create my-reviewer \
  --description "代码审查专家" \
  --instructions "你是一位资深代码审查专家，请仔细审查代码质量..."

# 查看所有技能
agentforge skill list

# 查看技能详情
agentforge skill show my-reviewer

# 测试技能
agentforge skill test my-reviewer

# 导出技能为 MCP 格式
agentforge skill export my-reviewer --format mcp --output my-reviewer.json
```

### 🤖 Agent 管理

Agent 是技能的载体，你可以为每个 Agent 分配不同的技能组合。

```bash
# 创建 Agent
agentforge agent create senior-dev \
  --role "高级开发工程师" \
  --system-prompt "你是一位经验丰富的高级开发工程师..." \
  --model gpt-4

# 查看所有 Agent
agentforge agent list

# 为 Agent 分配技能
agentforge agent assign senior-dev my-reviewer
```

### 🔄 团队编排

通过 DAG（有向无环图）依赖关系编排多个 Agent 协同工作。

```bash
# 创建团队
agentforge team create dev-team --description "开发流水线团队"

# 添加 Agent 到团队（支持依赖声明）
agentforge team add dev-team code-reviewer
agentforge team add dev-team bug-fixer --depends-on code-reviewer
agentforge team add dev-team test-gen --depends-on bug-fixer

# 可视化团队 DAG 结构
agentforge team visualize dev-team

# 执行团队编排
agentforge team run dev-team
```

### 📋 模板使用

AgentForge 内置了 20+ 个精心设计的技能模板，覆盖开发全流程：

| 模板名 | 用途 |
|--------|------|
| `code-review` | 代码审查，检测 Bug 和质量问题 |
| `doc-generator` | 从源码或描述生成文档 |
| `data-analyst` | 数据分析与洞察生成 |
| `api-tester` | API 端点测试用例生成 |
| `security-scanner` | 安全漏洞扫描（OWASP Top 10） |
| `code-refactorer` | 代码重构与优化 |
| `translator` | 多语言翻译 |
| `summarizer` | 文本摘要生成 |
| `bug-fixer` | Bug 定位与修复 |
| `perf-optimizer` | 性能优化建议 |
| `test-generator` | 单元测试与集成测试生成 |
| `code-explainer` | 代码解释与说明 |
| `req-analyst` | 需求分析与结构化 |
| `arch-designer` | 架构设计与模式推荐 |
| `project-manager` | 项目规划与管理 |
| `code-migrator` | 跨语言代码迁移 |
| `config-manager` | 配置文件生成与管理 |
| `log-analyst` | 日志分析与故障排查 |
| `deploy-helper` | 部署配置与 CI/CD 生成 |
| `monitor-analyst` | 监控与可观测性方案设计 |

```bash
# 查看所有可用模板
agentforge template list

# 基于模板创建技能
agentforge template apply code-review my-custom-reviewer
```

### 📤 导出功能

将技能导出为标准 MCP Server 格式，无缝接入 Claude Desktop、Cursor 等 LLM 客户端。

```bash
# 导出单个技能
agentforge skill export my-skill --format mcp --output skill.json

# 导出后可直接用于 MCP 客户端配置
```

---

## 💡 设计思路与迭代规划

### 🎯 设计理念

AgentForge Studio 的核心设计理念是 **"技能即积木，Agent 即工匠，团队即工厂"**：

- **技能层（Skill）**：定义原子化的 AI 能力单元，包含指令、参数、输入输出规范
- **Agent 层**：将技能组合赋予特定角色，形成专业化的 AI 助手
- **团队层（Team）**：通过 DAG 依赖图编排 Agent 执行顺序，实现复杂工作流

### 🗺️ 迭代规划

- **v1.0** ✅ — 核心功能：技能管理、Agent 管理、团队编排、MCP 导出、TUI 仪表盘
- **v1.1** 🔜 — 可视化 DAG 编辑器、技能市场、团队模板
- **v1.2** 🔜 — 分布式执行引擎、Web Dashboard、插件系统
- **v2.0** 🔮 — 多模态技能支持、AutoML 集成、企业级权限管理

---

## 📦 安装与部署指南

### 🐍 从源码安装

```bash
git clone https://github.com/gitstq/AgentForge-Studio.git
cd AgentForge-Studio
pip install -e ".[tui]"
```

### 🧪 开发环境

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=agentforge
```

### 📁 项目结构

```
AgentForge-Studio/
├── agentforge/           # 核心代码
│   ├── core/             # 核心模型（Skill, Agent, Team, Engine）
│   ├── export/           # MCP 导出模块
│   ├── sandbox/          # 测试沙箱
│   ├── templates/        # 内置模板
│   ├── tui/              # TUI 仪表盘
│   ├── utils/            # 工具函数
│   └── cli.py            # CLI 入口
├── tests/                # 单元测试（84 个）
├── pyproject.toml        # 项目配置
├── requirements.txt      # 依赖列表
└── LICENSE               # MIT 协议
```

---

## 🤝 贡献指南

我们欢迎各种形式的贡献！无论是提交 Bug、改进文档，还是贡献新功能。

### 📝 贡献流程

1. **Fork** 本仓库
2. 创建特性分支：`git checkout -b feature/amazing-feature`
3. 提交更改：`git commit -m 'Add some amazing feature'`
4. 推送到远程：`git push origin feature/amazing-feature`
5. 提交 **Pull Request**

### 📋 开发规范

- 遵循 PEP 8 编码规范
- 所有新功能必须附带单元测试
- 提交信息遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范
- 确保所有测试通过后再提交 PR

---

## 📄 开源协议

本项目基于 [MIT License](https://opensource.org/licenses/MIT) 开源。

```
MIT License

Copyright (c) 2024 AgentForge Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

<p align="center">
  用 ❤️ 构建 | AgentForge Studio
</p>

---

<a name="繁體中文"></a>

# 🎉 AgentForge Studio

> 在終端打造你的 AI Agent 軍團 —— 輕量、高效、開箱即用。

AgentForge Studio 是一個運行在終端中的 AI Agent 技能工廠與團隊編排引擎。它讓你能夠像搭積木一樣創建、管理和編排 AI Agent 技能，並透過 DAG 依賴圖實現多 Agent 團隊協作。無需複雜配置，一條命令即可啟動你的 AI 工坊。

**GitHub:** [https://github.com/gitstq/AgentForge-Studio](https://github.com/gitstq/AgentForge-Studio)

---

## ✨ 核心特性

| 特性 | 說明 |
|------|------|
| 🛠️ **技能管理** | 建立、編輯、測試、匯出 AI Agent 技能，完整生命週期管理 |
| 🤖 **Agent 管理** | 建立 Agent 並靈活分配技能，打造專屬 AI 助手 |
| 🔄 **團隊編排** | 基於 DAG 依賴圖編排多 Agent 團隊協作，支援視覺化 |
| 📋 **20+ 內建模板** | 程式碼審查、文件生成、安全掃描、資料分析等開箱即用 |
| 📤 **MCP 匯出** | 技能一鍵匯出為 MCP Server 格式，無縫對接 LLM 生態 |
| 🧪 **測試沙箱** | 獨立測試每個技能，確保品質可靠 |
| 📊 **TUI 儀表板** | Rich 終端互動介面，資訊一目了然 |
| ✅ **84 個單元測試** | 全部通過，程式碼品質有保障 |

---

## 🚀 快速開始

### 📋 環境需求

- Python 3.9 或更高版本
- pip 套件管理器
- 終端（建議支援 256 色的終端以獲得最佳體驗）

### 🔧 安裝步驟

```bash
# 複製專案
git clone https://github.com/gitstq/AgentForge-Studio.git
cd AgentForge-Studio

# 安裝依賴
pip install -r requirements.txt

# 安裝專案（可選，註冊 agentforge 命令）
pip install -e .
```

### 🎮 使用命令

```bash
# 查看版本
agentforge --version

# 初始化專案
agentforge init

# 啟動 TUI 儀表板
agentforge dashboard
```

---

## 📖 詳細使用指南

### 🛠️ 技能管理

技能是 AgentForge 的核心建構單元。每個技能定義了 AI Agent 可以執行的具體能力。

```bash
# 建立新技能
agentforge skill create my-reviewer \
  --description "程式碼審查專家" \
  --instructions "你是一位資深程式碼審查專家，請仔細審查程式碼品質..."

# 查看所有技能
agentforge skill list

# 查看技能詳情
agentforge skill show my-reviewer

# 測試技能
agentforge skill test my-reviewer

# 匯出技能為 MCP 格式
agentforge skill export my-reviewer --format mcp --output my-reviewer.json
```

### 🤖 Agent 管理

Agent 是技能的載體，你可以為每個 Agent 分配不同的技能組合。

```bash
# 建立 Agent
agentforge agent create senior-dev \
  --role "高級開發工程師" \
  --system-prompt "你是一位經驗豐富的高級開發工程師..." \
  --model gpt-4

# 查看所有 Agent
agentforge agent list

# 為 Agent 分配技能
agentforge agent assign senior-dev my-reviewer
```

### 🔄 團隊編排

透過 DAG（有向無環圖）依賴關係編排多個 Agent 協同工作。

```bash
# 建立團隊
agentforge team create dev-team --description "開發流水線團隊"

# 新增 Agent 到團隊（支援依賴宣告）
agentforge team add dev-team code-reviewer
agentforge team add dev-team bug-fixer --depends-on code-reviewer
agentforge team add dev-team test-gen --depends-on bug-fixer

# 視覺化團隊 DAG 結構
agentforge team visualize dev-team

# 執行團隊編排
agentforge team run dev-team
```

### 📋 模板使用

AgentForge 內建了 20+ 個精心設計的技能模板，涵蓋開發全流程：

| 模板名稱 | 用途 |
|----------|------|
| `code-review` | 程式碼審查，偵測 Bug 和品質問題 |
| `doc-generator` | 從原始碼或描述生成文件 |
| `data-analyst` | 資料分析與洞察生成 |
| `api-tester` | API 端點測試案例生成 |
| `security-scanner` | 安全漏洞掃描（OWASP Top 10） |
| `code-refactorer` | 程式碼重構與最佳化 |
| `translator` | 多語言翻譯 |
| `summarizer` | 文字摘要生成 |
| `bug-fixer` | Bug 定位與修復 |
| `perf-optimizer` | 效能最佳化建議 |
| `test-generator` | 單元測試與整合測試生成 |
| `code-explainer` | 程式碼解釋與說明 |
| `req-analyst` | 需求分析與結構化 |
| `arch-designer` | 架構設計與模式推薦 |
| `project-manager` | 專案規劃與管理 |
| `code-migrator` | 跨語言程式碼遷移 |
| `config-manager` | 設定檔生成與管理 |
| `log-analyst` | 日誌分析與故障排查 |
| `deploy-helper` | 部署設定與 CI/CD 生成 |
| `monitor-analyst` | 監控與可觀測性方案設計 |

```bash
# 查看所有可用模板
agentforge template list

# 基於模板建立技能
agentforge template apply code-review my-custom-reviewer
```

### 📤 匯出功能

將技能匯出為標準 MCP Server 格式，無縫接入 Claude Desktop、Cursor 等 LLM 客戶端。

```bash
# 匯出單一技能
agentforge skill export my-skill --format mcp --output skill.json

# 匯出後可直接用於 MCP 客戶端設定
```

---

## 💡 設計思路與迭代規劃

### 🎯 設計理念

AgentForge Studio 的核心設計理念是 **「技能即積木，Agent 即工匠，團隊即工廠」**：

- **技能層（Skill）**：定義原子化的 AI 能力單元，包含指令、參數、輸入輸出規範
- **Agent 層**：將技能組合賦予特定角色，形成專業化的 AI 助手
- **團隊層（Team）**：透過 DAG 依賴圖編排 Agent 執行順序，實現複雜工作流

### 🗺️ 迭代規劃

- **v1.0** ✅ — 核心功能：技能管理、Agent 管理、團隊編排、MCP 匯出、TUI 儀表板
- **v1.1** 🔜 — 視覺化 DAG 編輯器、技能市場、團隊模板
- **v1.2** 🔜 — 分散式執行引擎、Web Dashboard、外掛系統
- **v2.0** 🔮 — 多模態技能支援、AutoML 整合、企業級權限管理

---

## 📦 安裝與部署指南

### 🐍 從原始碼安裝

```bash
git clone https://github.com/gitstq/AgentForge-Studio.git
cd AgentForge-Studio
pip install -e ".[tui]"
```

### 🧪 開發環境

```bash
# 安裝開發依賴
pip install -e ".[dev]"

# 執行測試
pytest

# 執行測試並生成覆蓋率報告
pytest --cov=agentforge
```

### 📁 專案結構

```
AgentForge-Studio/
├── agentforge/           # 核心程式碼
│   ├── core/             # 核心模型（Skill, Agent, Team, Engine）
│   ├── export/           # MCP 匯出模組
│   ├── sandbox/          # 測試沙箱
│   ├── templates/        # 內建模板
│   ├── tui/              # TUI 儀表板
│   ├── utils/            # 工具函式
│   └── cli.py            # CLI 入口
├── tests/                # 單元測試（84 個）
├── pyproject.toml        # 專案設定
├── requirements.txt      # 依賴清單
└── LICENSE               # MIT 授權
```

---

## 🤝 貢獻指南

我們歡迎各種形式的貢獻！無論是提交 Bug、改善文件，還是貢獻新功能。

### 📝 貢獻流程

1. **Fork** 本倉庫
2. 建立特性分支：`git checkout -b feature/amazing-feature`
3. 提交變更：`git commit -m 'Add some amazing feature'`
4. 推送到遠端：`git push origin feature/amazing-feature`
5. 提交 **Pull Request**

### 📋 開發規範

- 遵循 PEP 8 編碼規範
- 所有新功能必須附帶單元測試
- 提交訊息遵循 [Conventional Commits](https://www.conventionalcommits.org/) 規範
- 確保所有測試通過後再提交 PR

---

## 📄 開源協議

本專案基於 [MIT License](https://opensource.org/licenses/MIT) 開源。

```
MIT License

Copyright (c) 2024 AgentForge Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

<p align="center">
  用 ❤️ 打造 | AgentForge Studio
</p>

---

<a name="english"></a>

# 🎉 AgentForge Studio

> Build your AI Agent army right from the terminal — lightweight, efficient, and ready to go.

AgentForge Studio is a terminal-based AI Agent skill factory and team orchestration engine. It empowers you to create, manage, and orchestrate AI Agent skills as easily as building blocks, and coordinate multi-Agent team collaboration through DAG dependency graphs. No complex setup needed — launch your AI workshop with a single command.

**GitHub:** [https://github.com/gitstq/AgentForge-Studio](https://github.com/gitstq/AgentForge-Studio)

---

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🛠️ **Skill Management** | Create, edit, test, and export AI Agent skills with full lifecycle management |
| 🤖 **Agent Management** | Create Agents and flexibly assign skills to build your custom AI assistants |
| 🔄 **Team Orchestration** | Orchestrate multi-Agent team collaboration via DAG dependency graphs with visualization |
| 📋 **20+ Built-in Templates** | Code review, documentation generation, security scanning, data analysis, and more — ready to use |
| 📤 **MCP Export** | One-click export to MCP Server format for seamless integration with the LLM ecosystem |
| 🧪 **Test Sandbox** | Test each skill independently to ensure quality and reliability |
| 📊 **TUI Dashboard** | Rich terminal interactive interface for a clear overview at a glance |
| ✅ **84 Unit Tests** | All passing — code quality you can count on |

---

## 🚀 Quick Start

### 📋 Prerequisites

- Python 3.9 or higher
- pip package manager
- A terminal (256-color support recommended for the best experience)

### 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/gitstq/AgentForge-Studio.git
cd AgentForge-Studio

# Install dependencies
pip install -r requirements.txt

# Install the project (optional, registers the agentforge command)
pip install -e .
```

### 🎮 Usage

```bash
# Check version
agentforge --version

# Initialize a project
agentforge init

# Launch the TUI dashboard
agentforge dashboard
```

---

## 📖 Detailed Guide

### 🛠️ Skill Management

Skills are the fundamental building blocks of AgentForge. Each skill defines a specific capability that an AI Agent can execute.

```bash
# Create a new skill
agentforge skill create my-reviewer \
  --description "Code review expert" \
  --instructions "You are a senior code reviewer, please carefully review code quality..."

# List all skills
agentforge skill list

# Show skill details
agentforge skill show my-reviewer

# Test a skill
agentforge skill test my-reviewer

# Export a skill to MCP format
agentforge skill export my-reviewer --format mcp --output my-reviewer.json
```

### 🤖 Agent Management

Agents are the carriers of skills. You can assign different skill combinations to each Agent.

```bash
# Create an Agent
agentforge agent create senior-dev \
  --role "Senior Developer" \
  --system-prompt "You are an experienced senior developer..." \
  --model gpt-4

# List all Agents
agentforge agent list

# Assign a skill to an Agent
agentforge agent assign senior-dev my-reviewer
```

### 🔄 Team Orchestration

Coordinate multiple Agents working together through DAG (Directed Acyclic Graph) dependency relationships.

```bash
# Create a team
agentforge team create dev-team --description "Development pipeline team"

# Add Agents to the team (with dependency declarations)
agentforge team add dev-team code-reviewer
agentforge team add dev-team bug-fixer --depends-on code-reviewer
agentforge team add dev-team test-gen --depends-on bug-fixer

# Visualize the team DAG structure
agentforge team visualize dev-team

# Execute team orchestration
agentforge team run dev-team
```

### 📋 Templates

AgentForge comes with 20+ carefully crafted skill templates covering the entire development lifecycle:

| Template | Purpose |
|----------|---------|
| `code-review` | Code review — detect bugs and quality issues |
| `doc-generator` | Generate documentation from source code or descriptions |
| `data-analyst` | Data analysis and insight generation |
| `api-tester` | API endpoint test case generation |
| `security-scanner` | Security vulnerability scanning (OWASP Top 10) |
| `code-refactorer` | Code refactoring and optimization |
| `translator` | Multi-language translation |
| `summarizer` | Text summarization |
| `bug-fixer` | Bug identification and fixing |
| `perf-optimizer` | Performance optimization suggestions |
| `test-generator` | Unit and integration test generation |
| `code-explainer` | Code explanation and documentation |
| `req-analyst` | Requirements analysis and structuring |
| `arch-designer` | Architecture design and pattern recommendations |
| `project-manager` | Project planning and management |
| `code-migrator` | Cross-language code migration |
| `config-manager` | Configuration file generation and management |
| `log-analyst` | Log analysis and troubleshooting |
| `deploy-helper` | Deployment configuration and CI/CD generation |
| `monitor-analyst` | Monitoring and observability solution design |

```bash
# List all available templates
agentforge template list

# Create a skill from a template
agentforge template apply code-review my-custom-reviewer
```

### 📤 Export

Export skills to the standard MCP Server format for seamless integration with LLM clients like Claude Desktop and Cursor.

```bash
# Export a single skill
agentforge skill export my-skill --format mcp --output skill.json

# The exported file can be used directly in MCP client configuration
```

---

## 💡 Design Philosophy & Roadmap

### 🎯 Design Philosophy

The core design philosophy of AgentForge Studio is **"Skills as building blocks, Agents as craftsmen, Teams as factories"**:

- **Skill Layer**: Defines atomic AI capability units with instructions, parameters, and I/O specifications
- **Agent Layer**: Combines skills and assigns them to specific roles, creating specialized AI assistants
- **Team Layer**: Orchestrates Agent execution order through DAG dependency graphs for complex workflows

### 🗺️ Roadmap

- **v1.0** ✅ — Core features: skill management, Agent management, team orchestration, MCP export, TUI dashboard
- **v1.1** 🔜 — Visual DAG editor, skill marketplace, team templates
- **v1.2** 🔜 — Distributed execution engine, Web Dashboard, plugin system
- **v2.0** 🔮 — Multi-modal skill support, AutoML integration, enterprise-grade permission management

---

## 📦 Installation & Deployment

### 🐍 Install from Source

```bash
git clone https://github.com/gitstq/AgentForge-Studio.git
cd AgentForge-Studio
pip install -e ".[tui]"
```

### 🧪 Development Setup

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage report
pytest --cov=agentforge
```

### 📁 Project Structure

```
AgentForge-Studio/
├── agentforge/           # Core source code
│   ├── core/             # Core models (Skill, Agent, Team, Engine)
│   ├── export/           # MCP export module
│   ├── sandbox/          # Test sandbox
│   ├── templates/        # Built-in templates
│   ├── tui/              # TUI dashboard
│   ├── utils/            # Utility functions
│   └── cli.py            # CLI entry point
├── tests/                # Unit tests (84 tests)
├── pyproject.toml        # Project configuration
├── requirements.txt      # Dependency list
└── LICENSE               # MIT License
```

---

## 🤝 Contributing

We welcome contributions of all kinds! Whether it's filing a bug, improving documentation, or contributing new features.

### 📝 Contribution Workflow

1. **Fork** this repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the remote: `git push origin feature/amazing-feature`
5. Submit a **Pull Request**

### 📋 Development Standards

- Follow PEP 8 coding conventions
- All new features must include unit tests
- Commit messages should follow the [Conventional Commits](https://www.conventionalcommits.org/) specification
- Ensure all tests pass before submitting a PR

---

## 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

```
MIT License

Copyright (c) 2024 AgentForge Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

<p align="center">
  Built with ❤️ | AgentForge Studio
</p>

---

<a name="日本語"></a>

# 🎉 AgentForge Studio

> ターミナルで AI Agent 軍団を構築 —— 軽量・高效・すぐに使えます。

AgentForge Studio は、ターミナル上で動作する AI Agent スキルファクトリー＆チームオーケストレーションエンジンです。ブロックを組み立てるように AI Agent スキルを作成・管理・オーケストレーションでき、DAG 依存関係グラフを通じて複数 Agent のチームコラボレーションを実現します。複雑な設定は不要、コマンド一つで AI ワークショップを始められます。

**GitHub:** [https://github.com/gitstq/AgentForge-Studio](https://github.com/gitstq/AgentForge-Studio)

---

## ✨ 主な機能

| 機能 | 説明 |
|------|------|
| 🛠️ **スキル管理** | AI Agent スキルの作成・編集・テスト・エクスポート、ライフサイクル全体を管理 |
| 🤖 **Agent 管理** | Agent を作成し、スキルを柔軟に割り当てて専用 AI アシスタントを構築 |
| 🔄 **チームオーケストレーション** | DAG 依存関係グラフで複数 Agent のチームコラボレーションを編成、可視化対応 |
| 📋 **20+ 組み込みテンプレート** | コードレビュー、ドキュメント生成、セキュリティスキャン、データ分析など即座に利用可能 |
| 📤 **MCP エクスポート** | スキルをワンクリックで MCP Server 形式にエクスポート、LLM エコシステムとシームレス連携 |
| 🧪 **テストサンドボックス** | 各スキルを独立してテスト、品質と信頼性を確保 |
| 📊 **TUI ダッシュボード** | Rich ターミナルインタラクティブインターフェースで情報を一目で把握 |
| ✅ **84 のユニットテスト** | 全て合格、コード品質を保証 |

---

## 🚀 クイックスタート

### 📋 動作環境

- Python 3.9 以上
- pip パッケージマネージャー
- ターミナル（256色対応を推奨、最適な体験を提供）

### 🔧 インストール手順

```bash
# リポジトリをクローン
git clone https://github.com/gitstq/AgentForge-Studio.git
cd AgentForge-Studio

# 依存関係をインストール
pip install -r requirements.txt

# プロジェクトをインストール（任意、agentforge コマンドを登録）
pip install -e .
```

### 🎮 基本的な使い方

```bash
# バージョン確認
agentforge --version

# プロジェクトを初期化
agentforge init

# TUI ダッシュボードを起動
agentforge dashboard
```

---

## 📖 詳細ガイド

### 🛠️ スキル管理

スキルは AgentForge の基本構成単位です。各スキルは AI Agent が実行できる具体的な能力を定義します。

```bash
# 新しいスキルを作成
agentforge skill create my-reviewer \
  --description "コードレビュー専門家" \
  --instructions "あなたはシニアコードレビュアーです。コードの品質を注意深くレビューしてください..."

# 全スキルを一覧表示
agentforge skill list

# スキルの詳細を表示
agentforge skill show my-reviewer

# スキルをテスト
agentforge skill test my-reviewer

# スキルを MCP 形式でエクスポート
agentforge skill export my-reviewer --format mcp --output my-reviewer.json
```

### 🤖 Agent 管理

Agent はスキルの担い手です。各 Agent に異なるスキルの組み合わせを割り当てることができます。

```bash
# Agent を作成
agentforge agent create senior-dev \
  --role "シニア開発者" \
  --system-prompt "あなたは経験豊富なシニア開発者です..." \
  --model gpt-4

# 全 Agent を一覧表示
agentforge agent list

# Agent にスキルを割り当て
agentforge agent assign senior-dev my-reviewer
```

### 🔄 チームオーケストレーション

DAG（有向非巡回グラフ）の依存関係を通じて、複数 Agent の連携を編成します。

```bash
# チームを作成
agentforge team create dev-team --description "開発パイプラインチーム"

# Agent をチームに追加（依存関係の宣言に対応）
agentforge team add dev-team code-reviewer
agentforge team add dev-team bug-fixer --depends-on code-reviewer
agentforge team add dev-team test-gen --depends-on bug-fixer

# チームの DAG 構造を可視化
agentforge team visualize dev-team

# チームオーケストレーションを実行
agentforge team run dev-team
```

### 📋 テンプレートの利用

AgentForge には 20 以上の慎重に設計されたスキルテンプレートが組み込まれており、開発ライフサイクル全体をカバーしています：

| テンプレート | 用途 |
|-------------|------|
| `code-review` | コードレビュー、バグと品質問題の検出 |
| `doc-generator` | ソースコードや説明からドキュメントを生成 |
| `data-analyst` | データ分析とインサイト生成 |
| `api-tester` | API エンドポイントのテストケース生成 |
| `security-scanner` | セキュリティ脆弱性スキャン（OWASP Top 10） |
| `code-refactorer` | コードリファクタリングと最適化 |
| `translator` | 多言語翻訳 |
| `summarizer` | テキスト要約生成 |
| `bug-fixer` | バグの特定と修正 |
| `perf-optimizer` | パフォーマンス最適化の提案 |
| `test-generator` | ユニットテストと統合テストの生成 |
| `code-explainer` | コードの解説と説明 |
| `req-analyst` | 要件分析と構造化 |
| `arch-designer` | アーキテクチャ設計とパターンの推奨 |
| `project-manager` | プロジェクト計画と管理 |
| `code-migrator` | 言語間のコード移行 |
| `config-manager` | 設定ファイルの生成と管理 |
| `log-analyst` | ログ分析とトラブルシューティング |
| `deploy-helper` | デプロイ設定と CI/CD 生成 |
| `monitor-analyst` | 監視とオブザーバビリティの設計 |

```bash
# 利用可能なテンプレートを一覧表示
agentforge template list

# テンプレートからスキルを作成
agentforge template apply code-review my-custom-reviewer
```

### 📤 エクスポート機能

スキルを標準 MCP Server 形式にエクスポートし、Claude Desktop や Cursor などの LLM クライアントとシームレスに連携できます。

```bash
# 単一スキルをエクスポート
agentforge skill export my-skill --format mcp --output skill.json

# エクスポート後は MCP クライアント設定で直接利用可能
```

---

## 💡 設計思想とロードマップ

### 🎯 設計思想

AgentForge Studio の中核となる設計思想は **「スキルはブロック、Agent は職人、チームは工場」** です：

- **スキル層（Skill）**：命令、パラメータ、入出力仕様を含むアトミックな AI 能力ユニットを定義
- **Agent 層**：スキルを組み合わせて特定の役割に割り当て、専門的な AI アシスタントを形成
- **チーム層（Team）**：DAG 依存関係グラフで Agent の実行順序を編成し、複雑なワークフローを実現

### 🗺️ ロードマップ

- **v1.0** ✅ — コア機能：スキル管理、Agent 管理、チームオーケストレーション、MCP エクスポート、TUI ダッシュボード
- **v1.1** 🔜 — ビジュアル DAG エディタ、スキルマーケットプレイス、チームテンプレート
- **v1.2** 🔜 — 分散実行エンジン、Web ダッシュボード、プラグインシステム
- **v2.0** 🔮 — マルチモーダルスキル対応、AutoML 統合、エンタープライズ級権限管理

---

## 📦 インストールとデプロイ

### 🐍 ソースからインストール

```bash
git clone https://github.com/gitstq/AgentForge-Studio.git
cd AgentForge-Studio
pip install -e ".[tui]"
```

### 🧪 開発環境のセットアップ

```bash
# 開発用依存関係をインストール
pip install -e ".[dev]"

# テストを実行
pytest

# カバレッジレポート付きでテストを実行
pytest --cov=agentforge
```

### 📁 プロジェクト構成

```
AgentForge-Studio/
├── agentforge/           # コアソースコード
│   ├── core/             # コアモデル（Skill, Agent, Team, Engine）
│   ├── export/           # MCP エクスポートモジュール
│   ├── sandbox/          # テストサンドボックス
│   ├── templates/        # 組み込みテンプレート
│   ├── tui/              # TUI ダッシュボード
│   ├── utils/            # ユーティリティ関数
│   └── cli.py            # CLI エントリーポイント
├── tests/                # ユニットテスト（84 テスト）
├── pyproject.toml        # プロジェクト設定
├── requirements.txt      # 依存関係リスト
└── LICENSE               # MIT ライセンス
```

---

## 🤝 コントリビューション

あらゆる形のコントリビューションを歓迎します！バグ報告、ドキュメント改善、新機能の提供など、どのような貢献でも大歓迎です。

### 📝 コントリビューションフロー

1. リポジトリを **Fork** する
2. フィーチャーブランチを作成：`git checkout -b feature/amazing-feature`
3. 変更をコミット：`git commit -m 'Add some amazing feature'`
4. リモートにプッシュ：`git push origin feature/amazing-feature`
5. **Pull Request** を提出する

### 📋 開発規範

- PEP 8 コーディング規約に従うこと
- 新機能には必ずユニットテストを含めること
- コミットメッセージは [Conventional Commits](https://www.conventionalcommits.org/) 仕様に従うこと
- PR を提出前に全テストが通過することを確認すること

---

## 📄 ライセンス

このプロジェクトは [MIT License](https://opensource.org/licenses/MIT) の下でオープンソースとして公開されています。

```
MIT License

Copyright (c) 2024 AgentForge Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

<p align="center">
  ❤️ で構築 | AgentForge Studio
</p>

---

<a name="한국어"></a>

# 🎉 AgentForge Studio

> 터미널에서 AI Agent 군단을 구축하세요 — 가볍고, 효율적이며, 바로 사용할 수 있습니다.

AgentForge Studio는 터미널 기반의 AI Agent 스킬 팩토리 및 팀 오케스트레이션 엔진입니다. 블록을 조립하듯 AI Agent 스킬을 만들고, 관리하고, 오케스트레이션할 수 있으며, DAG 의존성 그래프를 통해 다중 Agent 팀 협업을 구현할 수 있습니다. 복잡한 설정 없이 명령어 하나로 AI 워크숍을 시작하세요.

**GitHub:** [https://github.com/gitstq/AgentForge-Studio](https://github.com/gitstq/AgentForge-Studio)

---

## ✨ 핵심 기능

| 기능 | 설명 |
|------|------|
| 🛠️ **스킬 관리** | AI Agent 스킬 생성, 편집, 테스트, 내보내기 — 전체 수명 주기 관리 |
| 🤖 **Agent 관리** | Agent 생성 및 스킬 유연한 할당으로 맞춤형 AI 어시스턴트 구축 |
| 🔄 **팀 오케스트레이션** | DAG 의존성 그래프 기반 다중 Agent 팀 협업 편성, 시각화 지원 |
| 📋 **20+ 내장 템플릿** | 코드 리뷰, 문서 생성, 보안 스캔, 데이터 분석 등 즉시 사용 가능 |
| 📤 **MCP 내보내기** | 스킬을 원클릭으로 MCP Server 형식으로 내보내기, LLM 생태계와 원활한 연동 |
| 🧪 **테스트 샌드박스** | 각 스킬을 독립적으로 테스트하여 품질과 신뢰성 보장 |
| 📊 **TUI 대시보드** | Rich 터미널 인터랙티브 인터페이스로 정보를 한눈에 파악 |
| ✅ **84개 단위 테스트** | 전체 통과, 코드 품질 보장 |

---

## 🚀 빠른 시작

### 📋 사전 요구 사항

- Python 3.9 이상
- pip 패키지 관리자
- 터미널 (256색 지원 권장, 최상의 경험을 위해)

### 🔧 설치 방법

```bash
# 저장소 복제
git clone https://github.com/gitstq/AgentForge-Studio.git
cd AgentForge-Studio

# 의존성 설치
pip install -r requirements.txt

# 프로젝트 설치 (선택 사항, agentforge 명령어 등록)
pip install -e .
```

### 🎮 사용법

```bash
# 버전 확인
agentforge --version

# 프로젝트 초기화
agentforge init

# TUI 대시보드 실행
agentforge dashboard
```

---

## 📖 상세 가이드

### 🛠️ 스킬 관리

스킬은 AgentForge의 기본 구성 단위입니다. 각 스킬은 AI Agent가 실행할 수 있는 구체적인 능력을 정의합니다.

```bash
# 새 스킬 생성
agentforge skill create my-reviewer \
  --description "코드 리뷰 전문가" \
  --instructions "당신은 시니어 코드 리뷰어입니다. 코드 품질을 꼼꼼하게 검토해 주세요..."

# 전체 스킬 목록 보기
agentforge skill list

# 스킬 상세 정보 보기
agentforge skill show my-reviewer

# 스킬 테스트
agentforge skill test my-reviewer

# 스킬을 MCP 형식으로 내보내기
agentforge skill export my-reviewer --format mcp --output my-reviewer.json
```

### 🤖 Agent 관리

Agent는 스킬의 운반체입니다. 각 Agent에 다양한 스킬 조합을 할당할 수 있습니다.

```bash
# Agent 생성
agentforge agent create senior-dev \
  --role "시니어 개발자" \
  --system-prompt "당신은 경험이 풍부한 시니어 개발자입니다..." \
  --model gpt-4

# 전체 Agent 목록 보기
agentforge agent list

# Agent에 스킬 할당
agentforge agent assign senior-dev my-reviewer
```

### 🔄 팀 오케스트레이션

DAG (유향 비순환 그래프) 의존성 관계를 통해 여러 Agent의 협업을 편성합니다.

```bash
# 팀 생성
agentforge team create dev-team --description "개발 파이프라인 팀"

# 팀에 Agent 추가 (의존성 선언 지원)
agentforge team add dev-team code-reviewer
agentforge team add dev-team bug-fixer --depends-on code-reviewer
agentforge team add dev-team test-gen --depends-on bug-fixer

# 팀 DAG 구조 시각화
agentforge team visualize dev-team

# 팀 오케스트레이션 실행
agentforge team run dev-team
```

### 📋 템플릿 활용

AgentForge에는 개발 라이프사이클 전체를 아우르는 20개 이상의 정교하게 설계된 스킬 템플릿이 내장되어 있습니다:

| 템플릿 | 용도 |
|--------|------|
| `code-review` | 코드 리뷰, 버그 및 품질 문제 감지 |
| `doc-generator` | 소스 코드나 설명에서 문서 생성 |
| `data-analyst` | 데이터 분석 및 인사이트 생성 |
| `api-tester` | API 엔드포인트 테스트 케이스 생성 |
| `security-scanner` | 보안 취약점 스캔 (OWASP Top 10) |
| `code-refactorer` | 코드 리팩토링 및 최적화 |
| `translator` | 다국어 번역 |
| `summarizer` | 텍스트 요약 생성 |
| `bug-fixer` | 버그 식별 및 수정 |
| `perf-optimizer` | 성능 최적화 제안 |
| `test-generator` | 단위 테스트 및 통합 테스트 생성 |
| `code-explainer` | 코드 설명 및 해설 |
| `req-analyst` | 요구사항 분석 및 구조화 |
| `arch-designer` | 아키텍처 설계 및 패턴 추천 |
| `project-manager` | 프로젝트 기획 및 관리 |
| `code-migrator` | 언어 간 코드 마이그레이션 |
| `config-manager` | 설정 파일 생성 및 관리 |
| `log-analyst` | 로그 분석 및 문제 해결 |
| `deploy-helper` | 배포 설정 및 CI/CD 생성 |
| `monitor-analyst` | 모니터링 및 관측 가능성 설계 |

```bash
# 사용 가능한 템플릿 목록 보기
agentforge template list

# 템플릿에서 스킬 생성
agentforge template apply code-review my-custom-reviewer
```

### 📤 내보내기 기능

스킬을 표준 MCP Server 형식으로 내보내어 Claude Desktop, Cursor 등 LLM 클라이언트와 원활하게 연동할 수 있습니다.

```bash
# 단일 스킬 내보내기
agentforge skill export my-skill --format mcp --output skill.json

# 내보낸 파일은 MCP 클라이언트 설정에서 직접 사용 가능
```

---

## 💡 설계 철학과 로드맵

### 🎯 설계 철학

AgentForge Studio의 핵심 설계 철학은 **"스킬은 블록, Agent는 장인, 팀은 공장"** 입니다:

- **스킬 레이어**: 명령어, 파라미터, 입출력 사양을 포함하는 원자적 AI 능력 단위를 정의
- **Agent 레이어**: 스킬을 조합하여 특정 역할에 할당하고, 전문화된 AI 어시스턴트를 형성
- **팀 레이어**: DAG 의존성 그래프로 Agent 실행 순서를 편성하여 복잡한 워크플로우를 구현

### 🗺️ 로드맵

- **v1.0** ✅ — 핵심 기능: 스킬 관리, Agent 관리, 팀 오케스트레이션, MCP 내보내기, TUI 대시보드
- **v1.1** 🔜 — 시각적 DAG 편집기, 스킬 마켓플레이스, 팀 템플릿
- **v1.2** 🔜 — 분산 실행 엔진, Web 대시보드, 플러그인 시스템
- **v2.0** 🔮 — 멀티모달 스킬 지원, AutoML 통합, 엔터프라이즈급 권한 관리

---

## 📦 설치 및 배포

### 🐍 소스에서 설치

```bash
git clone https://github.com/gitstq/AgentForge-Studio.git
cd AgentForge-Studio
pip install -e ".[tui]"
```

### 🧪 개발 환경 설정

```bash
# 개발용 의존성 설치
pip install -e ".[dev]"

# 테스트 실행
pytest

# 커버리지 리포트와 함께 테스트 실행
pytest --cov=agentforge
```

### 📁 프로젝트 구조

```
AgentForge-Studio/
├── agentforge/           # 핵심 소스 코드
│   ├── core/             # 핵심 모델 (Skill, Agent, Team, Engine)
│   ├── export/           # MCP 내보내기 모듈
│   ├── sandbox/          # 테스트 샌드박스
│   ├── templates/        # 내장 템플릿
│   ├── tui/              # TUI 대시보드
│   ├── utils/            # 유틸리티 함수
│   └── cli.py            # CLI 진입점
├── tests/                # 단위 테스트 (84개)
├── pyproject.toml        # 프로젝트 설정
├── requirements.txt      # 의존성 목록
└── LICENSE               # MIT 라이선스
```

---

## 🤝 기여하기

모든 형태의 기여를 환영합니다! 버그 제보, 문서 개선, 새로운 기능 제공 등 어떤 기여든 환영합니다.

### 📝 기여 절차

1. 저장소를 **Fork** 합니다
2. 기능 브랜치 생성: `git checkout -b feature/amazing-feature`
3. 변경 사항 커밋: `git commit -m 'Add some amazing feature'`
4. 원격에 푸시: `git push origin feature/amazing-feature`
5. **Pull Request** 제출

### 📋 개발 규범

- PEP 8 코딩 규칙을 따를 것
- 모든 새 기능에는 단위 테스트를 포함할 것
- 커밋 메시지는 [Conventional Commits](https://www.conventionalcommits.org/) 사양을 따를 것
- PR 제출 전 모든 테스트가 통과하는지 확인할 것

---

## 📄 라이선스

이 프로젝트는 [MIT License](https://opensource.org/licenses/MIT)에 따라 오픈소스로 공개됩니다.

```
MIT License

Copyright (c) 2024 AgentForge Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

<p align="center">
  ❤️로 제작 | AgentForge Studio
</p>

---

<a name="español"></a>

# 🎉 AgentForge Studio

> Construye tu ejercito de AI Agent desde la terminal — ligero, eficiente y listo para usar.

AgentForge Studio es una fabrica de habilidades y un motor de orquestacion de equipos de AI Agent basado en terminal. Te permite crear, gestionar y orquestar habilidades de AI Agent con la misma facilidad que armar bloques, y coordinar la colaboracion de multiples Agent mediante grafos de dependencia DAG. Sin configuraciones complejas: con un solo comando puedes poner en marcha tu taller de IA.

**GitHub:** [https://github.com/gitstq/AgentForge-Studio](https://github.com/gitstq/AgentForge-Studio)

---

## ✨ Caracteristicas Principales

| Caracteristica | Descripcion |
|----------------|-------------|
| 🛠️ **Gestion de Habilidades** | Crear, editar, probar y exportar habilidades de AI Agent con gestion completa del ciclo de vida |
| 🤖 **Gestion de Agentes** | Crear Agentes y asignar habilidades de forma flexible para construir asistentes de IA personalizados |
| 🔄 **Orquestacion de Equipos** | Orquestar la colaboracion de multiples Agentes mediante grafos de dependencia DAG con visualizacion |
| 📋 **20+ Plantillas Integradas** | Revision de codigo, generacion de documentacion, analisis de seguridad, analisis de datos y mas, listas para usar |
| 📤 **Exportacion MCP** | Exportacion con un clic al formato MCP Server para integracion perfecta con el ecosistema LLM |
| 🧪 **SandBox de Pruebas** | Probar cada habilidad de forma independiente para garantizar calidad y fiabilidad |
| 📊 **Panel TUI** | Interfaz interactiva de terminal con Rich para una vision clara de un vistazo |
| ✅ **84 Tests Unitarios** | Todos aprobados, calidad de codigo garantizada |

---

## 🚀 Inicio Rapido

### 📋 Requisitos Previos

- Python 3.9 o superior
- Gestor de paquetes pip
- Terminal (se recomienda soporte de 256 colores para la mejor experiencia)

### 🔧 Instalacion

```bash
# Clonar el repositorio
git clone https://github.com/gitstq/AgentForge-Studio.git
cd AgentForge-Studio

# Instalar dependencias
pip install -r requirements.txt

# Instalar el proyecto (opcional, registra el comando agentforge)
pip install -e .
```

### 🎮 Uso Basico

```bash
# Verificar la version
agentforge --version

# Inicializar un proyecto
agentforge init

# Iniciar el panel TUI
agentforge dashboard
```

---

## 📖 Guia Detallada

### 🛠️ Gestion de Habilidades

Las habilidades son las unidades fundamentales de AgentForge. Cada habilidad define una capacidad especifica que un AI Agent puede ejecutar.

```bash
# Crear una nueva habilidad
agentforge skill create my-reviewer \
  --description "Experto en revision de codigo" \
  --instructions "Eres un revisor de codigo senior. Por favor, revisa cuidadosamente la calidad del codigo..."

# Listar todas las habilidades
agentforge skill list

# Ver detalles de una habilidad
agentforge skill show my-reviewer

# Probar una habilidad
agentforge skill test my-reviewer

# Exportar una habilidad en formato MCP
agentforge skill export my-reviewer --format mcp --output my-reviewer.json
```

### 🤖 Gestion de Agentes

Los Agentes son los portadores de habilidades. Puedes asignar diferentes combinaciones de habilidades a cada Agente.

```bash
# Crear un Agente
agentforge agent create senior-dev \
  --role "Desarrollador Senior" \
  --system-prompt "Eres un desarrollador senior con amplia experiencia..." \
  --model gpt-4

# Listar todos los Agentes
agentforge agent list

# Asignar una habilidad a un Agente
agentforge agent assign senior-dev my-reviewer
```

### 🔄 Orquestacion de Equipos

Coordina la colaboracion de multiples Agentes mediante relaciones de dependencia DAG (Grafo Dirigido Aciclico).

```bash
# Crear un equipo
agentforge team create dev-team --description "Equipo de pipeline de desarrollo"

# Anadir Agentes al equipo (con declaracion de dependencias)
agentforge team add dev-team code-reviewer
agentforge team add dev-team bug-fixer --depends-on code-reviewer
agentforge team add dev-team test-gen --depends-on bug-fixer

# Visualizar la estructura DAG del equipo
agentforge team visualize dev-team

# Ejecutar la orquestacion del equipo
agentforge team run dev-team
```

### 📋 Uso de Plantillas

AgentForge incluye mas de 20 plantillas de habilidades cuidadosamente disenadas que cubren todo el ciclo de desarrollo:

| Plantilla | Proposito |
|-----------|-----------|
| `code-review` | Revision de codigo, deteccion de bugs y problemas de calidad |
| `doc-generator` | Generacion de documentacion a partir de codigo fuente o descripciones |
| `data-analyst` | Analisis de datos y generacion de insights |
| `api-tester` | Generacion de casos de prueba para endpoints de API |
| `security-scanner` | Escaneo de vulnerabilidades de seguridad (OWASP Top 10) |
| `code-refactorer` | Refactorizacion y optimizacion de codigo |
| `translator` | Traduccion a multiples idiomas |
| `summarizer` | Generacion de resumenes de texto |
| `bug-fixer` | Identificacion y correccion de bugs |
| `perf-optimizer` | Sugerencias de optimizacion de rendimiento |
| `test-generator` | Generacion de tests unitarios y de integracion |
| `code-explainer` | Explicacion y documentacion de codigo |
| `req-analyst` | Analisis y estructuracion de requisitos |
| `arch-designer` | Diseno de arquitectura y recomendacion de patrones |
| `project-manager` | Planificacion y gestion de proyectos |
| `code-migrator` | Migracion de codigo entre lenguajes |
| `config-manager` | Generacion y gestion de archivos de configuracion |
| `log-analyst` | Analisis de logs y resolucion de problemas |
| `deploy-helper` | Configuracion de despliegue y generacion de CI/CD |
| `monitor-analyst` | Diseno de monitorizacion y observabilidad |

```bash
# Listar todas las plantillas disponibles
agentforge template list

# Crear una habilidad a partir de una plantilla
agentforge template apply code-review my-custom-reviewer
```

### 📤 Funcionalidad de Exportacion

Exporta habilidades al formato estandar MCP Server para una integracion perfecta con clientes LLM como Claude Desktop y Cursor.

```bash
# Exportar una habilidad individual
agentforge skill export my-skill --format mcp --output skill.json

# El archivo exportado se puede usar directamente en la configuracion del cliente MCP
```

---

## 💡 Filosofia de Diseno y Hoja de Ruta

### 🎯 Filosofia de Diseno

La filosofia de diseno central de AgentForge Studio es **"Las habilidades son bloques, los Agentes son artesanos, los equipos son fabricas"**:

- **Capa de Habilidades (Skill)**: Define unidades atomicas de capacidad de IA con instrucciones, parametros y especificaciones de entrada/salida
- **Capa de Agentes**: Combina habilidades y las asigna a roles especificos, creando asistentes de IA especializados
- **Capa de Equipos**: Orquesta el orden de ejecucion de los Agentes mediante grafos de dependencia DAG para flujos de trabajo complejos

### 🗺️ Hoja de Ruta

- **v1.0** ✅ — Funciones principales: gestion de habilidades, gestion de Agentes, orquestacion de equipos, exportacion MCP, panel TUI
- **v1.1** 🔜 — Editor DAG visual, mercado de habilidades, plantillas de equipos
- **v1.2** 🔜 — Motor de ejecucion distribuido, panel Web, sistema de plugins
- **v2.0** 🔮 — Soporte de habilidades multimodales, integracion con AutoML, gestion de permisos a nivel empresarial

---

## 📦 Instalacion y Despliegue

### 🐍 Instalacion desde el Fuente

```bash
git clone https://github.com/gitstq/AgentForge-Studio.git
cd AgentForge-Studio
pip install -e ".[tui]"
```

### 🧪 Configuracion del Entorno de Desarrollo

```bash
# Instalar dependencias de desarrollo
pip install -e ".[dev]"

# Ejecutar tests
pytest

# Ejecutar tests con informe de cobertura
pytest --cov=agentforge
```

### 📁 Estructura del Proyecto

```
AgentForge-Studio/
├── agentforge/           # Codigo fuente principal
│   ├── core/             # Modelos principales (Skill, Agent, Team, Engine)
│   ├── export/           # Modulo de exportacion MCP
│   ├── sandbox/          # SandBox de pruebas
│   ├── templates/        # Plantillas integradas
│   ├── tui/              # Panel TUI
│   ├── utils/            # Funciones de utilidad
│   └── cli.py            # Punto de entrada CLI
├── tests/                # Tests unitarios (84 tests)
├── pyproject.toml        # Configuracion del proyecto
├── requirements.txt      # Lista de dependencias
└── LICENSE               # Licencia MIT
```

---

## 🤝 Contribuir

¡Agradecemos todo tipo de contribuciones! Ya sea informar de un bug, mejorar la documentacion o aportar nuevas funcionalidades.

### 📝 Flujo de Contribucion

1. **Fork** este repositorio
2. Crear una rama de funcionalidad: `git checkout -b feature/amazing-feature`
3. Confirmar los cambios: `git commit -m 'Add some amazing feature'`
4. Enviar al remoto: `git push origin feature/amazing-feature`
5. Enviar un **Pull Request**

### 📋 Normas de Desarrollo

- Seguir las convenciones de codificacion PEP 8
- Todas las nuevas funcionalidades deben incluir tests unitarios
- Los mensajes de commit deben seguir la especificacion [Conventional Commits](https://www.conventionalcommits.org/)
- Asegurarse de que todos los tests pasen antes de enviar un PR

---

## 📄 Licencia

Este proyecto se publica como codigo abierto bajo la [MIT License](https://opensource.org/licenses/MIT).

```
MIT License

Copyright (c) 2024 AgentForge Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

<p align="center">
  Hecho con ❤️ | AgentForge Studio
</p>
