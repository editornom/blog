import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api_utils import gemini_retry, gemini_limiter
from google.api_core import exceptions
import time

# Mock function to simulate API calls with failures
call_count = 0

@gemini_retry
def simulate_api_call(failure_type=None, fail_until=0):
    global call_count
    call_count += 1
    gemini_limiter.consume()
    print(f"[Attempt {call_count}] Calling simulated API...")
    
    if failure_type and call_count <= fail_until:
        if failure_type == "429":
            print(f"  -> Simulating 429 ResourceExhausted")
            raise exceptions.ResourceExhausted("Rate limit exceeded")
        elif failure_type == "503":
            print(f"  -> Simulating 503 ServiceUnavailable")
            raise exceptions.ServiceUnavailable("Service is busy")
    
    print("  -> Success!")
    return "OK"

def test_retry_logic():
    global call_count
    print("\n--- Testing Retry Logic (Exponential Backoff) ---")
    call_count = 0
    start_time = time.time()
    try:
        # Fail 2 times with 503, succeed on 3rd
        result = simulate_api_call(failure_type="503", fail_until=2)
        duration = time.time() - start_time
        print(f"Result: {result}, Duration: {duration:.2f}s")
    except Exception as e:
        print(f"Test failed with unexpected error: {e}")

def test_rate_limiter():
    print("\n--- Testing Rate Limiter (Token Bucket) ---")
    # Low RPM for testing
    gemini_limiter.capacity = 2
    gemini_limiter.tokens = 2
    gemini_limiter.refill_rate = 1.0 / 2.0 # 1 token every 2 seconds
    
    start_time = time.time()
    for i in range(3):
        gemini_limiter.consume()
        print(f"Call {i+1} at {time.time() - start_time:.2f}s")
    
    print(f"Total duration for 3 calls: {time.time() - start_time:.2f}s (Expected ~2s)")

if __name__ == "__main__":
    test_rate_limiter()
    test_retry_logic()
