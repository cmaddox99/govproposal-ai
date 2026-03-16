import { render, screen, waitFor } from '@testing-library/react';
import ScoringPage from '@/app/(dashboard)/proposals/[id]/scoring/page';

jest.mock('next/navigation', () => ({
  useParams: () => ({ id: 'proposal-123' }),
}));

// Mock scoring components
jest.mock('@/components/scoring/score-gauge', () => ({
  ScoreGauge: ({ score }: { score: number }) => <div data-testid="score-gauge">Score: {score}</div>,
}));
jest.mock('@/components/scoring/factor-breakdown', () => ({
  FactorBreakdown: () => <div data-testid="factor-breakdown">Factor Breakdown</div>,
}));
jest.mock('@/components/scoring/improvement-list', () => ({
  ImprovementList: () => <div data-testid="improvement-list">Improvements</div>,
}));
jest.mock('@/components/scoring/readiness-badge', () => ({
  ReadinessBadge: ({ level }: { level: string }) => <div data-testid="readiness-badge">{level}</div>,
}));
jest.mock('@/components/scoring/go-nogo-card', () => ({
  GoNoGoCard: () => <div data-testid="go-nogo-card">Go/No-Go</div>,
}));

jest.mock('@/lib/api', () => ({
  scoringApi: {
    getScore: jest.fn(),
    getImprovements: jest.fn(),
    getGoNoGo: jest.fn(),
    getReadiness: jest.fn(),
    calculateScore: jest.fn(),
    checkReadiness: jest.fn(),
  },
}));

import { scoringApi } from '@/lib/api';

const mockScore = {
  id: 'score-1',
  proposal_id: 'proposal-123',
  score_date: '2026-03-01T00:00:00Z',
  overall_score: 87,
  confidence_level: 'high',
  ai_model_used: 'claude',
  created_by: 'user-1',
  created_at: '2026-03-01T00:00:00Z',
  factors: [
    { id: 'f1', factor_type: 'completeness', factor_weight: 0.3, raw_score: 90, weighted_score: 27, evidence_summary: null, improvement_suggestions: null },
  ],
};

const mockGoNoGo = {
  proposal_id: 'proposal-123',
  overall_score: 87,
  readiness_level: 'go',
  recommendation: 'Proceed with submission',
  key_strengths: ['Strong technical approach'],
  key_risks: ['Tight timeline'],
  next_steps: ['Final review'],
};

beforeEach(() => {
  jest.clearAllMocks();
});

describe('ScoringPage', () => {
  it('shows loading state initially', () => {
    (scoringApi.getScore as jest.Mock).mockReturnValue(new Promise(() => {}));
    (scoringApi.getImprovements as jest.Mock).mockReturnValue(new Promise(() => {}));
    (scoringApi.getGoNoGo as jest.Mock).mockReturnValue(new Promise(() => {}));
    render(<ScoringPage />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('renders score overview after fetch', async () => {
    (scoringApi.getScore as jest.Mock).mockResolvedValue({ data: mockScore });
    (scoringApi.getImprovements as jest.Mock).mockResolvedValue({ data: null });
    (scoringApi.getGoNoGo as jest.Mock).mockResolvedValue({ data: mockGoNoGo });
    (scoringApi.getReadiness as jest.Mock).mockRejectedValue(new Error('none'));

    render(<ScoringPage />);

    await waitFor(() => {
      expect(screen.getByTestId('score-gauge')).toBeInTheDocument();
    });
    expect(screen.getByText('Score: 87')).toBeInTheDocument();
    expect(screen.getByTestId('go-nogo-card')).toBeInTheDocument();
  });

  it('shows no score message when no score calculated', async () => {
    (scoringApi.getScore as jest.Mock).mockResolvedValue({ data: null });
    (scoringApi.getImprovements as jest.Mock).mockResolvedValue({ data: null });
    (scoringApi.getGoNoGo as jest.Mock).mockResolvedValue({ data: null });
    (scoringApi.getReadiness as jest.Mock).mockRejectedValue(new Error('none'));

    render(<ScoringPage />);

    await waitFor(() => {
      expect(screen.getByText('No score calculated yet')).toBeInTheDocument();
    });
  });

  it('renders tabs', async () => {
    (scoringApi.getScore as jest.Mock).mockResolvedValue({ data: null });
    (scoringApi.getImprovements as jest.Mock).mockResolvedValue({ data: null });
    (scoringApi.getGoNoGo as jest.Mock).mockResolvedValue({ data: null });
    (scoringApi.getReadiness as jest.Mock).mockRejectedValue(new Error('none'));

    render(<ScoringPage />);

    await waitFor(() => {
      expect(screen.getByText('Score Overview')).toBeInTheDocument();
      expect(screen.getByText('Improvements')).toBeInTheDocument();
      expect(screen.getByText('Readiness')).toBeInTheDocument();
    });
  });

  it('shows calculate score button', () => {
    (scoringApi.getScore as jest.Mock).mockReturnValue(new Promise(() => {}));
    (scoringApi.getImprovements as jest.Mock).mockReturnValue(new Promise(() => {}));
    (scoringApi.getGoNoGo as jest.Mock).mockReturnValue(new Promise(() => {}));
    render(<ScoringPage />);
    expect(screen.getByText('Calculate Score')).toBeInTheDocument();
  });

  it('displays proposal ID', () => {
    (scoringApi.getScore as jest.Mock).mockReturnValue(new Promise(() => {}));
    (scoringApi.getImprovements as jest.Mock).mockReturnValue(new Promise(() => {}));
    (scoringApi.getGoNoGo as jest.Mock).mockReturnValue(new Promise(() => {}));
    render(<ScoringPage />);
    expect(screen.getByText(/Proposal ID:/)).toBeInTheDocument();
  });
});
