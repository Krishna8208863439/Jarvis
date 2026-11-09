import React, { useState } from "react";
import { MemoryItem } from "../store/useNovaStore";
import { Brain, Plus, Trash2, Shield, Check } from "lucide-react";

interface MemoryManagerModalProps {
  isOpen: boolean;
  onClose: () => void;
  memories: MemoryItem[];
  onAddMemory: (key: string, value: string) => void;
  onDeleteMemory: (id: string) => void;
}

export const MemoryManagerModal: React.FC<MemoryManagerModalProps> = ({
  isOpen,
  onClose,
  memories,
  onAddMemory,
  onDeleteMemory,
}) => {
  const [newKey, setNewKey] = useState("");
  const [newValue, setNewValue] = useState("");
  const [userConsentGiven, setUserConsentGiven] = useState(false);

  if (!isOpen) return null;

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    if (newKey.trim() && newValue.trim() && userConsentGiven) {
      onAddMemory(newKey.trim(), newValue.trim());
      setNewKey("");
      setNewValue("");
      setUserConsentGiven(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm animate-fade-in">
      <div className="w-full max-w-lg bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl p-6 text-slate-100 relative">
        <div className="flex items-center justify-between pb-3 border-b border-slate-800">
          <div className="flex items-center gap-2 text-purple-400 font-mono text-sm uppercase">
            <Brain className="w-4 h-4" />
            <span>User-Approved Memory Inspector</span>
          </div>
          <button
            onClick={onClose}
            className="text-xs font-mono text-slate-500 hover:text-slate-300 transition"
          >
            CLOSE
          </button>
        </div>

        {/* Existing Memories List */}
        <div className="mt-4">
          <label className="text-[11px] font-mono text-slate-400 uppercase tracking-wider block mb-2">
            Stored Memories ({memories.length})
          </label>
          <div className="max-h-48 overflow-y-auto space-y-2 pr-1 custom-scrollbar">
            {memories.length === 0 ? (
              <div className="text-xs text-slate-500 p-4 border border-dashed border-slate-800 rounded-xl text-center">
                No memories stored yet. Memories require explicit user approval.
              </div>
            ) : (
              memories.map((m) => (
                <div
                  key={m.id}
                  className="flex items-center justify-between p-2.5 rounded-xl bg-slate-950/60 border border-slate-800 text-xs"
                >
                  <div>
                    <span className="font-mono text-cyan-400 font-semibold">{m.key}:</span>{" "}
                    <span className="text-slate-200">{m.value}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="flex items-center gap-1 text-[10px] text-emerald-400 font-mono">
                      <Shield className="w-3 h-3" /> Approved
                    </span>
                    <button
                      onClick={() => onDeleteMemory(m.id)}
                      className="p-1 text-slate-500 hover:text-rose-400 transition"
                      title="Permanently Delete Memory"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Add New Memory Form with User Consent Check */}
        <form onSubmit={handleSave} className="mt-5 pt-4 border-t border-slate-800 space-y-3">
          <div className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">
            Authorize New Memory
          </div>
          <div className="grid grid-cols-2 gap-2">
            <input
              type="text"
              placeholder="Key (e.g., job_role)"
              value={newKey}
              onChange={(e) => setNewKey(e.target.value)}
              className="px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-200 focus:outline-none focus:border-cyan-400 font-mono"
            />
            <input
              type="text"
              placeholder="Value (e.g., Python Developer)"
              value={newValue}
              onChange={(e) => setNewValue(e.target.value)}
              className="px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-200 focus:outline-none focus:border-cyan-400"
            />
          </div>

          <label className="flex items-center gap-2 text-xs text-slate-400 cursor-pointer pt-1">
            <input
              type="checkbox"
              checked={userConsentGiven}
              onChange={(e) => setUserConsentGiven(e.target.checked)}
              className="rounded accent-cyan-400"
            />
            <span>I explicitly authorize NOVA to retain this memory.</span>
          </label>

          <div className="flex justify-end pt-2">
            <button
              type="submit"
              disabled={!newKey || !newValue || !userConsentGiven}
              className={`flex items-center gap-1.5 px-4 py-2 rounded-xl font-mono text-xs font-semibold transition ${
                newKey && newValue && userConsentGiven
                  ? "bg-purple-600 hover:bg-purple-500 text-white shadow-[0_0_12px_rgba(168,85,247,0.4)]"
                  : "bg-slate-800 text-slate-500 cursor-not-allowed"
              }`}
            >
              <Plus className="w-3.5 h-3.5" />
              <span>Save Approved Memory</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

