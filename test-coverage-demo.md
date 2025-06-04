# RITBuddy Test Coverage Demo

## Setup Overview
1. **Frontend Testing**: Vitest + React Testing Library
2. **Backend Testing**: Jest + Supertest

## Frontend Testing Demo
1. Show test files in `Frontend/src/__tests__/` directory
2. Run `npm run test:coverage` in the Frontend directory
3. Explain the coverage report
4. Highlight InputSection component with 87% coverage
5. Show test implementation for InputSection

## Backend Testing 
1. Show test files in `TempBackend/__tests__/` directory
2. Run `npm run test:coverage` in the root directory
3. Explain the coverage report
4. Show the placeholder tests and explain future improvements

## MongoDB Integration
1. Show the MongoDB connection in MainServer.js
2. Demonstrate CRUD operations through the API:
   - Create: POST /api/ask
   - Read: GET /api/history
   - Delete: DELETE /api/history/:id

## Documentation
1. Show install-dependencies.md
2. Show code-coverage-README.md

## Future Improvements
1. Enhance test coverage for all components
2. Implement actual API tests with supertest
3. Add more edge case testing
