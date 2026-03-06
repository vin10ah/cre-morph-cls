# back/app/services/predictor.py
from __future__ import annotations

import random
from typing import Dict, List, Literal

Label = Literal["REAL", "MORPH", "UNCERTAIN"]

def _softmax(xs: List[float]) -> List[float]:
    # simple stable softmax
    m = max(xs)
    exps = [pow(2.718281828, x - m) for x in xs]
    s = sum(exps)
    return [e / s for e in exps]

def predict_stub(image_bytes: bytes) -> Dict:
    """
    모델이 없을 때 사용하는 스텁 예측기.
    - 항상 3개 후보(candidates)를 score desc로 반환
    - final은 candidates[0]을 사용
    """
    # 이미지 bytes 길이에 따라 조금이라도 변동을 주고 싶으면 seed에 사용
    seed = len(image_bytes) % 10_000
    rnd = random.Random(seed)

    labels: List[Label] = ["REAL", "MORPH", "UNCERTAIN"]

    # 랜덤 로그릿 생성 -> softmax -> 확률
    logits = [rnd.uniform(-1.0, 1.0) for _ in labels]
    probs = _softmax(logits)

    candidates = [
        {"label": label, "score": float(prob)}
        for label, prob in zip(labels, probs)
    ]
    candidates.sort(key=lambda x: x["score"], reverse=True)

    final = {"label": candidates[0]["label"], "score": candidates[0]["score"]}

    return {
        "final": final,
        "candidates": candidates,
        "model_version": "stub-v0",
    }