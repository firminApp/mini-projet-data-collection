"""
Page de scraping interactif
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys
import os

# Ajouter le dossier parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.scraper import (
    scrape_voitures_brut,
    scrape_motos_brut,
    scrape_locations_brut,
    get_total_pages,
    clean_dataframe
)


def show():
    st.header("🔍 Scraping de Données")
    st.markdown("Scrapez des données depuis dakar-auto.com sur plusieurs pages")
    st.markdown("---")
    
    # Sélection de la catégorie
    col1, col2 = st.columns([2, 1])
    
    with col1:
        category = st.selectbox(
            "📂 Choisissez une catégorie:",
            ["🚗 Voitures", "🏍️ Motos", "🚙 Locations de voitures"]
        )
    
    # Configuration des URLs
    urls = {
        "🚗 Voitures": "https://dakar-auto.com/senegal/voitures-4",
        "🏍️ Motos": "https://dakar-auto.com/senegal/motos-and-scooters-3",
        "🚙 Locations de voitures": "https://dakar-auto.com/senegal/location-de-voitures-19"
    }
    
    url = urls[category]
    
    # Options de scraping
    st.markdown("### ⚙️ Options de scraping")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        detect_pages = st.checkbox("Détecter automatiquement le nombre de pages", value=True)
    
    with col2:
        if detect_pages:
            if st.button("🔍 Détecter les pages"):
                with st.spinner("Détection en cours..."):
                    total_pages = get_total_pages(url)
                    st.session_state['total_pages'] = total_pages
                    st.success(f"✅ {total_pages} pages détectées!")
        else:
            max_pages = st.number_input(
                "Nombre de pages à scraper:",
                min_value=1,
                max_value=3000,
                value=5,
                step=1
            )
            st.session_state['max_pages'] = max_pages
    
    with col3:
        clean_data = st.checkbox("Nettoyer les données après scraping", value=False)
    
    # Afficher les informations
    if 'total_pages' in st.session_state and detect_pages:
        st.info(f"📊 Nombre total de pages détectées: **{st.session_state['total_pages']}**")
    
    st.markdown("---")
    
    # Bouton de scraping
    if st.button("🚀 Lancer le scraping", type="primary", use_container_width=True):
        
        # Déterminer le nombre de pages
        if detect_pages and 'total_pages' in st.session_state:
            num_pages = st.session_state['total_pages']
        elif not detect_pages and 'max_pages' in st.session_state:
            num_pages = st.session_state['max_pages']
        else:
            st.error("⚠️ Veuillez d'abord détecter le nombre de pages ou spécifier un nombre.")
            return
        
        # Container pour les logs
        log_container = st.empty()
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        logs = []
        
        def log_callback(message):
            logs.append(message)
            log_container.text_area("📋 Logs:", "\n".join(logs), height=200)
        
        # Scraping selon la catégorie
        try:
            status_text.text(f"⏳ Scraping en cours... (0/{num_pages} pages)")
            
            if category == "🚗 Voitures":
                data = scrape_voitures_brut(url, num_pages, log_callback)
                df = pd.DataFrame(data)
                category_name = "voitures"
                
            elif category == "🏍️ Motos":
                data = scrape_motos_brut(url, num_pages, log_callback)
                df = pd.DataFrame(data)
                category_name = "motos"
                
            else:  # Locations
                data = scrape_locations_brut(url, num_pages, log_callback)
                df = pd.DataFrame(data)
                category_name = "locations"
            
            progress_bar.progress(100)
            status_text.text(f"✅ Scraping terminé! ({num_pages} pages)")
            
            # Nettoyage optionnel
            if clean_data:
                with st.spinner("Nettoyage des données..."):
                    df = clean_dataframe(df, category_name)
                    st.success("✅ Données nettoyées!")
            
            # Stocker dans session state
            st.session_state['scraped_data'] = df
            st.session_state['category_name'] = category_name
            st.session_state['is_cleaned'] = clean_data
            
            st.success(f"🎉 Scraping terminé avec succès! {len(df)} articles récupérés.")
            
        except Exception as e:
            st.error(f"❌ Erreur lors du scraping: {e}")
            progress_bar.empty()
            status_text.empty()
    
    # Affichage des résultats
    if 'scraped_data' in st.session_state:
        st.markdown("---")
        st.markdown("### 📊 Résultats du scraping")
        
        df = st.session_state['scraped_data']
        category_name = st.session_state['category_name']
        is_cleaned = st.session_state.get('is_cleaned', False)
        
        # Statistiques
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📄 Lignes", len(df))
        
        with col2:
            st.metric("📋 Colonnes", len(df.columns))
        
        with col3:
            missing = df.isnull().sum().sum()
            st.metric("⚠️ Valeurs manquantes", missing)
        
        with col4:
            duplicates = df.duplicated().sum()
            st.metric("🔄 Doublons", duplicates)
        
        # Aperçu des données
        st.markdown("#### Aperçu des données")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Informations sur les colonnes
        with st.expander("ℹ️ Informations sur les colonnes"):
            st.write(df.dtypes)
            if not df.empty and len(df.columns) > 0:
                st.write(df.describe())
            else:
                st.warning("⚠️ Le DataFrame est vide, aucune statistique à afficher.")
        
        # Options de sauvegarde
        st.markdown("---")
        st.markdown("### 💾 Sauvegarder les données")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Téléchargement direct
            suffix = "_nettoyees" if is_cleaned else "_brutes"
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 Télécharger CSV",
                data=csv,
                file_name=f"{category_name}{suffix}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            # Sauvegarde locale
            if st.button("💾 Sauvegarder localement", use_container_width=True):
                output_dir = Path("data_dakar_auto_brutes") if not is_cleaned else Path("data_dakar_auto")
                output_dir.mkdir(exist_ok=True)
                
                filename = output_dir / f"{category_name}{suffix}.csv"
                df.to_csv(filename, index=False, encoding='utf-8-sig')
                st.success(f"✅ Données sauvegardées dans: {filename}")
