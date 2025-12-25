import { useEffect, useState } from "react";
import {
  getBotKnowledge,
  uploadBotKnowledge,
  deleteBotKnowledge,
} from "@/lib/api";

export function useKnowledgeBase(botId: string) {
  const [files, setFiles] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchFiles = async () => {
    const data = await getBotKnowledge(botId);
    setFiles(data.files || []);
  };

  const uploadFile = async (file: File) => {
    setLoading(true);
    await uploadBotKnowledge(botId, file);
    await fetchFiles();
    setLoading(false);
  };

  const removeFile = async (filename: string) => {
    await deleteBotKnowledge(botId, filename);
    setFiles((prev) => prev.filter((f) => f !== filename));
  };

  useEffect(() => {
    fetchFiles();
  }, [botId]);

  return { files, uploadFile, removeFile, loading };
}
