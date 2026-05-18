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
    st.session_state.stock_owned = 0
    st.session_state.is_cleared = False 
    st.session_state.logs = []
    for f in FACILITIES.values():
        st.session_state[f["id"]] = False

def add_log(msg):
    st.session_state.logs.insert(0, f"[{st.session_state.date.strftime('%Y/%m')}] {msg}")
    st.session_state.logs = st.session_state.logs[:10]

def get_benefit_multiplier():
    owned = st.session_state.stock_owned
    if owned >= 1000000: return 0.5
    if owned >= 100000:  return 0.7
    if owned >= 10000:   return 0.9
    return 1.0

# --- 3. 決算処理 ---
def run_settlement(months=1):
    total_income = 0
    total_interest = 0
    total_dividend = 0
    total_bonus = 0
    res_total = 0
    mid_total = 0
    
    for _ in range(months):
        st.session_state.date += timedelta(days=30)
        current_month = st.session_state.date.month
        
        income = int(st.session_state.staff * 600000 * (1 + st.session_state.share / 100))
        interest = int(st.session_state.debt * 0.02)
        dividend = int((st.session_state.stock_owned * st.session_state.stock_price) * 0.005)
        
        bonus = 0
        if current_month == 12:
            bonus = st.session_state.staff * 1000000 
            total_bonus += bonus
        
        st.session_state.money += (income - interest + dividend - bonus)
        total_income += income
        total_interest += interest
        total_dividend += dividend
        st.session_state.stock_price = int(st.session_state.stock_price * random.uniform(0.85, 1.15))
        
        if current_month == 1:
            res = 0
        elif current_month in [3, 4]:
            base_res_rate = 0.08 if not st.session_state.get('f_resort') else 0.03
            res = int(st.session_state.staff * base_res_rate) + random.randint(5, 15)
        else:
            res = random.randint(1, 2) if st.session_state.staff > 5 else 0
            
        mid = int(res * 0.5)
        st.session_state.staff = max(1, st.session_state.staff - res + mid)
        res_total += res
        mid_total += mid
        
    net_profit = total_income - total_interest + total_dividend - total_bonus
    add_log(f"💰決算完了: 純利益 {net_profit:,}円")
    if total_bonus > 0:
        add_log(f"🎁12月ボーナス総額: {total_bonus:,}円を支給")

# --- 4. ヘッダー表示 ---
if st.session_state.share >= 100000000 and not st.session_state.is_cleared:
    st.balloons(); st.snow(); st.session_state.is_cleared = True

st.title("🏛️ 国家規模経営シミュレーター")

multiplier = get_benefit_multiplier()
if multiplier < 1.0:
    st.success(f"💎 株主優待発動中：全コスト {int((1-multiplier)*100)}% 割引！")

# 【修正箇所】一行目：日付と「株の保有数・現在値」
col_top1, col_top2 = st.columns(2)
with col_top1:
    st.caption("📅 日付")
    st.subheader(st.session_state.date.strftime("%Y年%m月%d日"))
with col_top2:
    st.caption("📈 株式情報")
    # 保有数と現在の価格を並べて表示
    st.subheader(f"{st.session_state.stock_owned:,} 株 (現在値: {st.session_state.stock_price:,}円)")

# 二行目：主要スコア
col1, col2, col3, col4 = st.columns(4)
col1.metric("現預金", f"{st.session_state.money / 100000000:.1f}億円")
col2.metric("借金", f"{st.session_state.debt / 100000000:.1f}億円")
col3.metric("シェア", f"{st.session_state.share:,}%")
col4.metric("従業員", f"{st.session_state.staff:,}名")

st.divider()

# --- 5. タブ ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["👤 採用", "💰 金融", "📈 証券", "🤝 M&A", "🏗️ 施設"])

