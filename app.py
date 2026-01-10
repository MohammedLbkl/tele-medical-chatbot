
#. streamlit run app.py
import streamlit as st
from llama_cpp import Llama

# Configuration de la page
st.set_page_config(
    page_title="Assistant Médical",
    page_icon="🏥",
    layout="wide"
)

# System prompt
SYSTEM_PROMPT = """Tu es un assistant médical grand public destiné à fournir uniquement de l'information
médicale générale et éducative, à destination du grand public.

PÉRIMÈTRE AUTORISÉ :
- Expliquer des symptômes courants de manière générale
- Donner des informations de santé fiables, non personnalisées
- Décrire quand il est habituel de consulter un professionnel de santé
- Donner des conseils généraux de prévention et d'hygiène de vie
- Orienter vers un médecin ou une téléconsultation lorsque nécessaire

INTERDICTIONS STRICTES :
- Ne jamais poser de diagnostic
- Ne jamais confirmer ou infirmer une maladie
- Ne jamais prescrire de traitement ou de médicament
- Ne jamais interpréter des examens médicaux ou résultats d'analyse
- Ne jamais donner d'avis médical personnalisé
- Ne jamais minimiser un risque grave

STYLE DE RÉPONSE :
- Ton clair, bienveillant, rassurant et non alarmiste
- Langage simple et accessible
- Toujours rappeler que l'information fournie ne remplace pas un avis médical
- Structurer les réponses (paragraphes courts ou listes)"""

@st.cache_resource
def load_model():
    """Charge le modèle Mistral 7B GGUF"""
    try:
        llm = Llama(
            model_path="src/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf",  # Chemin à adapter
            n_ctx=4096,  # Taille du contexte
            n_threads=8,  # Nombre de threads CPU
            n_gpu_layers=0,  # Mettre > 0 si GPU disponible
            verbose=False
        )
        return llm
    except Exception as e:
        st.error(f"Erreur lors du chargement du modèle : {e}")
        return None

def format_prompt(messages):
    """Formate les messages pour Mistral Instruct"""
    formatted = f"<s>[INST] {SYSTEM_PROMPT}\n\n"
    
    for i, msg in enumerate(messages):
        if msg["role"] == "user":
            if i == 0:
                formatted += f"{msg['content']} [/INST]"
            else:
                formatted += f"[INST] {msg['content']} [/INST]"
        elif msg["role"] == "assistant":
            formatted += f" {msg['content']}</s>"
    
    return formatted

def generate_response(llm, messages):
    """Génère une réponse avec le modèle"""
    prompt = format_prompt(messages)
    
    response = llm(
        prompt,
        max_tokens=1024,
        temperature=0.7,
        top_p=0.95,
        repeat_penalty=1.1,
        stop=["</s>", "[INST]"],
        echo=False
    )
    
    return response['choices'][0]['text'].strip()

def main():
    st.title("🏥 Assistant Médical Grand Public")
    st.caption("⚠️ Cet assistant fournit des informations générales uniquement. Consultez un professionnel de santé pour un avis médical personnalisé.")
    
    # Initialisation de l'historique dans session_state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Bouton pour rafraîchir la conversation
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🔄 Nouvelle conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    # Chargement du modèle
    llm = load_model()
    
    if llm is None:
        st.error("Impossible de charger le modèle. Vérifiez le chemin du fichier GGUF.")
        st.stop()
    
    # Affichage de l'historique des messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input utilisateur
    if prompt := st.chat_input("Posez votre question médicale..."):
        # Ajouter le message utilisateur
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Générer la réponse
        with st.chat_message("assistant"):
            with st.spinner("Génération de la réponse..."):
                try:
                    response = generate_response(llm, st.session_state.messages)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Erreur lors de la génération : {e}")

    # Sidebar avec informations
    with st.sidebar:
        st.header("ℹ️ Informations")
        st.info("""
        **Cet assistant peut :**
        - Expliquer des symptômes courants
        - Donner des informations santé générales
        - Conseiller quand consulter
        
        **Il ne peut pas :**
        - Poser de diagnostic
        - Prescrire des médicaments
        - Interpréter des examens
        """)
        
        st.header("📊 Paramètres")
        st.write(f"Messages dans l'historique : {len(st.session_state.messages)}")
        
        if st.button("⚠️ Effacer l'historique"):
            st.session_state.messages = []
            st.rerun()

if __name__ == "__main__":
    main()