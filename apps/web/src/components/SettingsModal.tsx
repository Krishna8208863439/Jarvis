"use client";

import React from "react";
import { LanguageCode, VoiceGender } from "@nova/protocol";
import { Settings as SettingsIcon, Volume2, Globe, UserCheck, X } from "lucide-react";

interface SettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
  language: LanguageCode;
  onLanguageChange: (lang: LanguageCode) => void;
  voiceGender: VoiceGender;
  onVoiceGenderChange: (gender: VoiceGender) => void;
  voiceSpeed: number;
  onVoiceSpeedChange: (speed: number) => void;
}

export const SettingsModal: React.FC<SettingsModalProps> = ({
  isOpen,
  onClose,
  language,
  onLanguageChange,
  voiceGender,
  onVoiceGenderChange,
  voiceSpeed,
  onVoiceSpeedChange,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fade-in">
      <div className="w-full max-w-md bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl p-6 text-slate-100 relative">
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div className="flex items-center gap-2 text-cyan-400 font-mono text-sm uppercase">
            <SettingsIcon className="w-4 h-4" />
            <span>Voice &amp; Neural Preferences</span>
          </div>
          <button onClick={onClose} className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="mt-5 space-y-5">
          {/* Language Selection */}
          <div>
            <label className="flex items-center gap-2 text-xs font-mono text-slate-400 mb-2">
              <Globe className="w-3.5 h-3.5 text-cyan-400" />
              <span>ACTIVE LANGUAGE</span>
            </label>
            <div className="grid grid-cols-3 gap-2">
              {[
                { code: "en", label: "English" },
                { code: "hi", label: "हिन्दी (Hindi)" },
                { code: "mr", label: "मराठी (Marathi)" },
              ].map((item) => (
                <button
                  key={item.code}
                  onClick={() => onLanguageChange(item.code as LanguageCode)}
                  className={`py-2 px-3 rounded-xl text-xs font-medium border transition-all ${
                    language === item.code
                      ? "border-cyan-400 bg-cyan-500/10 text-cyan-300"
                      : "border-slate-800 bg-slate-950/60 text-slate-400 hover:border-slate-700"
                  }`}
                >
                  {item.label}
                </button>
              ))}
            </div>
          </div>

          {/* Voice Gender Selection */}
          <div>
            <label className="flex items-center gap-2 text-xs font-mono text-slate-400 mb-2">
              <UserCheck className="w-3.5 h-3.5 text-purple-400" />
              <span>VOICE SELECTION</span>
            </label>
            <div className="grid grid-cols-2 gap-2">
              {[
                { id: "female", label: "Female (Neural)" },
                { id: "male", label: "Male (Neural)" },
              ].map((item) => (
                <button
                  key={item.id}
                  onClick={() => onVoiceGenderChange(item.id as VoiceGender)}
                  className={`py-2 px-3 rounded-xl text-xs font-medium border transition-all ${
                    voiceGender === item.id
                      ? "border-purple-400 bg-purple-500/10 text-purple-300"
                      : "border-slate-800 bg-slate-950/60 text-slate-400 hover:border-slate-700"
                  }`}
                >
                  {item.label}
                </button>
              ))}
            </div>
          </div>

          {/* Voice Speed Slider */}
          <div>
            <div className="flex items-center justify-between text-xs font-mono text-slate-400 mb-2">
              <span className="flex items-center gap-2">
                <Volume2 className="w-3.5 h-3.5 text-emerald-400" />
                <span>SPEECH RATE</span>
              </span>
              <span className="text-cyan-400">{voiceSpeed.toFixed(1)}x</span>
            </div>
            <input
              type="range"
              min="0.5"
              max="2.0"
              step="0.1"
              value={voiceSpeed}
              onChange={(e) => onVoiceSpeedChange(parseFloat(e.target.value))}
              className="w-full accent-cyan-400 cursor-pointer"
            />
          </div>
        </div>

        <div className="mt-6 pt-4 border-t border-slate-800 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-semibold text-xs transition"
          >
            Apply Settings
          </button>
        </div>
      </div>
    </div>
  );
};

