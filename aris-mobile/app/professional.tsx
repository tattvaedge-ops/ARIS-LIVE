// C:\AGENTIC AI- ARIS\aris-mobile\app\professional.tsx

import WorkspaceScreen from '../components/WorkspaceScreen';

export default function ProfessionalScreen() {
  return (
    <WorkspaceScreen
      title="Professional AI"
      subtitle="Productivity tools for business, presentations, and communication."
      tools={[
        {
          title: 'Email Writer',
          icon: 'mail-outline',
          starterQuestion:
            '📧 What type of professional email would you like me to draft?',
        },
        {
          title: 'Presentation Maker',
          icon: 'easel-outline',
          starterQuestion:
            '📊 What topic should I create a presentation outline for?',
        },
        {
          title: 'Business Strategy',
          icon: 'briefcase-outline',
          starterQuestion:
            '💼 What business challenge or strategy would you like me to analyze?',
        },
        {
          title: 'Proposal Generator',
          icon: 'document-outline',
          starterQuestion:
            '📄 What kind of business proposal would you like me to prepare?',
        },
      ]}
    />
  );
}