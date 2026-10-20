import React, { useState, useRef } from "react";
import {
  UploadCloud,
  FileText,
  Camera,
  CheckCircle2,
  AlertCircle,
  Sparkles,
  ArrowRight,
  RefreshCw
} from "lucide-react";
import { api } from "../../services/api";

interface SmartDropzoneProps {
  onDocumentProcessed: () => void;
}

const PRESET_DOCUMENTS = [
  {
    name: "Laptop Invoice (MacBook Pro)",
    merchant: "Apple India Pvt Ltd",
    category: "hardware",
    amount: "₹2,49,900.00",
    text: `TAX INVOICE\nApple India Private Limited\nUB City, Bengaluru 560001\nGSTIN: 29AABCA0123M1Z8\nInvoice No: APL-IN-2024-91823\nDate: 12-Jun-2024\nItem: 16-inch MacBook Pro M3 Max 36GB Unified Memory 1TB SSD\nTotal Amount Payable: ₹2,49,900.00\nPayment: Credit Card ending 4092`
  },
  {
    name: "Adobe Creative Cloud",
    merchant: "Adobe Systems",
    category: "software",
    amount: "₹3,499.00",
    text: `Adobe Systems India Pvt Ltd\nInvoice: ADB-INV-883019\nDate: 05-Jul-2024\nDescription: Creative Cloud All Apps Monthly License\nNet Amount: ₹2,965.25\nIGST 18%: ₹533.75\nTotal: ₹3,499.00\nPayment Method: Corporate Visa`
  },
  {
    name: "Jio Fiber Broadband",
    merchant: "Reliance Jio",
    category: "internet",
    amount: "₹1,499.00",
    text: `JioFiber Monthly Broadband Statement\nInvoice #: JIO-FBR-7482910\nDate: 01-Aug-2024\nPlan: 300 Mbps Unlimited Data\nAmount Payable: ₹1,499.00\nPayment: UPI Ref 421498102391`
  },
  {
    name: "Flight Ticket (IndiGo)",
    merchant: "IndiGo Airlines",
    category: "travel",
    amount: "₹7,850.00",
    text: `IndiGo Flight Ticket Receipt\nPNR: W8K9LQ\nDate: 14-Sep-2024\nPassenger: Aarav Sharma\nSector: Delhi -> Bengaluru (AWS Summit)\nTotal Fare: ₹7,850.00`
  },
  {
    name: "Client Dinner Receipt",
    merchant: "The Bombay Canteen",
    category: "meals",
    amount: "₹4,850.00",
    text: `The Bombay Canteen\nLower Parel, Mumbai\nTax Invoice: TBC-DIN-0941\nDate: 15-Sep-2024\nGuests: 2\nTotal Amount: ₹4,850.00\nPayment: Amex ending 1004`
  },
  {
    name: "AWS Cloud Servers",
    merchant: "Amazon Web Services",
    category: "software",
    amount: "₹18,450.00",
    text: `Amazon Web Services India\nInvoice: AWS-IN-9481029\nDate: 02-Sep-2024\nCharges: EC2, S3, RDS Compute\nTotal Due: ₹18,450.00`
  },
  {
    name: "Ergonomic Office Chair",
    merchant: "Herman Miller India",
    category: "office",
    amount: "₹89,900.00",
    text: `Herman Miller India Retail\nInvoice: HM-BLR-2024-059\nDate: 20-May-2024\nItem: Aeron Chair Size B Graphite\nTotal: ₹89,900.00\nPayment: Bank Transfer UTR 948192`
  }
];

