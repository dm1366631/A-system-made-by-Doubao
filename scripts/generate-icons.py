#!/usr/bin/env python3
"""
DoubaoOS 自定义图标生成器
自主生成全套 SVG 矢量图标，无外部素材依赖
"""

import os
import math

ICON_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "themes", "icons", "DoubaoOS-icons")

# 图标尺寸规格
SIZES = [16, 24, 32, 48, 64, 128, 256]

# 主题配色
COLORS = {
    "primary": "#3b82f6",
    "primary_dark": "#1d4ed8",
    "primary_light": "#93c5fd",
    "accent": "#06b6d4",
    "success": "#10b981",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "white": "#ffffff",
    "gray": "#6b7280",
    "gray_light": "#e5e7eb",
    "bg_dark": "#1e293b",
    "bg_medium": "#334155",
}

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def svg_header(size):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">'''

def svg_footer():
    return '</svg>'

def gen_gradient(dwg, gid, c1, c2, x1=0, y1=0, x2=1, y2=1):
    dwg.append(f'<defs><linearGradient id="{gid}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">')
    dwg.append(f'<stop offset="0%" stop-color="{c1}"/>')
    dwg.append(f'<stop offset="100%" stop-color="{c2}"/>')
    dwg.append('</linearGradient></defs>')

# ========== 各类图标生成函数 ==========

def icon_folder(size):
    """文件夹图标"""
    dwg = []
    gen_gradient(dwg, "g1", COLORS["primary"], COLORS["primary_dark"])
    dwg.append(svg_header(size))
    
    s = size
    # 文件夹主体
    dwg.append(f'<rect x="{s*0.1}" y="{s*0.25}" width="{s*0.8}" height="{s*0.6}" rx="{s*0.06}" fill="url(#g1)"/>')
    # 文件夹标签
    dwg.append(f'<rect x="{s*0.1}" y="{s*0.18}" width="{s*0.35}" height="{s*0.12}" rx="{s*0.04}" fill="{COLORS["primary_light"]}"/>')
    # 高光
    dwg.append(f'<rect x="{s*0.15}" y="{s*0.3}" width="{s*0.7}" height="{s*0.08}" rx="{s*0.02}" fill="white" opacity="0.2"/>')
    
    dwg.append(svg_footer())
    return '\n'.join(dwg)

def icon_terminal(size):
    """终端图标"""
    dwg = []
    gen_gradient(dwg, "g1", COLORS["bg_dark"], COLORS["bg_medium"])
    dwg.append(svg_header(size))
    
    s = size
    # 窗口背景
    dwg.append(f'<rect x="{s*0.08}" y="{s*0.15}" width="{s*0.84}" height="{s*0.7}" rx="{s*0.06}" fill="url(#g1)"/>')
    # 标题栏
    dwg.append(f'<rect x="{s*0.08}" y="{s*0.15}" width="{s*0.84}" height="{s*0.12}" rx="{s*0.06}" fill="{COLORS["bg_medium"]}"/>')
    # 窗口按钮
    colors = [COLORS["danger"], COLORS["warning"], COLORS["success"]]
    for i, c in enumerate(colors):
        dwg.append(f'<circle cx="{s*(0.15+i*0.08)}" cy="{s*0.21}" r="{s*0.025}" fill="{c}"/>')
    # 命令提示符
    dwg.append(f'<text x="{s*0.15}" y="{s*0.45}" font-family="monospace" font-size="{s*0.18}" fill="{COLORS["success"]}">$</text>')
    # 光标
    dwg.append(f'<rect x="{s*0.25}" y="{s*0.32}" width="{s*0.06}" height="{s*0.15}" fill="{COLORS["primary_light"]}">')
    dwg.append('<animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/>')
    dwg.append('</rect>')
    
    dwg.append(svg_footer())
    return '\n'.join(dwg)

