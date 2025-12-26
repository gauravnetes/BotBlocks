"use client";

import React from "react";
import { CircularProgressbar, buildStyles } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";

interface HealthScoreWidgetProps {
    score: number;
}

export function HealthScoreWidget({ score }: HealthScoreWidgetProps) {
    let color = "#10b981"; // Green-500
    let label = "Excellent";
    let description = "Your bot is answering most queries correctly.";

    if (score < 70) {
        color = "#ef4444"; // Red-500
        label = "Critical";
        description = "Immediate knowledge updates required.";
    } else if (score < 90) {
        color = "#f59e0b"; // Amber-500
        label = "Good";
        description = "Some knowledge gaps detected.";
    }

    return (
        <div className="bg-zinc-900/50 border border-white/5 rounded-xl p-6 flex flex-col items-center justify-center h-full hover:border-white/10 transition-colors duration-300">
            <h3 className="text-lg font-semibold text-white mb-6">Bot Health Score</h3>
            <div className="w-[180px] h-[180px] hover:scale-105 transition-transform duration-500 ease-out">
                <CircularProgressbar
                    value={score}
                    text={`${Math.round(score)}%`}
                    styles={buildStyles({
                        pathColor: color,
                        textColor: "#fff",
                        trailColor: "rgba(255,255,255,0.05)",
                        textSize: "16px",
                        pathTransitionDuration: 0.8,
                        backgroundColor: "#3e98c7",
                    })}
                />
            </div>
            <div className="mt-6 text-center animate-in fade-in slide-in-from-bottom-2 duration-500">
                <p className="text-2xl font-bold transition-colors duration-300" style={{ color }}>{label}</p>
                <p className="text-zinc-500 text-sm mt-1 max-w-[200px] mx-auto">{description}</p>
            </div>
        </div>
    );
}
