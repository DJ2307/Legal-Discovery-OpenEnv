---
title: Legal Discovery OpenEnv
emoji: 🏢
colorFrom: indigo
colorTo: yellow
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# ⚖️ Legal-Discovery-OpenEnv: Multi-Hop Deductive Reasoning Benchmark
**Meta PyTorch Hackathon x Scaler School of Technology Submission**

---

## 🚀 Overview
Legal-Discovery-OpenEnv is a commercial-grade Reinforcement Learning environment designed to test the **Chain of Thought (CoT)** and multi-agent deductive reasoning capabilities of frontier models (like Llama 3). 

Instead of generic text classification, this environment simulates the adversarial, high-stakes reality of corporate litigation. Models must ingest intake emails, intelligently navigate discovery, legally escalate access to hidden documents, and route cases accurately while avoiding deeply embedded logical traps.

## 🧠 The 12-Stage Architecture: CLAT-Level Logic Traps
This environment utilizes a custom 12-scenario gauntlet heavily inspired by advanced legal aptitude testing (CLAT/AILET). It evaluates true model intelligence using:

* **Enforced Chain of Thought:** Models are constrained by a strict Pydantic schema, forcing them to output step-by-step deductive `reasoning` in JSON before taking any action.
* **Procedural Escalation (Subpoenas):** Models cannot simply "gather" all evidence. Sensitive documents are locked behind `[ACCESS DENIED]` walls, requiring the LLM to dynamically shift strategy and execute a `request_subpoena` action based on probable cause.
* **Contradiction & Deception Traps:** Includes advanced legal barriers such as **"Fruit of the Poisonous Tree"** (ignoring illegally obtained evidence), **Attorney-Client Privilege** shields, and jurisdictional chess matches.

### 🛑 Example Trap: The Double-Blind Poisoning
To understand the complexity, consider Task 12:
1.  **Intake:** Client claims their partner poisoned their coffee. 
2.  **Surface Evidence:** `Medical History` confirms traces of arsenic. `Employee Communications` show the partner Googling "how to buy arsenic." (An average LLM routes to *Criminal Defense* here and fails).
3.  **The Subpoena Hop:** An elite model will subpoena the `Encrypted Server Logs`, revealing the *client* remotely accessed the partner's PC to make the search, and ingested a non-lethal dose to frame them for a hostile corporate takeover. 
4.  **True Route:** *Corporate Law* (Fraudulent Takeover).

## 🛠️ Technical Infrastructure & Resilience
This project was heavily battle-tested against strict automated validation constraints, resulting in a bulletproof execution framework:

* **Omni-Regex Compliant Logging:** Engineered dynamic `[START]`, `[STEP]`, and `[END]` telemetry that perfectly satisfies legacy backend parsers and modern PDF guidelines simultaneously.
* **Mathematically Clamped Reward Engine:** Reverse-engineered undocumented validation constraints by deploying a clamped sparse-reward system (`max(0.05, min(0.95))`). This mathematically guarantees scores stay strictly within the required (0, 1) float boundaries without triggering automated validation failures.
* **Optimized Inference Pacing:** Operates flawlessly under the mandated 2 vCPU / 8 GB RAM Hugging Face Docker constraints, carefully pacing OpenAI client calls to avoid proxy timeouts during the 12-stage validation loop.

---

### 💡 Why This Belongs in Round 2 (Bangalore)
1.  **Domain Expertise:** Translates high-level legal reasoning and NLU-prep logic directly into a highly sophisticated Reinforcement Learning benchmark.
2.  **Production-Level Engineering:** Forged through 50+ iterations of rigorous validation debugging, resulting in a highly stable, timeout-resistant, and strictly deterministic grading engine. 
3.  **True LLM Evaluation:** Evaluates *why* a model makes a decision, not just *what* decision it makes, aligning perfectly with Meta's goal for OpenEnv as a frontier evaluation tool.
