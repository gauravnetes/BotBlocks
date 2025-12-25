import { UploadCloud, Loader2 } from "lucide-react";

interface UploadBoxProps {
    onUpload: (file: File) => Promise<void>;
    loading: boolean;
}

export function UploadBox({ onUpload, loading }: UploadBoxProps) {
    const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            await onUpload(e.target.files[0]);
            e.target.value = ""; // Reset input
        }
    };

    return (
        <div className="relative group">
            <div className={`
        border-2 border-dashed border-zinc-700 
        rounded-xl p-8 
        flex flex-col items-center justify-center 
        gap-3 transition-all duration-200
        ${loading ? "bg-zinc-800/50" : "hover:border-blue-500 hover:bg-zinc-800/50 cursor-pointer"}
      `}>
                <input
                    type="file"
                    accept=".pdf,.txt"
                    onChange={handleFileChange}
                    disabled={loading}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer disabled:cursor-not-allowed"
                />

                <div className={`
          p-3 rounded-full 
          ${loading ? "bg-blue-500/20 text-blue-400" : "bg-zinc-800 text-zinc-400 group-hover:text-blue-500 group-hover:bg-blue-500/10"}
          transition-colors
        `}>
                    {loading ? (
                        <Loader2 className="w-6 h-6 animate-spin" />
                    ) : (
                        <UploadCloud className="w-6 h-6" />
                    )}
                </div>

                <div className="text-center">
                    <p className="text-sm font-medium text-white mb-1">
                        {loading ? "Training bot brain..." : "Click to upload or drag and drop"}
                    </p>
                    <p className="text-xs text-zinc-500">
                        Support for .pdf and .txt files
                    </p>
                </div>
            </div>
        </div>
    );
}
