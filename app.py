# =========================================================
# 1️⃣ IMPORTS
# =========================================================
import streamlit as st
import os
import re
import pandas as pd
from collections import Counter


# =========================================================
# 2️⃣ CONFIGURATION APP
# =========================================================
APP_TITLE = os.getenv("APP_TITLE", "Analyseur de Texte IA")
APP_VERSION = os.getenv("APP_VERSION", "2.0.0")

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🧠",
    layout="centered"
)


# =========================================================
# 3️⃣ SESSION STATE (mémoire de l'application)
# =========================================================
if "historique" not in st.session_state:
    st.session_state.historique = []

if "scores" not in st.session_state:
    st.session_state.scores = []


# =========================================================
# 4️⃣ FONCTIONS UTILITAIRES
# =========================================================
def analyser_texte(texte):

    mots = re.findall(r"\b\w+\b", texte.lower())

    phrases = [
        s.strip() for s in re.split(r"[.!?]", texte)
        if s.strip()
    ]

    freq = Counter(mots)

    stats = {
        "caracteres": len(texte),
        "nb_mots": len(mots),
        "phrases": len(phrases),
        "mots_uniques": len(set(mots)),
        "frequence": freq,
        "mots": mots
    }

    return stats


# =========================================================
# 5️⃣ INTERFACE
# =========================================================
st.title(f"🧠 {APP_TITLE}")
st.caption(f"Version {APP_VERSION} — Application IA avec Streamlit")

st.divider()

texte = st.text_area(
    "Entrez votre texte :",
    placeholder="Tapez ou collez un texte...",
    height=200
)


# =========================================================
# 6️⃣ ANALYSE
# =========================================================
if st.button("Analyser le texte", type="primary"):

    if texte:

        stats = analyser_texte(texte)

        st.divider()

        # KPIs
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Caractères", stats["caracteres"])
        col2.metric("Mots", stats["nb_mots"])
        col3.metric("Phrases", stats["phrases"])
        col4.metric("Mots uniques", stats["mots_uniques"])

        # Temps de lecture
        temps_lecture = round(stats["nb_mots"] / 200, 2)

        st.metric(
            "Temps de lecture estimé",
            f"{temps_lecture} min",
            help="Basé sur 200 mots/minute"
        )

        st.divider()

        # =================================================
        # Mots fréquents
        # =================================================
        st.subheader("📊 Mots les plus fréquents")

        top10 = stats["frequence"].most_common(10)

        mots_label = [m for m, _ in top10]
        mots_count = [c for _, c in top10]

        df = pd.DataFrame({
            "Mot": mots_label,
            "Frequence": mots_count
        })

        st.bar_chart(df.set_index("Mot"))

        # =================================================
        # Densité lexicale
        # =================================================
        densite = (
            len(set(stats["mots"])) / len(stats["mots"]) * 100
            if stats["mots"] else 0
        )

        st.metric(
            "Densité lexicale",
            f"{densite:.1f}%"
        )

        # =================================================
        # HISTORIQUE
        # =================================================
        st.session_state.historique.append({
            "caracteres": stats["caracteres"],
            "mots": stats["nb_mots"],
            "phrases": stats["phrases"],
            "densite": densite
        })

        st.session_state.scores.append(stats["nb_mots"])


# =========================================================
# 7️⃣ HISTORIQUE DES ANALYSES
# =========================================================
if st.session_state.historique:

    st.divider()
    st.subheader("📜 Historique des analyses")

    df_hist = pd.DataFrame(st.session_state.historique)

    st.dataframe(df_hist)

    # =====================================================
    # Graphique évolution
    # =====================================================
    st.subheader("📈 Evolution du nombre de mots")

    st.line_chart(st.session_state.scores)

    # =====================================================
    # Export CSV
    # =====================================================
    csv = df_hist.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Télécharger historique CSV",
        data=csv,
        file_name="historique_analyse.csv",
        mime="text/csv"
    )


# =========================================================
# 8️⃣ FOOTER
# =========================================================
st.divider()
st.caption("Projet IA — Analyse de Texte avec Streamlit")