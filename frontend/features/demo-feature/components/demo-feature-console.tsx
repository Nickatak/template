'use client';

import { DemoFeatureForm } from './demo-feature-form';
import { useDemoFeatureController } from '../hooks/use-demo-feature-controller';

export function DemoFeatureConsole() {
  // Composition owner: receives route entry and wires controller state/actions into child UI.
  const controllerApi = useDemoFeatureController();

  return (
    <section className="space-y-6 rounded-xl border border-slate-800 bg-slate-900/70 p-6 shadow-2xl shadow-slate-950/40">
      <header className="space-y-2">
        <h1 className="text-2xl font-semibold tracking-tight">Demo Feature Console</h1>
        <p className="text-sm text-slate-300">
          Reference implementation for the route-shim pattern: route file mounts this parent,
          parent owns flow, child handles form rendering.
        </p>
      </header>

      <p className="text-sm text-slate-300">{controllerApi.statusMessage}</p>

      <DemoFeatureForm
        title={controllerApi.title}
        onTitleChange={controllerApi.setTitle}
        details={controllerApi.details}
        onDetailsChange={controllerApi.setDetails}
        fieldErrors={controllerApi.fieldErrors}
        onSubmit={controllerApi.handleSubmit}
      />

      {controllerApi.lastSubmission ? (
        <div className="rounded-lg border border-emerald-600/40 bg-emerald-950/30 p-4">
          <p className="text-sm font-medium text-emerald-300">Last submission</p>
          <p className="mt-1 text-sm text-emerald-100">Title: {controllerApi.lastSubmission.title}</p>
          <p className="text-sm text-emerald-100">Details: {controllerApi.lastSubmission.details || '(none)'}</p>
        </div>
      ) : null}
    </section>
  );
}
