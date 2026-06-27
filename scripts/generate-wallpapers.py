#!/usr/bin/env python3
"""
DoubaoOS 壁纸生成器
自主生成 SVG 格式系统壁纸，无外部素材依赖
"""

import os
import math
import random

WALLPAPER_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "themes", "wallpapers")

# 主题配色
COLORS = {
    "primary": "#3b82f6",
    "primary_dark": "#1e40af",
    "primary_darker": "#1e3a8a",
    "accent": "#06b6d4",
    "accent_dark": "#0891b2",
    "purple": "#8b5cf6",
    "pink": "#ec4899",
    "cyan": "#22d3ee",
    "bg_dark": "#0f172a",
    "bg_medium": "#1e293b",
    "bg_light": "#334155",
    "white": "#ffffff",
}

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def wallpaper_gradient_blue(width=1920, height=1080):
    """蓝色渐变几何壁纸 - 默认壁纸"""
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')
    
    # 背景渐变
    svg.append('<defs>')
    svg.append('<linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">')
    svg.append(f'<stop offset="0%" stop-color="{COLORS["bg_dark"]}"/>')
    svg.append(f'<stop offset="50%" stop-color="{COLORS["primary_darker"]}"/>')
    svg.append(f'<stop offset="100%" stop-color="{COLORS["bg_medium"]}"/>')
    svg.append('</linearGradient>')
    
    # 光晕渐变
    svg.append('<radialGradient id="glow1" cx="30%" cy="20%" r="40%">')
    svg.append(f'<stop offset="0%" stop-color="{COLORS["primary"]}" opacity="0.3"/>')
    svg.append('<stop offset="100%" stop-color="transparent"/>')
    svg.append('</radialGradient>')
    
    svg.append('<radialGradient id="glow2" cx="70%" cy="80%" r="35%">')
    svg.append(f'<stop offset="0%" stop-color="{COLORS["accent"]}" opacity="0.25"/>')
    svg.append('<stop offset="100%" stop-color="transparent"/>')
    svg.append('</radialGradient>')
    
    svg.append('<radialGradient id="glow3" cx="85%" cy="15%" r="25%">')
    svg.append(f'<stop offset="0%" stop-color="{COLORS["purple"]}" opacity="0.2"/>')
    svg.append('<stop offset="100%" stop-color="transparent"/>')
    svg.append('</radialGradient>')
    svg.append('</defs>')
    
    # 背景
    svg.append(f'<rect width="{width}" height="{height}" fill="url(#bgGrad)"/>')
    
    # 光晕效果
    svg.append(f'<rect width="{width}" height="{height}" fill="url(#glow1)"/>')
    svg.append(f'<rect width="{width}" height="{height}" fill="url(#glow2)"/>')
    svg.append(f'<rect width="{width}" height="{height}" fill="url(#glow3)"/>')
    
    # 几何图形 - 圆形
    circles = [
        (width*0.15, height*0.7, 120, COLORS["primary"], 0.1),
        (width*0.85, height*0.3, 80, COLORS["accent"], 0.15),
        (width*0.5, height*0.85, 150, COLORS["purple"], 0.08),
        (width*0.7, height*0.6, 60, COLORS["cyan"], 0.12),
    ]
    for cx, cy, r, color, opacity in circles:
        svg.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" opacity="{opacity}"/>')
    
    # 几何线条
    svg.append(f'<line x1="0" y1="{height*0.3}" x2="{width}" y2="{height*0.3}" stroke="{COLORS["primary"]}" stroke-width="1" opacity="0.1"/>')
    svg.append(f'<line x1="0" y1="{height*0.6}" x2="{width}" y2="{height*0.6}" stroke="{COLORS["accent"]}" stroke-width="1" opacity="0.08"/>')
    
    # 网格点阵
    dot_spacing = 60
    for x in range(0, width, dot_spacing):
        for y in range(0, height, dot_spacing):
            opacity = 0.03 + (math.sin(x*0.01) * math.cos(y*0.01) + 1) * 0.02
            svg.append(f'<circle cx="{x}" cy="{y}" r="1.5" fill="white" opacity="{opacity}"/>')
    
    # DoubaoOS Logo 水印
    logo_x = width * 0.5
    logo_y = height * 0.5
    svg.append(f'<g transform="translate({logo_x}, {logo_y})" opacity="0.08">')
    svg.append(f'<circle cx="0" cy="0" r="100" fill="none" stroke="white" stroke-width="3"/>')
    svg.append(f'<circle cx="0" cy="0" r="70" fill="none" stroke="white" stroke-width="2"/>')
    svg.append(f'<text x="0" y="10" font-family="sans-serif" font-size="48" font-weight="bold" fill="white" text-anchor="middle">DoubaoOS</text>')
    svg.append('</g>')
    
    svg.append('</svg>')
    return '\n'.join(svg)

