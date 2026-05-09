import React from 'react';
import {
  SafeAreaView,
  View,
  Text,
  StyleSheet,
  Image,
  TouchableOpacity,
  ScrollView,
  TextInput,
  StatusBar,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

export default function App() {
  const modes = [
    { title: 'Student AI', icon: 'school-outline' },
    { title: 'Professional AI', icon: 'briefcase-outline' },
    { title: 'Research AI', icon: 'flask-outline' },
    { title: 'Creator AI', icon: 'color-palette-outline' },
    { title: 'Life AI', icon: 'heart-outline' },
  ];

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />

      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Header */}
        <View style={styles.header}>
          <Image
            source={require('./assets/images/aris-logo.png')}
            style={styles.logo}
            resizeMode="contain"
          />

          <View style={styles.tokenBadge}>
            <Ionicons name="diamond-outline" size={16} color="#FFD700" />
            <Text style={styles.tokenText}>1,250</Text>
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
                color="#00E5FF"
              />
              <Text style={styles.cardText}>{mode.title}</Text>
            </TouchableOpacity>
          ))}
        </View>
      </ScrollView>

      {/* Bottom Input */}
      <View style={styles.inputContainer}>
        <TextInput
          placeholder="Ask ARIS anything..."
          placeholderTextColor="#888"
          style={styles.input}
        />
        <TouchableOpacity style={styles.sendButton}>
          <Ionicons name="arrow-up" size={20} color="#000" />
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0B0F1A',
    paddingHorizontal: 20,
    paddingTop: 20,
  },

  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 10,
  },

  logo: {
    width: 120,
    height: 50,
  },

  tokenBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1B2233',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 20,
  },

  tokenText: {
    color: '#FFF',
    marginLeft: 6,
    fontWeight: '600',
  },

  greeting: {
    color: '#FFF',
    fontSize: 28,
    fontWeight: '700',
    marginTop: 25,
  },

  subtitle: {
    color: '#A0A8B8',
    fontSize: 15,
    marginTop: 8,
    lineHeight: 22,
  },

  sectionTitle: {
    color: '#FFF',
    fontSize: 20,
    fontWeight: '600',
    marginTop: 30,
    marginBottom: 15,
  },

  grid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },

  card: {
    width: '48%',
    backgroundColor: '#151C2C',
    borderRadius: 20,
    padding: 20,
    marginBottom: 15,
    minHeight: 120,
    justifyContent: 'center',
  },

  cardText: {
    color: '#FFF',
    marginTop: 12,
    fontSize: 15,
    fontWeight: '600',
  },

  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#151C2C',
    borderRadius: 30,
    paddingHorizontal: 16,
    paddingVertical: 10,
    marginBottom: 20,
    marginTop: 10,
  },

  input: {
    flex: 1,
    color: '#FFF',
    fontSize: 16,
  },

  sendButton: {
    backgroundColor: '#00E5FF',
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
});