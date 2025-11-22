# 1. 定义收益数据
# 我们可以使用一个字典来存储收益表
# 键是决策方案，值是该方案在不同状态下的收益列表
payoff_data = {
    'a1 (投产)': [20, -3],
    'a2 (不投产)': [0, 0]
}

print("原始收益数据:")
for decision, payoffs in payoff_data.items():
    print(f"{decision}: {payoffs}")

print("-" * 30)

# 2. 找出每个决策的“最小收益”（悲观情况）
min_payoffs = {}
for decision, payoffs in payoff_data.items():
    # 使用 min() 函数找到列表中的最小值
    min_val = min(payoffs)
    min_payoffs[decision] = min_val

print("各决策的最小收益（最坏情况）:")
for decision, min_val in min_payoffs.items():
    print(f"{decision}: {min_val}")

print("-" * 30)

# 3. 找出“最小收益”中的“最大值” (Max-Min)
# .values() 获取所有的最小收益值，例如 [-3, 0]
max_min_value = max(min_payoffs.values())

print(f"“最小收益”中的最大值是: {max_min_value}")

# 4. 找到对应该最大值的决策
optimal_decisions = []
for decision, min_val in min_payoffs.items():
    if min_val == max_min_value:
        optimal_decisions.append(decision)

# 5. 打印最终结果
print(f"根据Max-Min（最大最小）原则，最优决策是:")
for decision in optimal_decisions:
    print(f"**{decision}**")