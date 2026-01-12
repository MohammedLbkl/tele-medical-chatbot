
import sys
import os
REPO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if REPO_PATH not in sys.path:
    sys.path.insert(0, REPO_PATH)

from llama_cpp import Llama
from src.prompts.prompts import SYSTEM_PROMPT_HALLUCINATION
from src.llm import model_llm
from typing import List



def generate_response_hallucination(llm: "Llama", reponse: str) -> str:
    """
    Génère une réponse du modèle LLaMA pour détecter une hallucination.

    Args:
        llm (Llama): Instance du modèle LLaMA.
        reponse (str): Texte ou réponse à analyser pour l'hallucination.

    Returns:
        str: Résultat de la détection d'hallucination, sans espaces superflus.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_HALLUCINATION},
        {"role": "user", "content": reponse}
    ]

    response = llm.create_chat_completion(
        messages=messages,
        temperature=0,
        max_tokens=15
    )

    return response['choices'][0]['message']['content'].strip()


def evaluation_hallucination(model_paths: str, list_question: List[str]) -> List[str]:
    """
    Évalue une liste de réponses pour détecter des hallucinations en utilisant un modèle LLaMA.

    Args:
        model_paths (str): Chemin vers les fichiers du modèle LLaMA.
        list_question (List[str]): Liste de réponses à analyser.

    Returns:
        List[str]: Liste des résultats de détection d'hallucination pour chaque réponse.
    """
    list_proba = []
    for q in list_question:
        llm = model_llm(model_paths)
        proba = generate_response_hallucination(llm, q)
        list_proba.append(proba)
    return list_proba