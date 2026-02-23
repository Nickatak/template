import { FormEvent } from 'react';

export type DemoFeatureFieldErrors = {
  title?: string;
};

export type DemoSubmission = {
  title: string;
  details: string;
};

export type DemoFeatureControllerApi = {
  title: string;
  setTitle: (value: string) => void;
  details: string;
  setDetails: (value: string) => void;
  fieldErrors: DemoFeatureFieldErrors;
  statusMessage: string;
  lastSubmission: DemoSubmission | null;
  handleSubmit: (event: FormEvent<HTMLFormElement>) => void;
};

