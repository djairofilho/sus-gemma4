import type { Referral, RiskLevel } from "./types.ts";

export const riskLabels: Record<RiskLevel, string> = {
  low: "Baixo",
  moderate: "Moderado",
  high: "Alto",
  emergency: "Emergencia",
};

export const referralLabels: Record<Referral, string> = {
  UBS: "UBS",
  UPA: "UPA",
  SAMU: "SAMU 192",
  emergency: "Emergencia",
  scheduled_follow_up: "Retorno programado",
  administrative_guidance: "Orientacao administrativa",
  unknown: "A definir",
};

export const runtimeLabels: Record<string, string> = {
  mock: "Mock local",
  ollama: "Ollama local",
  mock_fallback: "Fallback seguro",
  mock_backend: "Backend mock",
  ollama_enabled: "Ollama habilitado",
};

export const ragIndexLabels: Record<string, string> = {
  ready: "Indice RAG pronto",
  not_built: "Indice RAG sera criado localmente",
};
