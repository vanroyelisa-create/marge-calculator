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

# --- SCENARIO 2 (De tabel uit je screenshot) ---
with tab2:
    st.header("Scenario 2: Prijs per woord")
    
    # Invoer
    woorden = st.number_input("Aantal woorden:", min_value=0, value=1000, step=1)
    
    col1, col2 = st.columns(2)
    with col1:
        verkoop_w = st.number_input("Verkoopprijs p.w. incl. revisie (€):", format="%.4f", value=0.2250)
        inkoop_w = st.number_input("Inkoopprijs p.w. excl. revisie (€):", format="%.4f", value=0.1000)
    with col2:
        revisie_w = st.number_input("Inkoopprijs revisie p.w. (€):", format="%.4f", value=0.0200)
        extra_kosten = st.number_input("Extra kosten (€):", min_value=0.0, value=0.00, format="%.2f")

    # BEREKENINGEN (Gecorrigeerd naar Winst/Verkoop)
    tot_verkoop = woorden * verkoop_w
    tot_inkoop = (woorden * (inkoop_w + revisie_w)) + extra_kosten
    winst = tot_verkoop - tot_inkoop
    
    # DE CRUCIALE FORMULE VOOR 47%: Winst / Verkoop
    marge_procent = (winst / tot_verkoop * 100) if tot_verkoop > 0 else 0
    
    st.divider()
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Totale Verkoop", f"€ {tot_verkoop:.2f}")
    c2.metric("Totale Inkoop", f"€ {tot_inkoop:.2f}")
    c3.metric("Marge (%)", f"{marge_procent:.2f}%")

    st.write(f"**Winst op dit project:** € {winst:.2f}")

# --- SCENARIO 3 (Terugrekenen op basis van Winst/Verkoop) ---
with tab3:
    st.header("Scenario 3: Target Marge")
    v_w_3 = st.number_input("Verkoopprijs p.w. (€):", format="%.4f", value=0.2250, key="v3")
    a_3 = st.number_input("Aantal woorden:", value=1000, key="a3")
    t_3 = st.number_input("Gewenste minimale marge (%):", value=47.00, key="t3")
    e_3 = st.number_input("Extra kosten (€):", value=0.0, key="e3")
    r_3 = st.number_input("Inkoop revisie p.w. (€):", value=0.0200, format="%.4f", key="r3")
    
    # Formule voor Inkoop bij Profit Margin: Inkoop = Verkoop * (1 - Marge)
    t_v = a_3 * v_w_3
    max_inkoop_budget = t_v * (1 - (t_3 / 100))
    max_p_w_incl = (max_inkoop_budget - e_3) / a_3 if a_3 > 0 else 0
    max_p_w_excl = max_p_w_incl - r_3
    
    st.divider()
    st.success(f"Om {t_3}% marge te halen mag de inkoopprijs per woord max. **€ {max_p_w_excl:.4f}** zijn.")
    st.info(f"Totaal inkoopbudget (excl. extra kosten): € {max_inkoop_budget - e_3:.2f}")
