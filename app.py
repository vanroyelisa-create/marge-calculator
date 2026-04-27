import streamlit as st

# Pagina configuratie
st.set_page_config(page_title="Margecalculator PM", page_icon="📊")

st.title("📊 Margecalculator voor Projectmanagers")
st.write("Gebruik deze tool om snel marges te berekenen of de maximale inkoopprijs te bepalen.")

# Tabs voor de verschillende scenario's (net als in je Excel)
tab1, tab2, tab3 = st.tabs(["Scenario 1: Totalen", "Scenario 2: Per woord", "Scenario 3: Target Marge"])

with tab1:
    st.header("Berekening op basis van totalen")
    verkoop = st.number_input("Totale verkoopprijs (€)", min_value=0.0, value=0.0, step=10.0, key="s1_v")
    inkoop = st.number_input("Totale inkoopprijs (€)", min_value=0.0, value=0.0, step=10.0, key="s1_i")
    extra = st.number_input("Extra kosten (DTP etc.) (€)", min_value=0.0, value=0.0, step=5.0, key="s1_e")
    
    totaal_kost = inkoop + extra
    winst = verkoop - totaal_kost
    marge = (winst / verkoop * 100) if verkoop > 0 else 0
    
    col1, col2 = st.columns(2)
    col1.metric("Winst", f"€ {winst:.2f}")
    col2.metric("Marge %", f"{marge:.2f}%")
    
    if marge < 20 and verkoop > 0:
        st.warning("Let op: De marge is lager dan 20%!")
    elif marge >= 35:
        st.success("Goede marge!")

with tab2:
    st.header("Berekening op basis van woordprijs")
    woorden = st.number_input("Aantal woorden", min_value=0, value=0, step=100)
    inkoop_w = st.number_input("Inkoopprijs per woord excl. revisie (€)", format="%.4f", value=0.0000)
    revisie_w = st.number_input("Inkoopprijs revisie per woord (€)", format="%.4f", value=0.0200)
    verkoop_w = st.number_input("Verkoopprijs per woord incl. revisie (€)", format="%.4f", value=0.0000)
    extra_2 = st.number_input("Extra kosten (€)", min_value=0.0, value=0.0, key="s2_e")
    
    tot_verkoop = woorden * verkoop_w
    tot_inkoop = (woorden * (inkoop_w + revisie_w)) + extra_2
    winst_2 = tot_verkoop - tot_inkoop
    marge_2 = (winst_2 / tot_verkoop * 100) if tot_verkoop > 0 else 0
    
    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.write(f"**Totaal Verkoop:** € {tot_verkoop:.2f}")
    c2.write(f"**Totaal Inkoop:** € {tot_inkoop:.2f}")
    c3.metric("Marge", f"{marge_2:.2f}%", delta=f"€ {winst_2:.2f}")

with tab3:
    st.header("Target Marge (Terugrekenen)")
    st.info("Bereken de maximale prijs die je aan een freelancer kunt bieden.")
    
    v_woord = st.number_input("Verkoopprijs per woord (€)", format="%.4f", value=0.1500, key="s3_v")
    aantal = st.number_input("Aantal woorden", min_value=0, value=1000, key="s3_a")
    extra_3 = st.number_input("Extra projectkosten (€)", min_value=0.0, value=0.0, key="s3_e")
    target = st.slider("Gewenste minimale marge (%)", 0, 100, 30)
    
    totaal_v = v_woord * aantal
    # Max kosten om target te halen: Verkoop * (1 - marge)
    max_totale_kosten = totaal_v * (1 - (target / 100))
    max_inkoop_budget = max_totale_kosten - extra_3
    max_per_woord = max_inkoop_budget / aantal if aantal > 0 else 0
    
    st.success(f"**Maximale inkoopprijs per woord:** € {max_per_woord:.4f}")
    st.write(f"Bij deze inkoop maak je exact {target}% marge.")
