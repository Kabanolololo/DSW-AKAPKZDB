import React, { useEffect, useState, useCallback } from "react";
import { View, Text, FlatList, StyleSheet, TouchableOpacity, Alert } from "react-native";
import { getNotes, createNote, deleteNote, pingBackend } from "../../services/api";
import { useAuth } from "../../context/AuthContext";
import { useRouter } from "expo-router";
import { useThemeColors } from "../../theme/useThemeColors";
import { Ionicons } from "@expo/vector-icons";
import { useFocusEffect } from "@react-navigation/native";
import { getLocalNotes, getAllUsers, getAllTags, getCurrentUser, getUserTags } from "../../database/localdb";

export default function HomeScreen() {
  const { apiKey, userId } = useAuth();
  const [notes, setNotes] = useState<any[]>([]);
  const [error, setError] = useState("");
  const [isOnline, setIsOnline] = useState<boolean | null>(null);
  const router = useRouter();
  const colors = useThemeColors();

  useFocusEffect(
    useCallback(() => {
      if (apiKey === null || userId === null) {
        setTimeout(() => {
          router.replace("/login");
        }, 0);
        return;
      }
      getNotes(apiKey ?? "", userId ?? 0)       //dodac petle 
        .then(setNotes)
        .catch(() => {
          setError("Błąd pobierania notatek");
        });
    }, [apiKey, userId])
  );

  useEffect(() => {
    let interval: ReturnType<typeof setInterval>;

    const checkStatus = async () => {
      const status = await pingBackend();
      setIsOnline(status);
    };

    checkStatus(); // sprawdź od razu po starcie

    interval = setInterval(checkStatus, 5000); // co 5 sekund

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    console.log("Użytkownicy:", getAllUsers());
    console.log("Tagi:", getAllTags());
    console.log("Notatki lokalne:", getLocalNotes(userId ?? 0));
  }, []);

  useEffect(() => {
    if (userId) {
      console.log("Aktualny użytkownik:", getCurrentUser(userId));
      console.log("Tagi użytkownika:", getUserTags(userId));
    }
  }, [userId]);

  // Funkcja do tworzenia pustej notatki i przejścia do jej szczegółów
  const handleCreateNote = async () => {
    try {
      const newNote = await createNote(apiKey ?? "", userId ?? 0, {
        title: "Nowa notatka",
        content: "",
      });
      // Odśwież listę notatek
      setNotes((prev) => [newNote, ...prev]);
      // Przejdź do szczegółów nowej notatki
      router.push(`/note/${newNote.id}`);
    } catch (e: any) {
      Alert.alert("Błąd", e?.message || "Nie udało się utworzyć notatki");
    }
  };

  // Funkcja do usuwania notatki
  const handleDeleteNote = async (noteId: number) => {
    Alert.alert(
      "Usuń notatkę",
      "Czy na pewno chcesz usunąć tę notatkę?",
      [
        { text: "Anuluj", style: "cancel" },
        {
          text: "Usuń",
          style: "destructive",
          onPress: async () => {
            try {
              await deleteNote(apiKey ?? "", userId ?? 0, noteId);
              setNotes((prev) => prev.filter((n) => n.id !== noteId));
            } catch (e: any) {
              Alert.alert("Błąd", e?.message || "Nie udało się usunąć notatki");
            }
          },
        },
      ]
    );
  };

  return (
    <View style={{ flex: 1 }}>
      <TouchableOpacity
        style={{
          position: "absolute",
          right: 24,
          bottom: 24,
          zIndex: 10,
          backgroundColor: colors.tint,
          borderRadius: 32,
          width: 56,
          height: 56,
          alignItems: "center",
          justifyContent: "center",
          elevation: 4,
        }}
        onPress={() => router.push("/note/new")}
        activeOpacity={0.8}
      >
        <Ionicons name="add" size={36} color="#fff" />
      </TouchableOpacity>
      <View style={[styles.container, { backgroundColor: colors.background }]}>
        <Text style={[styles.title, { color: colors.text }]}>
          Twoje notatki
        </Text>
        {error ? (
          <Text style={{ color: "red", marginBottom: 10 }}>{error}</Text>
        ) : null}
        <Text style={{ color: colors.text, textAlign: "center", marginBottom: 10 }}>
          Status połączenia z backendem:{" "}
          {isOnline === null
            ? "Sprawdzanie..."
            : isOnline
            ? "✅ Połączono"
            : "❌ Brak połączenia"}
        </Text>
        <FlatList
          data={notes}
          keyExtractor={(item) => item.id.toString()}
          renderItem={({ item }) => (
            <View
              style={[
                styles.note,
                { backgroundColor: colors.background, borderColor: colors.tabIconDefault, borderWidth: 1 },
              ]}
            >
              <TouchableOpacity
                onPress={() => router.push(`/note/${item.id}`)}
                style={{ flex: 1 }}
              >
                <Text style={[styles.noteTitle, { color: colors.text }]}>
                  {item.id}. {item.title}
                </Text>
                <Text style={[styles.noteContent, { color: colors.text }]} numberOfLines={2}>
                  {item.content}
                </Text>
              </TouchableOpacity>
              <View style={{ flexDirection: "row", justifyContent: "flex-end", marginTop: 8 }}>
                <TouchableOpacity onPress={() => handleDeleteNote(item.id)}>
                  <Ionicons name="trash-outline" size={22} color="#e53935" />
                </TouchableOpacity>
              </View>
            </View>
          )}
          ListEmptyComponent={
            <Text style={{ color: colors.icon, textAlign: "center", marginTop: 40 }}>
              Brak notatek do wyświetlenia.
            </Text>
          }
        />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    paddingTop: 40,
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 24,
    textAlign: "center",
  },
  note: {
    borderRadius: 10,
    padding: 16,
    marginBottom: 16,
    elevation: 2,
  },
  noteTitle: {
    fontSize: 18,
    fontWeight: "bold",
    marginBottom: 8,
  },
  noteContent: {
    fontSize: 15,
  },
});