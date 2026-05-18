import streamlit as st
from datetime import datetime, timedelta
import random
import pandas as pd

# --- 1. セッションステート初期化（安全チェック強化） ---
if 'money' not in st.session_state:
    st.session_state.money = 1970000000 
    st.session_state.debt = 0
    st.session_state.share = 1
    st.session_state.staff = 121
    st.session_state.date = datetime(2052, 4, 3)
    st.session_state.stock_price = 10000
    st.session_state.last_stock_price = 10000
    st.session_state.stock_owned = 0
    st.session_state.scandal_timer = 0
    st.session_state.logs = []
    st.session_state.price_history = [10000] # 初期の履歴
    st.session_state.page = "メイン"

# 【重要】途中で追加した変数が消えていた場合、ここで復活させる
if 'price_history' not in st.session_state:
    st.session_state.price_history = [st.session_state.stock_price]
if 'page' not in st.session_state:
    st.session_state.page = "メイン"

# --- 2. 共通関数 ---
def add_log(msg):
    st.session_state.logs.insert(0, f"[{st.session_state.date.strftime('%Y/%m')}] {msg}")
    st.session_state.logs = st.session_state.logs[:10]

def run_settlement(months=1):
    for _ in range(months):
        st.session_state.date += timedelta(days=30)
        # 収益計算（通常 or 不祥事）
        income = int(st.session_state.staff * 600000 * (1 + st.session_state.share / 100))
        if st.session_state.scandal_timer > 0:
            income //= 10
            st.session_state.scandal_timer -= 1
        
        # 利息・配当
        div = int((st.session_state.stock_owned * st.session_state.stock_price) * 0.005)
        st.session_state.money += (income - int(st.session_state.debt * 0.02) + div)
        
        # 株価変動
        st.session_state.last_stock_price = st.session_state.stock_price
        change = random.uniform(0.85, 1.15)
        st.session_state.stock_price = max(100, int(st.session_state.stock_price * change))
        
        # 履歴を保存
        st.session_state.price_history.append(st.session_state.stock_price)
        if len(st.session_state.price_history) > 24:
            st.session_state.price_history.pop(0)
            
    add_log(f"決算完了 ({months}ヶ月)")

# --- 3. ナビゲーション ---
st.title("🏛️ 国家規模経営シミュレーター")
nav_col1, nav_col2 = st.columns(2)
with nav_col1:
    if st.button("🏢 経営・施設画面へ", use_container_width=True):
        st.session_state.page = "メイン"
        st.rerun()
with nav_col2:
    if st.button("📈 株専用ページへ", use_container_width=True):
        st.session_state.page = "株"
        st.rerun()
st.divider()

# --- 4. 共通ステータス ---
col_t1, col_t2 = st.columns(2)
with col_t1:
    st.subheader(st.session_state.date.strftime("%Y年%m月%d日"))
with col_t2:
    st.subheader(f"💰 所持金: {st.session_state.money / 100000000:.1f} 億円")

# --- 5. ページ出し分け ---

# 【A. メインページ】
if st.session_state.page == "メイン":
    st.header("🏢 経営本部")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("従業員", f"{st.session_state.staff}名")
    col2.metric("シェア", f"{st.session_state.share}%")
    col3.metric("借金", f"{st.session_state.debt / 100000000:.1f}億円")
    col4.metric("保有株", f"{st.session_state.stock_owned:,}株")

    st.write("---")
    st.subheader("採用・施設")
    if st.button("精鋭を採用 (1,000万円)"):
        st.session_state.money -= 10000000
        st.session_state.staff += 5
        st.rerun()

# 【B. 株専用ページ】
elif st.session_state.page == "株":
    st.header("📈 証券取引・市場チャート")
    
    # チャート表示
    st.subheader("株価トレンド（直近24ヶ月）")
    # データが空にならないよう安全に変換
    if st.session_state.price_history:
        chart_data = pd.DataFrame(st.session_state.price_history, columns=["株価"])
        st.line_chart(chart_data)
    
    col_s1, col_s2, col_s3 = st.columns(3)
    diff = st.session_state.stock_price - st.session_state.last_stock_price
    ratio = (diff / st.session_state.last_stock_price * 100) if st.session_state.last_stock_price > 0 else 0
    col_s1.metric("現在株価", f"{st.session_state.stock_price:,}円", delta=f"{ratio:.1f}%")
    col_s2.metric("保有株数", f"{st.session_state.stock_owned:,}株")
    col_s3.metric("配当見込", f"{int(st.session_state.stock_owned * st.session_state.stock_price * 0.005):,}円")

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        if st.button("1000株購入"):
            cost = st.session_state.stock_price * 1000
            if st.session_state.money >= cost:
                st.session_state.money -= cost
                st.session_state.stock_owned += 1000
                st.rerun()
    with c2:
        if st.button("1000株売却"):
            if st.session_state.stock_owned >= 1000:
                st.session_state.money += st.session_state.stock_price * 1000
                st.session_state.stock_owned -= 1000
                st.rerun()

# --- 6. 共通下部操作 ---
st.write("---")
skip1, skip2 = st.columns(2)
with skip1:
    if st.button("⏩ 翌月スキップ", use_container_width=True):
        run_settlement(1)
        st.rerun()
with skip2:
    if st.button("📅 1年スキップ", use_container_width=True):
        run_settlement(12)
        st.rerun()

st.subheader("📜 経営ログ")
for log in st.session_state.logs:
    st.caption(log)
