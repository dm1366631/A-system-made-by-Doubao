#!/bin/bash
# ============================================================
# DoubaoOS 桌面美化一键安装脚本
# 基于 Debian 12 (Bookworm) + Xfce 桌面环境
# ============================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 系统信息
OS_NAME="DoubaoOS"
OS_VERSION="1.0"
DESKTOP_ENV="Xfce"

# ============================================================
# 工具函数
# ============================================================

print_banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                                                          ║"
    echo "║   ██████╗  ██████╗ ██╗   ██╗██████╗  █████╗  ██████╗    ║"
    echo "║   ██╔══██╗██╔═══██╗██║   ██║██╔══██╗██╔══██╗██╔═══██╗   ║"
    echo "║   ██║  ██║██║   ██║██║   ██║██████╔╝███████║██║   ██║   ║"
    echo "║   ██║  ██║██║   ██║██║   ██║██╔══██╗██╔══██║██║   ██║   ║"
    echo "║   ██████╔╝╚██████╔╝╚██████╔╝██████╔╝██║  ██║╚██████╔╝   ║"
    echo "║   ╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ║"
    echo "║                                                          ║"
    echo "║         Debian 定制美化系统  v${OS_VERSION}                      ║"
    echo "║                                                          ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_root() {
    if [ "$EUID" -ne 0 ]; then
        error "请使用 root 权限运行此脚本"
        info "使用方法: sudo ./install.sh"
        exit 1
    fi
}

check_os() {
    info "检测系统环境..."
    
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        info "操作系统: $PRETTY_NAME"
        
        if [ "$ID" != "debian" ]; then
            warning "此脚本专为 Debian 设计，当前系统为 $ID"
            read -p "是否继续安装？(y/N): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                info "安装已取消"
                exit 0
            fi
        fi
    else
        warning "无法检测操作系统版本"
        read -p "是否继续安装？(y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            info "安装已取消"
            exit 0
        fi
    fi
}

# ============================================================
# 安装函数
# ============================================================

install_dependencies() {
    info "安装系统依赖包..."
    
    apt-get update -qq
    
    # 基础工具
    apt-get install -y -qq \
        curl \
        wget \
        git \
        python3 \
        python3-pip \
        unzip \
        htop \
        neofetch \
        2>/dev/null
    
    # Xfce 桌面环境相关
    apt-get install -y -qq \
        xfce4 \
        xfce4-goodies \
        xfce4-terminal \
        thunar \
        mousepad \
        ristretto \
        parole \
        2>/dev/null
    
    # 主题相关工具
    apt-get install -y -qq \
        gtk2-engines \
        gtk2-engines-murrine \
        gtk2-engines-pixbuf \
        libgtk-3-bin \
        2>/dev/null
    
    success "依赖包安装完成"
}

install_icons() {
    info "安装自定义图标主题..."
    
    local ICONS_DIR="/usr/share/icons"
    local THEME_NAME="DoubaoOS-icons"
    
    # 创建目录
    mkdir -p "$ICONS_DIR"
    
    # 复制图标主题
    cp -r "$SCRIPT_DIR/themes/icons/$THEME_NAME" "$ICONS_DIR/"
    
    # 更新图标缓存
    gtk-update-icon-cache -q -t -f "$ICONS_DIR/$THEME_NAME" 2>/dev/null || true
    
    success "图标主题安装完成: $THEME_NAME"
}

install_gtk_theme() {
    info "安装 GTK 主题..."
    
    local THEMES_DIR="/usr/share/themes"
    local THEME_NAME="DoubaoOS-Theme"
    
    # 创建目录
    mkdir -p "$THEMES_DIR"
    
    # 复制主题
    cp -r "$SCRIPT_DIR/themes/gtk-theme/$THEME_NAME" "$THEMES_DIR/"
    
    success "GTK 主题安装完成: $THEME_NAME"
}

install_cursors() {
    info "安装光标主题..."
    
    local ICONS_DIR="/usr/share/icons"
    local CURSOR_NAME="DoubaoOS-cursors"
    
    # 创建目录
    mkdir -p "$ICONS_DIR"
    
    # 复制光标主题
    cp -r "$SCRIPT_DIR/themes/cursors/$CURSOR_NAME" "$ICONS_DIR/"
    
    success "光标主题安装完成: $CURSOR_NAME"
}

install_wallpapers() {
    info "安装系统壁纸..."
    
    local WALLPAPER_DIR="/usr/share/backgrounds/doubaoos"
    
    # 创建目录
    mkdir -p "$WALLPAPER_DIR"
    
    # 复制壁纸
    cp -r "$SCRIPT_DIR/themes/wallpapers/"* "$WALLPAPER_DIR/"
    
    success "壁纸安装完成，共 $(ls -1 "$WALLPAPER_DIR" | wc -l) 张壁纸"
}

