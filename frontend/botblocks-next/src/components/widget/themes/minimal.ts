// Apple Transparent Liquid Glass Theme
import { hexToRgba } from './utils';

export const minimalTheme = (primaryColor: string) => ({
  name: 'minimal',

  /* ======================
     MAIN GLASS WINDOW
  ====================== */

  // TRUE TRANSPARENCY
  windowBackground: 'rgba(255,255,255,0.12)',

  // Edge highlight (Apple style)
  windowBorder: '1px solid rgba(255,255,255,0.35)',

  windowBorderRadius: '26px',

  // VERY minimal shadow (almost invisible)
  windowShadow: '0 6px 18px rgba(0,0,0,0.12)',

  // THIS IS THE MAGIC
  backdropFilter: 'blur(36px) saturate(200%)',

  /* ======================
     HEADER
  ====================== */
  headerBackground: 'transparent',
  headerBorder: 'none',
  headerText: '#ffffff',
  headerSubtext: 'rgba(255,255,255,0.6)',

  /* ======================
     AVATAR (GLASS ORB)
  ====================== */
  avatarBackground: 'rgba(255,255,255,0.35)',
  avatarBorder: '1px solid rgba(255,255,255,0.45)',
  avatarBorderRadius: '50%',

  /* ======================
     TOGGLE BUTTON (FLOATING GLASS)
  ====================== */
  toggleBackground: 'rgba(255,255,255,0.25)',
  toggleBorder: '1px solid rgba(255,255,255,0.45)',
  toggleShadow: '0 6px 18px rgba(0,0,0,0.15)',
  toggleHoverShadow: `0 10px 28px ${hexToRgba(primaryColor, 0.25)}`,
  toggleHoverBorder: hexToRgba(primaryColor, 0.4),

  /* ======================
     BOT MESSAGE (FROSTED GLASS)
  ====================== */
  botMessageBackground: 'rgba(255,255,255,0.35)',
  botMessageBorder: '1px solid rgba(255,255,255,0.45)',
  botMessageText: '#ffffff',

  // Apple uses INNER highlight instead of shadow
  botMessageShadow: 'inset 0 1px 0 rgba(255,255,255,0.6)',

  /* ======================
     USER MESSAGE (TINTED GLASS)
  ====================== */
  userMessageBackground: hexToRgba(primaryColor, 0.35),
  userMessageBorder: `1px solid ${hexToRgba(primaryColor, 0.45)}`,
  userMessageText: '#ffffff',
  userMessageShadow: 'inset 0 1px 0 rgba(255,255,255,0.6)',

  messageBorderRadius: '22px',

  /* ======================
     INPUT (GLASS BAR)
  ====================== */
  inputBackground: 'rgba(255,255,255,0.25)',
  inputBorder: '1px solid rgba(255,255,255,0.45)',
  inputBorderRadius: '22px',
  inputText: '#ffffff',
  inputPlaceholder: 'rgba(255,255,255,0.6)',

  inputFocusBorder: hexToRgba(primaryColor, 0.45),
  inputFocusShadow: `0 0 0 3px ${hexToRgba(primaryColor, 0.2)}`,

  /* ======================
     SEND BUTTON (GLOSSY GLASS)
  ====================== */
  sendButtonBackground: `
    linear-gradient(
      180deg,
      ${hexToRgba(primaryColor, 0.9)},
      ${hexToRgba(primaryColor, 0.7)}
    )
  `,
  sendButtonText: '#ffffff',

  // NO heavy shadow
  sendButtonShadow: 'inset 0 1px 0 rgba(255,255,255,0.6)',
  sendButtonHoverBackground: `
    linear-gradient(
      180deg,
      ${hexToRgba(primaryColor, 1)},
      ${hexToRgba(primaryColor, 0.85)}
    )
  `,
  sendButtonHoverShadow: 'inset 0 1px 0 rgba(255,255,255,0.7)',

  /* ======================
     CLOSE BUTTON
  ====================== */
  closeButtonBackground: 'rgba(255,255,255,0.3)',
  closeButtonBorder: '1px solid rgba(255,255,255,0.45)',
  closeButtonText: '#ffffff',
  closeButtonHoverBackground: 'rgba(255,255,255,0.5)',
  closeButtonHoverText: '#ffffff',

  /* ======================
     SCROLLBAR
  ====================== */
  scrollbarTrack: 'transparent',
  scrollbarThumb: 'rgba(255,255,255,0.25)',

  /* ======================
     STATUS DOT
  ====================== */
  statusIndicatorOnline: '#22c55e',
  statusIndicatorOffline: '#ef4444',
});
