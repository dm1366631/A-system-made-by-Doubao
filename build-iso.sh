#!/bin/bash
#
# DoubaoOS ISO 构建脚本
# 使用 Debian live-build 系统构建可引导 ISO
#
# 使用方法: sudo ./build-iso.sh
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 打印 Banner
print_banner() {
    echo -e "${CYAN}"
    echo "  ____                        ___  ____  "
    echo " |  _ \  ___  _   _  __ _   / _ \/ ___| "
    echo " | | | |/ _ \| | | |/ _' | | | | \___ \ "
    echo " | |_| | (_) | |_| | (_| | | |_| |___) |"
    echo " |____/ \___/ \__,_|\__,_|  \___/|____/ "
    echo ""
    echo "        DoubaoOS ISO 构建工具 v1.0"
    echo -e "${NC}"
    echo ""
}

# 检查 root 权限
check_root() {
    if [ "$EUID" -ne 0 ]; then
        echo -e "${RED}❌ 请使用 root 权限运行此脚本${NC}"
        echo "   使用方法: sudo ./build-iso.sh"
        exit 1
    fi
}

# 检查系统
check_system() {
    echo -e "${BLUE}🔍 检查系统环境...${NC}"
    
    if [ ! -f /etc/debian_version ]; then
        echo -e "${RED}❌ 此脚本只能在 Debian 系统上运行${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Debian 系统检测通过${NC}"
    echo ""
}

# 安装依赖
install_dependencies() {
    echo -e "${BLUE}📦 安装构建依赖...${NC}"
    
    apt-get update -qq
    apt-get install -y -qq \
        live-build \
        debootstrap \
        squashfs-tools \
        xorriso \
        isolinux \
        syslinux-common \
        2>&1 | tail -3
    
    echo -e "${GREEN}✅ 依赖安装完成${NC}"
    echo ""
}

# 准备构建目录
prepare_build_dir() {
    echo -e "${BLUE}📁 准备构建目录...${NC}"
    
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    BUILD_DIR="${SCRIPT_DIR}/build/iso-build"
    
    # 清理旧的构建目录
    if [ -d "$BUILD_DIR" ]; then
        echo -e "${YELLOW}   清理旧的构建目录...${NC}"
        rm -rf "$BUILD_DIR"
    fi
    
    mkdir -p "$BUILD_DIR"
    cd "$BUILD_DIR"
    
    echo -e "${GREEN}✅ 构建目录已准备: ${BUILD_DIR}${NC}"
    echo ""
}

# 配置 live-build
configure_live_build() {
    echo -e "${BLUE}⚙️  配置 live-build...${NC}"
    
    # 初始化 live-build 配置
    lb config noauto \
        --distribution bookworm \
        --archive-areas "main contrib non-free non-free-firmware" \
        --architectures amd64 \
        --binary-images iso-hybrid \
        --bootloader syslinux \
        --debian-installer live \
        --debian-installer-distribution bookworm \
        --system live \
        --zsync false \
        --apt-indices false \
        --memtest none \
        2>&1 | tail -3
    
    echo -e "${GREEN}✅ live-build 配置完成${NC}"
    echo ""
}

# 添加软件包列表
add_package_lists() {
    echo -e "${BLUE}📋 配置软件包列表...${NC}"
    
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    BUILD_DIR="${SCRIPT_DIR}/build/iso-build"
    
    # 创建软件包列表
    cat > "${BUILD_DIR}/config/package-lists/doubaoos.list.chroot" << 'EOF'
# 桌面环境
xfce4
xfce4-goodies
lightdm

# 主题引擎
gtk2-engines
gtk2-engines-pixbuf
gtk3-engines-xfce

# 系统工具
sudo
bash-completion
htop
neofetch
git
curl
wget
vim
nano

# 办公软件
libreoffice
libreoffice-gtk3
thunderbird

# 网络工具
firefox-esr
network-manager
network-manager-gnome

# 多媒体
pulseaudio
pavucontrol
xfce4-pulseaudio-plugin

# 文件管理
thunar
thunar-archive-plugin
file-roller

# 其他
fonts-noto-cjk
fonts-dejavu
dbus-x11
policykit-1-gnome
EOF
    
    echo -e "${GREEN}✅ 软件包列表已添加${NC}"
    echo ""
}

