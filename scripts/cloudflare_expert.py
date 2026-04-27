import os
import requests
from dotenv import load_dotenv

load_dotenv()

class CloudflareExpert:
    def __init__(self):
        self.api_token = os.getenv("CLOUDFLARE_API_TOKEN")
        self.account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        self.project_name = os.getenv("CLOUDFLARE_PROJECT_NAME")
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/pages/projects/{self.project_name}"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    def get_latest_deployments(self, count=5):
        """
        Fetches the most recent deployments for the project.
        """
        url = f"{self.base_url}/deployments"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data.get("result", [])[:count]
        except Exception as e:
            print(f"Error fetching deployments: {e}")
            return []

    def get_deployment_logs(self, deployment_id):
        """
        Fetches build logs (history) for a specific deployment.
        """
        url = f"{self.base_url}/deployments/{deployment_id}/history"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            result = data.get("result", {})
            # FULL DEBUG DUMP for failed deployment
            import json
            print(f"DEBUG FULL RESULT: {json.dumps(result, indent=2)}")
            
            stages = result.get("stages", [])
            full_logs = []
            for stage in stages:
                name = stage.get("name", "Unknown Step")
                status = stage.get("status", "unknown")
                full_logs.append(f"--- Stage: {name} ({status.upper()}) ---")
                
            return "\n".join(full_logs)
        except Exception as e:
            print(f"Error fetching logs for {deployment_id}: {e}")
            return None

    def get_last_failed_deployment(self):
        """
        Finds the most recent deployment that failed.
        """
        deployments = self.get_latest_deployments(count=10)
        for d in deployments:
            if d.get("latest_stage", {}).get("status") == "failure":
                return d
        return None

if __name__ == "__main__":
    expert = CloudflareExpert()
    print("Checking connection to Cloudflare Pages...")
    deps = expert.get_latest_deployments(count=3)
    if deps:
        print(f"Successfully fetched {len(deps)} deployments.")
        for d in deps:
            status = d.get("latest_stage", {}).get("status")
            created = d.get("created_on")
            print(f"- ID: {d['id']} | Status: {status} | Created: {created}")
            
            if status == "failure":
                print(f"  Fetching logs for failed build {d['id']}...")
                logs = expert.get_deployment_logs(d['id'])
                print(f"  --- LOGS ---\n{logs}\n-----------")
    else:
        print("Failed to fetch deployments. Please check your credentials.")
