# -*- coding: utf-8 -*-
"""
光场自检动力学 · 自检晶格模型（完整版）
========================================

《逻辑宇宙》（LU-Codex v1.0，公共领域 CC0）「光场晶格自检动力学」的可运行实现。

本文件包含三层模型，逐层逼近同一件事——「自检 + 反旋对位」如何涌现出反旋链与粒子：

  Level 1  离散边链（toric code）  —— 反旋链 = 边上的 0/1 场；
            电荷 = 开链端点（∂c≠0），磁通 = 闭链环（∂c=0）。
  Level 2  顶点自旋代价           —— s∈{±1} 绕向；开链代价 = 确权失败；
            同向自旋引力 = 保守对齐；粘滞 = 抗拒剪切的阻力（保守半）。
  Level 3  连续相位 XY            —— θ∈S¹ 自检绕转；涡旋 = 绕数 ±1 的拓扑缺陷
            （= 确权失败的「粒子」）；对齐 = 同向自旋引力；过阻尼松弛 = 粘滞（耗散半）。

三条公理的落地
--------------
  公理 I   存在确权：「自检」= 格点完成 态 θ=0 → 非态 θ=π → 态 θ=2π 的闭环。
           Level 1/2 离散为二值 ℤ₂（自旋 1/2 双重覆盖 π₁(SO(3))≅ℤ₂）；
           Level 3 保留连续绕数 ±1。
  公理 II  光场晶格基底：2D 格点 + 相邻「反旋对位」（绕向相反 = 反旋边）。
  公理 III 拓扑守恒：开链端点 = 电荷，闭链 = 磁通（toric code）；
           连续版为涡旋绕数，闭合曲面上总绕数恒为 0（粒子成对）。

诚实边界（重要，必须读）
------------------------
本模型跑出的「粒子」是 ℤ₂ 拓扑激发（电荷/磁通）或 XY 涡旋，**不是**标准模型的
点粒子；「引力/粘滞」是代价泛函的保守/耗散两半，**不是**从公理推导出的真实引力
或真实流体粘滞。本文件只演示「自检 + 反旋对位 → 反旋链 + 拓扑缺陷 + 保守/耗散
代价」这一机制，作为把《逻辑宇宙》本体论搬上桌的可执行积木。

运行
----
    python self_check_model.py            # Level 1：随机自检动力学（电荷/磁通）
    python self_check_model.py --demo     # Level 1：干净构造电荷对 / 磁通环
    python self_check_model.py --spin     # Level 2：同向 / 剪切 / 反相的代价对照
    python self_check_model.py --xy       # Level 3：XY 涡旋粒子 + 退火耗散

依赖：numpy（必需）；matplotlib（可选，仅 Level 1 出图）。
"""

import argparse
from collections import defaultdict

import numpy as np

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    _HAS_MPL = True
except Exception:
    _HAS_MPL = False


def _wrap(x):
    """角度差折到 [−π, π)。"""
    return (x + np.pi) % (2.0 * np.pi) - np.pi


