"""
Application Streamlit pour le scraping et l'analyse de dakar-auto.com
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import os

# Configuration de la page
st.set_page_config(
    page_title="Dakar Auto Scraper",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"

)

# Titre principal
st.title("🚗 Dakar Auto - Scraping & Analytics")
st.subheader("TP Mini-Projet Data Collection realisé par Kpapou BANIGANTE [Linkdin](https://www.linkedin.com/in/kpapou-banigante-023988121/)")
st.markdown("---")

# Sidebar pour la navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choisissez une page:",
    ["🏠 Accueil", "🔍 Scraping", "📥 Téléchargement", "📊 Dashboard", "📝 Évaluation"]
)

# Page d'accueil
if page == "🏠 Accueil":
    # st.header("Bienvenue sur l'application Dakar Auto Scraper")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("### 🔍 Scraping\nScrapez des données sur plusieurs pages de dakar-auto.com")
    
    with col2:
        st.info("### 📥 Téléchargement\nTéléchargez les données déjà scrapées (brutes)")
    
    with col3:
        st.info("### 📊 Dashboard\nVisualisez les données nettoyées")
    
    st.markdown("---")
    st.success("### 📝 Évaluation\nVotre avis nous intéresse! N'oubliez pas d'évaluer l'application.")
    
    st.markdown("---")
    st.markdown("""
    ### Fonctionnalités:
    - ✅ Scraping interactif avec sélection du nombre de pages
    - ✅ Téléchargement des données brutes (CSV)
    - ✅ Dashboard interactif avec visualisations
    - ✅ Formulaire d'évaluation de l'application
    
    ### Sources de données:
    - 🚗 Voitures: https://www.dakar-auto.com/senegal/voitures-4
    - 🏍️ Motos: https://www.dakar-auto.com/senegal/motos-and-scooters-3
    - 🚙 Locations: https://www.dakar-auto.com/senegal/location-de-voitures-19
    """)

# Import des autres pages (à créer)
elif page == "🔍 Scraping":
    from modules import scraping
    scraping.show()

elif page == "📥 Téléchargement":
    from modules import download
    download.show()

elif page == "📊 Dashboard":
    from modules import dashboard
    dashboard.show()

elif page == "📝 Évaluation":
    from modules import evaluation
    evaluation.show()
