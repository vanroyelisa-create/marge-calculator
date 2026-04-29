import streamlit as st

st.set_page_config(page_title="Margecalculator PM", page_icon="📊")
st.title("📊 PM Margecalculator")

tab1, tab2, tab3 = st.tabs(["Scenario 1: Totalen", "Scenario 2: Per woord", "Scenario 3: Target Marge"])

with tab1:
    st.header("Berekening op basis van totalen")
    verkoop = st.number_input("Totale verkoopprijs (€)", min_value=0.0, value=180.0, step=10.0, key="s1_v")
    inkoop = st.number_input("Totale inkoopprijs (€)", min_value=0.0, value=120.0, step=10.0, key="s1_i")
    extra = st.number_input("Extra kosten (€)", min_value=0.0, value=0.0, key="s1_e")
    
    totaal_kost = inkoop + extra
    winst = verkoop - totaal_kost
    # Excel Logica: Winst / Inkoop (Markup)
    markup = (winst / totaal_kost * 100) if totaal_kost > 0 else 0
    
    st.metric("Winst", f"€ {winst:.2f}")
    st.metric("Marge (Markup) %", f"{markup:.2f}%")

with tab2:
    st.header("Berekening op basis van woordprijs")
    woorden = st.number_input("Aantal woorden", min_value=0, value=1000)
    inkoop_w = st.number_input("Inkoopprijs per woord excl. revisie (€)", format="%.4f", value=0.1000)
    revisie_w = st.number_input("Inkoopprijs revisie per woord (€)", format="%.4f", value=0.0200)
    verkoop_w = st.number_input("Verkoopprijs per woord incl. revisie (€)", format="%.4f", value=0.1800)
    
    tot_verkoop = woorden * verkoop_w
    tot_inkoop = (woorden * (inkoop_w + revisie_w))
    winst_2 = tot_verkoop - tot_inkoop
    # Excel Logica: Winst / Inkoop
    markup_2 = (winst_2 / tot_inkoop * 100) if tot_inkoop > 0 else 0
    
    st.divider()
    st.metric("Marge (Markup)", f"{markup_2:.2f}%", delta=f"€ {winst_2:.2f} winst")

with tab3:
    st.header("Scenario 3: Target Marge (Terugrekenen)")
    v_woord = st.number_input("Verkoopprijs per woord (€)", format="%.4f", value=0.1800)
    aantal = st.number_input("Aantal woorden", min_value=0, value=1000)
    target_markup = st.number_input("Gewenste marge (Markup) %", value=30.0)
    revisie_i_w = st.number_input("Inkoopprijs revisie per woord (€)", format="%.4f", value=0.0200)

    tot_verkoop = v_woord * aantal
    # Excel Formule voor inkoop: Verkoop / (1 + Marge_decimal)
    max_totale_inkoop = tot_verkoop / (1 + (target_markup / 100))
    max_inkoop_p_w_incl = max_totale_inkoop / aantal if aantal > 0 else 0
    max_inkoop_p_w_excl = max_inkoop_p_w_incl - revisie_i_w
    
    st.success(f"Maximale inkoopprijs per woord (incl. revisie): € {max_inkoop_p_w_incl:.4f}")
    st.info(f"Maximale inkoopprijs per woord (excl. revisie): € {max_inkoop_p_w_excl:.4f}")
