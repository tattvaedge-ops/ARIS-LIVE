// C:\AGENTIC AI- ARIS\aris-mobile\app\home.tsx

import React, { useEffect, useRef, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Image,
  TouchableOpacity,
  ScrollView,
  TextInput,
  StatusBar,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';
import { sendMessage } from '../services/api';

const COLORS = {
  background: '#0a192f',
  card: '#10213f',
  primary: '#f97316',
  primaryText: '#0a192f',
  text: '#ffffff',
  textSecondary: '#d1d5db',
  border: 'rgba(255,255,255,0.08)',
  userBubble: '#f97316',
  assistantBubble: '#10213f',
};

type ChatMessage = {
  id: string;
  role: 'user' | 'assistant';
  content: string;
};

export default function HomeScreen() {
  const [userName, setUserName] = useState('User');
  const [tokens, setTokens] = useState(0);
  const [message, setMessage] = useState('');
  const [sending, setSending] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const scrollViewRef = useRef<ScrollView>(null);

  useEffect(() => {
    loadUserData();
  }, []);

  useEffect(() => {
    setTimeout(() => {
      scrollViewRef.current?.scrollToEnd({ animated: true });
    }, 100);
  }, [messages, sending]);

  const loadUserData = async () => {
    try {
      const storedName = await AsyncStorage.getItem('user_name');
      const storedTokens = await AsyncStorage.getItem('user_tokens');

      if (storedName) setUserName(storedName);
      if (storedTokens) setTokens(parseInt(storedTokens, 10));
    } catch (error) {
      console.log('Error loading user data:', error);
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

  const addMessage = (
    role: 'user' | 'assistant',
    content: string
  ) => {
    setMessages((prev) => [
      ...prev,
      {
        id: Date.now().toString() + Math.random(),
        role,
        content,
      },
    ]);
  };

  const handleSendMessage = async () => {
    const trimmed = message.trim();

    if (!trimmed || sending) {
      return;
    }

    try {
      setSending(true);

      const authToken = await AsyncStorage.getItem('auth_token');

      if (!authToken) {
        router.replace('/login');
        return;
      }

      addMessage('user', trimmed);
      setMessage('');

      const result = await sendMessage(trimmed, authToken);

      addMessage(
        'assistant',
        result.reply || 'No response received.'
      );

      if (typeof result.tokens_left === 'number') {
        setTokens(result.tokens_left);
        await AsyncStorage.setItem(
          'user_tokens',
          String(result.tokens_left)
        );
      }
    } catch (error: any) {
      addMessage(
        'assistant',
        error.message || 'ARIS server error.'
      );
    } finally {
      setSending(false);
    }
  };

  const quickPrompts = [
    'Explain Quantum Physics',
    'Create a Study Plan',
    'Generate an Image',
    'Analyze My Business',
  ];

  const handleQuickPrompt = (prompt: string) => {
    setMessage(prompt);
  };

  const modes = [
    { title: 'Student AI', icon: 'school-outline' },
    { title: 'Professional AI', icon: 'briefcase-outline' },
    { title: 'Research AI', icon: 'flask-outline' },
    { title: 'Creator AI', icon: 'color-palette-outline' },
    { title: 'Life AI', icon: 'heart-outline' },
  ];

  const showWelcome = messages.length === 0;

  return (
    <SafeAreaView
      style={styles.container}
      edges={['top', 'left', 'right']}
    >
      <StatusBar
        barStyle="light-content"
        backgroundColor={COLORS.background}
      />

      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={
          Platform.OS === 'ios' ? 'padding' : undefined
        }
      >
        {/* Header */}
        <View style={styles.header}>
          <Image
            source={require('../assets/images/aris-logo.png')}
            style={styles.logo}
            resizeMode="contain"
          />

          <View style={styles.headerRight}>
            <View style={styles.tokenBadge}>
              <Text style={styles.tokenText}>
                🧠 {tokens.toLocaleString()}
              </Text>
            </View>

            <TouchableOpacity
              style={styles.logoutButton}
              onPress={handleLogout}
            >
              <Ionicons
                name="log-out-outline"
                size={22}
                color="#ffffff"
              />
            </TouchableOpacity>
          </View>
        </View>

        {/* Chat Area */}
        <ScrollView
          ref={scrollViewRef}
          style={styles.chatArea}
          contentContainerStyle={styles.chatContent}
          showsVerticalScrollIndicator={false}
        >
          {showWelcome && (
            <>
              <Text style={styles.greeting}>
                Hello, {userName}
              </Text>

              <Text style={styles.subtitle}>
                This is ARIS Intelligence. What would you like to do today?
              </Text>

              {/* AI Modes */}
              <Text style={styles.sectionTitle}>
                AI Modes
              </Text>

              <View style={styles.grid}>
                {modes.map((mode, index) => (
                  <TouchableOpacity
                    key={index}
                    style={styles.card}
                  >
                    <Ionicons
                      name={mode.icon as any}
                      size={28}
                      color={COLORS.primary}
                    />
                    <Text style={styles.cardText}>
                      {mode.title}
                    </Text>
                  </TouchableOpacity>
                ))}
              </View>

              {/* Quick Prompts */}
              <Text style={styles.sectionTitle}>
                Quick Prompts
              </Text>

              <View style={styles.promptContainer}>
                {quickPrompts.map((prompt, index) => (
                  <TouchableOpacity
                    key={index}
                    style={styles.promptChip}
                    onPress={() =>
                      handleQuickPrompt(prompt)
                    }
                  >
                    <Text style={styles.promptText}>
                      {prompt}
                    </Text>
                  </TouchableOpacity>
                ))}
              </View>
            </>
          )}

          {/* Messages */}
          {messages.map((msg) => (
            <View
              key={msg.id}
              style={[
                styles.messageRow,
                msg.role === 'user'
                  ? styles.userRow
                  : styles.assistantRow,
              ]}
            >
              <View
                style={[
                  styles.messageBubble,
                  msg.role === 'user'
                    ? styles.userBubble
                    : styles.assistantBubble,
                ]}
              >
                <Text
                  style={[
                    styles.messageText,
                    msg.role === 'user'
                      ? styles.userMessageText
                      : styles.assistantMessageText,
                  ]}
                >
                  {msg.content}
                </Text>
              </View>
            </View>
          ))}

          {/* Typing Indicator */}
          {sending && (
            <View
              style={[
                styles.messageRow,
                styles.assistantRow,
              ]}
            >
              <View
                style={[
                  styles.messageBubble,
                  styles.assistantBubble,
                ]}
              >
                <ActivityIndicator
                  size="small"
                  color={COLORS.primary}
                />
              </View>
            </View>
          )}
        </ScrollView>

        {/* Bottom Input */}
        <SafeAreaView
          edges={['bottom']}
          style={styles.bottomSafeArea}
        >
          <View style={styles.inputContainer}>
            <TouchableOpacity
              style={styles.attachButton}
            >
              <Text style={styles.attachText}>📎</Text>
            </TouchableOpacity>

            <TextInput
              placeholder="Talk to ARIS..."
              placeholderTextColor="#9CA3AF"
              style={styles.input}
              value={message}
              onChangeText={setMessage}
              multiline
              editable={!sending}
            />

            <TouchableOpacity
              style={styles.sendButton}
              onPress={handleSendMessage}
              disabled={sending}
            >
              <Ionicons
                name="send"
                size={20}
                color={COLORS.primaryText}
              />
            </TouchableOpacity>
          </View>
        </SafeAreaView>
      </KeyboardAvoidingView>
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
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingTop: 10,
    paddingBottom: 10,
  },

  logo: {
    width: 180,
    height: 42,
  },

  headerRight: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },

  tokenBadge: {
    backgroundColor: COLORS.primary,
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 12,
  },

  tokenText: {
    color: COLORS.primaryText,
    fontWeight: '700',
    fontSize: 14,
  },

  logoutButton: {
    width: 42,
    height: 42,
    borderRadius: 12,
    backgroundColor: 'rgba(255,255,255,0.08)',
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: COLORS.border,
  },

  chatArea: {
    flex: 1,
  },

  chatContent: {
    paddingHorizontal: 20,
    paddingBottom: 20,
  },

  greeting: {
    fontSize: 34,
    fontWeight: '700',
    color: COLORS.text,
    marginTop: 20,
  },

  subtitle: {
    marginTop: 8,
    color: COLORS.textSecondary,
    fontSize: 16,
    lineHeight: 24,
  },

  sectionTitle: {
    marginTop: 28,
    marginBottom: 16,
    color: COLORS.text,
    fontSize: 24,
    fontWeight: '700',
  },

  grid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },

  card: {
    width: '48%',
    backgroundColor: COLORS.card,
    borderRadius: 22,
    padding: 20,
    marginBottom: 16,
    minHeight: 125,
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: COLORS.border,
  },

  cardText: {
    marginTop: 14,
    color: COLORS.text,
    fontSize: 16,
    fontWeight: '600',
  },

  promptContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 10,
    marginBottom: 20,
  },

  promptChip: {
    backgroundColor: COLORS.card,
    borderRadius: 20,
    paddingHorizontal: 14,
    paddingVertical: 10,
    borderWidth: 1,
    borderColor: COLORS.border,
  },

  promptText: {
    color: COLORS.text,
    fontSize: 14,
  },

  messageRow: {
    marginBottom: 12,
  },

  userRow: {
    alignItems: 'flex-end',
  },

  assistantRow: {
    alignItems: 'flex-start',
  },

  messageBubble: {
    maxWidth: '85%',
    borderRadius: 18,
    paddingHorizontal: 16,
    paddingVertical: 12,
  },

  userBubble: {
    backgroundColor: COLORS.userBubble,
    borderBottomRightRadius: 6,
  },

  assistantBubble: {
    backgroundColor: COLORS.assistantBubble,
    borderBottomLeftRadius: 6,
    borderWidth: 1,
    borderColor: COLORS.border,
  },

  messageText: {
    fontSize: 15,
    lineHeight: 22,
  },

  userMessageText: {
    color: COLORS.primaryText,
    fontWeight: '500',
  },

  assistantMessageText: {
    color: COLORS.text,
  },

  bottomSafeArea: {
    backgroundColor: COLORS.background,
  },

  inputContainer: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    paddingHorizontal: 14,
    paddingTop: 12,
    paddingBottom: 12,
    borderTopWidth: 1,
    borderTopColor: COLORS.border,
    backgroundColor: COLORS.background,
    gap: 8,
  },

  attachButton: {
    width: 46,
    height: 46,
    borderRadius: 12,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
  },

  attachText: {
    fontSize: 20,
  },

  input: {
    flex: 1,
    backgroundColor: '#ffffff',
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 12,
    fontSize: 16,
    color: '#111827',
    maxHeight: 120,
  },

  sendButton: {
    width: 46,
    height: 46,
    borderRadius: 12,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
  },
});