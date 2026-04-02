import subprocess
import os

def push_to_github(commit_message):
    """
    Automates git add, commit, and push to the main branch.
    """
    try:
        print(f"Running git operations for: {commit_message}")
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("Successfully pushed to GitHub!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git Error: {e}")
        return False
    except Exception as e:
        print(f"General Error: {e}")
        return False

if __name__ == "__main__":
    # Test (safe push)
    push_to_github("test automation commit")
