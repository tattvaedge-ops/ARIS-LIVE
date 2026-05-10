// C:\AGENTIC AI- ARIS\aris-mobile\app\profile.tsx

import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  StatusBar,
  ScrollView,
  Linking,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';

const COLORS = {
  background: '#0a192f',
  card: '#10213f',
  primary: '#f97316',
  primaryText: '#0a192f',
  text: '#ffffff',
  textSecondary: '#d1d5db',
  border: 'rgba(255,255,255,0.08)',
};

export default function ProfileScreen() {
  const [userName, setUserName] = useState('User');
  const [userEmail, setUserEmail] = useState('');
  const [tokens, setTokens] = useState(0);

  useEffect(() => {
    loadUserData();
  }, []);

  const loadUserData = async () => {
    try {
      const storedName =
        await AsyncStorage.getItem('user_name');
      const storedEmail =
        await AsyncStorage.getItem('user_email');
      const storedTokens =
        await AsyncStorage.getItem('user_tokens');

      if (storedName) setUserName(storedName);
      if (storedEmail) setUserEmail(storedEmail);
      if (storedTokens) {
        setTokens(parseInt(storedTokens, 10));
      }
    } catch (error) {
      console.log('Profile load error:', error);
    }
  };

  const handleBuyTokens = async () => {
    try {
      await Linking.openURL(
        'https://aris-live-production.up.railway.app/buy_tokens'
      );
    } catch (error) {
      console.log('Unable to open buy tokens page.');
    }
  };

  const handleLogout = async () => {
    try {
      await AsyncStorage.multiRemove([
        'auth_token',
        'user_name',
        'user_email',
        'user_tokens',
      ]);

      router.replace('/login');
    } catch (error) {
      console.log('Logout error:', error);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar
        barStyle="light-content"
        backgroundColor={COLORS.background}
      />

      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.iconButton}
          onPress={() => router.back()}
        >
          <Ionicons
            name="arrow-back"
            size={22}
            color="#ffffff"
          />
        </TouchableOpacity>

        <Text style={styles.headerTitle}>
          Profile
        </Text>

        <View style={styles.iconButtonPlaceholder} />
      </View>

      <ScrollView
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        {/* Profile Card */}
        <View style={styles.profileCard}>
          <View style={styles.avatar}>
            <Text style={styles.avatarText}>
              {userName.charAt(0).toUpperCase()}
            </Text>
          </View>

          <Text style={styles.userName}>
            {userName}
          </Text>

          <Text style={styles.userEmail}>
            {userEmail}
          </Text>

          <View style={styles.tokenBadge}>
            <Text style={styles.tokenText}>
              🧠 {tokens.toLocaleString()} Tokens
            </Text>
          </View>
        </View>

        {/* Actions */}
        <TouchableOpacity
          style={styles.actionCard}
          onPress={handleBuyTokens}
        >
          <Ionicons
            name="wallet-outline"
            size={24}
            color={COLORS.primary}
          />
          <Text style={styles.actionText}>
            Buy Tokens
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.actionCard}
          onPress={handleLogout}
        >
          <Ionicons
            name="log-out-outline"
            size={24}
            color="#ef4444"
          />
          <Text style={styles.actionText}>
            Logout
          </Text>
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },

  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingTop: 10,
    paddingBottom: 10,
  },

  headerTitle: {
    fontSize: 24,
    fontWeight: '700',
    color: COLORS.text,
  },

  iconButton: {
    width: 42,
    height: 42,
    borderRadius: 12,
    backgroundColor: 'rgba(255,255,255,0.08)',
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: COLORS.border,
  },

  iconButtonPlaceholder: {
    width: 42,
    height: 42,
  },

  content: {
    paddingHorizontal: 20,
    paddingBottom: 30,
  },

  profileCard: {
    backgroundColor: COLORS.card,
    borderRadius: 24,
    padding: 28,
    alignItems: 'center',
    marginTop: 10,
    marginBottom: 24,
    borderWidth: 1,
    borderColor: COLORS.border,
  },

  avatar: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
  },

  avatarText: {
    fontSize: 32,
    fontWeight: '700',
    color: COLORS.primaryText,
  },

  userName: {
    fontSize: 24,
    fontWeight: '700',
    color: COLORS.text,
    marginBottom: 6,
  },

  userEmail: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginBottom: 18,
  },

  tokenBadge: {
    backgroundColor: COLORS.primary,
    paddingHorizontal: 18,
    paddingVertical: 10,
    borderRadius: 14,
  },

  tokenText: {
    color: COLORS.primaryText,
    fontWeight: '700',
    fontSize: 14,
  },

  actionCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.card,
    borderRadius: 18,
    padding: 18,
    marginBottom: 14,
    borderWidth: 1,
    borderColor: COLORS.border,
  },

  actionText: {
    marginLeft: 14,
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
  },
});