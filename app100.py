import streamlit as st
from datetime import datetime, timedelta
import random

# --- 1. 施設データ ---
FACILITIES = {
    "自社ビル": {"cost": 100000000, "id": "f_building", "effect": "家賃無料"},
    "社員研修所": {"cost": 100000000, "id": "f_training", "effect": "効率+20%"},
    "R&Dセンター": {"cost": 500000000, "id": "f_rd", "effect": "シェア増"},
    "AIデータセンター": {"cost": 2000000000, "id": "f_data", "effect": "売上+5%"},
    "物流拠点": {"cost": 1500000000, "id": "f_logi", "effect": "コスト減"},
    "海外支社": {"cost": 5000000000, "id": "f_overseas", "effect": "世界進出"},
    "政府交渉窓口": {"cost": 1000000000, "id": "f_gov", "effect": "補助金獲得"},
    "保養所": {"cost": 50000000, "id": "f_resort", "effect": "離職防止"},
    "サイバー防衛局": {"cost": 3000000000, "id": "f_cyber", "effect": "不祥事防止"},
    "宇宙開発部門": {"cost": 10000000000, "id": "f_space", "effect": "国家威信UP"},
    "量子計算ラボ": {"cost": 8000000000, "id": "f_quantum", "effect": "開発爆速"},
    "社員食堂": {"cost": 30000000, "id": "f_cafeteria", "effect": "満足度UP"},
    "自家発電施設": {"cost": 200000000, "id": "f_power", "effect": "停電耐性"},
    "社内保育園": {"cost": 70000000, "id": "f_nursery", "effect": "復職率UP"},
    "地下シェルター": {"cost": 5000000000, "id": "f_shelter", "effect": "災害対策"},
    "特許管理事務所": {"cost": 300000000, "id": "f_patent", "effect": "不労所得"},
    "巨大展示場": {"cost": 2500000000, "id": "f_expo", "effect": "知名度UP"},
    "社員専用鉄道": {"cost": 6000000000, "id": "f_train", "effect": "遅刻ゼロ"},
    "AI倫理委員会": {"cost": 150000000, "id": "f_ethics", "effect": "炎上防止"},
    "超高層タワー": {"cost": 50000000000, "id": "f_tower", "effect": "世界一の象徴"}
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
    for f in FACILITIES.values():
        st.session_state[f["id"]] = False

TARGET_SHARE = 100000000

# --- 3. 決算処理 ---
def run_settlement(months=1):
    total_income = 0
    total_interest = 0
    resignation_total = 0
    event_msg = []
    for _ in range(months):
        st.session_state.date += timedelta(days=30)
        income = int(st.session_state.staff * 600000 * (1 + st.session_state.share / 100))
        interest = int(st.session_state.debt * 0.02)
        st.session_state.money += (income - interest)
        total_income += income
        total_interest += interest
        st.session_state.stock_price = int(st.session_state.stock_price * random.uniform(0.85, 1.15))
        resignation_rate = 0.05 if not st.session_state.get('f_resort') else 0.01
        resign_count = int(st.session_state.staff * resignation_rate)
        st.session_state.staff -= resign_count
        resignation_total += resign_count
    return total_income, total_interest, resignation_total, event_msg

# --- 4. クリア判定 ---
if st.session_state.share >= TARGET_SHARE and not st.session_state.is_cleared:
    st.balloons()
    st.snow()
    st.session_state.is_cleared = True

# --- 5. ヘッダー表示 ---
if st.session_state.is_cleared:
    st.title("🌌 銀河帝国シミュレーター")
else:
    st.title("🏛️ 国家規模経営シミュレーター")

col1, col2, col3, col4 = st.columns(4)
col1.metric("現預金", f"{st.session_state.money / 100000000:.2f}億円")
col2.metric("借金", f"{st.session_state.debt / 100000000:.2f}億円")
col3.metric("シェア", f"{st.session_state.share:,}%")
col4.metric("従業員", f"{st.session_state.staff}名")

st.divider()

# --- 6. タブ ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["👤 採用", "💰 金融", "📈 証券", "🤝 M&A", "🏗️ 施設"])

with tab1:
    st.subheader("人材確保")
    st.write("規模に合わせて採用人数を選択してください。")
    
    # 採用単価（クリア後は割引）
    unit_cost = 1000000 if st.session_state.is_cleared else 2000000
    
    # 採用プランの作成
    c_hire1, c_hire2 = st.columns(2)
    with c_hire1:
        if st.button(f"1人採用 ({unit_cost/10000:,.0f}万円)"):
            if st.session_state.money >= unit_cost:
                st.session_state.money -= unit_cost
                st.session_state.staff += 1
                st.rerun()
        if st.button(f"50人一括採用 ({unit_cost*50/100000000:.1f}億円)"):
            if st.session_state.money >= unit_cost * 50:
                st.session_state.money -= unit_cost * 50
                st.session_state.staff += 50
                st.rerun()
    with c_hire2:
        if st.button(f"10人採用 ({unit_cost*10/100000000:.1f}億円)"):
            if st.session_state.money >= unit_cost * 10:
                st.session_state.money -= unit_cost * 10
                st.session_state.staff += 10
                st.rerun()
        if st.button(f"100人一括採用 ({unit_cost*100/100000000:.1f}億円)"):
            if st.session_state.money >= unit_cost * 100:
                st.session_state.money -= unit_cost * 100
                st.session_state.staff += 100
                st.rerun()

# (tab2以降は前のコードと同じため省略していますが、構造は維持されています)
with tab2:
    st.subheader("100億円単位の金融操作")
    c_fin1, c_fin2 = st.columns(2)
    with c_fin1:
        if st.button("💵 100億円 融資"):
            st.session_state.money += 10000000000
            st.session_state.debt += 10000000000
            st.rerun()
    with c_fin2:
        if st.button("🏦 100億円 返済"):
            amount = min(st.session_state.debt, 10000000000)
            if st.session_state.money >= amount:
                st.session_state.money -= amount
                st.session_state.debt -= amount
                st.rerun()

with tab3:
    st.subheader("証券取引")
    if st.button("1000株購入"):
        cost = st.session_state.stock_price * 1000
        if st.session_state.money >= cost:
            st.session_state.money -= cost
            st.session_state.stock_owned += 1000
            st.rerun()
    if st.button("1000株売却"):
        if st.session_state.stock_owned >= 1000:
            st.session_state.money += st.session_state.stock_price * 1000
            st.session_state.stock_owned -= 1000
            st.rerun()

with tab4:
    ma_val = 10 if st.session_state.is_cleared else 1
    if st.button(f"{ma_val}兆円でM&A実行"):
        cost = ma_val * 1000000000000
        if st.session_state.money >= cost:
            st.session_state.money -= cost
            st.session_state.share += (15 * ma_val)
            st.balloons()
            st.rerun()

with tab5:
    cols = st.columns(2)
    for i, (name, info) in enumerate(FACILITIES.items()):
        with cols[i % 2]:
            if not st.session_state[info["id"]]:
                if st.button(f"{name} ({info['cost']/100000000:.1f}億)", key=f"btn_{info['id']}"):
                    if st.session_state.money >= info["cost"]:
                        st.session_state.money -= info["cost"]
                        st.session_state[info["id"]] = True
                        st.rerun()
            else:
                st.success(f"✅ {name}")

# --- 7. スキップボタン ---
st.write("---")
skip_col1, skip_col2 = st.columns(2)
with skip_col1:
    if st.button("⏩ 翌月までスキップ", use_container_width=True):
        run_settlement(1)
        st.rerun()
with skip_col2:
    if st.button("📅 1年（12ヶ月）一括スキップ", use_container_width=True):
        run_settlement(12)
        st.rerun()
