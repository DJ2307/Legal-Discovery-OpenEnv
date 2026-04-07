from server.app import run_baseline

if __name__ == "__main__":
    print("--- STARTING META VALIDATOR BASELINE RUN ---")
    try:
        run_baseline()
        print("--- BASELINE RUN COMPLETE ---")
    except Exception as e:
        print(f"Error during baseline run: {e}")
