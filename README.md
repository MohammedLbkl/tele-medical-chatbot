# Language Model Evaluation Project for Teleconsultation

This project aims to test and compare several language models on medical questions in order to generate informative answers, detect situations requiring immediate teleconsultation, and evaluate the risk of hallucinations.

---

## Table of Contents

- Overview
- Project Architecture
- Installation
- Running the Project
- How It Works
- Results

---

## Overview

The project tests three language models:

1. [Mistral 7B](https://huggingface.co/mistralai/Mistral-7B-v0.1)
2. [Qwen 2.5 1.5B](https://huggingface.co/Qwen/Qwen2.5-1.5B)
3. [Qwen 2.5 7B](https://huggingface.co/Qwen/Qwen2.5-7B)

The goal is to generate answers to medical questions, classify whether a teleconsultation is required, and detect hallucinations in the responses.

---

## Project Architecture

```yaml
project/
│
├─ data/                     # Data used by the chatbot
│  └─ data.json
│
├─ notebooks/                # Notebooks for testing and evaluation
│  ├─ evaluation.ipynb
│  └─ test.ipynb
│
├─ src/                      # Main source code
│  │
│  ├─ prompts/               # Prompt logic and LLM processing
│  │  ├─ __pycache__/
│  │  ├─ prompts.py          # Prompt templates
│  │  ├─ classification.py  # Medical request classification
│  │  ├─ hallucination.py   # Hallucination handling / reduction
│  │  └─ llm.py              # Model calling interface (external path)
│
├─ .gitignore
├─ README.md                 # Project documentation
└─ requirements.txt          # Python dependencies
```
---

## Installation

Clone the repository:
```bash
git clone https://github.com/MohammedLbkl/tele-medical-chatbot.git
cd tele-medical-chatbot
```
Install Python dependencies:
```bash
pip install -r requirements.txt
```
Make sure the .gguf models are placed in the models/ directory and that the data.json dataset is located in the data/ folder.

---

## Running the Project

Open the main notebook `notebooks/evaluation.ipynb` and run the cells in order.

---

## How It Works

- Model configuration via `MODELS_CONFIG`  
- Loading questions from `data.json`  
- Classification of teleconsultation necessity  
- Hallucination detection  
- Analysis using confusion matrices and classification reports  

---

## Results

Teleconsultation classification:
- Mistral 7B: Accuracy 0.89
- Qwen 2.5 1.5B: Accuracy 0.79
- Qwen 2.5 7B: Accuracy 0.95

Hallucination detection:
- Mistral 7B: Accuracy 0.84
- Qwen 2.5 1.5B: Accuracy 0.95
- Qwen 2.5 7B: Accuracy 0.95

Conclusion: Qwen 2.5 7B offers the best trade-off between accuracy and reliability.

