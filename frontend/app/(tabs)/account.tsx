import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, TextInput, Button, Alert, TouchableOpacity, ScrollView, Modal } from "react-native";
import { useAuth } from "../../context/AuthContext";
import { useThemeColors } from "../../theme/useThemeColors";
import { useRouter } from "expo-router";
import { API_URL } from "../../constants/Api";

export default function AccountScreen() {
  const { apiKey, userId, setApiKey, setUserId, logout } = useAuth();
  const colors = useThemeColors();
  const router = useRouter();

  const [user, setUser] = useState<any>(null);
  const [nick, setNick] = useState("");
  const [email, setEmail] = useState("");
  const [edit, setEdit] = useState(false);
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(true);
  const [showApiKey, setShowApiKey] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showPassword, setShowPassword] = useState(false); // <-- nowy stan

  useEffect(() => {
    if (!apiKey || !userId) return;
    setLoading(true);
    fetch(`${API_URL}/users/${userId}?api_key=${apiKey}`)
      .then(res => res.json())
      .then(data => {
        setUser(data);
        setNick(data.nick);
        setEmail(data.email);
      })
      .finally(() => setLoading(false));
  }, [apiKey, userId]);

  const handleEdit = async () => {
    if (!apiKey || !userId) return;
    const body: any = {};
    if (nick !== user.nick) body.nick = nick;
    if (email !== user.email) body.email = email;
    if (password) body.password = password;
    if (Object.keys(body).length === 0) {
      Alert.alert("Brak zmian", "Nie wprowadzono żadnych zmian.");
      return;
    }
    try {
      const res = await fetch(`${API_URL}/users/${userId}?api_key=${apiKey}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (!res.ok) throw new Error("Błąd edycji konta");
      Alert.alert("Sukces", "Dane konta zostały zaktualizowane.");
      setPassword("");
      setEdit(false);
      const updated = await res.json();
      setUser({ ...user, ...body });
    } catch {
      Alert.alert("Błąd", "Nie udało się zaktualizować konta.");
    }
  };

  const handleLogout = async () => {
    if (!apiKey) return;
    try {
      await fetch(`${API_URL}/logout/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ api_key: apiKey }),
      });
    } catch {}
    setApiKey(null);
    setUserId(null);
    router.replace("/login");
  };

  const handleDeleteAccount = async () => {
    if (!apiKey || !userId) return;
    setShowDeleteModal(false);
    try {
      const res = await fetch(`${API_URL}/users?user_id=${userId}&api_key=${apiKey}`, {
        method: "DELETE",
      });
      if (!res.ok) {
        const errText = await res.text();
        Alert.alert("Błąd usuwania konta", errText || "Nieznany błąd");
        return;
      }
      Alert.alert("Konto usunięte", "Twoje konto zostało usunięte.");
      setApiKey(null);
      setUserId(null);
      router.replace("/login");
    } catch (e) {
      Alert.alert("Błąd", "Nie udało się usunąć konta.");
    }
  };

  if (loading) {
    return (
      <View style={[styles.container, { backgroundColor: colors.background }]}>
        <Text style={{ color: colors.text }}>Ładowanie...</Text>
      </View>
    );
  }

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      <Text style={[styles.title, { color: colors.text }]}>Konto</Text>
      {/* API KEY */}
      <Text style={[styles.label, { color: colors.text }]}>API Key:</Text>
      <View style={styles.apiKeyRow}>
        <ScrollView
          horizontal
          showsHorizontalScrollIndicator
          style={{ flex: 1 }}
          contentContainerStyle={{ flexGrow: 1 }}
        >
          <TextInput
            style={[
              styles.apiKeyInput,
              { color: colors.text, borderColor: colors.tabIconDefault },
            ]}
            value={showApiKey ? (apiKey ?? "") : (apiKey ? apiKey.replace(/./g, "*") : "")}
            editable={false}
            secureTextEntry={false}
          />
        </ScrollView>
        <TouchableOpacity onPress={() => setShowApiKey((v) => !v)}>
          <Text style={{ color: colors.tint, marginLeft: 10 }}>
            {showApiKey ? "Ukryj" : "Pokaż"}
          </Text>
        </TouchableOpacity>
      </View>
      {/* --- reszta formularza --- */}
      <Text style={[styles.label, { color: colors.text }]}>Nick:</Text>
      <TextInput
        style={[styles.input, { color: colors.text, borderColor: colors.tabIconDefault }]}
        value={nick}
        editable={edit}
        onChangeText={setNick}
      />
      <Text style={[styles.label, { color: colors.text }]}>Email:</Text>
      <TextInput
        style={[styles.input, { color: colors.text, borderColor: colors.tabIconDefault }]}
        value={email}
        editable={edit}
        onChangeText={setEmail}
        keyboardType="email-address"
      />
      {edit && (
        <>
          <Text style={[styles.label, { color: colors.text }]}>Nowe hasło:</Text>
          <View style={styles.apiKeyRow}>
            <TextInput
              style={[styles.input, { color: colors.text, borderColor: colors.tabIconDefault, flex: 1 }]}
              value={password}
              onChangeText={setPassword}
              secureTextEntry={!showPassword}
              placeholder="Zostaw puste, jeśli nie zmieniasz"
              placeholderTextColor={colors.icon}
            />
            <TouchableOpacity onPress={() => setShowPassword((v) => !v)}>
              <Text style={{ color: colors.tint, marginLeft: 10 }}>
                {showPassword ? "Ukryj" : "Pokaż"}
              </Text>
            </TouchableOpacity>
          </View>
        </>
      )}
      <View style={styles.row}>
        <Button
          title={edit ? "Zapisz" : "Edytuj"}
          onPress={edit ? handleEdit : () => setEdit(true)}
          color={colors.tint}
        />
        {edit && (
          <Button
            title="Anuluj"
            onPress={() => {
              setEdit(false);
              setNick(user.nick);
              setEmail(user.email);
              setPassword("");
            }}
            color={colors.tint}
          />
        )}
        <Button
          title="Wyloguj"
          onPress={logout}
          color={colors.logout}
        />
      </View>
      <View style={styles.deleteRow}>
        <TouchableOpacity onPress={() => setShowDeleteModal(true)}>
          <Text style={{ color: "#e53935", marginTop: 32, fontWeight: "bold" }}>
            Usuń konto
          </Text>
        </TouchableOpacity>
      </View>
      {/* MODAL POTWIERDZENIA USUWANIA */}
      <Modal
        visible={showDeleteModal}
        transparent
        animationType="fade"
        onRequestClose={() => setShowDeleteModal(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={[styles.modalContent, { backgroundColor: colors.background }]}>
            <Text style={{ color: colors.text, fontSize: 18, marginBottom: 16, textAlign: "center" }}>
              Czy na pewno chcesz usunąć konto? Tej operacji nie można cofnąć.
            </Text>
            <Button title="Potwierdź" onPress={handleDeleteAccount} color="#e53935" />
            <Button title="Anuluj" onPress={() => setShowDeleteModal(false)} color={colors.tint} />
          </View>
        </View>
      </Modal>
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
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 24,
    textAlign: "center",
  },
  label: {
    fontSize: 16,
    marginTop: 8,
    marginBottom: 4,
  },
  input: {
    borderWidth: 1,
    borderRadius: 8,
    padding: 10,
    marginBottom: 8,
    fontSize: 16,
  },
  apiKeyRow: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 8,
  },
  apiKeyInput: {
    flex: 1,
    borderWidth: 1,
    borderRadius: 8,
    padding: 10,
    fontSize: 16,
    letterSpacing: 2,
    backgroundColor: "transparent",
  },
  row: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginTop: 24,
    gap: 10,
  },
  deleteRow: {
    alignItems: "center",
    marginTop: 16,
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: "rgba(0,0,0,0.4)",
    justifyContent: "center",
    alignItems: "center",
  },
  modalContent: {
    width: "85%",
    borderRadius: 12,
    padding: 24,
    elevation: 4,
  },
});