def icon_settings(size):
    """设置图标（齿轮）"""
    dwg = []
    gen_gradient(dwg, "g1", COLORS["gray"], COLORS["bg_medium"])
    dwg.append(svg_header(size))
    
    s = size
    cx, cy = s/2, s/2
    r_outer = s * 0.38
    r_inner = s * 0.22
    
    # 齿轮齿
    teeth = 8
    for i in range(teeth):
        angle = i * (2 * math.pi / teeth)
        x1 = cx + r_outer * math.cos(angle)
        y1 = cy + r_outer * math.sin(angle)
        x2 = cx + (r_outer + s*0.08) * math.cos(angle)
        y2 = cy + (r_outer + s*0.08) * math.sin(angle)
        dwg.append(f'<rect x="{x2-s*0.04}" y="{y2-s*0.04}" width="{s*0.08}" height="{s*0.08}" rx="{s*0.015}" fill="url(#g1)" transform="rotate({i*45} {x2} {y2})"/>')
    
    # 齿轮主体
    dwg.append(f'<circle cx="{cx}" cy="{cy}" r="{r_outer}" fill="url(#g1)"/>')
    dwg.append(f'<circle cx="{cx}" cy="{cy}" r="{r_inner}" fill="{COLORS["bg_dark"]}"/>')
    dwg.append(f'<circle cx="{cx}" cy="{cy}" r="{r_inner*0.5}" fill="{COLORS["primary"]}"/>')
    
    dwg.append(svg_footer())
    return '\n'.join(dwg)

def icon_browser(size):
    """浏览器图标"""
    dwg = []
    gen_gradient(dwg, "g1", COLORS["primary"], COLORS["accent"])
    dwg.append(svg_header(size))
    
    s = size
    cx, cy = s/2, s/2
    
    # 外圆
    dwg.append(f'<circle cx="{cx}" cy="{cy}" r="{s*0.42}" fill="url(#g1)"/>')
    # 内圆（白色背景）
    dwg.append(f'<circle cx="{cx}" cy="{cy}" r="{s*0.32}" fill="white"/>')
    # 地球经纬线
    dwg.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{s*0.32}" ry="{s*0.1}" fill="none" stroke="{COLORS["primary_light"]}" stroke-width="{s*0.02}"/>')
    dwg.append(f'<line x1="{cx}" y1="{s*0.18}" x2="{cx}" y2="{s*0.82}" stroke="{COLORS["primary_light"]}" stroke-width="{s*0.02}"/>')
    dwg.append(f'<path d="M {s*0.2} {cy} Q {cx} {s*0.3} {s*0.8} {cy}" fill="none" stroke="{COLORS["primary_light"]}" stroke-width="{s*0.02}"/>')
    dwg.append(f'<path d="M {s*0.2} {cy} Q {cx} {s*0.7} {s*0.8} {cy}" fill="none" stroke="{COLORS["primary_light"]}" stroke-width="{s*0.02}"/>')
    
    dwg.append(svg_footer())
    return '\n'.join(dwg)

def icon_document(size):
    """文档图标"""
    dwg = []
    gen_gradient(dwg, "g1", "white", COLORS["gray_light"])
    dwg.append(svg_header(size))
    
    s = size
    # 纸张
    dwg.append(f'<rect x="{s*0.22}" y="{s*0.1}" width="{s*0.56}" height="{s*0.8}" rx="{s*0.03}" fill="url(#g1)" stroke="{COLORS["gray"]}" stroke-width="{s*0.01}"/>')
    # 折角
    dwg.append(f'<polygon points="{s*0.78},{s*0.1} {s*0.78},{s*0.28} {s*0.6},{s*0.1}" fill="{COLORS["gray_light"]}" stroke="{COLORS["gray"]}" stroke-width="{s*0.01}"/>')
    # 文字行
    for i in range(5):
        y = s * (0.35 + i * 0.1)
        w = s * (0.45 - i * 0.03)
        dwg.append(f'<rect x="{s*0.28}" y="{y}" width="{w}" height="{s*0.04}" rx="{s*0.01}" fill="{COLORS["gray_light"]}"/>')
    
    dwg.append(svg_footer())
    return '\n'.join(dwg)

def icon_disk(size):
    """磁盘/硬盘图标"""
    dwg = []
    gen_gradient(dwg, "g1", COLORS["bg_medium"], COLORS["bg_dark"])
    dwg.append(svg_header(size))
    
    s = size
    # 硬盘主体
    dwg.append(f'<rect x="{s*0.08}" y="{s*0.28}" width="{s*0.84}" height="{s*0.44}" rx="{s*0.06}" fill="url(#g1)"/>')
    # 正面面板
    dwg.append(f'<rect x="{s*0.12}" y="{s*0.32}" width="{s*0.76}" height="{s*0.2}" rx="{s*0.03}" fill="{COLORS["bg_dark"]}"/>')
    # 指示灯
    dwg.append(f'<circle cx="{s*0.8}" cy="{s*0.42}" r="{s*0.03}" fill="{COLORS["success"]}">')
    dwg.append('<animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>')
    dwg.append('</circle>')
    # 接口
    dwg.append(f'<rect x="{s*0.3}" y="{s*0.56}" width="{s*0.4}" height="{s*0.08}" rx="{s*0.02}" fill="{COLORS["gray"]}"/>')
    
    dwg.append(svg_footer())
    return '\n'.join(dwg)

