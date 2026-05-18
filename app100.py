import streamlit as st
from datetime import datetime, timedelta
import random
import pandas as pd

# --- 1. 施設データ（価格高騰版） ---
FACILITIES = {
    "自社ビル": {"cost": 500000000, "id": "f_building", "effect": "家賃無料"},
    "社員研修所": {"cost": 1000000000, "id": "f_training", "effect": "効率+20%"},
    "R&Dセンター": {"cost": 5000000000, "id": "f_rd", "effect": "シェア増"},
    "AIデータセンター": {"cost": 20000000000, "id": "f_data", "effect": "売上+5%"},
    "物流拠点": {"cost": 5000000000, "id": "f_logi", "effect": "コスト減"},
    "海外支社": {"cost": 100000000000, "id": "f_overseas", "effect": "世界進出"},
    "政府交渉窓口": {"cost": 300000000000, "id": "f_gov", "effect": "補助金獲得"},
    "保養所": {"cost": 10000000000, "id": "f_resort", "effect": "離職防止"},
    "サイバー防衛局": {"cost": 500000000000, "id": "f_cyber", "effect": "不祥事防止"},
    "宇宙開発部門": {"cost": 1000000000000, "id": "f_space", "effect": "国家威信UP"},
    "量子計算ラボ": {"cost": 2000000000000, "id": "f_quantum", "effect": "開発爆速"},
    "社員食堂": {"cost": 500000000, "id": "f_cafeteria", "effect": "満足度UP"},
    "自家発電施設": {"cost": 3000000000, "id": "f_power", "effect": "停電耐性"},
    "社内保育園": {"cost": 1000000000, "id": "f_nursery", "effect": "復職率UP"},
    "地下シェルター": {"cost": 1000000000000, "id": "f_shelter", "effect": "災害対策"},
    "特許管理事務所": {"cost": 50000000000, "id": "f_patent", "effect": "不労所得"},
    "巨大展示場": {"cost": 150000000000, "id": "f_expo", "effect": "知名度UP"},
    "社員専用鉄道": {"cost": 800000000000, "id": "f_train", "effect": "遅刻ゼロ"},
    "AI倫理委員会": {"cost": 20000000000, "id": "f_ethics", "effect": "不祥事期間短縮"},
    "超高層タワー": {"cost": 5000000000000, "id": "f_tower", "effect": "世界一の象徴"}
}

# --- 2. セッションステート初期化 ---
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
    st.session_state.price_history = [10000]
    st.session_state.page = "メイン"
    for f in FACILITIES.values(): st.session_state[f["id"]] = False

# 変数欠落の安全対策
if 'price_history' not in st.session_state: st.session_state.price_history = [st.session_state.stock_price]
if 'page' not in st.session_state: st.session_state.page = "メイン"

# --- 3. 共通関数 ---
def add_log(msg):
    st.session_state.logs.insert(0, f"[{st.session_state.date.strftime('%Y/%m')}] {msg}")
    st.session_state.logs = st.session_state.logs[:10]

def get_benefit_multiplier():
    owned = st.session_state.stock_owned
    if owned >= 1000000: return 0.5
    if owned >= 100000:  return 0.7
    if owned >= 10000:   return 0.9
    return 1.0

def run_settlement(months=1):
    for _ in range(months):
        st.session_state.date += timedelta(days=30)
        curr_m = st.session_state.date.month
        
        income = int(st.session_state.staff * 600000 * (1 + st.session_state.share / 100))
        if st.session_state.scandal_timer > 0:
            income //= 10
            st.session_state.scandal_timer -= 2 if st.session_state.get('f_ethics') else 1
            st.session_state.scandal_timer = max(0, st.session_state.scandal_timer)
        
        interest = int(st.session_state.debt * 0.02)
        div = int((st.session_state.stock_owned * st.session_state.stock_price) * 0.005)
        bonus = st.session_state.staff * 1000000 if curr_m == 12 else 0
        st.session_state.money += (income - interest + div - bonus)
        
        st.session_state.last_stock_price = st.session_state.stock_price
        st.session_state.stock_price = max(100, int(st.session_state.stock_price * random.uniform(0.85, 1.15)))
        st.session_state.price_history.append(st.session_state.stock_price)
        if len(st.session_state.price_history) > 24: st.session_state.price_history.pop(0)
        
        res = 0 if curr_m == 1 else (int(st.session_state.staff * 0.08) + 5) if curr_m in [3, 4] else random.randint(1, 3)
        st.session_state.staff = max(1, st.session_state.staff - res + int(res*0.5))

# --- 4. 画面表示とナビゲーション ---
st.title("🏛️ 国家規模経営シミュレーター")
n1, n2 = st.columns(2)
if n1.button("🏢 経営本部 (採用・融資・M&A・施設)", use_container_width=True):
    st.session_state.page = "メイン"
    st.rerun()
