"""
Page d'évaluation de l'application
"""

import streamlit as st


def show():
    st.header("📝 Évaluation de l'Application")
    st.markdown("Votre avis nous intéresse! Aidez-nous à améliorer l'application.")
    st.markdown("---")
    
    # Tabs pour les deux options
    tab1, tab2 = st.tabs(["🔗 Google Forms", "📱 KoboToolbox"])
    
    # TAB 1: Google Forms
    with tab1:
        st.markdown("### 🔗 Formulaire Google Forms")
        st.info("Pour une évaluation plus détaillée, vous pouvez également remplir notre formulaire Google Forms.")
        
        # URL du formulaire Google Forms
        google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfBAaC3kYyUgOxts5hxNabLCwCvzotKBRgMWxSeWEx5X3K4VQ/viewform?usp=header"
        
        st.markdown(f"""
        Cliquez sur le bouton ci-dessous pour accéder au formulaire Google Forms:
        
        [![Ouvrir le formulaire]({create_button_badge()})]({google_form_url})
        """)
        
        # Afficher le formulaire en iframe
        st.markdown("#### Aperçu du formulaire:")
        
        # URL embed pour Google Forms
        embed_url = "https://docs.google.com/forms/d/e/1FAIpQLSfBAaC3kYyUgOxts5hxNabLCwCvzotKBRgMWxSeWEx5X3K4VQ/viewform?embedded=true"
        iframe_code = f"""
        <iframe 
            src="{embed_url}" 
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
    
    # TAB 2: KoboToolbox
    with tab2:
        st.markdown("### 📱 Formulaire KoboToolbox")
        st.info("Remplissez notre questionnaire sur KoboToolbox pour une collecte de données optimisée.")
        
        # URL du formulaire KoboToolbox
        kobo_form_url = "https://ee.kobotoolbox.org/x/Jzh0Kes7"
        
        st.markdown(f"""
        Cliquez sur le bouton ci-dessous pour accéder au formulaire KoboToolbox:
        
        [![Ouvrir le formulaire](https://img.shields.io/badge/KoboToolbox-Ouvrir-00A3E0?style=for-the-badge&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAA0gAAANIBKVDmugAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAADxSURBVCiRY2AYBcMHAAKI+f//PwM2DICAQQYI/g8QvAcI3gME7wCC/0DwHwj+AwX/gQL/wQEDVg0MQMAPFPwHCv4DBf+Bgv9AwX+g4D9Q8B8o+A8O/oMC/+EAWyNQw3+g4D9Q8B8o+A8U/AcK/gMF/4GC/0DBf3DwHxT4Dwe4NAI1/AcK/gMF/4GC/0DBf6DgP1DwHyj4Dw7+gwL/4QBZIxDgBf//AwX/gYL/QMF/oOA/UPAfKPgPDv6DAv/hAKcGIOAHCv4DBf+Bgv9AwX+g4D9Q8B8c/AcF/sMBTg1AwA8U/AcK/gMF/4GC/0DBf6DgPzj4Dwr8hwMAaKxUJq2wDiUAAAAASUVORK5CYII=&logoColor=white)]({kobo_form_url})
        """)
        
        # Afficher le formulaire en iframe
        # st.markdown("#### Aperçu du formulaire:")
        
        # iframe_code = f"""
        # <iframe 
        #     src="{kobo_form_url}" 
        #     width="100%" 
        #     height="800" 
        #     frameborder="0" 
        #     marginheight="0" 
        #     marginwidth="0">
        #     Chargement…
        # </iframe>
        # """
        
        # st.components.v1.html(iframe_code, height=800, scrolling=True)
        
        st.markdown("---")
        st.caption("💡 Astuce: Vous pouvez aussi remplir le formulaire directement sur KoboToolbox en cliquant sur le lien ci-dessus.")


def create_button_badge():
    """Crée un badge de bouton pour Google Forms"""
