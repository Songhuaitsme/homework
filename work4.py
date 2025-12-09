import gurobipy as gp
from gurobipy import GRB
import random
import pandas as pd
import matplotlib.pyplot as plt

def solve_portfolio_scenario(synergy_ab_val, synergy_cd_val, scenario_id):
    """针对给定的协同效应值求解最优项目组合"""
    # 1. 创建模型
    m = gp.Model(f"Portfolio_Scenario_{scenario_id}")
    m.setParam('OutputFlag', 0)  # 静默模式，不输出求解日志
    # 2. 定义数据
    projects = ['A', 'B', 'C', 'D']
    costs = {'A': 50, 'B': 40, 'C': 55, 'D': 35}
    returns = {'A': 100, 'B': 80, 'C': 110, 'D': 60}
    budget = 150
    # 3. 定义变量 (0-1 变量)
    x = m.addVars(projects, vtype=GRB.BINARY, name="x")
    # 定义协同效应的辅助变量 (线性化 xA*xB 和 xC*xD)
    # z_ab = 1 当且仅当 A和B都被选中,z_cd = 1 当且仅当 C和D都被选中
    z_ab = m.addVar(vtype=GRB.BINARY, name="z_ab")
    z_cd = m.addVar(vtype=GRB.BINARY, name="z_cd")
    # 4. 设置约束
    # 预算约束
    m.addConstr(gp.quicksum(x[i] * costs[i] for i in projects) <= budget, name="Budget")
    # 协同效应逻辑约束 (Linearization)
    # z_ab <= x['A'], z_ab <= x['B'], z_ab >= x['A'] + x['B'] - 1
    m.addConstr(z_ab <= x['A'])
    m.addConstr(z_ab <= x['B'])
    m.addConstr(z_ab >= x['A'] + x['B'] - 1)
    # z_cd <= x['C'], z_cd <= x['D'], z_cd >= x['C'] + x['D'] - 1
    m.addConstr(z_cd <= x['C'])
    m.addConstr(z_cd <= x['D'])
    m.addConstr(z_cd >= x['C'] + x['D'] - 1)
    # 5. 设置目标函数：最大化 (基础收益 + 协同收益)
    base_return = gp.quicksum(x[i] * returns[i] for i in projects)
    synergy_return = (synergy_ab_val * z_ab) + (synergy_cd_val * z_cd)
    m.setObjective(base_return + synergy_return, GRB.MAXIMIZE)
    # 6. 求解
    m.optimize()
    # 7. 提取结果
    if m.status == GRB.OPTIMAL:
        selected = [p for p in projects if x[p].x > 0.5]
        total_return = m.ObjVal
        return sorted(selected), total_return
    else:
        return None, 0

def robust_decision_analysis():
    # 模拟次数
    num_scenarios = 150
    results = []
    print(f"--- 开始 {num_scenarios} 次不确定性模拟 ---")
    print(f"{'场景':<5} | {'AB协同':<8} | {'CD协同':<8} | {'最优组合':<15} | {'总收益':<8}")
    print("-" * 60)
    decision_counts = {}
    for i in range(num_scenarios):
        # 随机生成协同效应值 (均匀分布)
        # A和B协同: [10, 40]
        syn_ab = random.uniform(10, 40)
        # C和D协同: [20, 50]
        syn_cd = random.uniform(20, 50)
        # 求解
        selected_projects, profit = solve_portfolio_scenario(syn_ab, syn_cd, i + 1)
        combo_str = "+".join(selected_projects)
        # 记录
        results.append({
            'Scenario': i + 1,
            'Synergy_AB': syn_ab,
            'Synergy_CD': syn_cd,
            'Selection': combo_str,
            'Profit': profit
        })
        # 统计频次
        decision_counts[combo_str] = decision_counts.get(combo_str, 0) + 1
        print(f"{i + 1:<5} | {syn_ab:.2f}     | {syn_cd:.2f}     | {combo_str:<15} | {profit:.2f}")
    print("-" * 60)
    print("--- 鲁棒性分析结论 ---")
    best_decision = max(decision_counts, key=decision_counts.get)
    print("在所有模拟场景中，各组合出现次数：")
    for combo, count in decision_counts.items():
        print(f"  组合 [{combo}]: {count} 次 (占比 {count / num_scenarios * 100:.1f}%)")
    print(f"推荐的鲁棒决策是: **{best_decision}**")
    # 可选：计算最坏情况 (Max-Min Robustness)
    # 最坏情况：协同效应取下限 AB=10, CD=20
    wc_combo, wc_profit = solve_portfolio_scenario(10, 20, "WorstCase")
    print(f"[验证] 最坏情况 (AB=10, CD=20) 下的最优解: {'+'.join(wc_combo)} (收益: {wc_profit})")

if __name__ == "__main__":
    robust_decision_analysis()