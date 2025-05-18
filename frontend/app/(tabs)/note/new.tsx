import React, { useState } from "react";
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert } from "react-native";
import { useThemeColors } from "../../../theme/useThemeColors";
import { useAuth } from "../../../context/AuthContext";
import { useRouter } from "expo-router";
import { createNote } from "../../../services/api";
import { useFocusEffect } from "@react-navigation/native";

export default function NewNoteScreen() {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(false);
  const colors = useThemeColors();
  const { apiKey, userId } = useAuth();
  const router = useRouter();

  useFocusEffect(
    React.useCallback(() => {
      setTitle("");
      setContent("");
    }, [])
  );

  const handleSave = async () => {
    if (!title.trim()) {
      Alert.alert("Błąd", "Tytuł nie może być pusty");
      return;
    }
    setLoading(true);
    try {
      const note = await createNote(apiKey ?? "", userId ?? 0, { title, content });
      router.replace("/"); // wróć na główną i odśwież listę
    } catch (e: any) {
      Alert.alert("Błąd", e?.message || "Nie udało się utworzyć notatki");
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      <Text style={[styles.title, { color: colors.text }]}>Nowa notatka</Text>
      <TextInput
        placeholder="Tytuł"
        placeholderTextColor={colors.icon}
        value={title}
        onChangeText={setTitle}
        style={[
          styles.input,
          { backgroundColor: colors.background, borderColor: colors.tabIconDefault, color: colors.text },
        ]}
      />
      <TextInput
        placeholder="Treść"
        placeholderTextColor={colors.icon}
        value={content}
        onChangeText={setContent}
        multiline
        style={[
          styles.textarea,
          { backgroundColor: colors.background, borderColor: colors.tabIconDefault, color: colors.text },
        ]}
      />
      <TouchableOpacity
        style={[styles.button, { backgroundColor: colors.tint }]}
        onPress={handleSave}
        disabled={loading}
        activeOpacity={0.8}
      >
        <Text style={[styles.buttonText, { color: "#fff" }]}>
          {loading ? "Zapisywanie..." : "Zapisz"}
        </Text>
      </TouchableOpacity>
      <TouchableOpacity onPress={() => router.back()}>
        <Text style={{ color: colors.tint, marginTop: 24, textAlign: "center" }}>
          Anuluj
        </Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 24,
    justifyContent: "flex-start",
  },
  title: {
    fontSize: 22,
    fontWeight: "bold",
    marginBottom: 24,
    textAlign: "center",
  },
  input: {
    borderWidth: 1,
    borderRadius: 8,
    padding: 12,
    marginBottom: 16,
    fontSize: 16,
  },
  textarea: {
    borderWidth: 1,
    borderRadius: 8,
    padding: 12,
    minHeight: 120,
    fontSize: 16,
    marginBottom: 16,
    textAlignVertical: "top",
  },
  button: {
    borderRadius: 8,
    paddingVertical: 14,
    alignItems: "center",
    marginTop: 8,
  },
  buttonText: {
    fontSize: 16,
    fontWeight: "bold",
  },
});