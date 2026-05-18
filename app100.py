import streamlit as st

# --- 定数設定 ---
BUILDING_COST = 100000000
TRAINING_CAMP_COST = 100000000
R_D_CENTER_COST = 500000000
DATA_CENTER_COST = 2000000000

# --- セッションステート初期化 ---
if 'money' not in st.session_state:
    st.session_state.money = 1970000000  # 画像に合わせて19.7億
    st.session_state.debt = 0
    st.session_state.share = 1
    st.session_state.staff = 121
    st.session_state.date = "2052年04月03日"
    st.session_state.ma_count = 0
    st.session_state.has_building = False
    st.session_state.has_training_camp = False
    st.session_state.has_rd_center = False
    st.session_state.has_data_center = False

# --- ヘッダー部分 (画像のデザインを再現) ---
st.title("🏛️ 国家規模経営シミュレーター")

# 日付と決算タイマーの行
col_header1, col_header2 = st.columns(2)
with col_header1:
    st.caption("📅 日付")
    st.subheader(st.session_state.date)
with col_header2:
    st.caption("⏳ 決算まで")
    st.subheader("75秒")

# 主要ステータスの4列表示
col1, col2, col3, col4 = st.columns(4)
col1.metric("現預金", f"{st.session_state.money / 100000000:.1f}億円")
col2.metric("借金", f"{st.session_state.debt / 100000000:.1f}億円")
col3.metric("シェア", f"{st.session_state.share}%")
col4.metric("従業員", f"{st.session_state.staff}名")

st.divider() # 区切り線

# --- タブの配置 ---
tab1, tab2, tab3, tab4 = st.tabs(["採用・広報", "巨大融資", "1兆円M&A", "⏩ 施設投資"])

# 施設投資タブの中身
with tab4:
    st.subheader("🏗️ 拠点・インフラ整備")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        if not st.session_state.has_building:
            if st.button(f"🏢 自社ビル (1億)"):
                if st.session_state.money >= BUILDING_COST:
                    st.session_state.money -= BUILDING_COST
                    st.session_state.has_building = True
                    st.rerun()
        else:
            st.success("🏢 自社ビル保有")

    with col_f2:
        if not st.session_state.get('has_training_camp'):
            if st.button(f"🏫 研修所 (1億)"):
                if st.session_state.money >= TRAINING_CAMP_COST:
                    st.session_state.money -= TRAINING_CAMP_COST
                    st.session_state.has_training_camp = True
                    st.rerun()
        else:
            st.success("🏫 研修所稼働中")

    col_f3, col_f4 = st.columns(2)
    with col_f3:
        if not st.session_state.get('has_rd_center'):
            if st.button(f"🔬 R&Dセンター (5億)"):
                if st.session_state.money >= R_D_CENTER_COST:
                    st.session_state.money -= R_D_CENTER_COST
                    st.session_state.has_rd_center = True
                    st.rerun()
        else:
            st.success("🔬 R&Dセンター稼働中")

    with col_f4:
        if not st.session_state.get('has_data_center'):
            if st.button(f"🛰️ AIデータセンター (20億)"):
                if st.session_state.money >= DATA_CENTER_COST:
                    st.session_state.money -= DATA_CENTER_COST
                    st.session_state.has_data_center = True
                    st.rerun()
        else:
            st.success("🛰️ AIデータセンター稼働中")

# 下部の操作ボタン
st.write("")
if st.button("⏩ 翌月までスキップ"):
    # ここに process_settlement() を呼び出す処理
    st.toast("一ヶ月が経過しました")
