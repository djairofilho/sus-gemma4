import type { TriageResponse } from "./types.ts";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export async function requestTriage(caseText: string): Promise<TriageResponse> {
  const response = await fetch(`${API_BASE_URL}/api/triage`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ case_text: caseText }),
  });

  if (!response.ok) {
    throw new Error("Nao foi possivel obter a orientacao estruturada do backend local.");
  }

  return (await response.json()) as TriageResponse;
}
