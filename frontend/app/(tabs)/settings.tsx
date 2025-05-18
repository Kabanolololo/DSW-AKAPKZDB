import React from "react";
import { View, Text, Switch, StyleSheet } from "react-native";
import { useThemeContext } from "../../context/ThemeContext";
import { useThemeColors } from "../../theme/useThemeColors";

export default function SettingsScreen() {
  const { theme, toggleTheme } = useThemeContext();
  const isDark = theme === "dark";
  const colors = useThemeColors();

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      <View style={styles.inner}>
        <Text style={[styles.title, { color: colors.text }]}>
          Ustawienia
        </Text>
        <View style={styles.row}>
          <Text style={[styles.label, { color: colors.text }]}>
            Ciemny motyw
          </Text>
          <Switch value={isDark} onValueChange={toggleTheme} />
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 24,
    justifyContent: "flex-start", // <-- ustaw na górę
  },
  inner: {
    marginTop: 40, // odstęp od górnej krawędzi
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 24,
    textAlign: "center",
  },
  row: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: 16,
  },
  label: {
    fontSize: 18,
  },
});