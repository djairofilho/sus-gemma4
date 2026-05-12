export type RiskLevel = "low" | "moderate" | "high" | "emergency";

export type Referral =
  | "UBS"
  | "UPA"
  | "SAMU"
  | "emergency"
  | "scheduled_follow_up"
  | "administrative_guidance"
  | "unknown";

export type TriageResponse = {
  risk_level: RiskLevel;
  summary: string;
  suggested_action: string;
  referral: Referral;
  red_flags: string[];
  sus_basis: string[];
  limitations: string;
  safety_notice: string;
  runtime: "mock" | "ollama" | "mock_fallback";
};

export type HealthResponse = {
  status: string;
  model_runtime: string;
  rag_index: string;
};
