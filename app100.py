import streamlit as st

# --- 定数設定 ---
BUILDING_COST = 100000000
TRAINING_CAMP_COST = 100000000
R_D_CENTER_COST = 500000000
DATA_CENTER_COST = 2000000000

# --- セッションステート初期化 ---
if 'money' not in st.session_state:
    st.session_state.money = 1970000000 
    st.session_state.debt = 0
    st.session_state.share = 1
    st.session_state.staff = 121
    st.session_state.date = "2052年04月03日"
    st.session_state.has_building = False
    st.session_state.has_training_camp = False
    st.session_state.has_rd_center = False
    st.session_state.has_data_center = False

# --- ヘッダー・ステータス表示 ---
st.title("🏛️ 国家規模経営シミュレーター")

col_header1, col_header2 = st.columns(2)
with col_header1:
    st.caption("📅 日付")
    st.subheader(st.session_state.date)
with col_header2:
    st.caption("⏳ 決算まで")
    st.subheader("75秒")

col1, col2, col3, col4 = st.columns(4)
col1.metric("現預金", f"{st.session_state.money / 100000000:.1f}億円")
col2.metric("借金", f"{st.session_state.debt / 100000000:.1f}億円")
col3.metric("シェア", f"{st.session_state.share}%")
col4.metric("従業員", f"{st.session_state.staff}名")

st.divider()

# --- 【重要】タブごとの中身をしっかり定義 ---
tab1, tab2, tab3, tab4 = st.tabs(["採用・広報", "巨大融資", "1兆円M&A", "施設投資"])

with tab1:
    st.subheader("👤 人材採用・広告")
    if st.button("新人採用 (1,000万円)"):
        if st.session_state.money >= 10000000:
            st.session_state.money -= 10000000
            st.session_state.staff += 5
            st.success("5名の精鋭を採用しました")
        else:
            st.error("資金が足りません")

with tab2:
    st.subheader("💰 巨大融資")
    if st.button("国家特別融資を受ける (10億円)"):
        st.session_state.money += 1000000000
        st.session_state.debt += 1000000000
        st.warning("10億円を借り入れました")

with tab3:
    st.subheader("🤝 巨大M&A")
    if st.button("競合他社を買収する (100億円)"):
        if st.session_state.money >= 10000000000:
            st.session_state.money -= 10000000000
            st.session_state.share += 20
            st.success("業界シェアを大幅に獲得しました！")
        else:
            st.error("100億円には及びません")

with tab4:
    st.subheader("🏗️ 拠点・インフラ整備")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        if not st.session_state.has_building:
            if st.button("🏢 自社ビル (1億)"):
                if st.session_state.money >= BUILDING_COST:
                    st.session_state.money -= BUILDING_COST
                    st.session_state.has_building = True
                    st.rerun()
        else:
            st.info("🏢 自社ビル保有済み")

    with col_f2:
        if not st.session_state.get('has_training_camp'):
            if st.button("🏫 研修所 (1億)"):
                if st.session_state.money >= TRAINING_CAMP_COST:
                    st.session_state.money -= TRAINING_CAMP_COST
                    st.session_state.has_training_camp = True
                    st.rerun()
        else:
            st.info("🏫 研修所稼働中")

# --- 共通の操作ボタン（タブの外に配置） ---
st.write("---")
if st.button("⏩ 翌月までスキップ"):
    # 決算ロジックをここに書くか、別関数を呼び出す
    st.toast("一ヶ月が経過しました")
    st.rerun()
