def calculate_emv(payoffs, probabilities):
    """
    一个辅助函数，用于计算给定收益和概率的期望货币价值(EMV)。

    :param payoffs: 一个包含收益的列表 (例如: [-100, 0, 100])
    :param probabilities: 一个包含相应概率的列表 (例如: [0.1, 0.5, 0.4])
    :return: 计算出的EMV值
    """
    return sum(p * v for p, v in zip(probabilities, payoffs))


# --- 1. 定义基本数据 ---

# 市场状态的概率
market_probs = [0.1, 0.5, 0.4]  # [低价, 中价, 高价]

# 收益表 (单位: 万元)
payoffs = {
    'original': [-100, 0, 100],
    'buy_no_change': [-200, 50, 150],
    'buy_increase': [-300, 50, 250],
    'self_no_change': [-200, 0, 200],
    'self_increase': [-300, -250, 600]
}

# 成功/失败的概率
prob_buy = {'success': 0.8, 'failure': 0.2}
prob_self = {'success': 0.6, 'failure': 0.4}

print("开始计算决策树的期望货币价值 (EMV)...")
print("-" * 40)

# --- 2. 计算各个分支的EMV (从后往前推) ---

# 步骤 2a: 计算“按原工艺”的EMV (这是基准)
emv_original = calculate_emv(payoffs['original'], market_probs)
print(f"方案 A: 按原工艺的 EMV = {emv_original:.2f} 万元")

# 步骤 2b: 计算“买专利”分支
#   - 如果成功，需要从“产量不变”和“增产”中选一个
emv_buy_success_no_change = calculate_emv(payoffs['buy_no_change'], market_probs)
emv_buy_success_increase = calculate_emv(payoffs['buy_increase'], market_probs)

print(f"  [买专利->成功] '产量不变' 的 EMV = {emv_buy_success_no_change:.2f} 万元")
print(f"  [买专利->成功] '增产' 的 EMV = {emv_buy_success_increase:.2f} 万元")

# 决策点：选择两者中EMV最大的
emv_buy_success = max(emv_buy_success_no_change, emv_buy_success_increase)
if emv_buy_success == emv_buy_success_increase:
    decision_after_buy = "增产"
else:
    decision_after_buy = "产量不变"
print(f"  -> 买专利成功后的最优选择是 '{decision_after_buy}' (EMV = {emv_buy_success:.2f} 万元)")

#   - 如果失败，则EMV等于“按原工艺”
emv_buy_failure = emv_original

#   - 计算“买专利”的总EMV
emv_buy_total = (prob_buy['success'] * emv_buy_success) + (prob_buy['failure'] * emv_buy_failure)
print(
    f"\n方案 B: 买专利的总 EMV = (0.8 * {emv_buy_success:.2f}) + (0.2 * {emv_buy_failure:.2f}) = {emv_buy_total:.2f} 万元")

# 步骤 2c: 计算“自研”分支
#   - 如果成功，需要从“产量不变”和“增产”中选一个
emv_self_success_no_change = calculate_emv(payoffs['self_no_change'], market_probs)
emv_self_success_increase = calculate_emv(payoffs['self_increase'], market_probs)

print(f"\n  [自研->成功] '产量不变' 的 EMV = {emv_self_success_no_change:.2f} 万元")
print(f"  [自研->成功] '增产' 的 EMV = {emv_self_success_increase:.2f} 万元")

# 决策点：选择两者中EMV最大的
emv_self_success = max(emv_self_success_no_change, emv_self_success_increase)
if emv_self_success == emv_self_success_increase:
    decision_after_self = "增产"
else:
    decision_after_self = "产量不变"
print(f"  -> 自研成功后的最优选择是 '{decision_after_self}' (EMV = {emv_self_success:.2f} 万元)")

#   - 如果失败，则EMV等于“按原工艺”
emv_self_failure = emv_original

#   - 计算“自研”的总EMV
emv_self_total = (prob_self['success'] * emv_self_success) + (prob_self['failure'] * emv_self_failure)
print(
    f"\n方案 C: 自研的总 EMV = (0.6 * {emv_self_success:.2f}) + (0.4 * {emv_self_failure:.2f}) = {emv_self_total:.2f} 万元")

# --- 3. 比较三个初始方案，得出最终结论 ---
print("-" * 40)

results = {
    '按原工艺': emv_original,
    '买专利': emv_buy_total,
    '自研': emv_self_total
}

# 找到EMV最高的决策
optimal_decision = max(results, key=results.get)
max_emv = results[optimal_decision]

print("最终决策比较:")
print(f"  按原工艺 EMV: {results['按原工艺']:.2f} 万元")
print(f"  买专利 EMV: {results['买专利']:.2f} 万元")
print(f"  自研 EMV: {results['自研']:.2f} 万元")

print("\n" + "=" * 40)
print(f"🏆 最优决策是: **{optimal_decision}**")
print(f"   其期望货币价值 (EMV) 为: **{max_emv:.2f} 万元**")
print("=" * 40)

# 打印完整的策略路径
if optimal_decision == '买专利':
    print(f"\n推荐的完整策略是：")
    print(f"1. 选择 '{optimal_decision}'。")
    print(f"2. 如果成功 (80% 概率), 则选择 '{decision_after_buy}'。")
    print(f"3. 如果失败 (20% 概率), 则 '按原方案生产'。")
elif optimal_decision == '自研':
    print(f"\n推荐的完整策略是：")
    print(f"1. 选择 '{optimal_decision}'。")
    print(f"2. 如果成功 (60% 概率), 则选择 '{decision_after_self}'。")
    print(f"3. 如果失败 (40% 概率), 则 '按原方案生产'。")
else:
    print(f"\n推荐的完整策略是：\n1. 选择 '{optimal_decision}'。")