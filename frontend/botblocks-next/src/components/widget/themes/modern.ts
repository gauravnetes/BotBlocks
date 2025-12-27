// Modern Theme - BotBlocks Gen Z (High Contrast, Rounded)
import { hexToRgba } from './utils';

export const modernTheme = (primaryColor: string) => ({
    name: 'modern',

    // Container
    windowBackground: '#09090b', // zinc-950
    windowBorder: '1px solid #27272a', // zinc-800
    windowBorderRadius: '30px', // Super rounded
    windowShadow: '0 0 0 1px #000000, 0 12px 40px rgba(0,0,0,0.4)',
    backdropFilter: 'none',

    // Header
    headerBackground: 'transparent',
    headerBorder: '1px solid #27272a',
    headerText: '#ffffff',
    headerSubtext: '#a1a1aa', // zinc-400

    // Avatar
    avatarBackground: '#18181b', // zinc-900
    avatarBorder: '1px solid #27272a',
    avatarBorderRadius: '50%', // Circle for roundness

    // Toggle Button
    toggleBackground: '#000000',
    toggleBorder: '1px solid #27272a',
    toggleShadow: '0 4px 12px rgba(0,0,0,0.2)',
    toggleHoverShadow: '0 8px 24px rgba(0,0,0,0.4)',
    toggleHoverBorder: '#ffffff',

    // Messages
    botMessageBackground: '#18181b', // zinc-900
    botMessageBorder: '1px solid #27272a',
    botMessageText: '#ffffff',
    botMessageShadow: 'none',

    userMessageBackground: '#ffffff', // Pure white pop
    userMessageBorder: 'none',
    userMessageText: '#000000',
    userMessageShadow: '0 2px 8px rgba(0,0,0,0.1)',

    messageBorderRadius: '20px', // Rounder bubbles

    // Input
    inputBackground: '#18181b',
    inputBorder: '1px solid #27272a',
    inputBorderRadius: '24px', // Pill shape
    inputText: '#ffffff',
    inputPlaceholder: '#71717a',
    inputFocusBorder: '#52525b',
    inputFocusShadow: 'none',

    // Send Button
    sendButtonBackground: '#ffffff',
    sendButtonText: '#000000',
    sendButtonShadow: 'none',
    sendButtonHoverBackground: '#e4e4e7',
    sendButtonHoverShadow: 'none',

    // Close Button
    closeButtonBackground: '#18181b',
    closeButtonBorder: 'none',
    closeButtonText: '#a1a1aa',
    closeButtonHoverBackground: '#27272a',
    closeButtonHoverText: '#ffffff',

    // Scrollbar
    scrollbarTrack: 'transparent',
    scrollbarThumb: '#3f3f46',

    // Status Indicator
    statusIndicatorOnline: '#10b981',
    statusIndicatorOffline: '#ef4444',
});