if n2.button("📈 証券取引 (チャート・売買・乗っ取り)", use_container_width=True):
    st.session_state.page = "株"
    st.rerun()

st.divider()

# 共通ステータス表示
col_top1, col_top2 = st.columns(2)
with col_top1:
    st.caption("📅 日付")
    st.subheader(st.session_state.date.strftime("%Y年%m月%d日"))
with col_top2:
    st.caption("💰 所持金")
    st.subheader(f"{st.session_state.money / 100000000:.2f} 億円")

# --- 5. ページ切り替え ---

if st.session_state.page == "メイン":
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("従業員", f"{st.session_state.staff:,}名")
    c2.metric("シェア", f"{st.session_state.share:,}%")
    c3.metric("借金", f"{st.session_state.debt / 100000000:.1f}億")
    c4.metric("不祥事", f"{st.session_state.scandal_timer}ヶ月" if st.session_state.scandal_timer > 0 else "なし")

    t1, t2, t3, t4 = st.tabs(["👤 採用", "💰 金融", "🤝 M&A", "🏗️ 施設投資"])
    mult = get_benefit_multiplier()

    with t1:
        if st.session_state.date.month == 4:
            if st.button("🎓 4月限定:新卒200名採用 (2億円)"):
                if st.session_state.money >= 200000000:
                    st.session_state.money -= 200000000; st.session_state.staff += 200
                    if random.randint(1,20000) <= 200: st.session_state.scandal_timer = 120
                    st.rerun()
        u_cost = int((1000000 if st.session_state.share >= 100000000 else 2000000) * mult)
        for n in [1, 10, 50, 100]:
            if st.button(f"{n}人採用 ({u_cost*n/100000000:.3f}億)", key=f"hire_{n}"):
                if st.session_state.money >= u_cost*n:
                    st.session_state.money -= u_cost*n; st.session_state.staff += n; st.rerun()

    with t2:
        if st.button("💵 100億円 融資"): 
            st.session_state.money += 10000000000; st.session_state.debt += 10000000000; st.rerun()
        if st.button("🏦 100億円 返済"):
            amt = min(st.session_state.debt, 10000000000)
            if st.session_state.money >= amt: st.session_state.money -= amt; st.session_state.debt -= amt; st.rerun()

    with t3:
        ma_cost = int(1000000000000 * mult)
        if st.button(f"1兆円規模M&A実行 (実費:{ma_cost/1000000000000:.2f}兆円)"):
            if st.session_state.money >= ma_cost:
                st.session_state.money -= ma_cost; st.session_state.share += 15; st.balloons(); st.rerun()

    with t4:
        cols = st.columns(2)
        for i, (name, info) in enumerate(FACILITIES.items()):
            with cols[i % 2]:
                if not st.session_state.get(info["id"]):
                    c = int(info['cost'] * mult)
                    label = f"{name} ({c/100000000:.0f}億)" if c < 1000000000000 else f"{name} ({c/1000000000000:.1f}兆)"
                    if st.button(label, key=f"btn_{info['id']}"):
                        if st.session_state.money >= c: st.session_state.money -= c; st.session_state[info["id"]] = True; st.rerun()
                else: st.success(f"✅ {name}")

elif st.session_state.page == "株":
    st.subheader("株価トレンド (直近24ヶ月)")
    st.line_chart(pd.DataFrame(st.session_state.price_history, columns=["株価"]))
    
    s1, s2, s3 = st.columns(3)
    diff = st.session_state.stock_price - st.session_state.last_stock_price
    s1.metric("現在株価", f"{st.session_state.stock_price:,}円", delta=f"{(diff/st.session_state.last_stock_price*100):.1f}%")
    s2.metric("保有数", f"{st.session_state.stock_owned:,}株")
    s3.metric("月間配当", f"{int(st.session_state.stock_owned * st.session_state.stock_price * 0.005):,}円")

    c1, c2 = st.columns(2)
    if c1.button("1000株 購入"):
        cost = st.session_state.stock_price * 1000
        if st.session_state.money >= cost: st.session_state.money -= cost; st.session_state.stock_owned += 1000; st.rerun()
    if c2.button("1000株 売却"):
        if st.session_state.stock_owned >= 1000:
            st.session_state.money += st.session_state.stock_price * 1000; st.session_state.stock_owned -= 1000; st.rerun()
    
    st.divider()
    if st.button("💥 敵対的買収 (10万株を消費してシェア+25%)"):
        if st.session_state.stock_owned >= 100000:
            st.session_state.stock_owned -= 100000; st.session_state.share += 25; st.balloons(); st.rerun()

# --- 6. 共通下部操作 ---
st.write("---")
sk1, sk2 = st.columns(2)
if sk1.button("⏩ 翌月スキップ", use_container_width=True): run_settlement(1); st.rerun()
if sk2.button("📅 1年一括スキップ", use_container_width=True): run_settlement(12); st.rerun()

st.subheader("📜 経営ログ")
for log in st.session_state.logs: st.caption(log)
