'use client';

import { useEffect, type ReactNode } from 'react';
import { usePathname, useRouter } from 'next/navigation';

import { isPublicAuthRoute } from '../features/session/public-routes';
import { useSessionAuthorization } from '../features/session/session-authorization';

type AuthGateProps = {
  children: ReactNode;
};

export function AuthGate({ children }: AuthGateProps) {
  const pathname = usePathname();
  const router = useRouter();
  const { isAuthorized, isChecking } = useSessionAuthorization();
  const isPublicRoute = isPublicAuthRoute(pathname);

  useEffect(() => {
    if (isChecking) {
      return;
    }

    if (isPublicRoute) {
      if (isAuthorized && (pathname === '/login' || pathname === '/register')) {
        router.replace('/dashboard');
      }
      return;
    }

    if (!isAuthorized) {
      router.replace('/login');
    }
  }, [isAuthorized, isChecking, isPublicRoute, pathname, router]);

  if (isPublicRoute) {
    return <>{children}</>;
  }

  if (isChecking) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 to-slate-800">
        <div className="text-slate-200 text-lg">Obtaining session...</div>
      </main>
    );
  }

  if (!isAuthorized) {
    return null;
  }

  return <>{children}</>;
}
