// Classic Theme - Dracula VS Code (Official Palette)
import { hexToRgba } from './utils';

// Dracula Palette
const DRACULA = {
   background: '#282a36',
   currentLine: '#44475a',
   foreground: '#f8f8f2',
   comment: '#6272a4',
   cyan: '#8be9fd',
   green: '#50fa7b',
   orange: '#ffb86c',
   pink: '#ff79c6',
   purple: '#bd93f9',
   red: '#ff5555',
   yellow: '#f1fa8c',
};

export const classicTheme = (primaryColor: string) => ({
   name: 'classic',

   // Container - Dracula Background
   windowBackground: DRACULA.background,
   windowBorder: `1px solid ${DRACULA.currentLine}`,
   windowBorderRadius: '28px',
   windowShadow: '0 12px 40px rgba(0,0,0,0.4)',
   backdropFilter: 'none',

   // Header
   headerBackground: DRACULA.background,
   headerBorder: `1px solid ${DRACULA.currentLine}`,
   headerText: DRACULA.foreground,
   headerSubtext: DRACULA.comment,

   // Avatar
   avatarBackground: DRACULA.currentLine,
   avatarBorder: `1px solid ${DRACULA.comment}`,
   avatarBorderRadius: '50%',

   // Toggle Button - Dark (Dracula Current Line)
   toggleBackground: DRACULA.currentLine,
   toggleBorder: `1px solid ${DRACULA.comment}`,
   toggleShadow: '0 6px 14px rgba(0,0,0,0.3)',
   toggleHoverShadow: `0 8px 24px ${hexToRgba(DRACULA.purple, 0.4)}`,
   toggleHoverBorder: 'none',

   // Messages
   botMessageBackground: DRACULA.currentLine,
   botMessageBorder: 'none',
   botMessageText: DRACULA.foreground,
   botMessageShadow: 'none',

   userMessageBackground: DRACULA.pink, // Pink for user pop
   userMessageBorder: 'none',
   userMessageText: DRACULA.background, // Dark text on pink
   userMessageShadow: '0 2px 4px rgba(0,0,0,0.2)',

   messageBorderRadius: '20px',

   // Input
   inputBackground: DRACULA.currentLine,
   inputBorder: '1px solid #6272a4', // comment color
   inputBorderRadius: '24px',
   inputText: DRACULA.foreground,
   inputPlaceholder: DRACULA.comment,
   inputFocusBorder: DRACULA.pink,
   inputFocusShadow: `0 0 0 2px ${hexToRgba(DRACULA.pink, 0.2)}`,

   // Send Button - Green (Go!)
   sendButtonBackground: DRACULA.green,
   sendButtonText: DRACULA.background, // Dark text on green
   sendButtonShadow: '0 2px 4px rgba(0,0,0,0.2)',
   sendButtonHoverBackground: '#5af78e', // slightly lighter green
   sendButtonHoverShadow: '0 4px 12px rgba(80, 250, 123, 0.3)',

   // Close Button
   closeButtonBackground: 'transparent',
   closeButtonBorder: 'none',
   closeButtonText: DRACULA.comment,
   closeButtonHoverBackground: DRACULA.currentLine,
   closeButtonHoverText: DRACULA.red, // Red hover for close

   // Scrollbar
   scrollbarTrack: 'transparent',
   scrollbarThumb: DRACULA.comment,

   // Status Indicator
   statusIndicatorOnline: DRACULA.green,
   statusIndicatorOffline: DRACULA.red,
});
