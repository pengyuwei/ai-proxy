# AI Proxy

解决chatGPT等海外API国内无法访问情况，通过海内外双节点部署提供AI访问代理服务。

## 目录结构

- api: 对外暴露的访问接口，部署在国内；
- proxy: 代理API，部署在海外服务器；
- adapter: AI适配，实际访问具体的AI接口，如chatGPT。部署在海外服务器；
  - chatGPT: chatGPT API接口实现；
  - xiaoP: 小P机器人接口；
- scripts: 环境脚本；

## 架构图

![架构图](http://www.memcd.com/files/ai-proxy-architecture.png)

