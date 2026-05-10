// C:\AGENTIC AI- ARIS\aris-mobile\app\research.tsx

import WorkspaceScreen from '../components/WorkspaceScreen';

export default function ResearchScreen() {
  return (
    <WorkspaceScreen
      title="Research AI"
      subtitle="Advanced research tools for literature review, summaries, citations, and data analysis."
      tools={[
        {
          title: 'Literature Review',
          icon: 'library-outline',
          starterQuestion:
            '📚 What research topic would you like a literature review on?',
        },
        {
          title: 'Research Summary',
          icon: 'reader-outline',
          starterQuestion:
            '📝 Which topic or paper would you like me to summarize?',
        },
        {
          title: 'Citation Generator',
          icon: 'bookmark-outline',
          starterQuestion:
            '🔖 Please share the source details for citation generation.',
        },
        {
          title: 'Data Analysis',
          icon: 'bar-chart-outline',
          starterQuestion:
            '📈 Please share the data or describe what you want analyzed.',
        },
      ]}
    />
  );
}