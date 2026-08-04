"""
모델 ID 중앙 관리.

이전에는 gemini-3-flash-preview / gemini-2.5-flash / gemini-2.0-flash / gemini-3 이
스크립트 19곳에 하드코딩되어 있었고, 그중 대부분이 preview 모델이었습니다.
preview 모델은 예고 없이 동작이 바뀌거나 종료될 수 있으므로 기본값은 안정 버전을 씁니다.

바꾸고 싶으면 .env 에서 한 줄만 고치면 됩니다:
    GEMINI_MODEL=models/gemini-3-flash-preview
"""

import os

# 기본값은 안정 모델. api_utils 의 Fallback Watchdog 도 이 모델을 최후 보루로 씁니다.
_STABLE = "models/gemini-2.5-flash"


def _resolve(env_key: str, default: str) -> str:
    value = (os.getenv(env_key) or "").strip()
    return value if value else default


# 본문 집필 / 조사 / 검증 등 품질이 중요한 호출
MAIN = _resolve("GEMINI_MODEL", _STABLE)

# 슬러그·메타 디스크립션·alt 태그처럼 짧고 기계적인 호출
FAST = _resolve("GEMINI_MODEL_FAST", _STABLE)

# 번역
TRANSLATE = _resolve("GEMINI_MODEL_TRANSLATE", MAIN)


def summary() -> str:
    return f"main={MAIN} fast={FAST} translate={TRANSLATE}"
