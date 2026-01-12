import sys
import os
REPO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if REPO_PATH not in sys.path:
    sys.path.insert(0, REPO_PATH)
    
from typing import List
from llama_cpp import Llama
from src.llm import model_llm
from src.prompts.prompts import SYSTEM_PROMPT_CLASSIFICATION


def generate_response_classification(llm: "Llama", question: str) -> str:
    """
    Génère une réponse de classification à partir d'une question en utilisant le modèle LLaMA.

    Args:
        llm (Llama): Instance du modèle LLaMA.
        question (str): Texte ou question à envoyer au modèle.

    Returns:
        str: Réponse de classification générée par le modèle, sans espaces superflus.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_CLASSIFICATION},
        {"role": "user", "content": question}
    ]

    response = llm.create_chat_completion(
        messages=messages,
        temperature=0,
        max_tokens=15
    )

    return response['choices'][0]['message']['content'].strip()

def evaluation_classification(model_paths: str, list_question: List[str]) -> List[str]:
    """
    Évalue une liste de questions en utilisant un modèle LLaMA pour la classification.

    Args:
        model_paths (str): Chemin vers les fichiers du modèle LLaMA.
        list_question (List[str]): Liste de questions à classer.

    Returns:
        List[str]: Liste des réponses de classification pour chaque question.
    """
    list_proba = []
    for q in list_question:
        llm = model_llm(model_paths)
        proba = generate_response_classification(llm, q)
        list_proba.append(proba)
    return list_proba