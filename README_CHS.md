# midishow-downloader-selfhost
自动下载 midishow 上的 midi 文件
- - -
[English](https://github.com/Saobby/midishow-downloader-selfhost/blob/main/README.md)
# 使用
1. 设置 Redis
下载并安装适用于 Windows 的 Redis。
由于 Redis 不正式支持 Windows，您可以从 [这里](https://github.com/tporadowski/redis/releases/tag/v5.0.14.1) 下载。

2. 启动 Redis 服务
按 `Win+R`，输入 `services.msc`，然后按 `Enter`
在弹出的窗口中找到 `Redis`，然后单击左侧的 `Start`。

3. 设置 Redis 地址
一般情况下，您不需要进行额外的配置，只需保留默认设置即可。
但如果您想使用远程 Redis 服务器，请在 `./config.toml` 中进行配置

4. 下载 midishow 下载器
下载下载器的最新版本。
- [32 位下载](https://nightly.link/Saobby/midishow-downloader-selfhost/workflows/build.yaml/main/midishow_downloader-x86.zip)
- [64 位下载](https://nightly.link/Saobby/midishow-downloader-selfhost/workflows/build.yaml/main/midishow_downloader-x64.zip)

如果您不知道计算机的架构，只需下载 `32 位` 版本。
您应该会得到一个 .zip 存档。**请在下载后解压。**

5. 设置您的 midishow 帐户
打开 `config.toml` 并将您的 midishow 用户名和密码放在 `midishow.accounts` 部分下。
如果你有多个账户，可以这样写：
```toml
[[midishow.accounts]]
username = "username1"
password = "password1"

[[midishow.accounts]]
username = "username2"
password = "password2"

[[midishow.accounts]]
username = "username3"
password = "password3"
```
下载器每次下载都会使用一个随机账户。

6. 启动下载器
双击 `./server.exe` 运行下载器。
如果一切顺利，你的浏览器会自动打开下载器的网页。
输入 midi 的网址，尽情享受吧！
# 故障排除
如果你有任何问题，请随时在 [Issues](https://github.com/Saobby/midishow-downloader-selfhost/issues) 告诉我。
报告错误时请附上错误日志。
# 免责声明
此工具仅用于教育目的。由于 midishow 网站已禁用 midi 预览功能，因此它旨在方便地预览 midi。请尊重知识产权。**未经作者许可，请勿将您下载的 midi 转发到其他网站。不要将您下载的 midi 出售给他人。**本项目的开发人员对因使用或误用本工具而引起的任何损害、损失或法律问题概不负责。这包括但不限于任何直接、间接、偶然或后果性损害。**用户承担与使用此工具相关的所有风险。**本免责声明可能随时更新或修改，恕不另行通知。鼓励用户定期查看，以了解他们的责任和义务。
# 贡献
请随时做出任何贡献。
# 第三方许可
本项目使用以下第三方库：
- wux-ui（原始 repo 已删除）
- [tabler-icons](https://github.com/tabler/tabler-icons)
- [Tone.js](https://www.npmjs.com/package/tone)
- [@magenta/music](https://www.npmjs.com/package/@magenta/music)
- [focus-visible](https://www.npmjs.com/package/focus-visible)
- [html-midi-player](https://www.npmjs.com/package/html-midi-player)

其许可可在 `./third_party_licenses` 中找到