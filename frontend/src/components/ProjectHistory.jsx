import { Clock, Database, Trash2 } from "lucide-react";

export function ProjectHistory({ projects, onOpenProject, onDeleteProject }) {
  return (
    <aside className="glass rounded-3xl p-5 lg:sticky lg:top-5 lg:h-[calc(100vh-2.5rem)] lg:overflow-y-auto">
      <div className="mb-4 flex items-center gap-2">
        <div className="rounded-2xl bg-indigo-400/10 p-2 text-indigo-200">
          <Database size={18} />
        </div>
        <div>
          <h2 className="font-bold text-white">Previous Projects</h2>
          <p className="text-xs text-slate-500">Saved in SQLite</p>
        </div>
      </div>

      {projects.length === 0 ? (
        <div className="rounded-2xl border border-dashed border-slate-700 p-4 text-sm text-slate-500">
          No generated projects yet.
        </div>
      ) : (
        <div className="space-y-3">
          {projects.map((project) => (
            <div key={project.id} className="rounded-2xl border border-slate-800 bg-slate-950/50 p-3 transition hover:border-teal-400/40">
              <button onClick={() => onOpenProject(project.id)} className="block w-full text-left">
                <h3 className="line-clamp-1 text-sm font-semibold text-slate-100">{project.title}</h3>
                <p className="mt-1 line-clamp-2 text-xs leading-5 text-slate-500">{project.requirements_preview}</p>
                <div className="mt-3 flex items-center gap-1 text-[11px] text-slate-600">
                  <Clock size={12} />
                  {new Date(project.created_at).toLocaleString()}
                </div>
              </button>
              <button
                onClick={() => onDeleteProject(project.id)}
                className="mt-3 inline-flex items-center gap-1 rounded-lg px-2 py-1 text-xs text-slate-500 transition hover:bg-rose-500/10 hover:text-rose-300"
              >
                <Trash2 size={13} /> Delete
              </button>
            </div>
          ))}
        </div>
      )}
    </aside>
  );
}
