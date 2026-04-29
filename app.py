import streamlit as st

st.set_page_config(page_title="Margecalculator PM", page_icon="📊")
st.title("📊 PM Margecalculator")

tab1, tab2, tab3 = st.tabs(["Scenario 1: Totalen", "Scenario 2: Per woord", "Scenario 3: Target Marge"])

# --- SCENARIO 1 ---
with tab1:
    st.header("Scenario 1: Totale Verkoop- en Inkoopprijs")
    verkoop = st.number_input("Totale verkoopprijs (€):", min_value=0.0, value=0.0, step=10.0, key="s1_v")
    inkoop = st.number_input("Totale inkoopprijs (€):", min_value=0.0, value=0.0, step=10.0, key="s1_i")
    extra = st.number_input("Extra kosten (DTP etc.) (€):", min_value=0.0, value=0.0, step=5.0, key="s1_e")
    
    # Berekening
    totaal_kost = inkoop + extra
    winst = verkoop - totaal_kost
    markup = (winst / totaal_kost * 100) if totaal_kost > 0 else 0
    
    st.divider()
    col1, col2, col3 = st.columns(3)
    col1.metric("Totale kostprijs", f"€ {totaal_kost:.2f}")
    col2.metric("Winst", f"€ {winst:.2f}")
    col3.metric("Marge (Markup) %", f"{markup:.2f}%")

# --- SCENARIO 2 ---
with tab2:
    st.header("Scenario 2: Prijs per woord en aantal woorden")
    # Aantal woorden bovenaan zoals gevraagd
    woorden = st.number_input("Aantal woorden:", min_value=0, value=0, step=100, key="s2_a")
    
    c1, c2 = st.columns(2)
    with c1:
        verkoop_w = st.number_input("Verkoopprijs per woord incl. revisie (€):", format="%.4f", value=0.0000)
        inkoop_w = st.number_input("Inkoopprijs per woord excl. revisie (€):", format="%.4f", value=0.0000)
    with c2:
        revisie_w = st.number_input("Inkoopprijs revisie per woord (€):", format="%.4f", value=0.0200)
        extra_2 = st.number_input("Extra kosten (€):", min_value=0.0, value=0.0, key="s2_e")
    
    # Berekening
    tot_verkoop = woorden * verkoop_w
    tot_inkoop_zonder_extra = woorden * (inkoop_w + revisie_w)
    tot_inkoop_totaal = tot_inkoop_zonder_extra + extra_2
    winst_2 = tot_verkoop - tot_inkoop_totaal
    markup_2 = (winst_2 / tot_inkoop_totaal * 100) if tot_inkoop_totaal > 0 else 0
    
    st.divider()
    res1, res2, res3 = st.columns(3)
    res1.write(f"**Totale verkoop:** € {tot_verkoop:.2f}")
    res2.write(f"**Totale inkoop:** € {tot_inkoop_totaal:.2f}")
    res3.metric("Marge (Markup)", f"{markup_2:.2f}%", delta=f"€ {winst_2:.2f} winst")

# --- SCENARIO 3 ---
with tab3:
    st.header("Scenario 3: Minimale marge en max inkoopprijs")
    # Aantal woorden bovenaan zoals gevraagd
    aantal_3 = st.number_input("Aantal woorden:", min_value=0, value=0, key="s3_a")
    
    c3, c4 = st.columns(2)
    with c3:
        v_woord_3 = st.number_input("Verkoopprijs per woord incl. revisie (€):", format="%.4f", value=0.0000, key="s3_v")
        extra_3 = st.number_input("Extra kosten (€):", min_value=0.0, value=0.0, key="s3_e")
    with c4:
        target_3 = st.number_input("Gewenste minimale marge (%):", value=0.0, key="s3_t")
        revisie_inkoop = st.number_input("Vaste inkoopprijs revisie per woord (€):", format="%.4f", value=0.0200, key="s3_r")

    # Logica exact uit Excel:
    tot_verkoop_3 = aantal_3 * v_woord_3
    # Max kostprijs incl. extra kosten (€) = Verkoop / (1 + Marge%)
    max_kost_incl_extra = tot_verkoop_3 / (1 + (target_3 / 100)) if target_3 > -100 else 0
    # Max inkoopprijs excl. extra kosten (€)
    max_inkoop_excl_extra = max_kost_incl_extra - extra_3
    # Max inkoopprijs per woord inclusief revisie (€)
    max_p_w_incl = max_inkoop_excl_extra / aantal_3 if aantal_3 > 0 else 0
    # Max inkoopprijs per woord exclusief revisie (€)
    max_p_w_excl = max_p_w_incl - revisie_inkoop
    
    st.divider()
    st.write(f"**Totale verkoopprijs:** € {tot_verkoop_3:.2f}")
    
    col_a, col_b = st.columns(2)
    col_a.success(f"**Max inkoop per woord (incl. rev):**\n\n€ {max_p_w_incl:.4f}")
    col_b.success(f"**Max inkoop per woord (excl. rev):**\n\n€ {max_p_w_excl:.4f}")
    
    st.info(f"Totaal budget voor freelancer (excl. extra kosten): € {max_inkoop_excl_extra:.2f}")
