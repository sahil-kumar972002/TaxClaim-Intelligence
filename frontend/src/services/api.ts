import axios from "axios";
import {
  User,
  BusinessProfile,
  Expense,
  WhyDecisionData,
  DigitalTwinSummary,
  SimulatorResponse,
  AuditPackage,
  CopilotResponse,
  TaxRule
} from "../types";

const API_BASE_URL = "http://localhost:8000/api/v1";

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const api = {
  // Health & Admin
  getHealth: async () => (await apiClient.get("/health")).data,
  seedDemo: async () => (await apiClient.post("/admin/seed-demo")).data,
  getModelMetrics: async () => (await apiClient.get("/admin/metrics")).data,
  getAuditLogs: async () => (await apiClient.get("/admin/audit-logs")).data,

  // Profile
  getProfile: async (): Promise<BusinessProfile> => (await apiClient.get("/profiles/me")).data,
  updateProfile: async (data: Partial<BusinessProfile>): Promise<BusinessProfile> =>
    (await apiClient.put("/profiles/me", data)).data,

  // Expenses
  getExpenses: async (status?: string, category?: string): Promise<Expense[]> => {
    const params: Record<string, string> = {};
    if (status) params.status = status;
    if (category) params.category = category;
    return (await apiClient.get("/expenses/", { params })).data;
  },
  getExpenseById: async (id: string): Promise<Expense> =>
    (await apiClient.get(`/expenses/${id}`)).data,
  getWhyDecision: async (id: string): Promise<WhyDecisionData> =>
    (await apiClient.get(`/expenses/${id}/why`)).data,
  patchMissingEvidence: async (id: string, patch: { business_purpose?: string; business_use_percentage?: number; payment_proof_reference?: string }) =>
    (await apiClient.post(`/expenses/${id}/missing-evidence`, patch)).data,
  confirmExpense: async (id: string) =>
    (await apiClient.post(`/expenses/${id}/confirm`)).data,

  // Ingestion & Upload
  uploadDocument: async (file: File, samplePresetText?: string) => {
    const formData = new FormData();
    formData.append("file", file);
    if (samplePresetText) {
      formData.append("sample_preset", samplePresetText);
    }
    return (await apiClient.post("/documents/upload", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    })).data;
  },
  correctOCR: async (docId: string, correctedFields: any) =>
    (await apiClient.patch(`/documents/${docId}/correct`, correctedFields)).data,

  // Digital Twin
  getDigitalTwin: async (): Promise<DigitalTwinSummary> =>
    (await apiClient.get("/digital-twin/summary")).data,

  // Simulator
  getSimulatorDefaults: async (): Promise<SimulatorResponse> =>
    (await apiClient.get("/simulator/defaults")).data,
  simulate: async (data: { annual_gross_receipts: number; total_business_expenses: number; business_use_multiplier: number }): Promise<SimulatorResponse> =>
    (await apiClient.post("/simulator/evaluate", data)).data,

  // Audit Pack
  generateAuditPack: async (taxYear: string = "2024-2025"): Promise<AuditPackage> =>
    (await apiClient.post("/audit-pack/generate", { tax_year: taxYear })).data,
  getAuditPackages: async (): Promise<AuditPackage[]> =>
    (await apiClient.get("/audit-pack/")).data,
  getDownloadUrl: (packageId: string) => `${API_BASE_URL}/audit-pack/${packageId}/download`,
  verifyPackage: async (packageId: string) =>
    (await apiClient.get(`/audit-pack/${packageId}/verify`)).data,

  // Copilot
  askCopilot: async (query: string, expenseId?: string, conversationId?: string): Promise<CopilotResponse> =>
    (await apiClient.post("/copilot/query", { query, expense_id: expenseId, conversation_id: conversationId })).data,

  // Rules
  getTaxRules: async (): Promise<TaxRule[]> =>
    (await apiClient.get("/tax-rules/")).data,
};
