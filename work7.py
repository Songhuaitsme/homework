import turtle
import random
import math
# 1. 设置基础参数
RADIUS = 150  # 圆的半径 (调大一点看得更清楚)
SAMPLES = 5000  # 模拟投点的次数
WIDTH = RADIUS * 2.2  # 窗口大小
# 2. 初始化画布
screen = turtle.Screen()
screen.title(f"蒙特卡洛仿真 PI - 半径: {RADIUS}")
screen.setup(WIDTH * 2, WIDTH * 2)
screen.tracer(0)  # 关闭自动刷新，极大提高绘制速度
# 初始化画笔
pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)
pen.width(2)

def draw_boundaries():
    pen.color("black")
    pen.penup()
    pen.goto(-RADIUS, -RADIUS)  # 移动到左下角
    pen.pendown()
    for _ in range(4):
        pen.forward(RADIUS * 2)
        pen.left(90)
    pen.penup()
    pen.goto(0, -RADIUS)  # 移动到圆的底部
    pen.pendown()
    pen.color("red")  # 圆的颜色
    pen.circle(RADIUS)  # 画圆
    pen.penup()
draw_boundaries()
screen.update()  # 刷新一下显示出圆

in_circle_count = 0
print("开始仿真...")
for i in range(SAMPLES):
    # 随机生成坐标 (-RADIUS 到 RADIUS)
    x = random.uniform(-RADIUS, RADIUS)
    y = random.uniform(-RADIUS, RADIUS)
    pen.goto(x, y)
    # 计算距离原点的距离 (x^2 + y^2)
    distance = math.sqrt(x ** 2 + y ** 2)
    if distance <= RADIUS:
        pen.color("red")  # 圆内：红色
        in_circle_count += 1
    else:
        pen.color("blue")  # 圆外：蓝色
    pen.dot(5)  # 画一个小点
    # 每画 10 个点刷新一次屏幕，以此产生动画效果
    if i % 10 == 0:
        screen.update()
# 4. 计算并显示结果
pi_estimate = 4 * in_circle_count / SAMPLES
screen.update()  # 最后刷新
# 在图上写出结果
pen.goto(0, RADIUS + 10)
pen.color("black")
pen.write(f"模拟次数: {SAMPLES}, 估计 Pi: {pi_estimate:.6f}",
          align="center", font=("Arial", 16, "bold"))
print(f"最终估计 PI: {pi_estimate}")
screen.exitonclick()