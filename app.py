import streamlit as st
import pandas as pd

st.set_page_config(page_title="Aandelen Kwaliteitsanalyse", layout="wide")

st.title("📊 Aandelen Kwaliteitsanalyse")
st.caption("Objectieve kwaliteitsbeoordeling volgens vast model")

# -------------------------------
# 1. Bedrijfsinfo
# -------------------------------
st.header("1️⃣ Bedrijfsinformatie")
company = st.text_input("Bedrijfsnaam")
ticker = st.text_input("Ticker / Symbool")
sector = st.text_input("Sector")

# -------------------------------
# 2. Kwalitatieve beoordeling
# -------------------------------
st.header("2️⃣ Kwalitatieve beoordeling (0–5)")
st.caption("Geef per criterium een score én korte onderbouwing")

qual_criteria = [
    "Begrijpelijkheid businessmodel",
    "Geografische spreiding & klantenbasis",
    "Structurele groei",
    "Duurzaam competitief voordeel (moat)",
    "Prijszettingsmacht",
    "Marktpositie",
    "Managementkwaliteit",
    "Recessiebestendigheid",
    "Disruptierisico"
]

qual_scores = {}
qual_notes = {}

for c in qual_criteria:
    col1, col2 = st.columns([1, 3])
    with col1:
        qual_scores[c] = st.slider(c, 0, 5, 3)
    with col2:
        qual_notes[c] = st.text_input(f"Onderbouwing – {c}")

# -------------------------------
# 3. Kwantitatieve beoordeling
# -------------------------------
st.header("3️⃣ Kwantitatieve beoordeling (0–5)")
st.caption("Onderbouw met cijfers / ratios")

quant_criteria = [
    "Langjarig omzet- & winsttrackrecord",
    "Omzet → vrije kasstroom conversie",
    "ROIC (kapitaalrendement)",
    "Schuldpositie & balanskwaliteit"
]

quant_scores = {}
quant_notes = {}

for c in quant_criteria:
    col1, col2 = st.columns([1, 3])
    with col1:
        quant_scores[c] = st.slider(c, 0, 5, 3)
    with col2:
        quant_notes[c] = st.text_input(f"Data-onderbouwing – {c}")

# -------------------------------
# 4. Berekeningen
# -------------------------------
qual_total = sum(qual_scores.values())
quant_total = sum(quant_scores.values())

quality_score = (
    0.6 * (qual_total / 45)
    + 0.4 * (quant_total / 20)
) * 100

# Classificatie
if quality_score >= 85:
    classification = "🌟 Compounder‑waardig"
elif quality_score >= 75:
    classification = "✅ Hoge kwaliteit"
elif quality_score >= 65:
    classification = "⚠️ Goede kwaliteit"
elif quality_score >= 50:
    classification = "❌ Matige kwaliteit"
else:
    classification = "🚫 Lage kwaliteit"

# -------------------------------
# 5. Resultaten
# -------------------------------
st.header("4️⃣ Resultaten")

st.metric("Kwaliteitscore (0–100)", f"{quality_score:.1f}")
st.subheader(f"Classificatie: {classification}")

# Overzichtstabel
st.subheader("📋 Overzichtstabel")

table_data = []
for c in qual_criteria:
    table_data.append(["Kwalitatief", c, qual_scores[c], qual_notes[c]])

for c in quant_criteria:
    table_data.append(["Kwantitatief", c, quant_scores[c], quant_notes[c]])

df = pd.DataFrame(
    table_data,
    columns=["Categorie", "Criterium", "Score (0–5)", "Onderbouwing"]
)

st.dataframe(df, use_container_width=True)

# -------------------------------
# 6. Analyse
# -------------------------------
st.subheader("🔍 Analyse")

strengths = [c for c, s in qual_scores.items() if s >= 4]
weaknesses = [c for c, s in qual_scores.items() if s <= 2]

st.write("**Sterktes:**")
st.write(", ".join(strengths) if strengths else "Geen uitgesproken sterktes")

st.write("**Zwaktes / risico's:**")
st.write(", ".join(weaknesses) if weaknesses else "Geen grote zwaktes")

st.write("**Recessierisico:**")
st.write(
    "Beperkt" if qual_scores["Recessiebestendigheid"] >= 4
    else "Aanwezig"
)

st.write("**Geschikt voor lange termijn?**")
st.write("✅ Ja" if quality_score >= 75 else "⚠️ Alleen selectief")
