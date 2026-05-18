import streamlit as st
from datetime import datetime, timedelta

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
    for f in FACILITIES.values():
        st.session_state[f["id"]] = False

# --- 3. 関数：決算処理 ---
def run_settlement(months=1):
    total_income = 0
    total_interest = 0
    
    for _ in range(months):
        st.session_state.date += timedelta(days=30)
        # 売上計算
        income = int(st.session_state.staff * 600000 * (1 + st.session_state.share / 100))
        # 利息計算（月2%）
        interest = int(st.session_state.debt * 0.02)
        
        st.session_state.money += (income - interest)
        total_income += income
        total_interest += interest
        
    return total_income, total_interest

# --- 4. ヘッダー表示 ---
st.title("🏛️ 国家規模経営シミュレーター")

col1, col2, col3, col4 = st.columns(4)
col1.metric("現預金", f"{st.session_state.money / 100000000:.2f}億円")
col2.metric("借金", f"{st.session_state.debt / 100000000:.2f}億円")
col3.metric("シェア", f"{st.session_state.share}%")
col4.metric("従業員", f"{st.session_state.staff}名")

st.divider()

# --- 5. タブ ---
tab1, tab2, tab3, tab4 = st.tabs(["👤 採用・広報", "💰 金融・融資", "🤝 1兆円M&A", "🏗️ 施設投資"])

with tab1:
    st.subheader("人材・ブランド戦略")
    if st.button("精鋭を採用 (1,000万円)"):
        st.session_state.money -= 10000000
        st.session_state.staff += 5
        st.rerun()

with tab2:
    st.subheader("資金調達と返済")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("10億円 融資を受ける"):
            st.session_state.money += 1000000000
            st.session_state.debt += 1000000000
            st.rerun()
    with c2:
        if st.button("10億円 借金を返済する"):
            if st.session_state.money >= 1000000000 and st.session_state.debt >= 1000000000:
                st.session_state.money -= 1000000000
                st.session_state.debt -= 1000000000
                st.success("返済成功")
                st.rerun()

with tab3:
    st.subheader("🤝 巨大M&A（企業買収）")
    st.write("ライバル企業を買収して市場を独占します。")
    
    ma_price = 1000000000000  # 1兆円
    st.info(f"買収価格: 1兆円 / 獲得シェア: +15%")
    
    if st.button("1兆円で競合他社を買収する"):
        if st.session_state.money >= ma_price:
            st.session_state.money -= ma_price
            st.session_state.share += 15
            st.balloons()
            st.success("歴史的なM&Aが成立しました！世界に衝撃が走っています。")
        else:
            st.error("資金が足りません。国家予算レベルの蓄えが必要です。")

with tab4:
    st.subheader(f"インフラ整備（{sum(st.session_state[f['id']] for f in FACILITIES.values())}/20）")
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

# --- 6. スキップボタンエリア ---
st.write("---")
skip_col1, skip_col2 = st.columns(2)

with skip_col1:
    if st.button("⏩ 翌月までスキップ", use_container_width=True):
        inc, intr = run_settlement(1)
        st.toast(f"1ヶ月経過：利益 {inc-intr:,}円")
        st.rerun()

with skip_col2:
    if st.button("📅 1年（12ヶ月）スキップ", use_container_width=True):
        inc, intr = run_settlement(12)
        st.warning(f"1年が経過しました！ 総利益: {inc-intr:,}円")
        st.rerun()
