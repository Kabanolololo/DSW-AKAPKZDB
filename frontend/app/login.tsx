import React, { useState } from "react";
import { View, TextInput, Text, StyleSheet, TouchableOpacity } from "react-native";
import { login } from "../services/api";
import { useAuth } from "../context/AuthContext";
import { useRouter } from "expo-router";
import { useThemeColors } from "../theme/useThemeColors";

export default function LoginScreen() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const { setApiKey, setUserId } = useAuth();
  const router = useRouter();
  const colors = useThemeColors();

  const handleLogin = async () => {
    try {
      const data = await login(email.trim().toLowerCase(), password);
      setApiKey(data.api_key);
      setUserId(data.user.id);
      router.replace("/");
    } catch (e) {
      setError("Nieprawidłowe dane logowania");
    }
  };

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      <Text style={[styles.title, { color: colors.text }]}>
        Logowanie
      </Text>
      <TextInput
        placeholder="Email"
        placeholderTextColor={colors.icon}
        value={email}
        onChangeText={setEmail}
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
        onPress={handleLogin}
        activeOpacity={0.8}
      >
        <Text style={[styles.buttonText, { color: colors.tagText }]}>Zaloguj</Text>
      </TouchableOpacity>
      {error ? (
        <Text style={{ color: "red", marginTop: 10 }}>{error}</Text>
      ) : null}
      <TouchableOpacity onPress={() => router.replace("/register")}>
        <Text style={{ color: colors.tint, marginTop: 24, textAlign: "center" }}>
          Nie masz konta? Zarejestruj się
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