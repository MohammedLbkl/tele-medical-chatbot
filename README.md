"""
# Projet d'Évaluation de Modèles de Langage pour Téléconsultation

Ce projet a pour objectif de tester et comparer plusieurs modèles de langage sur des questions médicales afin de générer des réponses informatives, détecter les situations nécessitant une téléconsultation immédiate et évaluer les risques d’hallucinations.

---

## Table des matières

- Présentation
- Architecture du projet
- Installation
- Lancement
- Fonctionnement
- Résultats

---

## Présentation

Le projet teste trois modèles de langage :

1. Mistral 7B
2. Qwen 2.5 1.5B
3. Qwen 2.5 7B

L’objectif est de générer des réponses aux questions médicales, classifier si une téléconsultation est nécessaire et détecter les hallucinations dans les réponses.

---

## Architecture du projet

project/
│
├─ models/ # Contient les fichiers des modèles (.gguf)
│  ├─ mistral-7b-instruct-v0.2.Q4_K_M.gguf
│  ├─ qwen2.5-1.5b-instruct-q8_0.gguf
│  └─ qwen2.5-7b-instruct-q2_k.gguf
│
├─ data/ # Contient les fichiers de données JSON
│  └─ data.json
│
├─ notebooks/ # Notebook principal pour l’évaluation
│  └─ evaluation.ipynb
│
├─ src/ # Fonctions utilitaires (si applicable)
│  ├─ model_utils.py
│  ├─ evaluation.py
│  └─ response_generation.py
│
└─ README.md

---

## Installation

Cloner le repository :
git clone <URL_DU_REPOSITORY>
cd project

Installer les dépendances Python :
pip install -r requirements.txt

Vérifier que les modèles .gguf sont placés dans le dossier models/ et que le dataset data.json est dans data/.

---

## Lancement

Ouvrir le notebook principal notebooks/evaluation.ipynb et exécuter les cellules dans l’ordre.

---

## Fonctionnement

- Configuration des modèles via MODELS_CONFIG  
- Lecture des questions depuis data.json  
- Classification de la nécessité d’une téléconsultation  
- Détection des hallucinations  
- Analyse via matrices de confusion et rapports de classification  

---

## Résultats

Classification téléconsultation :
- Mistral 7B : Accuracy 0.89
- Qwen 2.5 1.5B : Accuracy 0.79
- Qwen 2.5 7B : Accuracy 0.95

Détection des hallucinations :
- Mistral 7B : Accuracy 0.84
- Qwen 2.5 1.5B : Accuracy 0.95
- Qwen 2.5 7B : Accuracy 0.95

Conclusion : Qwen 2.5 7B offre le meilleur compromis entre précision et fiabilité.
"""
