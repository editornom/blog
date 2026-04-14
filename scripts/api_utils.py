import time
import threading
import logging
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type, before_sleep_log
from google.api_core import exceptions

# 로깅 설정: 재시도 시도를 콘솔에서 확인 가능하도록 함
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GeminiAPI")

class TokenBucket:
    """
    간단한 토큰 버킷 방식의 속도 제한기 (RPM 제어용).
    """
    def __init__(self, rpm=10):
        self.capacity = rpm
        self.tokens = float(rpm)
        self.last_refill = time.time()
        self.lock = threading.Lock()
        self.refill_rate = rpm / 60.0 # 초당 충전되는 토큰 수

    def consume(self, count=1):
        with self.lock:
            now = time.time()
            # 경과 시간에 따라 토큰 충전
            passed = now - self.last_refill
            self.tokens = min(float(self.capacity), self.tokens + passed * self.refill_rate)
            self.last_refill = now

            if self.tokens >= count:
                self.tokens -= count
                return True
            else:
                # 토큰이 부족하면 필요한 만큼 대기
                wait_time = (count - self.tokens) / self.refill_rate
                if wait_time > 0:
                    time.sleep(wait_time)
                # 재귀 호출로 충전 후 소비
                self.last_refill = time.time()
                self.tokens = 0
                return True

# 전역 속도 제한기 설정 (Gemini Flash 무료 티어 권장 상한선인 15 RPM 보다 낮은 12 RPM으로 설정)
gemini_limiter = TokenBucket(rpm=12)

# 지수 백오프 기반 재시도 데코레이터
# 429(ResourceExhausted), 503(ServiceUnavailable), 500(InternalServerError), 504(DeadlineExceeded) 대응
gemini_retry = retry(
    wait=wait_exponential(multiplier=2, min=5, max=60),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type((
        exceptions.ResourceExhausted,
        exceptions.ServiceUnavailable,
        exceptions.InternalServerError,
        exceptions.DeadlineExceeded
    )),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True
)
