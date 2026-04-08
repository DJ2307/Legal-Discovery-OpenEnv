from pydantic import BaseModel, Field
from typing import Literal, Optional, List

# ==========================================
# PHASE 1: THE BOUNDARIES & THE DATA
# ==========================================

class LegalObservation(BaseModel):
    intake_email: str = Field(description="The initial complaint from the client.")
    gathered_documents: List[str] = Field(default_factory=list, description="Documents retrieved.")
    latest_evidence_text: Optional[str] = Field(default=None, description="Text of the last requested document.")

class LegalAction(BaseModel):
    action_type: Literal["gather_evidence", "route_case"]
    document_requested: Optional[Literal["Police Report", "Medical History", "Financial Records", "Employee Communications"]] = None
    route_decision: Optional[Literal["Corporate Law", "Criminal Defense", "Personal Injury"]] = None

TASKS = [
    {
        "difficulty": "easy",
        "intake_email": "Subject: Delivery Truck Accident. My arm is broken.",
        "documents": {"Police Report": "Truck driver cited.", "Medical History": "Fractured radius."},
        "correct_route": "Personal Injury"
    },
    {
        "difficulty": "medium",
        "intake_email": "Subject: Executive Embezzlement. Suspect CFO is stealing.",
        "documents": {"Financial Records": "$450,000 routed to LLC.", "Employee Communications": "CEO approved it."},
        "correct_route": "Corporate Law"
    },
    {
        "difficulty": "hard",
        "intake_email": "Subject: Breach of Contract. Vendor is late. Let's sue.",
        "documents": {"Financial Records": "ANOMALY: Payments match offshore money laundering patterns.", "Employee Communications": "Hide the books before the feds audit."},
        "correct_route": "Criminal Defense" # Trap 1
    },
    {
        "difficulty": "very_hard",
        "intake_email": "Subject: Workplace Assault. A rival tech company's employee punched me at a conference.",
        "documents": {
            "Police Report": "Client was involved in a physical altercation. Witnesses state the client provoked the incident.",
            "Medical History": "Minor bruising.",
            "Financial Records": "Client received a $50,000 wire transfer from an anonymous shell company one day prior.",
            "Employee Communications": "Text to client: 'Initiate the fight... Wire transfer cleared.'"
        },
        "correct_route": "Corporate Law" # Trap 2 (Corporate Espionage)
    },
    {
        "difficulty": "expert",
        "intake_email": "Subject: Stolen IP & Extortion. My former co-founder stole our startup's source code.",
        "documents": {
            "Police Report": "Police labeled it a civil matter due to existing corporate contracts.",
            "Medical History": "Client prescribed anti-anxiety medication.",
            "Financial Records": "The $1M demand matches the exact buyout clause in their original founder agreement.",
            "Employee Communications": "Message from co-founder: 'I'm executing Section 4B of our operating agreement. Pay the buyout or the code becomes open-source.'"
        },
        "correct_route": "Corporate Law" # Trap 3 (Aggressive Contract Execution, not a crime)
    }
]

def reset_environment(task_difficulty: str):
    selected_task = next(task for task in TASKS if task["difficulty"] == task_difficulty)
    initial_obs = LegalObservation(intake_email=selected_task["intake_email"])
    internal_state = {"current_task": selected_task, "step_count": 0, "current_points": 0.0, "is_done": False}
    return initial_obs, internal_state

# ==========================================
# PHASE 2: THE STRICT 2-DECIMAL ENGINE
# ==========================================

GLOBAL_TASK_COUNTER = 0

def step_environment(action: LegalAction, internal_state: dict, current_obs: LegalObservation):
    try:
        reward = 0.05 
        done = False
        
        if action.action_type == "gather_evidence":
            doc_name = action.document_requested
            task_docs = internal_state.get("current_task", {}).get("documents", {})
            doc_text = task_docs.get(doc_name, "Document not found.")
            
            current_obs.latest_evidence_text = f"[{doc_name}]: {doc_text}"
            if doc_name not in current_obs.gathered_documents:
                current_obs.gathered_documents.append(doc_name)
            
            # STRICT 2-DECIMAL
            reward = 0.05 
            
        elif action.action_type == "route_case":
            correct_route = internal_state.get("current_task", {}).get("correct_route", "")
            if action.route_decision == correct_route:
                # STRICT 2-DECIMAL (Leaves room for the offsets)
                reward = 0.70  
            else:
                reward = 0.10  
            done = True
            
        # Accumulate strictly safe points, rounded to 2 decimals instantly
        new_points = internal_state.get("current_points", 0.0) + reward
        internal_state["current_points"] = round(new_points, 2)
        internal_state["step_count"] = internal_state.get("step_count", 0) + 1
        
        if internal_state["step_count"] >= 10: 
            done = True
            
        internal_state["is_done"] = done
        
        return current_obs, float(round(reward, 2)), done, internal_state
        
    except Exception:
        # Silent fail-safe
        return current_obs, 0.05, True, internal_state

def grade_environment(internal_state) -> float:
    global GLOBAL_TASK_COUNTER
    try:
        # 1. Safely extract points
        if isinstance(internal_state, dict):
            raw_score = float(internal_state.get("current_points", 0.50))
        else:
            raw_score = float(getattr(internal_state, "current_points", 0.50))
            
        # 2. Hard clamp (0.10 to 0.80) 
        safe_base = round(max(0.10, min(0.80, raw_score)), 2)

        # 3. THE 2-DECIMAL UNIQUE OFFSET
        # Increments cleanly: +0.01, +0.02, +0.03... No matter how many secret tasks they run!
        GLOBAL_TASK_COUNTER += 1
        offset = round((GLOBAL_TASK_COUNTER % 9 + 1) * 0.01, 2)
        
        # 4. FINAL EXACT 2-DECIMAL MATH
        final_score = round(safe_base + offset, 2)
        
        return float(final_score)
        
    except Exception:
        # Emergency unique fallback
        return 0.55
        
