import streamlit as st
from datetime import datetime, timedelta
import random

# --- 1. 施設データ ---
FACILITIES = {
    "自社ビル": {"cost": 500000000, "id": "f_building", "effect": "家賃無料"},
    "社員研修所": {"cost": 1000000000, "id": "f_training", "effect": "効率+20%"},
    "R&Dセンター": {"cost": 5000000000, "id": "f_rd", "effect": "シェア増"},
    "AIデータセンター": {"cost": 20000000000, "id": "f_data", "effect": "売上+5%"},
    "物流拠点": {"cost": 50000000000, "id": "f_logi", "effect": "コスト減"},
    "海外支社": {"cost": 100000000000, "id": "f_overseas", "effect": "世界進出"},
    "政府交渉窓口": {"cost": 300000000000, "id": "f_gov", "effect": "補助金獲得"},
    "保養所": {"cost": 10000000000, "id": "f_resort", "effect": "離職防止"},
    "サイバー防衛局": {"cost": 500000000000, "id": "f_cyber", "effect": "不祥事防止"},
    "宇宙開発部門": {"cost": 1000000000000, "id": "f_space", "effect": "国家威信UP"},
    "量子計算ラボ": {"cost": 2000000000000, "id": "f_quantum", "effect": "開発爆速"},
    "社員食堂": {"cost": 500000000, "id": "f_cafeteria", "effect": "満足度UP"},
    "自家発電施設": {"cost": 3000000000, "id": "f_power", "effect": "停電耐性"},
    "社内保育園": {"cost": 1000000000, "id": "f_nursery", "effect": "復職率UP"},
    "地下シェルター": {"cost": 1000000000000, "id": "f_shelter", "effect": "災害対策"},
    "特許管理事務所": {"cost": 50000000000, "id": "f_patent", "effect": "不労所得"},
    "巨大展示場": {"cost": 150000000000, "id": "f_expo", "effect": "知名度UP"},
    "社員専用鉄道": {"cost": 800000000000, "id": "f_train", "effect": "遅刻ゼロ"},
    "AI倫理委員会": {"cost": 20000000000, "id": "f_ethics", "effect": "炎上防止"},
    "超高層タワー": {"cost": 5000000000000, "id": "f_tower", "effect": "世界一の象徴"}
}

# --- 2. セッションステート初期化 ---
if 'money' not in st.session_state:
    st.session_state.money = 1970000000 
    st.session_state.debt = 0
    st.session_state.share = 1
    st.session_state.staff = 121
    st.session_state.date = datetime(2052, 4, 3)
    st.session_state.stock_price = 10000
    st.session_state.stock_owned = 0
    st.session_state.is_cleared = False 
    st.session_state.logs = []
    for f in FACILITIES.values():
        st.session_state[f["id"]] = False

def add_log(msg):
    st.session_state.logs.insert(0, f"[{st.session_state.date.strftime('%Y/%m')}] {msg}")
    st.session_state.logs = st.session_state.logs[:10]

# --- 3. 決算処理 ---
def run_settlement(months=1):
    total_income = 0
    total_interest = 0
    res_total = 0
    mid_total = 0
    for _ in range(months):
        st.session_state.date += timedelta(days=30)
        income = int(st.session_state.staff * 600000 * (1 + st.session_state.share / 100))
        interest = int(st.session_state.debt * 0.02)
        st.session_state.money += (income - interest)
        total_income += income
        total_interest += interest
        st.session_state.stock_price = int(st.session_state.stock_price * random.uniform(0.85, 1.15))
        res_rate = 0.04 if not st.session_state.get('f_resort') else 0.01
        res = int(st.session_state.staff * res_rate)
        mid = int(res * 0.5)
        st.session_state.staff = max(0, st.session_state.staff - res + mid)
        res_total += res
        mid_total += mid
    add_log(f"決算完了: 純益 {total_income-total_interest:,}円")

# --- 4. クリア判定・ヘッダー ---
if st.session_state.share >= 100000000 and not st.session_state.is_cleared:
    st.balloons(); st.snow(); st.session_state.is_cleared = True

