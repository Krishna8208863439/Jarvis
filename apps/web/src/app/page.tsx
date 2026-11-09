"use client";

import { useEffect, useState, useRef } from "react";
import { AppState } from "@nova/protocol";
import { useNovaStore } from "../store/useNovaStore";
import { NovaOrb } from "../components/NovaOrb";
import { AudioWaveform } from "../components/AudioWaveform";
import { TranscriptPanel } from "../components/TranscriptPanel";
import { DevicePanel } from "../components/DevicePanel";
import { SettingsModal } from "../components/SettingsModal";
import { MemoryManagerModal } from "../components/MemoryManagerModal";
import { ApplicationCenterModal } from "../components/ApplicationCenterModal";
import { TaskExecutionWidget } from "../components/TaskExecutionWidget";
import { VoiceRecognitionClient } from "../lib/voiceRecognition";
import { AudioPlaybackController } from "../lib/audioPlayback";
import { WakeWordDetector } from "../lib/wakeWordDetector";
import { Mic, MicOff, Settings, ShieldAlert, Cpu, Volume2, Square, Radio, Brain, MessageSquare, Laptop, ListOrdered, Sparkles, Grid } from "lucide-react";

export default function Home() {
  const {
    appState,
    setAppState,
    isMicActive,
    setIsMicActive,
    audioVolume,
    setAudioVolume,
    language,
    setLanguage,
    voiceGender,
    setVoiceGender,
    voiceSpeed,
    setVoiceSpeed,
    isSettingsOpen,
    setIsSettingsOpen,
    transcripts,
    addTranscript,
    clearTranscripts,
    devices,
    activePlan,
    setActivePlan,
    memories,
    addMemory,
    deleteMemory,
  } = useNovaStore();

  const [coreStatus, setCoreStatus] = useState<string>("Checking...");
  const [isMemoryOpen, setIsMemoryOpen] = useState<boolean>(false);
  const [isAppCenterOpen, setIsAppCenterOpen] = useState<boolean>(false);
  const [mobileTab, setMobileTab] = useState<"assistant" | "transcripts" | "devices" | "tasks">("assistant");
  const [isWakeWordActive, setIsWakeWordActive] = useState<boolean>(true);
  const recognitionRef = useRef<VoiceRecognitionClient | null>(null);
  const playbackRef = useRef<AudioPlaybackController | null>(null);
  const wakeWordRef = useRef<WakeWordDetector | null>(null);

  // Initialize Wake Word Detector & Continuous Background Listener
  useEffect(() => {
    wakeWordRef.current = new WakeWordDetector({
      sensitivity: 0.8,
      onWakeWordDetected: () => {
        addTranscript({
          id: Date.now().toString(),
          sender: "nova",
          text: "Hello! I'm here. What can I do for you?",
          timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        });
        triggerSpokenResponse("Hello! I'm here. What can I do for you?");
        setIsMicActive(true);
        setAppState("LISTENING");
        startContinuousListening();
      },
      onEmergencyStopDetected: () => {
        emergencyStop();
      },
    });

    if (isWakeWordActive) {
      wakeWordRef.current.start();
    }

    return () => {
      wakeWordRef.current?.stop();
    };
  }, [isWakeWordActive]);

  // Initialize Audio Playback controller with Barge-in state listener
  useEffect(() => {
    playbackRef.current = new AudioPlaybackController((speaking) => {
      if (speaking) {
        setAppState("SPEAKING");
      } else {
        setAppState("IDLE");
      }
    });
  }, []);

  // Initialize Speech Recognition client connected to Core WebSocket
  useEffect(() => {
    const voiceClient = new VoiceRecognitionClient(language);
    voiceClient.connectWebSocket("ws://localhost:8000/ws");
    recognitionRef.current = voiceClient;

    return () => {
      voiceClient.stop();
    };
  }, []);

  // Update speech recognition language when user switches between English, Hindi, and Marathi
  useEffect(() => {
    if (recognitionRef.current) {
      recognitionRef.current.setLanguage(language);
    }
  }, [language]);

  // Poll Core API health status
  useEffect(() => {
    const checkHealth = () => {
      fetch("http://localhost:8000/health")
        .then((res) => res.json())
        .then((data) => setCoreStatus(data.status === "healthy" ? "CONNECTED" : "UNAVAILABLE"))
        .catch(() => setCoreStatus("DISCONNECTED"));
    };
    checkHealth();
    const interval = setInterval(checkHealth, 5000);
    return () => clearInterval(interval);
  }, []);

  const triggerSpokenResponse = (text: string) => {
    if (playbackRef.current) {
      playbackRef.current.speakBrowserSpeech(text, language, voiceGender, voiceSpeed, () => {
        setAppState("IDLE");
      });
    }
  };

  const emergencyStop = () => {
    if (playbackRef.current) {
      playbackRef.current.stopPlayback();
    }
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
    setIsMicActive(false);
    setAppState("IDLE");
    addTranscript({
      id: Date.now().toString(),
      sender: "nova",
      text: "[EMERGENCY STOP EXECUTED: All audio playback & tasks terminated]",
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    });
  };

  const startContinuousListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.start(
        (text, isFinal) => {
          if (isFinal) {
            addTranscript({
              id: Date.now().toString(),
              sender: "user",
              text: text,
              timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
              language: language,
            });
            setAppState("THINKING");

            // Forward intent to Autonomous Operator Engine for multi-step task execution
            fetch("http://localhost:8000/api/v1/operator/execute", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                user_prompt: text,
                platform: "windows",
                device_id: "local-desktop",
                language: language,
              }),
            })
              .then((r) => r.json())
              .then((res) => {
                const plan = res.plan;
                if (plan) {
                  setActivePlan(plan);
                  setAppState(plan.status === "AWAITING_APPROVAL" ? "IDLE" : "EXECUTING");
                } else {
                  setAppState("EXECUTING");
                }

                addTranscript({
                  id: (Date.now() + 1).toString(),
                  sender: "nova",
                  text: res.spoken_response,
                  timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
                });
                triggerSpokenResponse(res.spoken_response);

                // Automatically keep listening for follow-up instructions
                setTimeout(() => {
                  setAppState("LISTENING");
                }, 1800);
              })
              .catch((e) => {
                console.error("Failed to execute operator intent:", e);
                setAppState("IDLE");
              });
          }
        },
        (err) => {
          if (err === "not-allowed") {
            setAppState("ERROR");
            addTranscript({
              id: Date.now().toString(),
              sender: "nova",
              text: "Microphone permission was denied. Please allow microphone access in your browser.",
              timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
            });
          } else {
            // Transient timeout/silence: return to listening or idle gracefully
            setAppState("LISTENING");
          }
        }
      );
    }
  };

  const toggleMic = () => {
    if (isMicActive) {
      setIsMicActive(false);
      setAppState("IDLE");
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
    } else {
      setIsMicActive(true);
      setAppState("LISTENING");
      startContinuousListening();
    }
  };

  // State tester cycle for Phase 1 verification
  const cycleState = () => {
    const states: AppState[] = ["IDLE", "LISTENING", "THINKING", "EXECUTING", "SPEAKING", "ERROR"];
    const currentIndex = states.indexOf(appState);
    const nextState = states[(currentIndex + 1) % states.length];
    setAppState(nextState);
  };

  return (
    <main className="flex min-h-screen flex-col bg-nova-dark text-slate-100 p-4 md:p-8 relative overflow-hidden select-none">
      {/* Background Holographic Atmosphere */}
      <div className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[700px] bg-cyan-600/10 rounded-full blur-[140px] pointer-events-none" />
      <div className="absolute bottom-0 right-10 w-[400px] h-[400px] bg-purple-600/10 rounded-full blur-[120px] pointer-events-none" />

      {/* Top Header Status Bar */}
      <header className="z-10 w-full max-w-7xl mx-auto flex items-center justify-between font-mono pb-6">
        <div className="flex items-center gap-3">
          <span className="relative flex h-3 w-3">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75" />
            <span className="relative inline-flex rounded-full h-3 w-3 bg-cyan-500 shadow-[0_0_12px_#00f0ff]" />
          </span>
          <span className="font-extrabold tracking-widest text-lg text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400">
            PROJECT NOVA
          </span>
          <span className="hidden sm:inline-block text-[11px] font-mono px-2 py-0.5 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-300">
            v0.1.0-alpha
          </span>
        </div>

        <div className="flex items-center gap-3">
          {/* Core Hub Status indicator */}
          <div className="flex items-center gap-2 bg-slate-900/60 border border-slate-800 backdrop-blur px-3 py-1.5 rounded-full text-xs">
            <Cpu className="w-3.5 h-3.5 text-slate-400" />
            <span className="text-slate-400">CORE HUB:</span>
            <span
              className={`font-semibold ${
                coreStatus === "CONNECTED" ? "text-emerald-400" : "text-amber-400"
              }`}
            >
              {coreStatus}
            </span>
          </div>

          {/* Universal Application Center Button */}
          <button
            onClick={() => setIsAppCenterOpen(true)}
            className="p-2 rounded-xl bg-slate-900/60 border border-slate-800 hover:border-slate-700 text-slate-300 hover:text-cyan-300 transition"
            title="Universal Application Center"
          >
            <Grid className="w-4 h-4 text-cyan-400" />
          </button>

          {/* Memory Inspector Button */}
          <button
            onClick={() => setIsMemoryOpen(true)}
            className="p-2 rounded-xl bg-slate-900/60 border border-slate-800 hover:border-slate-700 text-slate-300 hover:text-purple-300 transition"
            title="User-Approved Memory Inspector"
          >
            <Brain className="w-4 h-4 text-purple-400" />
          </button>

          {/* Settings Trigger */}
          <button
            onClick={() => setIsSettingsOpen(true)}
            className="p-2 rounded-xl bg-slate-900/60 border border-slate-800 hover:border-slate-700 text-slate-300 hover:text-white transition"
            title="Assistant Preferences"
          >
            <Settings className="w-4 h-4" />
          </button>
        </div>
      </header>

      {/* Main Multi-Panel Dashboard Layout: Responsive Grid & Mobile Tabs */}
      <div className="z-10 w-full max-w-7xl mx-auto flex-1 flex flex-col justify-between">
        {/* Mobile Navigation Bar */}
        <div className="flex lg:hidden items-center justify-around bg-slate-900/90 border border-slate-800 rounded-2xl p-1.5 mb-4 backdrop-blur shadow-lg">
          <button
            onClick={() => setMobileTab("assistant")}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-mono transition ${
              mobileTab === "assistant"
                ? "bg-cyan-500/20 text-cyan-300 font-bold border border-cyan-500/40"
                : "text-slate-400"
            }`}
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Assistant</span>
          </button>
          <button
            onClick={() => setMobileTab("transcripts")}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-mono transition ${
              mobileTab === "transcripts"
                ? "bg-cyan-500/20 text-cyan-300 font-bold border border-cyan-500/40"
                : "text-slate-400"
            }`}
          >
            <MessageSquare className="w-3.5 h-3.5" />
            <span>Chat</span>
          </button>
          <button
            onClick={() => setMobileTab("tasks")}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-mono transition ${
              mobileTab === "tasks"
                ? "bg-cyan-500/20 text-cyan-300 font-bold border border-cyan-500/40"
                : "text-slate-400"
            }`}
          >
            <ListOrdered className="w-3.5 h-3.5" />
            <span>Tasks</span>
          </button>
          <button
            onClick={() => setMobileTab("devices")}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-mono transition ${
              mobileTab === "devices"
                ? "bg-cyan-500/20 text-cyan-300 font-bold border border-cyan-500/40"
                : "text-slate-400"
            }`}
          >
            <Laptop className="w-3.5 h-3.5" />
            <span>Mesh</span>
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 my-auto">
          {/* Left Side: Device & Tasks (always visible on desktop, tabbed on mobile) */}
          <section
            className={`lg:col-span-3 flex-col gap-4 ${
              mobileTab === "devices" || mobileTab === "tasks" ? "flex" : "hidden lg:flex"
            }`}
          >
            <div className={mobileTab === "tasks" ? "hidden lg:block" : "block"}>
              <DevicePanel devices={devices} />
            </div>

            <div className={mobileTab === "devices" ? "hidden lg:block" : "block"}>
              <TaskExecutionWidget
                currentPlan={activePlan}
                onApproveTier2Plan={(planId) => {
                  if (activePlan) {
                    setAppState("EXECUTING");
                    fetch("http://localhost:8000/api/v1/operator/plan/approve", {
                      method: "POST",
                      headers: { "Content-Type": "application/json" },
                      body: JSON.stringify({
                        user_prompt: activePlan.user_prompt,
                        platform: "windows",
                        device_id: "local-desktop",
                        is_confirmed: true,
                      }),
                    })
                      .then((r) => r.json())
                      .then((res) => {
                        if (res.plan) {
                          setActivePlan(res.plan);
                        }
                        addTranscript({
                          id: Date.now().toString(),
                          sender: "nova",
                          text: res.spoken_response,
                          timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
                        });
                        triggerSpokenResponse(res.spoken_response);
                        setAppState("IDLE");
                      })
                      .catch(() => setAppState("IDLE"));
                  }
                }}
                onCancelPlan={() => {
                  setActivePlan(null);
                  setAppState("IDLE");
                }}
                onPlanUpdate={(updater) => {
                  if (activePlan) {
                    setActivePlan(updater(activePlan));
                  }
                }}
              />
            </div>

            {/* Application State Preview Controller */}
            <div className="bg-slate-900/50 backdrop-blur-md border border-slate-800 rounded-2xl p-4 shadow-xl">
              <div className="flex items-center justify-between pb-2 border-b border-slate-800 text-xs font-mono text-slate-400 mb-3">
                <span>STATE CONTROLLER</span>
                <button
                  onClick={cycleState}
                  className="text-[10px] text-cyan-400 hover:text-cyan-300 font-bold px-2 py-0.5 rounded bg-cyan-500/10 border border-cyan-500/20"
                >
                  CYCLE STATE
                </button>
              </div>
              <div className="grid grid-cols-3 gap-1.5 text-[11px] font-mono">
                {(["IDLE", "LISTENING", "THINKING", "EXECUTING", "SPEAKING", "ERROR"] as AppState[]).map(
                  (s) => (
                    <button
                      key={s}
                      onClick={() => setAppState(s)}
                      className={`py-1.5 px-1 rounded-lg border text-center transition ${
                        appState === s
                          ? "border-cyan-400 bg-cyan-500/20 text-cyan-300 font-bold shadow-[0_0_10px_rgba(0,240,255,0.2)]"
                          : "border-slate-800/80 bg-slate-950/40 text-slate-400 hover:text-slate-200"
                      }`}
                    >
                      {s}
                    </button>
                  )
                )}
              </div>
            </div>
          </section>

          {/* Center: NOVA Orb & Real-time Waveform Interaction */}
          <section
            className={`lg:col-span-5 flex-col items-center justify-center p-2 sm:p-4 ${
              mobileTab === "assistant" ? "flex" : "hidden lg:flex"
            }`}
          >
            <NovaOrb state={appState} audioVolume={audioVolume} onClick={toggleMic} />

            {/* Real Audio Waveform Visualizer */}
            <div className="mt-6 sm:mt-8 w-full max-w-sm flex flex-col items-center gap-4">
              <AudioWaveform isRecording={isMicActive} onVolumeChange={setAudioVolume} />

              {/* Action Microphone & Emergency Stop Controls */}
              <div className="flex items-center gap-3">
                <button
                  onClick={toggleMic}
                  className={`flex items-center gap-2.5 px-6 py-3 rounded-full font-mono text-xs font-bold transition-all shadow-lg active:scale-95 ${
                    isMicActive
                      ? "bg-rose-500 hover:bg-rose-600 text-white shadow-[0_0_20px_rgba(244,63,94,0.4)] animate-pulse"
                      : "bg-cyan-500 hover:bg-cyan-400 text-slate-950 shadow-[0_0_20px_rgba(0,240,255,0.3)]"
                  }`}
                >
                  {isMicActive ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
                  <span>{isMicActive ? "STOP LISTENING" : "START LISTENING"}</span>
                </button>

                <button
                  onClick={emergencyStop}
                  className="flex items-center gap-2 px-4 py-3 rounded-full font-mono text-xs font-bold bg-slate-900 border border-red-500/50 hover:bg-red-500/20 text-red-400 hover:text-red-300 transition shadow-lg active:scale-95"
                  title="Barge-in / Cancel all playback immediately"
                >
                  <Square className="w-3.5 h-3.5 fill-current" />
                  <span>STOP</span>
                </button>
              </div>
            </div>
          </section>

          {/* Right Side: Conversation Transcript & Task Feed */}
          <section
            className={`lg:col-span-4 flex-col h-[460px] sm:h-[520px] ${
              mobileTab === "transcripts" ? "flex" : "hidden lg:flex"
            }`}
          >
            <TranscriptPanel transcripts={transcripts} onClear={clearTranscripts} />
          </section>
        </div>
      </div>

      {/* Preferences Modal */}
      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        language={language}
        onLanguageChange={setLanguage}
        voiceGender={voiceGender}
        onVoiceGenderChange={setVoiceGender}
        voiceSpeed={voiceSpeed}
        onVoiceSpeedChange={setVoiceSpeed}
      />

      {/* User-Approved Memory Inspector Modal */}
      <MemoryManagerModal
        isOpen={isMemoryOpen}
        onClose={() => setIsMemoryOpen(false)}
        memories={memories}
        onAddMemory={addMemory}
        onDeleteMemory={deleteMemory}
      />

      {/* Universal Application Center Modal */}
      <ApplicationCenterModal
        isOpen={isAppCenterOpen}
        onClose={() => setIsAppCenterOpen(false)}
        onLaunchApp={(appName) => {
          fetch("http://localhost:8000/api/v1/operator/execute", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              user_prompt: `open ${appName}`,
              platform: "windows",
            }),
          });
        }}
      />
    </main>
  );
}
