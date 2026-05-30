/** @type {import('@stryker-mutator/api/core').PartialStrykerOptions} */
export default {
  testRunner: 'vitest',
  coverageAnalysis: 'perTest',
  mutate: [
    'src/**/*.js',
    '!src/__tests__/**',
  ],
  thresholds: {
    high: 80,
    low: 60,
    break: 50,
  },
  reporters: ['html', 'clear-text', 'progress'],
  htmlReporter: {
    fileName: 'stryker-report/mutation-report.html',
  },
};
