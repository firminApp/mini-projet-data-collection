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
    
    # Onglets pour données brutes, nettoyées et upload
    tab1, tab2, tab3 = st.tabs(["📦 Données Brutes", "✨ Données Nettoyées", "⬆️ Uploader CSV"])
    
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
    
    # TAB 3: Upload de fichiers CSV
    with tab3:
        st.markdown("### ⬆️ Uploader vos données CSV")
        st.info("Uploadez des fichiers CSV scrapés avec Web Scraper ou d'autres outils. Les fichiers seront stockés dans le dossier 'scraped'.")
        
        # Créer le dossier scraped
        scraped_dir = Path("scraped")
        scraped_dir.mkdir(exist_ok=True)
        
        # Deux colonnes: Upload et Fichiers existants
        col_upload, col_existing = st.columns([1, 1])
        
        with col_upload:
            st.markdown("#### 📤 Uploader nouveaux fichiers")
            # Zone d'upload
            uploaded_files = st.file_uploader(
                "Choisissez un ou plusieurs fichiers CSV",
                type=['csv'],
                accept_multiple_files=True,
                help="Vous pouvez uploader plusieurs fichiers CSV à la fois"
            )
            
            if uploaded_files:
                st.success(f"✅ {len(uploaded_files)} fichier(s) uploadé(s)")
                
                # Afficher et traiter chaque fichier
                for uploaded_file in uploaded_files:
                    with st.expander(f"📄 {uploaded_file.name}", expanded=False):
                        try:
                            # Lire le fichier
                            df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
                            
                            # Sauvegarder automatiquement le fichier dans le dossier scraped
                            save_path = scraped_dir / uploaded_file.name
                            df.to_csv(save_path, index=False, encoding='utf-8-sig')
                            
                            # Statistiques
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Lignes", len(df))
                            with col2:
                                st.metric("Colonnes", len(df.columns))
                            with col3:
                                st.metric("Taille", f"{save_path.stat().st_size / 1024:.1f} KB")
                            
                            # Aperçu des données
                            st.markdown("**Aperçu:**")
                            st.dataframe(df.head(3), use_container_width=True)
                            
                            st.success(f"💾 Sauvegardé: {save_path}")
                            
                        except Exception as e:
                            st.error(f"❌ Erreur: {e}")
                
                st.info("🔄 Rafraîchissez la page pour voir les fichiers dans la section 'Fichiers stockés'")
        
        with col_existing:
            st.markdown("#### 📁 Fichiers stockés")
            # Lister les fichiers dans le dossier scraped
            scraped_files = list(scraped_dir.glob("*.csv"))
            
            if scraped_files:
                st.success(f"✅ {len(scraped_files)} fichier(s) disponible(s)")
                
                # Sélection multiple des fichiers
                selected_files = st.multiselect(
                    "Sélectionnez les fichiers:",
                    options=[f.name for f in scraped_files],
                    default=None,
                    help="Sélectionnez pour visualiser, télécharger ou supprimer"
                )
                
                # Boutons d'action groupés
                col_btn1, col_btn2, col_btn3 = st.columns(3)
                
                with col_btn1:
                    # Bouton pour télécharger tous les fichiers en ZIP
                    if st.button("📥 Tout (ZIP)", use_container_width=True, help="Télécharger tous les fichiers"):
                        import zipfile
                        import io
                        
                        zip_buffer = io.BytesIO()
                        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                            for file_path in scraped_files:
                                zip_file.write(file_path, file_path.name)
                        
                        st.download_button(
                            label="💾 ZIP Complet",
                            data=zip_buffer.getvalue(),
                            file_name="scraped_files.zip",
                            mime="application/zip",
                            use_container_width=True
                        )
                
                with col_btn2:
                    # Bouton pour supprimer tous les fichiers
                    if st.button("🗑️ Tout suppr.", use_container_width=True, type="secondary", help="Supprimer tous les fichiers"):
                        if st.session_state.get('confirm_delete_all', False):
                            for file_path in scraped_files:
                                file_path.unlink()
                            st.success(f"✅ {len(scraped_files)} fichier(s) supprimé(s)")
                            st.session_state['confirm_delete_all'] = False
                            st.rerun()
                        else:
                            st.session_state['confirm_delete_all'] = True
                            st.warning("⚠️ Cliquez à nouveau pour confirmer")
                
                with col_btn3:
                    # Reset confirmation
                    if st.session_state.get('confirm_delete_all', False):
                        if st.button("❌ Annuler", use_container_width=True):
                            st.session_state['confirm_delete_all'] = False
                            st.rerun()
                
                # Actions sur les fichiers sélectionnés
                if selected_files:
                    st.markdown("---")
                    col_sel1, col_sel2 = st.columns(2)
                    
                    with col_sel1:
                        if len(selected_files) > 1:
                            # Télécharger les sélectionnés en ZIP
                            if st.button(f"📥 Télécharger {len(selected_files)} sélectionnés (ZIP)", use_container_width=True):
                                import zipfile
                                import io
                                
                                zip_buffer = io.BytesIO()
                                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                                    for file_name in selected_files:
                                        file_path = scraped_dir / file_name
                                        zip_file.write(file_path, file_name)
                                
                                st.download_button(
                                    label="💾 Télécharger ZIP",
                                    data=zip_buffer.getvalue(),
                                    file_name="selected_files.zip",
                                    mime="application/zip",
                                    use_container_width=True
                                )
                    
                    with col_sel2:
                        # Supprimer les fichiers sélectionnés
                        if st.button(f"🗑️ Supprimer {len(selected_files)} sélectionné(s)", use_container_width=True, type="secondary"):
                            if st.session_state.get('confirm_delete_selected', False):
                                for file_name in selected_files:
                                    file_path = scraped_dir / file_name
                                    file_path.unlink()
                                st.success(f"✅ {len(selected_files)} fichier(s) supprimé(s)")
                                st.session_state['confirm_delete_selected'] = False
                                st.rerun()
                            else:
                                st.session_state['confirm_delete_selected'] = True
                                st.warning("⚠️ Cliquez à nouveau pour confirmer la suppression")
            else:
                st.warning("⚠️ Aucun fichier dans le dossier 'scraped'")
                st.info("💡 Uploadez des fichiers pour commencer")
        
        # Affichage détaillé des fichiers sélectionnés
        if scraped_files and selected_files:
            st.markdown("---")
            st.markdown("### 📊 Détails des fichiers sélectionnés")
            
            for file_name in selected_files:
                file_path = scraped_dir / file_name
                with st.expander(f"📄 {file_name}", expanded=False):
                    try:
                        df = pd.read_csv(file_path, encoding='utf-8-sig')
                        
                        # Statistiques
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Lignes", len(df))
                        with col2:
                            st.metric("Colonnes", len(df.columns))
                        with col3:
                            st.metric("Taille", f"{file_path.stat().st_size / 1024:.1f} KB")
                        with col4:
                            st.metric("Valeurs nulles", df.isnull().sum().sum())
                        
                        # Informations sur les colonnes
                        st.markdown("**Colonnes:**")
                        col_info = pd.DataFrame({
                            'Colonne': df.columns,
                            'Type': df.dtypes.astype(str),
                            'Non-null': df.count().values
                        })
                        st.dataframe(col_info, use_container_width=True, height=150)
                        
                        # Aperçu des données
                        st.markdown("**Aperçu (5 premières lignes):**")
                        st.dataframe(df.head(5), use_container_width=True)
                        
                        # Boutons d'action
                        col_btn1, col_btn2 = st.columns(2)
                        
                        with col_btn1:
                            # Téléchargement individuel
                            csv_data = df.to_csv(index=False, encoding='utf-8-sig')
                            st.download_button(
                                label="📥 Télécharger",
                                data=csv_data,
                                file_name=file_name,
                                mime="text/csv",
                                key=f"download_{file_name}",
                                use_container_width=True
                            )
                        
                        with col_btn2:
                            # Bouton de suppression
                            if st.button("🗑️ Supprimer", key=f"delete_{file_name}", use_container_width=True):
                                file_path.unlink()
                                st.success(f"✅ {file_name} supprimé")
                                st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Erreur: {e}")
        
        # Section d'aide
        if not uploaded_files and not scraped_files:
            st.markdown("---")
            st.markdown("""
            ### 💡 Comment utiliser cette section?
            
            **1. Uploader des fichiers:**
            - Cliquez sur "Browse files" ou glissez-déposez vos fichiers CSV
            - Les fichiers seront automatiquement sauvegardés dans le dossier `scraped/`
            
            **2. Gérer les fichiers:**
            - Sélectionnez un ou plusieurs fichiers pour les visualiser
            - Téléchargez tous les fichiers en ZIP d'un seul clic
            - Téléchargez uniquement les fichiers sélectionnés
            - Supprimez les fichiers dont vous n'avez plus besoin
            
            **3. Formats supportés:**
            - CSV avec encodage UTF-8 ou UTF-8-sig
            - Fichiers exportés depuis Web Scraper
            - Tout fichier CSV standard
            """)
    
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
