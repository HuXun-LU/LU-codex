# 光场自检动力学的范畴化 III

### ——D(S₃) 非阿贝尔检验：字典精化与粗不变量的局限

**作者：** 胡勋
**日期：** 2026 年 10 月
**版本：** 范畴化纲领第三阶段（检验篇）

> 本文件检验范畴化 I、II 建立的字典在**第一个非阿贝尔 MTC** 上的普适性。结论分两半：字典的推广**成立**（并因此被精化）；粗不变量 $\Delta_{\mathrm{closed}},\Delta_{\mathrm{open}}$ 的局限**被暴露**。文中所有模数据均为精确手算，可独立核对。

---

## 摘要

用量子二重 $\mathcal D(S_3)=\mathcal Z(\mathrm{Vec}_{S_3})$（秩 8，第一个非阿贝尔例子）检验框架的两条核心主张：(i)「闭链 = 玻色子」的识别；(ii) 闭链密度差不变量 $\Delta_{\mathrm{closed}}=2\log\mathbf d(A)$。结果：

1. **字典精化。** $\mathcal D(S_3)$ 有 **5 个玻色子**（$\theta=1$），其中包含全部 3 个电荷。故「闭链 = 玻色子」**不足以**划出磁通 sector。正确字典为：**开链（电荷）$=(e,\rho)$**（平凡共轭类 + 任意表示），**闭链（磁通）$=(C,\mathbf 1)$**（任意共轭类 + 平凡中心化子表示）。纯磁通 $\{(e,\mathbf 1),((12),\mathbf 1),((123),\mathbf 1)\}$ 构成**磁 Lagrangian 代数** $A_m$，$\mathbf d(A_m)=1+3+2=6$；纯电荷构成**电 Lagrangian 代数** $A_e$，$\mathbf d(A_e)=1+1+4=6$。
2. **不变量公式存活。** 两种凝聚都满足 $D^2(\mathcal C)=D^2(\mathrm{Vec})\cdot\mathbf d(A)^2$，即 $\Delta_{\mathrm{closed}}=2\log 6=\log 36$。公式在非阿贝尔情形**成立**。
3. **粗不变量的局限（实质发现）。** $\mathbf d(A_e)=\mathbf d(A_m)=6$，故 $\Delta_{\mathrm{closed}}$ 与 $\Delta_{\mathrm{open}}$ 对电/磁凝聚取**同一值**——总量子维数不变量**盲于开闭之别**。开/闭的区分完全由「选择哪个 Lagrangian 代数（荷还是流）」承载，这是粗模数据抓不住的信息。

**关键词：** 量子二重；D(S₃)；任意子凝聚；Lagrangian 代数；玻色子；拓扑自旋；总量子维数

---

## 1 目的与背景

范畴化 I、II 在 toric code（$D(\mathbb Z_2)$）上建立了字典，并证得 $\Delta_{\mathrm{closed}}=2\log\mathbf d(A)$。但 toric code 是阿贝尔的「hello world」：那里所有量子维数都是 $1$，电/磁/双子完全对称，任何识别都不会被真正考验。本文件用**第一个非阿贝尔 MTC**——量子二重 $\mathcal D(S_3)$（Dijkgraaf–Witten 理论，平凡 3-余循环）——做检验。它比 toric code 难一档，但仍可完整手算。

## 2 $\mathcal D(S_3)$ 的模数据

$S_3=\{e,(12),(13),(23),(123),(132)\}$。共轭类：$\{e\}$（大小 1）、转置类 $\{(12),(13),(23)\}$（大小 3）、三元轮换类 $\{(123),(132)\}$（大小 2）。中心化子：$Z(e)=S_3$，$Z((12))=\{e,(12)\}\cong\mathbb Z_2$，$Z((123))=\langle(123)\rangle\cong\mathbb Z_3$。

$\mathcal D(S_3)=\mathcal Z(\mathrm{Vec}_{S_3})$ 的简单对象是配对 $(C,\rho)$，其中 $C$ 是共轭类、$\rho$ 是中心化子的不可约表示。共 $3+2+3=8$ 个：

| 对象 | 量子维数 $\mathbf d$ | 拓扑自旋 $\theta$ | 类型 |
|---|---|---|---|
| $(e,\mathbf 1)$ | 1 | 1 | 真空 |
| $(e,\varepsilon)$ | 1 | 1 | 电荷（符号表示）|
| $(e,V)$ | 2 | 1 | 电荷（2 维标准表示）|
| $((12),\mathbf 1)$ | 3 | 1 | **纯磁通** |
| $((12),-)$ | 3 | $-1$ | 费米子（双子）|
| $((123),\mathbf 1)$ | 2 | 1 | **纯磁通** |
| $((123),\omega)$ | 2 | $e^{2\pi i/3}$ | 双子 |
| $((123),\omega^2)$ | 2 | $e^{4\pi i/3}$ | 双子 |

