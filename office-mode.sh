#!/bin/bash
# ============================================================
# DoubaoOS 办公模式切换工具
# 一键切换办公/娱乐模式，优化桌面环境
# ============================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 配置文件
CONFIG_FILE="$HOME/.config/doubaoos/office-mode.conf"
STATE_FILE="$HOME/.config/doubaoos/office-mode.state"

# 确保配置目录存在
mkdir -p "$(dirname "$CONFIG_FILE")"
mkdir -p "$(dirname "$STATE_FILE")"

# 默认配置
DEFAULT_CONFIG='
# DoubaoOS 办公模式配置

# 办公模式壁纸
OFFICE_WALLPAPER="/usr/share/backgrounds/doubaoos/doubaoos-office.svg"

# 默认壁纸
DEFAULT_WALLPAPER="/usr/share/backgrounds/doubaoos/doubaoos-default.svg"

# 办公模式是否隐藏桌面图标
OFFICE_HIDE_DESKTOP_ICONS=true

# 办公模式面板透明度 (0-1)
OFFICE_PANEL_OPACITY=0.95

# 默认面板透明度
DEFAULT_PANEL_OPACITY=0.85

# 办公模式是否禁用通知
OFFICE_DISABLE_NOTIFICATIONS=true

# 办公模式自动启动的应用
OFFICE_AUTOSTART_APPS=("libreoffice-writer" "thunderbird")

# 默认自动启动的应用
DEFAULT_AUTOSTART_APPS=()
'

# ============================================================
# 工具函数
# ============================================================

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

load_config() {
    if [ ! -f "$CONFIG_FILE" ]; then
        echo "$DEFAULT_CONFIG" > "$CONFIG_FILE"
    fi
    source "$CONFIG_FILE"
}

get_state() {
    if [ -f "$STATE_FILE" ]; then
        cat "$STATE_FILE"
    else
        echo "off"
    fi
}

set_state() {
    echo "$1" > "$STATE_FILE"
}

# ============================================================
# 办公模式功能函数
# ============================================================

set_wallpaper() {
    local wallpaper="$1"
    
    info "设置壁纸: $wallpaper"
    
    # 使用 xfconf 设置 Xfce 壁纸
    if command -v xfconf-query &> /dev/null; then
        xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/workspace0/last-image -s "$wallpaper" 2>/dev/null || true
        xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/workspace0/image-style -s 5 2>/dev/null || true
    fi
    
    # 尝试其他方式
    if command -v feh &> /dev/null; then
        feh --bg-scale "$wallpaper" 2>/dev/null || true
    fi
}

set_panel_opacity() {
    local opacity="$1"
    
    info "设置面板透明度: $opacity"
    
    if command -v xfconf-query &> /dev/null; then
        # 转换为 rgba 格式
        local alpha=$(echo "$opacity" | bc -l 2>/dev/null || echo "0.95")
        
        xfconf-query -c xfce4-panel -p /panels/panel-1/background-style -s 1 2>/dev/null || true
        
        # 设置背景颜色和透明度
        xfconf-query -c xfce4-panel -p /panels/panel-1/background-color -s 0.117647 -s 0.160784 -s 0.235294 -s "$alpha" 2>/dev/null || true
    fi
}

toggle_desktop_icons() {
    local hide="$1"
    
    if [ "$hide" = true ]; then
        info "隐藏桌面图标"
    else
        info "显示桌面图标"
    fi
    
    if command -v xfconf-query &> /dev/null; then
        if [ "$hide" = true ]; then
            xfconf-query -c xfce4-desktop -p /desktop-icons/file-icons/show-filesystem -s false 2>/dev/null || true
            xfconf-query -c xfce4-desktop -p /desktop-icons/file-icons/show-home -s false 2>/dev/null || true
            xfconf-query -c xfce4-desktop -p /desktop-icons/file-icons/show-trash -s false 2>/dev/null || true
            xfconf-query -c xfce4-desktop -p /desktop-icons/file-icons/show-removable -s false 2>/dev/null || true
        else
            xfconf-query -c xfce4-desktop -p /desktop-icons/file-icons/show-filesystem -s true 2>/dev/null || true
            xfconf-query -c xfce4-desktop -p /desktop-icons/file-icons/show-home -s true 2>/dev/null || true
            xfconf-query -c xfce4-desktop -p /desktop-icons/file-icons/show-trash -s true 2>/dev/null || true
            xfconf-query -c xfce4-desktop -p /desktop-icons/file-icons/show-removable -s true 2>/dev/null || true
        fi
    fi
}

toggle_notifications() {
    local disable="$1"
    
    if [ "$disable" = true ]; then
        info "禁用桌面通知"
    else
        info "启用桌面通知"
    fi
    
    if command -v xfconf-query &> /dev/null; then
        if [ "$disable" = true ]; then
            xfconf-query -c xfce4-notifyd -p /do-not-disturb -s true 2>/dev/null || true
        else
            xfconf-query -c xfce4-notifyd -p /do-not-disturb -s false 2>/dev/null || true
        fi
    fi
}

