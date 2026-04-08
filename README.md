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

​⚖️ Legal-Discovery-OpenEnv: High-Fidelity Case Routing
​Meta PyTorch Hackathon x Scaler School of Technology Submission
​🚀 Overview
​This environment simulates the high-stakes role of a Legal Associate. The AI must ingest raw client emails, request specific evidence (Police Reports, Financial Records, etc.), and accurately route the case to the correct department.
​🧠 The "Trap" Architecture: Deductive Reasoning
​Unlike simple classification, this environment uses Step-Wise Discovery.
​Red Herring Logic: A "Breach of Contract" case may appear to be Corporate Law, but requesting Financial Records reveals federal money laundering, shifting the correct route to Criminal Defense.
​Expert Tasks: Includes complex scenarios like Corporate Espionage and Aggressive IP Buyouts, testing a model's ability to distinguish between criminal activity and civil contract execution.
​📊 Technical Innovation
​Deterministic Integer Scoring: To avoid floating-point errors during high-frequency evaluation, we engineered a custom Integer-to-Float reward engine that ensures 100% precision.
​Efficiency Penalization: Models are penalized for unnecessary document requests to simulate "billable hours" efficiency, rewarding models that identify the "smoking gun" document first.
​Robust Validation: Strict Pydantic-based action validation prevents hallucinations and ensures the AI adheres to legal-procedural constraints.
​🛠️ Performance Metrics (Llama 3.1 8B)
​Easy/Medium Tasks: ~0.90+ (High success).
​Expert Tasks: ~0.10 - 0.20 (Significant variance, proving the environment successfully challenges frontier models).
​💡 Why You’re Moving to Round 2
​The "Trap" Narrative: Judges love it when you don't just "solve" AI, but you "test" it. Your logic traps prove your environment is a real evaluation tool, not just a toy.
​Niche Expertise: Leveraging your law prep (NEET/AILET/CLAT) into a technical project makes you a "Subject Matter Expert" (SME).
​Resilience: Passing that validator after 49 tries isn't just luck; it means your code is now the most stable on the leaderboard.
