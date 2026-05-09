import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  Image,
  TouchableOpacity,
  ScrollView,
  TextInput,
  StatusBar,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';

const COLORS = {
  background: '#0a192f',
  card: '#10213f',
  primary: '#f97316',
  primaryLight: '#ff8c3a',
  primaryText: '#0a192f',
  text: '#ffffff',
  textSecondary: '#d1d5db',
  border: 'rgba(255,255,255,0.08)',
};

export default function HomeScreen() {
  const modes = [
    { title: 'Student AI', icon: 'school-outline' },
    { title: 'Professional AI', icon: 'briefcase-outline' },
    { title: 'Research AI', icon: 'flask-outline' },
    { title: 'Creator AI', icon: 'color-palette-outline' },
    { title: 'Life AI', icon: 'heart-outline' },
  ];

  return (
    <SafeAreaView style={styles.container} edges={['top', 'left', 'right']}>
      <StatusBar barStyle="light-content" backgroundColor={COLORS.background} />

      {/* Scrollable Content */}
      <ScrollView
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
      >
        {/* Header */}
        <View style={styles.header}>
          <View style={styles.logoContainer}>
            <Image
              source={require('../assets/images/aris-logo.png')}
              style={styles.logo}
              resizeMode="contain"
            />
          </View>

          <View style={styles.tokenBadge}>
            <Text style={styles.tokenText}>🧠 1,250</Text>
          </View>
        </View>

        {/* Greeting */}
        <Text style={styles.greeting}>Hello, Shree</Text>
        <Text style={styles.subtitle}>
          This is ARIS Intelligence. What would you like to do today?
        </Text>

        {/* AI Modes */}
        <Text style={styles.sectionTitle}>AI Modes</Text>

        <View style={styles.grid}>
          {modes.map((mode, index) => (
            <TouchableOpacity key={index} style={styles.card}>
              <Ionicons
                name={mode.icon as any}
                size={28}
                color={COLORS.primary}
              />
              <Text style={styles.cardText}>{mode.title}</Text>
            </TouchableOpacity>
          ))}
        </View>
      </ScrollView>

      {/* Bottom Input */}
      <SafeAreaView
        edges={['bottom']}
        style={styles.bottomSafeArea}
      >
        <View style={styles.inputContainer}>
          <TouchableOpacity style={styles.attachButton}>
            <Text style={styles.attachText}>📎</Text>
          </TouchableOpacity>

          <TextInput
            placeholder="Talk to ARIS..."
            placeholderTextColor="#9CA3AF"
            style={styles.input}
          />

          <TouchableOpacity style={styles.sendButton}>
            <Text style={styles.sendText}>Send</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },

  scrollContent: {
    paddingHorizontal: 20,
    paddingTop: 12,
    paddingBottom: 24,
  },

  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },

  logoContainer: {
    flex: 1,
    justifyContent: 'center',
  },

  logo: {
    width: 180,
    height: 42,
  },

  tokenBadge: {
    backgroundColor: COLORS.primary,
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 12,
    shadowColor: COLORS.primary,
    shadowOpacity: 0.45,
    shadowRadius: 10,
    elevation: 6,
  },

  tokenText: {
    color: COLORS.primaryText,
    fontWeight: '700',
    fontSize: 14,
  },

  greeting: {
    fontSize: 34,
    fontWeight: '700',
    color: COLORS.text,
    marginTop: 26,
    lineHeight: 40,
  },

  subtitle: {
    marginTop: 8,
    color: COLORS.textSecondary,
    fontSize: 16,
    lineHeight: 24,
    maxWidth: '92%',
  },

  sectionTitle: {
    marginTop: 30,
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

  bottomSafeArea: {
    backgroundColor: COLORS.background,
  },

  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
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
  },

  sendButton: {
    backgroundColor: COLORS.primary,
    paddingHorizontal: 18,
    height: 46,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
  },

  sendText: {
    color: COLORS.primaryText,
    fontWeight: '700',
    fontSize: 15,
  },
});