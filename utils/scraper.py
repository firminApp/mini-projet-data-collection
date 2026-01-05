"""
Module de scraping pour dakar-auto.com
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from typing import List, Dict, Optional


def get_page_content(url: str) -> Optional[BeautifulSoup]:
    """Récupère et parse le contenu HTML d'une page"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'lxml')
    except Exception as e:
        print(f"Erreur lors de la récupération de {url}: {e}")
        return None


def get_total_pages(base_url: str) -> int:
    """Détecte automatiquement le nombre total de pages"""
    soup = get_page_content(base_url)
    if not soup:
        return 1
    
    try:
        paginator = soup.find('nav', class_='paginator')
        if paginator:
            # Trouver tous les liens de pagination
            page_links = paginator.find_all('a', class_='page-link')
            max_page = 1
            
            for link in page_links:
                # Extraire le numéro de page de l'URL
                href = link.get('href', '')
                # Chercher tous les paramètres page= dans l'URL
                matches = re.findall(r'page=(\d+)', href)
                if matches:
                    # Prendre le dernier paramètre page= (le vrai numéro)
                    page_num = int(matches[-1])
                    max_page = max(max_page, page_num)
            
            return max_page
    except Exception as e:
        print(f"Erreur lors de la détection du nombre de pages: {e}")
    
    return 1


def clean_text(text: str) -> str:
    """Nettoie un texte en retirant les espaces superflus"""
    if not text:
        return ""
    return ' '.join(text.split())


def extract_number(text: str) -> Optional[float]:
    """Extrait un nombre d'une chaîne de caractères"""
    if not text:
        return None
    
    numbers = re.findall(r'\d+(?:\s?\d+)*', text.replace(',', ''))
    if numbers:
        number_str = ''.join(numbers[0].split())
        try:
            return float(number_str)
        except ValueError:
            return None
    return None


def scrape_voitures_brut(base_url: str, max_pages: int = None, progress_callback=None) -> List[Dict]:
    """
    Scrape les données brutes des voitures (SANS NETTOYAGE)
    Variables: titre, marque, année, prix, kilométrage, transmission, carburant, adresse
    """
    if max_pages is None:
        if progress_callback:
            progress_callback("🔍 Détection du nombre total de pages...")
        max_pages = get_total_pages(base_url)
        if progress_callback:
            progress_callback(f"✓ {max_pages} pages détectées\n")
    
    all_data = []
    
    for page in range(1, max_pages + 1):
        if progress_callback:
            progress_callback(f"📄 Scraping page {page}/{max_pages}...")
        
        url = f"{base_url}?page={page}" if page > 1 else base_url
        soup = get_page_content(url)
        
        if not soup:
            if progress_callback:
                progress_callback(f"❌ Impossible de récupérer la page {page}, arrêt.")
            break
            
        articles = soup.find_all('div', class_='listings-cards__list-item')
        
        if not articles:
            if progress_callback:
                progress_callback(f"⚠️ Aucun article trouvé sur la page {page}, arrêt.")
            break
            
        for article in articles:
            try:
                data = {}
                
                # V1: Titre - BRUT
                title_elem = article.find('h2', class_='listing-card__header__title')
                if title_elem:
                    title_link = title_elem.find('a')
                    data['titre'] = title_link.get_text().strip() if title_link else title_elem.get_text().strip()
                else:
                    data['titre'] = ""
                
                # V2: Marque
                data['marque'] = ""
                if data['titre']:
                    words = data['titre'].split()
                    if words:
                        data['marque'] = words[0]
                
                # V3: Année
                data['année'] = ""
                if data['titre']:
                    year_match = re.search(r'\b(19|20)\d{2}\b', data['titre'])
                    if year_match:
                        data['année'] = year_match.group()
                
                # V4: Prix - BRUT
                price_elem = article.find('h3', class_='listing-card__header__price')
                data['prix'] = price_elem.get_text().strip() if price_elem else ""
                
                # V5-V7: Attributs (kilométrage, transmission, carburant) - BRUT
                data['kilométrage'] = ""
                data['transmission'] = ""
                data['carburant'] = ""
                
                attributes = article.find_all('li', class_='listing-card__attribute')
                for i, attr in enumerate(attributes[:3]):
                    text = attr.get_text().strip()
                    if i == 0:
                        data['kilométrage'] = text
                    elif i == 1:
                        data['transmission'] = text
                    elif i == 2:
                        data['carburant'] = text
                
                # V8: Adresse - BRUT
                address_parts = []
                town_elem = article.find('span', class_='town-suburb')
                if town_elem:
                    address_parts.append(town_elem.get_text().strip())
                province_elem = article.find('span', class_='province')
                if province_elem:
                    address_parts.append(province_elem.get_text().strip())
                data['adresse'] = ' '.join(address_parts)
                
                all_data.append(data)
                
            except Exception as e:
                if progress_callback:
                    progress_callback(f"⚠️ Erreur article: {e}")
                continue
        
        if page < max_pages:
            time.sleep(1)
    
    if progress_callback:
        progress_callback(f"\n✅ Total voitures scrapées: {len(all_data)}")
    
    return all_data


