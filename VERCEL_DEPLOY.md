# 在 Vercel 上部署小红书内容提取 API

本文档介绍如何将这个小红书内容提取 API 部署到 Vercel 上。

## 预备步骤

1. 确保你有一个 [Vercel 账号](https://vercel.com/signup)
2. 确保你的 GitHub 仓库中包含以下文件：
   - `api.py` - FastAPI 应用主文件
   - `transform_xhs.py` - 小红书内容提取逻辑
   - `requirements.txt` - 依赖文件
   - `vercel.json` - Vercel 配置文件

## 部署步骤

### 方法一：通过 Vercel 控制台部署

1. 登录 [Vercel 控制台](https://vercel.com/)
2. 点击 "New Project" 按钮
3. 导入你的 GitHub 仓库
4. 不需要修改任何设置，Vercel 会自动识别 FastAPI 项目
5. 点击 "Deploy" 按钮

### 方法二：通过 Vercel CLI 部署

1. 全局安装 Vercel CLI：
   ```bash
   npm install -g vercel
   ```

2. 登录到你的 Vercel 账号：
   ```bash
   vercel login
   ```

3. 在项目目录中运行部署命令：
   ```bash
   vercel
   ```

4. 按照提示完成部署

## 部署后的注意事项

- 你的 API 将会在 `https://<your-project-name>.vercel.app/` 上可用
- API 文档可在 `https://<your-project-name>.vercel.app/docs` 访问
- 使用 `/extract` 端点提取小红书内容，例如：

```bash
curl -X POST "https://<your-project-name>.vercel.app/extract" \
     -H "Content-Type: application/json" \
     -d '{"url":"https://www.xiaohongshu.com/discovery/item/123456789"}'
```

## 相关注意事项

- Vercel 的免费层有一些限制，包括函数执行时间不能超过 10 秒
- 如果你的小红书内容抓取需要更长时间，可能需要考虑使用其他平台部署
- 如果你的应用需要频繁访问小红书，可能会被小红书检测到并封锁 IP 地址 