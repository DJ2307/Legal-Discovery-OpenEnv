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

​# ⚖️ Legal-Discovery-OpenEnv: High-Fidelity Case Routing
**Meta PyTorch Hackathon x Scaler School of Technology Submission**

---

## 🚀 Overview
This environment simulates the high-stakes role of a **Legal Associate**. The AI must ingest raw client emails, request specific evidence (Police Reports, Financial Records, etc.), and accurately route the case to the correct department.

## 🧠 The "Trap" Architecture: Deductive Reasoning
Unlike simple classification, this environment uses **Step-Wise Discovery** to test true model intelligence.

* **Red Herring Logic:** A "Breach of Contract" case may appear to be Corporate Law, but requesting **Financial Records** reveals federal money laundering, shifting the correct route to **Criminal Defense**.
* **Expert Scenarios:** Includes complex traps like **Corporate Espionage** and **Aggressive IP Buyouts**, testing a model's ability to distinguish between criminal activity and civil contract execution.

## 📈 Performance Metrics (Llama 3.1 8B)
Our baseline testing proves the environment successfully challenges frontier models:
* **Easy/Medium Tasks:** ~0.90+ (High success).
* **Hard/Expert Tasks:** ~0.10 - 0.20 (Significant variance).
* **Average Baseline Score:** 0.62 / 1.0

## 🛠️ Technical Innovation
* **Deterministic Integer Scoring:** To avoid floating-point errors common in RL environments, we engineered a custom Integer-to-Float reward engine for 100% precision.
* **Efficiency Penalization:** Models are penalized for excessive document requests to simulate "billable hours" efficiency.
* **Strict Pydantic Validation:** Prevents model hallucinations and ensures adherence to legal-procedural constraints.

---

### 💡 Why This Moves to Round 2
1.  **Subject Matter Expertise:** Leveraging law prep (**NEET/AILET/CLAT**) into a technical project makes this a unique "Legal-Tech" entry.
2.  **Resilience:** Passed deep validation after 49 iterations, ensuring a highly stable, production-ready environment.
3.  **Real-World Utility:** Designed as a scalable evaluation tool for law-firm automation.
