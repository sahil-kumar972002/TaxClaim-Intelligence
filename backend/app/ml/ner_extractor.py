import re
from typing import Dict, Any, List, Optional
from datetime import datetime

class EntityExtractor:
    """
    Robust Named Entity Recognition & Regex extraction for financial documents:
    Receipts, Invoices, Cloud Statements, Broadband Bills, and Flight Itineraries.
    """

    CURRENCY_SYMBOLS = {
        "₹": "INR", "rs": "INR", "inr": "INR",
        "$": "USD", "usd": "USD",
        "€": "EUR", "eur": "EUR",
        "£": "GBP", "gbp": "GBP"
    }

    DATE_PATTERNS = [
        # YYYY-MM-DD
        r"\b(20\d{2})[-/](0[1-9]|1[0-2])[-/](0[1-9]|[12]\d|3[01])\b",
        # DD/MM/YYYY or DD-MM-YYYY
        r"\b(0[1-9]|[12]\d|3[01])[-/.](0[1-9]|1[0-2])[-/.](20\d{2})\b",
        # MM/DD/YYYY
        r"\b(0[1-9]|1[0-2])[-/.](0[1-9]|[12]\d|3[01])[-/.](20\d{2})\b",
        # Month name e.g. 15 Oct 2024 or October 15, 2024
        r"\b(0[1-9]|[12]\d|3[01])\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,]+(20\d{2})\b",
    ]

    INVOICE_PATTERNS = [
        r"(?i)(?:invoice|bill|receipt|tax\s+invoice|ref)[\s#.:-]*([A-Z0-9][A-Z0-9\-_/]{3,24})\b",
        r"(?i)\b(?:inv|tax-inv)[\s#.:-]*([A-Z0-9\-_/]{4,20})\b",
        r"\b([A-Z]{2,4}[/-]\d{4,8})\b"
    ]

    TOTAL_PATTERNS = [
        r"(?i)(?:total|grand\s*total|amount\s*payable|net\s*amount|balance\s*due)[\s:₹$EURs.]*([0-9]{1,3}(?:,[0-9]{2,3})*(?:\.[0-9]{2})?)",
        r"(?i)(?:total)[\s]*[:=]?[\s]*([0-9]+(?:\.[0-9]{2})?)",
        r"(?:₹|\$|Rs\.?)\s*([0-9]{1,3}(?:,[0-9]{2,3})*(?:\.[0-9]{2})?)"
    ]

    TAX_PATTERNS = [
        r"(?i)(?:gst|cgst\s*\+\s*sgst|igst|tax\s*amount|vat|sales\s*tax)[\s:₹$EURs.]*([0-9]{1,3}(?:,[0-9]{2,3})*(?:\.[0-9]{2})?)",
        r"(?i)(?:tax)[\s]*[:=]?[\s]*([0-9]+(?:\.[0-9]{2})?)"
    ]

    KNOWN_MERCHANTS = [
        "Apple Store", "Adobe Systems", "Amazon Web Services", "GitHub", "JetBrains",
        "Google Cloud Platform", "Jio Fiber", "Airtel Broadband", "Uber India", "Ola Cabs",
        "IndiGo Airlines", "The Bombay Canteen", "Starbucks Coffee", "Herman Miller",
        "IKEA India", "Coursera", "Udemy", "WeWork India", "Staples", "Dell Technologies"
    ]

    def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extracts structured invoice/receipt metadata from text."""
        if not text:
            return self._empty_result()

        merchant = self._extract_merchant(text)
        date_str = self._extract_date(text)
        amount, currency = self._extract_amount(text)
        tax_amount = self._extract_tax(text)
        invoice_no = self._extract_invoice_number(text)
        line_items = self._extract_line_items(text)

        # Fallback tax amount estimation if not parsed explicitly
        if tax_amount == 0.0 and amount > 0:
            if currency == "INR":
                tax_amount = round(amount * 0.18 / 1.18, 2)  # Standard 18% GST reverse calculate
            elif currency == "USD":
                tax_amount = round(amount * 0.0825, 2)

        return {
            "merchant": merchant,
            "transaction_date": date_str,
            "amount": amount,
            "currency": currency,
            "tax_amount": tax_amount,
            "invoice_number": invoice_no,
            "line_items": line_items,
            "ocr_confidence": 0.94 if (merchant and amount > 0) else 0.78
        }

    def _extract_merchant(self, text: str) -> str:
        # Check known merchants
        for m in self.KNOWN_MERCHANTS:
            if re.search(rf"\b{re.escape(m)}\b", text, re.IGNORECASE):
                return m

        # Heuristic: First 3 non-empty lines often hold vendor name
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        for line in lines[:4]:
            if len(line) > 3 and not re.search(r"(invoice|tax|receipt|bill|date|total|welcome|cash)", line, re.IGNORECASE):
                # Clean up punctuation
                cleaned = re.sub(r"[#*_\-]", "", line).strip()
                if 3 <= len(cleaned) <= 40:
                    return cleaned
        return "Unknown Merchant"

    def _extract_date(self, text: str) -> str:
        for pattern in self.DATE_PATTERNS:
            match = re.search(pattern, text)
            if match:
                raw = match.group(0)
                # Attempt to normalize to YYYY-MM-DD
                try:
                    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%m/%d/%Y", "%d %b %Y"):
                        try:
                            dt = datetime.strptime(raw, fmt)
                            return dt.strftime("%Y-%m-%d")
                        except ValueError:
                            pass
                except Exception:
                    pass
                return raw
        return datetime.now().strftime("%Y-%m-%d")

    def _extract_amount(self, text: str) -> (float, str):
        currency = "INR"
        if "$" in text or "USD" in text.upper():
            currency = "USD"
        elif "€" in text or "EUR" in text.upper():
            currency = "EUR"

        for pattern in self.TOTAL_PATTERNS:
            match = re.search(pattern, text)
            if match:
                raw_amt = match.group(1).replace(",", "")
                try:
                    val = float(raw_amt)
                    if val > 0:
                        return val, currency
                except ValueError:
                    pass

        # Fallback: scan for highest number formatted like price
        candidates = re.findall(r"\b([0-9]{2,7}\.[0-9]{2})\b", text)
        if candidates:
            floats = [float(c) for c in candidates]
            return max(floats), currency

        return 0.0, currency

    def _extract_tax(self, text: str) -> float:
        for pattern in self.TAX_PATTERNS:
            match = re.search(pattern, text)
            if match:
                raw_amt = match.group(1).replace(",", "")
                try:
                    val = float(raw_amt)
                    if val > 0:
                        return val
                except ValueError:
                    pass
        return 0.0

    def _extract_invoice_number(self, text: str) -> Optional[str]:
        for pattern in self.INVOICE_PATTERNS:
            match = re.search(pattern, text)
            if match:
                inv = match.group(1).strip()
                if len(inv) >= 4 and not inv.lower().startswith("total"):
                    return inv
        return None

    def _extract_line_items(self, text: str) -> List[Dict[str, Any]]:
        items = []
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        for line in lines:
            # Pattern: Description ... Price
            item_match = re.search(r"^(.*?)\s{2,}(?:₹|\$)?\s*([0-9]{1,5}(?:\.[0-9]{2})?)$", line)
            if item_match:
                desc = item_match.group(1).strip()
                try:
                    price = float(item_match.group(2))
                    if price > 0 and len(desc) > 2:
                        items.append({
                            "description": desc,
                            "quantity": 1.0,
                            "unit_price": price,
                            "total_price": price
                        })
                except ValueError:
                    pass
        return items[:8]

    def _empty_result(self) -> Dict[str, Any]:
        return {
            "merchant": "Unknown Merchant",
            "transaction_date": datetime.now().strftime("%Y-%m-%d"),
            "amount": 0.0,
            "currency": "INR",
            "tax_amount": 0.0,
            "invoice_number": None,
            "line_items": [],
            "ocr_confidence": 0.0
        }

ner_extractor = EntityExtractor()