def icon_wifi(size):
    """WiFi图标"""
    dwg = []
    dwg.append(svg_header(size))
    
    s = size
    cx, cy = s/2, s*0.65
    
    # WiFi信号弧
    for i, (r, opacity) in enumerate([(s*0.4, 0.3), (s*0.32, 0.5), (s*0.24, 0.7), (s*0.16, 1)]):
        dwg.append(f'<path d="M {cx-r} {cy} A {r} {r} 0 0 1 {cx+r} {cy}" fill="none" stroke="{COLORS["primary"]}" stroke-width="{s*0.05}" stroke-linecap="round" opacity="{opacity}"/>')
    
    # 原点
    dwg.append(f'<circle cx="{cx}" cy="{cy}" r="{s*0.06}" fill="{COLORS["primary"]}"/>')
    
    dwg.append(svg_footer())
    return '\n'.join(dwg)

def icon_volume(size):
    """音量图标"""
    dwg = []
    dwg.append(svg_header(size))
    
    s = size
    # 喇叭
    dwg.append(f'<polygon points="{s*0.2},{s*0.4} {s*0.4},{s*0.4} {s*0.55},{s*0.25} {s*0.55},{s*0.75} {s*0.4},{s*0.6} {s*0.2},{s*0.6}" fill="{COLORS["gray"]}"/>')
    # 声波
    dwg.append(f'<path d="M {s*0.65} {s*0.35} Q {s*0.8} {s*0.5} {s*0.65} {s*0.65}" fill="none" stroke="{COLORS["primary"]}" stroke-width="{s*0.04}" stroke-linecap="round"/>')
    dwg.append(f'<path d="M {s*0.75} {s*0.28} Q {s*0.95} {s*0.5} {s*0.75} {s*0.72}" fill="none" stroke="{COLORS["primary"]}" stroke-width="{s*0.04}" stroke-linecap="round" opacity="0.6"/>')
    
    dwg.append(svg_footer())
    return '\n'.join(dwg)

def icon_power(size):
    """电源图标"""
    dwg = []
    gen_gradient(dwg, "g1", COLORS["success"], COLORS["primary"])
    dwg.append(svg_header(size))
    
    s = size
    cx, cy = s/2, s/2
    
    # 圆环
    dwg.append(f'<circle cx="{cx}" cy="{cy}" r="{s*0.38}" fill="none" stroke="url(#g1)" stroke-width="{s*0.08}" stroke-linecap="round" stroke-dasharray="{s*2} {s*0.5}"/>')
    # 电源符号
    dwg.append(f'<line x1="{cx}" y1="{s*0.25}" x2="{cx}" y2="{s*0.55}" stroke="{COLORS["primary"]}" stroke-width="{s*0.08}" stroke-linecap="round"/>')
    
    dwg.append(svg_footer())
    return '\n'.join(dwg)

def icon_home(size):
    """主页图标"""
    dwg = []
    gen_gradient(dwg, "g1", COLORS["primary"], COLORS["primary_dark"])
    dwg.append(svg_header(size))
    
    s = size
    # 屋顶
    dwg.append(f'<polygon points="{s*0.5},{s*0.15} {s*0.15},{s*0.5} {s*0.85},{s*0.5}" fill="url(#g1)"/>')
    # 房身
    dwg.append(f'<rect x="{s*0.25}" y="{s*0.5}" width="{s*0.5}" height="{s*0.35}" fill="{COLORS["primary_light"]}"/>')
    # 门
    dwg.append(f'<rect x="{s*0.42}" y="{s*0.62}" width="{s*0.16}" height="{s*0.23}" rx="{s*0.02}" fill="{COLORS["primary_dark"]}"/>')
    # 门把手
    dwg.append(f'<circle cx="{s*0.54}" cy="{s*0.75}" r="{s*0.02}" fill="white"/>')
    
    dwg.append(svg_footer())
    return '\n'.join(dwg)

