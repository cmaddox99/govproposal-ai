import { render, screen, waitFor } from '@testing-library/react';
import AnalyticsPage from '@/app/(dashboard)/analytics/page';

jest.mock('@/lib/api', () => ({
  dashboardApi: {
    getAnalytics: jest.fn(),
  },
}));

import { dashboardApi } from '@/lib/api';

const mockAnalytics = {
  active_proposals: 8,
  new_opportunities: 15,
  win_rate: 72,
  pending_deadlines: 4,
  total_contract_value: 5500000,
  total_submitted: 20,
  average_score: 85,
  pipeline: [
    { status: 'draft', count: 3 },
    { status: 'submitted', count: 5 },
    { status: 'awarded', count: 2 },
  ],
  recent_proposals: [],
};

beforeEach(() => {
  jest.clearAllMocks();
  Storage.prototype.getItem = jest.fn((key) => {
    if (key === 'currentOrgId') return 'org-1';
    return null;
  });
});

describe('AnalyticsPage', () => {
  it('shows loading spinner initially', () => {
    (dashboardApi.getAnalytics as jest.Mock).mockReturnValue(new Promise(() => {}));
    render(<AnalyticsPage />);
    expect(document.querySelector('.animate-spin')).toBeInTheDocument();
  });

  it('renders metric cards after fetch', async () => {
    (dashboardApi.getAnalytics as jest.Mock).mockResolvedValue({ data: mockAnalytics });
    render(<AnalyticsPage />);

    await waitFor(() => {
      expect(screen.getByText('72%')).toBeInTheDocument();
    });
    expect(screen.getByText('Win Rate')).toBeInTheDocument();
    expect(screen.getByText('$5.5M')).toBeInTheDocument();
    expect(screen.getByText('Total Contract Value')).toBeInTheDocument();
    expect(screen.getByText('20')).toBeInTheDocument();
    expect(screen.getByText('85')).toBeInTheDocument();
  });

  it('renders pipeline breakdown', async () => {
    (dashboardApi.getAnalytics as jest.Mock).mockResolvedValue({ data: mockAnalytics });
    render(<AnalyticsPage />);

    await waitFor(() => {
      expect(screen.getByText('Pipeline Breakdown')).toBeInTheDocument();
      expect(screen.getByText('Draft')).toBeInTheDocument();
      expect(screen.getByText('Submitted')).toBeInTheDocument();
      expect(screen.getByText('Awarded')).toBeInTheDocument();
    });
  });

  it('shows empty pipeline message when no data', async () => {
    (dashboardApi.getAnalytics as jest.Mock).mockResolvedValue({
      data: { ...mockAnalytics, pipeline: [] },
    });
    render(<AnalyticsPage />);

    await waitFor(() => {
      expect(screen.getByText('No proposals to analyze yet')).toBeInTheDocument();
    });
  });

  it('renders default data when no org selected', async () => {
    Storage.prototype.getItem = jest.fn(() => null);
    render(<AnalyticsPage />);

    await waitFor(() => {
      expect(screen.getByText('0%')).toBeInTheDocument();
      expect(screen.getByText('$0')).toBeInTheDocument();
    });
  });
});
