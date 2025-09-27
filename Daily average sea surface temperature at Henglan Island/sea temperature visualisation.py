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

# --- 彩虹渐变函数 ---
def rainbow_color(pos, total, frame=0):
    hue = (pos / total + frame * 0.01) % 1.0
    color = pygame.Color(0)
    color.hsva = (hue * 360, 18, 95, 100)  # 更高明度，更低饱和度
    blend_ratio = 0.45  # 0=纯色, 1=全白
    r = int(color.r * (1-blend_ratio) + 255 * blend_ratio)
    g = int(color.g * (1-blend_ratio) + 255 * blend_ratio)
    b = int(color.b * (1-blend_ratio) + 255 * blend_ratio)
    return r, g, b

# --- Pygame 初始化 ---
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 22, bold=False, italic=True)  # 纤细斜体字体

running = True
frame = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # 渐变背景
    screen.fill((255,255,255))
    # 取温度数据并生成平滑的波浪
    temp = temps[frame % len(temps)]
    amp = 40 + (temp-15)*3
    phase = frame * 0.12
    # 多频率平滑叠加，无噪声
    y = height//2 + amp * (np.sin(x + phase) + 0.3*np.sin(2*x + phase*1.7) + 0.2*np.sin(3*x - phase*0.7))
    points = list(zip(range(width), y.astype(int)))
    # 填充波浪线以下区域（彩虹渐变）
    for i in range(len(points)-1):
        color = rainbow_color(i, len(points), frame)
        poly_points = [points[i], points[i+1], (points[i+1][0], height), (points[i][0], height)]
        pygame.draw.polygon(screen, color, poly_points)
    # 画波浪线（更宽更淡的彩虹渐变）
    for i in range(len(points)-1):
        color = rainbow_color(i, len(points), frame)
        pygame.draw.line(screen, color, points[i], points[i+1], 22)
    # 用密集的竖线表示波浪，粗细随y值变化，颜色依旧渐变
    for i in range(len(points)):
        color = rainbow_color(i, len(points), frame)
        # 线条粗细根据波峰波谷变化，y越远离中心越粗
        thickness = int(8 + 18 * abs(points[i][1] - height//2) / (height//2))
        pygame.draw.line(screen, color, (points[i][0], points[i][1]), (points[i][0], height), thickness)
    # 显示温度
    # 温度数字固定在左上角，颜色加深
    temp_text = font.render(f"{temp:.1f}°C", True, (30, 120, 200))  # 深天蓝色
    screen.blit(temp_text, (18, 12))
    pygame.display.flip()
    frame += 1
    clock.tick(60)

pygame.quit()