def scrape_motos_brut(base_url: str, max_pages: int = None, progress_callback=None) -> List[Dict]:
    """
    Scrape les données brutes des motos (SANS NETTOYAGE)
    Variables: titre, marque, année, prix, kilométrage, adresse
    """
    if max_pages is None:
        if progress_callback:
            progress_callback("🔍 Détection du nombre total de pages...")
        max_pages = get_total_pages(base_url)
        if progress_callback:
            progress_callback(f"✓ {max_pages} pages détectées\n")
    
    all_data = []
    
    for page in range(1, max_pages + 1):
        if progress_callback:
            progress_callback(f"📄 Scraping page {page}/{max_pages}...")
        
        url = f"{base_url}?page={page}" if page > 1 else base_url
        soup = get_page_content(url)
        
        if not soup:
            if progress_callback:
                progress_callback(f"❌ Impossible de récupérer la page {page}, arrêt.")
            break
            
        articles = soup.find_all('div', class_='listings-cards__list-item')
        
        if not articles:
            if progress_callback:
                progress_callback(f"⚠️ Aucun article trouvé sur la page {page}, arrêt.")
            break
            
        for article in articles:
            try:
                data = {}
                
                # V1: Titre - BRUT
                title_elem = article.find('h2', class_='listing-card__header__title')
                if title_elem:
                    title_link = title_elem.find('a')
                    data['titre'] = title_link.get_text().strip() if title_link else title_elem.get_text().strip()
                else:
                    data['titre'] = ""
                
                # V2: Marque
                data['marque'] = ""
                if data['titre']:
                    words = data['titre'].split()
                    if words:
                        data['marque'] = words[0]
                
                # V3: Année
                data['année'] = ""
                if data['titre']:
                    year_match = re.search(r'\b(19|20)\d{2}\b', data['titre'])
                    if year_match:
                        data['année'] = year_match.group()
                
                # V4: Prix - BRUT
                price_elem = article.find('h3', class_='listing-card__header__price')
                data['prix'] = price_elem.get_text().strip() if price_elem else ""
                
                # V5: Kilométrage - BRUT
                data['kilométrage'] = ""
                km_attr = article.find('li', class_='listing-card__attribute')
                if km_attr:
                    data['kilométrage'] = km_attr.get_text().strip()
                
                # V6: Adresse - BRUT
                address_parts = []
                town_elem = article.find('span', class_='town-suburb')
                if town_elem:
                    address_parts.append(town_elem.get_text().strip())
                province_elem = article.find('span', class_='province')
                if province_elem:
                    address_parts.append(province_elem.get_text().strip())
                data['adresse'] = ' '.join(address_parts)
                
                all_data.append(data)
                
            except Exception as e:
                if progress_callback:
                    progress_callback(f"⚠️ Erreur article: {e}")
                continue
        
        if page < max_pages:
            time.sleep(1)
    
    if progress_callback:
        progress_callback(f"\n✅ Total motos scrapées: {len(all_data)}")
    
    return all_data


