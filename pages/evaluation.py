"""
Page d'évaluation de l'application
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
import json


def show():
    st.header("📝 Évaluation de l'Application")
    st.markdown("Votre avis nous intéresse! Aidez-nous à améliorer l'application.")
    st.markdown("---")
    
    # Tabs pour les deux options
    tab1, tab2 = st.tabs(["📋 Formulaire Intégré", "🔗 Google Forms"])
    
    # TAB 1: Formulaire intégré
    with tab1:
        st.markdown("### 📋 Évaluation Rapide")
        
        with st.form("evaluation_form"):
            # Informations de base
            col1, col2 = st.columns(2)
            
            with col1:
                nom = st.text_input("Nom (optionnel):", placeholder="Votre nom")
            
            with col2:
                email = st.text_input("Email (optionnel):", placeholder="votre.email@example.com")
            
            st.markdown("---")
            
            # Évaluation générale
            st.markdown("#### 🌟 Évaluation Générale")
            note_generale = st.slider(
                "Note globale de l'application:",
                min_value=1,
                max_value=5,
                value=4,
                help="1 = Très insatisfait, 5 = Très satisfait"
            )
            
            st.markdown("#### 📊 Évaluation par Fonctionnalité")
            
            col1, col2 = st.columns(2)
            
            with col1:
                note_scraping = st.select_slider(
                    "🔍 Module de Scraping:",
                    options=[1, 2, 3, 4, 5],
                    value=4
                )
                
                note_dashboard = st.select_slider(
                    "📊 Dashboard:",
                    options=[1, 2, 3, 4, 5],
                    value=4
                )
            
            with col2:
                note_download = st.select_slider(
                    "📥 Téléchargement:",
                    options=[1, 2, 3, 4, 5],
                    value=4
                )
                
                note_interface = st.select_slider(
                    "🎨 Interface Utilisateur:",
                    options=[1, 2, 3, 4, 5],
                    value=4
                )
            
            st.markdown("---")
            
            # Questions qualitatives
            st.markdown("#### 💭 Vos Commentaires")
            
            points_forts = st.text_area(
                "✅ Points forts de l'application:",
                placeholder="Qu'avez-vous particulièrement apprécié?",
                height=100
            )
            
            points_amelioration = st.text_area(
                "🔧 Points à améliorer:",
                placeholder="Que pourrait-on améliorer?",
                height=100
            )
            
            fonctionnalites_souhaitees = st.text_area(
                "💡 Fonctionnalités souhaitées:",
                placeholder="Quelles nouvelles fonctionnalités aimeriez-vous voir?",
                height=100
            )
            
            st.markdown("---")
            
            # Questions spécifiques
            st.markdown("#### 🎯 Questions Spécifiques")
            
            col1, col2 = st.columns(2)
            
            with col1:
                facilite_utilisation = st.radio(
                    "L'application est-elle facile à utiliser?",
                    ["Très facile", "Facile", "Moyenne", "Difficile", "Très difficile"]
                )
                
                vitesse_scraping = st.radio(
                    "La vitesse de scraping est-elle satisfaisante?",
                    ["Très rapide", "Rapide", "Acceptable", "Lente", "Très lente"]
                )
            
            with col2:
                recommandation = st.radio(
                    "Recommanderiez-vous cette application?",
                    ["Certainement", "Probablement", "Peut-être", "Probablement pas", "Certainement pas"]
                )
                
                frequence_utilisation = st.radio(
                    "À quelle fréquence prévoyez-vous d'utiliser l'app?",
                    ["Quotidiennement", "Hebdomadairement", "Mensuellement", "Rarement", "Une seule fois"]
                )
            
            st.markdown("---")
            
            # Bouton de soumission
            submitted = st.form_submit_button("📤 Envoyer l'évaluation", use_container_width=True, type="primary")
            
            if submitted:
                # Créer un dictionnaire avec toutes les réponses
                evaluation = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "nom": nom if nom else "Anonyme",
                    "email": email if email else "Non fourni",
                    "note_generale": note_generale,
                    "note_scraping": note_scraping,
                    "note_download": note_download,
                    "note_dashboard": note_dashboard,
                    "note_interface": note_interface,
                    "points_forts": points_forts,
                    "points_amelioration": points_amelioration,
                    "fonctionnalites_souhaitees": fonctionnalites_souhaitees,
                    "facilite_utilisation": facilite_utilisation,
                    "vitesse_scraping": vitesse_scraping,
                    "recommandation": recommandation,
                    "frequence_utilisation": frequence_utilisation
                }
                
                # Sauvegarder l'évaluation
                save_evaluation(evaluation)
                
                st.success("✅ Merci pour votre évaluation! Vos retours sont précieux.")
                st.balloons()
    
    # TAB 2: Google Forms
    with tab2:
        st.markdown("### 🔗 Formulaire Google Forms")
        st.info("Pour une évaluation plus détaillée, vous pouvez également remplir notre formulaire Google Forms.")
        
        # URL du formulaire (à personnaliser)
        google_form_url = "https://forms.gle/VOTRE_FORMULAIRE"
        
        st.markdown(f"""
        Cliquez sur le bouton ci-dessous pour accéder au formulaire Google Forms:
        
        [![Ouvrir le formulaire]({create_button_badge()})]({google_form_url})
        """)
        
        # Afficher le formulaire en iframe
        st.markdown("#### Aperçu du formulaire:")
        
        # Note: Remplacez cette URL par l'URL embed de votre Google Form
        iframe_code = f"""
        <iframe 
            src="{google_form_url}" 
            width="100%" 
            height="800" 
            frameborder="0" 
            marginheight="0" 
            marginwidth="0">
            Chargement…
        </iframe>
        """
        
        st.components.v1.html(iframe_code, height=800, scrolling=True)
        
        st.markdown("---")
        st.caption("💡 Astuce: Vous pouvez aussi remplir le formulaire directement sur Google Forms en cliquant sur le lien ci-dessus.")
    
    # Section statistiques des évaluations
    st.markdown("---")
    show_evaluation_stats()


def save_evaluation(evaluation):
    """Sauvegarde une évaluation dans un fichier JSON"""
    
    # Créer le dossier d'évaluations
    eval_dir = Path("evaluations")
    eval_dir.mkdir(exist_ok=True)
    
    # Nom du fichier avec timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = eval_dir / f"evaluation_{timestamp}.json"
    
    # Sauvegarder en JSON
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(evaluation, f, ensure_ascii=False, indent=2)
    
    # Ajouter aussi à un fichier CSV consolidé
    csv_file = eval_dir / "evaluations_consolidated.csv"
    df_eval = pd.DataFrame([evaluation])
    
    if csv_file.exists():
        df_existing = pd.read_csv(csv_file, encoding='utf-8-sig')
        df_combined = pd.concat([df_existing, df_eval], ignore_index=True)
        df_combined.to_csv(csv_file, index=False, encoding='utf-8-sig')
    else:
        df_eval.to_csv(csv_file, index=False, encoding='utf-8-sig')


def show_evaluation_stats():
    """Affiche les statistiques des évaluations"""
    
    eval_dir = Path("evaluations")
    csv_file = eval_dir / "evaluations_consolidated.csv"
    
    if not csv_file.exists():
        st.info("📊 Aucune évaluation enregistrée pour le moment.")
        return
    
    with st.expander("📊 Statistiques des Évaluations"):
        df_evals = pd.read_csv(csv_file, encoding='utf-8-sig')
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📝 Total d'évaluations", len(df_evals))
        
        with col2:
            avg_note = df_evals['note_generale'].mean()
            st.metric("⭐ Note moyenne", f"{avg_note:.1f}/5")
        
        with col3:
            recommandations = df_evals['recommandation'].value_counts()
            if 'Certainement' in recommandations.index or 'Probablement' in recommandations.index:
                positive = recommandations.get('Certainement', 0) + recommandations.get('Probablement', 0)
                pct = (positive / len(df_evals)) * 100
                st.metric("👍 Recommandations", f"{pct:.0f}%")
            else:
                st.metric("👍 Recommandations", "0%")
        
        with col4:
            recent_date = df_evals['timestamp'].max()
            st.metric("🕐 Dernière évaluation", recent_date[:10])
        
        # Graphique des notes
        st.markdown("#### 📊 Distribution des Notes")
        
        notes_cols = ['note_generale', 'note_scraping', 'note_download', 'note_dashboard', 'note_interface']
        notes_labels = ['Générale', 'Scraping', 'Téléchargement', 'Dashboard', 'Interface']
        
        avg_notes = [df_evals[col].mean() for col in notes_cols]
        
        import plotly.graph_objects as go
        
        fig = go.Figure(data=[
            go.Bar(x=notes_labels, y=avg_notes, marker_color='lightblue')
        ])
        fig.update_layout(
            yaxis_range=[0, 5],
            yaxis_title="Note Moyenne",
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)


def create_button_badge():
    """Crée un badge de bouton pour Google Forms"""
    return "https://img.shields.io/badge/Google%20Forms-Ouvrir-4285F4?style=for-the-badge&logo=google&logoColor=white"
