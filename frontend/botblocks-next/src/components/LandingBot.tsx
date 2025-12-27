"use client";
import { ChatWidget } from "./widget/ChatWidget";

export function LandingBot() {
    // Placeholder Bot ID. In a real scenario, the user would create a bot in the dashboard
    // and replace this ID with the one generated.
    const LANDING_BOT_ID = "landing-bot-demo";

    return (
        <ChatWidget
            botId={LANDING_BOT_ID}
            config={{
                theme: "classic",
                primary_color: "#581c87", // Purple-900 (Darkish Unique)
                bot_display_name: "BotBlocks AI",
                welcome_message: "Hi! I am BotBlocks AI, ask me anything about building chatbots!",
                position: "bottom-right",
                button_style: "circle",
                suggested_questions: [
                    "What is BotBlocks?",
                    "How do I build a bot?",
                    "Is there a free trial?",
                    "What integrations are supported?"
                ]
            }}
        />
    );
}
