import { modernTheme } from './modern';
import { classicTheme } from './classic';
import { minimalTheme } from './minimal';

export type ThemeName = 'modern' | 'classic' | 'minimal';

export function getTheme(themeName: ThemeName = 'modern', primaryColor: string = '#3b82f6') {
    switch (themeName) {
        case 'classic':
            return classicTheme(primaryColor);
        case 'minimal':
            return minimalTheme(primaryColor);
        case 'modern':
        default:
            return modernTheme(primaryColor);
    }
}

export { modernTheme, classicTheme, minimalTheme };
