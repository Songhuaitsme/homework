import random
import matplotlib.pyplot as plt
def monty_hall_simulation(n_simulations=1000):
    switch_wins = 0
    stick_wins = 0
    # 用于记录概率变化，以便绘图
    switch_probs = []
    stick_probs = []
    for i in range(1, n_simulations + 1):
        # 1. 放置奖品：0, 1, 2 代表三扇门，随机选一个放车
        doors = ['goat', 'goat', 'goat']
        car_position = random.randint(0, 2)
        doors[car_position] = 'car'
        # 2. 参赛者选择
        choice = random.randint(0, 2)
        # 3. 主持人打开一扇是羊的门 (且不是参赛者选的那扇)
        # 这一步在纯概率计算中可以简化：
        # 如果坚持选择 (stick)，只要原选择是车就赢。
        # 如果换门 (switch)，只要原选择是羊，换门后必然是车 (因为主持人排除了另一只羊)。
        # 策略 1: 坚持原选择
        if doors[choice] == 'car':
            stick_wins += 1
        # 策略 2: 换门
        # 如果一开始选的是羊，换门必赢；如果一开始选的是车，换门必输。
        if doors[choice] == 'goat':
            switch_wins += 1
        # 记录当前的胜率
        switch_probs.append(switch_wins / i)
        stick_probs.append(stick_wins / i)
    # 输出结果
    print(f"模拟次数: {n_simulations}")
    print(f"坚持原选择胜率: {stick_wins / n_simulations:.4f} (理论值 0.3333)")
    print(f"换门胜率:       {switch_wins / n_simulations:.4f} (理论值 0.6667)")
    # 绘图
    plt.figure(figsize=(10, 6))
    plt.plot(switch_probs, label='Switch Strategy (Change)')
    plt.plot(stick_probs, label='Stick Strategy (Keep)')
    plt.axhline(y=0.6666, color='r', linestyle='--', alpha=0.5, label='Theoretical 2/3')
    plt.axhline(y=0.3333, color='g', linestyle='--', alpha=0.5, label='Theoretical 1/3')
    plt.title('Monty Hall Problem: Win Probability Convergence')
    plt.xlabel('Number of Simulations')
    plt.ylabel('Win Probability')
    plt.legend()
    plt.grid(True)
    plt.show()
# 运行仿真
monty_hall_simulation(2000)