# DoubaoOS - Debian 定制美化系统

> 基于 Debian 12 (Bookworm) + Xfce 桌面环境的全自主定制美化系统
> 所有图标、壁纸、主题均由代码生成，零外部素材依赖

![DoubaoOS](https://img.shields.io/badge/DoubaoOS-v1.0-blue)
![Debian](https://img.shields.io/badge/Debian-12-red)
![Xfce](https://img.shields.io/badge/Xfce-4.18-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ 特性

### 🎨 全自主素材生成
- **28+ 种系统图标** × 7 种尺寸，纯 SVG 矢量代码生成
- **4 张系统壁纸**，几何渐变风格，纯代码生成
- **完整 GTK 主题**，支持 GTK2 / GTK3
- **自定义光标主题**

### 💼 办公模式
一键切换办公模式，专注效率：
- 极简办公壁纸
- 隐藏桌面图标
- 勿扰模式（禁用通知）
- 高透明度面板
- 关闭动画效果

### 🚀 一键部署
- 全自动安装脚本
- 自动检测系统环境
- 完整的 Xfce 桌面配置
- Neofetch 系统信息定制

---

## 📦 项目结构

```
DoubaoOS/
├── install.sh                  # 主安装脚本（一键部署）
├── office-mode.sh              # 办公模式切换工具
├── README.md                   # 项目说明文档
├── scripts/                    # 素材生成脚本
│   ├── generate-icons.py       # 图标生成器
│   └── generate-wallpapers.py  # 壁纸生成器
├── themes/                     # 主题资源
│   ├── icons/                  # 图标主题
│   │   └── DoubaoOS-icons/
│   ├── gtk-theme/              # GTK 主题
│   │   └── DoubaoOS-Theme/
│   │       ├── gtk-2.0/
│   │       ├── gtk-3.0/
│   │       ├── xfwm4/
│   │       └── index.theme
│   ├── cursors/                # 光标主题
│   │   └── DoubaoOS-cursors/
│   └── wallpapers/             # 系统壁纸
│       ├── doubaoos-default.svg
│       ├── doubaoos-office.svg
│       ├── doubaoos-dark-tech.svg
│       └── doubaoos-nature.svg
└── config/                     # 配置文件
    ├── xfce/                   # Xfce 桌面配置
    └── office/                 # 办公模式配置
```

---

## 🚀 快速开始

### 环境要求
- Debian 12 (Bookworm) 或兼容版本
- Xfce 桌面环境（脚本会自动安装）
- root 权限（sudo）

### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/dm1366631/A-system-made-by-Doubao.git
cd A-system-made-by-Doubao
```

2. **运行安装脚本**
```bash
sudo ./install.sh
```

3. **注销并重新登录**
   注销当前用户，重新登录以应用所有主题设置。

4. **查看效果**
```bash
neofetch
```

---

## 💼 办公模式使用

### 命令行工具

```bash
# 开启办公模式
doubaoos-office-mode on

# 关闭办公模式
doubaoos-office-mode off

# 切换状态
doubaoos-office-mode toggle

# 查看当前状态
doubaoos-office-mode status

# 查看帮助
doubaoos-office-mode help
```

### 办公模式效果

| 功能 | 默认模式 | 办公模式 |
|------|---------|---------|
| 壁纸 | 蓝色渐变几何 | 极简浅灰 |
| 桌面图标 | 显示 | 隐藏 |
| 通知 | 正常 | 勿扰模式 |
| 面板透明度 | 85% | 95% |
| 动画效果 | 开启 | 关闭 |

### 自定义配置

配置文件位置：`~/.config/doubaoos/office-mode.conf`

```bash
# 编辑配置
nano ~/.config/doubaoos/office-mode.conf
```

---

## 💿 构建 ISO 镜像

如果你想生成可引导的 DoubaoOS ISO 安装镜像：

### 环境要求
- Debian 12 (Bookworm) 系统
- root 权限
- 至少 10GB 可用磁盘空间
- 稳定的网络连接

### 构建步骤

```bash
# 克隆仓库
git clone https://github.com/dm1366631/A-system-made-by-Doubao.git
cd A-system-made-by-Doubao

# 运行构建脚本（需要 root 权限）
sudo ./build-iso.sh
```

### 构建输出

构建完成后，ISO 文件将位于 `output/` 目录：

```
output/
├── DoubaoOS-v1.0-amd64.iso      # 可引导 ISO 镜像
└── DoubaoOS-v1.0-amd64.iso.md5  # MD5 校验文件
```

### ISO 特性
- ✅ 基于 Debian 12 Bookworm
- ✅ Xfce 桌面环境（预装）
- ✅ DoubaoOS 主题（开箱即用）
- ✅ LibreOffice 办公套件
- ✅ Firefox 浏览器
- ✅ 办公模式切换工具
- ✅ 可引导 Live 系统
- ✅ 支持安装到硬盘

---

## 🎨 主题预览

### 图标主题
- 28+ 种系统图标
- 7 种尺寸：16x16 / 24x24 / 32x32 / 48x48 / 64x64 / 128x128 / 256x256
- 覆盖分类：应用、设置、状态、设备、MIME 类型等

### 壁纸集
1. **doubaoos-default** - 蓝色渐变几何（默认）
2. **doubaoos-office** - 极简办公风格
3. **doubaoos-dark-tech** - 深色科技风
4. **doubaoos-nature** - 自然风景风格

### GTK 主题
- 现代圆角设计
- 蓝色主色调
- 完整的控件样式
- 支持 GTK2 / GTK3
- Xfwm4 窗口装饰

---

## 🛠️ 自定义开发

### 重新生成图标

```bash
cd scripts
python3 generate-icons.py
```

### 重新生成壁纸

```bash
cd scripts
python3 generate-wallpapers.py
```

### 修改主题配色

编辑 `themes/gtk-theme/DoubaoOS-Theme/gtk-3.0/gtk.css` 中的颜色变量：

```css
@define-color accent_color #3b82f6;      /* 主色调 */
@define-color accent_bg_color #dbeafe;   /* 主色背景 */
@define-color accent_fg_color #1d4ed8;   /* 主色文字 */
```

---

## 📋 已安装组件

### 桌面环境
- Xfce4 桌面环境
- Xfce4 Goodies 插件包
- Thunar 文件管理器
- Mousepad 文本编辑器
- Ristretto 图片查看器
- Parole 媒体播放器

### 系统工具
- htop - 系统监控
- neofetch - 系统信息展示
- curl / wget - 网络工具
- git - 版本控制
- Python 3 - 运行环境

### 主题相关
- GTK2 引擎
- Murrine 主题引擎
- Pixbuf 主题引擎

---

## 🎯 系统定制内容

### 系统标识
- `/etc/issue` - 登录界面 ASCII Logo
- `/etc/motd` - 登录欢迎信息
- Neofetch 定制配置

### 桌面配置
- GTK 主题设置
- 图标主题设置
- 光标主题设置
- 默认壁纸设置
- 窗口管理器主题
- 面板样式配置

---

## 🔧 故障排除

### 主题没有生效？
1. 确保已注销并重新登录
2. 手动设置主题：`设置 -> 外观`
3. 检查图标缓存：`gtk-update-icon-cache /usr/share/icons/DoubaoOS-icons`

### 办公模式无法切换？
1. 确保使用 Xfce 桌面环境
2. 检查 xfconf-query 是否可用：`which xfconf-query`
3. 查看配置文件：`cat ~/.config/doubaoos/office-mode.state`

### 壁纸没有变化？
1. 手动设置：`设置 -> 桌面 -> 背景`
2. 壁纸位置：`/usr/share/backgrounds/doubaoos/`

---

## 📝 更新日志

### v1.0 (2026-06-27)
- ✨ 初始版本发布
- 🎨 完整的图标主题（28+ 图标 × 7 尺寸）
- 🖼️  4 张系统壁纸
- 🎭 GTK2 / GTK3 完整主题
- 💼 办公模式切换工具
- 🚀 一键安装脚本
- 📊 Neofetch 定制配置
- 🏷️ 系统标识定制

---

## 📄 许可证

MIT License - 详见 LICENSE 文件

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 🙏 致谢

- Debian 项目 - 优秀的 Linux 发行版
- Xfce 桌面环境 - 轻量高效的桌面
- 所有开源软件贡献者

---

**DoubaoOS** - 由豆包 AI 全自主生成的 Debian 定制美化系统 🎉
