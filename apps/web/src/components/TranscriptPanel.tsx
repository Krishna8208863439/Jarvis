"use client";

import React, { useRef, useEffect } from "react";
import { TranscriptMessage } from "../store/useNovaStore";
import { MessageSquare, Bot, User } from "lucide-react";
import { LinkPreviewCard, extractUrls } from "./LinkPreviewCard";

interface TranscriptPanelProps {
  transcripts: TranscriptMessage[];
  onClear: () => void;
}

export const TranscriptPanel: React.FC<TranscriptPanelProps> = ({ transcripts, onClear }) => {
  const bottomRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [transcripts]);

  return (
    <div className="flex flex-col h-full bg-slate-900/50 backdrop-blur-md border border-slate-800 rounded-2xl p-4 shadow-xl">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2 text-cyan-400 font-mono text-xs uppercase tracking-wider">
          <MessageSquare className="w-4 h-4" />
          <span>Live Conversation Stream</span>
        </div>
        <button
          onClick={onClear}
          className="text-[11px] font-mono text-slate-500 hover:text-slate-300 transition-colors"
        >
          CLEAR
        </button>
      </div>

      <div className="flex-1 overflow-y-auto space-y-3 py-3 pr-1 text-sm custom-scrollbar">
        {transcripts.map((msg) => {
          const urls = extractUrls(msg.text);
          return (
            <div
              key={msg.id}
              className={`flex gap-3 ${msg.sender === "user" ? "flex-row-reverse text-right" : "flex-row"}`}
            >
              <div
                className={`w-7 h-7 rounded-lg flex items-center justify-center shrink-0 ${
                  msg.sender === "user" ? "bg-cyan-600/30 text-cyan-300" : "bg-purple-600/30 text-purple-300"
                }`}
              >
                {msg.sender === "user" ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>

              <div
                className={`max-w-[85%] rounded-xl px-3.5 py-2 text-xs leading-relaxed ${
                  msg.sender === "user"
                    ? "bg-cyan-500/10 border border-cyan-500/30 text-cyan-100"
                    : "bg-slate-800/80 border border-slate-700/60 text-slate-200 text-left"
                }`}
              >
                <div className="text-[10px] text-slate-500 font-mono mb-1">{msg.timestamp}</div>
                <div>{msg.text}</div>

                {/* Rich Link Preview Cards */}
                {urls.length > 0 && (
                  <div className="mt-2 space-y-2">
                    {urls.map((url, idx) => (
                      <LinkPreviewCard key={`${msg.id}-url-${idx}`} url={url} />
                    ))}
                  </div>
                )}
              </div>
            </div>
          );
        })}
        <div ref={bottomRef} />
      </div>
    </div>
  );
};
