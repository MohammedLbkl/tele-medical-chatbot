import sys
import os
REPO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if REPO_PATH not in sys.path:
    sys.path.insert(0, REPO_PATH)
    
from llama_cpp import Llama
from src.prompts.prompts import SYSTEM_PROMPT_CLASSIFICATION


def format_prompt(messages):
    """Formate les messages pour Mistral Instruct"""
    formatted = f"<s>[INST] {SYSTEM_PROMPT_CLASSIFICATION}\n\n"
    
    for i, msg in enumerate(messages):
        if msg["role"] == "user":
            if i == 0:
                formatted += f"{msg['content']} [/INST]"
            else:
                formatted += f"[INST] {msg['content']} [/INST]"
        elif msg["role"] == "assistant":
            formatted += f" {msg['content']}</s>"
    
    return formatted

def generate_response_classification(llm, messages):
    """Génère une réponse avec le modèle"""
    prompt = format_prompt(messages)
    
    response = llm(
        prompt,
        max_tokens=254,
        temperature=0,
        stop=["</s>", "[INST]"],
        echo=False
    )
    
    return response['choices'][0]['text'].strip()

if __name__ == "__main__":
    
    llm = Llama(
        model_path="src/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf",  # Chemin à adapter
        n_ctx=32768,  # Taille du contexte
        n_threads=8,  # Nombre de threads CPU
        n_gpu_layers=0,  # Mettre > 0 si GPU disponible
        verbose=False
    )
    list_questions_generales = ["J’ai mal à la gorge depuis deux jours, est-ce grave ?",
                                "Pourquoi je tousse souvent quand je dors ?" 
                                ]
    for question in list_questions_generales:
        messages = [{"role": "user", "content": question}]
        reponse = generate_response_classification(llm, messages)
        print(f"Question : {question}\nRéponse : {reponse}\n")
    