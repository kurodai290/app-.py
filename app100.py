# --- 3. 決算（修正版） ---
def run_settlement(months=1):
    m_profit = 0
    for _ in range(months):
        st.session_state.date += timedelta(days=30)
        curr_m = st.session_state.date.month
        
        # 収支計算
        inc = int(st.session_state.staff * 600000 * (1 + st.session_state.share / 100))
        if st.session_state.scandal_timer > 0:
            inc //= 10
            st.session_state.scandal_timer -= (3 if st.session_state.get('f_AI倫理委員会') else 1)
        
        bonus = st.session_state.staff * 1000000 if curr_m == 12 else 0
        div = int((st.session_state.stock_owned * st.session_state.stock_price) * 0.005)
        m_profit += (inc - int(st.session_state.debt * 0.02) + div - bonus)
        
        # 株価変動（ここを少し強化）
        # 前回の価格を保持
        st.session_state.last_stock_price = st.session_state.stock_price
        change = random.uniform(0.8, 1.2) # 変動幅を±20%に拡大
        st.session_state.stock_price = max(100, int(st.session_state.stock_price * change))
        
        # 履歴を保存（60個 = 5年分に増加）
        st.session_state.price_history.append(st.session_state.stock_price)
        if len(st.session_state.price_history) > 60: 
            st.session_state.price_history.pop(0)

        # 人員
        res = 0 if curr_m == 1 else (int(st.session_state.staff * 0.08) + 5) if curr_m in [3,4] else random.randint(1, 3)
        st.session_state.staff = max(1, st.session_state.staff - res + int(res*0.5))

    st.session_state.money += m_profit
    add_log(f"決算完了: {months}ヶ月分")

# --- 株ページの描画部分（修正版） ---
elif st.session_state.page == "株":
    # グラフをPandasのDataFrameとして明示的に作成
    df = pd.DataFrame(st.session_state.price_history, columns=["株価"])
    st.line_chart(df) # これで安定して動きます
    
    s1, s2 = st.columns(2)
    # 前月比のデルタ（矢印）も表示
    diff = st.session_state.stock_price - st.session_state.get('last_stock_price', 10000)
    s1.metric("現在の株価", f"{st.session_state.stock_price:,}円", delta=f"{diff:,}円")
    s2.metric("総保有数", f"{st.session_state.stock_owned:,}株")
