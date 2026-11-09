"use client";

import React from "react";
import { motion } from "framer-motion";
import { AppState } from "@nova/protocol";

interface NovaOrbProps {
  state: AppState;
  audioVolume: number; // 0.0 to 1.0
  onClick?: () => void;
}

export const NovaOrb: React.FC<NovaOrbProps> = ({ state, audioVolume, onClick }) => {
  // Determine color themes based on application state
  const getStateColors = () => {
    switch (state) {
      case "LISTENING":
        return {
          glow: "rgba(0, 240, 255, 0.6)",
          outerRing: "border-cyan-400",
          innerRing: "border-sky-300",
          coreGradient: "from-cyan-400 via-sky-500 to-blue-600",
          statusText: "LISTENING...",
          textColor: "text-cyan-400",
        };
      case "THINKING":
        return {
          glow: "rgba(168, 85, 247, 0.6)",
          outerRing: "border-purple-400",
          innerRing: "border-fuchsia-300",
          coreGradient: "from-purple-500 via-indigo-600 to-fuchsia-500",
          statusText: "THINKING...",
          textColor: "text-purple-400",
        };
      case "EXECUTING":
        return {
          glow: "rgba(234, 179, 8, 0.6)",
          outerRing: "border-amber-400",
          innerRing: "border-yellow-300",
          coreGradient: "from-amber-400 via-orange-500 to-yellow-600",
          statusText: "EXECUTING TASK...",
          textColor: "text-amber-400",
        };
      case "SPEAKING":
        return {
          glow: "rgba(16, 185, 129, 0.7)",
          outerRing: "border-emerald-400",
          innerRing: "border-teal-300",
          coreGradient: "from-emerald-400 via-teal-500 to-green-600",
          statusText: "SPEAKING...",
          textColor: "text-emerald-400",
        };
      case "ERROR":
        return {
          glow: "rgba(239, 68, 68, 0.7)",
          outerRing: "border-red-500",
          innerRing: "border-rose-400",
          coreGradient: "from-red-600 via-rose-600 to-red-800",
          statusText: "SYSTEM ALERT",
          textColor: "text-red-400",
        };
      case "IDLE":
      default:
        return {
          glow: "rgba(0, 240, 255, 0.25)",
          outerRing: "border-cyan-500/30",
          innerRing: "border-purple-500/40",
          coreGradient: "from-cyan-500 via-indigo-500 to-purple-600",
          statusText: "NOVA READY",
          textColor: "text-slate-400",
        };
    }
  };

  const theme = getStateColors();

  // Dynamic reactive scaling based on real audio level or state
  const reactiveScale = 1 + (state === "LISTENING" || state === "SPEAKING" ? audioVolume * 0.45 : 0);

  return (
    <div className="flex flex-col items-center justify-center select-none" onClick={onClick}>
      <div className="relative w-64 h-64 flex items-center justify-center cursor-pointer group">
        {/* Ambient Outer Halo */}
        <motion.div
          animate={{
            scale: [1 * reactiveScale, 1.15 * reactiveScale, 1 * reactiveScale],
            opacity: state === "ERROR" ? [0.6, 1, 0.6] : [0.3, 0.6, 0.3],
          }}
          transition={{
            repeat: Infinity,
            duration: state === "THINKING" ? 1.5 : 3.5,
            ease: "easeInOut",
          }}
          className="absolute inset-0 rounded-full blur-2xl"
          style={{ background: theme.glow }}
        />

        {/* Outer Orbital Rotating Ring */}
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ repeat: Infinity, duration: state === "THINKING" ? 4 : 20, ease: "linear" }}
          className={`absolute w-56 h-56 rounded-full border-2 border-dashed ${theme.outerRing} opacity-60`}
        />

        {/* Middle Counter-Rotating Holographic Ring */}
        <motion.div
          animate={{ rotate: -360 }}
          transition={{ repeat: Infinity, duration: state === "THINKING" ? 6 : 28, ease: "linear" }}
          className={`absolute w-44 h-44 rounded-full border ${theme.innerRing} opacity-40`}
          style={{
            borderTopColor: "transparent",
            borderBottomColor: "transparent",
          }}
        />

        {/* Core Glowing Orb with Reactive Breathing */}
        <motion.div
          animate={{
            scale: [1 * reactiveScale, 1.06 * reactiveScale, 1 * reactiveScale],
          }}
          transition={{
            repeat: Infinity,
            duration: state === "LISTENING" ? 0.8 : 2.5,
            ease: "easeInOut",
          }}
          className={`w-32 h-32 rounded-full bg-gradient-to-tr ${theme.coreGradient} shadow-2xl flex items-center justify-center backdrop-blur-md relative overflow-hidden`}
        >
          {/* Inner Light Flare */}
          <div className="absolute -top-6 -left-6 w-20 h-20 bg-white/30 rounded-full blur-md pointer-events-none" />
          <div className="w-16 h-16 rounded-full bg-slate-950/40 backdrop-blur-sm border border-white/20 flex items-center justify-center">
            <span className="w-4 h-4 rounded-full bg-white/80 shadow-[0_0_10px_#ffffff] animate-ping" />
          </div>
        </motion.div>
      </div>

      {/* State Text Label */}
      <motion.div
        key={state}
        initial={{ opacity: 0, y: 5 }}
        animate={{ opacity: 1, y: 0 }}
        className="mt-4 flex items-center gap-2 font-mono text-xs tracking-wider"
      >
        <span className={`font-semibold ${theme.textColor}`}>{theme.statusText}</span>
      </motion.div>
    </div>
  );
};
