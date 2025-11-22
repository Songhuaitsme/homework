import pandas as pd

# 1. 定义所有已知数据
# 自然状态 (Theta)
states = ['t1', 't2', 't3']

# 方案 (A)
actions = ['A1', 'A2', 'A3']

# 预测 (H)
predictions = ['H1', 'H2', 'H3']

# 先验概率 P(theta_j) - 来自表3-6
prior_probs = {'t1': 0.5, 't2': 0.3, 't3': 0.2}

# 收益表 V(A_i, theta_j) - 来自表3-6
payoffs = {
    'A1': {'t1': 200, 't2': 50, 't3': -100},
    'A2': {'t1': 150, 't2': 100, 't3': -50},
    'A3': {'t1': 180, 't2': 50, 't3': -10}
}

# 似然概率 (条件概率) P(H_k | theta_j) - 来自表3-7
likelihoods = {
    'H1': {'t1': 0.6, 't2': 0.1, 't3': 0.3},  # 预测 H1 (有利)
    'H2': {'t1': 0.2, 't2': 0.7, 't3': 0.1},  # 预测 H2 (一般)
    'H3': {'t1': 0.2, 't2': 0.2, 't3': 0.6}  # 预测 H3 (不景气)
}

# --- 2. 贝叶斯计算 ---

# 存储 P(H_k)
marginal_probs_H = {}
# 存储 P(theta_j | H_k)
posterior_probs = {}
# 存储最终决策
final_decisions = {}

print("--- 贝叶斯决策计算开始 ---\n")

for k in predictions:
    print(f"=== 正在分析预测: {k} (预测{likelihoods[k].get('note', '')}) ===")

    # 2a. 计算边际概率 P(H_k) = SUM[ P(H_k | t_j) * P(t_j) ]
    marginal_p = 0
    joint_probs = {}  # 存储 P(H_k | t_j) * P(t_j)

    for j in states:
        joint = likelihoods[k][j] * prior_probs[j]
        joint_probs[j] = joint
        marginal_p += joint

    marginal_probs_H[k] = marginal_p
    print(f"P({k}) 的边际概率 = {marginal_p:.4f}")

    # 2b. 计算后验概率 P(t_j | H_k) = ( P(H_k | t_j) * P(t_j) ) / P(H_k)
    posterior_probs[k] = {}
    print("计算得到的后验概率 P(theta | H_k):")
    for j in states:
        posterior = joint_probs[j] / marginal_p
        posterior_probs[k][j] = posterior
        print(f"  P({j} | {k}) = {posterior:.4f}")

    # 3. 计算 EMV(A_i | H_k)
    emv_results = {}
    print("计算各方案的期望收益 EMV(A_i | H_k):")
    for i in actions:
        emv = 0
        for j in states:
            emv += payoffs[i][j] * posterior_probs[k][j]
        emv_results[i] = emv
        print(f"  EMV({i} | {k}) = {emv:.2f} 万元")

    # 4. 找出最优决策
    best_action = max(emv_results, key=emv_results.get)
    best_emv = emv_results[best_action]

    final_decisions[k] = {
        'best_action': best_action,
        'best_emv': best_emv
    }

    print(f"-> 结论: 若预测为 {k}，应选择方案 **{best_action}**，期望收益为 {best_emv:.2f} 万元。\n")

print("--- 计算结束 ---")

# --- 5. 汇总最终答案 ---
print("\n" + "=" * 40)
print("     最终决策方案汇总")
print("=" * 40)
print(f"| {'预测的市场情况':<10} | {'应选择的方案':<10} | {'期望收益 (万元)':<10} |")
print(f"|{'-' * 16}|{'-' * 16}|{'-' * 18}|")

for k, decision in final_decisions.items():
    if k == 'H1':
        situation = 'H1 (有利)'
    elif k == 'H2':
        situation = 'H2 (一般)'
    else:
        situation = 'H3 (不景气)'

    print(f"| {situation:<14} | {decision['best_action']:<14} | {decision['best_emv']:<16.2f} |")

print(f"|{'-' * 16}|{'-' * 16}|{'-' * 18}|")