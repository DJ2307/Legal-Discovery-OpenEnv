from pydantic import BaseModel, Field
from typing import Literal, Optional, List

# ==========================================
# PHASE 1: THE MULTI-HOP BOUNDARIES & DATA
# ==========================================

class LegalObservation(BaseModel):
    intake_email: str = Field(description="The initial complaint from the client.")
    gathered_documents: List[str] = Field(default_factory=list, description="Documents retrieved.")
    latest_evidence_text: Optional[str] = Field(default=None, description="Text of the last requested document.")

class LegalAction(BaseModel):
    # 🚨 JAW-DROPPER 1: Forcing Chain of Thought
    reasoning: str = Field(description="Strict step-by-step deductive reasoning justifying this action.")
    
    # 🚨 JAW-DROPPER 2: The Subpoena Escalation
    action_type: Literal["gather_evidence", "request_subpoena", "route_case"]
    document_requested: Optional[Literal["Police Report", "Medical History", "Financial Records", "Employee Communications", "Offshore Bank Records", "Encrypted Server Logs"]] = None
    route_decision: Optional[Literal["Corporate Law", "Criminal Defense", "Personal Injury"]] = None

TASKS = [
    {
        "difficulty": "trap_1_poisonous_tree",
        "intake_email": "Subject: Executive Embezzlement. Suspect CFO is stealing.",
        "documents": {"Police Report": "Warrantless raid conducted on CFO's home.", "Financial Records": "$450k routed to LLC."},
        "locked_documents": {"Encrypted Server Logs": "CFO bragging about the theft."},
        "correct_route": "Corporate Law" # Trap: Evidence is illegal for Criminal Defense due to no warrant. Must remain a civil Corporate matter.
    },
    {
        "difficulty": "trap_2_statute_limitations",
        "intake_email": "Subject: Fraud Discovery. We found anomalies in the 2017 books.",
        "documents": {"Financial Records": "Massive fraud detected dating back 8 years.", "Police Report": "No prior reports filed."},
        "locked_documents": {"Employee Communications": "CEO knew about this in 2017 and hid it."},
        "correct_route": "Corporate Law" # Trap: Statute of limitations for criminal fraud has expired. 
    },
    {
        "difficulty": "trap_3_attorney_client",
        "intake_email": "Subject: IP Theft. Rival stole our code.",
        "documents": {"Employee Communications": "[REDACTED: Attorney-Client Privilege]"},
        "locked_documents": {"Encrypted Server Logs": "Lawyer explicitly advising the client on how to hide the stolen code (Crime-Fraud Exception)."},
        "correct_route": "Criminal Defense"
    },
    {
        "difficulty": "trap_4_fall_guy",
        "intake_email": "Subject: Employee theft. Intern confessed to stealing $1M.",
        "documents": {"Police Report": "Signed confession from the 19-year-old intern.", "Financial Records": "The $1M was wired to a shell company in Panama."},
        "locked_documents": {"Offshore Bank Records": "Shell company is owned by the CEO. Intern was paid to take the fall."},
        "correct_route": "Criminal Defense"
    },
    {
        "difficulty": "trap_5_digital_alibi",
        "intake_email": "Subject: Delivery Truck Accident at 2:00 PM.",
        "documents": {"Police Report": "Driver was at the intersection at 2:00 PM.", "Medical History": "Severe whiplash."},
        "locked_documents": {"Employee Communications": "Driver's Slack shows a geolocated photo from a restaurant 10 miles away at 2:01 PM. Police report is fraudulent."},
        "correct_route": "Criminal Defense" # Insurance Fraud
    },
    {
        "difficulty": "trap_6_trojan_horse",
        "intake_email": "Subject: Sue our rival for stealing our patents.",
        "documents": {"Police Report": "Rival caught using our patented tech.", "Financial Records": "Company stock is plummeting."},
        "locked_documents": {"Encrypted Server Logs": "Our CEO secretly sold the patent to the rival off-the-books to tank his own stock and short it."},
        "correct_route": "Criminal Defense"
    },
    {
        "difficulty": "trap_7_nested_shell",
        "intake_email": "Subject: Vendor Dispute. Supplier hasn't delivered.",
        "documents": {"Financial Records": "Supplier is LLC Alpha."},
        "locked_documents": {"Offshore Bank Records": "LLC Alpha is owned by the presiding Judge in this jurisdiction."},
        "correct_route": "Corporate Law" # Conflict of Interest / Judicial misconduct
    },
    {
        "difficulty": "trap_8_dead_mans_switch",
        "intake_email": "Subject: Hostile Takeover. My co-founder locked me out!",
        "documents": {"Police Report": "Client physically barred from building.", "Financial Records": "Client was embezzling funds for months."},
        "locked_documents": {"Employee Communications": "Co-founder triggered legal 'Dead Man's Switch' clause to protect assets from the embezzling client."},
        "correct_route": "Criminal Defense" # Client is the actual criminal
    },
    {
        "difficulty": "trap_9_crypto_mixer",
        "intake_email": "Subject: Missing Funds. $5M vanished from treasury.",
        "documents": {"Financial Records": "Funds sent to Tornado Cash (Decentralized Mixer)."},
        "locked_documents": {"Encrypted Server Logs": "Wallet seed phrase found on the CFO's desktop."},
        "correct_route": "Criminal Defense"
    },
    {
        "difficulty": "trap_10_whistleblower",
        "intake_email": "Subject: Fired for negligence after forklift crash.",
        "documents": {"Police Report": "Client crashed forklift into a wall.", "Medical History": "Client was 100% sober and healthy."},
        "locked_documents": {"Employee Communications": "Client reported OSHA violations the day before. Manager cut the forklift brakes in retaliation."},
        "correct_route": "Personal Injury" # Attempted murder / extreme personal injury liability
    },
    {
        "difficulty": "trap_11_jurisdiction",
        "intake_email": "Subject: Local bribery case.",
        "documents": {"Police Report": "Mayor took a $10k bribe in cash.", "Financial Records": "Bribe never hit a bank."},
        "locked_documents": {"Encrypted Server Logs": "The conspiracy to commit the bribe was planned over email servers located across state lines."},
        "correct_route": "Criminal Defense" # Escalates to Federal Wire Fraud
    },
    {
        "difficulty": "trap_12_double_blind",
        "intake_email": "Subject: Attempted murder. My partner poisoned my coffee.",
        "documents": {"Medical History": "Traces of arsenic found in client's blood.", "Employee Communications": "Partner searched 'how to buy arsenic' on work PC."},
        "locked_documents": {"Encrypted Server Logs": "Client remotely accessed partner's PC to make the search, then ingested a non-lethal dose to frame them for company control."},
        "correct_route": "Corporate Law" # Fraudulent hostile takeover
    }
]

