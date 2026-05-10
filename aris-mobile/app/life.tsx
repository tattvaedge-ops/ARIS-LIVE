// C:\AGENTIC AI- ARIS\aris-mobile\app\life.tsx

import WorkspaceScreen from '../components/WorkspaceScreen';

export default function LifeScreen() {
  return (
    <WorkspaceScreen
      title="Life AI"
      subtitle="Personal planning tools for goals, productivity, decisions, and career growth."
      tools={[
        {
          title: 'Daily Planner',
          icon: 'calendar-outline',
          starterQuestion:
            '📅 What would you like to plan today?',
        },
        {
          title: 'Goal Planner',
          icon: 'flag-outline',
          starterQuestion:
            '🎯 What goal are you working toward?',
        },
        {
          title: 'Decision Matrix',
          icon: 'git-compare-outline',
          starterQuestion:
            '⚖️ What decision would you like help making?',
        },
        {
          title: 'Career Planner',
          icon: 'rocket-outline',
          starterQuestion:
            '🚀 What career path or next step would you like guidance on?',
        },
      ]}
    />
  );
}