set_gtk_theme_variant() {
    local mode="$1"
    
    info "切换 GTK 主题模式: $mode"
    
    local GTK_CONFIG="$HOME/.config/gtk-3.0/settings.ini"
    mkdir -p "$(dirname "$GTK_CONFIG")"
    
    if [ "$mode" = "office" ]; then
        # 办公模式：更简洁的配色
        cat > "$GTK_CONFIG" << EOF
[Settings]
gtk-theme-name=DoubaoOS-Theme
gtk-icon-theme-name=DoubaoOS-icons
gtk-cursor-theme-name=DoubaoOS-cursors
gtk-cursor-theme-size=24
gtk-font-name=Sans 10
gtk-application-prefer-dark-theme=0
gtk-decoration-layout=:minimize,maximize,close
gtk-enable-animations=0
EOF
    else
        # 默认模式
        cat > "$GTK_CONFIG" << EOF
[Settings]
gtk-theme-name=DoubaoOS-Theme
gtk-icon-theme-name=DoubaoOS-icons
gtk-cursor-theme-name=DoubaoOS-cursors
gtk-cursor-theme-size=24
gtk-font-name=Sans 10
gtk-application-prefer-dark-theme=0
gtk-decoration-layout=:minimize,maximize,close
gtk-enable-animations=1
EOF
    fi
}

restart_xfce_panel() {
    info "重启 Xfce 面板..."
    if command -v xfce4-panel &> /dev/null; then
        xfce4-panel -r 2>/dev/null || true
    fi
}

# ============================================================
# 模式切换函数
# ============================================================

enable_office_mode() {
    echo
    info "═══════════════════════════════════════════════════════════"
    info "  正在开启办公模式..."
    info "═══════════════════════════════════════════════════════════"
    echo
    
    # 加载配置
    load_config
    
    # 设置办公壁纸
    set_wallpaper "$OFFICE_WALLPAPER"
    
    # 设置面板透明度
    set_panel_opacity "$OFFICE_PANEL_OPACITY"
    
    # 隐藏桌面图标
    toggle_desktop_icons "$OFFICE_HIDE_DESKTOP_ICONS"
    
    # 禁用通知
    toggle_notifications "$OFFICE_DISABLE_NOTIFICATIONS"
    
    # 切换主题模式
    set_gtk_theme_variant "office"
    
    # 重启面板
    restart_xfce_panel
    
    # 保存状态
    set_state "on"
    
    echo
    success "═══════════════════════════════════════════════════════════"
    success "  ✅ 办公模式已开启！"
    success "═══════════════════════════════════════════════════════════"
    echo
    info "  • 壁纸已切换为极简办公风格"
    info "  • 桌面图标已隐藏"
    info "  • 通知已静音"
    info "  • 面板透明度已调整"
    info "  • 动画效果已关闭"
    echo
    info "专注工作，效率翻倍！💼"
    echo
}

disable_office_mode() {
    echo
    info "═══════════════════════════════════════════════════════════"
    info "  正在关闭办公模式..."
    info "═══════════════════════════════════════════════════════════"
    echo
    
    # 加载配置
    load_config
    
    # 恢复默认壁纸
    set_wallpaper "$DEFAULT_WALLPAPER"
    
    # 恢复面板透明度
    set_panel_opacity "$DEFAULT_PANEL_OPACITY"
    
    # 显示桌面图标
    toggle_desktop_icons false
    
    # 启用通知
    toggle_notifications false
    
    # 恢复主题模式
    set_gtk_theme_variant "default"
    
    # 重启面板
    restart_xfce_panel
    
    # 保存状态
    set_state "off"
    
    echo
    success "═══════════════════════════════════════════════════════════"
    success "  ✅ 办公模式已关闭！"
    success "═══════════════════════════════════════════════════════════"
    echo
    info "  • 壁纸已恢复默认"
    info "  • 桌面图标已显示"
    info "  • 通知已恢复"
    info "  • 面板透明度已恢复"
    info "  • 动画效果已开启"
    echo
    info "欢迎回来，享受你的桌面！🎉"
    echo
}

show_status() {
    local state=$(get_state)
    
    echo
    info "═══════════════════════════════════════════════════════════"
    info "  办公模式状态"
    info "═══════════════════════════════════════════════════════════"
    echo
    
    if [ "$state" = "on" ]; then
        echo -e "  状态: ${GREEN}● 已开启${NC}"
        echo
        info "当前配置:"
        info "  • 极简办公壁纸"
        info "  • 隐藏桌面图标"
        info "  • 勿扰模式"
        info "  • 高透明度面板"
    else
        echo -e "  状态: ${RED}○ 已关闭${NC}"
        echo
        info "当前配置:"
        info "  • 默认主题壁纸"
        info "  • 显示桌面图标"
        info "  • 正常通知"
        info "  • 标准面板透明度"
    fi
    
    echo
    info "使用方法:"
    info "  doubaoos-office-mode on     # 开启办公模式"
    info "  doubaoos-office-mode off    # 关闭办公模式"
    info "  doubaoos-office-mode toggle # 切换办公模式"
    info "  doubaoos-office-mode status # 查看当前状态"
    echo
}

show_help() {
    echo
    echo "DoubaoOS 办公模式切换工具 v1.0"
    echo
    echo "用法: doubaoos-office-mode [命令]"
    echo
    echo "命令:"
    echo "  on        开启办公模式"
    echo "  off       关闭办公模式"
    echo "  toggle    切换办公模式状态"
    echo "  status    查看当前办公模式状态"
    echo "  help      显示此帮助信息"
    echo
    echo "配置文件: $CONFIG_FILE"
    echo
}

# ============================================================
# 主函数
# ============================================================

main() {
    local command="${1:-status}"
    
    case "$command" in
        on)
            enable_office_mode
            ;;
        off)
            disable_office_mode
            ;;
        toggle)
            local state=$(get_state)
            if [ "$state" = "on" ]; then
                disable_office_mode
            else
                enable_office_mode
            fi
            ;;
        status)
            show_status
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            error "未知命令: $command"
            echo
            show_help
            exit 1
            ;;
    esac
}

main "$@"
