import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_decision_tree():
    # 设置支持中文的字体（根据您的系统环境可能需要调整，如 SimHei, Microsoft YaHei 等）
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    # 定义节点样式
    # 决策节点（方形）
    decision_node_style = dict(boxstyle="square,pad=0.3", fc="lightgreen", ec="black", lw=2)
    # 机会节点（圆形）
    chance_node_style = dict(boxstyle="circle,pad=0.3", fc="lightblue", ec="black", lw=2)
    # 结果/叶节点（灰色圆角）
    leaf_node_style = dict(boxstyle="round,pad=0.3", fc="lightgray", ec="black", lw=1)
    # 绘制连线的辅助函数
    def connect(xy1, xy2, text=None, text_offset=(0, 0.2), color="black", linestyle="-"):
        ax.plot([xy1[0], xy2[0]], [xy1[1], xy2[1]], color=color, lw=1.5, linestyle=linestyle)
        if text:
            mid_x = (xy1[0] + xy2[0]) / 2
            mid_y = (xy1[1] + xy2[1]) / 2
            ax.text(mid_x + text_offset[0], mid_y + text_offset[1], text,
                    ha='center', va='center', fontsize=10, color='darkblue', backgroundcolor='white')
    # 绘制节点的辅助函数
    def draw_node(xy, text, style):
        ax.text(xy[0], xy[1], text, ha='center', va='center', fontsize=10, bbox=style, zorder=10)
    # --- 1. 定义坐标位置 ---
    root_xy = (1, 5)  # 根节点
    # 第一层：两个主要方案（机会节点）
    pat_xy = (3, 7.5)  # 买专利
    res_xy = (3, 2.5)  # 自研
    # 第二层：成功/失败分支
    pat_succ_xy = (5, 8.5)  # 专利成功（决策点）
    pat_fail_xy = (5, 6.5)  # 专利失败（结果）
    res_succ_xy = (5, 3.5)  # 自研成功（决策点）
    res_fail_xy = (5, 1.5)  # 自研失败（结果）
    # 第三层：具体的生产决策及其EMV（叶节点）
    pat_succ_unc_xy = (8, 9)  # 专利成功-产量不变
    pat_succ_inc_xy = (8, 8)  # 专利成功-增产
    pat_fail_leaf_xy = (8, 6.5)  # 专利失败-原方案
    res_succ_unc_xy = (8, 4)  # 自研成功-产量不变
    res_succ_inc_xy = (8, 3)  # 自研成功-增产
    res_fail_leaf_xy = (8, 1.5)  # 自研失败-原方案
    # --- 2. 绘制连线 ---
    # 从根节点出发
    connect(root_xy, pat_xy, "买专利\n(EMV=82)", (-0.2, 0), color="red")  # 标记为最优决策
    connect(root_xy, res_xy, "自行研究\n(EMV=63)", (-0.2, 0))
    # 买专利分支
    connect(pat_xy, pat_succ_xy, "成功 (0.8)", (-0.5, 0.3))
    connect(pat_xy, pat_fail_xy, "失败 (0.2)", (-0.5, -0.3))
    # 自行研究分支
    connect(res_xy, res_succ_xy, "成功 (0.6)", (-0.5, 0.3))
    connect(res_xy, res_fail_xy, "失败 (0.4)", (-0.5, -0.3))
    # 专利成功后的决策
    connect(pat_succ_xy, pat_succ_unc_xy, "产量不变", (0, 0.2))
    connect(pat_succ_xy, pat_succ_inc_xy, "增产 (最优)", (0, -0.2), color="red")  # 子决策最优
    # 专利失败
    connect(pat_fail_xy, pat_fail_leaf_xy, "原方案", (0, 0))
    # 自研成功后的决策
    connect(res_succ_xy, res_succ_unc_xy, "产量不变", (0, 0.2))
    connect(res_succ_xy, res_succ_inc_xy, "增产 (最优)", (0, -0.2), color="red")  # 子决策最优
    # 自研失败
    connect(res_fail_xy, res_fail_leaf_xy, "原方案", (0, 0))
    # --- 3. 绘制节点 ---
    draw_node(root_xy, "决策\n起点", decision_node_style)
    draw_node(pat_xy, "专利\n机会", chance_node_style)
    draw_node(res_xy, "自研\n机会", chance_node_style)
    draw_node(pat_succ_xy, "生产\n决策", decision_node_style)
    draw_node(pat_fail_xy, "结果", leaf_node_style)
    draw_node(res_succ_xy, "生产\n决策", decision_node_style)
    draw_node(res_fail_xy, "结果", leaf_node_style)
    draw_node(pat_succ_unc_xy, "EMV: 65", leaf_node_style)
    draw_node(pat_succ_inc_xy, "EMV: 95", leaf_node_style)
    draw_node(pat_fail_leaf_xy, "EMV: 30", leaf_node_style)
    draw_node(res_succ_unc_xy, "EMV: 60", leaf_node_style)
    draw_node(res_succ_inc_xy, "EMV: 85", leaf_node_style)
    draw_node(res_fail_leaf_xy, "EMV: 30", leaf_node_style)
    plt.title("决策树分析图 (单位: 万元)", fontsize=16)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    draw_decision_tree()