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
    "AI倫理委員会": {"cost": 20000000000, "id": "f_ethics", "effect": "炎上防止"},
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
    st.session_state.scandal_timer = 0  # 不祥事残り月数
    st.session_state.logs = []
    for f in FACILITIES.values():
        st.session_state[f["id"]] = False

def add_log(msg):
    st.session_state.logs.insert(0, f"[{st.session_state.date.strftime('%Y/%m')}] {msg}")
    st.session_state.logs = st.session_state.logs[:10]

# トラブルメーカー判定関数 (20000分の1の確率)
def check_troublemaker(num_hired):
    for _ in range(num_hired):
        if random.randint(1, 20000) == 1:
            return True
    return False

# --- 3. 決算処理 ---
def run_settlement(months=1):
    for _ in range(months):
        st.session_state.date += timedelta(days=30)
        current_month = st.session_state.date.month
        
        # 売上計算
        income = int(st.session_state.staff * 600000 * (1 + st.session_state.share / 100))
        
        # 【不祥事デバフ】収益が1/10に
        if st.session_state.scandal_timer > 0:
            income = int(income / 10)
            st.session_state.scandal_timer -= 1
            if st.session_state.scandal_timer == 0:
                add_log("✅ようやく不祥事の悪評が消え、収益が元に戻りました。")

        interest = int(st.session_state.debt * 0.02)
        dividend = int((st.session_state.stock_owned * st.session_state.stock_price) * 0.005)
        
        bonus = st.session_state.staff * 1000000 if current_month == 12 else 0
        
        st.session_state.money += (income - interest + dividend - bonus)
        
        # 株価
        st.session_state.last_stock_price = st.session_state.stock_price
        st.session_state.stock_price = max(100, int(st.session_state.stock_price * random.uniform(0.85, 1.15)))
        
        # 人員
        if current_month == 1: res = 0
        elif current_month in [3, 4]: res = int(st.session_state.staff * 0.08) + 5
        else: res = random.randint(1, 3)
        st.session_state.staff = max(1, st.session_state.staff - res + int(res*0.5))

    add_log(f"💰決算完了 月数:{months}")

# --- 4. ヘッダー表示 ---
st.title("🏛️ 国家規模経営シミュレーター")

# 不祥事アラート
if st.session_state.scandal_timer > 0:
    st.error(f"🚨【不祥事発生中】トラブルメーカー新人の不祥事により、収益が1/10になっています（残り{st.session_state.scandal_timer}ヶ月）")

col_top1, col_top2 = st.columns(2)
with col_top1:
    st.caption("📅 日付")
    st.subheader(st.session_state.date.strftime("%Y年%m月%d日"))
with col_top2:
    diff = st.session_state.stock_price - st.session_state.last_stock_price
    ratio = (diff / st.session_state.last_stock_price) * 100 if st.session_state.last_stock_price > 0 else 0
    st.metric("📈 現在株価", f"{st.session_state.stock_price:,}円", delta=f"{ratio:.1f}%")

col1, col2, col3, col4 = st.columns(4)
col1.metric("現預金", f"{st.session_state.money / 100000000:.1f}億円")
col2.metric("借金", f"{st.session_state.debt / 100000000:.1f}億円")
col3.metric("保有株", f"{st.session_state.stock_owned:,}株")
col4.metric("従業員", f"{st.session_state.staff:,}名")

st.divider()

# --- 5. タブ ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["👤 採用", "💰 金融", "📈 証券", "🤝 M&A", "🏗️ 施設"])

with tab1:
    # 4月の新卒採用
    if st.session_state.date.month == 4:
        st.warning("🌸 4月限定：新卒採用イベント")
        if st.button("🎓 新卒200名採用 (2億円)"):
            if st.session_state.money >= 200000000:
                st.session_state.money -= 200000000
                st.session_state.staff += 200
                # トラブルメーカー判定
                if check_troublemaker(200):
                    st.session_state.scandal_timer = 120 # 10年分
                    add_log("😱最悪だ！新卒の中にトラブルメーカーが混じっていました。10年間収益が激減します。")
                else:
                    add_log("採用: 新卒200名が入社しました")
                st.rerun()

    st.subheader("中途採用")
    owned = st.session_state.stock_owned
    mult = 0.5 if owned >= 1000000 else 0.7 if owned >= 100000 else 0.9 if owned >= 10000 else 1.0
    unit = int(2000000 * mult)
    
    for n in [1, 10, 50, 100]:
        if st.button(f"{n}人採用 ({unit*n/100000000:.3f}億)", key=f"h_{n}"):
            if st.session_state.money >= unit * n:
                st.session_state.money -= unit * n
                st.session_state.staff += n
                # 中途でもトラブルメーカーが混じる可能性
                if check_troublemaker(n):
                    st.session_state.scandal_timer = 120
                    add_log("😱トラブルメーカーを採用してしまいました！10年間の収益激減が確定しました。")
                else:
                    add_log(f"採用: {n}名雇用")
                st.rerun()

# (その他のタブ:金融、証券、M&A、施設、スキップボタンは以前のロジック通り)
with tab2:
    if st.button("💵 100億円 融資"): st.session_state.money += 10000000000; st.session_state.debt += 10000000000; st.rerun()
    if st.button("🏦 100億円 返済"):
        amt = min(st.session_state.debt, 10000000000)
        if st.session_state.money >= amt: st.session_state.money -= amt; st.session_state.debt -= amt; st.rerun()
with tab3:
    if st.button("1000株購入"):
        if st.session_state.money >= st.session_state.stock_price * 1000:
            st.session_state.money -= st.session_state.stock_price * 1000; st.session_state.stock_owned += 1000; st.rerun()
    if st.button("1000株売却"):
        if st.session_state.stock_owned >= 1000:
            st.session_state.money += st.session_state.stock_price * 1000; st.session_state.stock_owned -= 1000; st.rerun()
with tab4:
    cost = int(1000000000000 * mult)
    if st.button(f"1兆円M&A実行 ({cost/1000000000000:.1f}兆円)"):
        if st.session_state.money >= cost: st.session_state.money -= cost; st.session_state.share += 15; st.balloons(); st.rerun()
with tab5:
    cols = st.columns(2)
    for i, (name, info) in enumerate(FACILITIES.items()):
        with cols[i % 2]:
            if not st.session_state[info["id"]]:
                c = int(info['cost'] * mult)
                if st.button(f"{name} ({c/100000000:.0f}億)", key=f"btn_{info['id']}"):
                    if st.session_state.money >= c: st.session_state.money -= c; st.session_state[info["id"]] = True; st.rerun()
            else: st.success(f"✅ {name}")

st.write("---")
c1, c2 = st.columns(2)
with c1:
    if st.button("⏩ 翌月スキップ", use_container_width=True): run_settlement(1); st.rerun()
with c2:
    if st.button("📅 1年スキップ", use_container_width=True): run_settlement(12); st.rerun()

st.subheader("📜 経営ログ")
for log in st.session_state.logs: st.caption(log)
