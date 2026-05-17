# --- 定数（新しい施設の設定） ---
R_D_CENTER_COST = 500000000        # 5億円：研究開発センター
DATA_CENTER_COST = 2000000000      # 20億円：AIデータセンター
TRAINING_CAMP_COST = 100000000     # 1億円：社員研修所

# --- process_settlement関数の中に追加（維持費と効果の処理） ---
def process_settlement():
    # (既存のコード)
    s = st.session_state.staff
    
    # --- 追加要素：施設によるバフと維持費 ---
    maintenance_fee = 0
    rd_bonus = 1.0
    
    if st.session_state.get('has_rd_center'):
        maintenance_fee += 10000000  # 維持費1000万
        rd_bonus = 1.3               # 広告効果30%アップ（内部フラグ用）
        st.session_state.share += 2  # 毎月シェア+2%
        
    if st.session_state.get('has_data_center'):
        maintenance_fee += 50000000  # 維持費5000万
        # データセンターは売上の5%を追加ボーナス
        
    if st.session_state.get('has_training_camp'):
        maintenance_fee += 2000000   # 維持費200万
        # 研修所があると1人あたりの売上が20%アップ
        s_efficiency = 1.2
    else:
        s_efficiency = 1.0

    # 売上計算の修正（効率化を反映）
    multiplier = 1 + (st.session_state.ma_count * 0.5)
    sales = int(s * 600000 * s_efficiency * (1 + st.session_state.share / 100) * multiplier)
    
    # データセンターボーナス
    if st.session_state.get('has_data_center'):
        sales = int(sales * 1.05)

    # (既存のコスト計算にmaintenance_feeを追加)
    costs = int(s * 450000) + rent_cost + interest + maintenance_fee
    # (以下、既存の処理と同じ)

# --- tab4 (施設投資) の書き換え ---
with tab4:
    st.subheader("拠点・インフラ整備")
    
    col_f1, col_f2 = st.columns(2)
    
    # 1. 自社ビル
    with col_f1:
        if not st.session_state.has_building:
            if st.button(f"🏢 自社ビル (1億)"):
                if st.session_state.money >= BUILDING_COST:
                    st.session_state.money -= BUILDING_COST
                    st.session_state.has_building = True
                    st.rerun()
        else:
            st.success("🏢 自社ビル保有 (家賃0/シェア増)")

    # 2. 研修所
    with col_f2:
        if not st.session_state.get('has_training_camp'):
            if st.button(f"🏫 研修所 (1億)"):
                if st.session_state.money >= TRAINING_CAMP_COST:
                    st.session_state.money -= TRAINING_CAMP_COST
                    st.session_state.has_training_camp = True
                    st.rerun()
        else:
            st.success("🏫 研修所 (社員効率+20%)")

    col_f3, col_f4 = st.columns(2)

    # 3. 研究開発センター
    with col_f3:
        if not st.session_state.get('has_rd_center'):
            if st.button(f"🔬 R&Dセンター (5億)"):
                if st.session_state.money >= R_D_CENTER_COST:
                    st.session_state.money -= R_D_CENTER_COST
                    st.session_state.has_rd_center = True
                    st.rerun()
        else:
            st.success("🔬 R&Dセンター (自動シェア増)")

    # 4. AIデータセンター
    with col_f4:
        if not st.session_state.get('has_data_center'):
            if st.button(f"🛰️ AIデータセンター (20億)"):
                if st.session_state.money >= DATA_CENTER_COST:
                    st.session_state.money -= DATA_CENTER_COST
                    st.session_state.has_data_center = True
                    st.rerun()
        else:
            st.success("🛰️ データセンター (売上+5%)")
