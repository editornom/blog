import subprocess
import time
import sys

schedules = ["12_tech_feature", "15_ai_news", "18_ai_feature", "09_tech_news"]
cycles = 3

# Windows terminal encoding fix
sys.stdout.reconfigure(encoding='utf-8')

print(f"Starting {cycles} cycles of {schedules}...")

for i in range(cycles):
    print(f"\n{'='*40}")
    print(f"🔄 CYCLE {i+1} / {cycles}")
    print(f"{'='*40}")
    for sched in schedules:
        print(f"\n▶️ Running schedule: {sched} (Cycle {i+1})")
        
        # Run main.py
        result = subprocess.run(["python", "scripts/main.py", "--schedule", sched], encoding='utf-8')
        
        if result.returncode != 0:
            print(f"⚠️ Warning: main.py exited with code {result.returncode} for {sched}")
        
        print(f"⏳ Waiting 15 seconds before next run to avoid rate limits...")
        time.sleep(15)

print("\n🚀 All cycles completed! Pushing to GitHub...")
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", f"Auto: Generated {cycles} cycles of posts"])
subprocess.run(["git", "push"])
print("✅ Done!")
