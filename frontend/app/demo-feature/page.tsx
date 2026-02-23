import { DemoFeatureConsole } from '../../features/demo-feature';

export default function DemoFeaturePage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto max-w-3xl p-8">
        <DemoFeatureConsole />
      </div>
    </main>
  );
}