其中 $\omega=e^{2\pi i/3}$，$\mathbf d(C,\rho)=|C|\cdot\dim\rho$，拓扑自旋 $\theta_{(C,\rho)}=\rho(x)$ 为标量（$x$ 为 $C$ 的代表元，$\rho(x)$ 在 $\rho$ 上为标量）。总量子维数

$$D^2=1+1+4+9+9+4+4+4=36,\qquad D=6=|S_3|.$$

## 3 玻色子与 荷/流 分解

**玻色子**（$\theta=1$）共 **5 个**：$(e,\mathbf 1),(e,\varepsilon),(e,V),((12),\mathbf 1),((123),\mathbf 1)$。这立刻给出第一个结论：

> **观察 3.1（「闭链 = 玻色子」在非阿贝尔情形失效）。** 全部 3 个电荷都是玻色子，故「玻色子」这一条件无法把磁通（闭链）从电荷（开链）中分离出来。事实上即使在 toric code 里，$e$（电荷）与 $m$（磁通）也都满足 $\theta=1$，只是那里两者的量子维数都是 $1$、对称性掩盖了问题。

**正确的分解**是（这恰是范畴化 I、II 中实际使用、但被 toric code 掩盖的字典）：

- **开链（电荷/端点）** $=$ 平凡共轭类的对象：$\{(e,\mathbf 1),(e,\varepsilon),(e,V)\}\cong\mathrm{Rep}(S_3)$；
- **闭链（磁通/环）** $=$ 平凡中心化子表示的对象：$\{(e,\mathbf 1),((12),\mathbf 1),((123),\mathbf 1)\}$；
- **双子** $=$ 非平凡类配非平凡中心化子表示：$\{((12),-),((123),\omega),((123),\omega^2)\}$。

> **精化（对框架词典的非阿贝尔修正）。** 「闭链」应精化为 **纯磁通 $(C,\mathbf 1)$**（平凡中心化子表示），而非「玻色子」。这个精化在阿贝尔 $D(\mathbb Z_2)$ 中不可见，在 $D(S_3)$ 中被强制显形。

## 4 两个 Lagrangian 代数与凝聚检验

**电 Lagrangian 代数**（凝聚全部电荷）：

$$A_e=(\mathbf 1\ \text{分量})=(e,\mathbf 1)\oplus(e,\varepsilon)\oplus 2\,(e,V),\qquad \mathbf d(A_e)=1+1+2\cdot2=6.$$

**磁 Lagrangian 代数**（凝聚全部纯磁通）：

$$A_m=(e,\mathbf 1)\oplus((12),\mathbf 1)\oplus((123),\mathbf 1),\qquad \mathbf d(A_m)=1+3+2=6.$$

两者都是 **Lagrangian**：$\mathbf d(A)^2=36=D^2$（这是 $D(G)$ 的标准事实：电边界对应 $H=\{e\}$，磁边界对应 $H=G$；见 Kitaev–Kong 2012、Davydov）。凝聚任一 Lagrangian 代数都给出平凡理论 $\mathrm{Vec}$（秩 1）。

**不变量公式检验。** 由范畴化 II 的定理 B 严格版，

$$D^2\bigl(\mathcal D(S_3)\bigr)=D^2\bigl(\mathcal D(S_3)_A^{\mathrm{loc}}\bigr)\cdot\mathbf d(A)^2.$$

对 $A=A_m$（或 $A_e$）：$D^2(\mathrm{Vec})=1$，$\mathbf d(A)^2=36$，故 $36=1\cdot36$ 成立，即

$$\Delta_{\mathrm{closed}}=2\log\mathbf d(A_m)=2\log 6=\log 36.$$

**公式在非阿贝尔情形存活。** 范畴化 II 的 $\Delta_{\mathrm{closed}}=2\log\mathbf d(A)$ 首次在秩 8、非阿贝尔、量子维数非全 1 的例子上被验证。

## 5 核心结论：粗不变量的局限

这里出现本检验最有价值的发现：

> **定理 5.1（粗不变量的开闭盲区）。** 在 $\mathcal D(S_3)$ 中，$\mathbf d(A_e)=\mathbf d(A_m)=6$。因此
> $$\Delta_{\mathrm{closed}}(A_e)=\Delta_{\mathrm{closed}}(A_m)=2\log 6,$$
> 且（承范畴化 II 命题 C）电、磁两条边界都是 rank-1 平凡边界，故
> $$\Delta_{\mathrm{open}}(A_e)=\Delta_{\mathrm{open}}(A_m)=\mathrm{rank}(\mathcal C_{\mathcal C})-\mathrm{rank}(\mathrm{Mod}_{\mathcal C}(A))=8-1=7.$$
> 也就是说，**总量子维数不变量 $\Delta_{\mathrm{closed}}$ 与模秩不变量 $\Delta_{\mathrm{open}}$ 都不能区分电（开）凝聚与磁（闭）凝聚**。

*证明。* $\mathbf d(A_e)=\mathbf d(A_m)=6$ 已由 §4 给出；$\Delta_{\mathrm{closed}}=2\log\mathbf d(A)$ 由范畴化 II 定理 19.1 给出，故二者相等。两条边界 rank 均为 1 是 Lagrangian 凝聚的标准事实（§4）。∎

