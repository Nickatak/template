'use client';

import { DemoFeatureForm } from './demo-feature-form';
import { useDemoFeatureController } from '../hooks/use-demo-feature-controller';

export function DemoFeatureConsole() {
  // Composition owner: receives route entry and wires controller state/actions into child UI.
  const controller = useDemoFeatureController();

  return (
    <section className="space-y-6 rounded-xl border border-slate-800 bg-slate-900/70 p-6 shadow-2xl shadow-slate-950/40">
      <header className="space-y-2">
        <h1 className="text-2xl font-semibold tracking-tight">Demo Feature Console</h1>
        <p className="text-sm text-slate-300">
          Reference implementation for the route-shim pattern: route file mounts this parent,
          parent owns flow, child handles form rendering.
        </p>
      </header>

      <p className="text-sm text-slate-300">{controller.statusMessage}</p>

      <DemoFeatureForm
        title={controller.title}
        onTitleChange={controller.setTitle}
        details={controller.details}
        onDetailsChange={controller.setDetails}
        fieldErrors={controller.fieldErrors}
        onSubmit={controller.handleSubmit}
      />

      {controller.lastSubmission ? (
        <div className="rounded-lg border border-emerald-600/40 bg-emerald-950/30 p-4">
          <p className="text-sm font-medium text-emerald-300">Last submission</p>
          <p className="mt-1 text-sm text-emerald-100">Title: {controller.lastSubmission.title}</p>
          <p className="text-sm text-emerald-100">Details: {controller.lastSubmission.details || '(none)'}</p>
        </div>
      ) : null}
    </section>
  );
}
