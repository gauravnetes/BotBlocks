import { useEffect, useState } from "react";
import { Asset, getBotKnowledge, uploadBotKnowledge, deleteBotKnowledge } from "@/lib/api";
import { useAuth } from "@clerk/nextjs";

export function useKnowledgeBase(botId: string) {
  const [files, setFiles] = useState<Asset[]>([]);
  const [loading, setLoading] = useState(false);
  const { getToken } = useAuth();

  const fetchFiles = async () => {
    try {
      const token = await getToken();
      const data = await getBotKnowledge(botId, token);
      setFiles(data.files || []);
    } catch (e) {
      console.error("Failed to fetch files", e);
    }
  };

  const uploadFile = async (file: File) => {
    setLoading(true);
    try {
      const token = await getToken();
      await uploadBotKnowledge(botId, file, token);
      await fetchFiles();
    } catch (e) {
      console.error("Failed to upload file", e);
    } finally {
      setLoading(false);
    }
  };

  const removeFile = async (filename: string) => {
    try {
      const token = await getToken();
      await deleteBotKnowledge(botId, filename, token);
      setFiles((prev) => prev.filter((f) => f.filename !== filename));
    } catch (e) {
      console.error("Failed to remove file", e);
    }
  };

  useEffect(() => {
    fetchFiles();
  }, [botId]);

  return { files, uploadFile, removeFile, loading };
}
