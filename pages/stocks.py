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
with col1:
    if st.button("1000株 購入"):
        cost = st.session_state.stock_price * 1000
        if st.session_state.money >= cost:
            st.session_state.money -= cost
            st.session_state.stock_owned += 1000
            st.success("購入完了")
            st.rerun()

with col2:
    if st.button("1000株 売却"):
        if st.session_state.stock_owned >= 1000:
            st.session_state.money += st.session_state.stock_price * 1000
            st.session_state.stock_owned -= 1000
            st.rerun()

st.divider()
st.subheader("💥 敵対的買収 (TOB)")
if st.button("10万株を消費して市場を乗っ取る"):
    if st.session_state.stock_owned >= 100000:
        st.session_state.stock_owned -= 100000
        st.session_state.share += 25
        st.balloons()
        st.rerun()
