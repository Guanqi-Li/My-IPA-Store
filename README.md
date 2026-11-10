# 我的 IPA 软件源

供个人使用的 IPA 目录。安装包存放在 GitHub Releases，网页目录和 JSON 软件源由 GitHub Pages 发布。

- [打开网页目录](https://guanqi-li.github.io/My-IPA-Store/)
- [打开 JSON 软件源](https://guanqi-li.github.io/My-IPA-Store/source.json)

软件源采用 **AltStore Classic 风格的 JSON**。请使用支持这一格式的客户端导入。

## 在 iPhone 上手动发布

如果 IPA 文件在 iPhone 的「文件」App 中：

1. 在 Safari 登录 GitHub，打开[新建 Release](https://github.com/Guanqi-Li/My-IPA-Store/releases/new)。
2. 选择 **Choose a tag**，创建一个新标签，例如 `upload-app-a-1.0`。目标分支选 `main`，标题填写软件名称。
3. 在附件区选中 `.ipa` 文件，等待上传完成，点击 **Publish release**。
4. 在发布页的 **Assets** 下长按 IPA 文件名，拷贝下载链接。

如果手里已有 HTTPS 下载直链，可以直接从这里开始：

1. 打开 [Import IPA from URL](https://github.com/Guanqi-Li/My-IPA-Store/actions/workflows/import-ipa.yml)，点击 **Run workflow**，选择 `main` 分支。
2. 填写以下字段，再点击 **Run workflow** 提交。

   | 字段 | 填写内容 |
   | --- | --- |
   | `ipa_url` | 可直接下载 IPA 的 HTTPS 链接。请使用附件下载链接，网盘分享页无法直接导入。 |
   | `name` | 软件名称，可留空，由脚本从 IPA 读取。 |
   | `description` | 显示在软件目录里的介绍，可留空。 |
   | `icon_url` | 图标的 HTTPS 图片直链，可留空。 |

3. 在 [Actions](https://github.com/Guanqi-Li/My-IPA-Store/actions) 查看进度。导入成功后会自动触发 Pages 部署。部署完成后刷新网页目录即可。

如果先把 IPA 上传到本仓库的 Releases 再用直链导入，工作流会在正式的软件 Release 中再保存一份安装包。

## 在电脑上发布本地 IPA

安装 Python 3 和 [GitHub CLI](https://cli.github.com/)，运行 `gh auth login` 登录。克隆仓库后，在仓库目录执行：

```sh
python scripts/manage.py add --file "/path/to/App.ipa" --repo Guanqi-Li/My-IPA-Store --description "软件介绍"
git add docs/source.json
git commit -m "添加 IPA 软件"
git push
```

将 `/path/to/App.ipa` 换成实际文件路径。需要自定义图标时，可以在第一条命令末尾加上 `--icon "https://example.com/icon.png"`。

脚本会从 IPA 的 `Info.plist` 读取名称、包名、版本和构建号，并记录文件大小。图标需另外提供，脚本目前不会从 IPA 提取图标。同一包名的多个版本和构建会归到同一个软件条目。将更新推送到 `main` 后，Pages 会自动部署。

## 首次部署

1. 在仓库 **Settings → General → Danger Zone → Change repository visibility** 中，将仓库设为 **Public**。
2. 在 **Settings → Pages → Source** 中选择 **GitHub Actions**。
3. 打开 [Publish software source](https://github.com/Guanqi-Li/My-IPA-Store/actions/workflows/pages.yml)，点击 **Run workflow** 完成首次部署。

## 使用限制与维护

- 单个 Release 附件须小于 **2 GiB**。总容量可能超过 50 GB，实际可用容量和服务稳定性以 GitHub 为准。
- 中国大陆直连 GitHub Pages 和 Releases 的速度与可用性因网络而异。
- 公开仓库的网页、软件源和已发布的附件均可被他人访问。请勿上传私有签名证书、令牌或个人资料。
- 如需清理旧安装包，请在 GitHub Releases 中删除对应附件。从软件源移除条目后，原附件仍会保留。
