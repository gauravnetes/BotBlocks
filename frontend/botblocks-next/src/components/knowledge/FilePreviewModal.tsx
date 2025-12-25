import { X, ExternalLink, Download } from "lucide-react";

interface FilePreviewModalProps {
    url: string;
    filename: string;
    onClose: () => void;
    onDownload: () => void;
}

export function FilePreviewModal({ url, filename, onClose, onDownload }: FilePreviewModalProps) {
    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-200">
            <div className="bg-zinc-900 border border-white/10 w-full max-w-5xl h-[85vh] rounded-2xl flex flex-col shadow-2xl relative">

                {/* Header */}
                <div className="flex items-center justify-between p-4 border-b border-white/10 bg-zinc-900 rounded-t-2xl">
                    <h3 className="text-white font-medium flex items-center gap-2">
                        <span className="opacity-70">Previewing:</span> {filename}
                    </h3>
                    <div className="flex items-center gap-2">
                        <button
                            onClick={onDownload}
                            className="p-2 text-zinc-400 hover:text-white hover:bg-white/10 rounded-lg transition-colors flex items-center gap-2 text-sm"
                            title="Download File"
                        >
                            <Download className="w-4 h-4" />
                            <span className="hidden sm:inline">Download</span>
                        </button>
                        <a
                            href={url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="p-2 text-zinc-400 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
                            title="Open in New Tab"
                        >
                            <ExternalLink className="w-4 h-4" />
                        </a>
                        <button
                            onClick={onClose}
                            className="p-2 text-zinc-400 hover:text-red-400 hover:bg-red-400/10 rounded-lg transition-colors"
                            title="Close Preview"
                        >
                            <X className="w-5 h-5" />
                        </button>
                    </div>
                </div>

                {/* Content */}
                <div className="flex-1 bg-zinc-950 relative overflow-hidden">
                    <iframe
                        src={url}
                        className="w-full h-full border-none"
                        title={`Preview of ${filename}`}
                    />
                </div>
            </div>
        </div>
    );
}
