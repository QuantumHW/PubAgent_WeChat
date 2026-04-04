# PubAgent-WeChat

> **当前版本：v1.0.0 (Official Release)**
>
> *注：首个正式版本，已跑通从选题、创作到微信草稿箱发布的完整流水线。*

PubAgent 是一个基于 Python 的自动化内容创作与发布系统，旨在通过多模型协作，实现从选题生成、内容创作、格式化到微信公众号草稿创建的全流程自动化。

## 🌟 核心功能

1. **自动生成文章**：支持多阶段生成（选题、正文、摘要）。
2. **自动格式化**：Markdown 自动转换为适配微信公众号的 HTML。
3. **自动素材管理**：自动上传正文图片和封面图至微信永久素材库。
4. **自动创建草稿**：在微信公众平台自动创建草稿，无需手动复制粘贴。
5. **定时/手动运行**：支持 CLI 手动触发和 APScheduler 定时任务。
6. **提示词灵活管理**：支持多套提示词方案，一键切换写作风格。
7. **高扩展性**：模块化设计，支持后续增加多账号、多平台及更多大模型。

## 🛠️ 技术栈

- **Python ≥ 3.10**
- **uv**: 现代 Python 依赖与环境管理器
- **requests**: 微信 API 调用
- **Markdown / Mistune**: Markdown 转 HTML
- **Pydantic / PyYAML**: 配置管理与验证
- **APScheduler**: 定时任务调度
- **Tenacity**: 指数退避的错误重试机制
- **SQLite**: 日志持久化存储

## 📂 项目结构

```text
PubAgent_WeChat/
├── config.yaml          # 核心配置文件（密钥、模型、风格切换）
├── pyproject.toml       # uv 项目配置文件
├── main.py              # CLI 入口程序
├── README.md            # 项目说明文档
├── .cache/              # 生成内容缓存（自动创建）
├── assets/              # 本地素材目录（封面图、正文图）
│   ├── content_image.jpg
│   └── cover_image.jpg
├── prompts/             # 提示词库（存放不同风格的提示词文件）
│   ├── default/         # 默认写作风格
│   │   ├── topic.txt    # 选题生成提示词
│   │   ├── content.txt  # 正文生成提示词
│   │   └── digest.txt   # 摘要生成提示词
│   └── tech-news/       # 其他写作风格示例
└── pubagent/            # 核心源代码目录
    ├── __init__.py
    ├── auth.py          # 微信 Access Token 中控（支持缓存与自动刷新）
    ├── config.py        # 配置解析模块（基于 Pydantic）
    ├── formatter.py     # 格式化模块（MD -> HTML，微信样式适配）
    ├── llm.py           # 大模型调度核心（支持多模型、多任务切换）
    ├── logger.py        # 日志系统（支持 Console & SQLite 持久化）
    ├── media.py         # 微信素材管理（图片上传、MediaID 获取）
    ├── pipeline.py      # 内容生成流水线（选题 -> 正文 -> 摘要）
    ├── publisher.py     # 微信发布模块（草稿箱接口对接）
    ├── scheduler.py     # 定时调度模块
    └── utils.py         # 辅助工具（简易内容缓存）
```

## 🚀 快速开始

### 1. 环境准备

确保已安装 [uv](https://github.com/astral-sh/uv)。

```bash
# 同步并安装依赖
uv sync
```

### 2. 配置说明

编辑项目根目录下的 `config.yaml`（可参考 `config.example.yaml`）：

- **wechat**: 填写微信公众平台的 `app_id` 和 `app_secret`。记得在微信后台配置 **IP白名单**。
- **llm**:
  - `api_key` & `base_url`: 配置大模型 API 访问。
  - `active_style`: 设置当前激活的写作风格（对应 `prompts/` 下的文件夹名称）。
- **scheduler**: 设置定时执行的间隔时间。

### 3. 素材准备

在 `assets/` 文件夹下放置以下文件（若不存在则需手动创建）：

- `cover_image.jpg`: 文章封面图（**必须**，微信草稿接口要求）。
- `content_image.jpg`: 正文插图（可选）。

### 4. 运行程序

```bash
# 单次运行测试
uv run python main.py --once

# 启动定时调度模式
uv run python main.py --schedule
```

## 📝 提示词管理 (Prompt Management)

系统支持通过外部文件灵活管理提示词，实现写作风格的一键切换：

- **组织结构**：在 `prompts/` 目录下为每种风格建立子文件夹。
- **核心文件**：每个风格文件夹内应包含 `topic.txt`, `content.txt`, `digest.txt` 三个文件，分别对应不同阶段的任务。

## 📈 版本记录 (Changelog)

### [v1.0.0] - 2026-04-04

- **First Official Release**
- **修复微信接口兼容性**：支持微信最新 API 要求的 32 字符标题限制，并自动进行智能截断。
- **优化编码处理**：禁用 Unicode 转义，改用 UTF-8 直传，解决微信后台中文乱码/报错问题。
- **优化 Prompt 引导**：在选题阶段增加长度约束，从源头减少长标题产生。
- **完善文档**：更新 README 说明及配置指南。

### [v0.1.0-alpha] - 2026-04-03

- **Initial MVP Release**
- 实现基于 Pipeline 的多阶段内容生成。
- 实现外部提示词文件夹管理与微信草稿箱发布。

## 📝 许可证

MIT License
