import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# ======================
# 1. 璇诲彇鏁版嵁
# ======================
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/experimental/dataset_with_wt.csv"))
df = pd.read_csv(file_path)

# 鎸?File ID 鍜?Pressure 鎺掑簭锛岀‘淇濇姌绾夸笉浼氫贡
df = df.sort_values(by=["File ID", "Pressure (bar)"])

# 鑾峰彇鎵€鏈夊敮涓€鐨?File ID
unique_ids = df["File ID"].unique()
num_lines = len(unique_ids)  # 搴旇鏄?44

# ======================
# 2. 绉戠爺璁烘枃鏍煎紡閰嶇疆 (Matplotlib Style)
# ======================
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "Liberation Sans"]
plt.rcParams["axes.edgecolor"] = "black"
plt.rcParams["axes.linewidth"] = 1.2
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"
plt.rcParams["xtick.major.size"] = 5
plt.rcParams["ytick.major.size"] = 5

# 鍒涘缓鐢诲竷 (瀹?8.5 鑻卞锛岄珮 6 鑻卞锛岀暀鍑哄彸渚х粰鍥句緥)
fig, ax = plt.subplots(figsize=(8.5, 6), dpi=300)

# ======================
# 3. 棰滆壊涓?Marker 鍑嗗
# ======================
# 浣跨敤 "turbo" 娓愬彉鑹茬洏锛?4鏉＄嚎鑳藉舰鎴愭紓浜殑棰滆壊杩囨浮
colors = sns.color_palette("turbo", num_lines)

# 澶囬€夌殑 Marker 鍒楄〃锛屽惊鐜娇鐢?
all_markers = [
    "o",
    "s",
    "^",
    "v",
    "D",
    "<",
    ">",
    "p",
    "*",
    "h",
    "H",
    "X",
    "d",
    "P",
]  # P 浠ｈ〃瀹炲績鍔犲彿锛屾浛浠ｄ簡鍘熸潵鐨勫ぇ鍐?O
markers = [all_markers[i % len(all_markers)] for i in range(num_lines)]

# ======================
# 4. 寰幆缁樺埗 44 鏉℃姌绾?
# ======================
for i, file_id in enumerate(unique_ids):
    sub_df = df[df["File ID"] == file_id]

    ax.plot(
        sub_df["Pressure (bar)"],
        sub_df["wt%"],
        label=f"ID: {file_id}",
        color=colors[i],
        marker=markers[i],
        markersize=5,
        markerfacecolor="none",  # 绌哄績 marker锛屾洿鍏风鎶€鎰?
        markeredgewidth=1.0,
        linewidth=1.2,
        alpha=0.85,
    )

# ======================
# 5. 鍧愭爣杞存爣绛句笌鑼冨洿
# ======================
ax.set_xlabel("Pressure (bar)", fontsize=12, fontweight="bold", labelpad=8)
ax.set_ylabel(
    r"Adsorption Capacity wt%)",
    fontsize=12,
    fontweight="bold",
    labelpad=8,
)

# 鑷姩缇庡寲鍒诲害鑼冨洿
ax.set_xlim(left=0)
ax.set_ylim(bottom=0)
ax.tick_params(axis="both", labelsize=10)

# ======================
# 6. 鍗曠嫭鐨勬俯搴︽枃鏈 (T=77K)
# ======================
# 浣跨敤 text 鏀剧疆鍦ㄥ乏涓婅锛宖rameon=True 甯﹁竟妗?
props = dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="gray", alpha=0.8)
ax.text(
    0.05,
    0.95,
    "T = 77 K",
    transform=ax.transAxes,
    fontsize=11,
    fontweight="bold",
    verticalalignment="top",
    bbox=props,
)

# ======================
# 7. 绱у噾鍨?44 鏉＄嚎鍥句緥璁剧疆 (鏀惧湪鍥惧鍙充晶)
# ======================
# ncol=3 琛ㄧず鍥句緥鍒?鍒楁樉绀猴紝handletextpad 鎺у埗鍥捐〃鍜屾枃瀛楄窛绂伙紝columnspacing 鎺у埗鍒楄窛
legend = ax.legend(
    bbox_to_anchor=(1.02, 1),
    loc="upper left",
    borderaxespad=0,
    ncol=3,
    fontsize=8,
    title="Structure ID",
    title_fontsize=9,
    frameon=True,
    edgecolor="black",
    handletextpad=0.4,
    columnspacing=0.8,
)
legend.get_frame().set_linewidth(0.8)

# ======================
# 8. 璋冩暣甯冨眬骞朵繚瀛?
# ======================
plt.tight_layout()

# 淇濆瓨涓虹鐮斿父鐢ㄧ殑 TIFF 鎴?PDF 鏍煎紡
output_img = os.path.join(os.path.dirname(file_path), "wt.png")
plt.savefig(output_img, bbox_inches="tight", dpi=300)
plt.show()

print(f"馃搳 缁樺浘瀹屾垚锛佸浘鐗囧凡淇濆瓨鑷? {output_img}")
