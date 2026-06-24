import pandas as pd
import os

# ======================
# 璺緞璁剧疆
# ======================
structure_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/gnn/graph_tp_tda/data_prepare"))
dataset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/experimental/77K_for_wt_cal.csv"))
output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/experimental/dataset_with_wt.csv"))

# ======================
# 鍘熷瓙璐ㄩ噺 (g/mol)
# ======================
M_C = 12.011
M_H = 1.008
M_H2 = 2.016

# ======================
# 璇诲彇鏁版嵁闆?
# ======================
df = pd.read_csv(dataset_path)

# ======================
# 缂撳瓨缁撴瀯璐ㄩ噺锛堥伩鍏嶉噸澶嶈鍙栵級
# ======================
mass_cache = {}

def get_structure_mass(file_id):
    if file_id in mass_cache:
        return mass_cache[file_id]

    file_path = os.path.join(structure_folder, f"{file_id}.csv")

    structure = pd.read_csv(file_path)

    # 缁熻鍏冪礌鏁伴噺
    n_C = (structure['Element'] == 'C').sum()
    n_H = (structure['Element'] == 'H').sum()

    # 鍩哄簳璐ㄩ噺
    m_sub = n_C * M_C + n_H * M_H

    # 榛樿锛氬惛闄勪綅鐐?= C鍘熷瓙鏁?
    n_site = n_C

    mass_cache[file_id] = (m_sub, n_site)
    return m_sub, n_site

# ======================
# 璁＄畻 wt%
# ======================
wt_list = []

for _, row in df.iterrows():
    file_id = int(row['File ID'])
    theta = row['theta']

    m_sub, n_site = get_structure_mass(file_id)

    # 鍚搁檮H2鏁?
    n_H2 = theta * n_site

    # H2璐ㄩ噺
    m_H2 = n_H2 * M_H2

    # wt%
    wt_percent = (m_H2 / (m_sub + m_H2)) * 100 if (m_sub + m_H2) > 0 else 0

    wt_list.append(wt_percent)

# 娣诲姞鍒?
df['wt%'] = wt_list

# ======================
# 淇濆瓨
# ======================
df.to_csv(output_path, index=False)

print("鉁?宸茬敓鎴愭柊鏂囦欢:", output_path)
