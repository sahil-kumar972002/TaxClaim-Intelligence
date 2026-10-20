import React, { useState } from "react";
import {
  Bot,
  Send,
  Sparkles,
  BookOpen,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  RefreshCw,
  User
} from "lucide-react";
import { api } from "../../services/api";
import { CopilotResponse } from "../../types";

interface MessageEntry {
  sender: "USER" | "COPILOT";
  text: string;
  cited_rules?: any[];
  followups?: string[];
}

export const TaxClaimCopilot: React.FC = () => {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<MessageEntry[]>([
    {
      sender: "COPILOT",
      text: "Hello! I am TaxClaim Copilot. I analyze your business expenses against verified statutory tax rules (Income Tax Act 1961 Section 37(1), 32, and 44ADA). Ask me anything regarding your deductions, evidence requirements, or regime comparisons—every answer will cite official statutes with zero hallucination.",
      followups: [
        "Is my MacBook Pro fully deductible in Year 1?",
        "Can I claim client dining expenses without receipts?",
        "Explain Section 44ADA vs Regular PGBP for software engineers"
      ]
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async (textToSend: string) => {
    if (!textToSend.trim()) return;

    const userText = textToSend;
    setQuery("");
    setMessages((prev) => [...prev, { sender: "USER", text: userText }]);
    setIsLoading(true);

    try {
      const res: CopilotResponse = await api.askCopilot(userText);
      setMessages((prev) => [
        ...prev,
        {
          sender: "COPILOT",
          text: res.answer,
          cited_rules: res.cited_rules,
          followups: res.suggested_followups
        }
      ]);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        {
          sender: "COPILOT",
          text: "I encountered a problem accessing the statutory knowledge base. Please check backend connection."
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
          <Bot className="w-5 h-5 text-brand-primary" />
          <span>TaxClaim Copilot — Statutory Tax Assistant</span>
        </h2>
        <p className="text-xs text-slate-400 mt-0.5">
          Grounded tax intelligence citing official laws. Never hallucinates deduction caps or percentages.
        </p>
      </div>

      {/* Main Chat Container */}
      <div className="glass-card rounded-2xl border border-brand-border h-[600px] flex flex-col justify-between overflow-hidden bg-brand-navy/60">
        {/* Messages List */}
        <div className="flex-1 p-6 overflow-y-auto space-y-5">
          {messages.map((m, idx) => (
            <div
              key={idx}
              className={`flex items-start space-x-3 ${
                m.sender === "USER" ? "flex-row-reverse space-x-reverse" : ""
              }`}
            >
              {/* Avatar */}
              <div
                className={`w-8 h-8 rounded-xl flex items-center justify-center shrink-0 text-white ${
                  m.sender === "USER"
                    ? "bg-brand-primary"
                    : "bg-gradient-to-tr from-brand-primary to-brand-accent shadow-glow"
                }`}
              >
                {m.sender === "USER" ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>

              {/* Message Bubble */}
              <div
                className={`rounded-2xl p-4 max-w-xl text-xs leading-relaxed space-y-3 ${
                  m.sender === "USER"
                    ? "bg-brand-primary text-white ml-auto"
                    : "bg-brand-card/90 text-slate-200 border border-brand-border"
                }`}
              >
                <div className="whitespace-pre-line">{m.text}</div>

                {/* Cited Rules Badge if assistant */}
                {m.cited_rules && m.cited_rules.length > 0 && (
                  <div className="pt-2 border-t border-slate-700/60 space-y-2">
                    <span className="text-[10px] font-bold uppercase tracking-wider text-brand-accent flex items-center gap-1">
                      <BookOpen className="w-3 h-3" />
                      <span>Statutory Citation Grounding:</span>
                    </span>
                    <div className="space-y-1.5">
                      {m.cited_rules.map((r, rIdx) => (
                        <div
                          key={rIdx}
                          className="bg-brand-dark/80 p-2.5 rounded-lg border border-slate-700/80 text-[11px]"
                        >
                          <div className="font-bold text-white flex items-center justify-between">
                            <span>{r.title}</span>
                            <span className="font-mono text-[9px] text-brand-accent bg-brand-navy px-1.5 py-0.5 rounded">
                              {r.rule_code}
                            </span>
                          </div>
                          <div className="text-[10px] text-slate-400 mt-0.5 font-mono">
                            {r.source_statute}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Suggested followups */}
                {m.followups && m.followups.length > 0 && (
                  <div className="pt-2 flex flex-wrap gap-1.5">
                    {m.followups.map((f, fIdx) => (
                      <button
                        key={fIdx}
                        onClick={() => handleSend(f)}
                        className="px-2.5 py-1 rounded-full bg-brand-navy hover:bg-brand-card text-[10px] text-slate-300 hover:text-white border border-brand-border transition-colors text-left"
                      >
                        {f}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex items-center space-x-2 text-xs text-slate-400">
              <RefreshCw className="w-4 h-4 animate-spin text-brand-accent" />
              <span>TaxClaim Copilot is retrieving statutory tax rules...</span>
            </div>
          )}
        </div>

        {/* Input Bar */}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend(query);
          }}
          className="p-4 border-t border-brand-border bg-brand-dark/40 flex items-center space-x-3"
        >
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask anything about expense deductibility, statutory limits, or Section 44ADA..."
            className="flex-1 glass-input rounded-xl px-4 py-2.5 text-xs focus:ring-1 focus:ring-brand-primary"
          />
          <button
            type="submit"
            disabled={isLoading || !query.trim()}
            className="px-4 py-2.5 rounded-xl bg-brand-primary hover:bg-brand-primaryHover text-white text-xs font-bold shadow-glow flex items-center space-x-1.5 transition-all disabled:opacity-50"
          >
            <Send className="w-4 h-4" />
            <span>Send</span>
          </button>
        </form>
      </div>
    </div>
  );
};
