"use client";
import { useState, useEffect } from 'react';

interface WidgetConfig {
    theme: 'modern' | 'classic' | 'minimal';
    primary_color: string;
    avatar_url: string | null;
    welcome_message: string;
    bot_display_name: string | null;
    position: 'bottom-right' | 'bottom-left';
    button_style: 'circle' | 'rounded' | 'square';
}

interface WidgetCustomizerProps {
    botId: string;
    botName: string;
    initialConfig: WidgetConfig;
    onUpdate: (config: Partial<WidgetConfig>) => Promise<void>;
}

export function WidgetCustomizer({ botId, botName, initialConfig, onUpdate }: WidgetCustomizerProps) {
    const [config, setConfig] = useState<WidgetConfig>({
        ...initialConfig,
        bot_display_name: initialConfig.bot_display_name || botName
    });
    const [isSaving, setIsSaving] = useState(false);
    const [saveStatus, setSaveStatus] = useState<'idle' | 'success' | 'error'>('idle');

    const handleChange = (key: keyof WidgetConfig, value: any) => {
        setConfig(prev => ({ ...prev, [key]: value }));
    };

    const handleSave = async () => {
        setIsSaving(true);
        setSaveStatus('idle');

        try {
            await onUpdate(config);
            setSaveStatus('success');
            setTimeout(() => setSaveStatus('idle'), 3000);
        } catch (error) {
            setSaveStatus('error');
            setTimeout(() => setSaveStatus('idle'), 3000);
        } finally {
            setIsSaving(false);
        }
    };

    return (
        <div className="space-y-6">

            {/* THEME */}
            <div className="bg-zinc-900/60 border border-white/10 rounded-xl p-4">
                <label className="block text-xs font-semibold text-zinc-300 mb-3">
                    🎨 Widget Theme
                </label>

                <div className="grid grid-cols-3 gap-3">
                    {(['modern', 'classic', 'minimal'] as const).map((theme) => {
                        const active = config.theme === theme;
                        return (
                            <button
                                key={theme}
                                onClick={() => handleChange('theme', theme)}
                                className={`rounded-xl p-3 border transition-all
                ${active
                                        ? 'bg-blue-400/10 border-blue-400 ring-1 ring-blue-400/40'
                                        : 'bg-zinc-950 border-white/10 hover:border-white/20'
                                    }`}
                            >
                                <div className="text-center space-y-1">
                                    <div className="text-2xl">
                                        {theme === 'modern' ? '💎' : theme === 'classic' ? '📋' : '✨'}
                                    </div>
                                    <div className={`text-xs font-semibold capitalize ${active ? 'text-blue-300' : 'text-zinc-400'
                                        }`}>
                                        {theme}
                                    </div>
                                </div>
                            </button>
                        );
                    })}
                </div>
            </div>

            {/* PRIMARY COLOR */}
            <div className="bg-zinc-900/60 border border-white/10 rounded-xl p-4">
                <label className="block text-xs font-semibold text-zinc-300 mb-3">
                    🎯 Primary Accent Color
                </label>

                <div className="flex items-center gap-3">
                    <input
                        type="color"
                        value={config.primary_color}
                        onChange={(e) => handleChange('primary_color', e.target.value)}
                        className="w-12 h-10 rounded-lg cursor-pointer bg-transparent border border-white/10"
                    />
                    <input
                        type="text"
                        value={config.primary_color}
                        onChange={(e) => handleChange('primary_color', e.target.value)}
                        className="flex-1 bg-zinc-950 border border-white/10 rounded-lg px-3 py-2 text-white text-xs focus:outline-none focus:ring-1 focus:ring-blue-400/40"
                        placeholder="#FFD43B"
                    />
                </div>
            </div>

            {/* WELCOME MESSAGE */}
            <div className="bg-zinc-900/60 border border-white/10 rounded-xl p-4">
                <label className="block text-xs font-semibold text-zinc-300 mb-3">
                    👋 Welcome Message
                </label>

                <textarea
                    value={config.welcome_message}
                    onChange={(e) => handleChange('welcome_message', e.target.value)}
                    className="w-full bg-zinc-950 border border-white/10 rounded-lg p-3 text-white text-xs h-20 resize-none focus:outline-none focus:ring-1 focus:ring-blue-400/40"
                    placeholder="Hey! How can I help you today?"
                />
            </div>

            {/* DISPLAY NAME */}
            <div className="bg-zinc-900/60 border border-white/10 rounded-xl p-4">
                <label className="block text-xs font-semibold text-zinc-300 mb-2">
                    🏷 Bot Display Name
                </label>

                <input
                    type="text"
                    value={config.bot_display_name || ''}
                    onChange={(e) => handleChange('bot_display_name', e.target.value)}
                    className="w-full bg-zinc-950 border border-white/10 rounded-lg px-3 py-2 text-white text-xs focus:outline-none focus:ring-1 focus:ring-blue-400/40"
                    placeholder={botName}
                />
                <p className="text-[11px] text-zinc-500 mt-2">
                    Leave empty to use default name: <span className="text-zinc-300">{botName}</span>
                </p>
            </div>

            {/* POSITION */}
            <div className="bg-zinc-900/60 border border-white/10 rounded-xl p-4">
                <label className="block text-xs font-semibold text-zinc-300 mb-3">
                    📍 Widget Position
                </label>

                <div className="grid grid-cols-2 gap-3">
                    {(['bottom-right', 'bottom-left'] as const).map((position) => {
                        const active = config.position === position;
                        return (
                            <button
                                key={position}
                                onClick={() => handleChange('position', position)}
                                className={`rounded-lg px-4 py-2 text-xs font-medium border transition-all
                ${active
                                        ? 'bg-blue-400/10 border-blue-400 text-blue-300 ring-1 ring-blue-400/40'
                                        : 'bg-zinc-950 border-white/10 text-zinc-400 hover:border-white/20'
                                    }`}
                            >
                                {position === 'bottom-right' ? 'Bottom Right ↘' : 'Bottom Left ↙'}
                            </button>
                        );
                    })}
                </div>
            </div>

            {/* BUTTON STYLE */}
            <div className="bg-zinc-900/60 border border-white/10 rounded-xl p-4">
                <label className="block text-xs font-semibold text-zinc-300 mb-3">
                    🔘 Button Shape
                </label>

                <div className="grid grid-cols-3 gap-3">
                    {(['circle', 'rounded', 'square'] as const).map((style) => {
                        const active = config.button_style === style;
                        return (
                            <button
                                key={style}
                                onClick={() => handleChange('button_style', style)}
                                className={`rounded-lg py-2 text-xs capitalize border transition-all
                ${active
                                        ? 'bg-blue-400/10 border-blue-400 text-blue-300 ring-1 ring-blue-400/40'
                                        : 'bg-zinc-950 border-white/10 text-zinc-400 hover:border-white/20'
                                    }`}
                            >
                                {style}
                            </button>
                        );
                    })}
                </div>
            </div>

            {/* SAVE */}
            <div className="pt-2">
                <button
                    onClick={handleSave}
                    disabled={isSaving}
                    className="w-full rounded-xl py-3 text-sm font-bold transition-all
          bg-blue-500 text-white hover:bg-blue-600 duration-200 transition-all
          disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    {isSaving
                        ? '💾 Saving...'
                        : saveStatus === 'success'
                            ? '✅ Saved Successfully'
                            : saveStatus === 'error'
                                ? '❌ Failed to Save'
                                : '💾 Save Widget Settings'}
                </button>
            </div>
        </div>
    );

}
