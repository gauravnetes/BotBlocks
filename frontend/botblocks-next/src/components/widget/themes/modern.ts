// Modern Theme - Liquid Glass Effect
import { hexToRgba } from './utils';

export const modernTheme = (primaryColor: string) => ({
    name: 'modern',

    // Container
    windowBackground: 'rgba(10, 10, 10, 0.85)',
    windowBorder: '1px solid rgba(255, 255, 255, 0.1)',
    windowBorderRadius: '24px',
    windowShadow: `0 8px 32px rgba(0, 0, 0, 0.1), 0 0 0 1px rgba(255, 255, 255, 0.1), inset 0 0 0 1px rgba(255, 255, 255, 0.05)`,
    backdropFilter: 'blur(40px) saturate(180%)',

    // Header
    headerBackground: 'rgba(15, 15, 15, 0.5)',
    headerBorder: '1px solid rgba(255, 255, 255, 0.05)',
    headerText: '#ffffff',
    headerSubtext: 'rgba(255, 255, 255, 0.5)',

    // Avatar
    avatarBackground: hexToRgba(primaryColor, 0.1),
    avatarBorder: `1px solid ${hexToRgba(primaryColor, 0.3)}`,
    avatarBorderRadius: '12px',

    // Toggle Button
    toggleBackground: 'rgba(15, 15, 15, 0.8)',
    toggleBorder: '1px solid rgba(255, 255, 255, 0.1)',
    toggleShadow: '0 8px 32px rgba(0, 0, 0, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.1)',
    toggleHoverShadow: `0 12px 40px ${hexToRgba(primaryColor, 0.3)}, inset 0 1px 0 rgba(255, 255, 255, 0.2)`,
    toggleHoverBorder: hexToRgba(primaryColor, 0.4),

    // Messages
    botMessageBackground: 'rgba(255, 255, 255, 0.05)',
    botMessageBorder: '1px solid rgba(255, 255, 255, 0.1)',
    botMessageText: '#e0e0e0',
    botMessageShadow: '0 4px 16px rgba(0, 0, 0, 0.2)',

    userMessageBackground: hexToRgba(primaryColor, 0.15),
    userMessageBorder: `1px solid ${hexToRgba(primaryColor, 0.3)}`,
    userMessageText: '#ffffff',
    userMessageShadow: `0 4px 16px ${hexToRgba(primaryColor, 0.2)}`,

    messageBorderRadius: '16px',

    // Input
    inputBackground: 'rgba(255, 255, 255, 0.05)',
    inputBorder: '1px solid rgba(255, 255, 255, 0.1)',
    inputBorderRadius: '14px',
    inputText: '#ffffff',
    inputPlaceholder: 'rgba(255, 255, 255, 0.4)',
    inputFocusBorder: hexToRgba(primaryColor, 0.5),
    inputFocusShadow: `0 0 0 3px ${hexToRgba(primaryColor, 0.1)}`,

    // Send Button
    sendButtonBackground: primaryColor,
    sendButtonText: '#ffffff',
    sendButtonShadow: `0 4px 16px ${hexToRgba(primaryColor, 0.3)}`,
    sendButtonHoverBackground: primaryColor, // Ideally darken this slightly
    sendButtonHoverShadow: `0 6px 20px ${hexToRgba(primaryColor, 0.4)}`,

    // Close Button
    closeButtonBackground: 'rgba(255, 255, 255, 0.05)',
    closeButtonBorder: '1px solid rgba(255, 255, 255, 0.1)',
    closeButtonText: 'rgba(255, 255, 255, 0.7)',
    closeButtonHoverBackground: 'rgba(255, 255, 255, 0.1)',
    closeButtonHoverText: '#ffffff',

    // Scrollbar
    scrollbarTrack: 'transparent',
    scrollbarThumb: 'rgba(255, 255, 255, 0.1)',

    // Status Indicator
    statusIndicatorOnline: '#10b981',
    statusIndicatorOffline: '#ef4444',
});
