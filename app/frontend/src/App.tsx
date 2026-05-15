import { useEffect, useState } from "react";

import { requestHealth, requestTriage } from "./api.ts";
import { ragIndexLabels, referralLabels, riskLabels, runtimeLabels } from "./presentation.ts";
import type { HealthResponse, TriageResponse } from "./types.ts";

const exampleCases = [
  {
    label: "Urgencia UBS",
    text: "Paciente relata PA 18x12, cefaleia forte e falta de ar. Esta na UBS.",
  },
  {
    label: "Administrativo",
    text: "Usuario quer renovar encaminhamento para especialista feito pela UBS e nao relata sintomas novos.",
  },
  {
    label: "Receituario azul",
    text: "Usuario perdeu o receituario azul e pede uma nova receita de medicamento controlado.",
  },
];

export function App() {
  const [caseText, setCaseText] = useState(exampleCases[0].text);
  const [result, setResult] = useState<TriageResponse | null>(null);
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [statusError, setStatusError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    requestHealth()
      .then((response) => {
        setHealth(response);
        setStatusError(null);
      })
      .catch((requestError: unknown) => {
        setHealth(null);
        setStatusError(
          requestError instanceof Error ? requestError.message : "Status local indisponivel.",
        );
      });
  }, []);

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
        <div className="hero-content">
          <div className="sus-badge" aria-hidden="true">+ SUS</div>
          <div className="eyebrow">Local-first SUS workflow assistant</div>
          <h1 id="page-title">Gemma SUS Assistant</h1>
          <p>
            App web local para orientar fluxos clinico-administrativos do SUS com resposta estruturada,
            contexto RAG citado, backend FastAPI e runtime local via Ollama quando habilitado.
          </p>
          <div className="hero-chips" aria-label="Capacidades principais">
            <span>UBS • UPA • SAMU</span>
            <span>RAG oficial citado</span>
            <span>IA local validada</span>
          </div>
        </div>
        <div className="safety-banner" role="note">
          Nao substitui avaliacao profissional, nao gera diagnostico definitivo e deve escalar
          sinais de alarme para UPA, emergencia ou SAMU 192.
        </div>
      </section>

      <section className="workspace-grid" aria-label="Area de demonstracao">
        <div className="input-stack">
          <StatusPanel health={health} statusError={statusError} />

          <form className="case-card" onSubmit={handleSubmit}>
            <div className="form-heading">
              <div>
                <span className="section-kicker">Entrada</span>
                <label htmlFor="case-text">Caso clinico-administrativo</label>
              </div>
              <span className="character-count">{caseText.length}/4000</span>
            </div>
            <div className="example-row" aria-label="Casos de exemplo">
              {exampleCases.map((example) => (
                <button
                  key={example.label}
                  className="example-button"
                  onClick={() => setCaseText(example.text)}
                  type="button"
                >
                  {example.label}
                </button>
              ))}
            </div>
            <textarea
              id="case-text"
              value={caseText}
              onChange={(event) => setCaseText(event.target.value)}
              minLength={3}
              maxLength={4000}
              rows={10}
              placeholder="Descreva o caso em portugues brasileiro, sem dados identificaveis do paciente."
            />
            <p className="input-hint">
              Evite nome, CPF, endereco ou outros identificadores. Use termos do fluxo local: UBS,
              UPA, SAMU, regulacao, acolhimento.
            </p>
            <button disabled={isLoading || caseText.trim().length < 3} type="submit">
              {isLoading ? "Gerando orientacao..." : "Gerar resposta estruturada"}
            </button>
            {isLoading ? <p className="loading-message" role="status">Consultando backend local e contexto RAG.</p> : null}
            {error ? <p className="error-message" role="alert">{error}</p> : null}
          </form>
        </div>

        <ResultPanel result={result} />
      </section>
    </main>
  );
}

function StatusPanel({ health, statusError }: { health: HealthResponse | null; statusError: string | null }) {
  return (
    <section className="status-card" aria-label="Status local">
      <div>
        <span className="status-label">Backend</span>
        <strong><span className={health?.status === "ok" ? "status-dot online" : "status-dot"} />{health?.status === "ok" ? "Online" : "Aguardando"}</strong>
      </div>
      <div>
        <span className="status-label">Runtime</span>
        <strong><span className="status-dot" />{health ? runtimeLabels[health.model_runtime] ?? health.model_runtime : "Indisponivel"}</strong>
      </div>
      <div>
        <span className="status-label">RAG</span>
        <strong><span className={health?.rag_index === "ready" ? "status-dot online" : "status-dot"} />{health ? ragIndexLabels[health.rag_index] ?? health.rag_index : "Indisponivel"}</strong>
      </div>
      {statusError ? <p className="status-error" role="status">{statusError}</p> : null}
    </section>
  );
}

function ResultPanel({ result }: { result: TriageResponse | null }) {
  if (!result) {
    return (
      <aside className="result-card empty-state">
        <span className="section-kicker">Saida</span>
        <h2>Resposta estruturada</h2>
        <p>Envie um caso para visualizar nivel de risco, encaminhamento, sinais de alarme e base SUS.</p>
        <ul className="empty-list" aria-label="Campos exibidos na resposta">
          <li>Nivel de risco e encaminhamento SUS</li>
          <li>Sinais de alarme destacados</li>
          <li>Citacoes RAG e JSON validado</li>
        </ul>
      </aside>
    );
  }

  return (
    <aside className="result-card">
      <div className="result-header">
        <div>
          <span className="section-kicker">Orientacao estruturada</span>
          <h2>{referralLabels[result.referral]}</h2>
        </div>
        <div className={`risk-pill risk-${result.risk_level}`}>{riskLabels[result.risk_level]}</div>
      </div>
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
          <dd>
            {result.red_flags.length > 0 ? (
              <ul className="red-flag-list">
                {result.red_flags.map((flag) => <li key={flag}>{flag}</li>)}
              </ul>
            ) : "Nao destacados"}
          </dd>
        </div>
        <div>
          <dt>Limites</dt>
          <dd>{result.limitations}</dd>
        </div>
      </dl>

      <div className="safety-callout">{result.safety_notice}</div>

      <section className="citation-panel" aria-labelledby="citation-title">
        <h3 id="citation-title">Citacoes recuperadas</h3>
        <ul>
          {result.sus_basis.map((basis) => (
            <li key={basis}>{basis}</li>
          ))}
        </ul>
      </section>

      <details className="json-panel">
        <summary>JSON estruturado</summary>
        <pre>{JSON.stringify(result, null, 2)}</pre>
      </details>
    </aside>
  );
}
