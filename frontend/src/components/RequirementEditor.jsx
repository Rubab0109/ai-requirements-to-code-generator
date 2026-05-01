import { Sparkles, Wand2 } from "lucide-react";

const SAMPLE = `Build a campus event and society management system where students can register, societies can create events, admin can approve events, generate fee vouchers, track payments, manage departments/batches, and export attendance/reports. The system should have role based dashboards for admin, society head, and student.`;

export function RequirementEditor({ title, setTitle, requirements, setRequirements, onGenerate, loading }) {
  return (
    <section className="glass rounded-3xl p-5 lg:p-6">
      <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <div className="inline-flex items-center gap-2 rounded-full border border-teal-400/20 bg-teal-400/10 px-3 py-1 text-xs font-semibold text-teal-200">
            <Sparkles size={14} /> AI Software Architect
          </div>
          <h1 className="mt-3 text-2xl font-bold tracking-tight text-white lg:text-3xl">
            Requirements-to-Code Generator
          </h1>
          <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-400">
            Enter raw project requirements. The backend will generate analysis, UML, ERD, schema, starter code, and suggested stack.
          </p>
        </div>
      </div>

      <label className="mb-2 block text-sm font-semibold text-slate-200">Project title</label>
      <input
        value={title}
        onChange={(event) => setTitle(event.target.value)}
        placeholder="Example: Campus Event Management System"
        className="mb-4 w-full rounded-2xl border border-slate-700 bg-slate-950/70 px-4 py-3 text-sm text-white outline-none transition placeholder:text-slate-600 focus:border-teal-400/70 focus:ring-4 focus:ring-teal-400/10"
      />

      <div className="mb-2 flex items-center justify-between">
        <label className="block text-sm font-semibold text-slate-200">Requirement input editor</label>
        <button
          onClick={() => setRequirements(SAMPLE)}
          className="rounded-full border border-slate-700 px-3 py-1 text-xs font-semibold text-slate-300 transition hover:border-teal-400/70 hover:text-teal-200"
        >
          Use sample
        </button>
      </div>
      <textarea
        value={requirements}
        onChange={(event) => setRequirements(event.target.value)}
        placeholder="Write complete software requirements here..."
        className="min-h-[280px] w-full resize-y rounded-3xl border border-slate-700 bg-slate-950/80 p-4 font-mono text-sm leading-7 text-slate-100 outline-none transition placeholder:text-slate-600 focus:border-teal-400/70 focus:ring-4 focus:ring-teal-400/10"
      />

      <div className="mt-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <p className="text-xs text-slate-500">
          Tip: mention users, modules, database needs, reports, and security rules for better output.
        </p>
        <button
          onClick={onGenerate}
          disabled={loading}
          className="inline-flex items-center justify-center gap-2 rounded-2xl bg-gradient-to-r from-teal-400 to-indigo-500 px-6 py-3 text-sm font-bold text-slate-950 shadow-glow transition hover:scale-[1.01] disabled:cursor-not-allowed disabled:opacity-60"
        >
          <Wand2 size={18} />
          {loading ? "Generating..." : "Generate Architecture"}
        </button>
      </div>
    </section>
  );
}