def icon_trash(size):
    """回收站图标"""
    dwg = []
    gen_gradient(dwg, "g1", COLORS["danger"], "#b91c1c")
    dwg.append(svg_header(size))
    
    s = size
    # 桶身
    dwg.append(f'<rect x="{s*0.25}" y="{s*0.3}" width="{s*0.5}" height="{s*0.55}" rx="{s*0.04}" fill="url(#g1)"/>')
    # 桶盖
    dwg.append(f'<rect x="{s*0.2}" y="{s*0.22}" width="{s*0.6}" height="{s*0.1}" rx="{s*0.03}" fill="{COLORS["danger"]}"/>')
    # 桶盖把手
    dwg.append(f'<rect x="{s*0.42}" y="{s*0.15}" width="{s*0.16}" height="{s*0.1}" rx="{s*0.02}" fill="{COLORS["danger"]}"/>')
    # 条纹
    for i in range(3):
        x = s * (0.35 + i * 0.15)
        dwg.append(f'<rect x="{x}" y="{s*0.38}" width="{s*0.04}" height="{s*0.4}" rx="{s*0.01}" fill="white" opacity="0.3"/>')
    
    dwg.append(svg_footer())
    return '\n'.join(dwg)

def icon_image(size):
    """图片图标"""
    dwg = []
    gen_gradient(dwg, "g1", COLORS["accent"], COLORS["primary"])
    dwg.append(svg_header(size))
    
    s = size
    # 相框
    dwg.append(f'<rect x="{s*0.12}" y="{s*0.18}" width="{s*0.76}" height="{s*0.64}" rx="{s*0.04}" fill="white" stroke="url(#g1)" stroke-width="{s*0.04}"/>')
    # 山
    dwg.append(f'<polygon points="{s*0.2},{s*0.7} {s*0.45},{s*0.4} {s*0.6},{s*0.55} {s*0.8},{s*0.35} {s*0.8},{s*0.7}" fill="{COLORS["primary_light"]}"/>')
    # 太阳
    dwg.append(f'<circle cx="{s*0.7}" cy="{s*0.35}" r="{s*0.08}" fill="{COLORS["warning"]}"/>')
    
    dwg.append(svg_footer())
    return '\n'.join(dwg)

def icon_music(size):
    """音乐图标"""
    dwg = []
    gen_gradient(dwg, "g1", COLORS["accent"], "#7c3aed")
    dwg.append(svg_header(size))
    
    s = size
    # 音符
    dwg.append(f'<circle cx="{s*0.35}" cy="{s*0.7}" r="{s*0.12}" fill="url(#g1)"/>')
    dwg.append(f'<rect x="{s*0.45}" y="{s*0.2}" width="{s*0.08}" height="{s*0.5}" fill="url(#g1)"/>')
    dwg.append(f'<path d="M {s*0.45} {s*0.2} Q {s*0.7} {s*0.15} {s*0.75} {s*0.3}" fill="none" stroke="url(#g1)" stroke-width="{s*0.08}" stroke-linecap="round"/>')
    dwg.append(f'<circle cx="{s*0.75}" cy="{s*0.55}" r="{s*0.1}" fill="url(#g1)"/>')
    
    dwg.append(svg_footer())
    return '\n'.join(dwg)

def icon_video(size):
    """视频图标"""
    dwg = []
    gen_gradient(dwg, "g1", COLORS["danger"], "#7c2d12")
    dwg.append(svg_header(size))
    
    s = size
    # 摄像机主体
    dwg.append(f'<rect x="{s*0.12}" y="{s*0.3}" width="{s*0.55}" height="{s*0.4}" rx="{s*0.04}" fill="url(#g1)"/>')
    # 镜头
    dwg.append(f'<circle cx="{s*0.35}" cy="{s*0.5}" r="{s*0.15}" fill="{COLORS["bg_dark"]}"/>')
    dwg.append(f'<circle cx="{s*0.35}" cy="{s*0.5}" r="{s*0.1}" fill="{COLORS["primary_light"]}"/>')
    # 取景器
    dwg.append(f'<polygon points="{s*0.67},{s*0.35} {s*0.88},{s*0.28} {s*0.88},{s*0.72} {s*0.67},{s*0.65}" fill="{COLORS["gray_light"]}"/>')
    
    dwg.append(svg_footer())
    return '\n'.join(dwg)

