<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-alist

_✨ 一个支持多账号的 Alist 管理的 NoneBot 插件 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/iam57ao/nonebot-plugin-alist.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-template">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-alist.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="python">

</div>

### 📖 介绍

一个支持多账号的 Alist 管理的 NoneBot 插件。

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-alist

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-alist

</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-alist

</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-alist

</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-alist

</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_alist"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

|          配置项          | 必填 | 默认值 |       说明        |
|:---------------------:|:--:|:---:|:---------------:|
| ALIST_REQUEST_TIMEOUT | 否  | 10  | Alist请求的超时时间（秒） |

## 🎉 使用

### 指令表

|          指令           | 权限 | 需要@ |  范围   |          说明          |
|:---------------------:|:--:|:---:|:-----:|:--------------------:|
|       alist cd        | 所有 |  否  | 私聊、群聊 |        进入指定目录        |
|  alist download add   | 所有 |  否  | 私聊、群聊 |     添加一条或多条下载链接      |
| alist download cancel | 所有 |  否  | 私聊、群聊 |       取消一个下载任务       |
|  alist download list  | 所有 |  否  | 私聊、群聊 |       列出所有下载链接       |
|      alist help       | 所有 |  否  | 私聊、群聊 |    显示所有可用命令的帮助信息     |
|     alist logout      | 所有 |  否  | 私聊、群聊 |    退出当前登录的Alist账户    |
|       alist ls        | 所有 |  否  | 私聊、群聊 |  列出当前目录的文件, 支持分页显示   |
|       alist me        | 所有 |  否  | 私聊、群聊 |  显示当前登录的Alist账户的信息   |
|       alist pwd       | 所有 |  否  | 私聊、群聊 |     显示当前所在目录的路径      |
|     alist relogin     | 所有 |  否  |  私聊   |  重新登录一个添加过的Alist账户   |
|   alist account add   | 所有 |  否  |  私聊   | 添加一个新的Alist账户并切换到该账户 |
|   alist account del   | 所有 |  否  | 私聊、群聊 |   删除一个已存在的Alist账户    |
|  alist account info   | 所有 |  否  | 私聊、群聊 |   显示当前Alist账户的详细信息   |
|  alist account list   | 所有 |  否  | 私聊、群聊 |   列出所有已添加的Alist账户    |
| alist account switch  | 所有 |  否  | 私聊、群聊 |    切换到指定的Alist账户     |

## 📝 TODO

未来开发计划：

- [ ] 机器人图片回复
- [ ] 通过RSS订阅自动离线下载
- [ ] 完善对Alist文件API的支持