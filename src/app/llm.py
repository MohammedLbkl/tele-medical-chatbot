import sys
import os
REPO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if REPO_PATH not in sys.path:
    sys.path.insert(0, REPO_PATH)
    
from llama_cpp import Llama
from src.prompts.prompts import SYSTEM_PROMPT

llm = Llama(
    model_path="src/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf",  # Chemin à adapter
    n_ctx=32768,  # Taille du contexte
    n_threads=8,  # Nombre de threads CPU
    n_gpu_layers=0,  # Mettre > 0 si GPU disponible
    verbose=False
)

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

if __name__ == "__main__":
    
    list_questions_generales = ["J’ai mal à la gorge depuis deux jours, est-ce grave ?",
                                "Pourquoi je tousse souvent quand je dors ?",
                                "J’ai parfois des étourdissements, que peut-on dire de manière générale ?"  
                                ]
    list_questions_grave = ["Mon bébé a une fièvre très élevée et semble très fatigué, que devrais-je faire ?",
                                "Je respire difficilement et j’ai du mal à parler, que devrais-je faire en général ?",
                                "J’ai été blessé à la tête et je vomis, que devrais-je faire en général ?"  
                                ]
for question in list_questions_generales:
    messages = [{"role": "user", "content": question}]
    reponse = generate_response(llm, messages)
    print(f"Question : {question}\nRéponse : {reponse}\n")
    
for question in list_questions_grave:
    messages = [{"role": "user", "content": question}]
    reponse = generate_response(llm, messages)
    print(f"Question : {question}\nRéponse : {reponse}\n")