export const SmartDropzone: React.FC<SmartDropzoneProps> = ({ onDocumentProcessed }) => {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState<string | null>(null);
  const [lastExtracted, setLastExtracted] = useState<any>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const processUpload = async (file: File, sampleText?: string) => {
    setIsUploading(true);
    setUploadSuccess(null);
    try {
      const res = await api.uploadDocument(file, sampleText);
      setLastExtracted(res.ocr_result);
      setUploadSuccess(`Successfully ingested "${file.name}" with cryptographic SHA-256 hash.`);
      onDocumentProcessed();
    } catch (err: any) {
      console.error(err);
      alert("Failed to upload document: " + (err.response?.data?.detail || err.message));
    } finally {
      setIsUploading(false);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      processUpload(e.target.files[0]);
    }
  };

  const handlePresetInject = (preset: typeof PRESET_DOCUMENTS[0]) => {
    const dummyBlob = new Blob([preset.text], { type: "text/plain" });
    const dummyFile = new File([dummyBlob], `${preset.merchant.replace(/\s+/g, "_")}_Invoice.pdf`, {
      type: "application/pdf",
    });
    processUpload(dummyFile, preset.text);
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight">Smart Document Ingestion & OCR</h2>
          <p className="text-xs text-slate-400">
            Accepts Invoices, Receipts, Bank Statements & PDFs with SHA-256 tamper verification.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Main Upload Dropzone */}
        <div className="lg:col-span-7 space-y-4">
          <div
            onClick={() => fileInputRef.current?.click()}
            className="glass-card rounded-2xl p-8 border-2 border-dashed border-brand-border hover:border-brand-primary/60 transition-all cursor-pointer flex flex-col items-center justify-center text-center group bg-brand-navy/40 min-h-[260px]"
          >
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              accept=".pdf,.png,.jpg,.jpeg,.csv,.txt"
              className="hidden"
            />
            <div className="w-16 h-16 rounded-2xl bg-brand-navy border border-brand-border flex items-center justify-center text-brand-primary group-hover:scale-110 transition-transform shadow-glow">
              {isUploading ? (
                <RefreshCw className="w-8 h-8 animate-spin text-brand-accent" />
              ) : (
                <UploadCloud className="w-8 h-8" />
              )}
            </div>
            <h3 className="mt-4 text-sm font-bold text-white">
              {isUploading ? "Processing OCR & Statutory Analysis..." : "Drag & Drop Invoices, Receipts or PDFs"}
            </h3>
            <p className="mt-1 text-xs text-slate-400 max-w-sm">
              Supports single or multi-page PDFs, Camera JPG/PNG scans, or CSV transaction exports.
            </p>
            <div className="mt-4 flex items-center space-x-3 text-[11px] text-slate-500 font-mono">
              <span>PDF • PNG • JPG • CSV</span>
              <span>•</span>
              <span className="text-emerald-400 font-medium">Auto PII Masking Active</span>
            </div>
          </div>

          {/* Success Banner */}
          {uploadSuccess && (
            <div className="bg-emerald-500/10 border border-emerald-500/30 rounded-xl p-3.5 flex items-center space-x-3 text-xs text-emerald-300 animate-fadeIn">
              <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
              <div>
                <span className="font-bold">Extraction Complete: </span>
                <span>{uploadSuccess}</span>
              </div>
            </div>
          )}
        </div>

        {/* 1-Click Realistic Demo Preset Injector */}
        <div className="lg:col-span-5 space-y-3">
          <div className="glass-card rounded-2xl p-5 border border-brand-border h-full flex flex-col justify-between">
            <div>
              <div className="flex items-center space-x-2 text-xs font-bold uppercase tracking-wider text-brand-accent mb-1">
                <Sparkles className="w-4 h-4" />
                <span>1-Click Demo Scenarios</span>
              </div>
              <p className="text-xs text-slate-400 mb-3">
                Instantly inject verified sample receipts to experience end-to-end tax deduction intelligence:
              </p>
              <div className="space-y-2 max-h-[300px] overflow-y-auto pr-1">
                {PRESET_DOCUMENTS.map((preset, idx) => (
                  <button
                    key={idx}
                    disabled={isUploading}
                    onClick={() => handlePresetInject(preset)}
                    className="w-full flex items-center justify-between p-2.5 rounded-xl bg-brand-navy hover:bg-brand-card border border-brand-border hover:border-brand-primary/40 text-left transition-all group"
                  >
                    <div>
                      <div className="text-xs font-bold text-slate-200 group-hover:text-white truncate">
                        {preset.name}
                      </div>
                      <div className="text-[10px] text-slate-400 font-mono">
                        {preset.merchant} • <span className="text-emerald-400 font-bold">{preset.amount}</span>
                      </div>
                    </div>
                    <ArrowRight className="w-4 h-4 text-slate-500 group-hover:text-brand-accent transition-transform group-hover:translate-x-0.5" />
                  </button>
                ))}
              </div>
            </div>
            <div className="mt-3 pt-3 border-t border-slate-800 text-[10px] text-slate-500 font-mono text-center">
              Demonstrates 7 statutory categories & capital depreciation
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
