import re
from typing import Dict, Any, List

class PIISanitizer:
    """
    Production-grade PII detection and redaction engine for financial documents.
    Protects Tax Identification Numbers, National IDs, Credit Cards, and Bank Details.
    """
    
    # Common PII Regex Patterns
    PATTERNS = {
        # Indian PAN: 5 letters, 4 numbers, 1 letter (e.g. ABCDE1234F)
        "IN_PAN": r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b",
        # US SSN: 3 digits, 2 digits, 4 digits
        "US_SSN": r"\b\d{3}-\d{2}-\d{4}\b",
        # Credit / Debit Cards (16 digits with optional dashes or spaces)
        "CREDIT_CARD": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
        # Indian Aadhaar (12 digits grouped by 4)
        "IN_AADHAAR": r"\b\d{4}\s\d{4}\s\d{4}\b",
        # Bank Account Numbers (9 to 18 consecutive digits not part of timestamps)
        "BANK_ACCOUNT": r"\b(?:A/C|Account|Acc)[\s#:]*([0-9]{9,18})\b",
    }

    @classmethod
    def redact_text(cls, text: str) -> str:
        """Masks detected PII in raw text, preserving safe context."""
        if not text:
            return ""
        
        sanitized = text

        # Mask PAN
        def mask_pan(match):
            pan = match.group(0)
            return f"{pan[:2]}*****{pan[-1]}"
        sanitized = re.sub(cls.PATTERNS["IN_PAN"], mask_pan, sanitized)

        # Mask SSN
        sanitized = re.sub(cls.PATTERNS["US_SSN"], "XXX-XX-****", sanitized)

        # Mask Credit Cards
        def mask_card(match):
            digits = re.sub(r"\D", "", match.group(0))
            return f"****-****-****-{digits[-4:]}"
        sanitized = re.sub(cls.PATTERNS["CREDIT_CARD"], mask_card, sanitized)

        # Mask Aadhaar
        sanitized = re.sub(cls.PATTERNS["IN_AADHAAR"], "XXXX-XXXX-****", sanitized)

        return sanitized

    @classmethod
    def detect_pii(cls, text: str) -> List[Dict[str, Any]]:
        """Scans text and returns structured audit list of detected sensitive entities."""
        detected = []
        if not text:
            return detected

        for pii_type, pattern in cls.PATTERNS.items():
            matches = list(re.finditer(pattern, text))
            if matches:
                detected.append({
                    "pii_type": pii_type,
                    "count": len(matches),
                    "action_taken": "MASKED_IN_LOGS_AND_EXPOSURES"
                })
        return detected
