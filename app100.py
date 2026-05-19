import streamlit as st
from datetime import datetime, timedelta
import random
import pandas as pd

# --- 1. 施設・銀河投資データ ---
FACILITIES = {
    "自社ビル": 500000000, "社員研修所": 1000000000, "R&Dセンター": 5000000000,
    "AIデータセンター": 20000000000, "海外支社": 100000000000, "サイバー防衛局": 500000000000,
    "宇宙開発部門": 1000000000000, "AI倫理委員会": 20000000000, "超高層タワー": 5000000000000
}
GALAXY_INV = {
    "月面基地建設": {"cost": 10000000000000, "share": 500},
    "火星テラフォーミング": {"cost": 50000000000000, "share": 2500},
    "銀河証券取引所設立": {"cost": 100000000000000, "share": 10000}
}

# --- 2. 初期化 ---
if 'money' not in st.session_state:
    st.session_state.update({
        'money': 1970000000, 'debt': 0, 'share': 1, 'staff': 121,
        'date': datetime(2052, 4, 3), 'stock_price': 10000, 'last_stock_price': 10000,
        'stock_owned': 0, 'scandal_timer': 0,
        'logs': [], 'price_history': [10000], 'page': "メイン"
    })
    for k in FACILITIES: st.session_state[f"f_{k}"] = False
    for k in GALAXY_INV: st.session_state[f"g_{k}"] = False

def add_log(msg):
    st.session_state.logs.insert(0, f"[{st.session_state.date.strftime('%y/%m')}] {msg}")
    st.session_state.logs = st.session_state.logs[:8]

# --- 3. 決算（株価変動修正版） ---
def run_settlement(months=1):
    m_profit = 0
    for _ in range(months):
        st.session_state.date += timedelta(days=30)
        curr_m = st.session_state.date.month
        
        inc = int(st.session_state.staff * 600000 * (1 + st.session_state.share / 100))
        if st.session_state.scandal_timer > 0:
            inc //= 10
            st.session_state.scandal_timer -= (3 if st.session_state.get('f_AI倫理委員会') else 1)
        
        bonus = st.session_state.staff * 1000000 if curr_m == 12 else 0
        div = int((st.session_state.stock_owned * st.session_state.stock_price) * 0.005)
        m_profit += (inc - int(st.session_state.debt * 0.02) + div - bonus)
        
        # 株価変動
        st.session_state.last_stock_price = st.session_state.stock_price
        st.session_state.stock_price = max(100, int(st.session_state.stock_price * random.uniform(0.8, 1.2)))
        st.session_state.price_history.append(st.session_state.stock_price)
        if len(st.session_state.price_history) > 60: st.session_state.price_history.pop(0)

        res = 0 if curr_m == 1 else (int(st.session_state.staff * 0.08) + 5) if curr_m in [3,4] else random.randint(1, 3)
        st.session_state.staff = max(1, st.session_state.staff - res + int(res*0.5))

    st.session_state.money += m_profit
    add_log(f"決算完了: {months}ヶ月分")

# --- 4. 描画 ---
st.title("🏛️ 国家・銀河経営シミュレーター")
n1, n2 = st.columns(2)
if n1.button("🏢 経営本部", use_container_width=True): st.session_state.page = "メイン"; st.rerun()
if n2.button("📈 証券・銀河", use_container_width=True): st.session_state.page = "株"; st.rerun()

st.subheader(f"📅 {st.session_state.date.strftime('%Y/%m/%d')} | 💰 {st.session_state.money / 100000000:.1f} 億円")

# --- 5. メインページ ---
if st.session_state.page == "メイン":
    c1, c2, c3 = st.columns(3)
    c1.metric("従業員", f"{st.session_state.staff:,}名")
    c2.metric("シェア", f"{st.session_state.share:,}%")
    c3.metric("不祥事残", f"{max(0, st.session_state.scandal_timer)}月")

    t1, t2, t3 = st.tabs(["👥 採用", "🏢 施設", "🤝 M&A/金融"])
    mult = 0.5 if st.session_state.stock_owned >= 1000000 else 0.8 if st.session_state.stock_owned >= 100000 else 1.0

    with t1:
        u_cost = int(2000000 * mult)
        cols = st.columns(2)
        for i, n in enumerate([10, 50, 100, 1000]):
            with cols[i % 2]:
                if st.button(f"{n}人採用 ({u_cost*n/100000000:.2f}億)", key=f"hire_{n}"):
                    if st.session_state.money >= u_cost*n:
                        st.session_state.money -= u_cost*n; st.session_state.staff += n; st.rerun()
    with t2:
        cols = st.columns(2)
        for i, (name, cost) in enumerate(FACILITIES.items()):
            with cols[i % 2]:
                if not st.session_state.get(f"f_{name}"):
                    c = int(cost * mult)
                    if st.button(f"{name} ({c/100000000:.0f}億)", key=f"fac_{name}"):
                        if st.session_state.money >= c: st.session_state.money -= c; st.session_state[f"f_{name}"] = True; st.rerun()
                else: st.success(f"✅ {name}")
    with t3:
        if st.button("💵 100億融資"): st.session_state.money += 10000000000; st.session_state.debt += 10000000000; st.rerun()
        if st.button("🏦 100億返済"):
            amt = min(st.session_state.debt, 10000000000)
            if st.session_state.money >= amt: st.session_state.money -= amt; st.session_state.debt -= amt; st.rerun()
        ma_cost = int(1e12 * mult)
        if st.button(f"1兆円M&A (実費:{ma_cost/1e12:.2f}兆)"):
            if st.session_state.money >= ma_cost: st.session_state.money -= ma_cost; st.session_state.share += 15; st.balloons(); st.rerun()

# --- 6. 株ページ ---
elif st.session_state.page == "株":
    # グラフの修正
    df = pd.DataFrame(st.session_state.price_history, columns=["株価"])
    st.line_chart(df)
    
    s1, s2 = st.columns(2)
    diff = st.session_state.stock_price - st.session_state.last_stock_price
    s1.metric("株価", f"{st.session_state.stock_price:,}円", delta=f"{diff:,}円")
    s2.metric("保有株", f"{st.session_state.stock_owned:,}株")
    
    if st.button("1万株購入"):
        c = st.session_state.stock_price * 10000
        if st.session_state.money >= c:
            st.session_state.money -= c; st.session_state.stock_owned += 10000; st.rerun()
    
    st.divider()
    st.subheader("🌌 銀河進出プロジェクト")
    for name, info in GALAXY_INV.items():
        if not st.session_state.get(f"g_{name}"):
            if st.button(f"{name} ({info['cost']/1e12:.0f}兆円)"):
                if st.session_state.money >= info['cost']:
                    st.session_state.money -= info['cost']; st.session_state.share += info['share']; st.session_state[f"g_{name}"] = True; st.balloons(); st.rerun()
        else: st.success(f"🌌 {name} 完了")

# --- 7. 共通スキップ ---
st.write("---")
sk1, sk2 = st.columns(2)
if sk1.button("⏩ 翌月スキップ", use_container_width=True): run_settlement(1); st.rerun()
if sk2.button("📅 1年一括スキップ", use_container_width=True): run_settlement(12); st.rerun()
for log in st.session_state.logs: st.caption(log)