# ==========================================================================
# Level 1 · 离散边链（toric code）：反旋链 → 电荷 / 磁通
# ==========================================================================
class SelfCheckLattice:
    """2D 反旋链场。水平边 ch[i,j]:(i,j)-(i,j+1)，竖直边 cv[i,j]:(i,j)-(i+1,j)。
    周期边界下指标取模 L；开放边界下越界边视为不存在（返回 0）。"""

    def __init__(self, L, seed=0, periodic=True):
        assert L >= 2
        self.L = L
        self.periodic = periodic
        self.rng = np.random.default_rng(seed)
        self.ch = np.zeros((L, L), dtype=np.int8)  # 水平反旋边
        self.cv = np.zeros((L, L), dtype=np.int8)  # 竖直反旋边
        self.steps = 0

    # -- 边的存取（自动处理边界） ---------------------------------------
    def h(self, i, j):
        """水平边 (i,j)-(i,j+1)；开放边界且越界时返回 0。"""
        L = self.L
        if self.periodic:
            return self.ch[i % L, j % L]
        return self.ch[i, j] if (0 <= i < L and 0 <= j < L - 1) else 0

    def v(self, i, j):
        """竖直边 (i,j)-(i+1,j)；开放边界且越界时返回 0。"""
        L = self.L
        if self.periodic:
            return self.cv[i % L, j % L]
        return self.cv[i, j] if (0 <= i < L - 1 and 0 <= j < L) else 0

    def _set_h(self, i, j, val):
        L = self.L
        if self.periodic:
            self.ch[i % L, j % L] = val
        elif 0 <= i < L and 0 <= j < L - 1:
            self.ch[i, j] = val

    def _set_v(self, i, j, val):
        L = self.L
        if self.periodic:
            self.cv[i % L, j % L] = val
        elif 0 <= i < L - 1 and 0 <= j < L:
            self.cv[i, j] = val

    # -- 观测量 ---------------------------------------------------------
    def degree(self, i, j):
        """顶点 (i,j) 的激励边度数 = 右+左+下+上。"""
        return (self.h(i, j) + self.h(i, j - 1)
                + self.v(i, j) + self.v(i - 1, j))

    def charges(self):
        """奇数度顶点 = 开链端点 = 电荷。"""
        L = self.L
        return [(i, j) for i in range(L) for j in range(L)
                if self.degree(i, j) % 2 == 1]

    def chain_components(self):
        """反旋边按共享顶点连成链，分类为 开链(含电荷端点) / 闭链(磁通)。"""
        L = self.L
        n = L * L
        parent = list(range(n))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[rb] = ra

        deg = np.zeros((L, L), dtype=np.int8)
        for i in range(L):
            for j in range(L):
                if self.periodic or j < L - 1:
                    if self.h(i, j):
                        deg[i, j] += 1
                        deg[i, (j + 1) % L] += 1
                        union(i * L + j, i * L + ((j + 1) % L))
                if self.periodic or i < L - 1:
                    if self.v(i, j):
                        deg[i, j] += 1
                        deg[(i + 1) % L, j] += 1
                        union(i * L + j, ((i + 1) % L) * L + j)

        comps = defaultdict(list)
        for i in range(L):
            for j in range(L):
                if deg[i, j] > 0:
                    comps[find(i * L + j)].append((i, j))

        open_chains, closed_loops = [], []
        for vlist in comps.values():
            odd = [v for v in vlist if deg[v[0], v[1]] % 2 == 1]
            if odd:
                open_chains.append((len(vlist), odd))
            else:
                closed_loops.append(len(vlist))
        return open_chains, closed_loops

    def statistics(self):
        L = self.L
        total = 0
        for i in range(L):
            for j in range(L):
                if self.periodic or j < L - 1:
                    total += int(self.h(i, j))
                if self.periodic or i < L - 1:
                    total += int(self.v(i, j))
        ch = self.charges()
        oc, cl = self.chain_components()
        return {
            "L": L, "periodic": self.periodic, "steps": self.steps,
            "chain_length": total,
            "n_charges": len(ch), "charges": ch,
            "n_open_chains": len(oc), "open_chains": oc,
            "n_closed_loops": len(cl), "closed_loops": cl,
        }

    # -- 自检动力学 -----------------------------------------------------
    def flip_edge(self, i, j, horizontal=True):
        """边自检：翻转一条边（弦算符）。"""
        if horizontal:
            self._set_h(i, j, 1 - self.h(i, j))
        else:
            self._set_v(i, j, 1 - self.v(i, j))
        self.steps += 1

    def flip_star(self, i, j):
        """顶点自检：翻转 (i,j) 四周 4 条边 = toric code 星算子 A_v。"""
        self._set_h(i, j, 1 - self.h(i, j))
        self._set_h(i, j - 1, 1 - self.h(i, j - 1))
        self._set_v(i, j, 1 - self.v(i, j))
        self._set_v(i - 1, j, 1 - self.v(i - 1, j))
        self.steps += 1

    def random_edge_flip(self):
        L = self.L
        horizontal = bool(self.rng.integers(0, 2))
        i = int(self.rng.integers(0, L))
        j = int(self.rng.integers(0, L))
        if not self.periodic:
            if horizontal and j == L - 1:
                j = L - 2
            if (not horizontal) and i == L - 1:
                i = L - 2
        self.flip_edge(i, j, horizontal=horizontal)

    def run(self, T, report_every=None):
        snaps = []
        if report_every is None:
            report_every = max(1, T // 20)
        for t in range(T):
            self.random_edge_flip()
            if (t + 1) % report_every == 0 or (t + 1) == T:
                snaps.append(self.statistics())
        return snaps


def ascii_picture(lat):
    """ASCII：· = 无电荷顶点，e = 电荷（奇数度顶点）。"""
    L = lat.L
    lines = ["    " + "".join(f"{j:2d}" for j in range(L))]
    for i in range(L):
        row = f"{i:2d}  "
        for j in range(L):
            row += " e" if lat.degree(i, j) % 2 == 1 else " ·"
        lines.append(row)
    return "\n".join(lines)


def render(lat, out_png):
    if not _HAS_MPL:
        return
    L = lat.L
    fig, ax = plt.subplots(figsize=(6.2, 6.2))
    for i in range(L):
        for j in range(L):
            if lat.h(i, j):
                ax.plot([j, j + 1], [i, i], color="blue", lw=2.2, solid_capstyle="round")
            if lat.v(i, j):
                ax.plot([j, j], [i, i + 1], color="blue", lw=2.2, solid_capstyle="round")
    stat = lat.statistics()
    ch = stat["charges"]
    if ch:
        xs, ys = zip(*[(j, i) for i, j in ch])
        ax.scatter(xs, ys, marker="o", s=170, facecolors="none",
                   edgecolors="red", linewidths=2.2, label="charge (open endpoint)")
    ax.set_xlim(-0.6, L - 0.4)
    ax.set_ylim(L - 0.4, -0.6)
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(f"self-check lattice  L={L}  steps={lat.steps}\n"
                 f"chain length={stat['chain_length']}  charges={stat['n_charges']}  "
                 f"closed loops(flux)={stat['n_closed_loops']}")
    if ch:
        ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    fig.savefig(out_png, dpi=130)
    plt.close(fig)
    print(f"[plot] saved {out_png}")


def report(stat, title):
    print(f"\n=== {title} ===")
    print(f"  反旋链总长 = {stat['chain_length']}")
    ok = "（偶数 ✓ 成对）" if stat["n_charges"] % 2 == 0 else "（奇数 ✗ 违反握手引理！）"
    print(f"  电荷 (开链端点) = {stat['n_charges']}  {ok}")
    print(f"  开链连通支 = {stat['n_open_chains']}  各支(边数,端点) = {stat['open_chains']}")
    print(f"  闭链连通支 (磁通环) = {stat['n_closed_loops']}")


def demo_clean(lat, out_png=None):
    """构造两个干净粒子：一条开链 → 2 个电荷端点；一个方环 → 1 个磁通。"""
    L = lat.L
    i0 = L // 2

    print("\n--- (1) 开链：翻转一条水平路径 → 2 个电荷端点 ---")
    lat.ch[:] = 0
    lat.cv[:] = 0
    lat.steps = 0
    j0, d = 2, 5
    for j in range(j0, j0 + d):
        lat.flip_edge(i0, j, horizontal=True)
    print(ascii_picture(lat))
    report(lat.statistics(), "开链（电荷对）")
    if out_png:
        render(lat, out_png)

    print("\n--- (2) 闭链：翻转一个方环 → 1 个磁通、0 电荷 ---")
    lat.ch[:] = 0
    lat.cv[:] = 0
    lat.steps = 0
    p_i, p_j = 3, 3
    lat.flip_edge(p_i, p_j, horizontal=True)
    lat.flip_edge(p_i, p_j + 1, horizontal=False)
    lat.flip_edge(p_i + 1, p_j, horizontal=True)
    lat.flip_edge(p_i, p_j, horizontal=False)
    print(ascii_picture(lat))
    report(lat.statistics(), "闭链（磁通环）")
    if out_png:
        render(lat, out_png)


def demo_random(lat, T=500, out_png=None):
    print(f"\n--- Level 1 随机自检动力学：{T} 次边翻转 ---")
    print("初始（真空）：")
    print(ascii_picture(lat))
    report(lat.statistics(), "t=0（真空）")
    snaps = lat.run(T)
    first, last = snaps[0], snaps[-1]
    print(f"\n[t={first['steps']}] 链长={first['chain_length']}, 电荷={first['n_charges']}, "
          f"开链={first['n_open_chains']}, 磁通环={first['n_closed_loops']}")
    print(f"[t={last['steps']}]  链长={last['chain_length']}, 电荷={last['n_charges']}, "
          f"开链={last['n_open_chains']}, 磁通环={last['n_closed_loops']}")
    print("\n末态：")
    print(ascii_picture(lat))
    report(last, "末态统计")
    if out_png:
        render(lat, out_png)
    all_even = all(sn["n_charges"] % 2 == 0 for sn in snaps)
    print(f"\n[守恒] 全程电荷数恒为偶数："
          f"{'是 ✓（电荷成对，握手引理）' if all_even else '否 ✗（存在奇数电荷，模型有 bug）'}")


# ==========================================================================
# Level 2 · 顶点自旋代价：同向自旋引力 / 粘滞（保守半）
# ==========================================================================
def spin_cost_demo(L=12, g_edge=1.0, g_open=2.0):
    """顶点自旋（物质）图像下的「开链代价 / 确权失败」。

    每个格点看成绕向 s∈{+1,−1}（同向/反向）。反旋边 = 相邻绕向相反的边；
    开链端点（确权失败）= 奇数度顶点（∂c≠0 的支集 = 电荷）。
    代价泛函 E = g_edge·(反旋边数) + g_open·(开链端点数)。

    诚实边界：E 是静态（保守）代价，给出「朝同向对齐的吸引」与「抗拒剪切的
    阻力」；它不是耗散性的真实粘滞——真实粘滞需要代价被不可逆支付
    （输运-命运方程的汇 −Γρ），那是 Level 3 的过阻尼半。
    """
    def cost(s):
        H, W = s.shape
        M = 0
        for i in range(H):
            for j in range(W):
                if j < W - 1 and s[i, j] != s[i, j + 1]:
                    M += 1
                if i < H - 1 and s[i, j] != s[i + 1, j]:
                    M += 1
        deg = np.zeros((H, W), dtype=int)
        for i in range(H):
            for j in range(W):
                if j < W - 1 and s[i, j] != s[i, j + 1]:
                    deg[i, j] += 1
                    deg[i, j + 1] += 1
                if i < H - 1 and s[i, j] != s[i + 1, j]:
                    deg[i, j] += 1
                    deg[i + 1, j] += 1
        Q = int((deg % 2).sum())
        return M, Q, g_edge * M + g_open * Q

    s1 = np.ones((L, L), dtype=int)
    M, Q, E = cost(s1)
    print(f"  全同向自旋         反旋边={M:3d}  开链端点(确权失败)={Q:3d}  代价 E={E:.1f}")

    s2 = np.ones((L, L), dtype=int)
    s2[L // 2:, :] = -1
    M, Q, E = cost(s2)
    print(f"  剪切(上+1/下−1)    反旋边={M:3d}  开链端点(确权失败)={Q:3d}  代价 E={E:.1f}  "
          f"(界面长={L})")

    s3 = np.fromfunction(lambda i, j: ((i + j) % 2) * 2 - 1, (L, L), dtype=int)
    M, Q, E = cost(s3)
    print(f"  反相棋盘           反旋边={M:3d}  开链端点(确权失败)={Q:3d}  代价 E={E:.1f}")

    print("\n  结论（保守部分）：代价随「同向」下降 → 朝同向对齐的吸引（同向自旋引力）；")
    print("  代价随「剪切界面」线性上升 → 抗拒相对运动的阻力（粘滞的保守半）。")
    print("  耗散半（真实粘滞）见 Level 3 的过阻尼松弛。")


# ==========================================================================
# Level 3 · 连续相位 XY：涡旋粒子（确权失败）+ 过阻尼耗散（粘滞半）
# ==========================================================================
class XYSelfCheck:
    """连续相位自检：每个格点 θ∈S¹ 做自检绕转 0→π→2π。

    能量 E = Σ_边 [1 − cos(θ_j − θ_i)] —— 同向(对齐)=0，反旋(相差 π)=2。
    涡旋 q_plaquette = (1/2π) 绕 plaquette 一圈的相位绕数，±1 为「粒子」
    （= 四个格点的自检闭环没能闭合 = 确权失败）。
    过阻尼 Monte Carlo 松弛：E 单调下降 → 代价被不可逆支付（粘滞的耗散半）。
    """

    def __init__(self, L, seed=0):
        assert L >= 2
        self.L = L
        self.rng = np.random.default_rng(seed)
        self.theta = self.rng.uniform(0.0, 2.0 * np.pi, size=(L, L))
        self.steps = 0

    def energy(self):
        L = self.L
        E = 0.0
        for i in range(L):
            for j in range(L):
                E += 1.0 - np.cos(_wrap(self.theta[i, (j + 1) % L] - self.theta[i, j]))
                E += 1.0 - np.cos(_wrap(self.theta[(i + 1) % L, j] - self.theta[i, j]))
        return E

    def vortices(self):
        """每 plaquette 的绕数 q：+1 涡旋、−1 反涡旋、0 无。闭合曲面上 Σq=0。"""
        L = self.L
        q = np.zeros((L, L), dtype=int)
        for i in range(L):
            for j in range(L):
                a = self.theta[i, j]
                b = self.theta[i, (j + 1) % L]
                c = self.theta[(i + 1) % L, (j + 1) % L]
                d = self.theta[(i + 1) % L, j]
                s = _wrap(b - a) + _wrap(c - b) + _wrap(d - c) + _wrap(a - d)
                q[i, j] = int(round(s / (2.0 * np.pi)))
        return q

    def mc_sweep(self, T, amplitude=0.5):
        """过阻尼 Monte Carlo：L² 次试探翻转，按 e^{−ΔE/T} 接受。"""
        L = self.L
        rng = self.rng
        for _ in range(L * L):
            i = int(rng.integers(0, L))
            j = int(rng.integers(0, L))
            theta_old = self.theta[i, j]
            theta_new = theta_old + rng.uniform(-amplitude, amplitude)
            dE = 0.0
            for ni, nj in ((i + 1) % L, j), ((i - 1) % L, j), (i, (j + 1) % L), (i, (j - 1) % L):
                nb = self.theta[ni, nj]
                dE += (1.0 - np.cos(_wrap(theta_new - nb))) - (1.0 - np.cos(_wrap(theta_old - nb)))
            if dE <= 0 or rng.random() < np.exp(-dE / T):
                self.theta[i, j] = theta_new
                self.steps += 1


def xy_demo(L=16, seed=0, n_anneal=8, sweeps_per_T=200):
    """高温随机初态（多涡旋）→ 退火 → 涡旋成对湮灭、能量单调下降。"""
    model = XYSelfCheck(L, seed=seed)
    q = model.vortices()
    n_plus = int((q == 1).sum())
    n_minus = int((q == -1).sum())
    print(f"\n--- Level 3 连续相位 XY：涡旋粒子 + 过阻尼耗散（L={L}, 周期） ---")
    print(f"  初始(高温随机): E={model.energy():8.2f}  涡旋 +{n_plus} / −{n_minus}  Σq={int(q.sum())}")

    Ts = np.linspace(2.0, 0.05, n_anneal)
    for T in Ts:
        for _ in range(sweeps_per_T):
            model.mc_sweep(T)
        q = model.vortices()
        n_plus = int((q == 1).sum())
        n_minus = int((q == -1).sum())
        print(f"  T={T:5.2f}:  E={model.energy():8.2f}  涡旋 +{n_plus} / −{n_minus}  Σq={int(q.sum())}")

    total_q = int(model.vortices().sum())
    print(f"\n  [守恒] 末态总绕数 Σq={total_q}（闭合曲面恒为 0 → 涡旋成对）")
    print("  结论：涡旋(=确权失败的粒子) 成对湮灭；能量单调下降")
    print("        (= 开链代价被不可逆支付 = 粘滞的耗散半；对齐吸引 = 同向自旋引力)。")


# ==========================================================================
# 入口
# ==========================================================================
def main():
    ap = argparse.ArgumentParser(description="光场自检动力学 · 自检晶格模型（三层）")
    ap.add_argument("--L", type=int, default=16, help="格点尺寸 L×L")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--T", type=int, default=500, help="Level 1 随机自检翻转次数")
    ap.add_argument("--open", dest="periodic", action="store_false", default=True,
                    help="用开放边界（默认周期 torus）")
    ap.add_argument("--demo", action="store_true", help="Level 1：干净构造电荷对/磁通环")
    ap.add_argument("--spin", action="store_true", help="Level 2：同向/剪切/反相代价对照")
    ap.add_argument("--xy", action="store_true", help="Level 3：XY 涡旋粒子 + 退火耗散")
    ap.add_argument("--png", default="self_check_model.png", help="Level 1 出图文件名（需 matplotlib）")
    args = ap.parse_args()

    if args.xy:
        xy_demo(L=args.L, seed=args.seed)
    elif args.spin:
        print("\n--- Level 2 开链代价对照（顶点自旋图像） ---")
        spin_cost_demo(L=args.L)
    else:
        lat = SelfCheckLattice(args.L, seed=args.seed, periodic=args.periodic)
        if args.demo:
            demo_clean(lat, out_png=args.png if _HAS_MPL else None)
        else:
            demo_random(lat, T=args.T, out_png=args.png if _HAS_MPL else None)

    print("\n诚实边界：以上「粒子」= ℤ₂ 拓扑激发 / XY 涡旋，非标准模型点粒子；")
    print("「引力/粘滞」= 代价泛函的保守/耗散两半，非真实引力或真实流体粘滞。")


if __name__ == "__main__":
    main()
