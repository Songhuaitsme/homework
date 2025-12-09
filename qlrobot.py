import random


# ==========================================
# 第一部分：算法核心逻辑实现
# ==========================================

def choose_action(state, q_table, epsilon, actions=['u', 'r', 'd', 'l']):
    """
    实现 Epsilon-Greedy 策略 (对应截图中的编程练习)
    :param state: 当前机器人的状态 (例如 's1')
    :param q_table: 存储 Q 值的字典，格式 {state: {action: q_value}}
    :param epsilon: 探索概率 (0.0 ~ 1.0)
    :param actions: 动作列表
    :return: 选择的动作
    """
    action = None

    # 获取当前状态下的 Q 值字典，如果不存在则初始化为 0
    state_actions = q_table.get(state, {a: 0.0 for a in actions})

    # --- 核心逻辑开始 ---
    # 产生一个 0 到 1 之间的随机数
    if random.uniform(0, 1) < epsilon:
        # 【探索模式】：以 epsilon 的概率随机选择动作
        action = random.choice(actions)
        print(f"DEBUG: 触发探索 (Random) -> {action}")
    else:
        # 【利用模式】：选择具有最大 Q 值的动作
        # 使用 max 函数配合 key 参数，找到 value 最大的那个 key
        # 如果有多个最大值，默认取第一个，或者可以添加随机打断逻辑
        action = max(state_actions, key=state_actions.get)
        print(f"DEBUG: 触发利用 (Max Q) -> {action}")
    # --- 核心逻辑结束 ---

    return action


def update_q_table(q_table, state, action, reward, next_state, alpha, gamma, actions=['u', 'r', 'd', 'l']):
    """
    实现 Q-learning 的更新公式 (对应截图中的数学计算题)
    Q(s,a) <- Q(s,a) + alpha * [r + gamma * max(Q(s', a')) - Q(s,a)]
    """
    # 1. 获取旧的 Q 值: Q(s, a)
    old_q = q_table.get(state, {}).get(action, 0.0)

    # 2. 获取下一个状态的最大 Q 值: max Q(s', a')
    # 获取 next_state 的所有动作 Q 值，如果 next_state 不在表中，假设为 0
    next_state_q_values = q_table.get(next_state, {a: 0.0 for a in actions})
    max_q_next = max(next_state_q_values.values())

    # 3. 计算目标值 Target = R + gamma * max Q(s')
    target = reward + gamma * max_q_next

    # 4. 更新 Q 值
    new_q = old_q + alpha * (target - old_q)

    # 将新值写入 Q 表
    if state not in q_table:
        q_table[state] = {}
    q_table[state][action] = new_q

    return new_q, target, old_q


# ==========================================
# 第二部分：运行题目中的具体案例
# ==========================================

if __name__ == "__main__":
    print("-" * 30)
    print("任务 1: 测试 Epsilon-Greedy 代码逻辑")
    print("-" * 30)

    # 模拟一个简单的 Q 表数据用于测试 choose_action
    test_q_line = {'s1': {'u': 1.2, 'r': -2.1, 'd': -24.5, 'l': 27}}
    epsilon_val = 0.3

    # 运行 5 次看看效果
    for i in range(5):
        act = choose_action('s1', test_q_line, epsilon_val)

    print("\n" + "-" * 30)
    print("任务 2: 求解题目中的 Q 值更新")
    print("-" * 30)

    # --- 1. 初始化题目给定的已知条件 (截图 3) ---
    gamma = 0.9  # 衰减因子
    alpha = 0.7  # 学习率

    # 初始化 Q-Table (根据截图 3 中的表格)
    # 注意：s2 的最大值是 'l': 40
    q_table_data = {
        's1': {'u': 10, 'r': -0.29, 'd': -0.29, 'l': 0},
        's2': {'u': -24, 'r': -13, 'd': -0.29, 'l': 40},
        's3': {'u': -20, 'r': -20, 'd': 10, 'l': -20},
        's4': {'u': 0, 'r': 0, 'd': 0, 'l': 0}
    }

    # 当前状态和动作
    current_state = 's1'
    current_action = 'u'

    # 下一个状态 (根据地图，从 s1 向上走 u 会到达 s2)
    next_state = 's2'

    # 奖励 (根据规则：走到普通格子奖励是 -0.1)
    # 题目并未说 s2 是陷阱或终点，所以是普通情况
    reward = -0.1

    print(f"已知条件:")
    print(f"  当前状态: {current_state}, 采取动作: {current_action}")
    print(f"  到达状态: {next_state}, 获得奖励: {reward}")
    print(f"  旧的 Q({current_state}, {current_action}): {q_table_data[current_state][current_action]}")
    print(f"  s2 中最大的 Q 值 (max Q(s2)): {max(q_table_data['s2'].values())} (对应动作 'l': 40)")

    # --- 2. 执行计算 ---
    new_q_value, target_q, old_q_val = update_q_table(
        q_table_data,
        current_state,
        current_action,
        reward,
        next_state,
        alpha,
        gamma
    )

    print("\n计算结果:")
    print(f"  目标 Q 值 (Target) = {reward} + {gamma} * {max(q_table_data['s2'].values())} = {target_q}")
    print(f"  TD Error (差值) = {target_q} - {old_q_val} = {target_q - old_q_val}")
    print(f"  更新公式: New_Q = {old_q_val} + {alpha} * ({target_q} - {old_q_val})")
    print(f"  最终结果 New Q({current_state}, {current_action}) = {new_q_value:.2f}")

    # 验证是否符合手动计算: 10 + 0.7 * (-0.1 + 0.9*40 - 10) = 28.13