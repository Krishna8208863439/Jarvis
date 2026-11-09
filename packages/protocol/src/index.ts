/**
 * Project NOVA - Shared Core Protocol Definitions
 * Cross-platform schemas for Hub-Device-Agent communications.
 */

export type AppState =
  | 'IDLE'
  | 'LISTENING'
  | 'THINKING'
  | 'EXECUTING'
  | 'SPEAKING'
  | 'ERROR';

export type LanguageCode = 'en' | 'hi' | 'mr';

export type VoiceGender = 'male' | 'female';

export type PlatformType = 'web' | 'desktop' | 'android' | 'ios' | 'linux' | 'macos' | 'windows';

export enum RiskTier {
  TIER_0_SAFE = 'TIER_0_SAFE',               // Read-only actions (search, weather, battery)
  TIER_1_REVERSIBLE = 'TIER_1_REVERSIBLE',   // Open apps, volume, reminders
  TIER_2_SENSITIVE = 'TIER_2_SENSITIVE',     // Send messages, emails, modify docs (requires confirmation)
  TIER_3_DANGEROUS = 'TIER_3_DANGEROUS',     // Delete files, sensitive commands, payment (UI confirmation + auth)
}

export interface DeviceInfo {
  deviceId: string;
  name: string;
  platform: PlatformType;
  osVersion: string;
  capabilities: string[];
  isOnline: boolean;
  lastSeenAt: string;
}

export interface UserVoiceSettings {
  gender: VoiceGender;
  language: LanguageCode;
  speed: number;    // 0.5 to 2.0
  volume: number;   // 0.0 to 1.0
  autoDetectLanguage: boolean;
}

export interface TaskStep {
  stepId: string;
  toolName: string;
  arguments: Record<string, unknown>;
  riskTier: RiskTier;
  status: 'PENDING' | 'CONFIRMING' | 'RUNNING' | 'COMPLETED' | 'FAILED' | 'CANCELLED';
  targetDeviceId?: string;
  result?: Record<string, unknown>;
  error?: string;
}

export interface TaskExecutionPlan {
  taskId: string;
  userId: string;
  userPrompt: string;
  steps: TaskStep[];
  currentStepIndex: number;
  status: 'PLANNING' | 'AWAITING_APPROVAL' | 'EXECUTING' | 'COMPLETED' | 'CANCELLED' | 'FAILED';
  createdAt: string;
  updatedAt: string;
}

export type WSMessageType =
  | 'CONNECT'
  | 'CONNECTED'
  | 'STATE_CHANGE'
  | 'AUDIO_STREAM_START'
  | 'AUDIO_CHUNK'
  | 'AUDIO_STREAM_END'
  | 'TRANSCRIPT_PARTIAL'
  | 'TRANSCRIPT_FINAL'
  | 'EMERGENCY_STOP'
  | 'TOOL_CALL_REQUEST'
  | 'TOOL_CALL_RESPONSE'
  | 'CONFIRMATION_REQUEST'
  | 'CONFIRMATION_RESPONSE'
  | 'HEARTBEAT';

export interface WSMessage<T = unknown> {
  id: string;
  type: WSMessageType;
  timestamp: string;
  sessionId?: string;
  deviceId?: string;
  payload: T;
}

