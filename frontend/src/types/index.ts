export interface User {
  id: string;
  email: string;
  full_name: string;
  role: string;
  is_verified: boolean;
  is_active: boolean;
}

export interface BusinessProfile {
  id: string;
  user_id: string;
  profession: string;
  business_type: string;
  country: string;
  jurisdiction: string;
  tax_year: string;
  tax_regime: string;
  business_use_patterns: Record<string, number>;
  recurring_expenses: string[];
  business_description?: string;
  estimated_annual_income: number;
}

export interface TaxRule {
  id: string;
  rule_code: string;
  country: string;
  jurisdiction: string;
  tax_year: string;
  taxpayer_type: string;
  profession: string;
  expense_category: string;
  title: string;
  description: string;
  deductibility_status: string;
  eligibility_conditions: string[];
  limitations: Record<string, any>;
  evidence_requirements: string[];
  effective_date: string;
  source_statute: string;
  statute_citation_url?: string;
  rule_version: string;
  last_verified_date: string;
}

export interface MissingEvidenceItem {
  field: string;
  label: string;
  prompt: string;
}

export interface Decision {
  id: string;
  expense_id: string;
  tax_rule_id?: string;
  potential_treatment: string;
  ai_confidence: number;
  evidence_strength_score: number;
  decision_status: "AUTO" | "REVIEW" | "INSUFFICIENT_DATA" | "CONFIRMED";
  reasoning_summary: string[];
  limitations_applied?: string;
  missing_evidence: MissingEvidenceItem[];
  human_review_required: boolean;
  confirmed_by_user: boolean;
  tax_rule?: TaxRule;
}

export interface Anomaly {
  id: string;
  expense_id: string;
  anomaly_type: string;
  anomaly_score: number;
  explanation: string;
  detected_by: string;
  details_json?: Record<string, any>;
  resolved: boolean;
}

export interface RiskFlag {
  id: string;
  expense_id: string;
  risk_type: string;
  severity: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  description: string;
}

export interface Expense {
  id: string;
  user_id: string;
  document_id?: string;
  merchant: string;
  transaction_date: string;
  amount: number;
  currency: string;
  tax_amount: number;
  invoice_number?: string;
  category: string;
  payment_method: string;
  business_purpose?: string;
  business_use_percentage: number;
  eligible_deductible_amount: number;
  status: "AUTO_RECOMMENDED" | "NEEDS_REVIEW" | "INSUFFICIENT_DATA" | "CONFIRMED" | "REJECTED";
  created_at: string;
  decision?: Decision;
  risk_flags?: RiskFlag[];
  anomalies?: Anomaly[];
}

export interface WhyDecisionData {
  expense_id: string;
  merchant: string;
  amount: number;
  category: string;
  decision: Decision;
  statutory_rule?: TaxRule;
  evidence_trail: {
    step: number;
    item: string;
    detail: string;
    status: string;
  }[];
  verification_steps: string[];
  audit_trail_timestamp: string;
}

export interface DigitalTwinSummary {
  user_id: string;
  profession: string;
  tax_year: string;
  current_regime: string;
  total_income_tracked: number;
  total_expenses_recorded: number;
  total_potentially_deductible: number;
  estimated_tax_savings: number;
  average_evidence_strength: number;
  audit_readiness_score: number;
  total_receipts_ingested: number;
  auto_recommended_count: number;
  needs_review_count: number;
  insufficient_data_count: number;
  flagged_anomalies_count: number;
  category_totals: Record<string, number>;
  monthly_trend: {
    month: string;
    total_expense: number;
    deductible: number;
    savings: number;
  }[];
  radar_metrics: {
    subject: string;
    score: number;
    fullMark: number;
  }[];
  proactive_insights: {
    type: string;
    severity: string;
    title: string;
    message: string;
  }[];
}

export interface RegimeCalculation {
  regime_name: string;
  statutory_basis: string;
  taxable_income: number;
  estimated_tax_payable: number;
  effective_tax_rate_percent: number;
  audit_requirement: string;
  books_of_accounts_required: boolean;
  pros_and_cons: {
    pros: string[];
    cons: string[];
  };
}

export interface SimulatorResponse {
  gross_receipts: number;
  claimed_expenses: number;
  regimes: Record<string, RegimeCalculation>;
  recommended_regime: string;
  potential_tax_savings: number;
  disclaimer: string;
}

export interface AuditPackage {
  id: string;
  package_reference: string;
  tax_year: string;
  total_expenses_evaluated: number;
  total_claimed_deductions: number;
  average_evidence_strength: number;
  pdf_file_path: string;
  package_sha256: string;
  generated_at: string;
}

export interface RuleCitation {
  rule_code: string;
  title: string;
  source_statute: string;
  statute_citation_url?: string;
  relevance_summary: string;
}

export interface CopilotResponse {
  conversation_id: string;
  message_id: string;
  answer: string;
  grounding_confidence: number;
  cited_rules: RuleCitation[];
  suggested_followups: string[];
}