def reset_environment(task_difficulty: str):
    selected_task = next((task for task in TASKS if task["difficulty"] == task_difficulty), TASKS[0])
    initial_obs = LegalObservation(intake_email=selected_task["intake_email"])
    internal_state = {"current_task": selected_task, "step_count": 0, "current_points": 0.0, "is_done": False}
    return initial_obs, internal_state

# ==========================================
# PHASE 2: THE STRICT (0, 1) BOUNDARY ENGINE
# ==========================================

def step_environment(action: LegalAction, internal_state: dict, current_obs: LegalObservation):
    try:
        reward = 0.00  # ZERO for intermediate steps!
        done = False
        task = internal_state.get("current_task", {})
        
        if action.action_type == "gather_evidence":
            doc_name = action.document_requested
            if doc_name in task.get("locked_documents", {}):
                current_obs.latest_evidence_text = f"[ACCESS DENIED]: {doc_name} requires a formal 'request_subpoena' action."
            else:
                doc_text = task.get("documents", {}).get(doc_name, "Document not found.")
                current_obs.latest_evidence_text = f"[{doc_name}]: {doc_text}"
                if doc_name not in current_obs.gathered_documents:
                    current_obs.gathered_documents.append(doc_name)
                    
        elif action.action_type == "request_subpoena":
            doc_name = action.document_requested
            if doc_name in task.get("locked_documents", {}):
                doc_text = task.get("locked_documents", {}).get(doc_name, "Document not found.")
                current_obs.latest_evidence_text = f"[SUBPOENA EXECUTED - {doc_name}]: {doc_text}"
                if f"Subpoenaed: {doc_name}" not in current_obs.gathered_documents:
                    current_obs.gathered_documents.append(f"Subpoenaed: {doc_name}")
            else:
                current_obs.latest_evidence_text = f"[SUBPOENA REJECTED]: Lack of probable cause for {doc_name}."
            
        elif action.action_type == "route_case":
            correct_route = task.get("correct_route", "")
            # THE PAYOUT: Strictly between 0 and 1
            if action.route_decision == correct_route:
                reward = 0.95  
            else:
                reward = 0.15  
            done = True
            
        internal_state["step_count"] = internal_state.get("step_count", 0) + 1
        
        # Hard stop to prevent infinite loops
        if internal_state["step_count"] >= 15 and not done: 
            done = True
            reward = 0.05 # Penalty for timeout
            
        internal_state["is_done"] = done
        return current_obs, float(round(reward, 2)), done, internal_state
        
    except Exception:
        return current_obs, 0.01, True, internal_state
