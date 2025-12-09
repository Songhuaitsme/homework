import pulp
def solve_production_problem():
    # 1. 创建问题实例
    prob = pulp.LpProblem("Production_Optimization", pulp.LpMinimize)
    # 2. 定义决策变量 (单位: 万件)
    x_A = pulp.LpVariable('Product_A', lowBound=0, cat='Continuous')
    x_B = pulp.LpVariable('Product_B', lowBound=0, cat='Continuous')
    # 3. 添加硬约束 (材料限制)
    prob += 0.5 * x_A + 0.3 * x_B <= 300, "Material_Jia_Limit"
    prob += 0.2 * x_A + 0.3 * x_B <= 240, "Material_Yi_Limit"
    # ==========================================
    # 优先级 1: 确保利润值恰好为 755 (最小化偏差)
    # ==========================================
    print("--- 正在计算优先级 1 ---")
    # 定义偏差变量 d1_neg (负偏差/不足), d1_pos (正偏差/超出)
    d1_neg = pulp.LpVariable('d1_neg', lowBound=0)
    d1_pos = pulp.LpVariable('d1_pos', lowBound=0)
    prob += 1.3 * x_A + 1.0 * x_B + d1_neg - d1_pos == 755, "Profit_Goal_Constraint"
    # P1 目标: 最小化偏差之和 (d1_neg + d1_pos)
    prob.setObjective(d1_neg + d1_pos)
    prob.solve()
    # 获取 P1 的结果
    p1_deviation = pulp.value(d1_neg) + pulp.value(d1_pos)
    print(f"P1 结果: 最小偏差 = {p1_deviation}")
    # 将 P1 达成的效果固化为硬约束，供下一级使用
    prob += d1_neg + d1_pos <= p1_deviation + 1e-5, "Lock_P1_Result"
    # ==========================================
    # 优先级 2: B产量不低于650，且尽可能多生产 B
    # ==========================================
    print("\n--- 正在计算优先级 2 ---")
    prob += x_B >= 650, "B_Min_Requirement"
    # P2 目标: 最大化 B 的产量
    prob.setObjective(-x_B)
    prob.solve()
    # 获取 P2 的结果
    p2_max_B = pulp.value(x_B)
    print(f"P2 结果: B 的最大产量 = {p2_max_B}")
    # 将 P2 达成的效果固化为硬约束
    prob += x_B >= p2_max_B - 1e-5, "Lock_P2_Result"
    # ==========================================
    # 优先级 3: 在确保上述前提下，最大化总利润
    # ==========================================
    print("\n--- 正在计算优先级 3 ---")
    # P3 目标: 最大化利润 (1.3A + 1.0B) -> 最小化 -(1.3A + 1.0B)
    prob.setObjective(-(1.3 * x_A + 1.0 * x_B))
    prob.solve()
    # ==========================================
    # 输出最终决策分析结果
    # ==========================================
    print("\n" + "=" * 30)
    print("最终决策分析报告")
    print("=" * 30)
    print(f"求解状态: {pulp.LpStatus[prob.status]}")
    print(f"产品 A 产量: {pulp.value(x_A):.2f} (万件)")
    print(f"产品 B 产量: {pulp.value(x_B):.2f} (万件)")
    total_profit = 1.3 * pulp.value(x_A) + 1.0 * pulp.value(x_B)
    print(f"总利润: {total_profit:.2f} (万元)")
    # 验证约束情况
    material_jia_used = 0.5 * pulp.value(x_A) + 0.3 * pulp.value(x_B)
    material_yi_used = 0.2 * pulp.value(x_A) + 0.3 * pulp.value(x_B)
    print(f"材料甲消耗: {material_jia_used:.2f} / 300")
    print(f"材料乙消耗: {material_yi_used:.2f} / 240")
    print(f"B产量达标情况: {pulp.value(x_B)} >= 650")
if __name__ == "__main__":
    solve_production_problem()