# 复制 DoubaoOS 定制内容
copy_custom_content() {
    echo -e "${BLUE}🎨 复制 DoubaoOS 定制内容...${NC}"
    
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    BUILD_DIR="${SCRIPT_DIR}/build/iso-build"
    CHROOT_DIR="${BUILD_DIR}/config/includes.chroot"
    
    # 创建目录结构
    mkdir -p "${CHROOT_DIR}/usr/share/icons"
    mkdir -p "${CHROOT_DIR}/usr/share/themes"
    mkdir -p "${CHROOT_DIR}/usr/share/backgrounds/doubaoos"
    mkdir -p "${CHROOT_DIR}/usr/local/bin"
    mkdir -p "${CHROOT_DIR}/etc/skel/.config"
    mkdir -p "${CHROOT_DIR}/etc/skel/.config/doubaoos"
    
    # 复制图标主题
    if [ -d "${SCRIPT_DIR}/themes/icons/DoubaoOS-icons" ]; then
        cp -r "${SCRIPT_DIR}/themes/icons/DoubaoOS-icons" "${CHROOT_DIR}/usr/share/icons/"
        echo -e "${GREEN}   ✅ 图标主题已复制${NC}"
    fi
    
    # 复制 GTK 主题
    if [ -d "${SCRIPT_DIR}/themes/gtk-theme/DoubaoOS-Theme" ]; then
        cp -r "${SCRIPT_DIR}/themes/gtk-theme/DoubaoOS-Theme" "${CHROOT_DIR}/usr/share/themes/"
        echo -e "${GREEN}   ✅ GTK 主题已复制${NC}"
    fi
    
    # 复制光标主题
    if [ -d "${SCRIPT_DIR}/themes/cursors/DoubaoOS-cursors" ]; then
        cp -r "${SCRIPT_DIR}/themes/cursors/DoubaoOS-cursors" "${CHROOT_DIR}/usr/share/icons/"
        echo -e "${GREEN}   ✅ 光标主题已复制${NC}"
    fi
    
    # 复制壁纸
    if [ -d "${SCRIPT_DIR}/themes/wallpapers" ]; then
        cp "${SCRIPT_DIR}/themes/wallpapers/"*.svg "${CHROOT_DIR}/usr/share/backgrounds/doubaoos/"
        echo -e "${GREEN}   ✅ 壁纸已复制${NC}"
    fi
    
    # 复制办公模式脚本
    if [ -f "${SCRIPT_DIR}/office-mode.sh" ]; then
        cp "${SCRIPT_DIR}/office-mode.sh" "${CHROOT_DIR}/usr/local/bin/doubaoos-office-mode"
        chmod +x "${CHROOT_DIR}/usr/local/bin/doubaoos-office-mode"
        echo -e "${GREEN}   ✅ 办公模式脚本已复制${NC}"
    fi
    
    echo -e "${GREEN}✅ DoubaoOS 定制内容复制完成${NC}"
    echo ""
}