with tab1:
    is_april = st.session_state.date.month == 4
    if is_april:
        st.warning("🌸 4月限定：新卒一括採用イベント実施中！")
        fresh_cost = 200000000 
        if st.button(f"🎓 新卒一括採用 (200名 / {fresh_cost/100000000:.1f}億円)"):
            if st.session_state.money >= fresh_cost:
                st.session_state.money -= fresh_cost
                st.session_state.staff += 200
                add_log("🌸 新卒採用: 200名入社"); st.balloons(); st.rerun()
        st.divider()

    st.subheader("中途採用センター")
    base_unit = 1000000 if st.session_state.is_cleared else 2000000
    unit = int(base_unit * multiplier)
    c_h1, c_h2 = st.columns(2)
    for i, n in enumerate([1, 10, 50, 100]):
        col = c_h1 if i % 2 == 0 else c_h2
        if col.button(f"{n}人採用 ({unit*n/100000000:.3f}億)", key=f"h_{n}"):
            if st.session_state.money >= unit * n:
                st.session_state.money -= unit * n; st.session_state.staff += n; add_log(f"採用: {n}名雇用"); st.rerun()

with tab2:
    st.subheader("金融")
    c_f1, c_f2 = st.columns(2)
    with c_f1:
        if st.button("💵 100億円 融資"):
            st.session_state.money += 10000000000; st.session_state.debt += 10000000000; add_log("融資: 100億"); st.rerun()
    with c_f2:
        if st.button("🏦 100億円 返済"):
            amt = min(st.session_state.debt, 10000000000)
            if st.session_state.money >= amt:
                st.session_state.money -= amt; st.session_state.debt -= amt; add_log("返済: 100億"); st.rerun()

with tab3:
    st.subheader("証券取引センター")
    total_val = st.session_state.stock_owned * st.session_state.stock_price
    st.info(f"評価額合計: {total_val:,}円 / 配当金予想: {int(total_val*0.005):,}円/月")
    c_s1, c_s2 = st.columns(2)
    with c_s1:
        if st.button("1000株購入"):
            cost = st.session_state.stock_price * 1000
            if st.session_state.money >= cost:
                st.session_state.money -= cost; st.session_state.stock_owned += 1000; add_log("証券: 1000株購入"); st.rerun()
    with c_s2:
        if st.button("1000株売却"):
            if st.session_state.stock_owned >= 1000:
                st.session_state.money += st.session_state.stock_price * 1000; st.session_state.stock_owned -= 1000; add_log("証券: 1000株売却"); st.rerun()

with tab4:
    ma_val = 10 if st.session_state.is_cleared else 1
    actual_cost = int(ma_val * 1000000000000 * multiplier)
    if st.button(f"{ma_val}兆円規模M&A実行"):
        if st.session_state.money >= actual_cost:
            st.session_state.money -= actual_cost; st.session_state.share += (15 * ma_val); add_log("M&A成功"); st.balloons(); st.rerun()

with tab5:
    cols = st.columns(2)
    for i, (name, info) in enumerate(FACILITIES.items()):
        with cols[i % 2]:
            if not st.session_state[info["id"]]:
                d_cost = int(info['cost'] * multiplier)
                cost_t = f"{d_cost/100000000:.0f}億" if d_cost < 1000000000000 else f"{d_cost/1000000000000:.1f}兆"
                if st.button(f"{name} ({cost_t})", key=f"btn_{info['id']}"):
                    if st.session_state.money >= d_cost:
                        st.session_state.money -= d_cost; st.session_state[info["id"]] = True; add_log(f"建設: {name}"); st.rerun()
            else:
                st.success(f"✅ {name}")

# --- 7. 下部操作 ---
st.write("---")
c_sk1, c_sk2 = st.columns(2)
with c_sk1:
    if st.button("⏩ 翌月スキップ", use_container_width=True): run_settlement(1); st.rerun()
with c_sk2:
    if st.button("📅 1年一括スキップ", use_container_width=True): run_settlement(12); st.rerun()

st.subheader("📜 経営ログ")
for log in st.session_state.logs:
    st.caption(log)
