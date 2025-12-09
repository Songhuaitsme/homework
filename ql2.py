import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns
import os  # 引入 os 库来创建文件夹

# 1. 定义环境 (R-Matrix)
r = np.array([
    [-1, -1, -1, 0, -1, -1, -1],  # 0
    [-1, -1, 0, -1, -1, -1, -1],  # 1
    [-1, 0, -1, 0, -1, 0, -1],  # 2
    [0, -1, 0, -1, 0, -1, -1],  # 3
    [-1, -1, -1, 0, -1, 0, 100],  # 4
    [-1, -1, 0, -1, 0, -1, 100],  # 5
    [-1, -1, -1, -1, 0, 0, 100]  # 6
])


def run_experiment(gamma, episodes=2001, update_freq=100):
    """
    运行Q-Learning训练并按指定频率保存热力图。

    更改说明:
    gamma (float): 衰减因子
    episodes (int): 总训练轮次
    update_freq (int): 每隔多少轮保存一次图像
    """

    print(f"\n--- 🚀 开始实验: Gamma = {gamma} ---")

    # 为此次实验创建一个文件夹
    save_dir = f"gamma_{gamma}"
    os.makedirs(save_dir, exist_ok=True)
    print(f"图像将保存到: {save_dir}/")

    # 每次实验都重新初始化 Q-Table
    q = np.zeros((7, 7))

    for i in range(episodes):
        state = random.randint(0, 5)

        while state != 6:
            # 探索：找到所有可能的动作
            possible_actions = [a for a, reward in enumerate(r[state]) if reward >= 0]

            # 探索：随机选择一个动作
            next_state = random.choice(possible_actions)

            # Q-Learning 核心公式
            q[state, next_state] = r[state, next_state] + gamma * q[next_state].max()

            state = next_state

        # --- 核心修改：保存图像 ---
        # 每 100 轮或在最后一轮保存
        if i % update_freq == 0 or i == episodes - 1:

            # 1. 创建一个新的图像窗口
            fig, ax = plt.subplots(figsize=(8, 6))

            # 2. 绘制热力图
            # vmin=0, vmax=101: 固定颜色范围，确保所有图像的颜色刻度一致
            sns.heatmap(q, ax=ax, annot=True, fmt=".1f", cmap="viridis",
                        linewidths=.5, cbar=True, vmin=0, vmax=101)

            ax.set_title(f"Q-Table (Gamma = {gamma} | Episode: {i})")
            ax.set_xlabel("Action (Next State)")
            ax.set_ylabel("Current State")

            # 3. 定义保存路径
            # 使用 zfill(4) 确保文件名按数字顺序排列 (例如 0100, 0200, ... 1000)
            filename = f"{save_dir}/episode_{str(i).zfill(4)}.png"

            # 4. 保存图像
            plt.savefig(filename)

            # 5. 关闭图像，防止内存泄漏
            plt.close(fig)

            if i % update_freq == 0:
                print(f"  ...已保存 {filename}")

    print(f"--- ✅ 实验完成: Gamma = {gamma} ---")


# --- 运行主程序 ---
if __name__ == "__main__":
    # 实验1: 高 Gamma (有远见)
    run_experiment(gamma=0.9)

    # 实验2: 低 Gamma (短视)
    run_experiment(gamma=0.2)

    print("\n所有实验均已完成。请检查生成的文件夹。")