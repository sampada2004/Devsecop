export default {
  testEnvironment: 'node',
  transform: {
    '^.+\.[t|j]sx?$': 'babel-jest'
  },
  transformIgnorePatterns: [
    '/node_modules/(?!(node-fetch|fetch-blob|formdata-polyfill|data-uri-to-buffer|web-streams-polyfill)/)',
  ],
  moduleNameMapper: {
    '^(\.{1,2}/.*)\.js$': '$1',
  },
  collectCoverage: true,
  coverageDirectory: './coverage',
  coverageReporters: ['text', 'lcov', 'clover', 'html'],
  collectCoverageFrom: [
    'TempBackend/**/*.js',
    '!TempBackend/**/*.test.js',
    '!**/node_modules/**',
    '!**/vendor/**'
  ],
  testMatch: ['**/__tests__/**/*.js', '**/?(*.)+(spec|test).js'],
  verbose: true
};
