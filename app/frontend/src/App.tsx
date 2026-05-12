import { useState } from "react";

import { requestTriage } from "./api.ts";
import { referralLabels, riskLabels, runtimeLabels } from "./presentation.ts";
import type { TriageResponse } from "./types.ts";

const exampleCase = "Paciente relata PA 18x12, cefaleia forte e falta de ar. Esta na UBS.";

export function App() {
  const [caseText, setCaseText] = useState(exampleCase);
  const [result, setResult] = useState<TriageResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const response = await requestTriage(caseText);
      setResult(response);
    } catch (requestError) {
      setResult(null);
      setError(requestError instanceof Error ? requestError.message : "Erro inesperado.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="page-shell">
      <section className="hero-panel" aria-labelledby="page-title">
        <div className="eyebrow">Local-first SUS workflow assistant</div>
        <h1 id="page-title">Gemma SUS Assistant</h1>
        <p>
          App web local para orientar fluxos clinico-administrativos do SUS com resposta
          estruturada, backend FastAPI e runtime local via Ollama nas proximas etapas.
        </p>
        <div className="safety-banner" role="note">
          Nao substitui avaliacao profissional, nao gera diagnostico definitivo e deve escalar
          sinais de alarme para UPA, emergencia ou SAMU 192.
        </div>
      </section>

      <section className="workspace-grid" aria-label="Area de demonstracao">
        <form className="case-card" onSubmit={handleSubmit}>
          <label htmlFor="case-text">Caso clinico-administrativo</label>
          <textarea
            id="case-text"
            value={caseText}
            onChange={(event) => setCaseText(event.target.value)}
            minLength={3}
            maxLength={4000}
            rows={10}
          />
          <button disabled={isLoading || caseText.trim().length < 3} type="submit">
            {isLoading ? "Gerando orientacao..." : "Gerar resposta estruturada"}
          </button>
          {error ? <p className="error-message">{error}</p> : null}
        </form>

        <ResultPanel result={result} />
      </section>
    </main>
  );
}

function ResultPanel({ result }: { result: TriageResponse | null }) {
  if (!result) {
    return (
      <aside className="result-card empty-state">
        <h2>Resposta estruturada</h2>
        <p>Envie um caso para visualizar nivel de risco, encaminhamento, sinais de alarme e base SUS.</p>
      </aside>
    );
  }

  return (
    <aside className="result-card">
      <div className={`risk-pill risk-${result.risk_level}`}>{riskLabels[result.risk_level]}</div>
      <h2>{referralLabels[result.referral]}</h2>
      <p className="summary">{result.summary}</p>

      <dl className="structured-list">
        <div>
          <dt>Runtime</dt>
          <dd>{runtimeLabels[result.runtime] ?? result.runtime}</dd>
        </div>
        <div>
          <dt>Conduta sugerida</dt>
          <dd>{result.suggested_action}</dd>
        </div>
        <div>
          <dt>Sinais de alarme</dt>
          <dd>{result.red_flags.length > 0 ? result.red_flags.join(", ") : "Nao destacados"}</dd>
        </div>
        <div>
          <dt>Base SUS</dt>
          <dd>{result.sus_basis.join("; ")}</dd>
        </div>
        <div>
          <dt>Limites</dt>
          <dd>{result.limitations}</dd>
        </div>
      </dl>

      <div className="safety-callout">{result.safety_notice}</div>
    </aside>
  );
}
