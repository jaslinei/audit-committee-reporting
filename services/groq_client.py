import os
import time
import logging
from collections import deque
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class GroqClient:
    MODEL = "llama-3.3-70b-versatile"
    MAX_RETRIES = 3

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "GROQ_API_KEY is not set. "
                "Copy .env.example → .env and add your key from console.groq.com"
            )
        self.client = Groq(api_key=api_key)
        # Rolling window of last 10 response times (ms) for /health stats
        self._response_times: deque[float] = deque(maxlen=10)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def call(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 1000,
    ) -> str | None:
        """
        Call the Groq LLM with up to 3 retries and exponential backoff.

        Args:
            system_prompt: Role/instructions for the model.
            user_prompt:   The actual input from the application.
            temperature:   0.2–0.3 for factual/structured tasks,
                           0.5–0.7 for creative/generative tasks.
            max_tokens:    Maximum tokens in the response (default 1000).

        Returns:
            The model's response string, or None if all retries failed.
            Callers MUST handle None and return a fallback response —
            never propagate None to the HTTP response body.
        """
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                t_start = time.time()

                response = self.client.chat.completions.create(
                    model=self.MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user",   "content": user_prompt},
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

                elapsed_ms = (time.time() - t_start) * 1000
                self._response_times.append(elapsed_ms)

                content = response.choices[0].message.content
                tokens  = response.usage.total_tokens

                logger.info(
                    "Groq call succeeded | attempt=%d model=%s tokens=%d time=%.0fms",
                    attempt, self.MODEL, tokens, elapsed_ms,
                )
                return content

            except Exception as exc:
                wait = 2 ** attempt  # 2s, 4s, 8s
                logger.warning(
                    "Groq call failed | attempt=%d/%d error=%s retrying_in=%ds",
                    attempt, self.MAX_RETRIES, exc, wait,
                )
                if attempt < self.MAX_RETRIES:
                    time.sleep(wait)

        logger.error(
            "Groq call failed after %d attempts — returning None for fallback",
            self.MAX_RETRIES,
        )
        return None

    # ------------------------------------------------------------------
    # Stats helpers (used by /health endpoint)
    # ------------------------------------------------------------------

    @property
    def avg_response_time_ms(self) -> float:
        """Average of the last 10 response times in milliseconds."""
        if not self._response_times:
            return 0.0
        return round(sum(self._response_times) / len(self._response_times), 1)

    @property
    def model_name(self) -> str:
        return self.MODEL


# ---------------------------------------------------------------------------
# Singleton — import this everywhere:
#   from services.groq_client import groq_client
# ---------------------------------------------------------------------------
groq_client = GroqClient()
#############################################################################