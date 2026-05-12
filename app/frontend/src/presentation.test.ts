import { describe, expect, it } from "vitest";

import { referralLabels, riskLabels } from "./presentation.ts";

describe("presentation labels", () => {
  it("labels emergency risk in Portuguese", () => {
    expect(riskLabels.emergency).toBe("Emergencia");
  });

  it("labels SUS referral options", () => {
    expect(referralLabels.UBS).toBe("UBS");
    expect(referralLabels.SAMU).toBe("SAMU 192");
  });
});
