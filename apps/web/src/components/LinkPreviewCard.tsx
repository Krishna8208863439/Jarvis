"use client";

import React, { useState, useEffect } from "react";
import { ExternalLink, Globe, Sparkles, Shield, Cpu, Mic, Layers, ArrowUpRight } from "lucide-react";

interface UrlMetadata {
  url: string;
  title: string;
  description: string;
  siteName: string;
  image?: string;
  themeColor?: string;
  isProjectNova?: boolean;
}

export function extractUrls(text: string): string[] {
  const urlRegex = /(https?:\/\/[^\s]+)/g;
  const matches = text.match(urlRegex);
  return matches ? Array.from(new Set(matches)) : [];
}

export const LinkPreviewCard: React.FC<{ url: string }> = ({ url }) => {
  const [meta, setMeta] = useState<UrlMetadata | null>(null);

  useEffect(() => {
    let hostname = "";
    try {
      hostname = new URL(url).hostname;
    } catch {
      hostname = url;
    }

    // Specialized Project NOVA rich preview card if url references local host, nova domain, or project repository
    const isNova =
      hostname.includes("localhost") ||
      hostname.includes("nova") ||
      url.toLowerCase().includes("nova") ||
      url.toLowerCase().includes("project");

    if (isNova) {
      setMeta({
        url,
        title: "PROJECT NOVA — Real-World JARVIS AI Assistant",
        description:
          "Neural Operating & Virtual Assistant: Multilingual voice reasoning, dynamic desktop application control, and autonomous verified workflows.",
        siteName: "PROJECT NOVA Core Hub",
        image: "/og-image.svg",
        themeColor: "#00f0ff",
        isProjectNova: true,
      });
    } else if (hostname.includes("github.com")) {
      setMeta({
        url,
        title: "GitHub Repository",
        description: "Source code repository and developer documentation.",
        siteName: "GitHub",
        themeColor: "#2dba4e",
      });
    } else if (hostname.includes("google.com")) {
      setMeta({
        url,
        title: "Google Search",
        description: "Web search results and external knowledge retrieval.",
        siteName: "Google",
        themeColor: "#4285f4",
      });
    } else if (hostname.includes("youtube.com") || hostname.includes("youtu.be")) {
      setMeta({
        url,
        title: "YouTube Video / Media",
        description: "Media playback and video streaming via Project NOVA Media Connector.",
        siteName: "YouTube",
        themeColor: "#ff0000",
      });
    } else {
      setMeta({
        url,
        title: hostname,
        description: `External link to ${url}`,
        siteName: hostname,
        themeColor: "#38bdf8",
      });
    }
  }, [url]);

  if (!meta) return null;

  return (
    <a
      href={meta.url}
      target="_blank"
      rel="noopener noreferrer"
      className="mt-2.5 block text-left group no-underline"
    >
      <div className="overflow-hidden rounded-xl border border-slate-800 bg-slate-950/70 hover:border-cyan-500/50 hover:bg-slate-900/80 transition-all duration-300 shadow-lg hover:shadow-[0_0_20px_rgba(0,240,255,0.15)]">
        {/* If Project NOVA link: render branded visual header */}
        {meta.isProjectNova && (
          <div className="relative h-28 w-full bg-gradient-to-br from-slate-950 via-[#0a1128] to-slate-900 overflow-hidden border-b border-slate-800/80 p-3 flex items-center justify-between">
            {/* Ambient Cyan glow */}
            <div className="absolute -left-10 -top-10 w-32 h-32 bg-cyan-500/20 rounded-full blur-2xl pointer-events-none" />
            <div className="absolute right-0 bottom-0 w-32 h-32 bg-purple-500/20 rounded-full blur-2xl pointer-events-none" />

            <div className="z-10 flex flex-col justify-center">
              <div className="flex items-center gap-1.5 text-[10px] font-mono font-bold text-cyan-400 uppercase tracking-widest">
                <Sparkles className="w-3 h-3 text-cyan-400 animate-pulse" />
                <span>AI Operating System</span>
              </div>
              <h4 className="text-base font-black tracking-wider text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-purple-300 to-pink-400 font-mono mt-0.5">
                PROJECT NOVA
              </h4>
              <p className="text-[11px] text-slate-400 font-mono mt-0.5">
                Neural Operating &amp; Virtual Assistant
              </p>
            </div>

            {/* Glowing Orb Miniature badge */}
            <div className="z-10 relative flex items-center justify-center w-14 h-14 rounded-full bg-slate-900/90 border border-cyan-500/40 shadow-[0_0_15px_rgba(0,240,255,0.3)]">
              <div className="w-7 h-7 rounded-full bg-gradient-to-br from-cyan-400 to-purple-500 animate-pulse" />
              <div className="absolute inset-0 rounded-full border border-cyan-400/30 animate-spin" style={{ animationDuration: "8s" }} />
            </div>
          </div>
        )}

        {/* Content body */}
        <div className="p-3">
          <div className="flex items-center justify-between text-[10px] font-mono text-slate-500 mb-1">
            <span className="flex items-center gap-1 text-cyan-400">
              <Globe className="w-3 h-3" />
              {meta.siteName}
            </span>
            <span className="flex items-center gap-1 group-hover:text-cyan-300 transition-colors">
              Visit Link <ArrowUpRight className="w-3 h-3" />
            </span>
          </div>

          <div className="font-semibold text-slate-200 text-xs line-clamp-1 group-hover:text-cyan-300 transition-colors">
            {meta.title}
          </div>

          <p className="text-[11px] text-slate-400 mt-1 line-clamp-2 leading-relaxed">
            {meta.description}
          </p>

          {/* Feature tags for Project NOVA */}
          {meta.isProjectNova && (
            <div className="mt-2.5 pt-2 border-t border-slate-800/80 flex items-center gap-2 flex-wrap text-[10px] font-mono text-slate-400">
              <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded bg-cyan-500/10 text-cyan-300 border border-cyan-500/20">
                <Mic className="w-2.5 h-2.5" /> Voice
              </span>
              <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded bg-purple-500/10 text-purple-300 border border-purple-500/20">
                <Layers className="w-2.5 h-2.5" /> OS Control
              </span>
              <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/20">
                <Cpu className="w-2.5 h-2.5" /> Local Ollama
              </span>
              <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                <Shield className="w-2.5 h-2.5" /> 4-Tier Security
              </span>
            </div>
          )}
        </div>
      </div>
    </a>
  );
};

