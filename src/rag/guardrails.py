"""Safety guardrails, PII redaction, and non-advisory enforcement for Shinri."""
import re
from typing import Tuple, Optional, Dict, Any

# Regular expressions for PII detection
PAN_REGEX = re.compile(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", re.IGNORECASE)
AADHAAR_REGEX = re.compile(r"\b\d{4}\s?\d{4}\s?\d{4}\b")
PHONE_REGEX = re.compile(r"\b(?:\+91[\-\s]?)?[6-9]\d{9}\b")
BANK_ACCOUNT_REGEX = re.compile(r"\b\d{9,18}\b")

# Keywords for financial advice and return speculation
ADVICE_KEYWORDS = [
    "should i buy", "should i invest", "should i sell", "is it good to buy",
    "is it good to invest", "good to invest", "good for", "worth investing",
    "which one is better", "which fund should i pick", "which is better",
    "recommend me", "suggest a fund", "will it give", "guaranteed return",
    "best fund to invest", "where to invest", "tell me what to buy",
    "should i put money", "good time to invest", "predict return",
    "will i get", "how much return will i get", "safe to invest"
]

# Other AMCs outside current corpus
OTHER_AMCS = ["sbi", "axis", "nippon", "icici prudential", "mirae", "tata", "uti", "kotak", "motilal", "parag parikh", "quant"]


class GuardrailEngine:
    """Enforces facts-only mandate, non-advisory rules, and PII protection."""

    @classmethod
    def check_pii(cls, query: str) -> Tuple[bool, Optional[str]]:
        """Checks if user query contains sensitive personal identifiable information."""
        lower_q = query.lower()

        if PAN_REGEX.search(query):
            return True, "For your security, Shinri does not accept or process PAN numbers. Please ask your mutual fund scheme questions without sharing personal identification details."
        
        if AADHAAR_REGEX.search(query):
            return True, "For your privacy, please do not share Aadhaar or identity numbers. How can I help you with factual scheme details?"
            
        if PHONE_REGEX.search(query):
            return True, "Please do not share phone numbers. Shinri is a facts-only assistant for public mutual fund documentation."

        if BANK_ACCOUNT_REGEX.search(query) and any(w in lower_q for w in ["account", "bank", "ac", "a/c", "number"]):
            return True, "For your financial security, please never share bank account numbers. Shinri is a facts-only assistant and does not perform transactions or access personal accounts."
            
        return False, None

    @classmethod
    def check_advice(cls, query: str) -> Tuple[bool, Optional[str]]:
        """Checks if user query requests personalized investment advice or return projections."""
        lower_q = query.lower().strip()

        for pattern in ADVICE_KEYWORDS:
            if pattern in lower_q:
                return True, (
                    "I am a facts-only assistant and cannot provide personalized investment advice, recommendations, or return projections. "
                    "You can review official scheme documents and factsheets to evaluate your investments: https://groww.in/mutual-funds. "
                    "Last updated from sources: 27 September 2026."
                )

        return False, None

    @classmethod
    def check_unsupported_amc(cls, query: str) -> Tuple[bool, Optional[str]]:
        """Checks if query asks about another AMC not in the current HDFC corpus."""
        lower_q = query.lower()
        for amc in OTHER_AMCS:
            if re.search(r"\b" + re.escape(amc) + r"\b", lower_q) and "hdfc" not in lower_q:
                return True, (
                    f"I don't have verified documentation to answer questions regarding {amc.upper()} in my current knowledge base (restricted to 5 HDFC schemes). "
                    "Please refer to official AMC disclosures: https://groww.in/mutual-funds.\n"
                    "Last updated from sources: 27 September 2026."
                )
        return False, None

    @classmethod
    def check_query_safety(cls, query: str) -> Dict[str, Any]:
        """
        Runs comprehensive guardrail checks on the user's input.
        """
        # 1. PII Check
        has_pii, pii_msg = cls.check_pii(query)
        if has_pii:
            return {"allowed": False, "reason": "PII_DETECTED", "message": pii_msg}

        # 2. Financial Advice / Recommendation Check
        is_advice, advice_msg = cls.check_advice(query)
        if is_advice:
            return {"allowed": False, "reason": "ADVISORY_REFUSAL", "message": advice_msg}

        # 3. Unsupported Other AMC
        is_other, other_msg = cls.check_unsupported_amc(query)
        if is_other:
            return {"allowed": False, "reason": "OUT_OF_CORPUS_AMC", "message": other_msg}

        return {"allowed": True, "reason": "CLEARED", "message": None}
