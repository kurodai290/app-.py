import streamlit as st
from datetime import datetime, timedelta
import random

# --- 設定・初期化（全ページ共通） ---
st.set_page_config(page_title="国家規模経営シミュレーター", layout="wide")

if 'money' not in st.session_state:
    st.session_state.money = 1970000000 
    st.session_state.debt = 0
    st.session_state.share = 1
    st.session_state.staff = 121
    st.session_state.date = datetime(2052, 4, 3)
    st.session_state.stock_price = 10000
    st.session_state.stock_owned = 0
    st.session_state.scandal_timer = 0
    st.session_state.logs = []
    # 施設フラグの初期化
    if 'facilities' not in st.session_state:
        st.session_state.facilities = {}

# --- 共通ヘッダー関数 ---
def show_status():
    st.title("🏛️ 国家規模経営シミュレーター")
    if st.session_state.scandal_timer > 0:
        st.error(f"🚨 不祥事デバフ中（残り{st.session_state.scandal_timer}ヶ月）")
    
    col_t1, col_t2 = st.columns(2)
    col_t1.subheader(st.session_state.date.strftime("%Y年%m月%d日"))
    col_t2.subheader(f"📈 保有株: {st.session_state.stock_owned:,} 株")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("現預金", f"{st.session_state.money / 100000000:.1f}億円")
    col2.metric("借金", f"{st.session_state.debt / 100000000:.1f}億円")
    col3.metric("シェア", f"{st.session_state.share:,}%")
    col4.metric("従業員", f"{st.session_state.staff:,}名")
    st.divider()

show_status()

# --- メインコンテンツ（採用・施設など） ---
tab1, tab2, tab3 = st.tabs(["👤 採用", "💰 金融", "🏗️ 施設投資"])

with tab1:
    st.subheader("採用センター")
    if st.button("10人採用 (2,000万円)"):
        if st.session_state.money >= 20000000:
            st.session_state.money -= 20000000
            st.session_state.staff += 10
            st.rerun()

with tab2:
    if st.button("💵 100億円 融資"):
        st.session_state.money += 10000000000
        st.session_state.debt += 10000000000
        st.rerun()

# 翌月スキップなどの共通操作
st.write("---")
if st.button("⏩ 翌月スキップ", use_container_width=True):
    # ここに共通のrun_settlementロジックを入れる
    st.session_state.date += timedelta(days=30)
    st.session_state.stock_price = int(st.session_state.stock_price * random.uniform(0.9, 1.1))
    st.rerun()

st.sidebar.info("左のメニューから「株専用ページ」へ移動できます")
