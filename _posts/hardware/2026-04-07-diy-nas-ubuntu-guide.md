---
layout: single
title: "Untitled"
date: 2026-04-07
categories: [hardware]
permalink: /posts/hardware/:title.html
author_profile: false
show_date: true
toc: true
---

---
layout: post
title: "从零开始自建NAS教程：Ubuntu系统改造实战指南"
date: 2026-04-07
category: hardware/nas
category_name: "数码硬件/NAS存储"
---

1100元打造2000元档位NAS性能，完全可控的私人数据中心。

## 前置条件

阅读本文需要：

- **命令行操作基础** - Linux基本操作

- **网络知识** - 理解IP、端口、协议

- **折腾精神** - 享受动手过程最重要

**不适合谁**：只想开箱即用、不想折腾的用户（建议直接买成品NAS）

---

## 核心优势

对比项成品NAS自建NAS
价格2000元+1100元（主机700+硬盘柜400）
可控性依赖厂商完全自主
性能N5105级别N100（接近2000元档位）
服务付费部分功能需订阅全部免费
学习成本低高

---

## 硬件配置

项目配置成本
主机零刻EQ12小主机（闲鱼）¥600
CPUN100-
内存二手¥200
固态二手¥300
硬盘柜双盘位¥400
**总计****¥1500-3500**

---

## 系统安装

**Ubuntu 22.04**

- 下载带GUI的系统镜像

- 制作启动U盘

- 按向导安装（类似Windows）

---

## 核心软件配置

### 1. OpenList + Aria2（网盘+下载）

**OpenList安装：**

`docker run -d \
 --name="openlist" \
 --restart unless-stopped \
 -v /opt/alist:/opt/openlist/data \
 -v /root/Downloads:/download \
 -v /media/data:/data \
 --network host \
 openlistteam/openlist:latest
`

访问地址：`ip:5244`

**功能：**

- 支持百度网盘、阿里云盘、夸克等挂载

- WebDAV协议支持

- 离线下载

### 2. Jellyfin（影音中心）

`docker run -d \
 --name jellyfin \
 --net=host \
 -v /opt/jellyfin/config:/config \
 -v /media/data:/media \
 --device /dev/dri/:/dev/dri/ \
 --restart=unless-stopped \
 jellyfin/jellyfin
`

**关键特性：**

- `--device /dev/dri/` 开启硬件解码

- N100可流畅转码4K视频

- 实测70G泰坦尼克号正常转码

**串流 vs 转码：**

对比项串流转码
画质原始画质压缩后可选
带宽要求极高低，自适应
服务器压力低高
适用场景局域网外网观看

### 3. 海报刮削（TinyMediaManager）

`docker run -d \
 --name=tinymediamanager \
 -v /opt/tinymediamanager/config:/config \
 -v /media:/media \
 -p 5800:5800 \
 romancin/tinymediamanager:latest-v4
`

需要：TMDB API Key（免费申请）

### 4. 字幕刮削（ChineseSubFinder）

`docker run -d \
 -v /opt/ChineseSubFinder/config:/config \
 -v /media/data:/media \
 --net=host \
 --name chinesesubfinder \
 --restart=unless-stopped \
 allanpk716/chinesesubfinder:latest
`

### 5. 迅雷下载

`docker run -d \
 --name=xunlei \
 --network=host \
 -v /opt/xunlei/data:/xunlei/data \
 -v /root/Downloads:/xunlei/downloads \
 --restart=unless-stopped \
 --privileged \
 cnk3x/xunlei:latest
`

### 6. 跨设备备份（Syncthing）

`docker run -d \
 --network=host \
 --name syncthing \
 -v /media/backup/Syncthing:/var/syncthing \
 syncthing/syncthing:latest
`

---

## 内网穿透

### Tailscale（推荐）

`curl -fsSL https://tailscale.com/install.sh | sh
tailscale up --accept-routes=true --advertise-routes=192.168.28.0/24 --advertise-exit-node
`

**核心功能：**

- **Subnet** - 局域网地址转发，无需记忆Tailscale IP

- **Exit Node** - 全流量代理出口

- **IPV6打洞** - 99%成功率

**优势：**

- 无需公网IP

- 安全性高

- 免费使用

### DDNS（备选）

**前提**：光猫改桥接，获取公网IPV6

`docker run -d \
 --name ddns-go \
 --restart=always \
 --net=host \
 -v /opt/ddns-go:/root \
 jeessy/ddns-go
`

---

## 软路由配置（进阶）

### 为什么需要软路由？

- 全屋代理 - 一站式科学上网

- 流量监控 - 设备资源占用

- 内网穿透增强

- 广告拦截

- 旁路由模式 - 不影响主路由

### 硬件推荐

设备价格特点
友善R5C¥300+双2.5G网口
友善R2S¥200+千兆，性价比高
X86软路由¥500+性能强，兼容性好

### 系统推荐

**iStoreOS** - 国内优化的OpenWRT：

- 应用商店丰富

- 兼容性好

- 社区活跃

---

## 手机端应用（iOS）

功能应用
内网穿透Tailscale（需美区ID）
照片备份PhotosSync
文件传输xList（WebDAV）
视频播放Infuse
音乐播放音流（连接Jellyfin）
服务器监控NeoServer
远程桌面Microsoft Remote Desktop
看漫画YAC Reader

---

## 完整功能清单

功能方案状态
远程照片同步WebDAV + PhotosSync✅
个人网盘OpenList✅
家庭影院Jellyfin✅
文件备份Syncthing / rsync✅
离线下载迅雷 / Aria2✅
海报刮削TinyMediaManager✅
字幕匹配ChineseSubFinder✅
内网穿透Tailscale✅
远程控制微软远程桌面✅

---

## 成本总结

项目金额
主机（EQ12 + 内存 + 固态）¥1100
硬盘柜¥400
硬盘（按需）¥500-2000
**总计****¥2000-3500**

**性能对标**：市面2000元档位成品NAS

---

## 注意事项

- **二手硬盘水深** - 确保靠谱商家

- **数据安全** - 重要数据建议RAID1或定期备份

- **学习曲线陡** - 需要耐心折腾

- **时间成本** - 配置完善需数周时间

- **持续维护** - 系统更新、故障排查

---

## 总结

**自建NAS适合：**

- ✅ 技术爱好者

- ✅ 追求性价比

- ✅ 需要完全可控

- ✅ 享受折腾过程

**不适合：**

- ❌ 只想开箱即用

- ❌ 不想学习Linux

- ❌ 数据极其重要且无备份习惯

**一句话**：折腾得起，就上；折腾不起，买成品。

---

原文来源：知乎用户「大水果」原创教程
改写时间：2026-04-07