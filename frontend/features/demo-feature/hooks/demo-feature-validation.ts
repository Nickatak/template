import { DemoFeatureFieldErrors } from './demo-feature-controller.types';

export function validateDemoFields(title: string): DemoFeatureFieldErrors {
  const nextErrors: DemoFeatureFieldErrors = {};

  if (!title.trim()) {
    nextErrors.title = 'Title is required.';
  }

  return nextErrors;
}