st.title("🌌 " + ("銀河帝国" if st.session_state.is_cleared else "国家規模経営") + "シミュレーター")

# 【修正箇所1】ヘッダーに保有株数を追加
col1, col2, col3, col4 = st.columns(4)
col1.metric("現預金", f"{st.session_state.money / 100000000:.2f}億円")
col2.metric("借金", f"{st.session_state.debt / 100000000:.2f}億円")
col3.metric("保有株", f"{st.session_state.stock_owned:,}株") # ←追加！
col4.metric("従業員", f"{st.session_state.staff}名")

st.divider()

# --- 5. タブ ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["👤 採用", "💰 金融", "📈 証券", "🤝 M&A", "🏗️ 施設"])

with tab1:
    st.subheader("採用センター")
    unit = 1000000 if st.session_state.is_cleared else 2000000
    c_h1, c_h2 = st.columns(2)
    with c_h1:
        for n in [1, 50]:
            if st.button(f"{n}人採用 ({unit*n/100000000:.2f}億)", key=f"h_{n}"):
                if st.session_state.money >= unit * n:
                    st.session_state.money -= unit * n; st.session_state.staff += n; st.rerun()
    with c_h2:
        for n in [10, 100]:
            if st.button(f"{n}人採用 ({unit*n/100000000:.2f}億)", key=f"h_{n}"):
                if st.session_state.money >= unit * n:
                    st.session_state.money -= unit * n; st.session_state.staff += n; st.rerun()

with tab2:
    if st.button("💵 100億円 融資"):
        st.session_state.money += 10000000000; st.session_state.debt += 10000000000; st.rerun()
    if st.button("🏦 100億円 返済"):
        amt = min(st.session_state.debt, 10000000000)
        if st.session_state.money >= amt:
            st.session_state.money -= amt; st.session_state.debt -= amt; st.rerun()

with tab3:
    # 【修正箇所2】証券タブ内の表示をリッチに
    st.subheader("証券取引")
    total_val = st.session_state.stock_owned * st.session_state.stock_price
    st.info(f"現在の株価: {st.session_state.stock_price:,}円 / 保有数: {st.session_state.stock_owned:,}株 (時価総額: {total_val:,}円)")
    
    c_s1, c_s2 = st.columns(2)
    with c_s1:
        if st.button("1000株購入"):
            cost = st.session_state.stock_price * 1000
            if st.session_state.money >= cost:
                st.session_state.money -= cost; st.session_state.stock_owned += 1000; st.rerun()
    with c_s2:
        if st.button("1000株売却"):
            if st.session_state.stock_owned >= 1000:
                st.session_state.money += st.session_state.stock_price * 1000; st.session_state.stock_owned -= 1000; st.rerun()

with tab4:
    ma_val = 10 if st.session_state.is_cleared else 1
    if st.button(f"{ma_val}兆円でM&A調印"):
        cost = ma_val * 1000000000000
        if st.session_state.money >= cost:
            st.session_state.money -= cost; st.session_state.share += (15 * ma_val); st.balloons(); st.rerun()

with tab5:
    st.subheader("インフラ整備")
    cols = st.columns(2)
    for i, (name, info) in enumerate(FACILITIES.items()):
        with cols[i % 2]:
            if not st.session_state[info["id"]]:
                cost_t = f"{info['cost']/100000000:.0f}億" if info['cost'] < 1000000000000 else f"{info['cost']/1000000000000:.1f}兆"
                if st.button(f"{name} ({cost_t})", key=f"btn_{info['id']}"):
                    if st.session_state.money >= info["cost"]:
                        st.session_state.money -= info["cost"]; st.session_state[info["id"]] = True; st.rerun()
            else:
                st.success(f"✅ {name}")

# --- 6. スキップ & ログ ---
st.write("---")
c_sk1, c_sk2 = st.columns(2)
with c_sk1:
    if st.button("⏩ 翌月スキップ", use_container_width=True): run_settlement(1); st.rerun()
with c_sk2:
    if st.button("📅 1年一括スキップ", use_container_width=True): run_settlement(12); st.rerun()

st.subheader("📜 経営ログ")
for log in st.session_state.logs:
    st.caption(log)
