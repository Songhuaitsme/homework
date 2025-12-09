def calculate_emv(probs, payoffs):
    """计算期望值 (Expected Monetary Value)
    probs: 概率列表 [低价概率, 中价概率, 高价概率]
    payoffs: 收益列表 [低价收益, 中价收益, 高价收益]"""
    return sum(p * v for p, v in zip(probs, payoffs))

def decision_tree_analysis():
    # 1. 定义基础数据
    # 市场状态概率: [低价, 中价, 高价]
    market_probs = [0.1, 0.5, 0.4]
    # 成功/失败概率
    prob_patent_success = 0.8
    prob_patent_fail = 0.2
    prob_research_success = 0.6
    prob_research_fail = 0.4
    # 2. 定义收益表 (单位: 万元)
    # 对应顺序: [低价, 中价, 高价]
    # 方案 A: 按原工艺生产 (用于失败时的兜底，或基准比较)
    payoff_original = [-100, 0, 100]
    # 方案 B: 买专利 (成功后)
    payoff_patent_unchanged = [-200, 50, 150]  # 产量不变
    payoff_patent_increase = [-300, 50, 250]  # 增产
    # 方案 C: 自行研究 (成功后)
    payoff_research_unchanged = [-200, 0, 200]  # 产量不变
    payoff_research_increase = [-300, -250, 600]  # 增产
    # 3. 计算各末端节点的期望值 (EMV)
    emv_original = calculate_emv(market_probs, payoff_original)
    # 买专利分支的EMV
    emv_pat_u = calculate_emv(market_probs, payoff_patent_unchanged)
    emv_pat_i = calculate_emv(market_probs, payoff_patent_increase)
    # 自研分支的EMV
    emv_res_u = calculate_emv(market_probs, payoff_research_unchanged)
    emv_res_i = calculate_emv(market_probs, payoff_research_increase)
    print(f"--->步骤 1: 计算各市场场景下的期望收益 (EMV) ---")
    print(f"原方案 EMV: {emv_original} 万元")
    print(f"买专利(产量不变) EMV: {emv_pat_u} 万元")
    print(f"买专利(增产) EMV: {emv_pat_i} 万元")
    print(f"自研(产量不变) EMV: {emv_res_u} 万元")
    print(f"自研(增产) EMV: {emv_res_i} 万元")
    # 4. 决策节点 1: 若技术革新成功，选择“产量不变”还是“增产”？
    # 取两者中的最大值
    # 买专利成功后的最优决策
    if emv_pat_i > emv_pat_u:
        emv_patent_success_node = emv_pat_i
        decision_patent_success = "增产"
    else:
        emv_patent_success_node = emv_pat_u
        decision_patent_success = "产量不变"
    # 自研成功后的最优决策
    if emv_res_i > emv_res_u:
        emv_research_success_node = emv_res_i
        decision_research_success = "增产"
    else:
        emv_research_success_node = emv_res_u
        decision_research_success = "产量不变"
    print(f"--->步骤 2: 决策节点 (若成功后的生产选择) ---")
    print(f"若买专利成功，应选择: {decision_patent_success} (EMV: {emv_patent_success_node})")
    print(f"若自研成功，应选择:   {decision_research_success} (EMV: {emv_research_success_node})")
    # 5. 机会节点: 考虑成功率与失败风险
    # 若失败，则按原方案生产 (收益为 emv_original)
    # 买专利的总期望值
    total_emv_patent = (prob_patent_success * emv_patent_success_node) + \
                       (prob_patent_fail * emv_original)
    # 自研的总期望值
    total_emv_research = (prob_research_success * emv_research_success_node) + \
                         (prob_research_fail * emv_original)
    print(f"--->步骤 3: 综合期望值 (考虑成功率) ---")
    print(f"【买专利】 方案总 EMV: {total_emv_patent:.2f} 万元")
    print(f"   计算公式: {prob_patent_success} * {emv_patent_success_node} + {prob_patent_fail} * {emv_original}")
    print(f"【自行研究】 方案总 EMV: {total_emv_research:.2f} 万元")
    print(f"   计算公式: {prob_research_success} * {emv_research_success_node} + {prob_research_fail} * {emv_original}")
    # 6. 最终决策
    print(f"--->最终结论 ---")
    if total_emv_patent > total_emv_research:
        print(f"最优方案是: **买专利**")
        print(f"后续策略: 若成功，则选择**{decision_patent_success}**；若失败，则按原方案生产。")
    else:
        print(f"最优方案是: **自行研究**")
        print(f"后续策略: 若成功，则选择**{decision_research_success}**；若失败，则按原方案生产。")

if __name__ == "__main__":
    decision_tree_analysis()