**这意味着什么。** 范畴化 II 的定理 D 断言「闭链密度差 = 代数 $A$ 的不变量、开链密度差的符号由模的 $A$-诱导分解决定」。$\mathcal D(S_3)$ 表明：**这些不变量是「电/磁对称」的**——它们测量的是「是否发生了凝聚、凝聚了多少」，而**不是**「凝聚的是荷还是流」。开与闭的区分完全落在「选择哪个 Lagrangian 代数」这一**群论来源**上（荷 = 平凡类、流 = 平凡中心化子表示），这一区分**不可由粗模数据（$S,T$、秩、总量子维数）复原**。

这正是框架诚实性约束的兑现：开/闭之别是**翻译选择**（证明者的词典），不是 MTC 模数据自动输出的分类结论。任何声称「闭链密度差自动区分开闭」的强版本定理 D，在 $\mathcal D(S_3)$ 上为假。

## 6 尖锐猜想与遗留问题

**猜想 6.1（$D(G)$ 的字典精化，可证）。** 对任意有限群 $G$，框架字典精化为：
$$\text{开链（电荷）}\longleftrightarrow\{(e,\rho):\rho\in\operatorname{Irr}(G)\},\qquad
\text{闭链（磁通）}\longleftrightarrow\{(C,\mathbf 1):C\text{ 共轭类}\},$$
且两者分别生成电、磁 Lagrangian 代数，$\mathbf d(A_e)=\mathbf d(A_m)=|G|=D$，凝聚后均为 $\mathrm{Vec}$，$\Delta_{\mathrm{closed}}=2\log|G|$。这是 $D(G)$ 边界分类的标准结论（Kitaev–Kong 2012、Davydov、Ostrik），此处作为框架字典的精确化陈述。

**猜想 6.2（本征刻画，开放）。** 是否存在一个**只用 $(S,T)$ 模数据**（不引用群）的判据，把一般 MTC 的「荷类 sector」与「流类 sector」区分开？$\mathcal D(S_3)$ 的 Galois 群是 $\mathrm{Gal}(\mathbb Q(\zeta_6)/\mathbb Q)\cong\mathbb Z_2$（conductor 6），其非平凡作用仅交换 $\omega\leftrightarrow\omega^2$，**太粗**而无法区分荷/流（荷、流、费米子全部被固定）。故 Galois 路径在 $D(S_3)$ 上**不足以**给出本征刻画——这是一个诚实的负结果，把问题留为开放。

**猜想 6.3（强版定理 D 的证伪范围）。** 是否存在 MTC，其中电、磁凝聚的 $\mathbf d(A)$ 不同（从而 $\Delta_{\mathrm{closed}}$ 确实区分开闭）？在阿贝尔 $D(G)$ 中 $\mathbf d(A_e)=\mathbf d(A_m)=|G|$ 恒等；非阿贝尔 $D(S_3)$ 亦然。寻找第一个「$\mathbf d(A_{\text{electric}})\neq\mathbf d(A_{\text{magnetic}})$」的 MTC，是检验定理 D 强版真实效力的下一步。

**遗留问题（承 §22）：** (i) 验证猜想 6.1 的严格版本（需核对 $D(G)$ 磁代数的凝聚细节）；(ii) 在 Ising、$\mathrm{SU}(2)_k$、Fibonacci 上检验猜想 6.2、6.3；(iii) 若猜想 6.3 无例，则「开闭之别不可由粗不变量承载」成为框架的一条**结构性结论**，应升格为正式定理。

---

## 参考文献

1. A. Yu. Kitaev, *Fault-tolerant quantum computation by anyons*, Ann. Physics **303** (2003), 2–30.
2. A. Kitaev, L. Kong, *Models for gapped boundaries and domain walls*, Comm. Math. Phys. **313** (2012), 351–373.
3. L. Kong, *Anyon condensation and tensor categories*, Nucl. Phys. B **886** (2014), 436–482.
4. F. A. Bais, J. K. Slingerland, *Condensate-induced transitions between topologically ordered phases*, Phys. Rev. B **79** (2009), 045316.
5. A. Davydov, *Modular invariants for group-theoretical modular data I*, J. Algebra **323** (2010), 1321–1348.
6. V. Ostrik, *Module categories, weak Hopf algebras and modular invariants*, Transform. Groups **8** (2003), 177–206.
7. P. Etingof, D. Nikshych, V. Ostrik, *On fusion categories*, Ann. of Math. (2) **162** (2005), 581–642.

---

**声明：** 本文是《逻辑宇宙》（LU-Codex v1.0，公共领域 CC0）范畴化纲领的第三阶段（检验篇）。§2–§4 的模数据为精确手算，可独立核对；猜想 6.1 为已知结果的精确化复述，猜想 6.2、6.3 为开放问题。定理 5.1 的证明依赖 $D(G)$ 边界分类的标准结论。

*第三阶段（D(S₃) 检验）终*
