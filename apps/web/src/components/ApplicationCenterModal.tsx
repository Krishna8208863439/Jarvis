import React, { useState, useEffect } from "react";
import { Grid, Search, Plus, Play, CheckCircle, Shield, X, RefreshCw } from "lucide-react";

export interface DiscoveredApp {
  app_id: string;
  name: string;
  platform: string;
  executable_path?: string;
  launch_command: string;
  is_available: boolean;
  capabilities: string[];
  category: string;
}

interface ApplicationCenterModalProps {
  isOpen: boolean;
  onClose: () => void;
  onLaunchApp: (appName: string) => void;
}

export const ApplicationCenterModal: React.FC<ApplicationCenterModalProps> = ({
  isOpen,
  onClose,
  onLaunchApp,
}) => {
  const [apps, setApps] = useState<DiscoveredApp[]>([]);
  const [search, setSearch] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("all");
  const [loading, setLoading] = useState(false);

  // Manual register form
  const [isRegistering, setIsRegistering] = useState(false);
  const [customId, setCustomId] = useState("");
  const [customName, setCustomName] = useState("");
  const [customCmd, setCustomCmd] = useState("");

  const fetchApps = () => {
    setLoading(true);
    fetch("http://localhost:8000/api/v1/operator/apps")
      .then((res) => res.json())
      .then((data) => {
        setApps(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  };

  useEffect(() => {
    if (isOpen) {
      fetchApps();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const filteredApps = apps.filter((app) => {
    const matchesSearch =
      app.name.toLowerCase().includes(search.toLowerCase()) ||
      app.app_id.toLowerCase().includes(search.toLowerCase());
    const matchesCat = categoryFilter === "all" || app.category.toLowerCase() === categoryFilter.toLowerCase();
    return matchesSearch && matchesCat;
  });

  const handleManualRegister = (e: React.FormEvent) => {
    e.preventDefault();
    if (customId && customName && customCmd) {
      fetch("http://localhost:8000/api/v1/operator/apps/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          app_id: customId,
          name: customName,
          launch_command: customCmd,
          category: "User Custom",
        }),
      })
        .then((r) => r.json())
        .then((newApp) => {
          setApps((prev) => [...prev, newApp]);
          setIsRegistering(false);
          setCustomId("");
          setCustomName("");
          setCustomCmd("");
        });
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fade-in">
      <div className="w-full max-w-4xl bg-slate-900 border border-slate-800 rounded-3xl shadow-2xl p-6 text-slate-100 flex flex-col max-h-[85vh]">
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
              <Grid className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-100 flex items-center gap-2">
                <span>UNIVERSAL APPLICATION CENTER</span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-300 border border-cyan-500/20">
                  {apps.length} DISCOVERED
                </span>
              </h2>
              <p className="text-xs text-slate-400">
                Discovered installed applications and authorized controls on this device.
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={fetchApps}
              className="p-2 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-slate-300 transition"
              title="Rescan Applications"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
            </button>
            <button
              onClick={onClose}
              className="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800 transition"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Search & Filter Bar */}
        <div className="flex flex-col sm:flex-row items-center gap-3 my-4">
          <div className="relative flex-1 w-full">
            <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
            <input
              type="text"
              placeholder="Search by application name (e.g. VS Code, Excel, Chrome, Word)..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-10 pr-4 py-2 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-200 focus:outline-none focus:border-cyan-400 font-mono"
            />
          </div>

          <div className="flex items-center gap-2 w-full sm:w-auto justify-between">
            <div className="flex items-center gap-1 overflow-x-auto text-xs font-mono">
              {["all", "Productivity", "Browser", "System", "Development", "Media"].map((cat) => (
                <button
                  key={cat}
                  onClick={() => setCategoryFilter(cat)}
                  className={`px-3 py-1.5 rounded-lg border transition ${
                    categoryFilter === cat
                      ? "border-cyan-400 bg-cyan-500/10 text-cyan-300 font-semibold"
                      : "border-slate-800 bg-slate-950/60 text-slate-400 hover:text-slate-200"
                  }`}
                >
                  {cat}
                </button>
              ))}
            </div>

            <button
              onClick={() => setIsRegistering(!isRegistering)}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-mono font-semibold transition shrink-0"
            >
              <Plus className="w-3.5 h-3.5" />
              <span>Register App</span>
            </button>
          </div>
        </div>

        {/* Manual Register Drawer */}
        {isRegistering && (
          <form
            onSubmit={handleManualRegister}
            className="mb-4 p-4 rounded-2xl bg-slate-950 border border-purple-500/30 grid grid-cols-1 sm:grid-cols-4 gap-2 text-xs"
          >
            <input
              type="text"
              placeholder="App ID (e.g., blender)"
              value={customId}
              onChange={(e) => setCustomId(e.target.value)}
              className="px-3 py-2 rounded-lg bg-slate-900 border border-slate-800 text-slate-200"
              required
            />
            <input
              type="text"
              placeholder="Display Name (e.g., Blender 3D)"
              value={customName}
              onChange={(e) => setCustomName(e.target.value)}
              className="px-3 py-2 rounded-lg bg-slate-900 border border-slate-800 text-slate-200"
              required
            />
            <input
              type="text"
              placeholder="Executable Command or Path"
              value={customCmd}
              onChange={(e) => setCustomCmd(e.target.value)}
              className="px-3 py-2 rounded-lg bg-slate-900 border border-slate-800 text-slate-200 font-mono"
              required
            />
            <button
              type="submit"
              className="px-4 py-2 rounded-lg bg-purple-600 hover:bg-purple-500 font-bold text-white transition"
            >
              Save Application
            </button>
          </form>
        )}

        {/* Application Cards Grid */}
        <div className="flex-1 overflow-y-auto pr-1 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 custom-scrollbar">
          {filteredApps.map((app) => (
            <div
              key={app.app_id}
              className="p-3.5 rounded-2xl bg-slate-950/70 border border-slate-800/80 hover:border-slate-700 transition flex flex-col justify-between group"
            >
              <div>
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-slate-200 text-xs">{app.name}</span>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-900 text-slate-400 border border-slate-800">
                    {app.category}
                  </span>
                </div>
                <div className="text-[11px] font-mono text-slate-500 truncate mt-1">
                  CMD: {app.launch_command}
                </div>

                {/* Capability Badges */}
                <div className="flex items-center gap-1 mt-2 flex-wrap">
                  {app.capabilities.map((cap) => (
                    <span
                      key={cap}
                      className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-cyan-500/10 text-cyan-300 border border-cyan-500/20"
                    >
                      {cap}
                    </span>
                  ))}
                </div>
              </div>

              <div className="mt-3 pt-2.5 border-t border-slate-800/80 flex items-center justify-between">
                <span className="text-[10px] font-mono text-emerald-400 flex items-center gap-1">
                  <CheckCircle className="w-3 h-3" /> Ready
                </span>
                <button
                  onClick={() => {
                    onLaunchApp(app.name);
                    onClose();
                  }}
                  className="flex items-center gap-1.5 px-3 py-1 rounded-lg bg-cyan-500/20 hover:bg-cyan-500 text-cyan-300 hover:text-slate-950 text-xs font-mono font-semibold transition"
                >
                  <Play className="w-3 h-3 fill-current" />
                  <span>Launch</span>
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
