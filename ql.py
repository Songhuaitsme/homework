import numpy as np
import random
import matplotlib.pyplot as plt  # --- 新增：用于绘图 ---
# --- 1. 定义环境和参数 (Setup) ---

r = np.array([
    [-1, -1, -1, 0, -1, -1, -1],  # 状态 0 (State 0) -> 3
    [-1, -1, 0, -1, -1, -1, -1],  # 状态 1 (State 1) -> 2
    [-1, 0, -1, 0, -1, 0, -1],  # 状态 2 (State 2) -> 1, 3, 5
    [0, -1, 0, -1, 0, -1, -1],  # 状态 3 (State 3) -> 0, 2, 4
    [-1, -1, -1, 0, -1, 0, 100],  # 状态 4 (State 4) -> 3, 5, 6
    [-1, -1, 0, -1, 0, -1, 100],  # 状态 5 (State 5) -> 2, 4, 6
    [-1, -1, -1, -1, 0, 0, 100]  # 状态 6 (State 6) -> 4, 5, 6 (Terminal)
])


q = np.zeros((7, 7))

gamma = 0.8

episodes = 1000
# --- 新增：用于记录训练结果 ---
steps_per_episode = [] # 记录每轮走了多少步

# --- 2. 训练阶段 (Training) ---
# 对应图片左侧的训练循环
print("--- 🤖 开始训练 ---")
for i in range(episodes):
    # 随机选择一个起始状态 (不能是终点 6)
    state = random.randint(0, 5)
    steps_this_episode = 0  # 初始化当前轮的步数 ---
    while state != 6:
        # --- 探索 (Exploration) ---
        # 1. 找出当前状态所有可能的行动 (r[state, action] >= 0)
        possible_actions = []
        for action in range(7):
            if r[state, action] >= 0:
                possible_actions.append(action)

        # 2. 随机选择一个可能的行动 (即下一个状态)
        # 这是为了探索环境
        next_state = random.choice(possible_actions)

        # --- Q值更新 (Bellman Equation) ---
        # 核心公式：Q(s, a) = R(s, a) + γ * max(Q(s', a'))
        # q[state, next_state] = r[state, next_state] + gamma * q[next_state].max()
        #
        # r[state, next_state]: 采取该行动的即时奖励
        # q[next_state].max(): 智能体在下一个状态所能获得的"未来"最大预期奖励
        # gamma * ...: 对未来奖励的折现

        q[state, next_state] = r[state, next_state] + gamma * q[next_state].max()

        # 3. 转移到下一个状态
        state = next_state
        steps_this_episode += 1  # --- 新增：步数加 1 ---
        # 安全退出：防止在早期训练中无限循环
        if steps_this_episode > 100:
            break

    steps_per_episode.append(steps_this_episode)  # --- 新增：记录本轮的总步数 ---

print("--- ✅ 训练完成 ---")
print("最终的 Q-Table (四舍五入到2位小数):")
print(np.round(q, 2))


# --- 新增：绘制训练结果图表 ---

def plot_training_results(steps_list):
    print("\n--- 📊 正在生成训练结果图表 ---")
    plt.figure(figsize=(12, 6))

    # 绘制原始的每轮步数（会很杂乱）
    plt.plot(steps_list, alpha=0.3, label='Steps per Episode')

    # 计算并绘制移动平均线（更能反映趋势）
    # 使用 50 轮的窗口计算移动平均值
    window_size = 50
    if len(steps_list) >= window_size:
        # 使用 np.convolve 计算移动平均
        moving_avg = np.convolve(steps_list, np.ones(window_size) / window_size, mode='valid')
        # 绘制移动平均线
        plt.plot(range(window_size - 1, len(steps_list)), moving_avg, color='red',
                 label=f'{window_size}-Episode Moving Average')

    plt.title('Training Progress: Steps to Reach Goal')
    plt.xlabel('Episode')
    plt.ylabel('Number of Steps')
    plt.legend()
    plt.grid(True)

    # 保存图表
    plt.savefig("training_progress.png")
    print("图表已保存为 training_progress.png")
    # 显示图表
    plt.show()


plot_training_results(steps_per_episode)

# --- 3. 测试阶段 (Testing / Exploitation) ---
# 对应图片右侧的测试代码
print("\n--- 🤖 开始测试 (从随机位置出发) ---")

# 随机选择一个起始点
state = random.randint(0, 5)
print(f"机器人初始位置于: {state}")

count = 0
path = [state]  # 记录路径

while state != 6:
    # 对应图片中的 "if count > 20" 安全检查
    count += 1
    if count > 20:
        print("测试失败：超过20步，可能陷入循环")
        break

    # --- 利用 (Exploitation) ---
    # 1. 找到当前状态下 Q 值最大的那个值
    q_max = q[state].max()

    # 2. 找到所有等于最大 Q 值的行动 (可能不止一个)
    q_max_actions = []
    for action in range(7):
        if q[state, action] == q_max:
            q_max_actions.append(action)

    # 3. 从所有最佳行动中随机选择一个
    # (图片中用了 random.randint，这里用 random.choice 更简洁，逻辑一致)
    next_state = random.choice(q_max_actions)

    print(f"机器人 goes to {next_state}.")
    path.append(next_state)
    state = next_state

if state == 6:
    print(f"🏆 成功! 机器人到达终点 6.")
    print(f"路径: {' -> '.join(map(str, path))}")

# --- 3. 测试阶段 (Testing / Exploitation) ---
# (确保这部分在前面板训练代码运行之后执行)

print("\n--- 🤖 开始测试 (从指定位置 1 出发) ---")

# --- 修改点：指定起始状态为 0 ---
state = 1
# --------------------------------

print(f"机器人初始位置于: {state}")

count = 0
path = [state]  # 记录路径

while state != 6:
    count += 1
    if count > 20:
        print("测试失败：超过20步，可能陷入循环")
        break

    # --- 利用 (Exploitation) ---
    # 1. 找到当前状态下 Q 值最大的那个值
    q_max = q[state].max()

    # 2. 找到所有等于最大 Q 值的行动 (可能不止一个)
    q_max_actions = []
    for action in range(7):
        # 确保动作是有效的 (Q > 0 或 R >= 0)
        # 并且等于最大值
        if q[state, action] == q_max and q[state, action] > 0:
            q_max_actions.append(action)

    # 如果没有找到 Q > 0 的行动（可能在训练不足时发生），则退回原始R矩阵找路
    if not q_max_actions:
        print(f" (在状态 {state} 遇到困难，根据R矩阵探索...)")
        for action in range(7):
            if r[state, action] >= 0:
                q_max_actions.append(action)
        if not q_max_actions:
            print("彻底卡住，无法移动。")
            break

    # 3. 从所有最佳行动中随机选择一个
    next_state = random.choice(q_max_actions)

    print(f"机器人 goes to {next_state}.")
    path.append(next_state)
    state = next_state

if state == 6:
    print(f"🏆 成功! 机器人到达终点 6.")
    print(f"路径: {' -> '.join(map(str, path))}")