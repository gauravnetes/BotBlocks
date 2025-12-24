import { ChatWidget } from '@/components/widget/ChatWidget';

async function getWidgetConfig(botId: string) {
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/v1/bots/${botId}/widget-config`, {
      cache: 'no-store'
    });

    if (!res.ok) {
      console.warn('Failed to fetch widget config, using default');
      return {
        theme: 'modern',
        primary_color: '#3b82f6',
        avatar_url: null,
        welcome_message: 'Hello! How can I help you today?',
        bot_display_name: 'AI Assistant',
        position: 'bottom-right',
        button_style: 'circle'
      };
    }
    return await res.json();
  } catch (error) {
    console.error('Error fetching widget config:', error);
    return {
      theme: 'modern',
      primary_color: '#3b82f6',
      avatar_url: null,
      welcome_message: 'Hello! How can I help you today?',
      bot_display_name: 'AI Assistant',
      position: 'bottom-right',
      button_style: 'circle'
    };
  }
}

export default async function WidgetPage({ params }: { params: Promise<{ botId: string }> }) {
  const { botId } = await params;
  const config = await getWidgetConfig(botId);

  return (
    <>
      <style>{`
        html, body {
          background: transparent !important;
        }
        /* Hide Next.js Dev Tools Indicator in Iframe */
        [class^="nextjs-"], #__next-build-watcher, [data-nextjs-toast] {
          display: none !important;
        }
      `}</style>
      <div className="min-h-screen bg-transparent">
        <ChatWidget botId={botId} config={config} />
      </div>
    </>
  );
}
