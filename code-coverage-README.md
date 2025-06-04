# Code Coverage Setup for RITBuddy

This document explains how to use the code coverage setup for both the backend and frontend of the RITBuddy application.

## Overview

Code coverage is a metric that helps you understand how much of your code is being tested. The setup includes:

- Backend: Jest + Supertest for testing Express routes with coverage reporting
- Frontend: Vitest + React Testing Library with coverage reporting

## Prerequisites

Before running the tests, make sure to install the required dependencies as listed in the `install-dependencies.md` file.

## Running Tests with Coverage

### Backend (Express)

From the root directory:

```bash
npm run test:coverage
```

This will:
1. Run all tests in the `TempBackend/__tests__` directory
2. Generate a coverage report in the `coverage` directory
3. Display a summary of the coverage in the terminal

### Frontend (React)

From the Frontend directory:

```bash
cd Frontend
npm run test:coverage
```

This will:
1. Run all tests in the `src/__tests__` directory
2. Generate a coverage report in the `coverage` directory
3. Display a summary of the coverage in the terminal

## Coverage Reports

The coverage reports include:

- **Statement coverage**: Percentage of statements executed
- **Branch coverage**: Percentage of branches (if/else, switch cases) executed
- **Function coverage**: Percentage of functions called
- **Line coverage**: Percentage of lines executed

## Viewing Coverage Reports

### Text Report

The coverage summary is displayed in the terminal after running the tests.

### HTML Report

For a more detailed view, open the HTML report:

- Backend: `coverage/lcov-report/index.html`
- Frontend: `Frontend/coverage/index.html`

## Adding More Tests

To improve coverage:

1. Create test files in the `__tests__` directories
2. Follow the patterns in the existing test files
3. Run the coverage command to see your progress

## Coverage Thresholds

The current setup requires:
- 70% statement coverage
- 70% branch coverage
- 70% function coverage
- 70% line coverage

You can adjust these thresholds in:
- Backend: `jest.config.js`
- Frontend: `vite.config.js`

## Best Practices

1. Write tests for critical functionality first
2. Aim for high coverage in business logic and components
3. Don't obsess over 100% coverage - focus on meaningful tests
4. Use the coverage report to identify untested code paths
