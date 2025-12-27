"use client";

import { useKnowledgeBase } from "@/hooks/useKnowledgeBase";
import { useParams } from "next/navigation";
import { UploadBox } from "@/components/knowledge/UploadBox";
import { KnowledgeList } from "@/components/knowledge/KnowledgeList";

export default function KnowledgePage() {
    const params = useParams();
    const id = params?.id as string;
    const { files, uploadFile, removeFile, loading } = useKnowledgeBase(id);

    return (
        <div className="max-w-3xl space-y-8">
            <div>
                <h2 className="text-xl font-semibold text-white mb-2">Knowledge Base</h2>
                <p className="text-zinc-400 text-sm">
                    Upload documents to train your bot. It will use this knowledge to answer questions.
                </p>
            </div>

            <UploadBox onUpload={uploadFile} loading={loading} />

            <div className="space-y-4">
                <h3 className="text-sm font-medium text-zinc-300 uppercase tracking-wider">
                    Uploaded Files ({files.length})
                </h3>
                <KnowledgeList files={files} onDelete={removeFile} botId={id} loading={loading} />
            </div>
        </div>
    );
}
