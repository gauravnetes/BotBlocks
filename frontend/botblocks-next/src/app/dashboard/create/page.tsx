"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { createBot, uploadFile } from "@/lib/api";
import { ArrowLeft, ArrowRight, Upload, Check, Bot as BotIcon, FileText, Globe, MessageCircle } from "lucide-react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";

export default function CreateBotWizard() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [isLoading, setIsLoading] = useState(false);

  // Form State
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [type, setType] = useState<"rag" | "persona">("rag");
  const [files, setFiles] = useState<File[]>([]);
  const [persona, setPersona] = useState("friendly");
  const [customPrompt, setCustomPrompt] = useState("");
  const [platform, setPlatform] = useState<"web" | "telegram" | "discord">("web");
  const [platformToken, setPlatformToken] = useState("");

  const handleCreate = async () => {
    setIsLoading(true);
    try {
      // 1. Determine System Prompt
      let systemPrompt = "You are a helpful assistant.";
      if (persona === "friendly") systemPrompt = "You are a friendly and helpful assistant. Use emojis!";
      if (persona === "professional") systemPrompt = "You are a professional business assistant. Be concise.";
      if (persona === "custom") systemPrompt = customPrompt;

      // 2. Create Bot
      const newBot = await createBot({
        name,
        system_prompt: systemPrompt,
        platform: platform,
        platform_token: platformToken,
      });

      // 3. Upload Files (if RAG)
      if (type === "rag" && files.length > 0) {
        for (const file of files) {
          await uploadFile(newBot.public_id, file);
        }
      }

      // 4. Redirect
      router.push("/dashboard");
      router.refresh();

    } catch (error) {
      alert("Failed to create bot. Check console.");
      console.error(error);
      setIsLoading(false);
    }
  };

  const nextStep = () => setStep(s => s + 1);
  const prevStep = () => setStep(s => s - 1);

  return (
    <div className="max-w-2xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <Link href="/dashboard" className="text-sm text-zinc-500 hover:text-white mb-4 inline-block">
          ← Back to Dashboard
        </Link>
        <h1 className="text-3xl font-bold text-white">Create New Bot</h1>
        <div className="flex gap-2 mt-4">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div
              key={i}
              className={`h-1 flex-1 rounded-full transition-colors duration-300 ${i <= step ? "bg-blue-500" : "bg-zinc-800"}`}
            />
          ))}
        </div>
      </div>

      <AnimatePresence mode="wait">
        <motion.div
          key={step}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -20 }}
          transition={{ duration: 0.2 }}
        >
          {/* Step 1: Basics */}
          {step === 1 && (
            <div className="space-y-6">
              <h2 className="text-xl font-bold text-white">Let&apos;s start with the basics</h2>
              <div>
                <label className="block text-sm font-medium text-zinc-400 mb-2">Bot Name</label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full bg-zinc-900 border border-white/10 rounded-lg p-3 text-white focus:outline-none focus:border-blue-500"
                  placeholder="e.g. Support Assistant"
                  autoFocus
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-zinc-400 mb-2">Description</label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="w-full bg-zinc-900 border border-white/10 rounded-lg p-3 text-white focus:outline-none focus:border-blue-500 h-32"
                  placeholder="What does this bot do?"
                />
              </div>
              <div className="flex justify-end">
                <button
                  onClick={nextStep}
                  disabled={!name}
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                >
                  Next <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}

          {/* Step 2: Type */}
          {step === 2 && (
            <div className="space-y-6">
              <h2 className="text-xl font-bold text-white">What kind of bot is this?</h2>
              <div className="grid grid-cols-2 gap-4">
                <button
                  onClick={() => setType("rag")}
                  className={`p-6 rounded-xl border text-left transition-all ${type === "rag" ? "bg-blue-600/10 border-blue-500" : "bg-zinc-900 border-white/10 hover:border-white/20"}`}
                >
                  <FileText className={`w-8 h-8 mb-4 ${type === "rag" ? "text-blue-500" : "text-zinc-400"}`} />
                  <h3 className="font-bold text-white mb-1">Knowledge Bot (RAG)</h3>
                  <p className="text-sm text-zinc-400">Answers based on uploaded documents.</p>
                </button>

                <button
                  onClick={() => setType("persona")}
                  className={`p-6 rounded-xl border text-left transition-all ${type === "persona" ? "bg-blue-600/10 border-blue-500" : "bg-zinc-900 border-white/10 hover:border-white/20"}`}
                >
                  <BotIcon className={`w-8 h-8 mb-4 ${type === "persona" ? "text-blue-500" : "text-zinc-400"}`} />
                  <h3 className="font-bold text-white mb-1">Persona Bot</h3>
                  <p className="text-sm text-zinc-400">Chat with a specific personality.</p>
                </button>
              </div>

              <div className="flex justify-between">
                <button onClick={prevStep} className="text-zinc-400 hover:text-white">Back</button>
                <button
                  onClick={nextStep}
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-500 flex items-center gap-2"
                >
                  Next <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}

          {/* Step 3: Knowledge / Persona */}
          {step === 3 && (
            <div className="space-y-6">
              {type === "rag" ? (
                <div>
                  <h2 className="text-xl font-bold text-white mb-4">Upload Knowledge</h2>
                  <div className="border-2 border-dashed border-white/10 rounded-xl p-8 text-center hover:border-blue-500/50 transition-colors">
                    <Upload className="w-10 h-10 text-zinc-500 mx-auto mb-4" />
                    <p className="text-zinc-400 mb-4">Drag and drop PDF or TXT files here</p>
                    <input
                      type="file"
                      multiple
                      accept=".pdf,.txt"
                      onChange={(e) => setFiles(Array.from(e.target.files || []))}
                      className="block w-full text-sm text-zinc-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-500"
                    />
                  </div>
                  {files.length > 0 && (
                    <div className="mt-4 space-y-2">
                      {files.map((f, i) => (
                        <div key={i} className="flex items-center gap-2 text-sm text-zinc-300 bg-white/5 p-2 rounded">
                          <FileText className="w-4 h-4" /> {f.name}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ) : (
                <div>
                  <h2 className="text-xl font-bold text-white mb-4">Choose Personality</h2>
                  <div className="space-y-3">
                    {["friendly", "professional", "custom"].map((p) => (
                      <label key={p} className="flex items-center gap-3 p-4 rounded-lg border border-white/10 bg-zinc-900 cursor-pointer hover:border-white/20">
                        <input
                          type="radio"
                          name="persona"
                          value={p}
                          checked={persona === p}
                          onChange={(e) => setPersona(e.target.value)}
                          className="text-blue-600 focus:ring-blue-500"
                        />
                        <span className="capitalize text-white">{p}</span>
                      </label>
                    ))}
                  </div>
                  {persona === "custom" && (
                    <textarea
                      value={customPrompt}
                      onChange={(e) => setCustomPrompt(e.target.value)}
                      className="w-full mt-4 bg-zinc-900 border border-white/10 rounded-lg p-3 text-white h-32"
                      placeholder="Enter custom system prompt..."
                    />
                  )}
                </div>
              )}

              <div className="flex justify-between">
                <button onClick={prevStep} className="text-zinc-400 hover:text-white">Back</button>
                <button
                  onClick={nextStep}
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-500 flex items-center gap-2"
                >
                  Next <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}

          {/* Step 4: Platform */}
          {step === 4 && (
            <div className="space-y-6">
              <h2 className="text-xl font-bold text-white">Where will this bot live?</h2>
              <div className="grid grid-cols-3 gap-4">
                {[
                  { id: "web", label: "Website", icon: Globe },
                  { id: "telegram", label: "Telegram", icon: MessageCircle },
                  { id: "discord", label: "Discord", icon: MessageCircle },
                ].map((p) => (
                  <button
                    key={p.id}
                    onClick={() => setPlatform(p.id as any)}
                    className={`p-4 rounded-xl border text-center transition-all ${platform === p.id ? "bg-blue-600/10 border-blue-500" : "bg-zinc-900 border-white/10 hover:border-white/20"}`}
                  >
                    <p.icon className={`w-8 h-8 mx-auto mb-2 ${platform === p.id ? "text-blue-500" : "text-zinc-400"}`} />
                    <span className={`font-medium ${platform === p.id ? "text-white" : "text-zinc-400"}`}>{p.label}</span>
                  </button>
                ))}
              </div>
              <div className="flex justify-between">
                <button onClick={prevStep} className="text-zinc-400 hover:text-white">Back</button>
                <button onClick={nextStep} className="bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-500 flex items-center gap-2">
                  Next <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}

          {/* Step 5: Details */}
          {step === 5 && (
            <div className="space-y-6">
              <h2 className="text-xl font-bold text-white">Platform Details</h2>
              {platform === "web" ? (
                <div className="bg-blue-500/10 border border-blue-500/20 rounded-xl p-6 text-center">
                  <Globe className="w-12 h-12 text-blue-500 mx-auto mb-4" />
                  <h3 className="text-white font-bold mb-2">No Configuration Needed</h3>
                  <p className="text-zinc-400">You'll get an embed code after creating the bot.</p>
                </div>
              ) : (
                <div>
                  <label className="block text-sm font-medium text-zinc-400 mb-2">
                    {platform === "telegram" ? "Telegram Bot Token" : "Discord Bot Token"}
                  </label>
                  <input
                    type="password"
                    value={platformToken}
                    onChange={(e) => setPlatformToken(e.target.value)}
                    className="w-full bg-zinc-900 border border-white/10 rounded-lg p-3 text-white focus:outline-none focus:border-blue-500"
                    placeholder="Enter your bot token"
                  />
                  <p className="text-xs text-zinc-500 mt-2">
                    {platform === "telegram" ? "Get this from @BotFather" : "Get this from Discord Developer Portal"}
                  </p>
                </div>
              )}
              <div className="flex justify-between">
                <button onClick={prevStep} className="text-zinc-400 hover:text-white">Back</button>
                <button onClick={nextStep} className="bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-500 flex items-center gap-2">
                  Next <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}

          {/* Step 6: Review */}
          {step === 6 && (
            <div className="space-y-6">
              <h2 className="text-xl font-bold text-white mb-4">Review & Create</h2>

              <div className="bg-zinc-900 border border-white/10 rounded-xl p-6 space-y-4">
                <div className="flex justify-between">
                  <span className="text-zinc-400">Name</span>
                  <span className="text-white font-medium">{name}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-zinc-400">Type</span>
                  <span className="text-white font-medium uppercase">{type}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-zinc-400">Platform</span>
                  <span className="text-white font-medium uppercase">{platform}</span>
                </div>
                {type === "rag" && (
                  <div className="flex justify-between">
                    <span className="text-zinc-400">Files</span>
                    <span className="text-white font-medium">{files.length} selected</span>
                  </div>
                )}
                {type === "persona" && (
                  <div className="flex justify-between">
                    <span className="text-zinc-400">Persona</span>
                    <span className="text-white font-medium capitalize">{persona}</span>
                  </div>
                )}
              </div>

              <div className="flex justify-between">
                <button onClick={prevStep} className="text-zinc-400 hover:text-white">Back</button>
                <button
                  onClick={handleCreate}
                  disabled={isLoading}
                  className="bg-green-600 text-white px-8 py-3 rounded-lg font-bold hover:bg-green-500 flex items-center gap-2 disabled:opacity-50"
                >
                  {isLoading ? (
                    <>
                      <span className="animate-spin">⏳</span> Creating...
                    </>
                  ) : (
                    <>
                      Create Bot <Check className="w-4 h-4" />
                    </>
                  )}
                </button>
              </div>
            </div>
          )}
        </motion.div>
      </AnimatePresence>
    </div>
  );
}