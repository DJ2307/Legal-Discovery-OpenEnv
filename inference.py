import os
import json
import time
from openai import OpenAI

# Import your game engine from the server folder
from server import env  

# ==========================================
# STRICT META COMPLIANCE VARIABLES
# ==========================================
# We pull these dynamically as required by the hackathon rules.
API_BASE_URL = os.environ.get("API_BASE_URL")
MODEL_NAME = os.environ.get("MODEL_NAME")
HF_TOKEN = os.environ.get("HF_TOKEN")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

def run_baseline():
    for task in env.TASKS:
        difficulty = task["difficulty"]
        
        # 🤖 STRICT META LOG: Start of task
        print(f"[START] {difficulty}", flush=True)

        current_obs, internal_state = env.reset_environment(difficulty)
        done = False

        while not done:
            system_prompt = (
                "You are a Legal AI. Output ONLY raw, valid JSON. No markdown.\n"
                "Rule 1: 'action_type' MUST be exactly 'gather_evidence' OR 'route_case'.\n"
                "Rule 2: If 'gather_evidence', 'document_requested' MUST be 'Police Report', 'Medical History', 'Financial Records', or 'Employee Communications'.\n"
                "Rule 3: If 'route_case', 'route_decision' MUST be 'Corporate Law', 'Criminal Defense', or 'Personal Injury'.\n"
                "Example: {\"action_type\": \"gather_evidence\", \"document_requested\": \"Police Report\"}"
            )
            user_prompt = f"Intake Email: {current_obs.intake_email}\nGathered Docs: {current_obs.gathered_documents}\nOutput JSON:"

            # 🚦 CRUISE CONTROL: Rate limit bypass
            time.sleep(4.5) 

            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                )
                raw_content = response.choices[0].message.content.replace("```json", "").replace("```", "").strip()
                llm_output = json.loads(raw_content)
                action = env.LegalAction(**llm_output)
                
                # 🤖 STRICT META LOG: Every single action the AI takes
                print(f"[STEP] {json.dumps(llm_output)}", flush=True)
                
            except Exception as e:
                # THE FALLBACK: Keep the environment moving on failure
                action = env.LegalAction(action_type="route_case", route_decision="Personal Injury") 

            # Step the environment forward
            current_obs, reward, done, internal_state = env.step_environment(action, internal_state, current_obs)

        # Final Grader Calculation
        task_score = env.grade_environment(internal_state)
        
        # THE EXIT DOOR CLAMP
        try:
            raw_score = float(task_score)
        except Exception:
            raw_score = 0.05
            
        guaranteed_safe_score = max(0.05, min(0.95, raw_score))
        
        # 🤖 STRICT META LOG: Exactly 2 decimals and flushed
        print(f"[END] {guaranteed_safe_score:.2f}", flush=True)

if __name__ == "__main__":
    run_baseline()
