# Analytics Components

This directory contains the visualization widgets for the Bot Analytics Dashboard.

## Components

### 1. `HealthScoreWidget`
Displays the overall health of the chatbot as a circular progress bar.
- **Props:** `score: number` (0-100)
- **Logic:**
  - Green (90-100): Excellent
  - Yellow (70-89): Good
  - Red (<70): Critical

### 2. `KnowledgeGapStats`
A grid of 4 key metrics: Total Queries, Success Rate, Failed Queries, Avg Confidence.
- **Props:** `stats: AnalyticsStats`

### 3. `TopFailedQueriesChart`
A horizontal bar chart showing the most frequent questions the bot failed to answer.
- **Props:** `data: FailedQuery[]`
- **Library:** `recharts`

### 4. `RecentGapsList`
A scrollable list of recent queries that were flagged as knowledge gaps.
- **Props:** `gaps: KnowledgeGap[]`

### 5. `AIInsightsList`
An interactive list of AI-generated suggestions to improve the bot.
- **Props:** 
  - `insights: AIInsight[]`
  - `onRefresh: () => void`
  - `refreshing: boolean`

## Usage

```tsx
import { 
  HealthScoreWidget, 
  KnowledgeGapStats 
} from "@/components/analytics";

// ... inside your page
<HealthScoreWidget score={85} />
<KnowledgeGapStats stats={statsData} />
```

## Styling
All components use **Tailwind CSS** and match the dashboard's design system:
- Background: `bg-zinc-900/50`
- Border: `border-white/5`
- Text: `text-zinc-400` (secondary), `text-white` (primary)
