
export default function TrainingPage() {
    return (
        <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="border-b border-white/5 pb-8">
                <span className="text-indigo-400 font-bold tracking-wider text-xs uppercase mb-2 block">Guides</span>
                <h1 className="text-3xl md:text-4xl font-black mb-4 tracking-tight">Training Your AI (RAG)</h1>
                <p className="text-lg text-zinc-400 leading-relaxed">
                    Understand how BotBlocks processes your data and how to optimize your content for the best answers.
                </p>
            </div>

            <div className="prose prose-invert prose-zinc max-w-none">

                <h3>How it Works</h3>
                <p>
                    BotBlocks uses a technique called <strong>Retrieval-Augmented Generation (RAG)</strong>. When a user asks a question, we don't just rely on the AI's general training. instead:
                </p>
                <ol className="list-decimal pl-5 space-y-2">
                    <li>We search your uploaded <strong>Knowledge Base</strong> for relevant snippets.</li>
                    <li>We retrieve the most similar text chunks based on the user's intent.</li>
                    <li>We feed these chunks to the LLM (Large Language Model) as "context".</li>
                    <li>The AI generates an accurate answer using <em>only</em> that context.</li>
                </ol>

                <h3>Supported Data Sources</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 not-prose my-6">
                    <div className="bg-zinc-900 border border-white/10 p-4 rounded-lg">
                        <h4 className="font-bold text-white mb-2">📄 Text & PDFs</h4>
                        <p className="text-sm text-zinc-400">Upload product manuals, employee handbooks, or support scripts. Text is extracted and chunked automatically.</p>
                    </div>
                    <div className="bg-zinc-900 border border-white/10 p-4 rounded-lg">
                        <h4 className="font-bold text-white mb-2">🌐 Website Crawling</h4>
                        <p className="text-sm text-zinc-400">Enter a starting URL (e.g., <code>docs.yoursite.com</code>). We will visit pages and index the text content.</p>
                    </div>
                </div>

                <h3>Best Practices</h3>
                <ul>
                    <li><strong>Keep it clear:</strong> The AI works best with unstructured but clear text. Bullet points and headings help.</li>
                    <li><strong>Small chunks:</strong> If manually adding text, try to keep each "fact" or "topic" distinct.</li>
                    <li><strong>Refresh often:</strong> If your website changes, remember to re-crawl or update the documents in BotBlocks.</li>
                </ul>

            </div>
        </div>
    );
}
