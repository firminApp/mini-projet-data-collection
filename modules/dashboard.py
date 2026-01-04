"""
Dashboard de visualisation des données
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import numpy as np


def show():
    st.header("📊 Dashboard Analytics")
    st.markdown("Visualisez les données nettoyées de dakar-auto.com")
    st.markdown("---")
    
    # Charger les données nettoyées
    data_dir = Path("data_dakar_auto")
    
    if not data_dir.exists():
        data_dir.mkdir(exist_ok=True)
    
    # Rechercher les fichiers
    files = list(data_dir.glob("*nettoyees.csv")) + list(data_dir.glob("*_nettoyees.csv"))
    
    if not files:
        st.warning("⚠️ Aucune donnée nettoyée disponible pour le dashboard.")
        st.info("💡 Utilisez la page 'Scraping' avec l'option 'Nettoyer les données' pour générer des données.")
        
        # Afficher un dashboard de démonstration
        if st.checkbox("Voir un dashboard de démonstration"):
            show_demo_dashboard()
        return
    
    # Sélection du fichier
    file_options = {f.name: f for f in files}
    selected_file_name = st.selectbox("📂 Sélectionnez un fichier:", list(file_options.keys()))
    selected_file = file_options[selected_file_name]
    
    # Charger les données
    try:
        df = pd.read_csv(selected_file, encoding='utf-8-sig')
        
        # Déterminer le type de données
        if 'voiture' in selected_file_name.lower():
            show_voitures_dashboard(df)
        elif 'moto' in selected_file_name.lower():
            show_motos_dashboard(df)
        elif 'location' in selected_file_name.lower():
            show_locations_dashboard(df)
        else:
            st.error("❌ Type de données non reconnu.")
            
    except Exception as e:
        st.error(f"❌ Erreur de chargement: {e}")


def show_voitures_dashboard(df):
    """Dashboard spécifique pour les voitures"""
    
    st.markdown("### 🚗 Analyse des Voitures")
    
    # Métriques globales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total d'annonces", len(df))
    
    with col2:
        if 'prix_numerique' in df.columns:
            avg_price = df['prix_numerique'].mean()
            st.metric("💰 Prix moyen", f"{avg_price:,.0f} FCFA")
        else:
            st.metric("💰 Prix moyen", "N/A")
    
    with col3:
        if 'km_numerique' in df.columns:
            avg_km = df['km_numerique'].mean()
            st.metric("🛣️ KM moyen", f"{avg_km:,.0f} km")
        else:
            st.metric("🛣️ KM moyen", "N/A")
    
    with col4:
        if 'année' in df.columns:
            avg_year = df['année'].mean()
            st.metric("📅 Année moyenne", f"{avg_year:.0f}")
        else:
            st.metric("📅 Année moyenne", "N/A")
    
    st.markdown("---")
    
    # Graphiques en colonnes
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 10 marques
        if 'marque' in df.columns:
            st.markdown("#### 🏆 Top 10 Marques")
            top_marques = df['marque'].value_counts().head(10)
            fig = px.bar(
                x=top_marques.values,
                y=top_marques.index,
                orientation='h',
                labels={'x': 'Nombre d\'annonces', 'y': 'Marque'},
                color=top_marques.values,
                color_continuous_scale='Blues'
            )
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Distribution des prix
        if 'prix_numerique' in df.columns:
            st.markdown("#### 💰 Distribution des Prix")
            df_clean_price = df[df['prix_numerique'].notna() & (df['prix_numerique'] > 0)]
            if len(df_clean_price) > 0:
                fig = px.histogram(
                    df_clean_price,
                    x='prix_numerique',
                    nbins=30,
                    labels={'prix_numerique': 'Prix (FCFA)'},
                    color_discrete_sequence=['#1f77b4']
                )
                fig.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Pas de données de prix disponibles")
    
    # Deuxième ligne de graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        # Transmission
        if 'transmission' in df.columns:
            st.markdown("#### ⚙️ Type de Transmission")
            transmission_counts = df['transmission'].value_counts()
            fig = px.pie(
                values=transmission_counts.values,
                names=transmission_counts.index,
                hole=0.4
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Carburant
        if 'carburant' in df.columns:
            st.markdown("#### ⛽ Type de Carburant")
            carburant_counts = df['carburant'].value_counts()
            fig = px.pie(
                values=carburant_counts.values,
                names=carburant_counts.index,
                hole=0.4
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # Prix par marque (Top 10)
    if 'marque' in df.columns and 'prix_numerique' in df.columns:
        st.markdown("---")
        st.markdown("#### 📊 Prix Moyen par Marque (Top 10)")
        
        top_marques_list = df['marque'].value_counts().head(10).index
        df_top = df[df['marque'].isin(top_marques_list)].copy()
        df_top = df_top[df_top['prix_numerique'].notna() & (df_top['prix_numerique'] > 0)]
        
        if len(df_top) > 0:
            prix_par_marque = df_top.groupby('marque')['prix_numerique'].mean().sort_values(ascending=False)
            
            fig = px.bar(
                x=prix_par_marque.index,
                y=prix_par_marque.values,
                labels={'x': 'Marque', 'y': 'Prix Moyen (FCFA)'},
                color=prix_par_marque.values,
                color_continuous_scale='Viridis'
            )
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # Tableau des données
    st.markdown("---")
    st.markdown("#### 📋 Données Détaillées")
    
    # Filtres
    with st.expander("🔍 Filtres"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'marque' in df.columns:
                marques = ['Toutes'] + sorted(df['marque'].dropna().unique().tolist())
                selected_marque = st.selectbox("Marque:", marques)
        
        with col2:
            if 'transmission' in df.columns:
                transmissions = ['Toutes'] + sorted(df['transmission'].dropna().unique().tolist())
                selected_transmission = st.selectbox("Transmission:", transmissions)
        
        with col3:
            if 'carburant' in df.columns:
                carburants = ['Tous'] + sorted(df['carburant'].dropna().unique().tolist())
                selected_carburant = st.selectbox("Carburant:", carburants)
    
    # Appliquer les filtres
    df_filtered = df.copy()
    
    if 'marque' in df.columns and 'selected_marque' in locals() and selected_marque != 'Toutes':
        df_filtered = df_filtered[df_filtered['marque'] == selected_marque]
    
    if 'transmission' in df.columns and 'selected_transmission' in locals() and selected_transmission != 'Toutes':
        df_filtered = df_filtered[df_filtered['transmission'] == selected_transmission]
    
    if 'carburant' in df.columns and 'selected_carburant' in locals() and selected_carburant != 'Tous':
        df_filtered = df_filtered[df_filtered['carburant'] == selected_carburant]
    
    st.dataframe(df_filtered, use_container_width=True, height=400)
    st.caption(f"📊 {len(df_filtered)} résultats affichés sur {len(df)} total")


def show_motos_dashboard(df):
    """Dashboard spécifique pour les motos"""
    
    st.markdown("### 🏍️ Analyse des Motos")
    
    # Métriques globales
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📊 Total d'annonces", len(df))
    
    with col2:
        if 'prix_numerique' in df.columns:
            avg_price = df['prix_numerique'].mean()
            st.metric("💰 Prix moyen", f"{avg_price:,.0f} FCFA")
        else:
            st.metric("💰 Prix moyen", "N/A")
    
    with col3:
        if 'km_numerique' in df.columns:
            avg_km = df['km_numerique'].mean()
            st.metric("🛣️ KM moyen", f"{avg_km:,.0f} km")
        else:
            st.metric("🛣️ KM moyen", "N/A")
    
    st.markdown("---")
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        # Top marques
        if 'marque' in df.columns:
            st.markdown("#### 🏆 Top 10 Marques")
            top_marques = df['marque'].value_counts().head(10)
            fig = px.bar(
                x=top_marques.values,
                y=top_marques.index,
                orientation='h',
                labels={'x': 'Nombre d\'annonces', 'y': 'Marque'},
                color=top_marques.values,
                color_continuous_scale='Reds'
            )
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Distribution des prix
        if 'prix_numerique' in df.columns:
            st.markdown("#### 💰 Distribution des Prix")
            df_clean_price = df[df['prix_numerique'].notna() & (df['prix_numerique'] > 0)]
            if len(df_clean_price) > 0:
                fig = px.histogram(
                    df_clean_price,
                    x='prix_numerique',
                    nbins=30,
                    labels={'prix_numerique': 'Prix (FCFA)'},
                    color_discrete_sequence=['#d62728']
                )
                fig.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig, use_container_width=True)
    
    # Tableau des données
    st.markdown("---")
    st.markdown("#### 📋 Données Détaillées")
    st.dataframe(df, use_container_width=True, height=400)


def show_locations_dashboard(df):
    """Dashboard spécifique pour les locations"""
    
    st.markdown("### 🚙 Analyse des Locations")
    
    # Métriques globales
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("📊 Total d'annonces", len(df))
    
    with col2:
        if 'prix_numerique' in df.columns:
            avg_price = df['prix_numerique'].mean()
            st.metric("💰 Prix moyen", f"{avg_price:,.0f} FCFA")
        else:
            st.metric("💰 Prix moyen", "N/A")
    
    st.markdown("---")
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        # Top marques
        if 'marque' in df.columns:
            st.markdown("#### 🏆 Top 10 Marques")
            top_marques = df['marque'].value_counts().head(10)
            fig = px.bar(
                x=top_marques.values,
                y=top_marques.index,
                orientation='h',
                labels={'x': 'Nombre d\'annonces', 'y': 'Marque'},
                color=top_marques.values,
                color_continuous_scale='Greens'
            )
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Distribution des prix
        if 'prix_numerique' in df.columns:
            st.markdown("#### 💰 Distribution des Prix")
            df_clean_price = df[df['prix_numerique'].notna() & (df['prix_numerique'] > 0)]
            if len(df_clean_price) > 0:
                fig = px.histogram(
                    df_clean_price,
                    x='prix_numerique',
                    nbins=30,
                    labels={'prix_numerique': 'Prix (FCFA)'},
                    color_discrete_sequence=['#2ca02c']
                )
                fig.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig, use_container_width=True)
    
    # Tableau des données
    st.markdown("---")
    st.markdown("#### 📋 Données Détaillées")
    st.dataframe(df, use_container_width=True, height=400)


def show_demo_dashboard():
    """Affiche un dashboard de démonstration"""
    st.info("📊 Dashboard de démonstration avec données simulées")
    
    # Générer des données factices
    np.random.seed(42)
    
    demo_data = {
        'marque': np.random.choice(['Toyota', 'Mercedes', 'BMW', 'Honda', 'Ford'], 100),
        'prix_numerique': np.random.randint(1000000, 15000000, 100),
        'km_numerique': np.random.randint(0, 200000, 100),
        'année': np.random.randint(2010, 2024, 100),
        'transmission': np.random.choice(['Automatique', 'Manuelle'], 100),
        'carburant': np.random.choice(['Essence', 'Diesel', 'Hybride'], 100)
    }
    
    df_demo = pd.DataFrame(demo_data)
    show_voitures_dashboard(df_demo)
