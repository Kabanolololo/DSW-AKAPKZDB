import React, { useEffect, useState } from "react";
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert, useColorScheme } from "react-native";
import { useLocalSearchParams, useRouter } from "expo-router";
import { useAuth } from "../../../context/AuthContext";
import { useThemeColors } from "../../../theme/useThemeColors";
import { getNote, createNote, getTagsForNote, createTag, updateTag, deleteTag } from "../../../services/api";
import { API_URL } from "../../../constants/Api";
import { Ionicons } from "@expo/vector-icons"; // <-- DODAJ TEN IMPORT
import { useFocusEffect } from "@react-navigation/native";

export default function NoteDetailsScreen() {
  const { id, edit } = useLocalSearchParams();
  const { apiKey, userId } = useAuth();
  const colors = useThemeColors();
  const router = useRouter();
  const colorScheme = useColorScheme();

  const [note, setNote] = useState<any>(null);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [isEdit, setIsEdit] = useState(edit === "1");
  const [tags, setTags] = useState<any[]>([]);
  const [newTag, setNewTag] = useState("");
  const [editTagId, setEditTagId] = useState<number | null>(null);
  const [editTagName, setEditTagName] = useState("");

  useFocusEffect(
    React.useCallback(() => {
      if (!apiKey || !userId || !id) return;
      getNote(apiKey ?? "", Number(id), userId ?? 0)
        .then((data) => {
          setNote(data);
          setTitle(data.title);
          setContent(data.content);
        })
        .catch(() => {
          Alert.alert("Błąd", "Nie udało się pobrać notatki");
          router.back();
        });
      // pobierz tagi jeśli trzeba
      getTagsForNote(apiKey ?? "", Number(id), userId ?? 0).then(setTags);
    }, [apiKey, userId, id])
  );

  const handleSave = async () => {
    try {
      const res = await fetch(
        `${API_URL}/notes/${id}?user_id=${userId}&api_key=${apiKey}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ title, content }),
        }
      );
      if (!res.ok) {
        const err = await res.text();
        throw new Error(err || "Błąd edycji notatki");
      }
      const updated = await res.json();
      setNote(updated);
      setIsEdit(false);
      Alert.alert("Sukces", "Notatka zaktualizowana");
      router.replace("/"); // wróć na główną i odśwież listę
    } catch (e: any) {
      Alert.alert("Błąd", e?.message || "Nie udało się zapisać zmian");
    }
  };

  const handleAddTag = async () => {
    if (!newTag.trim()) return;
    try {
      const tag = await createTag(apiKey ?? "", userId ?? 0, Number(id), newTag.trim()); // <--- poprawka: apiKey ?? "", userId ?? 0
      setTags((prev) => [...prev, tag]);
      setNewTag("");
    } catch (e: any) {
      Alert.alert("Błąd", e?.message || "Nie udało się dodać tagu");
    }
  };

  const handleEditTag = async () => {
    if (!editTagName.trim() || editTagId === null) return;
    try {
      await updateTag(apiKey ?? "", userId ?? 0, editTagId, editTagName.trim());
      setTags((prev) =>
        prev.map((t) => (t.id === editTagId ? { ...t, name: editTagName.trim() } : t))
      );
      setEditTagId(null);
      setEditTagName("");
    } catch (e: any) {
      Alert.alert("Błąd", e?.message || "Nie udało się edytować tagu");
    }
  };

  const handleDeleteTag = async (tagId: number) => {
    try {
      await deleteTag(apiKey ?? "", userId ?? 0, tagId);
      setTags((prev) => prev.filter((t) => t.id !== tagId));
    } catch (e: any) {
      Alert.alert("Błąd", e?.message || "Nie udało się usunąć tagu");
    }
  };

  if (!note) {
    return (
      <View style={[styles.container, { backgroundColor: colors.background }]}>
        <Text style={{ color: colors.text }}>Ładowanie...</Text>
      </View>
    );
  }

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      {isEdit ? (
        <>
          <TextInput
            style={[styles.titleInput, { color: colors.text, borderColor: colors.tabIconDefault }]}
            value={title}
            onChangeText={setTitle}
          />
          <TextInput
            style={[styles.contentInput, { color: colors.text, borderColor: colors.tabIconDefault }]}
            value={content}
            onChangeText={setContent}
            multiline
          />
          <TouchableOpacity style={[styles.button, { backgroundColor: colors.tint }]} onPress={handleSave}>
            <Text style={{ color: "#fff", fontWeight: "bold" }}>Zapisz</Text>
          </TouchableOpacity>
          <TouchableOpacity onPress={() => setIsEdit(false)}>
            <Text style={{ color: colors.tint, marginTop: 16, textAlign: "center" }}>Anuluj</Text>
          </TouchableOpacity>
        </>
      ) : (
        <>
          <Text style={[styles.title, { color: colors.text }]}>{note.title}</Text>
          <Text style={[styles.content, { color: colors.text }]}>{note.content}</Text>
          {!isEdit && (
            <TouchableOpacity
              style={[styles.button, { backgroundColor: colors.tint, marginTop: 24 }]}
              onPress={() => setIsEdit(true)}
            >
              <Text style={{ color: "#fff", fontWeight: "bold" }}>Edytuj</Text>
            </TouchableOpacity>
          )}
          <Text style={{ color: colors.text, marginTop: 24, fontWeight: "bold" }}>Tagi:</Text>
          <View style={{ flexDirection: "row", flexWrap: "wrap", marginTop: 8 }}>
            {tags.map((tag) =>
              <View
                key={tag.id}
                style={{
                  backgroundColor: colors.tagBackground,
                  borderRadius: 8,
                  paddingHorizontal: 12,
                  paddingVertical: 8,
                  marginRight: 12,
                  marginBottom: 12,
                  minWidth: 90,
                  alignItems: "center",
                }}
              >
                {editTagId === tag.id ? (
                  <>
                    <TextInput
                      value={editTagName}
                      onChangeText={setEditTagName}
                      style={{
                        borderWidth: 1,
                        borderColor: colors.tabIconDefault,
                        color: colors.text,
                        backgroundColor: colors.background,
                        borderRadius: 8,
                        padding: 4,
                        minWidth: 60,
                        marginBottom: 6,
                        textAlign: "center",
                      }}
                    />
                    <View style={{ flexDirection: "row", width: "100%", justifyContent: "space-between" }}>
                      <TouchableOpacity onPress={handleEditTag}>
                        <Text
                          style={{
                            color: colors.tagTextmodify,
                            fontWeight: "bold",
                          }}
                        >
                          Zapisz
                        </Text>
                      </TouchableOpacity>
                      <TouchableOpacity onPress={() => { setEditTagId(null); setEditTagName(""); }}>
                        <Text
                          style={{
                            color: colors.tagTextmodify,
                            fontWeight: "bold",
                          }}
                        >
                          Anuluj
                        </Text>
                      </TouchableOpacity>
                    </View>
                  </>
                ) : (
                  <>
                    <Text style={{ color: colors.tagText, fontWeight: "bold", marginBottom: 6, textAlign: "center" }}>
                      {tag.name}
                    </Text>
                    <View style={{ flexDirection: "row", width: "100%", justifyContent: "space-between" }}>
                      <TouchableOpacity
                        onPress={() => { setEditTagId(tag.id); setEditTagName(tag.name); }}
                        style={{
                          backgroundColor: colors.buttonBackground,
                          borderRadius: 6,
                          padding: 2,
                        }}
                      >
                        <Ionicons
                          name="ellipsis-horizontal-circle-sharp"
                          size={22}
                          color={colors.buttonText}
                        />
                      </TouchableOpacity>
                      <TouchableOpacity
                        onPress={() => handleDeleteTag(tag.id)}
                        style={{
                          backgroundColor: colors.buttonBackground,
                          borderRadius: 6,
                          padding: 2,
                        }}
                      >
                        <Ionicons
                          name="close-circle"
                          size={22}
                          color="#e53935"
                        />
                      </TouchableOpacity>
                    </View>
                  </>
                )}
              </View>
            )}
          </View>
          <View style={{ flexDirection: "row", alignItems: "center", marginTop: 8 }}>
            <TextInput
              value={newTag}
              onChangeText={setNewTag}
              placeholder="Dodaj tag"
              placeholderTextColor={colors.icon}
              style={{
                borderWidth: 1,
                borderColor: colors.tabIconDefault,
                color: colors.text,
                backgroundColor: colors.background,
                borderRadius: 8,
                padding: 8,
                minWidth: 100,
                marginRight: 8,
              }}
            />
            <TouchableOpacity onPress={handleAddTag}>
              <Ionicons name="add-circle-outline" size={24} color={colors.tint} />
            </TouchableOpacity>
          </View>
        </>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 24 },
  title: { 
    fontSize: 22, 
    fontWeight: "bold", 
    marginBottom: 16, 
    textAlign: "center" // <-- dodaj to
  },
  content: { fontSize: 16 },
  titleInput: {
    borderWidth: 1,
    borderRadius: 8,
    padding: 10,
    fontSize: 20,
    fontWeight: "bold",
    marginBottom: 16,
  },
  contentInput: {
    borderWidth: 1,
    borderRadius: 8,
    padding: 10,
    fontSize: 16,
    minHeight: 120,
    textAlignVertical: "top",
    marginBottom: 16,
  },
  button: {
    borderRadius: 8,
    paddingVertical: 14,
    alignItems: "center",
    marginTop: 8,
  },
});