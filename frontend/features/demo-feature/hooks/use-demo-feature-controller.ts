'use client';

import { FormEvent, useState } from 'react';

export type DemoFeatureFieldErrors = {
  title?: string;
};

type DemoSubmission = {
  title: string;
  details: string;
};

function validateDemoFields(title: string): DemoFeatureFieldErrors {
  const nextErrors: DemoFeatureFieldErrors = {};

  if (!title.trim()) {
    nextErrors.title = 'Title is required.';
  }

  return nextErrors;
}

export function useDemoFeatureController() {
  const [title, setTitle] = useState('');
  const [details, setDetails] = useState('');
  const [fieldErrors, setFieldErrors] = useState<DemoFeatureFieldErrors>({});
  const [statusMessage, setStatusMessage] = useState(
    'Fill out the form and submit to see controller-owned state updates.',
  );
  const [lastSubmission, setLastSubmission] = useState<DemoSubmission | null>(null);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const nextErrors = validateDemoFields(title);
    setFieldErrors(nextErrors);

    if (Object.keys(nextErrors).length > 0) {
      setStatusMessage('Fix the required field and submit again.');
      return;
    }

    const submission = {
      title: title.trim(),
      details: details.trim(),
    };

    setLastSubmission(submission);
    setStatusMessage('Demo submission saved in local feature state.');
    setTitle('');
    setDetails('');
    setFieldErrors({});
  }

  return {
    title,
    setTitle,
    details,
    setDetails,
    fieldErrors,
    statusMessage,
    lastSubmission,
    handleSubmit,
  };
}
