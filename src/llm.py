import sys
import os
REPO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if REPO_PATH not in sys.path:
    sys.path.insert(0, REPO_PATH)
    
from llama_cpp import Llama
from src.prompts.prompts import SYSTEM_PROMPT
from contextlib import contextmanager

def model_llm(model_path: str) -> "Llama":
    """
    Charge un modèle LLaMA depuis le chemin spécifié tout en supprimant les sorties
    standard et d'erreur pendant le chargement pour éviter l'affichage des logs.

    Args:
        model_path (str): Chemin vers les fichiers du modèle LLaMA.

    Returns:
        Llama: Instance du modèle prête à être utilisée.
    """
    @contextmanager
    def suppress_llama_output():
        with open(os.devnull, 'w') as devnull:
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = devnull
            sys.stderr = devnull
            try:
                yield
            finally:
                sys.stdout = old_stdout
                sys.stderr = old_stderr

    with suppress_llama_output():
        llm = Llama(
            model_path=model_path,
            n_ctx=2048,
            chat_format="chatml",
            verbose=False
        )
    return llm

def generate_response(llm: "Llama", question: str) -> str:
    """
    Génère une réponse à partir d'une question en utilisant le modèle LLaMA fourni.

    Args:
        llm (Llama): Instance du modèle LLaMA.
        question (str): Texte ou question à envoyer au modèle.

    Returns:
        str: Réponse générée par le modèle, sans espaces superflus.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]

    response = llm.create_chat_completion(
        messages=messages,
        temperature=0.3,
        max_tokens=512
    )
    return response['choices'][0]['message']['content'].strip()