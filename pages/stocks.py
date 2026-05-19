import streamlit as st

# 共通データがsession_stateにあるか確認
if 'money' not in st.session_state:
    st.error("メインページを先に開いてください")
    st.stop()

st.title("📈 証券取引・乗っ取り専用ページ")

# 簡易的なステータス表示
st.write(f"現在の所持金: **{st.session_state.money / 100000000:.2f}億円**")
st.write(f"現在の株価: **{st.session_state.stock_price:,}円**")
st.write(f"保有株数: **{st.session_state.stock_owned:,}株**")

st.divider()

col1, col2 = st.columns(2)

# --- 株を買うボタン ---
with col1:
    if st.button("🛒 1000株 購入", key="buy_1000"):
        cost = st.session_state.stock_price * 1000
        if st.session_state.money >= cost:
            st.session_state.money -= cost
            st.session_state.stock_owned += 1000
            st.success(f"{cost/100000000:.2f}億円で購入しました")
            st.rerun()
        else:
            st.error("資金が足りません")

# --- 株を売るボタン (修正箇所) ---
with col2:
    if st.button("💰 1000株 売却", key="sell_1000"):
        if st.session_state.stock_owned >= 1000:
            gain = st.session_state.stock_price * 1000
            st.session_state.money += gain
            st.session_state.stock_owned -= 1000
            st.success(f"{gain/100000000:.2f}億円で売却しました")
            st.rerun()
        else:
            st.error("売却できる株を持っていません")

st.divider()

# --- 敵対的買収 ---
st.subheader("💥 敵対的買収 (TOB)")
if st.button("🚀 10万株を消費して乗っ取る", key="tob_action"):
    if st.session_state.stock_owned >= 100000:
        st.session_state.stock_owned -= 100000
        st.session_state.share += 25
        st.balloons()
        st.success("敵対的買収に成功！シェアが25%拡大しました。")
        st.rerun()
    else:
        st.error(f"あと {100000 - st.session_state.stock_owned:,} 株足りません")
