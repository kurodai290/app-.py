import streamlit as st
from datetime import datetime, timedelta

# --- 1. 施設データ（20種類に増量！） ---
FACILITIES = {
    "自社ビル": {"cost": 100000000, "id": "f_building", "effect": "家賃無料"},
    "社員研修所": {"cost": 100000000, "id": "f_training", "effect": "効率+20%"},
    "R&Dセンター": {"cost": 500000000, "id": "f_rd", "effect": "シェア増"},
    "AIデータセンター": {"cost": 2000000000, "id": "f_data", "effect": "売上+5%"},
    "物流拠点": {"cost": 1500000000, "id": "f_logi", "effect": "コスト減"},
    "海外支社": {"cost": 5000000000, "id": "f_overseas", "effect": "世界進出"},
    "政府交渉窓口": {"cost": 1000000000, "id": "f_gov", "effect": "補助金獲得"},
    "保養所": {"cost": 50000000, "id": "f_resort", "effect": "離職防止"},
    "サイバー防衛局": {"cost": 3000000000, "id": "f_cyber", "effect": "不祥事防止"},
    "宇宙開発部門": {"cost": 10000000000, "id": "f_space", "effect": "国家威信UP"},
    "量子計算ラボ": {"cost": 8000000000, "id": "f_quantum", "effect": "開発爆速"},
    "社員食堂": {"cost": 30000000, "id": "f_cafeteria", "effect": "満足度UP"},
    "自家発電施設": {"cost": 200000000, "id": "f_power", "effect": "停電耐性"},
    "社内保育園": {"cost": 70000000, "id": "f_nursery", "effect": "復職率UP"},
    "地下シェルター": {"cost": 5000000000, "id": "f_shelter", "effect": "災害対策"},
    "特許管理事務所": {"cost": 300000000, "id": "f_patent", "effect": "不労所得"},
    "巨大展示場": {"cost": 2500000000, "id": "f_expo", "effect": "知名度UP"},
    "社員専用鉄道": {"cost": 6000000000, "id": "f_train", "effect": "遅刻ゼロ"},
    "AI倫理委員会": {"cost": 150000000, "id": "f_ethics", "effect": "炎上防止"},
    "超高層タワー": {"cost": 50000000000, "id": "f_tower", "effect": "世界一の象徴"}
}

# --- 2. セッションステート初期化 ---
if 'money' not in st.session_state:
    st.session_state.money = 1970000000 
    st.session_state.debt = 0
    st.session_state.share = 1
    st.session_state.staff = 121
    st.session_state.timer = 75
    st.session_state.date = datetime(2052, 4, 3)
    # 施設保有フラグ（ボタンのkeyと被らないよう prefix を外す）
    for f in FACILITIES.values():
        st.session_state[f["id"]] = False

# --- 3. 関数：決算処理 ---
def next_month():
    st.session_state.date += timedelta(days=30)
    income = int(st.session_state.staff * 600000 * (1 + st.session_state.share / 100))
    st.session_state.money += income
    st.session_state.timer = 75
    st.toast(f"【決算報告】{income:,}円の利益が出ました！")

# --- 4. ヘッダー表示 ---
st.title("🏛️ 国家規模経営シミュレーター")

col_h1, col_h2 = st.columns(2)
with col_h1:
    st.caption("📅 日付")
    st.subheader(st.session_state.date.strftime("%Y年%m月%d日"))
with col_h2:
    st.caption("⏳ 決算まで")
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
        st.rerun()

with tab2:
    if st.button("国家融資 (10億円)"):
        st.session_state.money += 1000000000
        st.session_state.debt += 1000000000
        st.rerun()

with tab3:
    st.info("競合他社の買収案件をリストアップ中...")

with tab4:
    st.subheader("🏗️ インフラ整備（全20施設）")
    # 2列でスクロールせず見やすく配置
    cols = st.columns(2)
    for i, (name, info) in enumerate(FACILITIES.items()):
        with cols[i % 2]:
            if not st.session_state[info["id"]]:
                # key を 'btn_' + id にすることで重複エラーを回避
                if st.button(f"{name} ({info['cost']/100000000:.1f}億)", key=f"btn_{info['id']}"):
                    if st.session_state.money >= info["cost"]:
                        st.session_state.money -= info["cost"]
                        st.session_state[info["id"]] = True
                        st.rerun()
                    else:
                        st.error("資金が不足しています")
            else:
                st.success(f"✅ {name} ({info['effect']})")

# --- 6. 画面下部：スキップボタン ---
st.write("---")
if st.button("⏩ 翌月までスキップ"):
    next_month()
    st.rerun()
