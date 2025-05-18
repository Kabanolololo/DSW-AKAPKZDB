import React, { useState } from "react";
import { View, Text, TextInput, TouchableOpacity, StyleSheet } from "react-native";
import { useThemeColors } from "../theme/useThemeColors";
import { useRouter } from "expo-router";
import { API_URL } from "../constants/Api";

export default function RegisterScreen() {
  const [nick, setNick] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const colors = useThemeColors();
  const router = useRouter();

  const handleRegister = async () => {
    setError("");
    setSuccess("");
    if (!nick || !email || !password) {
      setError("Wszystkie pola są wymagane.");
      return;
    }
    try {
      const res = await fetch(`${API_URL}/users/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nick, email, password }),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        if (Array.isArray(data.detail) && data.detail.length > 0 && data.detail[0].msg) {
          setError(data.detail[0].msg);
        } else if (typeof data.detail === "string") {
          setError(data.detail);
        } else {
          setError("Błąd rejestracji");
        }
        return;
      }
      setSuccess("Rejestracja zakończona sukcesem! Możesz się zalogować.");
      setTimeout(() => router.replace("/login"), 1500);
    } catch {
      setError("Błąd połączenia z serwerem");
    }
  };

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      <Text style={[styles.title, { color: colors.text }]}>Rejestracja</Text>
      <TextInput
        placeholder="Nick"
        placeholderTextColor={colors.icon}
        value={nick}
        onChangeText={setNick}
        style={[
          styles.input,
          { backgroundColor: colors.background, borderColor: colors.tabIconDefault, color: colors.text },
        ]}
      />
      <TextInput
        placeholder="Email"
        placeholderTextColor={colors.icon}
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
        style={[
          styles.input,
          { backgroundColor: colors.background, borderColor: colors.tabIconDefault, color: colors.text },
        ]}
      />
      <View style={styles.passwordRow}>
        <TextInput
          placeholder="Hasło"
          placeholderTextColor={colors.icon}
          value={password}
          onChangeText={setPassword}
          secureTextEntry={!showPassword}
          style={[
            styles.input,
            { backgroundColor: colors.background, borderColor: colors.tabIconDefault, color: colors.text, flex: 1 },
          ]}
        />
        <TouchableOpacity onPress={() => setShowPassword((v) => !v)}>
          <Text style={{ color: colors.tint, marginLeft: 10, marginTop: 4 }}>
            {showPassword ? "Ukryj" : "Pokaż"}
          </Text>
        </TouchableOpacity>
      </View>
      <TouchableOpacity
        style={[styles.button, { backgroundColor: colors.tagBackground }]}
        onPress={handleRegister}
        activeOpacity={0.8}
      >
        <Text style={[styles.buttonText, { color: colors.tagText }]}>Zarejestruj</Text>
      </TouchableOpacity>
      {error ? <Text style={{ color: "red", marginTop: 10 }}>{error}</Text> : null}
      {success ? <Text style={{ color: colors.tint, marginTop: 10 }}>{success}</Text> : null}
      <TouchableOpacity onPress={() => router.replace("/login")}>
        <Text style={{ color: colors.tint, marginTop: 24, textAlign: "center" }}>
          Masz już konto? Zaloguj się
        </Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    padding: 24,
  },
  title: {
    fontSize: 24,
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
  passwordRow: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 16,
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