def wallpaper_minimal_office(width=1920, height=1080):
    """极简办公壁纸 - 办公模式专用"""
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')
    
    # 背景
    svg.append('<defs>')
    svg.append('<linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="1">')
    svg.append(f'<stop offset="0%" stop-color="#f8fafc"/>')
    svg.append(f'<stop offset="100%" stop-color="#e2e8f0"/>')
    svg.append('</linearGradient>')
    svg.append('</defs>')
    
    svg.append(f'<rect width="{width}" height="{height}" fill="url(#bgGrad)"/>')
    
    # 简洁几何装饰
    svg.append(f'<rect x="0" y="0" width="{width}" height="{height*0.08}" fill="{COLORS["primary"]}" opacity="0.1"/>')
    svg.append(f'<rect x="0" y="{height*0.92}" width="{width}" height="{height*0.08}" fill="{COLORS["primary"]}" opacity="0.05"/>')
    
    # 侧边装饰线
    svg.append(f'<rect x="{width*0.03}" y="{height*0.15}" width="4" height="{height*0.7}" rx="2" fill="{COLORS["primary"]}" opacity="0.3"/>')
    
    # 极简点阵
    dot_spacing = 80
    for x in range(int(width*0.1), int(width*0.9), dot_spacing):
        for y in range(int(height*0.2), int(height*0.8), dot_spacing):
            svg.append(f'<circle cx="{x}" cy="{y}" r="2" fill="{COLORS["primary"]}" opacity="0.1"/>')
    
    svg.append('</svg>')
    return '\n'.join(svg)

def wallpaper_dark_tech(width=1920, height=1080):
    """深色科技风壁纸"""
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')
    
    svg.append('<defs>')
    # 背景渐变
    svg.append('<linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">')
    svg.append(f'<stop offset="0%" stop-color="#0a0a0f"/>')
    svg.append(f'<stop offset="100%" stop-color="#1a1a2e"/>')
    svg.append('</linearGradient>')
    
    # 网格渐变
    svg.append('<linearGradient id="gridGrad" x1="0" y1="0" x2="0" y2="1">')
    svg.append(f'<stop offset="0%" stop-color="{COLORS["cyan"]}" opacity="0.3"/>')
    svg.append(f'<stop offset="100%" stop-color="{COLORS["primary"]}" opacity="0.1"/>')
    svg.append('</linearGradient>')
    
    svg.append('</defs>')
    
    # 背景
    svg.append(f'<rect width="{width}" height="{height}" fill="url(#bgGrad)"/>')
    
    # 科技网格线
    grid_size = 50
    for x in range(0, width, grid_size):
        opacity = 0.05 + (x / width) * 0.05
        svg.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{height}" stroke="{COLORS["cyan"]}" stroke-width="0.5" opacity="{opacity}"/>')
    for y in range(0, height, grid_size):
        opacity = 0.05 + (y / height) * 0.05
        svg.append(f'<line x1="0" y1="{y}" x2="{width}" y2="{y}" stroke="{COLORS["cyan"]}" stroke-width="0.5" opacity="{opacity}"/>')
    
    # 发光圆环
    for i, (cx, cy, r, color) in enumerate([
        (width*0.3, height*0.4, 200, COLORS["primary"]),
        (width*0.7, height*0.6, 150, COLORS["cyan"]),
        (width*0.5, height*0.3, 100, COLORS["purple"]),
    ]):
        svg.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="1" opacity="0.2"/>')
        svg.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.7}" fill="none" stroke="{color}" stroke-width="0.5" opacity="0.15"/>')
        svg.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.4}" fill="none" stroke="{color}" stroke-width="0.5" opacity="0.1"/>')
    
    # 粒子效果
    random.seed(42)
    for _ in range(50):
        x = random.randint(0, width)
        y = random.randint(0, height)
        r = random.uniform(1, 3)
        opacity = random.uniform(0.3, 0.8)
        svg.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{COLORS["cyan"]}" opacity="{opacity}"/>')
    
    svg.append('</svg>')
    return '\n'.join(svg)

