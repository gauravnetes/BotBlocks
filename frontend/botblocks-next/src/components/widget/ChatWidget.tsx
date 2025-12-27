"use client";
import { useState, useEffect, useRef } from 'react';
import { Send, X } from 'lucide-react';
import { getTheme, ThemeName } from './themes';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface Message {
    text: string;
    type: 'user' | 'bot';
}

interface ChatWidgetProps {
    botId: string;
    config: {
        theme: ThemeName;
        primary_color: string;
        avatar_url?: string;
        welcome_message: string;
        bot_display_name: string;
        position: 'bottom-right' | 'bottom-left';
        suggested_questions?: string[];
        button_style?: 'circle' | 'rounded' | 'square';
    };
    previewMode?: boolean;
    customWidth?: string;
    customHeight?: string;
}

export function ChatWidget({
    botId,
    config,
    previewMode = false,
    customWidth = '400px',
    customHeight = '600px'
}: ChatWidgetProps) {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<Message[]>([
        { text: config.welcome_message, type: 'bot' }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const theme = getTheme(config.theme, config.primary_color);
    const position = config.position === 'bottom-left' ? 'left-6' : 'right-6';

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const sendMessage = async (overrideText?: string) => {
        const textToSend = overrideText || input.trim();
        if (!textToSend || isLoading) return;

        setInput('');
        setMessages(prev => [...prev, { text: textToSend, type: 'user' }]);
        setIsLoading(true);

        try {
            const res = await fetch('http://127.0.0.1:8000/api/v1/chat/web', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ bot_id: botId, message: textToSend })
            });

            const data = await res.json();
            setMessages(prev => [...prev, { text: data.response, type: 'bot' }]);
        } catch (error) {
            setMessages(prev => [...prev, { text: 'Connection error. Please try again.', type: 'bot' }]);
        } finally {
            setIsLoading(false);
        }
    };

    const toggleWidget = () => setIsOpen(prev => !prev);
    const closeWidget = () => setIsOpen(false);

    // Notify parent window about size changes for iframe embedding
    useEffect(() => {
        if (!previewMode && typeof window !== 'undefined') {
            const message = {
                type: 'BOTBLOCKS_RESIZE',
                // Large padding for shadows
                // Increased container size for larger widget + shadows
                // Use custom dimensions + 60px/220px padding for shadows and gap
                width: isOpen ? `calc(${customWidth} + 60px)` : '120px',
                height: isOpen ? `calc(${customHeight} + 220px)` : '120px',
                position: config.position,
                isOpen
            };
            window.parent.postMessage(message, '*');
        }
    }, [isOpen, previewMode]);

    // Dynamic styles for preview mode vs fixed mode
    const containerStyle: React.CSSProperties = previewMode
        ? {
            position: 'absolute',
            bottom: '24px',
            [config.position === 'bottom-left' ? 'left' : 'right']: '24px',
            zIndex: 10
        }
        : {
            position: 'fixed',
            // Increase margin to prevent shadow clipping (48px)
            // Tighten edge margin to 20px
            bottom: '48px',
            [config.position === 'bottom-left' ? 'left' : 'right']: '20px',
            zIndex: 9999
        };

    const windowStyle: React.CSSProperties = previewMode
        ? {
            position: 'absolute',
            bottom: '90px',
            [config.position === 'bottom-left' ? 'left' : 'right']: '0',
            zIndex: 20
        }
        : {
            position: 'fixed',
            // Gap above toggle button (48px bottom + 45px height + 17px gap = 110px)
            bottom: '110px',
            [config.position === 'bottom-left' ? 'left' : 'right']: '20px',
        };

    return (
        <div
            className={previewMode ? "absolute" : "fixed"}
            style={containerStyle}
        >
            {/* Toggle Button */}
            <button
                onClick={toggleWidget}
                className="transition-all duration-200 ease-out hover:scale-110"
                style={{
                    width: '45px',
                    height: '45px',
                    background: theme.toggleBackground,
                    backdropFilter: theme.backdropFilter,
                    WebkitBackdropFilter: theme.backdropFilter,
                    border: theme.toggleBorder,
                    borderRadius: config.button_style === 'circle' ? '50%' : config.button_style === 'rounded' ? '16px' : '8px',
                    boxShadow: theme.toggleShadow,
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '28px',
                    position: 'relative',
                    overflow: 'hidden'
                }}
                onMouseEnter={(e) => {
                    e.currentTarget.style.boxShadow = theme.toggleHoverShadow;
                    e.currentTarget.style.borderColor = theme.toggleHoverBorder;
                }}
                onMouseLeave={(e) => {
                    e.currentTarget.style.boxShadow = theme.toggleShadow;
                    e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.1)';
                }}
            >
                {config.avatar_url ? (
                    <img src={config.avatar_url} alt="Bot" className="w-8 h-8 rounded-full" />
                ) : (
                    <span style={{ filter: 'drop-shadow(0 0 8px rgba(59, 130, 246, 0.5))' }}>💬</span>
                )}
            </button>

            {/* Chat Window */}
            {isOpen && (
                <div
                    className="max-w-[calc(100vw-40px)] flex flex-col overflow-hidden"
                    style={{
                        ...windowStyle,
                        width: customWidth,
                        height: customHeight,
                        background: theme.windowBackground,
                        backdropFilter: theme.backdropFilter,
                        WebkitBackdropFilter: theme.backdropFilter,
                        border: theme.windowBorder,
                        borderRadius: theme.windowBorderRadius,
                        boxShadow: theme.windowShadow,
                        transformOrigin: config.position === 'bottom-left' ? 'bottom left' : 'bottom right',
                        animation: 'openWidget 0.35s cubic-bezier(0.34, 1.56, 0.64, 1) forwards'
                    }}
                >
                    {/* Header */}
                    <div
                        className="flex justify-between items-center p-6"
                        style={{
                            background: theme.headerBackground,
                            backdropFilter: 'blur(10px)',
                            borderBottom: theme.headerBorder
                        }}
                    >
                        <div className="flex items-center gap-3">
                            <div
                                className="flex items-center justify-center text-xl"
                                style={{
                                    width: '40px',
                                    height: '40px',
                                    background: theme.avatarBackground,
                                    border: theme.avatarBorder,
                                    borderRadius: theme.avatarBorderRadius
                                }}
                            >
                                {config.avatar_url ? (
                                    <img src={config.avatar_url} alt="Bot" className="w-full h-full rounded-lg" />
                                ) : (
                                    '🤖'
                                )}
                            </div>
                            <div>
                                <h3 className="font-semibold capitalize" style={{ color: theme.headerText, fontSize: '16px' }}>
                                    {config.bot_display_name}
                                </h3>
                                <p className="text-xs" style={{ color: theme.headerSubtext }}>
                                    <span className="inline-block w-2 h-2 rounded-full mr-1.5 animate-pulse" style={{ background: theme.statusIndicatorOnline }}></span>
                                    Online
                                </p>
                            </div>
                        </div>

                        <button
                            onClick={closeWidget}
                            className="flex items-center justify-center w-8 h-8 rounded-xl transition-all duration-200"
                            style={{
                                background: theme.closeButtonBackground,
                                border: theme.closeButtonBorder,
                                color: theme.closeButtonText
                            }}
                            onMouseEnter={(e) => {
                                e.currentTarget.style.background = theme.closeButtonHoverBackground;
                                e.currentTarget.style.color = theme.closeButtonHoverText;
                                e.currentTarget.style.transform = 'rotate(90deg)';
                            }}
                            onMouseLeave={(e) => {
                                e.currentTarget.style.background = theme.closeButtonBackground;
                                e.currentTarget.style.color = theme.closeButtonText;
                                e.currentTarget.style.transform = 'rotate(0deg)';
                            }}
                        >
                            <X className="w-4 h-4" />
                        </button>
                    </div>



                    {/* Messages */}
                    <div className="flex-1 p-5 overflow-y-auto flex flex-col gap-4" style={{
                        scrollbarWidth: 'thin',
                        scrollbarColor: `${theme.scrollbarThumb} ${theme.scrollbarTrack}`
                    }}>
                        {messages.map((msg, idx) => (
                            <div
                                key={idx}
                                className="max-w-[80%] p-3.5 px-4 animate-[messageSlide_0.3s_cubic-bezier(0.34,1.56,0.64,1)]"
                                style={{
                                    alignSelf: msg.type === 'user' ? 'flex-end' : 'flex-start',
                                    background: msg.type === 'user' ? theme.userMessageBackground : theme.botMessageBackground,
                                    border: msg.type === 'user' ? theme.userMessageBorder : theme.botMessageBorder,
                                    borderRadius: theme.messageBorderRadius,
                                    color: msg.type === 'user' ? theme.userMessageText : theme.botMessageText,
                                    boxShadow: msg.type === 'user' ? theme.userMessageShadow : theme.botMessageShadow,
                                    backdropFilter: 'blur(10px)',
                                    fontSize: '14px',
                                    lineHeight: '1.5'
                                }}
                            >
                                {msg.type === 'bot' ? (
                                    <div className="prose prose-sm prose-invert max-w-none break-words markdown-content">
                                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                            {msg.text}
                                        </ReactMarkdown>
                                    </div>
                                ) : (
                                    msg.text
                                )}
                            </div>
                        ))}
                        {isLoading && (
                            <div className="flex items-center gap-2 text-sm" style={{ color: theme.botMessageText }}>
                                <div className="flex gap-1">
                                    <span className="w-2 h-2 rounded-full animate-bounce" style={{ background: theme.botMessageText, animationDelay: '0ms' }}></span>
                                    <span className="w-2 h-2 rounded-full animate-bounce" style={{ background: theme.botMessageText, animationDelay: '150ms' }}></span>
                                    <span className="w-2 h-2 rounded-full animate-bounce" style={{ background: theme.botMessageText, animationDelay: '300ms' }}></span>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />

                        {/* Suggested Questions */}
                        {config.suggested_questions && config.suggested_questions.length > 0 && messages.length === 1 && (
                            <div className="flex flex-col gap-2 mt-auto animate-[fadeIn_0.5s_ease-out]">
                                {config.suggested_questions.map((q, idx) => (
                                    <button
                                        key={idx}
                                        onClick={() => {
                                            setInput(q);
                                            // Need to wrap in timeout/effect or call submit directly but input state update is async.
                                            // Better to extract send logic to accept text.
                                            // For now, let's just modify sendMessage to take optional text.
                                            sendMessage(q);
                                        }}
                                        className="text-left px-4 py-2.5 rounded-xl text-sm transition-all duration-200 hover:-translate-y-0.5"
                                        style={{
                                            background: theme.botMessageBackground,
                                            border: theme.botMessageBorder,
                                            color: theme.botMessageText,
                                            boxShadow: '0 2px 8px rgba(0,0,0,0.05)',
                                            backdropFilter: 'blur(10px)'
                                        }}
                                        onMouseEnter={(e) => {
                                            e.currentTarget.style.background = theme.headerBackground;
                                            e.currentTarget.style.borderColor = "#3b82f6"; // Fallback to blue-500 since primaryColor isn't on theme object directly
                                        }}
                                        onMouseLeave={(e) => {
                                            e.currentTarget.style.background = theme.botMessageBackground;
                                            e.currentTarget.style.borderColor = 'transparent'; // assumption based on usage
                                        }}
                                    >
                                        {q}
                                    </button>
                                ))}
                            </div>
                        )}
                    </div>

                    <div className="p-5 flex flex-col gap-3" style={{
                        background: theme.headerBackground,
                        backdropFilter: 'blur(10px)',
                        borderTop: theme.headerBorder
                    }}>
                        <div className="flex gap-2">
                            <input
                                type="text"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                                placeholder="Type your message..."
                                className="flex-1 px-4 py-3 rounded-2xl outline-none transition-all duration-200"
                                style={{
                                    background: theme.inputBackground,
                                    border: theme.inputBorder,
                                    borderRadius: theme.inputBorderRadius,
                                    color: theme.inputText,
                                    fontSize: '14px'
                                }}
                                onFocus={(e) => {
                                    e.currentTarget.style.borderColor = theme.inputFocusBorder;
                                    e.currentTarget.style.boxShadow = theme.inputFocusShadow;
                                }}
                                onBlur={(e) => {
                                    e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.1)';
                                    e.currentTarget.style.boxShadow = 'none';
                                }}
                            />
                            <button
                                onClick={() => sendMessage()}
                                disabled={!input.trim() || isLoading}
                                className="w-12 h-12 flex items-center justify-center rounded-2xl font-semibold transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shrink-0"
                                style={{
                                    background: theme.sendButtonBackground,
                                    color: theme.sendButtonText,
                                    boxShadow: theme.sendButtonShadow,
                                }}
                                onMouseEnter={(e) => {
                                    if (!e.currentTarget.disabled) {
                                        e.currentTarget.style.background = theme.sendButtonHoverBackground;
                                        e.currentTarget.style.boxShadow = theme.sendButtonHoverShadow;
                                        e.currentTarget.style.transform = 'scale(1.05) rotate(-10deg)';
                                    }
                                }}
                                onMouseLeave={(e) => {
                                    e.currentTarget.style.background = theme.sendButtonBackground;
                                    e.currentTarget.style.boxShadow = theme.sendButtonShadow;
                                    e.currentTarget.style.transform = 'scale(1) rotate(0deg)';
                                }}
                            >
                                <Send className="w-5 h-5" />
                            </button>
                        </div>

                        {/* Relocated Watermark */}
                        <div className="text-center pt-1">
                            <a
                                href="https://botblocks.ai"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-[10px] font-bold opacity-30 hover:opacity-100 transition-all no-underline tracking-widest uppercase"
                                style={{ color: theme.inputText }}
                            >
                                Powered by BotBlocks
                            </a>
                        </div>
                    </div>
                </div>
            )}

            <style jsx global>{`
        @keyframes openWidget {
          from {
            opacity: 0;
            transform: scale(0.92) translateY(16px);
          }
          to {
            opacity: 1;
            transform: scale(1) translateY(0);
          }
        }

        @keyframes messageSlide {
          from {
            opacity: 0;
            transform: translateY(12px) scale(0.95);
          }
          to {
            opacity: 1;
            transform: translateY(0) scale(1);
          }
        }

        input::placeholder {
          color: ${theme.inputPlaceholder};
        }

        .markdown-content {
            line-height: 1.6;
            letter-spacing: 0.01em;
            color: rgba(255, 255, 255, 0.9);
        }
        .markdown-content p {
            margin-bottom: 0.8rem;
        }
        .markdown-content p:last-child {
            margin-bottom: 0;
        }
        .markdown-content ul, .markdown-content ol {
            padding-left: 1.2rem;
            margin: 0.8rem 0;
        }
        .markdown-content li {
            margin-bottom: 0.4rem;
        }
        .markdown-content strong {
            font-weight: 700;
            color: #fff;
            letter-spacing: 0;
        }
        .markdown-content code {
            background: rgba(255, 255, 255, 0.1);
            padding: 0.15rem 0.4rem;
            border-radius: 0.4rem;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            font-size: 0.9em;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
      `}</style>
        </div>
    );
}
