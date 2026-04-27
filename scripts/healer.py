import os
import re
import subprocess
from google import genai
from dotenv import load_dotenv

load_dotenv()

def analyze_and_fix():
    log_path = "build_log.txt"
    if not os.path.exists(log_path):
        print("No build log found. Skipping healer.")
        return

    with open(log_path, "r", encoding="utf-8") as f:
        logs = f.read()

    print("--- Analyzing Build Logs with Gemini ---")
    
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    prompt = f"""
You are a Self-Healing CI bot. A build failed with the following logs.
Analyze the logs, find the root cause (especially YAML syntax or code errors), and provide the fixed file content.

[BUILD LOGS]
{logs}

[INSTRUCTIONS]
1. Identify the file path that caused the error.
2. Provide the full corrected content of that file.
3. Output your response in the following JSON format ONLY:
{{
  "file_path": "path/to/file.md",
  "fixed_content": "full content here..."
}}
Do not include any other text or markdown formatting outside the JSON.
"""

    try:
        response = client.models.generate_content(
            model='models/gemini-2.0-flash', # Using a fast model for healing
            contents=prompt
        )
        
        import json
        # Extract JSON from response (handling potential markdown fences)
        resp_text = response.text.strip()
        if "```json" in resp_text:
            resp_text = resp_text.split("```json")[1].split("```")[0].strip()
        elif "```" in resp_text:
            resp_text = resp_text.split("```")[1].split("```")[0].strip()
            
        fix_data = json.loads(resp_text)
        file_path = fix_data['file_path']
        fixed_content = fix_data['fixed_content']

        if os.path.exists(file_path):
            print(f"Applying fix to: {file_path}")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(fixed_content)
            
            # Commit and Push
            commit_and_push(file_path)
        else:
            print(f"Error: AI suggested a file that doesn't exist: {file_path}")

    except Exception as e:
        print(f"Healer failed to fix the issue: {e}")

def commit_and_push(file_path):
    try:
        print(f"Committing fix for {file_path}...")
        
        # Git config (for CI environment)
        if os.getenv("GITHUB_ACTIONS") == "true":
            subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=True)
            subprocess.run(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"], check=True)

        subprocess.run(["git", "add", file_path], check=True)
        subprocess.run(["git", "commit", "-m", f"[Self-Healing] Fixed build error in {os.path.basename(file_path)}"], check=True)
        
        # Pull before push to avoid conflicts
        subprocess.run(["git", "pull", "--rebase", "origin", "main"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        
        print("Self-Healing fix pushed successfully!")
    except Exception as e:
        print(f"Failed to push self-healing fix: {e}")

if __name__ == "__main__":
    analyze_and_fix()
