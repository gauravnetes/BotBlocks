"use client";

import { useEffect, useState } from "react";
import { Copy, Loader2 } from "lucide-react";
import { useParams } from "next/navigation";
import { toast } from "sonner";
import { getBot, getWidgetConfig } from "@/lib/api";
import { useAuth } from "@clerk/nextjs";

export default function EmbedPage() {
    const params = useParams();
    const botId = params.id as string;
    const { getToken } = useAuth();
    const [config, setConfig] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchConfig = async () => {
            try {
                const data = await getWidgetConfig(botId);
                setConfig(data);
            } catch (err) {
                console.error("Failed to fetch bot config", err);
            } finally {
                setIsLoading(false);
            }
        };
        fetchConfig();
    }, [botId]);

    const copyToClipboard = (text: string) => {
        navigator.clipboard.writeText(text);
        toast.success("Copied to clipboard!");
    };

    if (isLoading) {
        return (
            <div className="flex flex-col items-center justify-center min-h-[400px] text-zinc-500">
                <Loader2 className="w-8 h-8 animate-spin mb-4" />
                <p>Loading bot configuration...</p>
            </div>
        );
    }

    const position = config?.position || 'bottom-right';
    const isLeft = position === 'bottom-left';

    return (
        <div className="space-y-6 max-w-4xl">
            {/* Test Widget Link */}
            <div className="bg-blue-500/10 border border-blue-500/20 rounded-xl p-6">
                <h3 className="text-blue-400 font-bold mb-2">🧪 Test Your Widget</h3>
                <p className="text-zinc-400 text-sm mb-4">
                    Open the widget in a new tab to test it before embedding.
                </p>
                <a
                    href={`http://localhost:3000/widget/${botId}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-500 transition-colors"
                >
                    Open Widget Preview →
                </a>
            </div>

            {/* iframe Embed */}
            <div className="bg-zinc-900 border border-white/5 rounded-xl p-6">
                <h3 className="text-white font-bold mb-2">📦 iframe Embed (Recommended)</h3>
                <p className="text-zinc-400 text-sm mb-4">
                    Embed the widget directly as an iframe. Best for simple integration.
                </p>
                <div className="relative group">
                    <pre className="bg-black/50 p-4 rounded-lg text-sm text-zinc-300 overflow-x-auto font-mono">
                        {`<iframe 
  src="http://localhost:3000/widget/${botId}"
  style="position: fixed; bottom: 20px; ${isLeft ? 'left' : 'right'}: 20px; width: 420px; height: 700px; border: none; z-index: 9999;"
  title="Chat Widget"
></iframe>`}
                    </pre>
                    <button
                        onClick={() => copyToClipboard(`<iframe src="http://localhost:3000/widget/${botId}" style="position: fixed; bottom: 20px; ${isLeft ? 'left' : 'right'}: 20px; width: 420px; height: 700px; border: none; z-index: 9999;" title="Chat Widget"></iframe>`)}
                        className="absolute top-2 right-2 bg-white/10 p-2 rounded hover:bg-white/20 text-white opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                        <Copy className="w-4 h-4" />
                    </button>
                </div>
            </div>

            {/* Lightweight Script Embed */}
            <div className="bg-zinc-900 border border-white/5 rounded-xl p-6">
                <h3 className="text-white font-bold mb-2">⚡ Smart Script Embed</h3>
                <p className="text-zinc-400 text-sm mb-4">
                    Auto-injects the widget and handles resizing automatically. Best user experience.
                </p>
                <div className="relative group">
                    <pre className="bg-black/50 p-4 rounded-lg text-sm text-zinc-300 overflow-x-auto font-mono scrollbar-thin scrollbar-thumb-zinc-700 scrollbar-track-transparent">
                        {`<script>
  (function() {
    const iframe = document.createElement('iframe');
    const botId = '${botId}';
    iframe.src = 'http://localhost:3000/widget/' + botId;
    iframe.style.cssText = 'position:fixed;bottom:0;${isLeft ? 'left' : 'right'}:0;width:120px;height:120px;border:none;z-index:9999;transition:all 0.3s ease;color-scheme:none;background:transparent;pointer-events:none;';
    iframe.title = 'Chat Widget';
    document.body.appendChild(iframe);

    // Dynamic Resizing & Positioning
    window.addEventListener('message', function(e) {
      if (e.data && e.data.type === 'BOTBLOCKS_RESIZE') {
        iframe.style.width = e.data.width;
        iframe.style.height = e.data.height;
        iframe.style.pointerEvents = 'auto'; 
        
        // Handle horizontal positioning (Left vs Right)
        if (e.data.position === 'bottom-left') {
          iframe.style.left = '0';
          iframe.style.right = 'auto';
        } else {
          iframe.style.right = '0';
          iframe.style.left = 'auto';
        }
      }
    });
  })();
</script>`}
                    </pre>
                    <button
                        onClick={() => {
                            const code = `<script>(function(){const iframe=document.createElement('iframe');const botId='${botId}';iframe.src='http://localhost:3000/widget/'+botId;iframe.style.cssText='position:fixed;bottom:0;${isLeft ? 'left' : 'right'}:0;width:120px;height:120px;border:none;z-index:9999;transition:all 0.3s ease;color-scheme:none;background:transparent;';iframe.title='Chat Widget';document.body.appendChild(iframe);window.addEventListener('message',function(e){if(e.data&&e.data.type==='BOTBLOCKS_RESIZE'){iframe.style.width=e.data.width;iframe.style.height=e.data.height;if(e.data.position==='bottom-left'){iframe.style.left='0';iframe.style.right='auto';}else{iframe.style.right='0';iframe.style.left='auto';}}});})();</script>`;
                            copyToClipboard(code);
                        }}
                        className="absolute top-2 right-2 bg-white/10 p-2 rounded-lg hover:bg-white/20 text-white opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                        <Copy className="w-4 h-4" />
                    </button>
                </div>
            </div>
        </div>
    );
}