# 添加自动配置脚本
add_auto_config() {
    echo -e "${BLUE}⚙️  添加自动配置脚本...${NC}"
    
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    BUILD_DIR="${SCRIPT_DIR}/build/iso-build"
    HOOKS_DIR="${BUILD_DIR}/config/hooks/normal"
    
    mkdir -p "$HOOKS_DIR"
    
    # 创建配置钩子
    cat > "${HOOKS_DIR}/01-doubaoos-config.hook.chroot" << 'EOF'
#!/bin/bash
# DoubaoOS 系统配置钩子

set -e

# 更新图标缓存
gtk-update-icon-cache -q -t -f /usr/share/icons/DoubaoOS-icons 2>/dev/null || true

# 创建默认用户配置目录
mkdir -p /etc/skel/.config/xfce4
mkdir -p /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml

# Xfce 外观配置
cat > /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/xsettings.xml << 'XSETTINGS'
<?xml version="1.0" encoding="UTF-8"?>
<channel name="xsettings" version="1.0">
  <property name="Net" type="empty">
    <property name="ThemeName" type="string" value="DoubaoOS-Theme"/>
    <property name="IconThemeName" type="string" value="DoubaoOS-icons"/>
    <property name="CursorThemeName" type="string" value="DoubaoOS-cursors"/>
    <property name="CursorThemeSize" type="int" value="24"/>
  </property>
  <property name="Xft" type="empty">
    <property name="DPI" type="int" value="96"/>
    <property name="Antialias" type="int" value="1"/>
    <property name="HintStyle" type="string" value="hintslight"/>
    <property name="RGBA" type="string" value="rgb"/>
  </property>
</channel>
XSETTINGS

# 桌面壁纸配置
cat > /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml << 'DESKTOP'
<?xml version="1.0" encoding="UTF-8"?>
<channel name="xfce4-desktop" version="1.0">
  <property name="backdrop" type="empty">
    <property name="screen0" type="empty">
      <property name="monitor0" type="empty">
        <property name="workspace0" type="empty">
          <property name="last-image" type="string" value="/usr/share/backgrounds/doubaoos/doubaoos-default.svg"/>
          <property name="image-style" type="int" value="5"/>
        </property>
      </property>
    </property>
  </property>
</channel>
DESKTOP

# 窗口管理器主题配置
cat > /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/xfwm4.xml << 'XFWM'
<?xml version="1.0" encoding="UTF-8"?>
<channel name="xfwm4" version="1.0">
  <property name="general" type="empty">
    <property name="theme" type="string" value="DoubaoOS-Theme"/>
  </property>
</channel>
XFWM

# 创建系统标识
cat > /etc/issue << 'ISSUE'
  ____                        ___  ____  
 |  _ \  ___  _   _  __ _   / _ \/ ___| 
 | | | |/ _ \| | | |/ _' | | | | \___ \ 
 | |_| | (_) | |_| | (_| | | |_| |___) |
 |____/ \___/ \__,_|\__,_|  \___/|____/ 

 DoubaoOS v1.0 - 基于 Debian 的定制美化系统

 \n \l

ISSUE

# 创建 motd
cat > /etc/motd << 'MOTD'
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   ____                        ___  ____                 ║
║  |  _ \  ___  _   _  __ _   / _ \/ ___|                ║
║  | | | |/ _ \| | | |/ _' | | | | \___ \                ║
║  | |_| | (_) | |_| | (_| | | |_| |___) |               ║
║  |____/ \___/ \__,_|\__,_|  \___/|____/                 ║
║                                                          ║
║         DoubaoOS v1.0 - 由豆包AI打造                     ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

  办公模式: doubaoos-office-mode help

MOTD

echo "DoubaoOS 配置完成！"
EOF
    
    chmod +x "${HOOKS_DIR}/01-doubaoos-config.hook.chroot"
    
    echo -e "${GREEN}✅ 自动配置脚本已添加${NC}"
    echo ""
}

# 构建 ISO
build_iso() {
    echo -e "${BLUE}🔨 开始构建 ISO...${NC}"
    echo -e "${YELLOW}   这可能需要较长时间，请耐心等待...${NC}"
    echo ""
    
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    BUILD_DIR="${SCRIPT_DIR}/build/iso-build"
    
    cd "$BUILD_DIR"
    
    # 开始构建
    lb build 2>&1 | tee "${SCRIPT_DIR}/build/build.log" | tail -20
    
    # 检查结果
    if [ -f "${BUILD_DIR}/live-image-amd64.hybrid.iso" ]; then
        echo ""
        echo -e "${GREEN}✅ ISO 构建成功！${NC}"
        
        # 移动到输出目录
        OUTPUT_DIR="${SCRIPT_DIR}/output"
        mkdir -p "$OUTPUT_DIR"
        
        ISO_NAME="DoubaoOS-v1.0-amd64.iso"
        mv "${BUILD_DIR}/live-image-amd64.hybrid.iso" "${OUTPUT_DIR}/${ISO_NAME}"
        
        # 计算 MD5
        md5sum "${OUTPUT_DIR}/${ISO_NAME}" > "${OUTPUT_DIR}/${ISO_NAME}.md5"
        
        # 显示文件信息
        ISO_SIZE=$(du -h "${OUTPUT_DIR}/${ISO_NAME}" | cut -f1)
        echo ""
        echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
        echo -e "${CYAN}  ISO 文件信息${NC}"
        echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
        echo -e "  📄 文件名: ${GREEN}${ISO_NAME}${NC}"
        echo -e "  📁 位置: ${GREEN}${OUTPUT_DIR}/${ISO_NAME}${NC}"
        echo -e "  📦 大小: ${GREEN}${ISO_SIZE}${NC}"
        echo -e "  🔐 MD5: ${GREEN}$(cat "${OUTPUT_DIR}/${ISO_NAME}.md5" | cut -d' ' -f1)${NC}"
        echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
        
    else
        echo ""
        echo -e "${RED}❌ ISO 构建失败${NC}"
        echo -e "${YELLOW}   请查看构建日志: ${SCRIPT_DIR}/build/build.log${NC}"
        exit 1
    fi
}

# 主函数
main() {
    print_banner
    check_root
    check_system
    install_dependencies
    prepare_build_dir
    configure_live_build
    add_package_lists
    copy_custom_content
    add_auto_config
    build_iso
    
    echo ""
    echo -e "${GREEN}🎉 DoubaoOS ISO 构建完成！${NC}"
    echo ""
}

main "$@"