def icon_user(size):
    """用户图标"""
    dwg = []
    gen_gradient(dwg, "g1", COLORS["primary"], COLORS["primary_dark"])
    dwg.append(svg_header(size))
    
    s = size
    cx = s/2
    
    # 头部
    dwg.append(f'<circle cx="{cx}" cy="{s*0.35}" r="{s*0.18}" fill="url(#g1)"/>')
    # 身体
    dwg.append(f'<path d="M {s*0.2} {s*0.85} Q {s*0.2} {s*0.55} {cx} {s*0.55} Q {s*0.8} {s*0.55} {s*0.8} {s*0.85}" fill="url(#g1)"/>')
    
    dwg.append(svg_footer())
    return '\n'.join(dwg)

def icon_search(size):
    """搜索图标"""
    dwg = []
    dwg.append(svg_header(size))
    
    s = size
    # 放大镜
    dwg.append(f'<circle cx="{s*0.4}" cy="{s*0.4}" r="{s*0.22}" fill="none" stroke="{COLORS["primary"]}" stroke-width="{s*0.07}"/>')
    # 手柄
    dwg.append(f'<line x1="{s*0.58}" y1="{s*0.58}" x2="{s*0.82}" y2="{s*0.82}" stroke="{COLORS["primary"]}" stroke-width="{s*0.07}" stroke-linecap="round"/>')
    
    dwg.append(svg_footer())
    return '\n'.join(dwg)

def icon_calculator(size):
    """计算器图标"""
    dwg = []
    gen_gradient(dwg, "g1", COLORS["bg_medium"], COLORS["bg_dark"])
    dwg.append(svg_header(size))
    
    s = size
    # 计算器主体
    dwg.append(f'<rect x="{s*0.2}" y="{s*0.12}" width="{s*0.6}" height="{s*0.76}" rx="{s*0.05}" fill="url(#g1)"/>')
    # 显示屏
    dwg.append(f'<rect x="{s*0.26}" y="{s*0.2}" width="{s*0.48}" height="{s*0.15}" rx="{s*0.02}" fill="{COLORS["success"]}" opacity="0.3"/>')
    dwg.append(f'<text x="{s*0.68}" y="{s*0.31}" font-family="monospace" font-size="{s*0.1}" fill="{COLORS["success"]}" text-anchor="end">0</text>')
    # 按钮
    btn_colors = [COLORS["gray"], COLORS["warning"], COLORS["primary"]]
    for row in range(4):
        for col in range(3):
            x = s * (0.26 + col * 0.17)
            y = s * (0.4 + row * 0.11)
            c = btn_colors[2] if (row == 3 and col == 2) else btn_colors[0]
            dwg.append(f'<rect x="{x}" y="{y}" width="{s*0.13}" height="{s*0.08}" rx="{s*0.015}" fill="{c}"/>')
    
    dwg.append(svg_footer())
    return '\n'.join(dwg)

def icon_text_editor(size):
    """文本编辑器图标"""
    dwg = []
    gen_gradient(dwg, "g1", COLORS["primary"], COLORS["primary_dark"])
    dwg.append(svg_header(size))
    
    s = size
    # 笔记本
    dwg.append(f'<rect x="{s*0.18}" y="{s*0.12}" width="{s*0.64}" height="{s*0.76}" rx="{s*0.03}" fill="white" stroke="url(#g1)" stroke-width="{s*0.03}"/>')
    # 装订线
    dwg.append(f'<line x1="{s*0.3}" y1="{s*0.12}" x2="{s*0.3}" y2="{s*0.88}" stroke="{COLORS["primary_light"]}" stroke-width="{s*0.02}"/>')
    # 文字行
    for i in range(6):
        y = s * (0.22 + i * 0.1)
        dwg.append(f'<rect x="{s*0.35}" y="{y}" width="{s*0.4}" height="{s*0.04}" rx="{s*0.01}" fill="{COLORS["gray_light"]}"/>')
    
    dwg.append(svg_footer())
    return '\n'.join(dwg)

