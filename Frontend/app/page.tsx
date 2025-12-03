"use client";

import React, { useState } from "react";

type DebateStatus =
  | "idle"
  | "loading"
  | "needs_confirmation"
  | "debated"
  | "error";

type NeedsConfirmation = {
  status: "needs_confirmation";
  domain: string;
  original_prompt: string;
  improved_prompt: string;
  explanation: string;
  message: string;
};

type Debated = {
  status: "debated";
  chat_id: string;
  domain: string;
  used_prompt: string;
  agents: string[];
  initial: Record<string, string>;
  critiques: Record<string, string>;
  defenses: Record<string, string>;
  winner: string;
  scoreboard: Record<string, number>;
  answer: string;
  reason: string;
  judge_raw: string;
};

const API_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://127.0.0.1:8000";

export default function HomePage() {
  const [question, setQuestion] = useState("");
  const [status, setStatus] = useState<DebateStatus>("idle");
  const [error, setError] = useState<string | null>(null);

  const [needsConfirm, setNeedsConfirm] =
    useState<NeedsConfirmation | null>(null);

  const [debated, setDebated] = useState<Debated | null>(null);
  const [chatId, setChatId] = useState<string | null>(null);

  async function callDebateAPI(
    useImproved: boolean,
    improvedPrompt?: string | null
  ) {
    if (!question.trim()) {
      setError("Please enter a question first.");
      return;
    }

    setError(null);
    setStatus("loading");
    setDebated(null);

    try {
      const body = {
        question,
        chat_id: chatId,
        use_improved: useImproved,
        improved_prompt: improvedPrompt ?? null,
      };

      const res = await fetch(`${API_URL}/debate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      if (!res.ok) {
        const txt = await res.text();
        throw new Error(`Backend error ${res.status}: ${txt}`);
      }

      const data = (await res.json()) as NeedsConfirmation | Debated;

      if (data.status === "needs_confirmation") {
        setNeedsConfirm(data);
        setDebated(null);
        setStatus("needs_confirmation");
      } else {
        setNeedsConfirm(null);
        setDebated(data);
        setChatId(data.chat_id);
        setStatus("debated");
      }
    } catch (err: any) {
      setError(err.message ?? "Something went wrong.");
      setStatus("error");
    }
  }

  function handleStartDebate() {
    callDebateAPI(false, null);
  }

  function handleUseImproved() {
    if (!needsConfirm) return;
    callDebateAPI(true, needsConfirm.improved_prompt);
  }

  function handleKeepOriginal() {
    callDebateAPI(false, null);
  }

  return (
    <main className="min-h-screen flex justify-center">
      <div className="w-full max-w-4xl px-4 py-10">
        {/* Header */}
        <header className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold flex items-center gap-2">
            🧠 AI Multi-Agent Debate
          </h1>
          <p className="text-slate-300 mt-2">
            Ask a question. The system may improve your prompt, then multiple AI
            agents debate and a judge picks the best answer.
          </p>
        </header>

        {/* Question Box */}
        <section className="mb-6">
          <div className="bg-slate-900/70 border border-slate-800 rounded-xl p-4 space-y-3">
            <label className="block text-sm font-medium text-slate-300 mb-1">
              Your question
            </label>
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Example: Explain difference between Diesel & Otto cycle..."
              className="w-full min-h-[120px] bg-slate-950 border border-slate-700/70 rounded-lg px-3 py-2 text-sm outline-none focus:border-indigo-400 focus:ring-1 focus:ring-indigo-500"
            />
            <div className="flex items-center justify-between">
              <span className="text-xs text-slate-500">
                The system may suggest a better prompt first.
              </span>
              <button
                onClick={handleStartDebate}
                disabled={status === "loading"}
                className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-500 hover:bg-indigo-600 text-sm font-medium disabled:opacity-50"
              >
                {status === "loading" ? "Thinking…" : "Start Debate"}
              </button>
            </div>
          </div>
        </section>

        {/* Error */}
        {error && (
          <div className="mb-4 bg-red-900/40 border border-red-700 text-red-100 text-sm rounded-lg px-4 py-2">
            {error}
          </div>
        )}

        {/* Needs Confirmation */}
        {status === "needs_confirmation" && needsConfirm && (
          <section className="mb-8">
            <div className="bg-amber-900/40 border border-amber-500 rounded-xl p-4 space-y-3">
              <h2 className="text-lg font-semibold">⚠️ Prompt Improvement Recommended</h2>
              <p className="text-sm text-slate-100">
                The system suggests a better version for higher quality.
              </p>

              <div className="grid md:grid-cols-2 gap-4 text-sm">
                <div className="bg-slate-950/70 border border-slate-800 rounded-lg p-3">
                  <div className="text-xs text-slate-400 mb-1">Original</div>
                  <p>{needsConfirm.original_prompt}</p>
                </div>

                <div className="bg-slate-950/70 border border-emerald-700 rounded-lg p-3">
                  <div className="text-xs text-emerald-300 mb-1">Improved</div>
                  <p>{needsConfirm.improved_prompt}</p>
                </div>
              </div>

              <div className="flex gap-3">
                <button
                  onClick={handleUseImproved}
                  className="px-4 py-2 rounded-lg bg-emerald-500 hover:bg-emerald-600 text-sm"
                >
                  Use Improved
                </button>
                <button
                  onClick={handleKeepOriginal}
                  className="px-4 py-2 rounded-lg bg-slate-700 hover:bg-slate-600 text-sm"
                >
                  Keep Original
                </button>
              </div>
            </div>
          </section>
        )}

        {/* Debate Results */}
        {status === "debated" && debated && (
          <section className="space-y-6">
            <div className="bg-slate-900/70 border border-slate-800 rounded-xl p-4 space-y-3">
              <h2 className="text-xl font-semibold">
                🏆 Winner:{" "}
                <span className="px-2 py-1 bg-emerald-500/20 border border-emerald-400 rounded">
                  {debated.winner}
                </span>
              </h2>

              <div>
                <h3 className="text-xs text-slate-400 mb-1">Final Answer</h3>
                <div className="bg-slate-950 border border-slate-800 rounded-lg p-3 text-sm whitespace-pre-wrap">
                  {debated.answer}
                </div>
              </div>

              <div>
                <h3 className="text-xs text-slate-400 mb-1">Judge Reason</h3>
                <div className="bg-slate-950 border border-slate-800 rounded-lg p-3 text-sm whitespace-pre-wrap">
                  {debated.reason}
                </div>
              </div>
            </div>
          </section>
        )}
      </div>
    </main>
  );
}
