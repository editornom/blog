"""
생성물 커밋/푸시.

[수정 사항]
1. 커밋할 변경이 없을 때 예외로 죽지 않습니다.
   기존에는 `git commit` 이 check=True 라 "nothing to commit" 에서 예외 → exit(1) →
   워크플로 실패 → `if: failure()` 로 healer 가 존재하지도 않는 빌드 오류를 고치려
   들었습니다. 정상 상황이 자기치유 트리거가 되는 구조였습니다.

2. rebase 실패를 무시하지 않습니다.
   기존에는 `git pull --rebase` 를 check=False 로 돌려 실패해도 그대로 add/commit/push
   했습니다. 충돌 상태에서 푸시가 진행될 수 있었습니다.
   이제 실패하면 rebase 를 중단하고 종료합니다.
"""

import os
import subprocess
import sys

# 자동 발행이 건드려도 되는 경로만 스테이징합니다.
STAGE_PATHS = ["src/data/blog/", "src/assets/images/", "source/", "reports/"]


def run(args, **kw):
    return subprocess.run(args, capture_output=True, text=True, **kw)


def configure_ci_identity():
    if os.getenv("GITHUB_ACTIONS") == "true":
        print("Configuring git user for GitHub Actions...")
        run(["git", "config", "user.name", "github-actions[bot]"])
        run(["git", "config", "user.email",
             "github-actions[bot]@users.noreply.github.com"])


def sync_with_remote():
    """원격과 동기화. 실패하면 rebase 를 정리하고 False 를 돌려줍니다."""
    print("Pulling latest changes with rebase...")
    r = run(["git", "pull", "--rebase", "origin", "main"])
    if r.returncode == 0:
        return True

    print(f"❌ rebase 실패:\n{r.stdout}\n{r.stderr}")
    # 충돌 상태를 남기지 않습니다. 충돌 상태로 push 가 진행되면 안 됩니다.
    run(["git", "rebase", "--abort"])
    print("   rebase 를 중단했습니다. 수동 확인이 필요합니다.")
    return False


def has_staged_changes():
    # --quiet: 차이가 있으면 exit 1
    return run(["git", "diff", "--cached", "--quiet"]).returncode != 0


def push_to_github(commit_message):
    """
    Returns:
        True  — 푸시했거나, 커밋할 것이 없어 정상 종료
        False — 실패
    """
    try:
        print(f"Running git operations for: {commit_message}")
        configure_ci_identity()

        if not sync_with_remote():
            return False

        existing = [p for p in STAGE_PATHS if os.path.exists(p.rstrip("/"))]
        if not existing:
            print("스테이징 대상 디렉터리가 없습니다. 커밋할 것이 없습니다.")
            return True

        r = run(["git", "add"] + existing)
        if r.returncode != 0:
            print(f"❌ git add 실패:\n{r.stderr}")
            return False

        if not has_staged_changes():
            # 생성물이 없는 실행(예: 파이프라인이 발행을 중단한 경우)은 정상입니다.
            print("✅ 커밋할 변경이 없습니다. 정상 종료합니다.")
            return True

        r = run(["git", "commit", "-m", commit_message])
        if r.returncode != 0:
            print(f"❌ git commit 실패:\n{r.stdout}\n{r.stderr}")
            return False

        r = run(["git", "push", "origin", "main"])
        if r.returncode != 0:
            print(f"❌ git push 실패:\n{r.stdout}\n{r.stderr}")
            return False

        print("Successfully pushed to GitHub!")
        return True

    except Exception as e:
        print(f"General Error: {e}")
        return False


if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "Auto-generate post"
    if not push_to_github(msg):
        sys.exit(1)
