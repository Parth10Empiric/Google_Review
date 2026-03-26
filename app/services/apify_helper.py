import requests
from app.config import APIFY_TOKEN


def abort_running_apify_runs():
    """
    Abort all currently RUNNING Apify actor runs
    to avoid memory limit errors.
    """

    base_url = "https://api.apify.com/v2/actor-runs"
    params = {"token": APIFY_TOKEN}

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        runs = data.get("data", {}).get("items", [])

        aborted_count = 0

        for run in runs:
            if run.get("status") == "RUNNING":
                run_id = run.get("id")

                abort_url = f"https://api.apify.com/v2/actor-runs/{run_id}/abort"
                requests.post(abort_url, params=params)

                print(f"❌ Aborted run: {run_id}")
                aborted_count += 1

        print(f"⚡ Total aborted runs: {aborted_count}")

    except Exception as e:
        print("❌ Error aborting runs:", str(e))
