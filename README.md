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

# ⚖️ Legal Discovery & Case Routing Simulation
**Powered by OpenEnv | Meta Llama 3 Hackathon Submission**

### 🚀 Overview
This environment simulates the high-stakes role of a Legal Associate performing discovery. The AI must ingest raw client emails, request specific evidence (Police Reports, Financial Records, etc.), and accurately route the case to the correct department: **Personal Injury**, **Corporate Law**, or **Criminal Defense**.

### 🧠 The Challenge: Logical "Trap" Design
Unlike simple classification tasks, this environment is designed with **CLAT-level deductive reasoning requirements**. We intentionally engineered "Hard" and "Expert" tasks where the initial intake email acts as a red herring. 

* **The Trap:** A "Breach of Contract" case looks like a standard Corporate Law dispute. 
* **The Reality:** Only by requesting *Financial Records* can the AI uncover patterns of federal money laundering, requiring a **Criminal Defense** routing.
* **The Scoring:** Models are penalized for every document requested to simulate "billable hours" efficiency, forcing the AI to balance thoroughness with speed.

### 📊 Performance Metrics (Llama 3.1 8B Baseline)
Our baseline testing shows significant score variance, proving the environment's robustness:
* **Easy/Medium Tasks:** ~0.90+ (High success)
* **Hard/Expert Tasks:** ~0.00 (Frontier models often fall for the red herrings without deep discovery)
* **Average Baseline Score:** **0.62 / 1.0**

### 🛠️ Technical Architecture
* **Framework:** Built on the `OpenEnv` standard.
* **Validation:** Strict Pydantic-based action validation to prevent model hallucinations.
* **Deployment:** Fully containerized via Docker for deterministic evaluation.

---
**Author:** Daksh Jain  
**Category:** Legal Tech / AI Safety & Evaluation

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
