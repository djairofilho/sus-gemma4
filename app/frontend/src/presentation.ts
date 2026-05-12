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
