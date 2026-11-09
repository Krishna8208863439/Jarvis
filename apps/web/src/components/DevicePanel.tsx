"use client";

import React from "react";
import { DeviceInfo } from "@nova/protocol";
import { Laptop, Smartphone, Globe, ShieldCheck } from "lucide-react";

interface DevicePanelProps {
  devices: DeviceInfo[];
}

export const DevicePanel: React.FC<DevicePanelProps> = ({ devices }) => {
  const getDeviceIcon = (platform: string) => {
    switch (platform) {
      case "android":
      case "ios":
        return <Smartphone className="w-4 h-4 text-emerald-400" />;
      case "windows":
      case "macos":
      case "linux":
      case "desktop":
        return <Laptop className="w-4 h-4 text-cyan-400" />;
      default:
        return <Globe className="w-4 h-4 text-purple-400" />;
    }
  };

  return (
    <div className="bg-slate-900/50 backdrop-blur-md border border-slate-800 rounded-2xl p-4 shadow-xl flex flex-col gap-3">
      <div className="flex items-center justify-between pb-2 border-b border-slate-800 text-xs font-mono text-slate-300">
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-cyan-400" />
          <span>REGISTERED DEVICE MESH</span>
        </div>
        <span className="text-[10px] text-emerald-400 font-bold px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/30">
          {devices.length} ONLINE
        </span>
      </div>

      <div className="space-y-2">
        {devices.map((device) => (
          <div
            key={device.deviceId}
            className="flex items-center justify-between p-2.5 rounded-xl bg-slate-950/40 border border-slate-800/80 hover:border-slate-700 transition"
          >
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-slate-900 border border-slate-800">
                {getDeviceIcon(device.platform)}
              </div>
              <div>
                <div className="text-xs font-semibold text-slate-200">{device.name}</div>
                <div className="text-[10px] text-slate-500 font-mono">{device.osVersion}</div>
              </div>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-400 shadow-[0_0_8px_#34d399]" />
              <span className="text-[10px] font-mono text-emerald-400">ACTIVE</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

