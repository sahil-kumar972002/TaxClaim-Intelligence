import React, { useState, useEffect } from "react";
import { Navbar } from "./components/layout/Navbar";
import { Sidebar } from "./components/layout/Sidebar";
import { TaxHealthHeader } from "./components/dashboard/TaxHealthHeader";
import { MetricCards } from "./components/dashboard/MetricCards";
import { MonthlyTrendsChart } from "./components/dashboard/MonthlyTrendsChart";
import { CategoryDistribution } from "./components/dashboard/CategoryDistribution";
import { ExpenseCard } from "./components/expenses/ExpenseCard";
import { WhyDecisionModal } from "./components/expenses/WhyDecisionModal";
import { MissingEvidenceModal } from "./components/expenses/MissingEvidenceModal";
import { SmartDropzone } from "./components/ingestion/SmartDropzone";
import { WhatIfSimulator } from "./components/simulator/WhatIfSimulator";
import { DigitalTwinView } from "./components/digital_twin/DigitalTwinView";
import { AuditPackStudio } from "./components/audit/AuditPackStudio";
import { TaxClaimCopilot } from "./components/copilot/TaxClaimCopilot";
import { AdminView } from "./components/admin/AdminView";
import { api } from "./services/api";
import { Expense, DigitalTwinSummary, BusinessProfile } from "./types";
import { Sparkles, Filter, Search, RefreshCw } from "lucide-react";

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>("dashboard");
  const [currentProfession, setCurrentProfession] = useState<string>("Software Developer");
  
  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [digitalTwin, setDigitalTwin] = useState<DigitalTwinSummary | null>(null);
  const [profile, setProfile] = useState<BusinessProfile | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Modals state
  const [selectedWhyExpense, setSelectedWhyExpense] = useState<Expense | null>(null);
  const [selectedMissingExpense, setSelectedMissingExpense] = useState<Expense | null>(null);

  // Filters
  const [statusFilter, setStatusFilter] = useState<string>("ALL");
  const [searchQuery, setSearchQuery] = useState<string>("");

  const loadData = async () => {
    setIsLoading(true);
    try {
      const [expList, twin, prof] = await Promise.all([
        api.getExpenses(),
        api.getDigitalTwin(),
        api.getProfile(),
      ]);
      setExpenses(expList);
      setDigitalTwin(twin);
      setProfile(prof);
      if (prof?.profession) {
        setCurrentProfession(prof.profession);
      }
    } catch (err) {
      console.error("Failed to load initial data", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleSelectProfession = async (newProf: string) => {
    setCurrentProfession(newProf);
    try {
      await api.updateProfile({ profession: newProf });
      await loadData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleConfirmExpense = async (id: string) => {
    try {
      await api.confirmExpense(id);
      await loadData();
    } catch (err) {
      console.error(err);
    }
  };

  const handlePatchMissingEvidence = async (
    expenseId: string,
    patch: {
      business_purpose?: string;
      business_use_percentage?: number;
      payment_proof_reference?: string;
    }
  ) => {
    try {
      await api.patchMissingEvidence(expenseId, patch);
      await loadData();
    } catch (err) {
      console.error(err);
    }
  };

  // Filtered expense feed
  const filteredExpenses = expenses.filter((e) => {
    const matchesStatus =
      statusFilter === "ALL" ||
      (statusFilter === "AUTO_RECOMMENDED" && e.status === "AUTO_RECOMMENDED") ||
      (statusFilter === "NEEDS_REVIEW" && e.status === "NEEDS_REVIEW") ||
      (statusFilter === "INSUFFICIENT_DATA" && e.status === "INSUFFICIENT_DATA") ||
      (statusFilter === "CONFIRMED" && e.status === "CONFIRMED");

    const matchesSearch =
      e.merchant.toLowerCase().includes(searchQuery.toLowerCase()) ||
      e.category.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (e.business_purpose && e.business_purpose.toLowerCase().includes(searchQuery.toLowerCase()));

    return matchesStatus && matchesSearch;
  });

  const reviewCount = digitalTwin?.needs_review_count ?? 0;
  const anomalyCount = digitalTwin?.flagged_anomalies_count ?? 0;
  const readinessScore = digitalTwin?.audit_readiness_score ?? 94;

  return (
    <div className="min-h-screen bg-brand-dark text-slate-100 flex flex-col">
      {/* Top Navbar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        currentProfession={currentProfession}
        onSelectProfession={handleSelectProfession}
        readinessScore={readinessScore}
      />

      {/* Main Container with Sidebar + Content */}
      <div className="flex-1 flex overflow-hidden">
        <Sidebar
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          reviewCount={reviewCount}
          anomalyCount={anomalyCount}
        />

        {/* Content Viewport */}
        <main className="flex-1 overflow-y-auto p-6 space-y-6">
          {/* TAB 1: COMMAND CENTER DASHBOARD */}
          {activeTab === "dashboard" && (
            <div className="space-y-6 animate-fadeIn">
              <TaxHealthHeader
                profession={currentProfession}
                taxYear={profile?.tax_year || "2024-2025"}
                regime={profile?.tax_regime || "Sec 44ADA (Presumptive)"}
                readinessScore={readinessScore}
                potentialSavings={digitalTwin?.estimated_tax_savings || 106950}
              />

              <MetricCards
                healthScore={readinessScore}
                avgEvidenceScore={digitalTwin?.average_evidence_strength || 0.82}
                potentialClaims={digitalTwin?.total_potentially_deductible || 342800}
                needsReviewCount={reviewCount}
                riskAlertCount={anomalyCount}
                onFilterReview={() => {
                  setStatusFilter("NEEDS_REVIEW");
                  const el = document.getElementById("expense-intelligence-panel");
                  el?.scrollIntoView({ behavior: "smooth" });
                }}
                onFilterRisk={() => {
                  setActiveTab("admin");
                }}
              />

              {/* Charts Row */}
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                <div className="lg:col-span-7">
                  <MonthlyTrendsChart data={digitalTwin?.monthly_trend || []} />
                </div>
                <div className="lg:col-span-5">
                  <CategoryDistribution categories={digitalTwin?.category_totals || {}} />
                </div>
              </div>

              {/* AI Expense Intelligence Section */}
              <div id="expense-intelligence-panel" className="space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div>
                    <h3 className="text-lg font-bold text-white tracking-tight flex items-center gap-2">
                      <Sparkles className="w-4 h-4 text-brand-accent" />
                      <span>AI Expense Intelligence Feed</span>
                    </h3>
                    <p className="text-xs text-slate-400">
                      Real-time statutory tax evaluation with traceable evidence chains.
                    </p>
                  </div>

                  {/* Filter Buttons */}
                  <div className="flex flex-wrap items-center gap-1.5 bg-brand-navy/80 p-1 rounded-xl border border-brand-border text-xs">
                    {["ALL", "AUTO_RECOMMENDED", "NEEDS_REVIEW", "CONFIRMED"].map((st) => (
                      <button
                        key={st}
                        onClick={() => setStatusFilter(st)}
                        className={`px-3 py-1 rounded-lg font-semibold transition-all ${
                          statusFilter === st
                            ? "bg-brand-primary text-white shadow-glow"
                            : "text-slate-400 hover:text-white"
                        }`}
                      >
                        {st.replace("_", " ")}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Expense Cards List */}
                <div className="space-y-3">
                  {filteredExpenses.length > 0 ? (
                    filteredExpenses.map((expense) => (
                      <ExpenseCard
                        key={expense.id}
                        expense={expense}
                        onWhyClick={(e) => setSelectedWhyExpense(e)}
                        onMissingEvidenceClick={(e) => setSelectedMissingExpense(e)}
                        onConfirmClick={handleConfirmExpense}
                      />
                    ))
                  ) : (
                    <div className="glass-card rounded-2xl p-12 text-center text-slate-400 text-xs">
                      No expenses match the selected filter.
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: EXPENSE INTELLIGENCE */}
          {activeTab === "expenses" && (
            <div className="space-y-6 animate-fadeIn">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div>
                  <h2 className="text-xl font-bold text-white tracking-tight">
                    Expense Intelligence Ledger
                  </h2>
                  <p className="text-xs text-slate-400">
                    Comprehensive ledger of all financial transactions with AI tax analysis and evidence links.
                  </p>
                </div>

                {/* Search Bar */}
                <div className="relative">
                  <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search merchant, category, purpose..."
                    className="glass-input rounded-xl pl-9 pr-4 py-2 text-xs w-64 focus:ring-1 focus:ring-brand-primary"
                  />
                </div>
              </div>

              {/* Status Filter Tabs */}
              <div className="flex flex-wrap items-center gap-1.5 bg-brand-navy/60 p-1.5 rounded-xl border border-brand-border text-xs">
                {["ALL", "AUTO_RECOMMENDED", "NEEDS_REVIEW", "INSUFFICIENT_DATA", "CONFIRMED"].map((st) => (
                  <button
                    key={st}
                    onClick={() => setStatusFilter(st)}
                    className={`px-3 py-1.5 rounded-lg font-semibold transition-all ${
                      statusFilter === st
                        ? "bg-brand-primary text-white shadow-glow"
                        : "text-slate-400 hover:text-white"
                    }`}
                  >
                    {st.replace("_", " ")}
                  </button>
                ))}
              </div>

              <div className="space-y-3">
                {filteredExpenses.map((expense) => (
                  <ExpenseCard
                    key={expense.id}
                    expense={expense}
                    onWhyClick={(e) => setSelectedWhyExpense(e)}
                    onMissingEvidenceClick={(e) => setSelectedMissingExpense(e)}
                    onConfirmClick={handleConfirmExpense}
                  />
                ))}
              </div>
            </div>
          )}

          {/* TAB 3: SMART INGESTION */}
          {activeTab === "ingestion" && (
            <div className="animate-fadeIn">
              <SmartDropzone onDocumentProcessed={loadData} />
            </div>
          )}

          {/* TAB 4: WHAT-IF SIMULATOR */}
          {activeTab === "simulator" && (
            <div className="animate-fadeIn">
              <WhatIfSimulator />
            </div>
          )}

          {/* TAB 5: DIGITAL TWIN */}
          {activeTab === "digital_twin" && (
            <div className="animate-fadeIn">
              <DigitalTwinView data={digitalTwin} />
            </div>
          )}

          {/* TAB 6: AUDIT PACK */}
          {activeTab === "audit" && (
            <div className="animate-fadeIn">
              <AuditPackStudio />
            </div>
          )}

          {/* TAB 7: TAX COPILOT */}
          {activeTab === "copilot" && (
            <div className="animate-fadeIn">
              <TaxClaimCopilot />
            </div>
          )}

          {/* TAB 8: ADMIN & MONITORING */}
          {activeTab === "admin" && (
            <div className="animate-fadeIn">
              <AdminView />
            </div>
          )}
        </main>
      </div>

      {/* Traceable Reasoning Modal */}
      <WhyDecisionModal
        expense={selectedWhyExpense}
        onClose={() => setSelectedWhyExpense(null)}
      />

      {/* Missing Evidence Copilot Modal */}
      <MissingEvidenceModal
        expense={selectedMissingExpense}
        onClose={() => setSelectedMissingExpense(null)}
        onSubmitPatch={handlePatchMissingEvidence}
      />
    </div>
  );
};

export default App;
