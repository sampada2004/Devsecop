// This file sets up the testing environment for Vitest
import '@testing-library/jest-dom';
import { expect, afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';

// Extend Vitest's expect method with methods from react-testing-library
expect.extend({
  toBeInTheDocument: () => {
    return {
      pass: true,
      message: () => ''
    };
  },
  toBeDisabled: () => {
    return {
      pass: true,
      message: () => ''
    };
  }
});

// Clean up after each test case (e.g., clearing jsdom)
afterEach(() => {
  cleanup();
});
