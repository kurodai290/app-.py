import streamlit as st
import pandas as pd

# 共通データの確認（エラー防止）
if 'money' not in st.session_state:
    st.error("メインページを先に開いてください")
    st.stop()

# 安全対策：historyが空、または数値以外が入っている場合の初期化
if 'price_history' not in st.session_state or not isinstance(st.session_state.price_history, list):
    st.session_state.price_history = [st.session_state.stock_price]

st.header("📈 証券取引・市場チャート")

# --- 1. 株価チャートの描画 ---
# データが1つしかない場合でも動くようにする
df = pd.DataFrame(st.session_state.price_history, columns=["株価"])
st.line_chart(df)

# --- 2. ステータス表示（画像のデザインを再現） ---
col_stat1, col_stat2 = st.columns(2)
with col_stat1:
    st.write("株価")
    st.subheader(f"{st.session_state.stock_price:,}円")
    # 前月比の表示（もしあれば）
    if 'last_stock_price' in st.session_state:
        diff = st.session_state.stock_price - st.session_state.last_stock_price
        color = "green" if diff >= 0 else "red"
        st.write(f":{color}[↑ {diff:,}円]" if diff >= 0 else f":{color}[↓ {abs(diff):,}円]")

with col_stat2:
    st.write("保有株")
    st.subheader(f"{st.session_state.stock_owned:,}株")

st.divider()

# --- 3. 売買ボタン（ここが修正の肝です！） ---
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    if st.button("🛒 1万株購入", use_container_width=True, key="buy_10000"):
        cost = st.session_state.stock_price * 10000
        if st.session_state.money >= cost:
            st.session_state.money -= cost
            st.session_state.stock_owned += 10000
            st.success(f"{cost/100000000:.1f}億円で購入しました")
            st.rerun()
        else:
            st.error("資金が足りません")

with col_btn2:
    # 画像で足りなかった「売却」ボタンを追加！
    if st.button("💰 1万株売却", use_container_width=True, key="sell_10000"):
        if st.session_state.stock_owned >= 10000:
            gain = st.session_state.stock_price * 10000
            st.session_state.money += gain
            st.session_state.stock_owned -= 10000
            st.success(f"{gain/100000000:.1f}億円で売却しました")
            st.rerun()
        else:
            st.error("売却できる株を持っていません")

st.divider()

# --- 4. 銀河進出プロジェクト（画像の下部） ---
st.subheader("🌌 銀河進出プロジェクト")
# （ここに以前のGALAXY_INVのループ処理を入れる）
if 'GALAXY_INV' in globals() or 'GALAXY_INV' in locals():
    for name, info in GALAXY_INV.items():
        if not st.session_state.get(f"g_{name}"):
            if st.button(f"{name} ({info['cost']/1e12:.0f}兆円)", key=f"gal_{name}"):
                if st.session_state.money >= info['cost']:
                    st.session_state.money -= info['cost']
                    st.session_state.share += info['share']
                    st.session_state[f"g_{name}"] = True
                    st.balloons()
                    st.rerun()
        else:
            st.success(f"🌌 {name} 完了")
