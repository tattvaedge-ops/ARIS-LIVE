import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
  ActivityIndicator,
  Image,
  StatusBar,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { router } from 'expo-router';
import { loginUser, signupUser } from '../services/api';

const COLORS = {
  background: '#0a192f',
  card: '#10213f',
  primary: '#f97316',
  primaryText: '#0a192f',
  text: '#ffffff',
  textSecondary: '#d1d5db',
  border: 'rgba(255,255,255,0.08)',
};

export default function LoginScreen() {
  const [mode, setMode] = useState<'login' | 'signup'>('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
  if (!email.trim() || !password.trim()) {
    Alert.alert('Validation', 'Please enter email and password.');
    return;
  }

  try {
    setLoading(true);

    const data =
      mode === 'login'
        ? await loginUser(email.trim(), password)
        : await signupUser(email.trim(), password);

    // Save auth data
    await AsyncStorage.setItem('auth_token', data.token);
    await AsyncStorage.setItem('user_name', data.user.name);
    await AsyncStorage.setItem('user_email', data.user.email);
    await AsyncStorage.setItem(
      'user_tokens',
      String(data.user.tokens)
    );

    // Navigate to home
    router.replace('/home');
  } catch (error: any) {
    Alert.alert(
      mode === 'login' ? 'Login Failed' : 'Signup Failed',
      error.message || 'Request failed.'
    );
  } finally {
    setLoading(false);
  }
};

  const handleForgotPassword = () => {
    Alert.alert(
      'Forgot Password',
      'Password reset functionality will be added next.'
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar
        barStyle="light-content"
        backgroundColor={COLORS.background}
      />

      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      >
        <ScrollView
          contentContainerStyle={styles.content}
          keyboardShouldPersistTaps="handled"
        >
          <Image
            source={require('../assets/images/aris-logo.png')}
            style={styles.logo}
            resizeMode="contain"
          />

          <Text style={styles.title}>ARIS Intelligence</Text>
          <Text style={styles.subtitle}>
            Your AI Brain for Life · Study · Business
          </Text>

          <View style={styles.card}>
            <TextInput
              placeholder="Email"
              placeholderTextColor="#9CA3AF"
              style={styles.input}
              autoCapitalize="none"
              keyboardType="email-address"
              value={email}
              onChangeText={setEmail}
            />

            <TextInput
              placeholder="Password"
              placeholderTextColor="#9CA3AF"
              style={styles.input}
              secureTextEntry
              value={password}
              onChangeText={setPassword}
            />

            <TouchableOpacity
              style={styles.loginButton}
              onPress={handleSubmit}
              disabled={loading}
            >
              {loading ? (
                <ActivityIndicator color={COLORS.primaryText} />
              ) : (
                <Text style={styles.loginText}>
                  {mode === 'login' ? 'Login' : 'Create Account'}
                </Text>
              )}
            </TouchableOpacity>

            <View style={styles.secondaryActions}>
              <TouchableOpacity
                onPress={() =>
                  setMode(mode === 'login' ? 'signup' : 'login')
                }
              >
                <Text style={styles.secondaryText}>
                  {mode === 'login'
                    ? 'Create Account'
                    : 'Back to Login'}
                </Text>
              </TouchableOpacity>

              {mode === 'login' && (
                <TouchableOpacity
                  onPress={handleForgotPassword}
                >
                  <Text style={styles.secondaryText}>
                    Forgot Password?
                  </Text>
                </TouchableOpacity>
              )}
            </View>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },

  content: {
    flexGrow: 1,
    justifyContent: 'center',
    paddingHorizontal: 24,
  },

  logo: {
    width: 220,
    height: 70,
    alignSelf: 'center',
    marginBottom: 24,
  },

  title: {
    fontSize: 28,
    fontWeight: '700',
    color: COLORS.text,
    textAlign: 'center',
  },

  subtitle: {
    fontSize: 15,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginTop: 8,
    marginBottom: 32,
  },

  card: {
    backgroundColor: COLORS.card,
    borderRadius: 20,
    padding: 24,
    borderWidth: 1,
    borderColor: COLORS.border,
  },

  input: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 14,
    fontSize: 16,
    color: '#111827',
    marginBottom: 16,
  },

  loginButton: {
    backgroundColor: COLORS.primary,
    borderRadius: 12,
    paddingVertical: 14,
    alignItems: 'center',
  },

  loginText: {
    color: COLORS.primaryText,
    fontSize: 16,
    fontWeight: '700',
  },

  secondaryActions: {
    marginTop: 18,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },

  secondaryText: {
    color: COLORS.primary,
    fontSize: 14,
    fontWeight: '600',
  },
});