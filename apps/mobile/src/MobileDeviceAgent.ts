/**
 * Project NOVA - Mobile Device Automation Agent
 * Native Intents (Android) & URL Schemes / App Intents (iOS)
 */

import { Platform } from "react-native";
import * as Linking from "expo-linking";
import * as Battery from "expo-battery";
import * as Notifications from "expo-notifications";

export interface MobileActionResult {
  success: boolean;
  message: string;
  data?: Record<string, unknown>;
  error?: string;
}

export class MobileDeviceAgent {
  /**
   * 1. Open installed application via Intent or URL Scheme
   */
  public static async openApp(appId: "whatsapp" | "youtube" | "maps" | "dialer", query?: string): Promise<MobileActionResult> {
    try {
      let targetUrl = "";
      if (appId === "whatsapp") {
        targetUrl = query ? `whatsapp://send?text=${encodeURIComponent(query)}` : "whatsapp://";
      } else if (appId === "youtube") {
        targetUrl = query ? `https://www.youtube.com/results?search_query=${encodeURIComponent(query)}` : "vnd.youtube://";
      } else if (appId === "maps") {
        targetUrl = Platform.OS === "ios" ? `maps://?q=${encodeURIComponent(query || "")}` : `geo:0,0?q=${encodeURIComponent(query || "")}`;
      } else if (appId === "dialer") {
        targetUrl = query ? `tel:${query}` : "tel:";
      }

      const supported = await Linking.canOpenURL(targetUrl);
      if (!supported && Platform.OS === "android") {
        // Fallback to web link
        await Linking.openURL(targetUrl);
        return { success: true, message: `Opened ${appId} via web intent fallback.` };
      }

      await Linking.openURL(targetUrl);
      return { success: true, message: `Successfully opened ${appId}.` };
    } catch (err: unknown) {
      return { success: false, message: `Failed to open ${appId}`, error: String(err) };
    }
  }

  /**
   * 2. Telemetry: Check real battery level (Tier 0 Safe)
   */
  public static async getBatteryTelemetry(): Promise<MobileActionResult> {
    try {
      const batteryLevel = await Battery.getBatteryLevelAsync();
      const batteryState = await Battery.getBatteryStateAsync();
      return {
        success: true,
        message: `Battery level is ${(batteryLevel * 100).toFixed(0)}%`,
        data: {
          level: batteryLevel,
          state: batteryState,
        },
      };
    } catch (err: unknown) {
      return { success: false, message: "Unable to read battery status", error: String(err) };
    }
  }

  /**
   * 3. Schedule Reminder / Notification (Tier 1 Reversible)
   */
  public static async scheduleReminder(title: string, body: string, triggerSeconds: number): Promise<MobileActionResult> {
    try {
      const id = await Notifications.scheduleNotificationAsync({
        content: { title, body, sound: true },
        trigger: { seconds: triggerSeconds },
      });
      return { success: true, message: `Reminder scheduled for ${triggerSeconds} seconds from now`, data: { notificationId: id } };
    } catch (err: unknown) {
      return { success: false, message: "Failed to schedule reminder", error: String(err) };
    }
  }
}

