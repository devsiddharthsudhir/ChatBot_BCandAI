# TrustChain Chatbot – Verifiable AI Conversations with Blockchain Provenance

**TrustChain Chatbot** is a full-stack project that combines a classic intent-based chatbot with **blockchain-backed provenance**.

Instead of being a black-box, every conversation is:

- Classified using a reproducible ML pipeline (NLTK + TF-IDF + LinearSVC)
- Logged as structured JSONL
- Hashed with **SHA-256**
- Anchored on **Ethereum (Sepolia / local Hardhat)** via a smart contract called `ProvenanceRegistry`

This makes chat history **tamper-evident**, version-aware, and auditable – useful for domains like healthcare, finance, or compliance where trust and accountability matter.

---

## ✨ Key Features

- 🧠 **Intent-based chatbot**
  - NLTK + TF-IDF + LinearSVC classifier trained on an `intents.json` corpus.
- 🧾 **Structured logging**
  - Each interaction is stored in per-session **JSONL** files (message, reply, intent, timestamps, model version, dataset ID).
- 🔐 **On-chain provenance**
  - `ProvenanceRegistry` smart contract tracks:
    - Datasets (`registerDataset`)
    - Model versions (`registerModel`)
    - Chat log hashes (`anchorLog`)
- 🔗 **End-to-end flow**
  - Flask backend + Web3.py + Hardhat/Alchemy.
  - Frontend shows reply + truncated **transaction hash** as a provenance badge.
- 🧪 **Local dev + testnet**
  - Works on both:
    - Local **Hardhat** network
    - **Sepolia** testnet via Alchemy + MetaMask

---

## 🧱 Architecture Overview

High-level flow:

1. **User** types a message in the web chat UI.
2. **Frontend** sends the message to **Flask backend** (`/chat`).
3. Flask:
   - runs **intent classification** (NLTK + TF-IDF + LinearSVC),
   - chooses an appropriate response,
   - appends interaction to a **session JSONL log**,
   - computes **SHA-256(log)**,
   - calls `ProvenanceRegistry.anchorLog` via **Web3.py**.
4. `ProvenanceRegistry` stores the log hash on-chain and emits a `LogAnchored` event.
5. Backend returns:
   - reply text,
   - intent tag,
   - dataset/model ids,
   - **transaction hash**.
6. Frontend displays response + a small **“Verified on-chain”** badge with truncated tx hash.

(You can add your Eraser AI architecture PNG under `/public/case-studies/trustchain/architecture.png` and reference it from your portfolio.)

---

## 🧰 Tech Stack

**ML & Backend**

- Python 3.10+
- Flask
- NLTK
- scikit-learn (TF-IDF + LinearSVC)
- JSONL for logs
- Web3.py

**Blockchain**

- Solidity (`^0.8.20`)
- Hardhat
- Ethereum (local Hardhat network, Sepolia testnet)
- MetaMask
- Alchemy (for Sepolia RPC)

**Frontend**

- HTML / CSS / JavaScript chat UI
- Fetch API to call Flask
- MetaMask browser extension

---

## 📁 Repository Structure

```text
ChatBot_BCandAI/
├─ ml/
│  ├─ intents.json           # Training data for intents
│  ├─ train_intents.py       # Train TF-IDF + LinearSVC model
│  ├─ model.pkl              # Trained classifier (generated)
│  └─ vectorizer.pkl         # TF-IDF vectorizer (generated)
│
├─ backend/
│  ├─ app.py                 # Flask API (chat endpoint + provenance)
│  ├─ provenance/
│  │  ├─ __init__.py
│  │  ├─ web3_client.py      # Web3.py setup, RPC config
│  │  ├─ provenance_registry.py  # Contract wrapper (anchorLog, etc.)
│  │  └─ abi/
│  │     └─ ProvenanceRegistry.json   # ABI copied from Hardhat artifacts
│  └─ requirements.txt
│
├─ blockchain/
│  ├─ contracts/
│  │  └─ ProvenanceRegistry.sol  # Solidity smart contract
│  ├─ scripts/
│  │  └─ deploy_provenance.ts    # Deploy contract and print address
│  ├─ hardhat.config.ts
│  ├─ package.json
│  └─ ... (artifacts, cache, node_modules)
│
├─ frontend/
│  ├─ index.html             # Simple chat interface
│  ├─ style.css
│  └─ app.js                 # Calls Flask /chat and displays tx hash
│
└─ README.md
