/**
 * Below are the colors that are used in the app. The colors are defined in the light and dark mode.
 * There are many other ways to style your app. For example, [Nativewind](https://www.nativewind.dev/), [Tamagui](https://tamagui.dev/), [unistyles](https://reactnativeunistyles.vercel.app), etc.
 */

const tintColorLight = '#2ecc40'; // mocna zieleń
const tintColorDark = '#2962ff';  // niebieski

export const Colors = {
  light: {
    text: '#1b3a1b',           // ciemna zieleń do tekstu
    background: '#e8f5e9',     // bardzo jasna zieleń
    tint: tintColorLight,      // zielony dla głównych przycisków
    icon: '#388e3c',           // ciemniejsza zieleń do ikon
    tabIconDefault: '#388e3c', // domyślna ikona
    tabIconSelected: tintColorLight, // wybrana ikona
    tagBackground: "#b9f6ca", // jasna zieleń
    tagText: "#1b3a1b",
    tagTextmodify: "#496b52", // zmodyfikowany tagText          xxxxxxx
    buttonBackground: "#b9f6ca", // taki sam jak tagBackground
    buttonText: "#1b3a1b",       // taki sam jak tagText
    logout: "#ff9800",         // pomarańczowy (Material Orange 500)
  },
  dark: {
    text: '#ECEDEE',
    background: '#151718',
    tint: tintColorDark,       // niebieski dla głównych przycisków
    icon: '#9BA1A6',
    tabIconDefault: '#9BA1A6',
    tabIconSelected: tintColorDark,
    tagBackground: "#2962ff", // niebieski dla ciemnego motywu
    tagText: "#fff",
    tagTextmodify: "#0e308c", // zmodyfikowany tagText               xxxxxxxxxxxxxxxxxxxxxx
    buttonBackground: "#2962ff", // taki sam jak tagBackground
    buttonText: "#fff",          // taki sam jak tagText
    logout: "#ff9800",         // pomarańczowy (taki sam)
  },
};
