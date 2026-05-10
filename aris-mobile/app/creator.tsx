// C:\AGENTIC AI- ARIS\aris-mobile\app\creator.tsx

import WorkspaceScreen from '../components/WorkspaceScreen';

export default function CreatorScreen() {
  return (
    <WorkspaceScreen
      title="Creator AI"
      subtitle="Creative tools for branding, images, videos, and content creation."
      tools={[
        {
          title: 'Logo Generator',
          icon: 'diamond-outline',
          starterQuestion:
            '🎨 What brand name and style would you like for your logo?',
        },
        {
          title: 'Image Generator',
          icon: 'image-outline',
          starterQuestion:
            '🖼️ Describe the image you would like me to create.',
        },
        {
          title: 'Video Creator',
          icon: 'videocam-outline',
          starterQuestion:
            '🎬 What type of video would you like to create?',
        },
        {
          title: 'Caption Generator',
          icon: 'text-outline',
          starterQuestion:
            '✍️ What content would you like captions for?',
        },
      ]}
    />
  );
}