import streamlit as st
from datetime import datetime, timedelta
import random

# --- 1. 施設データ（20種類） ---
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
    # 株システム
    st.session_state.stock_price = 10000  # 初期株価
    st.session_state.stock_owned = 0      # 保有株数
    for f in FACILITIES.values():
        st.session_state[f["id"]] = False

# --- 3. 関数：決算処理（株価変動を追加） ---
def run_settlement(months=1):
    total_income = 0
    total_interest = 0
    for _ in range(months):
        st.session_state.date += timedelta(days=30)
        # 売上・利息計算
        income = int(st.session_state.staff * 600000 * (1 + st.session_state.share / 100))
        interest = int(st.session_state.debt * 0.02)
        st.session_state.money += (income - interest)
        total_income += income
        total_interest += interest
        # 株価の変動 (±10%)
        change = random.uniform(0.9, 1.1)
        st.session_state.stock_price = int(st.session_state.stock_price * change)
    return total_income, total_interest

# --- 4. ヘッダー表示 ---
st.title("🏛️ 国家規模経営シミュレーター")

col_header1, col_header2 = st.columns(2)
with col_header1:
    st.caption("📅 日付")
    st.subheader(st.session_state.date.strftime("%Y年%m月%d日"))
with col_header2:
    st.caption("📈 市場株価")
    st.subheader(f"{st.session_state.stock_price:,}円")

col1, col2, col3, col4 = st.columns(4)
col1.metric("現預金", f"{st.session_state.money / 100000000:.2f}億円")
col2.metric("借金", f"{st.session_state.debt / 100000000:.2f}億円")
col3.metric("シェア", f"{st.session_state.share}%")
col4.metric("保有株", f"{st.session_state.stock_owned}株")

st.divider()

# --- 5. タブ ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["👤 採用・広報", "💰 金融・融資", "📈 証券取引", "🤝 1兆円M&A", "🏗️ 施設投資"])

with tab1:
    st.subheader("戦略的採用")
    if st.button("精鋭を採用 (1,000万円)"):
        st.session_state.money -= 10000000
        st.session_state.staff += 5
        st.rerun()

with tab2:
    st.subheader("100億円単位の金融操作")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💵 100億円 融資を受ける"):
            st.session_state.money += 10000000000
            st.session_state.debt += 10000000000
            st.rerun()
    with c2:
        if st.button("🏦 100億円 借金を返済する"):
            if st.session_state.money >= 10000000000 and st.session_state.debt >= 10000000000:
                st.session_state.money -= 10000000000
                st.session_state.debt -= 10000000000
                st.rerun()

with tab3:
    st.subheader("📉 株式売買（インデックス投資）")
    st.write(f"現在の株価: **{st.session_state.stock_price:,}円**")
    st.write(f"保有数: **{st.session_state.stock_owned:,}株** (評価額: {st.session_state.stock_owned * st.session_state.stock_price:,}円)")
    
    sc1, sc2 = st.columns(2)
    with sc1:
        if st.button("1000株 買う"):
            cost = st.session_state.stock_price * 1000
            if st.session_state.money >= cost:
                st.session_state.money -= cost
                st.session_state.stock_owned += 1000
                st.success(f"{cost:,}円で購入しました")
                st.rerun()
            else:
                st.error("資金不足です")
    with sc2:
        if st.button("1000株 売る"):
            if st.session_state.stock_owned >= 1000:
                gain = st.session_state.stock_price * 1000
                st.session_state.money += gain
                st.session_state.stock_owned -= 1000
                st.success(f"{gain:,}円で売却しました")
                st.rerun()
            else:
                st.error("持ち株がありません")

with tab4:
    st.subheader("🤝 巨大M&A")
    if st.button("1兆円で買収契約に調印"):
        if st.session_state.money >= 1000000000000:
            st.session_state.money -= 1000000000000
            st.session_state.share += 15
            st.balloons()
            st.rerun()

with tab5:
    st.subheader("🏗️ 施設建設")
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

# --- 6. スキップボタン ---
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
