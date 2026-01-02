# 🚗 Dakar Auto - Scraping & Analytics Application

Application Streamlit pour le scraping et l'analyse des données de [dakar-auto.com](https://www.dakar-auto.com).

## 📋 Fonctionnalités

- **🔍 Scraping Interactif**: Scrapez des données sur plusieurs pages avec détection automatique du nombre de pages
- **📥 Téléchargement**: Téléchargez les données brutes ou nettoyées au format CSV
- **📊 Dashboard**: Visualisations interactives des données nettoyées (graphiques, statistiques, filtres)
- **📝 Évaluation**: Formulaire d'évaluation de l'application intégré

## 🛠️ Installation

### Prérequis
- Python 3.8 ou supérieur
- pip

### Installation des dépendances

```bash
pip install -r requirements.txt
```

## 🚀 Lancement de l'application

```bash
streamlit run app.py
```

L'application sera accessible à l'adresse: `http://localhost:8501`

## 📁 Structure du projet

```
mini projet/
├── app.py                      # Application principale
├── requirements.txt            # Dépendances Python
├── README.md                   # Documentation
├── utils/
│   ├── __init__.py
│   └── scraper.py             # Fonctions de scraping
├── pages/
│   ├── __init__.py
│   ├── scraping.py            # Page de scraping
│   ├── download.py            # Page de téléchargement
│   ├── dashboard.py           # Page du dashboard
│   └── evaluation.py          # Page d'évaluation
├── data_dakar_auto/           # Données nettoyées (créé automatiquement)
├── data_dakar_auto_brutes/    # Données brutes (créé automatiquement)
└── evaluations/               # Évaluations sauvegardées (créé automatiquement)
```

## 📊 Sources de données

L'application scrape les données depuis trois catégories de dakar-auto.com:

1. **🚗 Voitures**: https://www.dakar-auto.com/voitures-4
2. **🏍️ Motos**: https://www.dakar-auto.com/motos-and-scooters-3
3. **🚙 Locations**: https://www.dakar-auto.com/location-de-voitures-19

## 💡 Utilisation

### 1. Scraping de données

1. Accédez à la page "🔍 Scraping"
2. Sélectionnez la catégorie (Voitures, Motos, ou Locations)
3. Choisissez le nombre de pages à scraper:
   - Détection automatique (recommandé)
   - Nombre manuel de pages
4. Option: Activer le nettoyage des données
5. Cliquez sur "🚀 Lancer le scraping"
6. Téléchargez ou sauvegardez les résultats

### 2. Téléchargement de données

1. Accédez à la page "📥 Téléchargement"
2. Choisissez entre données brutes ou nettoyées
3. Visualisez les fichiers disponibles
4. Téléchargez individuellement ou en lot (ZIP)

### 3. Visualisation des données

1. Accédez à la page "📊 Dashboard"
2. Sélectionnez un fichier de données nettoyées
3. Explorez les visualisations:
   - Statistiques globales
   - Graphiques interactifs
   - Tableaux filtrables

### 4. Évaluation de l'application

1. Accédez à la page "📝 Évaluation"
2. Remplissez le formulaire intégré ou Google Forms
3. Soumettez votre évaluation

## 🔧 Configuration

### Personnalisation du scraping

Modifiez `utils/scraper.py` pour:
- Ajuster les délais entre les requêtes
- Modifier les sélecteurs HTML
- Ajouter de nouvelles fonctions de nettoyage

### Personnalisation du dashboard

Modifiez `pages/dashboard.py` pour:
- Ajouter de nouveaux graphiques
- Modifier les couleurs et thèmes
- Créer des analyses personnalisées

## 📦 Déploiement

### Streamlit Cloud

1. Créez un compte sur [Streamlit Cloud](https://streamlit.io/cloud)
2. Connectez votre repository GitHub
3. Déployez l'application en un clic

### Autres options

- **Heroku**: Utilisez un `Procfile` avec `web: streamlit run app.py`
- **Docker**: Créez un Dockerfile basé sur `python:3.9-slim`
- **AWS/GCP/Azure**: Déployez sur une instance avec Streamlit installé

## ⚠️ Avertissements

- **Respect du site web**: Utilisez des délais raisonnables entre les requêtes
- **Données personnelles**: Ne partagez pas les données scrapées publiquement
- **Légalité**: Vérifiez les conditions d'utilisation du site avant de scraper
- **Performance**: Le scraping de toutes les pages peut prendre du temps

## 📝 Notes techniques

### Données brutes vs nettoyées

- **Données brutes**: Valeurs extraites telles quelles du site (avec espaces, symboles, etc.)
- **Données nettoyées**: Valeurs formatées avec colonnes numériques additionnelles (prix_numerique, km_numerique, etc.)

### Rate limiting

L'application attend 1 seconde entre chaque requête de page pour éviter de surcharger le serveur.

## 🤝 Contribution

Pour contribuer au projet:

1. Fork le repository
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Créez une Pull Request

## 📄 Licence

Ce projet est à usage éducatif uniquement.

## 👥 Auteurs

- Projet développé dans le cadre du Master IA - DIT
- Module: Data Collection

## 📞 Support

Pour toute question ou problème:
- Ouvrez une issue sur GitHub
- Contactez l'équipe de développement
- Consultez la documentation Streamlit: https://docs.streamlit.io

## 🎯 Roadmap

Fonctionnalités futures prévues:
- [ ] Export Excel en plus du CSV
- [ ] Filtres avancés dans le dashboard
- [ ] API REST pour accéder aux données
- [ ] Notifications par email après scraping
- [ ] Planification automatique du scraping
- [ ] Support multilingue (Français/Anglais)
- [ ] Mode sombre/clair
- [ ] Comparaison entre périodes différentes

## 🙏 Remerciements

- [Streamlit](https://streamlit.io) pour le framework
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) pour le parsing HTML
- [Plotly](https://plotly.com) pour les visualisations
- [dakar-auto.com](https://www.dakar-auto.com) pour les données

---

**Made with ❤️ and Python**
