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
# PHASE 2: THE ENGINE & THE GRADER
# ==========================================

def step_environment(action: LegalAction, internal_state: dict, current_obs: LegalObservation):
    reward = 0.0
    done = False
    
    if action.action_type == "gather_evidence":
        doc_name = action.document_requested
        doc_text = internal_state["current_task"]["documents"].get(doc_name, "Document not found.")
        current_obs.latest_evidence_text = f"[{doc_name}]: {doc_text}"
        if doc_name not in current_obs.gathered_documents:
            current_obs.gathered_documents.append(doc_name)
        reward = 0.40 # Discovery cost
        
    elif action.action_type == "route_case":
        if action.route_decision == internal_state["current_task"]["correct_route"]:
            reward = 0.95
        else:
            reward = 0.05 # Malpractice penalty
        done = True
        
    internal_state["current_points"] += reward
    internal_state["step_count"] += 1
    
    if internal_state["step_count"] >= 10: 
        done = True
        
    internal_state["is_done"] = done
    return current_obs, reward, done, internal_state
def grade_environment(internal_state: dict) -> float:
    # HONEST LOGIC: Did they fail to get positive points?
    if internal_state["current_points"] <= 0: 
        return 0.05  # A clean, honest failure score strictly > 0
        
    # HONEST LOGIC: Calculate based on evidence steps
    evidence_steps = max(0, internal_state["step_count"] - 1)
    raw_score = 1.0 - (evidence_steps * 0.05)
    
    # SAFETY: Clamp the score between 0.05 and 0.95 so it never touches 0 or 1
    safe_score = max(0.05, min(0.95, float(raw_score)))
    
    # PRECISION: Force Python to round to exactly 2 decimal places (e.g., 0.85)
    return round(safe_score, 2)
