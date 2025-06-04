# Installing Testing Dependencies

To complete the code coverage setup, you'll need to install the following dependencies:

## Backend Dependencies

Run this command in the root directory (`c:\College\RITBuddy\RITBuddy`):

```bash
npm install --save-dev jest supertest @babel/preset-env @babel/register c8 cross-env
```

## Frontend Dependencies

Run this command in the Frontend directory (`c:\College\RITBuddy\RITBuddy\Frontend`):

```bash
npm install --save-dev vitest jsdom @testing-library/react @testing-library/jest-dom @vitest/coverage-v8
```

After installing these dependencies, you can run the code coverage tests with the following commands:

## For Backend

```bash
npm run test:coverage
```

## For Frontend

```bash
cd Frontend
npm run test:coverage
```

The coverage reports will be generated in the `coverage` directory of each project.