def icon_system_monitor(size):
    """系统监视器图标"""
    dwg = []
    gen_gradient(dwg, "g1", COLORS["success"], COLORS["primary"])
    dwg.append(svg_header(size))
    
    s = size
    # 背景
    dwg.append(f'<rect x="{s*0.1}" y="{s*0.15}" width="{s*0.8}" height="{s*0.7}" rx="{s*0.04}" fill="{COLORS["bg_dark"]}"/>')
    # 柱状图
    heights = [0.3, 0.5, 0.7, 0.4, 0.6, 0.8, 0.5]
    for i, h in enumerate(heights):
        x = s * (0.18 + i * 0.1)
        y = s * (0.85 - h * 0.5)
        dwg.append(f'<rect x="{x}" y="{y}" width="{s*0.07}" height="{s*h*0.5}" rx="{s*0.01}" fill="url(#g1)"/>')
    
    dwg.append(svg_footer())
    return '\n'.join(dwg)

def icon_firefox(size):
    """Firefox风格浏览器图标"""
    dwg = []
    gen_gradient(dwg, "g1", "#f97316", "#dc2626")
    gen_gradient(dwg, "g2", "#fbbf24", "#f97316")
    dwg.append(svg_header(size))
    
    s = size
    cx, cy = s/2, s/2
    
    # 外圈（橙色狐狸环绕）
    dwg.append(f'<circle cx="{cx}" cy="{cy}" r="{s*0.4}" fill="url(#g1)"/>')
    # 内圈地球
    dwg.append(f'<circle cx="{cx}" cy="{cy}" r="{s*0.28}" fill="{COLORS["primary"]}"/>')
    dwg.append(f'<circle cx="{cx}" cy="{cy}" r="{s*0.22}" fill="{COLORS["primary_light"]}"/>')
    # 狐狸尾巴装饰
    dwg.append(f'<path d="M {cx} {s*0.12} Q {s*0.8} {s*0.3} {s*0.7} {s*0.7}" fill="none" stroke="url(#g2)" stroke-width="{s*0.08}" stroke-linecap="round"/>')
    
    dwg.append(svg_footer())
    return '\n'.join(dwg)

def icon_thunar(size):
    """Thunar文件管理器图标"""
    dwg = []
    gen_gradient(dwg, "g1", COLORS["primary"], COLORS["primary_dark"])
    dwg.append(svg_header(size))
    
    s = size
    # 文件夹主体
    dwg.append(f'<rect x="{s*0.1}" y="{s*0.28}" width="{s*0.8}" height="{s*0.58}" rx="{s*0.06}" fill="url(#g1)"/>')
    # 文件夹标签
    dwg.append(f'<rect x="{s*0.1}" y="{s*0.2}" width="{s*0.4}" height="{s*0.14}" rx="{s*0.04}" fill="{COLORS["primary_light"]}"/>')
    # 文件预览
    dwg.append(f'<rect x="{s*0.2}" y="{s*0.4}" width="{s*0.25}" height="{s*0.35}" rx="{s*0.02}" fill="white" opacity="0.9"/>')
    dwg.append(f'<rect x="{s*0.5}" y="{s*0.4}" width="{s*0.25}" height="{s*0.35}" rx="{s*0.02}" fill="white" opacity="0.7"/>')
    # 高光
    dwg.append(f'<rect x="{s*0.15}" y="{s*0.33}" width="{s*0.7}" height="{s*0.06}" rx="{s*0.01}" fill="white" opacity="0.25"/>')
    
    dwg.append(svg_footer())
    return '\n'.join(dwg)

def icon_mousepad(size):
    """Mousepad文本编辑器图标"""
    dwg = []
    gen_gradient(dwg, "g1", COLORS["accent"], "#0891b2")
    dwg.append(svg_header(size))
    
    s = size
    # 纸张
    dwg.append(f'<rect x="{s*0.2}" y="{s*0.1}" width="{s*0.6}" height="{s*0.8}" rx="{s*0.02}" fill="white" stroke="url(#g1)" stroke-width="{s*0.025}"/>')
    # 铅笔
    dwg.append(f'<polygon points="{s*0.75},{s*0.15} {s*0.85},{s*0.25} {s*0.55},{s*0.55} {s*0.45},{s*0.5}" fill="url(#g1)"/>')
    dwg.append(f'<polygon points="{s*0.45},{s*0.5} {s*0.55},{s*0.55} {s*0.5},{s*0.6}" fill="#fbbf24"/>')
    # 文字行
    for i in range(5):
        y = s * (0.25 + i * 0.1)
        dwg.append(f'<rect x="{s*0.28}" y="{y}" width="{s*0.35}" height="{s*0.03}" rx="{s*0.01}" fill="{COLORS["gray_light"]}"/>')
    
    dwg.append(svg_footer())
    return '\n'.join(dwg)

