'use client';

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-slate-900 to-slate-800">
      <div className="text-center">
        <h1 className="text-5xl font-bold text-white mb-4">Welcome to Pantry</h1>
        <p className="text-xl text-slate-300 mb-8">Your authenticated workspace is ready.</p>
      </div>
    </main>
  );
}
