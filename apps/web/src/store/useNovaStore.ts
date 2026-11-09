import { create } from "zustand";
import { AppState, LanguageCode, VoiceGender, DeviceInfo } from "@nova/protocol";

export interface TranscriptMessage {
  id: string;
  sender: "user" | "nova";
  text: string;
  timestamp: string;
  language?: LanguageCode;
}

export interface TaskTimelineItem {
  id: string;
  title: string;
  toolName: string;
  status: "PENDING" | "RUNNING" | "COMPLETED" | "FAILED";
  timestamp: string;
}

export interface MemoryItem {
  id: string;
  key: string;
  value: string;
  user_approved: boolean;
  created_at: string;
}

export interface MultiStepPlan {
  plan_id: string;
  user_prompt: string;
  status: "PLANNING" | "AWAITING_APPROVAL" | "EXECUTING" | "COMPLETED" | "CANCELLED" | "FAILED";
  steps: {
    step_id: string;
    tool_name: string;
    risk_tier: string;
    description: string;
    status: "PENDING" | "RUNNING" | "COMPLETED" | "FAILED";
    error?: string;
  }[];
}

interface NovaStore {
  appState: AppState;
  setAppState: (state: AppState) => void;

  // Audio / Mic
  isMicActive: boolean;
  setIsMicActive: (active: boolean) => void;
  audioVolume: number;
  setAudioVolume: (vol: number) => void;

  // Settings
  language: LanguageCode;
  setLanguage: (lang: LanguageCode) => void;
  voiceGender: VoiceGender;
  setVoiceGender: (gender: VoiceGender) => void;
  voiceSpeed: number;
  setVoiceSpeed: (speed: number) => void;

  // UI Panels
  isSettingsOpen: boolean;
  setIsSettingsOpen: (open: boolean) => void;

  // Transcript & History
  transcripts: TranscriptMessage[];
  addTranscript: (msg: TranscriptMessage) => void;
  clearTranscripts: () => void;

  // Connected Devices
  devices: DeviceInfo[];
  setDevices: (devices: DeviceInfo[]) => void;

  // Timeline
  timeline: TaskTimelineItem[];
  addTimelineItem: (item: TaskTimelineItem) => void;

  // User-Approved Memory
  memories: MemoryItem[];
  addMemory: (key: string, value: string) => void;
  deleteMemory: (id: string) => void;

  // Active Multi-step Plan
  activePlan: MultiStepPlan | null;
  setActivePlan: (plan: MultiStepPlan | null) => void;

  // Error Info
  errorMessage: string | null;
  setErrorMessage: (msg: string | null) => void;
}

export const useNovaStore = create<NovaStore>((set) => ({
  appState: "IDLE",
  setAppState: (state) => set({ appState: state }),

  isMicActive: false,
  setIsMicActive: (active) => set({ isMicActive: active }),
  audioVolume: 0,
  setAudioVolume: (audioVolume) => set({ audioVolume }),

  language: "en",
  setLanguage: (language) => set({ language }),
  voiceGender: "female",
  setVoiceGender: (voiceGender) => set({ voiceGender }),
  voiceSpeed: 1.0,
  setVoiceSpeed: (voiceSpeed) => set({ voiceSpeed }),

  isSettingsOpen: false,
  setIsSettingsOpen: (isSettingsOpen) => set({ isSettingsOpen }),

  transcripts: [
    {
      id: "initial-1",
      sender: "nova",
      text: "Hello! I am NOVA, your neural operating assistant. How can I assist you today?",
      timestamp: "",
    },
  ],
  addTranscript: (msg) => set((s) => ({ transcripts: [...s.transcripts, msg] })),
  clearTranscripts: () => set({ transcripts: [] }),

  devices: [
    {
      deviceId: "local-web",
      name: "Browser Client (Active)",
      platform: "web",
      osVersion: "Web Standards API",
      capabilities: ["audio.record", "audio.playback", "stt", "tts"],
      isOnline: true,
      lastSeenAt: "Just now",
    },
  ],
  setDevices: (devices) => set({ devices }),

  timeline: [
    {
      id: "t-1",
      title: "Core Hub Synchronized",
      toolName: "system.init",
      status: "COMPLETED",
      timestamp: "13:28",
    },
  ],
  addTimelineItem: (item) => set((s) => ({ timeline: [...s.timeline, item] })),

  memories: [
    {
      id: "mem-1",
      key: "preferred_name",
      value: "Krishna",
      user_approved: true,
      created_at: new Date().toISOString(),
    },
    {
      id: "mem-2",
      key: "target_career_role",
      value: "Python / AI Engineer",
      user_approved: true,
      created_at: new Date().toISOString(),
    },
  ],
  addMemory: (key, value) =>
    set((s) => ({
      memories: [
        ...s.memories,
        {
          id: `mem-${Date.now()}`,
          key,
          value,
          user_approved: true,
          created_at: new Date().toISOString(),
        },
      ],
    })),
  deleteMemory: (id) =>
    set((s) => ({
      memories: s.memories.filter((m) => m.id !== id),
    })),

  activePlan: {
    plan_id: "plan-wf1",
    user_prompt: "Prepare project report and save to desktop",
    status: "AWAITING_APPROVAL",
    steps: [
      {
        step_id: "step-1",
        tool_name: "internet.search_jobs",
        risk_tier: "TIER_0_SAFE",
        description: "Gather research data on Project NOVA architecture",
        status: "COMPLETED",
      },
      {
        step_id: "step-2",
        tool_name: "desktop.create_document",
        risk_tier: "TIER_2_SENSITIVE",
        description: "Save Project_Nova_Report.txt to Desktop",
        status: "PENDING",
      },
    ],
  },
  setActivePlan: (activePlan) => set({ activePlan }),

  errorMessage: null,
  setErrorMessage: (errorMessage) => set({ errorMessage }),
}));

