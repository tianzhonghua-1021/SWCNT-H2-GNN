import os
import pandas as pd

# ======================
# 璺緞璁剧疆
# ======================
structure_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/gnn/graph_tp_tda/data_prepare"))
dataset_path = (
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/experimental/for_experimental_data.csv"))
)
output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/experimental/dataset_with_V.csv"))

# ======================
# 鐗╃悊甯搁噺璁剧疆
# ======================
M_C = 12.011
M_H = 1.008
M_H2 = 2.016
V_m = 22414  # STP 涓嬬殑姘斾綋鎽╁皵浣撶Н (cm3/mol)

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
    n_C = (structure["Element"] == "C").sum()
    n_H = (structure["Element"] == "H").sum()

    # 鍩哄簳璐ㄩ噺
    m_sub = n_C * M_C + n_H * M_H

    # 榛樿锛氬惛闄勪綅鐐?= C鍘熷瓙鏁?
    n_site = n_C

    mass_cache[file_id] = (m_sub, n_site)
    return m_sub, n_site


# ======================
# 璁＄畻 V (cm3/g)
# ======================
v_list = []

for _, row in df.iterrows():
    file_id = int(row["File ID"])
    theta = row["theta"]

    m_sub, n_site = get_structure_mass(file_id)

    # 1. 鍚搁檮鐨?H2 鎽╁皵鏁?(mol)
    # 娉ㄦ剰锛氬墠闈㈢殑 m_sub 鍗曚綅鏄?g/mol锛屽叾瀹炰唬琛ㄢ€滄瘡鎽╁皵鍗曡優/缁撴瀯鐨勮川閲忊€?
    # 杩欓噷鐨?n_H2 瀵瑰簲鐨勪篃鏄€滄瘡鎽╁皵鍗曡優鍚搁檮鐨?H2 鎽╁皵鏁扳€?
    n_H2 = theta * n_site

    # 2. H2 鍦?STP 涓嬬殑浣撶Н (cm3)
    v_H2 = n_H2 * V_m

    # 3. 璁＄畻 V (cm3/g) = H2浣撶Н / 鍩哄簳璐ㄩ噺
    # 杩欐牱鍒嗗瓙鍒嗘瘝鍚屾椂绾﹀幓浜嗏€滄瘡鎽╁皵鍗曡優鈥濓紝寰楀埌鐨勫氨鏄櫘閫氱殑 cm3/g
    v_per_g = (v_H2 / m_sub) if m_sub > 0 else 0

    v_list.append(v_per_g)

# 娣诲姞鏂板垪锛岀Щ闄ゆ垨淇濈暀鏃х殑 wt%锛堝彇鍐充簬浣犵殑闇€姹傦級
df["V(cm3/g)"] = v_list

# ======================
# 淇濆瓨
# ======================
df.to_csv(output_path, index=False)

print("鉁?宸茬敓鎴愭柊鏂囦欢:", output_path)

