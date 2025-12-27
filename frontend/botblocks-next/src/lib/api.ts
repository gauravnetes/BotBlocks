export const API_URL = "https://gauravnetes-botblocks-production.hf.space";

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
  id: number | string; // unified: number for files, URL string for web
  filename: string; // name or title
  type?: "file" | "web";
  file_type: string;
  file_size: number;
  cloudinary_url: string;
  uploaded_at: string;
  // Web specific (optional)
  url?: string;
  title?: string;
}

export interface BotCreate {
  name: string;
  bot_type: "rag" | "persona";
  system_prompt?: string;
  platform?: string;
  platform_token?: string;
}

export async function getBots(token?: string | null): Promise<Bot[]> {
  const headers: Record<string, string> = {};
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_URL}/api/v1/bots/`, {
    cache: "no-store",
    headers
  });
  if (!res.ok) throw new Error("Failed to fetch bots");
  return res.json();
}

export async function deleteBot(public_id: string, token?: string | null): Promise<boolean> {
  const headers: Record<string, string> = {};
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_URL}/api/v1/bots/${public_id}`, {
    method: "DELETE",
    headers
  });
  return res.ok;
}

export async function createBot(data: BotCreate, token?: string | null): Promise<Bot> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_URL}/api/v1/bots/create`, {
    method: "POST",
    headers,
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to create bot");
  return res.json();
}

export async function uploadFile(botId: string, file: File, token?: string | null) {
  const formData = new FormData();
  formData.append("file", file);

  const headers: Record<string, string> = {};
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_URL}/api/v1/bots/${botId}/upload`, {
    method: "POST",
    body: formData,
    headers
  });

  if (!res.ok) throw new Error("Failed to upload file");
  return res.json();
}

export async function getBot(public_id: string, token?: string | null): Promise<Bot> {
  const headers: Record<string, string> = {};
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_URL}/api/v1/bots/${public_id}`, {
    cache: "no-store",
    headers
  });
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

export async function updateWidgetConfig(public_id: string, config: any, token?: string | null) {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_URL}/api/v1/bots/${public_id}/widget-config`, {
    method: "PUT",
    headers,
    body: JSON.stringify(config),
  });
  if (!res.ok) throw new Error("Failed to update widget config");
  return res.json();
}


// ===== Knowledge Base =====

export async function getBotKnowledge(botId: string, token?: string | null): Promise<{ files: Asset[] }> {
  const headers: Record<string, string> = {};
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_URL}/api/v1/bots/${botId}/knowledge-base`, {
    cache: "no-store",
    headers
  });
  if (!res.ok) throw new Error("Failed to fetch knowledge base");
  return res.json();
}

export async function uploadBotKnowledge(botId: string, file: File, token?: string | null) {
  const fd = new FormData();
  fd.append("file", file);

  const headers: Record<string, string> = {};
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(
    `${API_URL}/api/v1/bots/${botId}/knowledge-base/upload`,
    {
      method: "POST",
      body: fd,
      headers
    }
  );

  if (!res.ok) throw new Error("Failed to upload knowledge");
  return res.json();
}

export async function deleteBotKnowledge(botId: string, filename: string, token?: string | null) {
  const headers: Record<string, string> = {};
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(
    `${API_URL}/api/v1/bots/${botId}/knowledge-base/${filename}`,
    {
      method: "DELETE",
      headers
    }
  );

  if (!res.ok) throw new Error("Failed to delete knowledge");
  return true;
}

// ===== Analytics =====
import { ComprehensiveAnalytics } from "./types/analytics";

export async function getComprehensiveAnalytics(botId: string, token?: string | null): Promise<ComprehensiveAnalytics> {
  const headers: Record<string, string> = {};
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_URL}/api/v1/bots/${botId}/analytics/comprehensive`, {
    cache: "no-store",
    headers
  });
  if (!res.ok) throw new Error("Failed to fetch analytics");
  return res.json();
}

export async function refreshAIInsights(botId: string, token?: string | null): Promise<ComprehensiveAnalytics> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_URL}/api/v1/bots/${botId}/analytics/refresh-insights`, {
    method: "POST",
    headers,
  });
  if (!res.ok) throw new Error("Failed to refresh insights");
  return res.json();
}

export async function getKnowledgeGapStats(botId: string, days: number = 7, token?: string | null) {
  const headers: Record<string, string> = {};
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_URL}/api/v1/bots/${botId}/analytics/gaps?days=${days}`, {
    cache: "no-store",
    headers,
  });
  if (!res.ok) throw new Error("Failed to fetch gap stats");
  return res.json();
}

export async function resolveGap(botId: string, query: string, answer: string, logId?: number, token?: string | null): Promise<{ status: string, new_health_score: number }> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_URL}/api/v1/bots/${botId}/analytics/resolve-gap`, {
    method: "POST",
    headers,
    body: JSON.stringify({ query, answer, log_id: logId }),
  });

  if (!res.ok) throw new Error("Failed to resolve gap");
  return res.json();
}

// ===== Web Scraping =====

export interface ScrapeResult {
  success: boolean;
  message?: string;
  url?: string;
  title?: string;
  content_length?: number;
  results?: {
    total_urls: number;
    successful: number;
    failed: number;
    pages: any[];
  }
}

export async function scrapeSingleUrl(botId: string, url: string, token?: string | null): Promise<ScrapeResult> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_URL}/api/v1/bots/${botId}/scrape/single`, {
    method: "POST",
    headers,
    body: JSON.stringify({ url }),
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: "Scraping failed" }));
    throw new Error(error.detail || "Scraping failed");
  }
  return res.json();
}

export async function scrapeWebsite(botId: string, startUrl: string, method: "sitemap" | "crawl" | "single" = "sitemap", token?: string | null): Promise<ScrapeResult> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_URL}/api/v1/bots/${botId}/scrape/website`, {
    method: "POST",
    headers,
    body: JSON.stringify({ start_url: startUrl, method, max_pages: 50, max_depth: 2 }),
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: "Scraping failed" }));
    throw new Error(error.detail || "Scraping failed");
  }
  return res.json();
}

export async function scrapeWebsiteAsync(botId: string, startUrl: string, method: "sitemap" | "crawl" | "single" = "sitemap", token?: string | null): Promise<ScrapeResult> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_URL}/api/v1/bots/${botId}/scrape/website/async`, {
    method: "POST",
    headers,
    body: JSON.stringify({ start_url: startUrl, method, max_pages: 100, max_depth: 3 }),
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: "Scraping failed" }));
    throw new Error(error.detail || "Scraping failed");
  }
  return res.json();
}

export async function previewWebsiteScraping(botId: string, url: string, token?: string | null) {
  const headers: Record<string, string> = {};
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_URL}/api/v1/bots/${botId}/scrape/preview?url=${encodeURIComponent(url)}`, {
    cache: "no-store",
    headers
  });

  if (!res.ok) throw new Error("Failed to preview");
  return res.json();
}
