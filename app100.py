import streamlit as st

# --- 定数設定 ---
BUILDING_COST = 100000000         # 1億円
R_D_CENTER_COST = 500000000        # 5億円
DATA_CENTER_COST = 2000000000      # 20億円
TRAINING_CAMP_COST = 100000000     # 1億円

# --- セッションステートの初期化 ---
if 'money' not in st.session_state:
    st.session_state.money = 100000000  # 初期資金1億
    st.session_state.staff = 10
    st.session_state.share = 5
    st.session_state.ma_count = 0
    st.session_state.has_building = False
    st.session_state.has_training_camp = False
    st.session_state.has_rd_center = False
    st.session_state.has_data_center = False

# --- 関数：決算処理 ---
def process_settlement():
    s = st.session_state.staff
    maintenance_fee = 0
    s_efficiency = 1.0
    rent_cost = 2000000 if not st.session_state.has_building else 0
    interest = 0 # 借入がある場合はここに計算を入れる

    # --- 施設によるバフと維持費の処理 ---
    if st.session_state.get('has_rd_center'):
        maintenance_fee += 10000000  # 維持費1000万
        st.session_state.share += 2  # 毎月シェア+2%
        
    if st.session_state.get('has_data_center'):
        maintenance_fee += 50000000  # 維持費5000万
        
    if st.session_state.get('has_training_camp'):
        maintenance_fee += 2000000   # 維持費200万
        s_efficiency = 1.2           # 社員効率20%アップ

    # 売上計算
    multiplier = 1 + (st.session_state.ma_count * 0.5)
    sales = int(s * 600000 * s_efficiency * (1 + st.session_state.share / 100) * multiplier)
    
    if st.session_state.get('has_data_center'):
        sales = int(sales * 1.05)    # データセンターボーナス5%

    # 支出計算
    costs = int(s * 450000) + rent_cost + interest + maintenance_fee
    
    # 利益反映
    profit = sales - costs
    st.session_state.money += profit
    return sales, costs, profit

# --- メイン画面レイアウト ---
st.title("IT企業経営シミュレーション")
st.sidebar.metric("現預金", f"{st.session_state.money:,}円")

# 決算実行ボタン
if st.button("翌月へ進む（決算）"):
    sales, costs, profit = process_settlement()
    st.write(f"結果：売上 {sales:,}円 / 支出 {costs:,}円 / 利益 {profit:,}円")

# --- タブの定義 (ここが重要：NameErrorを防ぐ) ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 経営状況", "👤 人材・広告", "💰 銀行・買収", "🏗️ 施設投資"])

with tab1:
    st.subheader("ステータス")
    st.write(f"社員数: {st.session_state.staff}名")
    st.write(f"市場シェア: {st.session_state.share}%")

with tab2:
    st.subheader("人材採用・広告戦略")
    if st.button("社員を採用する (コスト: 100万)"):
        st.session_state.staff += 1
        st.session_state.money -= 1000000

with tab3:
    st.subheader("金融・M&A")
    st.write("準備中...")

# --- 施設投資タブ（ご提示いただいたコードの組み込み） ---
with tab4:
    st.subheader("拠点・インフラ整備")
    
    col_f1, col_f2 = st.columns(2)
    
    # 1. 自社ビル
    with col_f1:
        if not st.session_state.has_building:
            if st.button(f"🏢 自社ビル ({BUILDING_COST//100000000}億)"):
                if st.session_state.money >= BUILDING_COST:
                    st.session_state.money -= BUILDING_COST
                    st.session_state.has_building = True
                    st.rerun()
                else:
                    st.error("資金が不足しています")
        else:
            st.success("🏢 自社ビル保有 (家賃0/シェア増)")

    # 2. 研修所
    with col_f2:
        if not st.session_state.get('has_training_camp'):
            if st.button(f"🏫 研修所 ({TRAINING_CAMP_COST//100000000}億)"):
                if st.session_state.money >= TRAINING_CAMP_COST:
                    st.session_state.money -= TRAINING_CAMP_COST
                    st.session_state.has_training_camp = True
                    st.rerun()
                else:
                    st.error("資金が不足しています")
        else:
            st.success("🏫 研修所 (社員効率+20%)")

    col_f3, col_f4 = st.columns(2)

    # 3. 研究開発センター
    with col_f3:
        if not st.session_state.get('has_rd_center'):
            if st.button(f"🔬 R&Dセンター ({R_D_CENTER_COST//100000000}億)"):
                if st.session_state.money >= R_D_CENTER_COST:
                    st.session_state.money -= R_D_CENTER_COST
                    st.session_state.has_rd_center = True
                    st.rerun()
                else:
                    st.error("資金が不足しています")
        else:
            st.success("🔬 R&Dセンター (自動シェア増)")

    # 4. AIデータセンター
    with col_f4:
        if not st.session_state.get('has_data_center'):
            if st.button(f"🛰️ AIデータセンター ({DATA_CENTER_COST//100000000}億)"):
                if st.session_state.money >= DATA_CENTER_COST:
                    st.session_state.money -= DATA_CENTER_COST
                    st.session_state.has_data_center = True
                    st.rerun()
                else:
                    st.error("資金が不足しています")
        else:
            st.success("🛰️ データセンター (売上+5%)")
