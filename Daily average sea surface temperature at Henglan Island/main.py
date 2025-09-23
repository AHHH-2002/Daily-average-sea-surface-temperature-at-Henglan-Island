import pygame
import numpy as np
import pandas as pd
import os

# --- 数据读取 ---
DATA_FILE = 'daily_WGL_SST_2025.csv'
assert os.path.exists(DATA_FILE), f"数据文件 {DATA_FILE} 未找到，请放在项目根目录下。"

df = pd.read_csv(DATA_FILE, skiprows=2)
df = df[df['數值/Value'].apply(lambda x: str(x).replace('.','',1).isdigit())]
temps = df['數值/Value'].astype(float).values

# --- 波浪参数 ---
width, height = 900, 400
x = np.linspace(0, 2 * np.pi, width)

# --- 蓝色渐变函数 ---
def blue_gradient_and_width(pos, total):
    if pos < total/2:
        ratio = pos/(total/2)
        r = int(0 + (120-0)*ratio)
        g = int(60 + (200-60)*ratio)
        b = int(160 + (255-160)*ratio)
        width = int(8 + (36-8)*ratio)
    else:
        ratio = (pos-total/2)/(total/2)
        r = int(120 - (120-0)*ratio)
        g = int(200 - (200-60)*ratio)
        b = int(255 - (255-160)*ratio)
        width = int(36 - (36-8)*ratio)
    return (r, g, b), width

# --- 橙红到白色径向渐变背景 ---
def draw_radial_gradient(surface, center, radius, color_inner, color_outer):
    for r in range(radius, 0, -1):
        ratio = r / radius
        r_c = int(color_inner[0] * ratio + color_outer[0] * (1 - ratio))
        g_c = int(color_inner[1] * ratio + color_outer[1] * (1 - ratio))
        b_c = int(color_inner[2] * ratio + color_outer[2] * (1 - ratio))
        pygame.draw.circle(surface, (r_c, g_c, b_c), center, r)

# --- Pygame 初始化 ---
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

running = True
frame = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # 渐变背景
    draw_radial_gradient(screen, (width//2, height//2), max(width, height), (255,100,0), (255,255,255))
    # 取温度数据并生成波浪
    temp = temps[frame % len(temps)]
    amp = 40 + (temp-15)*3
    phase = frame * 0.12  # 波浪速度加快，原为0.04
    y = height//2 + amp * np.sin(x + phase)
    points = list(zip(range(width), y.astype(int)))
    # 填充波浪线以下区域
    for i in range(len(points)-1):
        color, _ = blue_gradient_and_width(i, len(points))
        poly_points = [points[i], points[i+1], (points[i+1][0], height), (points[i][0], height)]
        pygame.draw.polygon(screen, color, poly_points)
    # 画波浪线
    for i in range(len(points)-1):
        color, line_width = blue_gradient_and_width(i, len(points))
        pygame.draw.line(screen, color, points[i], points[i+1], line_width)
    # 显示温度
    temp_text = font.render(f"{temp:.1f}°C", True, (0,0,0))
    screen.blit(temp_text, (20, 20))
    pygame.display.flip()
    frame += 1
    clock.tick(60)

pygame.quit()
