// Minimal Theme - iOS Liquid Glass (Apple Aesthetic - Rounded)
import { hexToRgba } from './utils';

export const minimalTheme = (primaryColor: string) => ({
   name: 'minimal',

   // Container
   windowBackground: 'rgba(255, 255, 255, 0.75)',
   windowBorder: '1px solid rgba(255, 255, 255, 0.4)',
   windowBorderRadius: '32px', // Max roundness
   windowShadow: '0 20px 50px rgba(0, 0, 0, 0.1)',
   backdropFilter: 'blur(20px) saturate(180%)',

   // Header
   headerBackground: 'rgba(255, 255, 255, 0.5)',
   headerBorder: '1px solid rgba(0, 0, 0, 0.05)',
   headerText: '#1c1c1e',
   headerSubtext: '#8e8e93',

   // Avatar
   avatarBackground: '#f2f2f7',
   avatarBorder: 'none',
   avatarBorderRadius: '50%',

   // Toggle Button
   toggleBackground: 'rgba(255, 255, 255, 0.8)',
   toggleBorder: '1px solid rgba(0, 0, 0, 0.05)',
   toggleShadow: '0 4px 12px rgba(0, 0, 0, 0.08)',
   toggleHoverShadow: '0 8px 20px rgba(0, 0, 0, 0.12)',
   toggleHoverBorder: 'transparent',

   // Messages
   botMessageBackground: '#ffffff',
   botMessageBorder: 'none',
   botMessageText: '#1c1c1e',
   botMessageShadow: '0 2px 4px rgba(0, 0, 0, 0.02)',

   userMessageBackground: '#007AFF',
   userMessageBorder: 'none',
   userMessageText: '#ffffff',
   userMessageShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',

   messageBorderRadius: '22px', // Super round

   // Input
   inputBackground: 'rgba(255, 255, 255, 0.6)',
   inputBorder: '1px solid rgba(0, 0, 0, 0.05)',
   inputBorderRadius: '26px', // Maximum pill
   inputText: '#1c1c1e',
   inputPlaceholder: '#aeaeb2',
   inputFocusBorder: 'rgba(0, 0, 0, 0.1)',
   inputFocusShadow: 'none',

   // Send Button
   sendButtonBackground: '#1c1c1e',
   sendButtonText: '#ffffff',
   sendButtonShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
   sendButtonHoverBackground: '#3a3a3c',
   sendButtonHoverShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',

   // Close Button
   closeButtonBackground: '#e5e5ea',
   closeButtonBorder: 'none',
   closeButtonText: '#8e8e93',
   closeButtonHoverBackground: '#d1d1d6',
   closeButtonHoverText: '#1c1c1e',

   // Scrollbar
   scrollbarTrack: 'transparent',
   scrollbarThumb: 'rgba(0, 0, 0, 0.2)',

   // Status Indicator
   statusIndicatorOnline: '#34c759',
   statusIndicatorOffline: '#ff3b30',
});
