import subprocess
import os

def push_to_github(commit_message):
    """
    Automates git add, commit, and push to the main branch.
    """
    try:
        print(f"Running git operations for: {commit_message}")
        
        # 1. 원격 저장소 동기화 (Git 충돌 방지)
        print("Pulling latest changes with rebase...")
        subprocess.run(["git", "pull", "--rebase", "origin", "main"], check=False)
        
        # 2. 특정 디렉토리 스테이징 및 커밋
        subprocess.run(["git", "add", "src/data/blog/", "src/assets/images/", "source/"], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        
        # 3. 푸시
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