def scrape_locations_brut(base_url: str, max_pages: int = None, progress_callback=None) -> List[Dict]:
    """
    Scrape les données brutes des locations (SANS NETTOYAGE)
    Variables: marque, année, prix, adresse, propriétaire
    """
    if max_pages is None:
        if progress_callback:
            progress_callback("🔍 Détection du nombre total de pages...")
        max_pages = get_total_pages(base_url)
        if progress_callback:
            progress_callback(f"✓ {max_pages} pages détectées\n")
    
    all_data = []
    
    for page in range(1, max_pages + 1):
        if progress_callback:
            progress_callback(f"📄 Scraping page {page}/{max_pages}...")
        
        url = f"{base_url}?page={page}" if page > 1 else base_url
        soup = get_page_content(url)
        
        if not soup:
            if progress_callback:
                progress_callback(f"❌ Impossible de récupérer la page {page}, arrêt.")
            break
            
        articles = soup.find_all('div', class_='listings-cards__list-item')
        
        if not articles:
            if progress_callback:
                progress_callback(f"⚠️ Aucun article trouvé sur la page {page}, arrêt.")
            break
            
        for article in articles:
            try:
                data = {}
                
                # V1: Marque - BRUT
                title_elem = article.find('h2', class_='listing-card__header__title')
                if title_elem:
                    title_link = title_elem.find('a')
                    data['marque'] = title_link.get_text().strip() if title_link else title_elem.get_text().strip()
                else:
                    data['marque'] = ""
                
                # V2: Année
                data['année'] = ""
                if data['marque']:
                    year_match = re.search(r'\b(19|20)\d{2}\b', data['marque'])
                    if year_match:
                        data['année'] = year_match.group()
                
                # V3: Prix - BRUT
                price_elem = article.find('h3', class_='listing-card__header__price')
                data['prix'] = price_elem.get_text().strip() if price_elem else ""
                
                # V4: Adresse - BRUT
                address_parts = []
                town_elem = article.find('span', class_='town-suburb')
                if town_elem:
                    address_parts.append(town_elem.get_text().strip())
                province_elem = article.find('span', class_='province')
                if province_elem:
                    address_parts.append(province_elem.get_text().strip())
                data['adresse'] = ' '.join(address_parts)
                
                # V5: Propriétaire - BRUT
                author_elem = article.find('p', class_='time-author')
                if author_elem:
                    author_link = author_elem.find('a')
                    data['propriétaire'] = author_link.get_text().strip() if author_link else author_elem.get_text().strip()
                else:
                    data['propriétaire'] = ""
                
                all_data.append(data)
                
            except Exception as e:
                if progress_callback:
                    progress_callback(f"⚠️ Erreur article: {e}")
                continue
        
        if page < max_pages:
            time.sleep(1)
    
    if progress_callback:
        progress_callback(f"\n✅ Total locations scrapées: {len(all_data)}")
    
    return all_data


def clean_dataframe(df: pd.DataFrame, category: str) -> pd.DataFrame:
    """Nettoie un DataFrame selon la catégorie"""
    df_cleaned = df.copy()
    
    # Nettoyage du prix
    if 'prix' in df_cleaned.columns:
        df_cleaned['prix_numerique'] = df_cleaned['prix'].apply(extract_number)
    
    # Nettoyage du kilométrage
    if 'kilométrage' in df_cleaned.columns:
        df_cleaned['km_numerique'] = df_cleaned['kilométrage'].apply(extract_number)
    
    # Nettoyage de l'année
    if 'année' in df_cleaned.columns:
        df_cleaned['année'] = df_cleaned['année'].apply(lambda x: int(x) if x and x.isdigit() else None)
    
    # Nettoyage des textes
    text_columns = ['titre', 'marque', 'transmission', 'carburant', 'adresse', 'propriétaire']
    for col in text_columns:
        if col in df_cleaned.columns:
            df_cleaned[col] = df_cleaned[col].apply(clean_text)
    
    return df_cleaned
