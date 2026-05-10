// C:\AGENTIC AI- ARIS\aris-mobile\app\student.tsx

import WorkspaceScreen from '../components/WorkspaceScreen';

export default function StudentScreen() {
  return (
    <WorkspaceScreen
      title="Student AI"
      subtitle="Academic tools for concept learning, notes, problem solving, and testing."
      tools={[
        {
          title: 'Concept Explainer',
          icon: 'bulb-outline',
          starterQuestion:
            '📘 Which concept would you like me to explain?',
        },
        {
          title: 'Notes Generator',
          icon: 'document-text-outline',
          starterQuestion:
            '📝 Which topic would you like concise notes for?',
        },
        {
          title: 'Solve Question',
          icon: 'calculator-outline',
          starterQuestion:
            '➗ Please type or upload the question you want me to solve.',
        },
        {
          title: 'Mock Test',
          icon: 'clipboard-outline',
          starterQuestion:
            '📝 Which chapter or topic would you like the mock test on?',
        },
        {
          title: 'Ask Doubt',
          icon: 'help-circle-outline',
          starterQuestion:
            '❓ Type your doubt or upload a question image.',
        },
      ]}
    />
  );
}