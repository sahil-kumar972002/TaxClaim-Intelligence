from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class CopilotQueryRequest(BaseModel):
    query: str
    expense_id: Optional[str] = None
    conversation_id: Optional[str] = None

class RuleCitation(BaseModel):
    rule_code: str
    title: str
    source_statute: str
    statute_citation_url: Optional[str] = None
    relevance_summary: str

class CopilotQueryResponse(BaseModel):
    conversation_id: str
    message_id: str
    answer: str
    grounding_confidence: float
    cited_rules: List[RuleCitation]
    clarification_needed: Optional[str] = None
    suggested_followups: List[str] = []
