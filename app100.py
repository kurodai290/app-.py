import streamlit as st
from datetime import datetime, timedelta
import random

# --- 1. 施設データ ---
FACILITIES = {
    "自社ビル": {"cost": 500000000, "id": "f_building", "effect": "家賃無料"},
    "社員研修所": {"cost": 1000000000, "id": "f_training", "effect": "効率+20%"},
    "R&Dセンター": {"cost": 5000000000, "id": "f_rd", "effect": "シェア増"},
    "AIデータセンター": {"cost": 20000000000, "id": "f_data", "effect": "売上+5%"},
    "物流拠点": {"cost": 50000000000, "id": "f_logi", "effect": "コスト減"},
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
    "AI倫理委員会": {"cost": 20000000000, "id": "f_ethics", "effect": "不祥事期間短縮"}, # 救済用
    "超高層タワー": {"cost": 5000000000000, "id": "f_tower", "effect": "世界一の象徴"}
}

# --- 2. 初期化 ---
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
    for f in FACILITIES.values(): st.session_state[f["id"]] = False

def add_log(msg):
    st.session_state.logs.insert(0, f"[{st.session_state.date.strftime('%Y/%m')}] {msg}")
    st.session_state.logs = st.session_state.logs[:10]

# --- 3. 決算 & 上昇イベント追加 ---
def run_settlement(months=1):
    for _ in range(months):
        st.session_state.date += timedelta(days=30)
        current_month = st.session_state.date.month
        
        income = int(st.session_state.staff * 600000 * (1 + st.session_state.share / 100))
        if st.session_state.scandal_timer > 0:
            income //= 10
            # AI倫理委員会があれば2ヶ月分進む（実質期間半分）
            st.session_state.scandal_timer -= 2 if st.session_state.get('f_ethics') else 1
            st.session_state.scandal_timer = max(0, st.session_state.scandal_timer)
        
        interest = int(st.session_state.debt * 0.02)
        div = int((st.session_state.stock_owned * st.session_state.stock_price) * 0.005)
        bonus = st.session_state.staff * 1000000 if current_month == 12 else 0
        st.session_state.money += (income - interest + div - bonus)
        
        st.session_state.last_stock_price = st.session_state.stock_price
        st.session_state.stock_price = max(100, int(st.session_state.stock_price * random.uniform(0.85, 1.15)))
        
        # 季節離職
        res = 0 if current_month == 1 else (int(st.session_state.staff * 0.08) + 5) if current_month in [3, 4] else random.randint(1, 3)
        st.session_state.staff = max(1, st.session_state.staff - res + int(res*0.5))

        # 🌟 イベント発生
        ev = random.random()
        if ev < 0.01: # 1%：技術革命
            st.session_state.stock_price *= 3
            add_log("🚀【技術革命】次世代AIの開発に成功！株価が3倍に爆騰！")
        elif ev < 0.03: # 2%：外資買付
            st.session_state.stock_price = int(st.session_state.stock_price * 1.5)
            add_log("🌍【外資参入】海外ファンドが大量買い付け！株価が1.5倍に上昇！")
        elif ev < 0.05: # 2%：インフレ
            st.session_state.stock_price = int(st.session_state.stock_price * 1.2)
            add_log("📈【好景気】市場全体が活況。株価が20%アップ！")
        elif ev < 0.07: # 2%：ショック
            st.session_state.stock_price //= 2
            add_log("📉【経済ショック】市場が冷え込み、株価が半減...")

    add_log(f"決算完了 ({months}ヶ月)")

# --- 4. 画面表示 ---
st.title("🏛️ 国家規模経営シミュレーター")

if st.session_state.scandal_timer > 0:
    st.error(f"🚨【不祥事継続中】残り{st.session_state.scandal_timer}ヶ月")

col_top1, col_top2 = st.columns(2)
with col_top1:
    st.caption("📅 日付")
    st.subheader(st.session_state.date.strftime("%Y年%m月%d日"))
with col_top2:
    div_next = int(st.session_state.stock_owned * st.session_state.stock_price * 0.005)
    st.caption(f"💰 次回配当金")
    st.subheader(f"{div_next:,} 円")

col1, col2, col3, col4 = st.columns(4)
col1.metric("現預金", f"{st.session_state.money / 100000000:.1f}億円")
col2.metric("借金", f"{st.session_state.debt / 100000000:.1f}億円")
col3.metric("現在株価", f"{st.session_state.stock_price:,}円")
col4.metric("保有株数", f"{st.session_state.stock_owned:,}株")

st.divider()

# --- 5. タブ ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["👤 採用", "💰 金融", "📈 証券・乗っ取り", "🤝 M&A", "🏗️ 施設"])

with tab1:
    if st.session_state.date.month == 4:
        if st.button("🎓 新卒200名一括採用 (2億円)"):
            if st.session_state.money >= 200000000:
                st.session_state.money -= 200000000; st.session_state.staff += 200
                if random.randint(1, 20000) <= 200:
                    st.session_state.scandal_timer = 120
                    add_log("😱トラブルメーカー採用！呪いの10年が開始...")
                st.rerun()

with tab3:
    st.subheader("証券取引 & 敵対的買収")
    c_s1, c_s2 = st.columns(2)
    with c_s1:
        if st.button("1000株購入"):
            if st.session_state.money >= st.session_state.stock_price * 1000:
                st.session_state.money -= st.session_state.stock_price * 1000; st.session_state.stock_owned += 1000; st.rerun()
    with c_s2:
        if st.button("1000株売却"):
            if st.session_state.stock_owned >= 1000:
                st.session_state.money += st.session_state.stock_price * 1000; st.session_state.stock_owned -= 1000; st.rerun()
    
    st.divider()
    if st.button(f"💥 敵対的買収 (10万株を消費してシェア+25%)"):
        if st.session_state.stock_owned >= 100000:
            st.session_state.stock_owned -= 100000; st.session_state.share += 25
            add_log("💥【敵対的買収】市場を制圧！シェア大幅獲得。"); st.balloons(); st.rerun()

with tab2:
    if st.button("💵 100億円 融資"): st.session_state.money += 10000000000; st.session_state.debt += 10000000000; st.rerun()
    if st.button("🏦 100億円 返済"):
        amt = min(st.session_state.debt, 10000000000)
        if st.session_state.money >= amt: st.session_state.money -= amt; st.session_state.debt -= amt; st.rerun()
with tab4:
    if st.button(f"1兆円M&A実行"):
        if st.session_state.money >= 1000000000000: st.session_state.money -= 1000000000000; st.session_state.share += 15; st.balloons(); st.rerun()
with tab5:
    cols = st.columns(2)
    for i, (name, info) in enumerate(FACILITIES.items()):
        with cols[i % 2]:
            if not st.session_state[info["id"]]:
                if st.button(f"{name} ({info['cost']/100000000:.0f}億)", key=f"btn_{info['id']}"):
                    if st.session_state.money >= info['cost']: st.session_state.money -= info['cost']; st.session_state[info["id"]] = True; st.rerun()
            else: st.success(f"✅ {name}")

st.write("---")
c1, c2 = st.columns(2)
with c1:
    if st.button("⏩ 翌月スキップ", use_container_width=True): run_settlement(1); st.rerun()
with c2:
    if st.button("📅 1年スキップ", use_container_width=True): run_settlement(12); st.rerun()

st.subheader("📜 経営ログ")
for log in st.session_state.logs: st.caption(log)
