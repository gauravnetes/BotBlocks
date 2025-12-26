export const API_URL = "http://127.0.0.1:8000";

export interface Bot {
  public_id: string;
  name: string;
  description?: string;
  system_prompt?: string;
  bot_type?: "rag" | "persona";
  platform?: string;
  created_at?: string;
  widget_config?: string;
  health_score?: number;
  last_health_check_at?: string;
}

export interface Asset {
  id: number;
  filename: string;
  file_type: string;
  file_size: number;
  cloudinary_url: string;
  uploaded_at: string;
}

export interface BotCreate {
  name: string;
  bot_type: "rag" | "persona";
  system_prompt?: string;
  platform?: string;
  platform_token?: string;
}

export async function getBots(): Promise<Bot[]> {
  const res = await fetch(`${API_URL}/api/v1/bots/`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch bots");
  return res.json();
}

export async function deleteBot(public_id: string): Promise<boolean> {
  const res = await fetch(`${API_URL}/api/v1/bots/${public_id}`, {
    method: "DELETE",
  });
  return res.ok;
}

export async function createBot(data: BotCreate): Promise<Bot> {
  const res = await fetch(`${API_URL}/api/v1/bots/create`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to create bot");
  return res.json();
}

export async function uploadFile(botId: string, file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_URL}/api/v1/bots/${botId}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) throw new Error("Failed to upload file");
  return res.json();
}

export async function getBot(public_id: string): Promise<Bot> {
  const res = await fetch(`${API_URL}/api/v1/bots/${public_id}`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch bot");
  return res.json();
}
export async function chatWithBot(botId: string, message: string): Promise<string> {
  const res = await fetch(`${API_URL}/api/v1/chat/web`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ bot_id: botId, message }),
  });
  if (!res.ok) throw new Error("Failed to chat");
  const data = await res.json();
  return data.response;
}

// Widget Configuration
export async function getWidgetConfig(public_id: string) {
  const res = await fetch(`${API_URL}/api/v1/bots/${public_id}/widget-config`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch widget config");
  return res.json();
}

export async function updateWidgetConfig(public_id: string, config: any) {
  const res = await fetch(`${API_URL}/api/v1/bots/${public_id}/widget-config`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(config),
  });
  if (!res.ok) throw new Error("Failed to update widget config");
  return res.json();
}


// ===== Knowledge Base =====

export async function getBotKnowledge(botId: string): Promise<{ files: Asset[] }> {
  const res = await fetch(`${API_URL}/api/v1/bots/${botId}/knowledge-base`, {
    cache: "no-store",
  });
  if (!res.ok) throw new Error("Failed to fetch knowledge base");
  return res.json();
}

export async function uploadBotKnowledge(botId: string, file: File) {
  const fd = new FormData();
  fd.append("file", file);

  const res = await fetch(
    `${API_URL}/api/v1/bots/${botId}/knowledge-base/upload`,
    {
      method: "POST",
      body: fd,
    }
  );

  if (!res.ok) throw new Error("Failed to upload knowledge");
  return res.json();
}

export async function deleteBotKnowledge(botId: string, filename: string) {
  const res = await fetch(
    `${API_URL}/api/v1/bots/${botId}/knowledge-base/${filename}`,
    { method: "DELETE" }
  );

  if (!res.ok) throw new Error("Failed to delete knowledge");
  return true;
}

// ===== Analytics =====
import { ComprehensiveAnalytics } from "./types/analytics";

export async function getComprehensiveAnalytics(botId: string): Promise<ComprehensiveAnalytics> {
  const res = await fetch(`${API_URL}/api/v1/bots/${botId}/analytics/comprehensive`, {
    cache: "no-store",
  });
  if (!res.ok) throw new Error("Failed to fetch analytics");
  return res.json();
}

export async function refreshAIInsights(botId: string): Promise<ComprehensiveAnalytics> {
  const res = await fetch(`${API_URL}/api/v1/bots/${botId}/analytics/refresh-insights`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });
  if (!res.ok) throw new Error("Failed to refresh insights");
  return res.json();
}

export async function getKnowledgeGapStats(botId: string, days: number = 7) {
  const res = await fetch(`${API_URL}/api/v1/bots/${botId}/analytics/gaps?days=${days}`, {
    cache: "no-store",
  });
  if (!res.ok) throw new Error("Failed to fetch gap stats");
  return res.json();
}

export async function resolveGap(botId: string, query: string, answer: string, logId?: number): Promise<{ status: string, new_health_score: number }> {
  const res = await fetch(`${API_URL}/api/v1/bots/${botId}/analytics/resolve-gap`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, answer, log_id: logId }),
  });

  if (!res.ok) throw new Error("Failed to resolve gap");
  return res.json();
}