# ========== 主生成逻辑 ==========

ICON_GENERATORS = {
    # 基础系统图标
    "folder": icon_folder,
    "folder-home": icon_home,
    "folder-documents": icon_folder,
    "folder-downloads": icon_folder,
    "folder-pictures": icon_image,
    "folder-music": icon_music,
    "folder-videos": icon_video,
    "folder-trash": icon_trash,
    
    # 应用图标
    "utilities-terminal": icon_terminal,
    "preferences-system": icon_settings,
    "web-browser": icon_browser,
    "firefox": icon_firefox,
    "thunar": icon_thunar,
    "mousepad": icon_mousepad,
    "text-editor": icon_text_editor,
    "accessories-calculator": icon_calculator,
    "system-monitor": icon_system_monitor,
    
    # 状态图标
    "network-wireless": icon_wifi,
    "audio-volume-high": icon_volume,
    "system-shutdown": icon_power,
    
    # MIME类型
    "text-x-generic": icon_document,
    "image-x-generic": icon_image,
    "audio-x-generic": icon_music,
    "video-x-generic": icon_video,
    
    # 其他
    "user-home": icon_home,
    "system-search": icon_search,
    "user-identity": icon_user,
    "drive-harddisk": icon_disk,
}

def generate_all_icons():
    print("🚀 开始生成 DoubaoOS 图标集...")
    
    for size in SIZES:
        size_dir = os.path.join(ICON_ROOT, f"{size}x{size}", "apps")
        ensure_dir(size_dir)
        
        # 同时生成到 categories、mimetypes、places 等目录
        for category in ["apps", "categories", "mimetypes", "places", "status", "devices"]:
            cat_dir = os.path.join(ICON_ROOT, f"{size}x{size}", category)
            ensure_dir(cat_dir)
    
    # 生成每个图标
    for icon_name, gen_func in ICON_GENERATORS.items():
        for size in SIZES:
            svg_content = gen_func(size)
            
            # 写入多个目录
            categories_to_write = ["apps"]
            if "folder" in icon_name or "home" in icon_name or "trash" in icon_name:
                categories_to_write.append("places")
            if "wireless" in icon_name or "volume" in icon_name or "shutdown" in icon_name:
                categories_to_write.append("status")
            if "generic" in icon_name:
                categories_to_write.append("mimetypes")
            if "preferences" in icon_name or "system" in icon_name:
                categories_to_write.append("categories")
            if "drive" in icon_name or "disk" in icon_name:
                categories_to_write.append("devices")
            
            for cat in categories_to_write:
                icon_path = os.path.join(ICON_ROOT, f"{size}x{size}", cat, f"{icon_name}.svg")
                with open(icon_path, "w", encoding="utf-8") as f:
                    f.write(svg_content)
    
    # 生成 index.theme
    generate_index_theme()
    
    print(f"✅ 图标生成完成！共生成 {len(ICON_GENERATORS)} 种图标 × {len(SIZES)} 种尺寸")
    print(f"📁 输出目录: {ICON_ROOT}")

def generate_index_theme():
    """生成图标主题 index.theme 文件"""
    theme_content = f'''[Icon Theme]
Name=DoubaoOS Icons
Comment=DoubaoOS custom icon theme
Inherits=hicolor
Example=folder

# 目录列表
Directories={','.join([f"{s}x{s}/apps,{s}x{s}/categories,{s}x{s}/mimetypes,{s}x{s}/places,{s}x{s}/status,{s}x{s}/devices" for s in SIZES])}

'''
    
    for size in SIZES:
        for cat in ["apps", "categories", "mimetypes", "places", "status", "devices"]:
            theme_content += f'''[{size}x{size}/{cat}]
Size={size}
Type=Fixed
Context={cat.capitalize()}

'''
    
    index_path = os.path.join(ICON_ROOT, "index.theme")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(theme_content)

if __name__ == "__main__":
    generate_all_icons()
