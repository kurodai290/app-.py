import streamlit as st
from datetime import datetime, timedelta
import random

# --- 1. 施設データ（価格を大幅に引き上げ） ---
FACILITIES = {
    "自社ビル": {"cost": 500000000, "id": "f_building", "effect": "家賃無料"}, # 5億
    "社員研修所": {"cost": 1000000000, "id": "f_training", "effect": "効率+20%"}, # 10億
    "R&Dセンター": {"cost": 5000000000, "id": "f_rd", "effect": "シェア増"}, # 50億
    "AIデータセンター": {"cost": 20000000000, "id": "f_data", "effect": "売上+5%"}, # 200億
    "物流拠点": {"cost": 50000000000, "id": "f_logi", "effect": "コスト減"}, # 500億
    "海外支社": {"cost": 100000000000, "id": "f_overseas", "effect": "世界進出"}, # 1000億
    "政府交渉窓口": {"cost": 300000000000, "id": "f_gov", "effect": "補助金獲得"}, # 3000億
    "保養所": {"cost": 10000000000, "id": "f_resort", "effect": "離職防止"}, # 100億
    "サイバー防衛局": {"cost": 500000000000, "id": "f_cyber", "effect": "不祥事防止"}, # 5000億
    "宇宙開発部門": {"cost": 1000000000000, "id": "f_space", "effect": "国家威信UP"}, # 1兆
    "量子計算ラボ": {"cost": 2000000000000, "id": "f_quantum", "effect": "開発爆速"}, # 2兆
    "社員食堂": {"cost": 500000000, "id": "f_cafeteria", "effect": "満足度UP"}, # 5億
    "自家発電施設": {"cost": 3000000000, "id": "f_power", "effect": "停電耐性"}, # 30億
    "社内保育園": {"cost": 1000000000, "id": "f_nursery", "effect": "復職率UP"}, # 10億
    "地下シェルター": {"cost": 1000000000000, "id": "f_shelter", "effect": "災害対策"}, # 1兆
    "特許管理事務所": {"cost": 50000000000, "id": "f_patent", "effect": "不労所得"}, # 500億
    "巨大展示場": {"cost": 150000000000, "id": "f_expo", "effect": "知名度UP"}, # 1500億
    "社員専用鉄道": {"cost": 800000000000, "id": "f_train", "effect": "遅刻ゼロ"}, # 8000億
    "AI倫理委員会": {"cost": 20000000000, "id": "f_ethics", "effect": "炎上防止"}, # 200億
    "超高層タワー": {"cost": 5000000000000, "id": "f_tower", "effect": "世界一の象徴"} # 5兆
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
    for _ in range(months):
        st.session_state.date += timedelta(days=30)
        income = int(st.session_state.staff * 600000 * (1 + st.session_state.share / 100))
        interest = int(st.session_state.debt * 0.02)
        st.session_state.money += (income - interest)
        total_income += income
        total_interest += interest
        st.session_state.stock_price = int(st.session_state.stock_price * random.uniform(0.85, 1.15))
        resignation_rate = 0.05 if not st.session_state.get('f_resort') else 0.01
        st.session_state.staff = max(0, st.session_state.staff - int(st.session_state.staff * resignation_rate))
    return total_income, total_interest

# --- 4. クリア判定 ---
if st.session_state.share >= TARGET_SHARE and not st.session_state.is_cleared:
    st.balloons()
    st.snow()
    st.session_state.is_cleared = True

# --- 5. ヘッダー表示 ---
st.title("🌌 " + ("銀河帝国" if st.session_state.is_cleared else "国家規模経営") + "シミュレーター")

col1, col2, col3, col4 = st.columns(4)
col1.metric("現預金", f"{st.session_state.money / 100000000:.2f}億円")
col2.metric("借金", f"{st.session_state.debt / 100000000:.2f}億円")
col3.metric("シェア", f"{st.session_state.share:,}%")
col4.metric("従業員", f"{st.session_state.staff}名")

st.divider()

# --- 6. タブ ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["👤 採用", "💰 金融", "📈 証券", "🤝 M&A", "🏗️ 施設"])

with tab1:
    st.subheader("採用戦略")
    unit_cost = 1000000 if st.session_state.is_cleared else 2000000
    c_hire1, c_hire2 = st.columns(2)
    with c_hire1:
        if st.button(f"1人採用 ({unit_cost/10000:,.0f}万)"):
            if st.session_state.money >= unit_cost: st.session_state.money -= unit_cost; st.session_state.staff += 1; st.rerun()
        if st.button(f"50人採用 ({unit_cost*50/100000000:.1f}億)"):
            if st.session_state.money >= unit_cost * 50: st.session_state.money -= unit_cost * 50; st.session_state.staff += 50; st.rerun()
    with c_hire2:
        if st.button(f"10人採用 ({unit_cost*10/100000000:.1f}億)"):
            if st.session_state.money >= unit_cost * 10: st.session_state.money -= unit_cost * 10; st.session_state.staff += 10; st.rerun()
        if st.button(f"100人採用 ({unit_cost*100/100000000:.1f}億)"):
            if st.session_state.money >= unit_cost * 100: st.session_state.money -= unit_cost * 100; st.session_state.staff += 100; st.rerun()

with tab2:
    st.subheader("金融")
    c_fin1, c_fin2 = st.columns(2)
    with c_fin1:
        if st.button("💵 100億円 融資"): st.session_state.money += 10000000000; st.session_state.debt += 10000000000; st.rerun()
    with c_fin2:
        if st.button("🏦 100億円 返済"):
            amount = min(st.session_state.debt, 10000000000)
            if st.session_state.money >= amount: st.session_state.money -= amount; st.session_state.debt -= amount; st.rerun()

with tab3:
    st.subheader("証券（現在値: " + f"{st.session_state.stock_price:,}円)")
    if st.button("1000株購入"):
        cost = st.session_state.stock_price * 1000
        if st.session_state.money >= cost: st.session_state.money -= cost; st.session_state.stock_owned += 1000; st.rerun()
    if st.button("1000株売却"):
        if st.session_state.stock_owned >= 1000: st.session_state.money += st.session_state.stock_price * 1000; st.session_state.stock_owned -= 1000; st.rerun()

with tab4:
    ma_val = 10 if st.session_state.is_cleared else 1
    st.subheader(f"M&A ({ma_val}兆円)")
    if st.button(f"{ma_val}兆円で買収"):
        cost = ma_val * 1000000000000
        if st.session_state.money >= cost: st.session_state.money -= cost; st.session_state.share += (15 * ma_val); st.balloons(); st.rerun()

with tab5:
    st.subheader("インフラ整備")
    cols = st.columns(2)
    for i, (name, info) in enumerate(FACILITIES.items()):
        with cols[i % 2]:
            if not st.session_state[info["id"]]:
                # 億円または兆円で表示
                cost_text = f"{info['cost']/100000000:.0f}億" if info['cost'] < 1000000000000 else f"{info['cost']/1000000000000:.1f}兆"
                if st.button(f"{name} ({cost_text})", key=f"btn_{info['id']}"):
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
    if st.button("⏩ 翌月までスキップ", use_container_width=True): run_settlement(1); st.rerun()
with skip_col2:
    if st.button("📅 1年一括スキップ", use_container_width=True): run_settlement(12); st.rerun()
