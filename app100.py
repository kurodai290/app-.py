import streamlit as st
from datetime import datetime, timedelta

# --- 1. 施設データ（全10種類に拡充） ---
FACILITIES = {
    "自社ビル": {"cost": 100000000, "id": "has_building", "effect": "家賃無料"},
    "社員研修所": {"cost": 100000000, "id": "has_training", "effect": "効率+20%"},
    "R&Dセンター": {"cost": 500000000, "id": "has_rd", "effect": "シェア増"},
    "AIデータセンター": {"cost": 2000000000, "id": "has_data", "effect": "売上+5%"},
    "物流拠点": {"cost": 1500000000, "id": "has_logi", "effect": "コスト減"},
    "海外支社": {"cost": 5000000000, "id": "has_overseas", "effect": "世界進出"},
    "政府交渉窓口": {"cost": 1000000000, "id": "has_gov", "effect": "補助金"},
    "保養所": {"cost": 50000000, "id": "has_resort", "effect": "離職防止"},
    "サイバー防衛局": {"cost": 3000000000, "id": "has_cyber", "effect": "不祥事防止"},
    "宇宙開発部門": {"cost": 10000000000, "id": "has_space", "effect": "国家威信UP"}
}

# --- 2. セッションステート初期化 ---
if 'money' not in st.session_state:
    st.session_state.money = 1970000000 
    st.session_state.debt = 0
    st.session_state.share = 1
    st.session_state.staff = 121
    st.session_state.timer = 75
    st.session_state.date = datetime(2052, 4, 3)
    for f in FACILITIES.values():
        st.session_state[f["id"]] = False

# --- 3. 関数：決算処理（翌月へ） ---
def next_month():
    # 日付更新
    st.session_state.date += timedelta(days=30)
    # 売上・支出計算（簡易版）
    income = int(st.session_state.staff * 500000 * (1 + st.session_state.share / 100))
    st.session_state.money += income
    # タイマーリセット
    st.session_state.timer = 75
    st.toast(f"{income:,}円の利益を計上しました！")

# --- 4. ヘッダー表示（画像のデザインを再現） ---
st.title("🏛️ 国家規模経営シミュレーター")

col_h1, col_h2 = st.columns(2)
with col_h1:
    st.caption("📅 日付")
    st.subheader(st.session_state.date.strftime("%Y年%m月%d日"))
with col_h2:
    st.caption("⏳ 決算まで")
    # ここでは表示のみにし、ボタン操作で動くようにして安定化
    st.subheader(f"{st.session_state.timer}秒")

col1, col2, col3, col4 = st.columns(4)
col1.metric("現預金", f"{st.session_state.money / 100000000:.1f}億円")
col2.metric("借金", f"{st.session_state.debt / 100000000:.1f}億円")
col3.metric("シェア", f"{st.session_state.share}%")
col4.metric("従業員", f"{st.session_state.staff}名")

st.divider()

# --- 5. タブ ---
tab1, tab2, tab3, tab4 = st.tabs(["採用・広報", "巨大融資", "1兆円M&A", "施設投資"])

with tab1:
    if st.button("精鋭を採用 (1,000万円)"):
        st.session_state.money -= 10000000
        st.session_state.staff += 5

with tab2:
    if st.button("国家融資 (10億円)"):
        st.session_state.money += 1000000000
        st.session_state.debt += 1000000000

with tab3:
    st.write("1兆円規模の案件を精査中...")

with tab4:
    st.subheader("🏗️ インフラ整備（全10施設）")
    cols = st.columns(2)
    for i, (name, info) in enumerate(FACILITIES.items()):
        with cols[i % 2]:
            if not st.session_state[info["id"]]:
                if st.button(f"{name} ({info['cost']/100000000:.1f}億)", key=info["id"]):
                    if st.session_state.money >= info["cost"]:
                        st.session_state.money -= info["cost"]
                        st.session_state[info["id"]] = True
                        st.rerun()
            else:
                st.success(f"✅ {name} ({info['effect']})")

# --- 6. スキップボタン ---
st.write("---")
if st.button("⏩ 翌月までスキップ"):
    next_month()
    st.rerun()
