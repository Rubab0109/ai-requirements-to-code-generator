import { useEffect, useState } from "react";
import { AlertCircle, Bot, CheckCircle2, Server } from "lucide-react";
import { RequirementEditor } from "./components/RequirementEditor.jsx";
import { ProjectHistory } from "./components/ProjectHistory.jsx";
import { ResultsTabs } from "./components/ResultsTabs.jsx";
import { deleteProject, fetchProjectById, fetchProjects, generateProject } from "./api.js";

export default function App() {
  const [title, setTitle] = useState("AI Requirements-to-Code Generator Demo");
  const [requirements, setRequirements] = useState("");
  const [result, setResult] = useState(null);
  const [projects, setProjects] = useState([]);
  const [activeTab, setActiveTab] = useState("analysis");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  async function loadProjects() {
    try {
      const data = await fetchProjects();
      setProjects(data);
    } catch (err) {
      setError(err.message || "Could not load previous projects.");
    }
  }

  useEffect(() => {
    loadProjects();
  }, []);

  async function handleGenerate() {
    setError("");
    setNotice("");

    if (!requirements.trim()) {
      setError("Please enter software requirements first.");
      return;
    }
    if (requirements.trim().length < 30) {
      setError("Requirement is too short. Add modules, users, workflow, and data needs.");
      return;
    }

    setLoading(true);
    try {
      const data = await generateProject({ title, requirements });
      setResult(data);
      setActiveTab("analysis");
      setNotice("Project generated and stored successfully.");
      await loadProjects();
    } catch (err) {
      setError(err.message || "Generation failed.");
    } finally {
      setLoading(false);
    }
  }

  async function openProject(id) {
    setError("");
    try {
      const data = await fetchProjectById(id);
      setResult(data);
      setTitle(data.title);
      setRequirements(data.requirements);
      setActiveTab("analysis");
      setNotice("Previous project loaded.");
    } catch (err) {
      setError(err.message || "Could not open project.");
    }
  }

  async function removeProject(id) {
    setError("");
    try {
      await deleteProject(id);
      if (result?.id === id) setResult(null);
      await loadProjects();
      setNotice("Project deleted.");
    } catch (err) {
      setError(err.message || "Could not delete project.");
    }
  }

  return (
    <main className="min-h-screen px-4 py-5 text-slate-100 lg:px-6">
      <div className="mx-auto max-w-[1500px]">
        <header className="mb-5 flex flex-col gap-4 rounded-3xl border border-slate-800 bg-slate-950/45 p-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-teal-300 to-indigo-500 text-slate-950 shadow-glow">
              <Bot size={26} />
            </div>
            <div>
              <h1 className="text-lg font-black text-white">AI Requirements-to-Code Generator</h1>
              <p className="text-xs text-slate-500">React + Tailwind + FastAPI + LLM + Mermaid + SQLite</p>
            </div>
          </div>
          <div className="flex flex-wrap gap-2 text-xs font-semibold text-slate-300">
            <span className="inline-flex items-center gap-2 rounded-full border border-slate-800 bg-slate-900/70 px-3 py-2">
              <Server size={14} /> Backend API
            </span>
            <span className="inline-flex items-center gap-2 rounded-full border border-slate-800 bg-slate-900/70 px-3 py-2">
              <CheckCircle2 size={14} /> Mermaid Preview
            </span>
          </div>
        </header>

        {error ? (
          <div className="mb-4 flex items-start gap-2 rounded-2xl border border-rose-400/20 bg-rose-500/10 p-4 text-sm text-rose-100">
            <AlertCircle size={18} className="mt-0.5" /> {error}
          </div>
        ) : null}

        {notice ? (
          <div className="mb-4 flex items-start gap-2 rounded-2xl border border-teal-400/20 bg-teal-500/10 p-4 text-sm text-teal-100">
            <CheckCircle2 size={18} className="mt-0.5" /> {notice}
          </div>
        ) : null}

        <div className="grid gap-5 lg:grid-cols-[360px_1fr]">
          <ProjectHistory projects={projects} onOpenProject={openProject} onDeleteProject={removeProject} />
          <div className="space-y-5">
            <RequirementEditor
              title={title}
              setTitle={setTitle}
              requirements={requirements}
              setRequirements={setRequirements}
              onGenerate={handleGenerate}
              loading={loading}
            />
            <ResultsTabs result={result} activeTab={activeTab} setActiveTab={setActiveTab} />
          </div>
        </div>
      </div>
    </main>
  );
}
