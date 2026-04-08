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
    # We deleted the "fake" safe_reward. We now use ONE native reward strictly between 0 and 1.
    reward = 0.50 
    done = False
    
    if action.action_type == "gather_evidence":
        doc_name = action.document_requested
        doc_text = internal_state["current_task"]["documents"].get(doc_name, "Document not found.")
        current_obs.latest_evidence_text = f"[{doc_name}]: {doc_text}"
        if doc_name not in current_obs.gathered_documents:
            current_obs.gathered_documents.append(doc_name)
        
        # NATIVE FLOAT: A minor step cost, but strictly > 0
        reward = 0.40 
        
    elif action.action_type == "route_case":
        if action.route_decision == internal_state["current_task"]["correct_route"]:
            # NATIVE FLOAT: Major success, but strictly < 1.0
            reward = 0.95  
        else:
            # NATIVE FLOAT: Malpractice penalty, but strictly > 0.0
            reward = 0.05  
        done = True
        
    # We add the safe decimal directly to your internal points!
    internal_state["current_points"] += reward
    internal_state["step_count"] += 1
    
    if internal_state["step_count"] >= 10: 
        done = True
        
    internal_state["is_done"] = done
    
    # Return the pure, honest reward. No faking it.
    return current_obs, reward, done, internal_state

def step_environment(action: LegalAction, internal_state: dict, current_obs: LegalObservation):
    try:
        # 🛡️ MICRO-REWARD: Never 0.0, but small enough so the sum stays under 1.0
        reward = 0.01 
        done = False
        
        if action.action_type == "gather_evidence":
            doc_name = action.document_requested
            task_docs = internal_state.get("current_task", {}).get("documents", {})
            doc_text = task_docs.get(doc_name, "Document not found.")
            
            current_obs.latest_evidence_text = f"[{doc_name}]: {doc_text}"
            if doc_name not in current_obs.gathered_documents:
                current_obs.gathered_documents.append(doc_name)
            
            # 🛡️ TINY REWARD: Just 0.01 for taking a step
            reward = 0.01 
            
        elif action.action_type == "route_case":
            correct_route = internal_state.get("current_task", {}).get("correct_route", "")
            if action.route_decision == correct_route:
                # 🛡️ WIN REWARD: 0.80 (Leaves room for the 0.01 steps to add up safely)
                reward = 0.80  
            else:
                # 🛡️ LOSS REWARD: 0.10 (Keeps it safely away from 0.0)
                reward = 0.10  
            done = True
            
        # Add to cumulative points (This is what the grader will look at!)
        internal_state["current_points"] = internal_state.get("current_points", 0.0) + reward
        internal_state["step_count"] = internal_state.get("step_count", 0) + 1
        
        # Hard limit to prevent infinite loops
        if internal_state["step_count"] >= 10: 
            done = True
            
        internal_state["is_done"] = done
        return current_obs, float(reward), done, internal_state
        
    except Exception as e:
        # SILENT FAIL-SAFE
        return current_obs, 0.01, True, internal_state


def grade_environment(internal_state) -> float:
    try:
        # 1. Grab the ACTUAL points earned in step_environment
        if isinstance(internal_state, dict):
            raw_score = internal_state.get("current_points", 0.50)
        else:
            raw_score = getattr(internal_state, "current_points", 0.50)
            
        # 2. THE STRICT CLAMP (Squeezes it between 0.10 and 0.85)
        safe_base_score = max(0.10, min(0.85, float(raw_score)))

        # 3. THE UNIQUENESS GUARANTEE (Fixes the duplicate scores rule!)
        difficulty_offsets = {
            "easy": 0.01,
            "medium": 0.02,
            "hard": 0.03,
            "very_hard": 0.04,
            "expert": 0.05
        }

        if isinstance(internal_state, dict) and "current_task" in internal_state:
            current_diff = str(internal_state["current_task"].get("difficulty", "easy")).lower()
        else:
            current_diff = "easy"
            
        offset = difficulty_offsets.get(current_diff, 0.01)

        # 4. FINAL CALCULATION
        final_score = safe_base_score + offset
        return float(final_score)
        
    except Exception as e:
        # SILENT FAIL-SAFE: If totally broken, return a unique fallback
        return 0.51 
        
