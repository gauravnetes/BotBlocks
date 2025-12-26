import { FileText, Trash2, Eye, DownloadCloud, Globe } from "lucide-react";
import { API_URL, Asset } from "@/lib/api";
import { useState } from "react";
import { FilePreviewModal } from "./FilePreviewModal";

interface KnowledgeListProps {
    files: Asset[];
    onDelete: (filename: string) => void;
    botId: string;
}

export function KnowledgeList({ files, onDelete, botId }: KnowledgeListProps) {
    const [previewFile, setPreviewFile] = useState<string | null>(null);

    const getDownloadUrl = (filename: string, inline = false) =>
        `${API_URL}/api/v1/bots/${botId}/files/${filename}/download${inline ? "?inline=true" : ""}`;

    if (files.length === 0) {
        return (
            <div className="text-center py-12 border border-zinc-800 rounded-xl bg-zinc-900/50">
                <div className="bg-zinc-800/50 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3">
                    <FileText className="w-5 h-5 text-zinc-600" />
                </div>
                <p className="text-zinc-400 font-medium text-sm">No knowledge connected</p>
                <p className="text-zinc-600 text-xs mt-1">Upload documents to train your bot</p>
            </div>
        );
    }

    return (
        <>
            <div className="space-y-3">
                {files.map((file) => {
                    const isWeb = file.file_type === "web" || file.type === "web";
                    return (
                        <div
                            key={file.id}
                            className="group flex items-center justify-between p-4 bg-zinc-900 border border-zinc-800 rounded-lg hover:border-zinc-700 transition-colors"
                        >
                            <div className="flex items-center gap-3">
                                <div className={`p-2 rounded-lg ${isWeb ? "bg-purple-500/10" : "bg-blue-500/10"}`}>
                                    {isWeb ? (
                                        <Globe className="w-4 h-4 text-purple-400" />
                                    ) : (
                                        <FileText className="w-4 h-4 text-blue-400" />
                                    )}
                                </div>
                                <div className="max-w-[200px] sm:max-w-md overflow-hidden">
                                    <p className="text-sm font-medium text-white truncate" title={file.filename}>
                                        {file.filename}
                                    </p>
                                    <div className="flex items-center gap-2 text-xs text-zinc-500">
                                        {!isWeb && <span>{(file.file_size / 1024).toFixed(1)} KB</span>}
                                        {!isWeb && <span>•</span>}
                                        {isWeb ? (
                                            <a href={file.cloudinary_url} target="_blank" rel="noopener noreferrer" className="hover:text-blue-400 truncate max-w-[200px] block">
                                                {file.cloudinary_url}
                                            </a>
                                        ) : (
                                            <span>{new Date(file.uploaded_at).toLocaleDateString()}</span>
                                        )}
                                    </div>
                                </div>
                            </div>

                            <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-all">
                                {!isWeb && (
                                    <>
                                        {/* Preview Button */}
                                        <button
                                            onClick={() => setPreviewFile(file.filename)}
                                            className="p-2 text-zinc-500 hover:text-blue-400 hover:bg-blue-400/10 rounded-lg transition-all"
                                            title="Preview file"
                                        >
                                            <Eye className="w-4 h-4" />
                                        </button>

                                        {/* Download Button */}
                                        <a
                                            href={getDownloadUrl(file.filename)}
                                            className="p-2 text-zinc-500 hover:text-green-400 hover:bg-green-400/10 rounded-lg transition-all"
                                            title="Download file"
                                        >
                                            <DownloadCloud className="w-4 h-4" />
                                        </a>
                                    </>
                                )}

                                {/* Delete Button - Only for files for now until bulk delete is implemented */}
                                {!isWeb && (
                                    <button
                                        onClick={() => {
                                            if (window.confirm("Are you sure you want to delete this knowledge? The bot will forget this content immediately.")) {
                                                onDelete(file.filename);
                                            }
                                        }}
                                        className="p-2 text-zinc-500 hover:text-red-400 hover:bg-red-400/10 rounded-lg transition-all"
                                        title="Delete"
                                    >
                                        <Trash2 className="w-4 h-4" />
                                    </button>
                                )}
                            </div>
                        </div>
                    );
                })}
            </div>

            {/* Preview Modal */}
            {previewFile && (
                <FilePreviewModal
                    url={getDownloadUrl(previewFile, true)}
                    filename={previewFile}
                    onClose={() => setPreviewFile(null)}
                    onDownload={() => window.open(getDownloadUrl(previewFile), '_blank')}
                />
            )}
        </>
    );
}
