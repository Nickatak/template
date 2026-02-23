'use client';

import { FormEventHandler } from 'react';

import type { DemoFeatureFieldErrors } from '../hooks/use-demo-feature-controller';

type DemoFeatureFormProps = {
  title: string;
  onTitleChange: (value: string) => void;
  details: string;
  onDetailsChange: (value: string) => void;
  fieldErrors: DemoFeatureFieldErrors;
  onSubmit: FormEventHandler<HTMLFormElement>;
};

export function DemoFeatureForm({
  title,
  onTitleChange,
  details,
  onDetailsChange,
  fieldErrors,
  onSubmit,
}: DemoFeatureFormProps) {
  return (
    <form className="space-y-4" onSubmit={onSubmit}>
      <label className="block space-y-1">
        <span className="text-sm font-medium text-slate-200">Title</span>
        <input
          className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 outline-none ring-sky-500/50 focus:ring"
          name="title"
          value={title}
          onChange={(event) => onTitleChange(event.target.value)}
          placeholder="Example: Route shim pattern"
          required
        />
        {fieldErrors.title ? <p className="text-sm text-rose-300">{fieldErrors.title}</p> : null}
      </label>

      <label className="block space-y-1">
        <span className="text-sm font-medium text-slate-200">Details</span>
        <textarea
          className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 outline-none ring-sky-500/50 focus:ring"
          name="details"
          rows={3}
          value={details}
          onChange={(event) => onDetailsChange(event.target.value)}
          placeholder="Optional details"
        />
      </label>

      <button
        className="rounded-md bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-500"
        type="submit"
      >
        Submit Demo
      </button>
    </form>
  );
}
