import { Layers, GitBranch, Network, Table2, Code2, Cpu } from "lucide-react";
import { MermaidPreview } from "./MermaidPreview.jsx";
import { OutputCard } from "./OutputCard.jsx";

const tabs = [
  { id: "analysis", label: "Analysis", icon: Layers },
  { id: "uml", label: "UML Diagram", icon: GitBranch },
  { id: "erd", label: "ERD Diagram", icon: Network },
  { id: "schema", label: "Database Schema", icon: Table2 },
  { id: "code", label: "Code Skeleton", icon: Code2 },
  { id: "stack", label: "Tech Stack", icon: Cpu },
];

function ListBlock({ title, items }) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-950/55 p-4">
      <h4 className="mb-3 text-sm font-bold text-slate-200">{title}</h4>
      <ul className="space-y-2 text-sm leading-6 text-slate-400">
        {(items || []).map((item, index) => (
          <li key={`${title}-${index}`} className="flex gap-2">
            <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-teal-300" />
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export function ResultsTabs({ result, activeTab, setActiveTab }) {
  if (!result) {
    return (
      <section className="glass rounded-3xl p-8 text-center">
        <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-3xl bg-slate-800 text-slate-300">
          <Layers size={24} />
        </div>
        <h2 className="text-lg font-bold text-white">Generated output will appear here</h2>
        <p className="mx-auto mt-2 max-w-xl text-sm leading-6 text-slate-500">
          The app will display analysis, diagrams, schema, starter code, and technology stack in professional tabs.
        </p>
      </section>
    );
  }

  const generated = result.generated;
  const analysisText = [
    generated.analysis,
    "\nFunctional Requirements:\n" + (generated.functional_requirements || []).map((x, i) => `${i + 1}. ${x}`).join("\n"),
    "\nNon-Functional Requirements:\n" + (generated.non_functional_requirements || []).map((x, i) => `${i + 1}. ${x}`).join("\n"),
  ].join("\n");

  return (
    <section className="glass rounded-3xl p-4 lg:p-5">
      <div className="mb-4 flex flex-wrap gap-2">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`inline-flex items-center gap-2 rounded-2xl px-4 py-2 text-sm font-semibold transition ${
                isActive
                  ? "bg-teal-400 text-slate-950 shadow-glow"
                  : "border border-slate-800 bg-slate-950/50 text-slate-400 hover:border-teal-400/50 hover:text-teal-200"
              }`}
            >
              <Icon size={16} /> {tab.label}
            </button>
          );
        })}
      </div>

      {generated.warning ? (
        <div className="mb-4 rounded-2xl border border-amber-400/20 bg-amber-400/10 p-4 text-sm text-amber-100">
          {generated.warning}
        </div>
      ) : null}

      {activeTab === "analysis" ? (
        <div className="space-y-4">
          <OutputCard title="Clean Requirement Analysis" rawText={analysisText} filename="requirement-analysis.txt">
            <p className="whitespace-pre-line text-sm leading-7 text-slate-300">{generated.analysis}</p>
          </OutputCard>
          <div className="grid gap-4 lg:grid-cols-2">
            <ListBlock title="Functional Requirements" items={generated.functional_requirements} />
            <ListBlock title="Non-Functional Requirements" items={generated.non_functional_requirements} />
          </div>
          <ListBlock title="Assumptions" items={generated.assumptions} />
        </div>
      ) : null}

      {activeTab === "uml" ? (
        <MermaidPreview code={generated.uml_mermaid} title="UML Class Diagram Preview" filename="uml-class-diagram.mmd" />
      ) : null}

      {activeTab === "erd" ? (
        <MermaidPreview code={generated.erd_mermaid} title="ERD Diagram Preview" filename="erd-diagram.mmd" />
      ) : null}

      {activeTab === "schema" ? (
        <OutputCard title="Database Schema" rawText={generated.database_schema} filename="database-schema.sql">
          <pre className="code-block max-h-[520px] overflow-auto rounded-2xl bg-slate-950 p-4 text-sm leading-7 text-slate-300">
            {generated.database_schema}
          </pre>
        </OutputCard>
      ) : null}

      {activeTab === "code" ? (
        <OutputCard title="Initial Code Skeleton" rawText={generated.code_skeleton} filename="code-skeleton.txt">
          <pre className="code-block max-h-[560px] overflow-auto rounded-2xl bg-slate-950 p-4 text-sm leading-7 text-slate-300">
            {generated.code_skeleton}
          </pre>
        </OutputCard>
      ) : null}

      {activeTab === "stack" ? (
        <div className="grid gap-4 lg:grid-cols-2">
          <ListBlock title="Suggested Technology Stack" items={generated.tech_stack} />
          <ListBlock title="Testing Notes" items={generated.testing_notes} />
        </div>
      ) : null}
    </section>
  );
}
