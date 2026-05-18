import streamlit as st
from datetime import datetime, timedelta
import random
import pandas as pd

# --- 1. 施設データ ---
FACILITIES = {
    "自社ビル": {"cost": 500000000, "id": "f_building"},
    "社員研修所": {"cost": 1000000000, "id": "f_training"},
    "R&Dセンター": {"cost": 5000000000, "id": "f_rd"},
    "AIデータセンター": {"cost": 20000000000, "id": "f_data"},
    "海外支社": {"cost": 100000000000, "id": "f_overseas"},
    "サイバー防衛局": {"cost": 500000000000, "id": "f_cyber"},
    "宇宙開発部門": {"cost": 1000000000000, "id": "f_space"},
    "AI倫理委員会": {"cost": 20000000000, "id": "f_ethics"},
    "超高層タワー": {"cost": 5000000000000, "id": "f_tower"}
} # 施設を絞って軽量化（必要なら戻せます）

# --- 2. セッションステート初期化 ---
if 'money' not in st.session_state:
    st.session_state.update({
        'money': 1970000000, 'debt': 0, 'share': 1, 'staff': 121,
        'date': datetime(2052, 4, 3), 'stock_price': 10000,
        'last_stock_price': 10000, 'stock_owned': 0, 'scandal_timer': 0,
        'logs': [], 'price_history': [10000], 'page': "メイン"
    })
    for f in FACILITIES.values(): st.session_state[f["id"]] = False

def add_log(msg):
    st.session_state.logs.insert(0, f"[{st.session_state.date.strftime('%Y/%m')}] {msg}")
    st.session_state.logs = st.session_state.logs[:10]

# --- 3. 決算処理（ループを最小限にして軽量化） ---
def run_settlement(months=1):
    m_inc, m_int, m_div, m_bon, r_tot = 0, 0, 0, 0, 0
    
    for _ in range(months):
        st.session_state.date += timedelta(days=30)
        curr_m = st.session_state.date.month
        
        # 収支
        inc = int(st.session_state.staff * 600000 * (1 + st.session_state.share / 100))
        if st.session_state.scandal_timer > 0:
            inc //= 10
            st.session_state.scandal_timer -= (2 if st.session_state.get('f_ethics') else 1)
        
        # 合算
        m_inc += inc
        m_int += int(st.session_state.debt * 0.02)
        m_div += int((st.session_state.stock_owned * st.session_state.stock_price) * 0.005)
        if curr_m == 12: m_bon += st.session_state.staff * 1000000
        
        # 株価
        st.session_state.last_stock_price = st.session_state.stock_price
        st.session_state.stock_price = max(100, int(st.session_state.stock_price * random.uniform(0.85, 1.15)))
        st.session_state.price_history.append(st.session_state.stock_price)
        
        # 人員
        res = 0 if curr_m == 1 else (int(st.session_state.staff * 0.08) + 5) if curr_m in [3,4] else random.randint(1, 3)
        st.session_state.staff = max(1, st.session_state.staff - res + int(res*0.5))
        r_tot += res

    st.session_state.money += (m_inc - m_int + m_div - m_bon)
    if len(st.session_state.price_history) > 24: st.session_state.price_history = st.session_state.price_history[-24:]
    add_log(f"決算完了: 純利{m_inc-m_int+m_div-m_bon:,}円")

# --- 4. 画面表示 ---
st.title("🏛️ 国家規模経営シミュレーター")
n1, n2 = st.columns(2)
if n1.button("🏢 経営本部", use_container_width=True): st.session_state.page = "メイン"; st.rerun()
if n2.button("📈 証券取引", use_container_width=True): st.session_state.page = "株"; st.rerun()

# 共通ステータス
c_t1, c_t2 = st.columns(2)
c_t1.subheader(st.session_state.date.strftime("%Y年%m月%d日"))
c_t2.subheader(f"💰 {st.session_state.money / 100000000:.1f} 億円")

# --- 5. ページ出し分け ---
if st.session_state.page == "メイン":
    c1, c2, c3 = st.columns(3)
    c1.metric("従業員", f"{st.session_state.staff:,}名")
    c2.metric("シェア", f"{st.session_state.share:,}%")
    c3.metric("不祥事", f"{st.session_state.scandal_timer}月" if st.session_state.scandal_timer > 0 else "なし")

    t1, t2, t3, t4 = st.tabs(["👤 採用", "💰 金融", "🤝 M&A", "🏗️ 施設"])
    owned = st.session_state.stock_owned
    mult = 0.5 if owned >= 1000000 else 0.7 if owned >= 100000 else 0.9 if owned >= 10000 else 1.0

    with t1:
        u_cost = int(2000000 * mult)
        for n in [1, 10, 50, 100]:
            if st.button(f"{n}人採用 ({u_cost*n/100000000:.2f}億)", key=f"h_{n}"):
                if st.session_state.money >= u_cost*n:
                    st.session_state.money -= u_cost*n; st.session_state.staff += n; st.rerun()
    with t2:
        if st.button("💵 100億融資"): st.session_state.money += 10000000000; st.session_state.debt += 10000000000; st.rerun()
        if st.button("🏦 100億返済"):
            amt = min(st.session_state.debt, 10000000000)
            if st.session_state.money >= amt: st.session_state.money -= amt; st.session_state.debt -= amt; st.rerun()
    with t3:
        cost = int(1000000000000 * mult)
        if st.button(f"1兆円M&A (実費:{cost/1000000000000:.2f}兆)"):
            if st.session_state.money >= cost: st.session_state.money -= cost; st.session_state.share += 15; st.balloons(); st.rerun()
    with t4:
        cols = st.columns(2)
        for i, (name, info) in enumerate(FACILITIES.items()):
            with cols[i % 2]:
                if not st.session_state.get(info["id"]):
                    c = int(info['cost'] * mult)
                    if st.button(f"{name} ({c/100000000:.0f}億)", key=f"b_{info['id']}"):
                        if st.session_state.money >= c: st.session_state.money -= c; st.session_state[info["id"]] = True; st.rerun()
                else: st.success(f"✅ {name}")

elif st.session_state.page == "株":
    st.line_chart(pd.DataFrame(st.session_state.price_history, columns=["株価"]))
    s1, s2 = st.columns(2)
    s1.metric("現在株価", f"{st.session_state.stock_price:,}円")
    s2.metric("保有数", f"{st.session_state.stock_owned:,}株")
    if st.button("1000株購入"):
        c = st.session_state.stock_price * 1000
        if st.session_state.money >= c: st.session_state.money -= c; st.session_state.stock_owned += 1000; st.rerun()
    if st.button("1000株売却"):
        if st.session_state.stock_owned >= 1000:
            st.session_state.money += st.session_state.stock_price * 1000; st.session_state.stock_owned -= 1000; st.rerun()

st.write("---")
sk1, sk2 = st.columns(2)
if sk1.button("⏩ 翌月スキップ", use_container_width=True): run_settlement(1); st.rerun()
if sk2.button("📅 1年一括スキップ", use_container_width=True): run_settlement(12); st.rerun()

for log in st.session_state.logs: st.caption(log)
