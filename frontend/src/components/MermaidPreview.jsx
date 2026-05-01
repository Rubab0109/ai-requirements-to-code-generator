import { useEffect, useMemo, useState } from "react";
import mermaid from "mermaid";
import { AlertTriangle } from "lucide-react";
import { ActionButton } from "./ActionButton.jsx";

mermaid.initialize({
  startOnLoad: false,
  theme: "dark",
  securityLevel: "loose",
  themeVariables: {
    background: "#020617",
    primaryColor: "#0f172a",
    primaryTextColor: "#e2e8f0",
    primaryBorderColor: "#2dd4bf",
    lineColor: "#818cf8",
    secondaryColor: "#111827",
    tertiaryColor: "#1e293b",
  },
});

export function MermaidPreview({ code, title, filename }) {
  const [svg, setSvg] = useState("");
  const [error, setError] = useState("");
  const uniqueId = useMemo(() => `mermaid-${Math.random().toString(36).slice(2)}`, []);

  useEffect(() => {
    let cancelled = false;

    async function renderDiagram() {
      const diagram = (code || "").trim();
      if (!diagram) {
        setSvg("");
        setError("No Mermaid diagram generated yet.");
        return;
      }
      try {
        await mermaid.parse(diagram);
        const rendered = await mermaid.render(`${uniqueId}-${Date.now()}`, diagram);
        if (!cancelled) {
          setSvg(rendered.svg);
          setError("");
        }
      } catch (err) {
        if (!cancelled) {
          setSvg("");
          setError(err?.message || "Invalid Mermaid diagram syntax.");
        }
      }
    }

    renderDiagram();
    return () => {
      cancelled = true;
    };
  }, [code, uniqueId]);

  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-950/55 p-5">
      <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <h3 className="text-base font-bold text-white">{title}</h3>
        <ActionButton text={code} filename={filename} />
      </div>

      {error ? (
        <div className="rounded-2xl border border-amber-400/20 bg-amber-400/10 p-4 text-sm text-amber-100">
          <div className="mb-2 flex items-center gap-2 font-semibold">
            <AlertTriangle size={17} /> Mermaid preview issue
          </div>
          <p className="mb-3 text-amber-100/80">{error}</p>
          <pre className="code-block max-h-[360px] overflow-auto rounded-2xl bg-slate-950 p-4 text-xs text-slate-300">{code}</pre>
        </div>
      ) : (
        <div className="overflow-auto rounded-2xl border border-slate-800 bg-slate-950 p-4">
          <div className="min-w-[650px]" dangerouslySetInnerHTML={{ __html: svg }} />
        </div>
      )}
    </div>
  );
}