def wallpaper_nature(width=1920, height=1080):
    """自然风景风格壁纸"""
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')
    
    svg.append('<defs>')
    # 天空渐变
    svg.append('<linearGradient id="skyGrad" x1="0" y1="0" x2="0" y2="1">')
    svg.append(f'<stop offset="0%" stop-color="#0ea5e9"/>')
    svg.append(f'<stop offset="50%" stop-color="#38bdf8"/>')
    svg.append(f'<stop offset="100%" stop-color="#7dd3fc"/>')
    svg.append('</linearGradient>')
    
    # 山渐变
    svg.append('<linearGradient id="mountainGrad" x1="0" y1="0" x2="0" y2="1">')
    svg.append(f'<stop offset="0%" stop-color="#1e40af"/>')
    svg.append(f'<stop offset="100%" stop-color="#1e3a8a"/>')
    svg.append('</linearGradient>')
    
    svg.append('</defs>')
    
    # 天空
    svg.append(f'<rect width="{width}" height="{height}" fill="url(#skyGrad)"/>')
    
    # 太阳
    svg.append(f'<circle cx="{width*0.8}" cy="{height*0.25}" r="80" fill="#fef3c7" opacity="0.9"/>')
    svg.append(f'<circle cx="{width*0.8}" cy="{height*0.25}" r="60" fill="#fde68a"/>')
    
    # 云朵
    clouds = [
        (width*0.2, height*0.2, 1),
        (width*0.5, height*0.15, 0.8),
        (width*0.65, height*0.3, 0.6),
    ]
    for cx, cy, scale in clouds:
        svg.append(f'<g transform="translate({cx}, {cy}) scale({scale})">')
        svg.append(f'<ellipse cx="0" cy="0" rx="60" ry="25" fill="white" opacity="0.8"/>')
        svg.append(f'<ellipse cx="-30" cy="-10" rx="35" ry="20" fill="white" opacity="0.8"/>')
        svg.append(f'<ellipse cx="25" cy="-15" rx="40" ry="22" fill="white" opacity="0.8"/>')
        svg.append('</g>')
    
    # 远山
    svg.append(f'<polygon points="0,{height*0.6} {width*0.3},{height*0.35} {width*0.5},{height*0.5} {width*0.7},{height*0.3} {width},{height*0.55} {width},{height} 0,{height}" fill="url(#mountainGrad)" opacity="0.6"/>')
    
    # 近山
    svg.append(f'<polygon points="0,{height*0.75} {width*0.2},{height*0.5} {width*0.4},{height*0.65} {width*0.6},{height*0.45} {width*0.8},{height*0.6} {width},{height*0.5} {width},{height} 0,{height}" fill="url(#mountainGrad)"/>')
    
    # 水面
    svg.append(f'<rect x="0" y="{height*0.8}" width="{width}" height="{height*0.2}" fill="#0369a1" opacity="0.5"/>')
    
    # 水面反光
    for i in range(10):
        x = width * (0.1 + i * 0.1)
        y = height * 0.85
        w = width * 0.05
        svg.append(f'<ellipse cx="{x}" cy="{y}" rx="{w}" ry="3" fill="white" opacity="0.3"/>')
    
    svg.append('</svg>')
    return '\n'.join(svg)

def generate_all_wallpapers():
    print("🖼️  开始生成 DoubaoOS 壁纸...")
    ensure_dir(WALLPAPER_DIR)
    
    wallpapers = {
        "doubaoos-default.svg": wallpaper_gradient_blue(),
        "doubaoos-office.svg": wallpaper_minimal_office(),
        "doubaoos-dark-tech.svg": wallpaper_dark_tech(),
        "doubaoos-nature.svg": wallpaper_nature(),
    }
    
    for filename, content in wallpapers.items():
        filepath = os.path.join(WALLPAPER_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✅ 生成: {filename}")
    
    print(f"✅ 壁纸生成完成！共 {len(wallpapers)} 张壁纸")
    print(f"📁 输出目录: {WALLPAPER_DIR}")

if __name__ == "__main__":
    generate_all_wallpapers()
