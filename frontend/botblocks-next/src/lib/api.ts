export const API_URL = "http://127.0.0.1:8000";

export interface Bot {
  public_id: string;
  name: string;
  description?: string;
  system_prompt?: string;
  platform?: string;
  created_at?: string;
}

export interface BotCreate {
  name: string;
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