install_office_mode() {
    info "安装办公模式切换工具..."
    
    local BIN_DIR="/usr/local/bin"
    local CONFIG_DIR="/etc/doubaoos"
    
    # 创建配置目录
    mkdir -p "$CONFIG_DIR"
    
    # 复制办公模式脚本
    cp "$SCRIPT_DIR/office-mode.sh" "$BIN_DIR/doubaoos-office-mode"
    chmod +x "$BIN_DIR/doubaoos-office-mode"
    
    # 复制办公模式配置
    cp -r "$SCRIPT_DIR/config/office/"* "$CONFIG_DIR/" 2>/dev/null || true
    
    success "办公模式工具安装完成"
    info "使用方法: doubaoos-office-mode [on|off|status]"
}

configure_xfce() {
    info "配置 Xfce 桌面环境..."
    
    # 获取当前用户（如果用 sudo 运行）
    local USERNAME="${SUDO_USER:-$USER}"
    local HOME_DIR=$(getent passwd "$USERNAME" | cut -d: -f6)
    
    if [ -z "$HOME_DIR" ] || [ ! -d "$HOME_DIR" ]; then
        warning "无法获取用户主目录，跳过用户配置"
        return
    fi
    
    info "配置用户: $USERNAME"
    
    # Xfce 配置目录
    local XFCE_CONFIG="$HOME_DIR/.config/xfce4"
    local GTK_CONFIG="$HOME_DIR/.config/gtk-3.0"
    local GTK2_CONFIG="$HOME_DIR/.gtkrc-2.0"
    
    mkdir -p "$XFCE_CONFIG"
    mkdir -p "$GTK_CONFIG"
    
    # 设置 GTK 主题
    cat > "$GTK_CONFIG/settings.ini" << EOF
[Settings]
gtk-theme-name=DoubaoOS-Theme
gtk-icon-theme-name=DoubaoOS-icons
gtk-cursor-theme-name=DoubaoOS-cursors
gtk-cursor-theme-size=24
gtk-font-name=Sans 10
gtk-application-prefer-dark-theme=0
gtk-decoration-layout=:minimize,maximize,close
EOF
    
    # 设置 GTK2 主题
    cat > "$GTK2_CONFIG" << EOF
# DO NOT EDIT! This file will be overwritten by LXAppearance.
# Any customizations should be kept in ~/.gtkrc-2.0.mine

include "/usr/share/themes/DoubaoOS-Theme/gtk-2.0/gtkrc"
gtk-icon-theme-name="DoubaoOS-icons"
gtk-font-name="Sans 10"
gtk-cursor-theme-name="DoubaoOS-cursors"
gtk-cursor-theme-size=24
gtk-toolbar-style=GTK_TOOLBAR_ICONS
gtk-toolbar-icon-size=GTK_ICON_SIZE_LARGE_TOOLBAR
gtk-button-images=1
gtk-menu-images=1
gtk-enable-event-sounds=1
gtk-enable-input-feedback-sounds=0
gtk-xft-antialias=1
gtk-xft-hinting=1
gtk-xft-hintstyle="hintslight"
gtk-xft-rgba="rgb"
EOF
    
    # 设置默认壁纸
    local DEFAULT_WALLPAPER="/usr/share/backgrounds/doubaoos/doubaoos-default.svg"
    
    # Xfce 桌面属性配置
    mkdir -p "$XFCE_CONFIG/xfconf/xfce-perchannel-xml"
    
    cat > "$XFCE_CONFIG/xfconf/xfce-perchannel-xml/xfce4-desktop.xml" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>

<channel name="xfce4-desktop" version="1.0">
  <property name="backdrop" type="empty">
    <property name="screen0" type="empty">
      <property name="monitor0" type="empty">
        <property name="workspace0" type="empty">
          <property name="color-style" type="int" value="0"/>
          <property name="image-style" type="int" value="5"/>
          <property name="last-image" type="string" value="/usr/share/backgrounds/doubaoos/doubaoos-default.svg"/>
        </property>
      </property>
    </property>
  </property>
</channel>
EOF
    
    # 设置窗口管理器主题
    cat > "$XFCE_CONFIG/xfconf/xfce-perchannel-xml/xfwm4.xml" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>

<channel name="xfwm4" version="1.0">
  <property name="general" type="empty">
    <property name="theme" type="string" value="DoubaoOS-Theme"/>
    <property name="title_font" type="string" value="Sans Bold 10"/>
    <property name="button_layout" type="string" value="|HMC"/>
  </property>
</channel>
EOF
    
    # 设置面板配置
    cat > "$XFCE_CONFIG/xfconf/xfce-perchannel-xml/xfce4-panel.xml" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>

<channel name="xfce4-panel" version="1.0">
  <property name="panels" type="empty">
    <property name="panel-1" type="empty">
      <property name="position" type="string" value="p=6;x=0;y=0"/>
      <property name="size" type="int" value="32"/>
      <property name="background-style" type="int" value="1"/>
      <property name="background-color" type="array">
        <value type="double" value="0.11764705882352941"/>
        <value type="double" value="0.1607843137254902"/>
        <value type="double" value="0.23529411764705882"/>
        <value type="double" value="0.95"/>
      </property>
    </property>
  </property>
</channel>
EOF
    
    # 修复权限
    chown -R "$USERNAME:$USERNAME" "$HOME_DIR/.config" 2>/dev/null || true
    chown "$USERNAME:$USERNAME" "$GTK2_CONFIG" 2>/dev/null || true
    
    success "Xfce 桌面配置完成"
}

