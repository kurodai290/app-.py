import streamlit as st
import time

# --- 設定：施設リストの拡充 ---
FACILITIES = {
    "自社ビル": {"cost": 100000000, "maintenance": 0, "effect": "家賃無料・信頼度UP", "id": "has_building"},
    "社員研修所": {"cost": 100000000, "maintenance": 2000000, "effect": "社員効率+20%", "id": "has_training_camp"},
    "R&Dセンター": {"cost": 500000000, "maintenance": 10000000, "effect": "毎月シェア+2%", "id": "has_rd_center"},
    "AIデータセンター": {"cost": 2000000000, "maintenance": 50000000, "effect": "売上+5%", "id": "has_data_center"},
    "海外支社": {"cost": 5000000000, "maintenance": 100000000, "effect": "海外シェア獲得", "id": "has_overseas"},
    "物流センター": {"cost": 1500000000, "maintenance": 30000000, "effect": "コスト削減10%", "id": "has_logistics"},
    "保養所": {"cost": 50000000, "maintenance": 1000000, "effect": "離職率低下", "id": "has_resort"},
    "政府交渉窓口": {"cost": 1000000000, "maintenance": 20000000, "effect": "補助金獲得", "id": "has_gov"}
}

# --- セッションステート初期化 ---
if 'money' not in st.session_state:
    st.session_state.money = 1970000000 
    st.session_state.debt = 0
    st.session_state.share = 1
    st.session_state.staff = 121
    st.session_state.timer = 75  # 決算までの秒数
    for f in FACILITIES.values():
        st.session_state[f["id"]] = False

# --- カウントダウン処理 (秒数を動かす) ---
if st.session_state.timer > 0:
    time.sleep(1)
    st.session_state.timer -= 1
    st.rerun()  # 画面を強制更新して秒数を動かす
else:
    # 0秒になったら自動決算
    st.session_state.timer = 75
    st.toast("決算が行われました！")
    # ここに決算処理を入れる

# --- ヘッダー表示 ---
st.title("🏛️ 国家規模経営シミュレーター")

col_h1, col_h2 = st.columns(2)
with col_h1:
    st.caption("📅 日付")
    st.subheader("2052年04月03日")
with col_h2:
    st.caption("⏳ 決算まで")
    st.subheader(f"{st.session_state.timer}秒")

col1, col2, col3, col4 = st.columns(4)
col1.metric("現預金", f"{st.session_state.money / 100000000:.2f}億円")
col2.metric("借金", f"{st.session_state.debt / 100000000:.2f}億円")
col3.metric("シェア", f"{st.session_state.share}%")
col4.metric("従業員", f"{st.session_state.staff}名")

st.divider()

# --- タブ ---
tab1, tab2, tab3, tab4 = st.tabs(["採用・広報", "巨大融資", "1兆円M&A", "施設投資"])

with tab1:
    st.subheader("👤 採用・広報")
    if st.button("大規模求人 (1億円)"):
        st.session_state.money -= 100000000
        st.session_state.staff += 50

with tab2:
    st.subheader("💰 巨大融資")
    if st.button("国家予算級融資 (100億円)"):
        st.session_state.money += 10000000000
        st.session_state.debt += 10000000000

with tab3:
    st.subheader("🤝 巨大M&A")
    st.write("1兆円規模の合併交渉...")

with tab4:
    st.subheader("🏗️ 拠点・インフラ整備（全8施設）")
    # 2列で施設を表示
    cols = st.columns(2)
    for i, (name, info) in enumerate(FACILITIES.items()):
        with cols[i % 2]:
            if not st.session_state[info["id"]]:
                if st.button(f"{name} ({info['cost']/100000000:.1f}億)"):
                    if st.session_state.money >= info["cost"]:
                        st.session_state.money -= info["cost"]
                        st.session_state[info["id"]] = True
                        st.rerun()
                    else:
                        st.error("資金不足")
            else:
                st.success(f"✅ {name} (稼働中)")
            st.caption(f"効果: {info['effect']} / 維持費: {info['maintenance']/10000:,.0f}万")

# --- 下部操作 ---
st.write("---")
if st.button("⏩ 翌月までスキップ"):
    st.session_state.timer = 0 # タイマーを0にして決算を誘発
    st.rerun()
