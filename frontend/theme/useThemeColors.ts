import { useThemeContext } from "../context/ThemeContext";
import { Colors } from "../constants/Colors";

export function useThemeColors() {
  const { theme } = useThemeContext();
  return theme === "dark" ? Colors.dark : Colors.light;
}