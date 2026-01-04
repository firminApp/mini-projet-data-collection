"""
Page de téléchargement des données
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import os


def show():
    st.header("📥 Téléchargement de Données")
    st.markdown("Téléchargez les données déjà scrapées (non nettoyées)")
    st.markdown("---")
    
    # Vérifier les dossiers de données
    data_dir_brut = Path("data_dakar_auto_brutes")
    data_dir_clean = Path("data_dakar_auto")
    
    # Créer les dossiers s'ils n'existent pas
    data_dir_brut.mkdir(exist_ok=True)
    data_dir_clean.mkdir(exist_ok=True)
    
    # Onglets pour données brutes et nettoyées
    tab1, tab2 = st.tabs(["📦 Données Brutes", "✨ Données Nettoyées"])
    
    # TAB 1: Données brutes
    with tab1:
        st.markdown("### 📦 Données brutes (non nettoyées)")
        st.info("Ces données n'ont subi aucun traitement et contiennent les valeurs exactes extraites du site.")
        
        # Lister les fichiers disponibles
        files_brut = list(data_dir_brut.glob("*.csv"))
        
        if not files_brut:
            st.warning("⚠️ Aucun fichier de données brutes disponible.")
            st.info("💡 Utilisez la page 'Scraping' pour générer des données.")
        else:
            st.success(f"✅ {len(files_brut)} fichier(s) disponible(s)")
            
            # Afficher chaque fichier
            for file_path in sorted(files_brut):
                with st.expander(f"📄 {file_path.name}"):
                    try:
                        df = pd.read_csv(file_path, encoding='utf-8-sig')
                        
                        # Statistiques
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Lignes", len(df))
                        with col2:
                            st.metric("Colonnes", len(df.columns))
                        with col3:
                            file_size = file_path.stat().st_size / 1024  # KB
                            st.metric("Taille", f"{file_size:.1f} KB")
                        
                        # Aperçu
                        st.markdown("**Aperçu:**")
                        st.dataframe(df.head(5), use_container_width=True)
                        
                        # Bouton de téléchargement
                        csv_data = df.to_csv(index=False, encoding='utf-8-sig')
                        st.download_button(
                            label="📥 Télécharger ce fichier",
                            data=csv_data,
                            file_name=file_path.name,
                            mime="text/csv",
                            key=f"download_brut_{file_path.name}"
                        )
                        
                    except Exception as e:
                        st.error(f"❌ Erreur de lecture: {e}")
            
            # Téléchargement groupé
            st.markdown("---")
            if st.button("📥 Télécharger tous les fichiers bruts (ZIP)", use_container_width=True):
                import zipfile
                import io
                
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for file_path in files_brut:
                        zip_file.write(file_path, file_path.name)
                
                st.download_button(
                    label="💾 Télécharger le ZIP",
                    data=zip_buffer.getvalue(),
                    file_name="dakar_auto_donnees_brutes.zip",
                    mime="application/zip"
                )
    
    # TAB 2: Données nettoyées
    with tab2:
        st.markdown("### ✨ Données nettoyées")
        st.info("Ces données ont été nettoyées et formatées pour une meilleure utilisation.")
        
        # Lister les fichiers disponibles
        files_clean = list(data_dir_clean.glob("*.csv"))
        
        if not files_clean:
            st.warning("⚠️ Aucun fichier de données nettoyées disponible.")
            st.info("💡 Utilisez la page 'Scraping' avec l'option 'Nettoyer les données' activée.")
        else:
            st.success(f"✅ {len(files_clean)} fichier(s) disponible(s)")
            
            # Afficher chaque fichier
            for file_path in sorted(files_clean):
                with st.expander(f"📄 {file_path.name}"):
                    try:
                        df = pd.read_csv(file_path, encoding='utf-8-sig')
                        
                        # Statistiques
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Lignes", len(df))
                        with col2:
                            st.metric("Colonnes", len(df.columns))
                        with col3:
                            file_size = file_path.stat().st_size / 1024  # KB
                            st.metric("Taille", f"{file_size:.1f} KB")
                        
                        # Aperçu
                        st.markdown("**Aperçu:**")
                        st.dataframe(df.head(5), use_container_width=True)
                        
                        # Bouton de téléchargement
                        csv_data = df.to_csv(index=False, encoding='utf-8-sig')
                        st.download_button(
                            label="📥 Télécharger ce fichier",
                            data=csv_data,
                            file_name=file_path.name,
                            mime="text/csv",
                            key=f"download_clean_{file_path.name}"
                        )
                        
                    except Exception as e:
                        st.error(f"❌ Erreur de lecture: {e}")
            
            # Téléchargement groupé
            st.markdown("---")
            if st.button("📥 Télécharger tous les fichiers nettoyés (ZIP)", use_container_width=True):
                import zipfile
                import io
                
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for file_path in files_clean:
                        zip_file.write(file_path, file_path.name)
                
                st.download_button(
                    label="💾 Télécharger le ZIP",
                    data=zip_buffer.getvalue(),
                    file_name="dakar_auto_donnees_nettoyees.zip",
                    mime="application/zip"
                )
    
    # Section d'aide
    st.markdown("---")
    with st.expander("ℹ️ Aide - Différence entre données brutes et nettoyées"):
        st.markdown("""
        ### Données Brutes 📦
        - Valeurs exactes extraites du site web
        - Peuvent contenir des espaces, symboles, texte mixte
        - Exemple de prix: "3 000 000 FCFA" ou "Prix sur demande"
        - Idéal pour: archivage, analyse textuelle, vérification
        
        ### Données Nettoyées ✨
        - Valeurs formatées et standardisées
        - Nombres extraits et convertis en valeurs numériques
        - Colonnes supplémentaires (prix_numerique, km_numerique, etc.)
        - Idéal pour: analyse statistique, visualisations, machine learning
        
        ### Recommandation 💡
        - Utilisez les **données brutes** si vous voulez conserver l'intégralité des informations
        - Utilisez les **données nettoyées** pour des analyses et visualisations
        """)
