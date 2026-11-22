"""Conversation memory and follow-up query rewriting."""
import re
from typing import List, Dict, Any

SCHEME_PATTERNS = {
    "large cap": "HDFC Large Cap Fund Direct Plan - Growth",
    "top 100": "HDFC Large Cap Fund Direct Plan - Growth",
    "flexi cap": "HDFC Flexi Cap Fund Direct Plan - Growth",
    "equity fund": "HDFC Flexi Cap Fund Direct Plan - Growth",
    "elss": "HDFC ELSS Tax saver Fund Direct Plan - Growth",
    "tax saver": "HDFC ELSS Tax saver Fund Direct Plan - Growth",
    "small cap": "HDFC Small Cap Fund Direct Plan - Growth",
    "balanced advantage": "HDFC Balanced Advantage Fund Direct Plan - Growth",
    "hybrid": "HDFC Balanced Advantage Fund Direct Plan - Growth"
}

PRONOUN_TRIGGERS = [
    "its", "this fund", "that fund", "the fund", "same fund",
    "it", "and for it", "for this", "what about its"
]


class ConversationMemory:
    """Maintains a sliding window of the last 10 messages and rewrites follow-ups."""

    def __init__(self, max_history: int = 10):
        self.max_history = max_history
        self.messages: List[Dict[str, str]] = []

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]

    def clear(self):
        self.messages = []

    def get_history(self) -> List[Dict[str, str]]:
        return list(self.messages)

    def extract_last_active_scheme(self) -> str:
        """Finds the most recently mentioned scheme from the message history."""
        for msg in reversed(self.messages):
            text = msg["content"].lower()
            for key, full_name in SCHEME_PATTERNS.items():
                if key in text:
                    return full_name
        return "HDFC Mutual Fund"

    def rewrite_query(self, query: str) -> str:
        """
        Rewrites ambiguous follow-up questions using conversational context.
        Example: 'What is its exit load?' -> 'What is the exit load for HDFC ELSS Tax saver Fund?'
        """
        lower_q = query.lower()
        has_pronoun = any(re.search(r"\b" + re.escape(p) + r"\b", lower_q) for p in PRONOUN_TRIGGERS)

        # Check if the query already explicitly mentions a scheme
        has_explicit_scheme = any(key in lower_q for key in SCHEME_PATTERNS)

        if has_pronoun and not has_explicit_scheme:
            last_scheme = self.extract_last_active_scheme()
            # Replace pronouns with the explicit scheme name
            rewritten = query
            for p in PRONOUN_TRIGGERS:
                rewritten = re.sub(r"\b" + re.escape(p) + r"\b", f"for {last_scheme}", rewritten, flags=re.IGNORECASE)
            return rewritten.strip()

        # If it's a very short query without subject (e.g., 'minimum sip?', 'exit load?')
        if len(query.split()) <= 4 and not has_explicit_scheme and self.messages:
            last_scheme = self.extract_last_active_scheme()
            return f"{query} for {last_scheme}"

        return query
