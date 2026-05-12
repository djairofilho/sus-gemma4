import { describe, expect, it } from "vitest";

import { ragIndexLabels, referralLabels, riskLabels, runtimeLabels } from "./presentation.ts";

describe("presentation labels", () => {
  it("labels emergency risk in Portuguese", () => {
    expect(riskLabels.emergency).toBe("Emergencia");
  });

  it("labels SUS referral options", () => {
    expect(referralLabels.UBS).toBe("UBS");
    expect(referralLabels.SAMU).toBe("SAMU 192");
  });

  it("labels local runtime state", () => {
    expect(runtimeLabels.ollama).toBe("Ollama local");
    expect(runtimeLabels.mock_fallback).toBe("Fallback seguro");
    expect(runtimeLabels.ollama_enabled).toBe("Ollama habilitado");
  });

  it("labels RAG index state", () => {
    expect(ragIndexLabels.ready).toBe("Indice RAG pronto");
    expect(ragIndexLabels.not_built).toBe("Indice RAG sera criado localmente");
  });
});
