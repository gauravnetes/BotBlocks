// Classic Theme – Soft Matte Modern (FULL REVAMP)
import { hexToRgba } from './utils';

export const classicTheme = (primaryColor: string) => ({
  name: 'classic',

  /* ======================
     WINDOW / CONTAINER
  ====================== */
  windowBackground: '#0f0f10', // matte black
  windowBorder: '1px solid #1f1f22',
  windowBorderRadius: '16px',
  windowShadow: '0 12px 32px rgba(0,0,0,0.45)',
  backdropFilter: 'none',

  /* ======================
     HEADER
  ====================== */
  headerBackground: '#0f0f10',
  headerBorder: '1px solid #1f1f22',
  headerText: '#f5f5f5',
  headerSubtext: '#9ca3af',

  /* ======================
     AVATAR
  ====================== */
  avatarBackground: '#1f2933',
  avatarBorder: 'none',
  avatarBorderRadius: '8px',

  /* ======================
     TOGGLE BUTTON
  ====================== */
  toggleBackground: '#111113',
  toggleBorder: '1px solid #1f1f22',
  toggleShadow: 'none',
  toggleHoverShadow: 'none',
  toggleHoverBorder: hexToRgba(primaryColor, 0.6),

  /* ======================
     BOT MESSAGE
  ====================== */
  botMessageBackground: '#18181b',
  botMessageBorder: '1px solid #26262a',
  botMessageText: '#e5e7eb',
  botMessageShadow: 'none',

  /* ======================
     USER MESSAGE
  ====================== */
  userMessageBackground: '#f5f5f5',
  userMessageBorder: 'none',
  userMessageText: '#0f0f10',
  userMessageShadow: 'none',

  messageBorderRadius: '14px',

  /* ======================
     INPUT (MODERN CHAT BAR)
  ====================== */
  inputBackground: '#0f0f10',
  inputBorder: '1px solid #26262a',
  inputBorderRadius: '14px',
  inputText: '#f5f5f5',
  inputPlaceholder: '#6b7280',
  inputFocusBorder: primaryColor,
  inputFocusShadow: 'none',

  /* ======================
     SEND BUTTON (FLAT ACCENT)
  ====================== */
  sendButtonBackground: primaryColor,
  sendButtonText: '#ffffff',
  sendButtonShadow: 'none',
  sendButtonHoverBackground: hexToRgba(primaryColor, 0.9),
  sendButtonHoverShadow: 'none',

  /* ======================
     CLOSE BUTTON
  ====================== */
  closeButtonBackground: 'transparent',
  closeButtonBorder: 'none',
  closeButtonText: '#9ca3af',
  closeButtonHoverBackground: '#1f1f22',
  closeButtonHoverText: '#ffffff',

  /* ======================
     SCROLLBAR
  ====================== */
  scrollbarTrack: 'transparent',
  scrollbarThumb: '#2a2a2e',

  /* ======================
     STATUS
  ====================== */
  statusIndicatorOnline: '#16a34a',
  statusIndicatorOffline: '#dc2626',
});
