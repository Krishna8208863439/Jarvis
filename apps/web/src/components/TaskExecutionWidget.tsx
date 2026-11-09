"use client";

import React, { useEffect, useRef } from "react";
import { MultiStepPlan } from "../store/useNovaStore";
import { ListOrdered, CheckCircle2, Clock, AlertTriangle, Play, Ban, Zap } from "lucide-react";

interface TaskExecutionWidgetProps {
  currentPlan: MultiStepPlan | null;
  onApproveTier2Plan?: (planId: string) => void;
  onCancelPlan?: (planId: string) => void;
  onPlanUpdate?: (updater: (prev: MultiStepPlan) => MultiStepPlan) => void;
}

export const TaskExecutionWidget: React.FC<TaskExecutionWidgetProps> = ({
  currentPlan,
  onApproveTier2Plan,
  onCancelPlan,
  onPlanUpdate,
}) => {
  const wsRef = useRef<WebSocket | null>(null);

  // Connect to live task streaming WebSocket when a plan is active
  useEffect(() => {
    if (!currentPlan || !onPlanUpdate) return;

    // Only stream while a plan is running
    if (currentPlan.status !== "EXECUTING") return;

    if (wsRef.current) return; // already connected

    try {
      const ws = new WebSocket("ws://localhost:8000/ws/tasks");
      wsRef.current = ws;

      ws.onmessage = (event) => {
        try {
          const msg = JSON.parse(event.data);
          if (msg.type === "STEP_STARTING") {
            onPlanUpdate((prev) => ({
              ...prev,
              steps: prev.steps.map((s) =>
                s.step_id === msg.payload.step_id ? { ...s, status: "RUNNING" } : s
              ),
            }));
          } else if (msg.type === "STEP_COMPLETED") {
            onPlanUpdate((prev) => ({
              ...prev,
              steps: prev.steps.map((s) =>
                s.step_id === msg.payload.step_id
                  ? { ...s, status: msg.payload.status || "COMPLETED" }
                  : s
              ),
            }));
          } else if (msg.type === "STEP_FAILED") {
            onPlanUpdate((prev) => ({
              ...prev,
              steps: prev.steps.map((s) =>
                s.step_id === msg.payload.step_id ? { ...s, status: "FAILED" } : s
              ),
            }));
          } else if (msg.type === "TASK_COMPLETED") {
            onPlanUpdate((prev) => ({ ...prev, status: "COMPLETED" }));
          } else if (msg.type === "TASK_FAILED") {
            onPlanUpdate((prev) => ({ ...prev, status: "FAILED" }));
          } else if (msg.type === "HEARTBEAT") {
            ws.send("ping");
          }
        } catch {
          // Ignore parse errors
        }
      };

      ws.onerror = () => {
        wsRef.current = null;
      };

      ws.onclose = () => {
        wsRef.current = null;
      };
    } catch {
      wsRef.current = null;
    }

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
        wsRef.current = null;
      }
    };
  }, [currentPlan?.plan_id, currentPlan?.status]);

  if (!currentPlan) {
    return (
      <div className="bg-slate-900/50 backdrop-blur-md border border-slate-800 rounded-2xl p-4 shadow-xl text-xs font-mono text-slate-400 flex flex-col gap-2">
        <div className="flex items-center gap-2 pb-2 border-b border-slate-800 text-slate-300">
          <ListOrdered className="w-4 h-4 text-cyan-400" />
          <span>MULTI-STEP TASK EXECUTION TIMELINE</span>
        </div>
        <p className="py-4 text-center text-slate-500">
          No multi-step task active. Speak or prompt NOVA to run automations.
        </p>
      </div>
    );
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "COMPLETED":
        return <span className="text-[10px] text-emerald-400 flex items-center gap-1 font-bold"><CheckCircle2 className="w-3 h-3" /> DONE</span>;
      case "RUNNING":
        return <span className="text-[10px] text-cyan-400 flex items-center gap-1 font-bold animate-pulse"><Clock className="w-3 h-3" /> RUNNING</span>;
      case "AWAITING_APPROVAL":
        return <span className="text-[10px] text-amber-400 flex items-center gap-1 font-bold"><AlertTriangle className="w-3 h-3" /> CONFIRM</span>;
      case "FAILED":
        return <span className="text-[10px] text-rose-400 flex items-center gap-1 font-bold"><Ban className="w-3 h-3" /> FAILED</span>;
      default:
        return <span className="text-[10px] text-slate-500 font-mono">PENDING</span>;
    }
  };

  const getPlanStatusColor = (status: string) => {
    switch (status) {
      case "COMPLETED": return "text-emerald-300 border-emerald-500/30 bg-emerald-500/10";
      case "FAILED": return "text-rose-300 border-rose-500/30 bg-rose-500/10";
      case "AWAITING_APPROVAL": return "text-amber-300 border-amber-500/30 bg-amber-500/10";
      case "EXECUTING":
      case "RUNNING": return "text-cyan-300 border-cyan-500/20 bg-cyan-500/10";
      default: return "text-slate-400 border-slate-700 bg-slate-800/40";
    }
  };

  const completedSteps = currentPlan.steps.filter((s) => s.status === "COMPLETED").length;
  const totalSteps = currentPlan.steps.length;

  return (
    <div className="bg-slate-900/50 backdrop-blur-md border border-slate-800 rounded-2xl p-4 shadow-xl flex flex-col gap-3">
      {/* Header */}
      <div className="flex items-center justify-between pb-2 border-b border-slate-800 text-xs font-mono text-slate-300">
        <div className="flex items-center gap-2 min-w-0">
          <ListOrdered className="w-4 h-4 text-cyan-400 shrink-0" />
          <span className="truncate">ACTIVE TASK: {currentPlan.user_prompt}</span>
        </div>
        <span className={`ml-2 shrink-0 text-[10px] px-2 py-0.5 rounded border font-bold ${getPlanStatusColor(currentPlan.status)}`}>
          {currentPlan.status}
        </span>
      </div>

      {/* Progress bar */}
      {totalSteps > 0 && (
        <div className="w-full bg-slate-800 rounded-full h-1">
          <div
            className="bg-gradient-to-r from-cyan-500 to-purple-500 h-1 rounded-full transition-all duration-500"
            style={{ width: `${(completedSteps / totalSteps) * 100}%` }}
          />
        </div>
      )}

      {/* Steps */}
      <div className="space-y-2 mt-1">
        {currentPlan.steps.map((step, idx) => (
          <div
            key={step.step_id}
            className={`p-2.5 rounded-xl border text-xs transition-all ${
              step.status === "RUNNING"
                ? "bg-cyan-500/10 border-cyan-500/40 shadow-[0_0_8px_rgba(0,240,255,0.1)]"
                : step.status === "COMPLETED"
                ? "bg-slate-950/40 border-emerald-500/30"
                : step.status === "FAILED"
                ? "bg-rose-950/30 border-rose-500/30"
                : "bg-slate-950/30 border-slate-800/80"
            }`}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 min-w-0">
                {step.status === "RUNNING" && (
                  <Zap className="w-3 h-3 text-cyan-400 shrink-0 animate-pulse" />
                )}
                <span className="font-mono text-slate-500 shrink-0">#{idx + 1}</span>
                <span className="font-semibold text-slate-200 truncate">{step.description}</span>
              </div>
              <div className="shrink-0 ml-2">{getStatusBadge(step.status)}</div>
            </div>
            <div className="mt-1 flex items-center gap-3 text-[11px] font-mono text-slate-400">
              <span>TOOL: <strong className="text-cyan-300">{step.tool_name}</strong></span>
              <span>RISK: <strong className={step.risk_tier.includes("SAFE") ? "text-emerald-400" : "text-amber-400"}>{step.risk_tier}</strong></span>
            </div>
            {step.status === "FAILED" && step.error && (
              <div className="mt-1 text-[11px] text-rose-400 font-mono truncate">
                ⚠ {step.error}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Approval buttons */}
      {currentPlan.status === "AWAITING_APPROVAL" && onApproveTier2Plan && onCancelPlan && (
        <div className="mt-2 pt-3 border-t border-slate-800 flex items-center justify-end gap-3">
          <button
            onClick={() => onCancelPlan(currentPlan.plan_id)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-rose-500/40 bg-rose-500/10 text-rose-300 hover:bg-rose-500/20 text-xs font-mono transition"
          >
            <Ban className="w-3.5 h-3.5" />
            <span>REJECT</span>
          </button>
          <button
            onClick={() => onApproveTier2Plan(currentPlan.plan_id)}
            className="flex items-center gap-1.5 px-4 py-1.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs font-mono transition shadow-[0_0_12px_rgba(0,240,255,0.3)]"
          >
            <Play className="w-3.5 h-3.5 fill-current" />
            <span>APPROVE &amp; EXECUTE</span>
          </button>
        </div>
      )}

      {/* Completion summary */}
      {currentPlan.status === "COMPLETED" && (
        <div className="mt-1 pt-2 border-t border-slate-800 text-[11px] font-mono text-emerald-400 flex items-center gap-2">
          <CheckCircle2 className="w-3.5 h-3.5" />
          <span>All {totalSteps} steps completed successfully.</span>
        </div>
      )}
    </div>
  );
};
