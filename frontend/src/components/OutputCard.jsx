import { ActionButton } from "./ActionButton.jsx";

export function OutputCard({ title, children, rawText, filename }) {
  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-950/55 p-5">
      <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <h3 className="text-base font-bold text-white">{title}</h3>
        {rawText ? <ActionButton text={rawText} filename={filename} /> : null}
      </div>
      {children}
    </div>
  );
}
