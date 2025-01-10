# AI-Search 项目

## 项目简介

AI-Search 是一个基于多搜索引擎的搜索和总结工具，用户可以选择不同的搜索引擎进行关键词搜索，并对搜索结果进行总结。

## 项目结构

```
km_multiple/
├── front/                  # 前端代码
│   └── index.html          # 前端页面
├── server/                 # 后端代码
│   ├── html2md.py          # 后端服务
│   └── prompt_templates/   # 提示词模板
│       ├── keyword_prompt.txt
│       └── no_keyword_prompt.txt
└── README.md               # 项目说明文件
```

## 使用方法

### 前端

1. 打开 `front/index.html` 文件。
2. 选择搜索引擎，输入关键词，点击搜索按钮。
3. 查看搜索结果和总结内容。

### 后端

1. 安装依赖：

    ```bash
    pip install fastapi uvicorn playwright trafilatura requests
    playwright install
    ```

2. 启动后端服务：

    ```bash
    uvicorn server.html2md:app --host 0.0.0.0 --port 8000
    ```

3. 后端服务将会在 `http://0.0.0.0:8000` 运行。

## 提示词模板

提示词模板存放在 `server/prompt_templates/` 目录下，包括：

- `keyword_prompt.txt`：包含关键词的提示词模板。
- `no_keyword_prompt.txt`：不包含关键词的提示词模板。

## 日志

日志文件 `app.log` 存放在项目根目录下，记录了后端服务的运行日志。

## 许可证

本项目使用 MIT 许可证，详情请参阅 LICENSE 文件。