install_neofetch_config() {
    info "配置 Neofetch..."
    
    local USERNAME="${SUDO_USER:-$USER}"
    local HOME_DIR=$(getent passwd "$USERNAME" | cut -d: -f6)
    
    if [ -z "$HOME_DIR" ] || [ ! -d "$HOME_DIR" ]; then
        return
    fi
    
    local NEOFETCH_CONFIG="$HOME_DIR/.config/neofetch"
    mkdir -p "$NEOFETCH_CONFIG"
    
    cat > "$NEOFETCH_CONFIG/config.conf" << EOF
# Neofetch 配置 - DoubaoOS 定制

# 显示信息
print_info() {
    info title
    info underline

    info "OS" distro
    info "Host" model
    info "Kernel" kernel
    info "Uptime" uptime
    info "Packages" packages
    info "Shell" shell
    info "Resolution" resolution
    info "DE" de
    info "WM" wm
    info "Theme" theme
    info "Icons" icons
    info "Terminal" term
    info "CPU" cpu
    info "Memory" memory
}

# 颜色
colors=(distro)

# 分隔符
separator=":"

# 标题颜色
title_color="4"

# 副标题颜色
subtitle_color="4"

# 章节颜色
colon_color="4"

# 信息颜色
info_color="7"

# 架构颜色
arch_color="3"

# 启用彩色方块
color_blocks="on"

# 方块宽度
block_width=3

# 方块高度
block_height=1

# 方块范围
block_range=(0 15)

# 分隔符颜色
col_offset="auto"
EOF
    
    chown -R "$USERNAME:$USERNAME" "$HOME_DIR/.config/neofetch" 2>/dev/null || true
    
    success "Neofetch 配置完成"
}

install_issue() {
    info "配置系统标识..."
    
    # /etc/issue
    cat > /etc/issue << 'EOF'
[H[2J
  ██████╗  ██████╗ ██╗   ██╗██████╗  █████╗  ██████╗ ███████╗
  ██╔══██╗██╔═══██╗██║   ██║██╔══██╗██╔══██╗██╔═══██╗██╔════╝
  ██║  ██║██║   ██║██║   ██║██████╔╝███████║██║   ██║███████╗
  ██║  ██║██║   ██║██║   ██║██╔══██╗██╔══██║██║   ██║╚════██║
  ██████╔╝╚██████╔╝╚██████╔╝██████╔╝██║  ██║╚██████╔╝███████║
  ╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝

  Debian 定制美化系统  v1.0

  系统: \n
  内核: \r
  主机: \m

EOF
    
    # /etc/motd
    cat > /etc/motd << 'EOF'
Welcome to DoubaoOS - Debian Custom Edition!

  快速开始:
  • 切换办公模式: doubaoos-office-mode on
  • 查看系统信息: neofetch
  • 主题设置: 外观设置

  Enjoy your customized desktop experience!

EOF
    
    success "系统标识配置完成"
}

# ============================================================
# 主函数
# ============================================================

main() {
    print_banner
    
    # 检查权限
    check_root
    
    # 检查系统
    check_os
    
    echo
    info "开始安装 DoubaoOS 桌面美化..."
    echo
    
    # 安装步骤
    install_dependencies
    echo
    
    install_icons
    install_gtk_theme
    install_cursors
    install_wallpapers
    echo
    
    install_office_mode
    echo
    
    configure_xfce
    install_neofetch_config
    install_issue
    echo
    
    # 完成
    success "═══════════════════════════════════════════════════════════"
    success "  DoubaoOS 桌面美化安装完成！"
    success "═══════════════════════════════════════════════════════════"
    echo
    info "请注销并重新登录以应用所有主题设置"
    echo
    info "快速命令:"
    info "  • 开启办公模式: doubaoos-office-mode on"
    info "  • 关闭办公模式: doubaoos-office-mode off"
    info "  • 查看系统信息: neofetch"
    echo
}

# 运行主函数
main "$@"
