import Markdown from 'react-native-markdown-display';
import React, { useEffect, useRef, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  TextInput,
  StatusBar,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  Image,
  Linking,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';
import * as ImagePicker from 'expo-image-picker';
import {
  sendMessage,
  uploadImage,
} from '../services/api';

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

export type WorkspaceTool = {
  title: string;
  icon: string;
  starterQuestion: string;
};

type ChatAction = {
  label: string;
  action: 'camera' | 'gallery';
};

type ChatMessage = {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  imageUrl?: string;
  actions?: ChatAction[];
};

type Props = {
  title: string;
  subtitle: string;
  tools: WorkspaceTool[];
};

export default function WorkspaceScreen({
  title,
  subtitle,
  tools,
}: Props) {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [sending, setSending] = useState(false);
  const [tokens, setTokens] = useState(0);

  const scrollViewRef = useRef<ScrollView>(null);

  useEffect(() => {
    loadTokens();
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      scrollViewRef.current?.scrollToEnd({
        animated: true,
      });
    }, 100);

    return () => clearTimeout(timer);
  }, [messages, sending]);

  const loadTokens = async () => {
    try {
      const storedTokens = await AsyncStorage.getItem(
        'user_tokens'
      );

      if (storedTokens) {
        setTokens(parseInt(storedTokens, 10));
      }
    } catch (error) {
      console.log('Token load error:', error);
    }
  };

  const addMessage = (
    role: 'user' | 'assistant',
    content: string,
    imageUrl?: string,
    actions?: ChatAction[]
  ) => {
    setMessages((prev) => [
      ...prev,
      {
        id:
          Date.now().toString() +
          Math.random().toString(),
        role,
        content,
        imageUrl,
        actions,
      },
    ]);
  };

  const handleToolPress = async (
    tool: WorkspaceTool
  ) => {
    const isAskDoubt =
      tool.title.trim().toLowerCase() ===
      'ask doubt';

    if (isAskDoubt) {
      addMessage(
        'assistant',
        '📷 Choose how you would like to upload your question:',
        undefined,
        [
          {
            label: '📷 Take Photo',
            action: 'camera',
          },
          {
            label:
              '🖼️ Choose from Gallery',
            action: 'gallery',
          },
        ]
      );
      return;
    }

    addMessage(
      'assistant',
      tool.starterQuestion
    );
  };

  const handleBackPress = () => {
    if (messages.length > 0) {
      setMessages([]);
      setMessage('');
      return;
    }

    router.back();
  };

  const analyzeImage = async (
    imageUri: string
  ) => {
    try {
      setSending(true);

      const authToken =
        await AsyncStorage.getItem(
          'auth_token'
        );

      if (!authToken) {
        router.replace('/login');
        return;
      }

      const result = await uploadImage(
        imageUri,
        authToken
      );

      addMessage(
        'assistant',
        result.reply ||
          'Question analyzed successfully.'
      );

      if (
        typeof result.tokens_left ===
        'number'
      ) {
        setTokens(result.tokens_left);

        await AsyncStorage.setItem(
          'user_tokens',
          String(result.tokens_left)
        );
      }
    } catch (error: any) {
      addMessage(
        'assistant',
        error.message ||
          'Image analysis failed.'
      );
    } finally {
      setSending(false);
    }
  };

  const handleTakePhoto = async () => {
    try {
      const permission =
        await ImagePicker.requestCameraPermissionsAsync();

      if (!permission.granted) {
        addMessage(
          'assistant',
          '⚠️ Please grant camera access.'
        );
        return;
      }

      const result =
        await ImagePicker.launchCameraAsync({
          mediaTypes: ['images'],
          allowsEditing: true,
          aspect: [4, 3],
          quality: 1,
        });

      if (
        result.canceled ||
        !result.assets ||
        result.assets.length === 0
      ) {
        return;
      }

      const imageUri =
        result.assets[0].uri;

      addMessage(
        'assistant',
        '📷 Uploading and analyzing your question...',
        imageUri
      );

      await analyzeImage(imageUri);
    } catch (error) {
      addMessage(
        'assistant',
        '⚠️ Unable to open camera.'
      );
    }
  };

  const handlePickImage = async () => {
    try {
      const permission =
        await ImagePicker.requestMediaLibraryPermissionsAsync();

      if (!permission.granted) {
        addMessage(
          'assistant',
          '⚠️ Please grant photo library access.'
        );
        return;
      }

      const result =
        await ImagePicker.launchImageLibraryAsync({
          mediaTypes: ['images'],
          allowsEditing: true,
          aspect: [4, 3],
          quality: 1,
        });

      if (
        result.canceled ||
        !result.assets ||
        result.assets.length === 0
      ) {
        return;
      }

      const imageUri =
        result.assets[0].uri;

      addMessage(
        'assistant',
        '📎 Uploading and analyzing your question...',
        imageUri
      );

      await analyzeImage(imageUri);
    } catch (error) {
      addMessage(
        'assistant',
        '⚠️ Unable to select image.'
      );
    }
  };

  const handleActionPress = async (
    action: 'camera' | 'gallery'
  ) => {
    if (action === 'camera') {
      await handleTakePhoto();
    } else {
      await handlePickImage();
    }
  };

  const handleSendMessage = async () => {
    const trimmed = message.trim();

    if (!trimmed || sending) return;

    try {
      setSending(true);

      const authToken =
        await AsyncStorage.getItem(
          'auth_token'
        );

      if (!authToken) {
        router.replace('/login');
        return;
      }

      addMessage('user', trimmed);
      setMessage('');

      const result = await sendMessage(
        trimmed,
        authToken
      );

      addMessage(
        'assistant',
        result.reply ||
          'No response received.',
        result.type === 'image'
          ? result.url
          : undefined
      );

      if (
        typeof result.tokens_left ===
        'number'
      ) {
        setTokens(result.tokens_left);

        await AsyncStorage.setItem(
          'user_tokens',
          String(result.tokens_left)
        );
      }
    } catch (error: any) {
      addMessage(
        'assistant',
        error.message ||
          'ARIS server error.'
      );
    } finally {
      setSending(false);
    }
  };

  return (
    <SafeAreaView
      style={styles.container}
    >
      <StatusBar
        barStyle="light-content"
        backgroundColor={
          COLORS.background
        }
      />

      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={
          Platform.OS === 'ios'
            ? 'padding'
            : undefined
        }
      >
        <View style={styles.header}>
          <TouchableOpacity
            style={styles.iconButton}
            onPress={handleBackPress}
          >
            <Ionicons
              name="arrow-back"
              size={22}
              color="#ffffff"
            />
          </TouchableOpacity>

          <Text style={styles.headerTitle}>
            {title}
          </Text>

          <View style={styles.tokenBadge}>
            <Text style={styles.tokenText}>
              🧠 {tokens.toLocaleString()}
            </Text>
          </View>
        </View>

        <ScrollView
          ref={scrollViewRef}
          style={{ flex: 1 }}
          contentContainerStyle={
            styles.content
          }
          showsVerticalScrollIndicator={
            false
          }
        >
          {messages.length === 0 && (
            <>
              <Text style={styles.subtitle}>
                {subtitle}
              </Text>

              <View style={styles.grid}>
                {tools.map(
                  (tool, index) => (
                    <TouchableOpacity
                      key={index}
                      style={styles.card}
                      onPress={() =>
                        handleToolPress(tool)
                      }
                    >
                      <Ionicons
                        name={tool.icon as any}
                        size={30}
                        color={COLORS.primary}
                      />

                      <Text
                        style={
                          styles.cardTitle
                        }
                      >
                        {tool.title}
                      </Text>
                    </TouchableOpacity>
                  )
                )}
              </View>
            </>
          )}

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
                {!!msg.content &&
                  (msg.role ===
                  'assistant' ? (
                    <Markdown
                      style={{
                        body:
                          styles.assistantMessageText,
                        heading1: {
                          color: '#ffffff',
                          fontSize: 24,
                          fontWeight: '700',
                          marginBottom: 8,
                        },
                        heading2: {
                          color: '#ffffff',
                          fontSize: 20,
                          fontWeight: '700',
                          marginBottom: 8,
                        },
                        heading3: {
                          color: '#ffffff',
                          fontSize: 18,
                          fontWeight: '600',
                          marginBottom: 8,
                        },
                        bullet_list: {
                          marginVertical: 6,
                        },
                        ordered_list: {
                          marginVertical: 6,
                        },
                        code_inline: {
                          backgroundColor:
                            '#1f2937',
                          color:
                            '#f97316',
                          paddingHorizontal: 4,
                          borderRadius: 4,
                        },
                        fence: {
                          backgroundColor:
                            '#111827',
                          color:
                            '#f97316',
                          padding: 12,
                          borderRadius: 8,
                        },
                        strong: {
                          color:
                            '#ffffff',
                          fontWeight:
                            '700',
                        },
                        em: {
                          color:
                            '#d1d5db',
                          fontStyle:
                            'italic',
                        },
                      }}
                    >
                      {msg.content}
                    </Markdown>
                  ) : (
                    <Text
                      style={[
                        styles.messageText,
                        styles.userMessageText,
                      ]}
                    >
                      {msg.content}
                    </Text>
                  ))}

                {msg.actions && (
                  <View
                    style={
                      styles.actionsContainer
                    }
                  >
                    {msg.actions.map(
                      (
                        action,
                        index
                      ) => (
                        <TouchableOpacity
                          key={index}
                          style={
                            styles.actionButton
                          }
                          onPress={() =>
                            handleActionPress(
                              action.action
                            )
                          }
                        >
                          <Text
                            style={
                              styles.actionButtonText
                            }
                          >
                            {
                              action.label
                            }
                          </Text>
                        </TouchableOpacity>
                      )
                    )}
                  </View>
                )}

                {msg.imageUrl && (
                  <TouchableOpacity
                    onPress={() =>
                      Linking.openURL(
                        msg.imageUrl!
                      )
                    }
                    style={
                      styles.chatImageWrapper
                    }
                  >
                    <Image
                      source={{
                        uri: msg.imageUrl,
                      }}
                      style={
                        styles.chatImage
                      }
                      resizeMode="cover"
                    />
                  </TouchableOpacity>
                )}
              </View>
            </View>
          ))}

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

        <SafeAreaView
          edges={['bottom']}
          style={styles.bottomSafeArea}
        >
          <View
            style={styles.inputContainer}
          >
            <TouchableOpacity
              style={styles.attachButton}
              onPress={handlePickImage}
            >
              <Text
                style={styles.attachText}
              >
                📎
              </Text>
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
                color={
                  COLORS.primaryText
                }
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
    backgroundColor:
      COLORS.background,
  },

  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent:
      'space-between',
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
    backgroundColor:
      'rgba(255,255,255,0.08)',
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: COLORS.border,
  },

  tokenBadge: {
    backgroundColor:
      COLORS.primary,
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 12,
  },

  tokenText: {
    color: COLORS.primaryText,
    fontWeight: '700',
    fontSize: 14,
  },

  content: {
    paddingHorizontal: 20,
    paddingBottom: 20,
  },

  subtitle: {
    marginTop: 8,
    marginBottom: 24,
    fontSize: 15,
    lineHeight: 24,
    color:
      COLORS.textSecondary,
  },

  grid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent:
      'space-between',
  },

  card: {
    width: '48%',
    minHeight: 150,
    backgroundColor: COLORS.card,
    borderRadius: 22,
    padding: 20,
    marginBottom: 16,
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: COLORS.border,
  },

  cardTitle: {
    marginTop: 16,
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
    lineHeight: 22,
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
    backgroundColor:
      COLORS.userBubble,
    borderBottomRightRadius: 6,
  },

  assistantBubble: {
    backgroundColor:
      COLORS.assistantBubble,
    borderBottomLeftRadius: 6,
    borderWidth: 1,
    borderColor: COLORS.border,
  },

  messageText: {
    fontSize: 15,
    lineHeight: 22,
    color: COLORS.text,
  },

  userMessageText: {
    color: COLORS.primaryText,
    fontWeight: '500',
  },

  assistantMessageText: {
    color: COLORS.text,
    fontSize: 15,
    lineHeight: 22,
  },

  actionsContainer: {
    marginTop: 12,
    gap: 10,
  },

  actionButton: {
    backgroundColor:
      'rgba(249,115,22,0.15)',
    borderWidth: 1,
    borderColor: COLORS.primary,
    paddingVertical: 12,
    paddingHorizontal: 14,
    borderRadius: 12,
  },

  actionButtonText: {
    color: COLORS.text,
    fontSize: 14,
    fontWeight: '600',
  },

  chatImageWrapper: {
    marginTop: 10,
  },

  chatImage: {
    width: 240,
    height: 240,
    borderRadius: 12,
    backgroundColor: '#1f2937',
  },

  bottomSafeArea: {
    backgroundColor:
      COLORS.background,
  },

  inputContainer: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    paddingHorizontal: 14,
    paddingTop: 12,
    paddingBottom: 12,
    borderTopWidth: 1,
    borderTopColor:
      COLORS.border,
    backgroundColor:
      COLORS.background,
    gap: 8,
  },

  attachButton: {
    width: 46,
    height: 46,
    borderRadius: 12,
    backgroundColor:
      COLORS.primary,
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
    backgroundColor:
      COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
  },
});