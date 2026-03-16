import { render, screen, waitFor } from '@testing-library/react';
import DashboardPage from '@/app/(dashboard)/dashboard/page';

jest.mock('next/link', () => {
  return ({ children, href }: { children: React.ReactNode; href: string }) => (
    <a href={href}>{children}</a>
  );
});

jest.mock('@/lib/api', () => ({
  dashboardApi: {
    getDashboard: jest.fn(),
  },
}));

import { dashboardApi } from '@/lib/api';

const mockDashboardData = {
  active_proposals: 5,
  new_opportunities: 12,
  win_rate: 68,
  pending_deadlines: 3,
  pipeline: [
    { status: 'draft', count: 2 },
    { status: 'in_progress', count: 3 },
    { status: 'submitted', count: 1 },
  ],
  recent_proposals: [
    {
      id: '1',
      title: 'DoD Cyber Contract',
      agency: 'Department of Defense',
      status: 'in_progress',
      estimated_value: 2500000,
      due_date: '2026-06-01',
      updated_at: '2026-03-01T00:00:00Z',
    },
  ],
};

beforeEach(() => {
  jest.clearAllMocks();
  Storage.prototype.getItem = jest.fn((key) => {
    if (key === 'currentOrgId') return 'org-1';
    if (key === 'currentOrgName') return 'Acme Corp';
    return null;
  });
});

describe('DashboardPage', () => {
  it('shows loading spinner initially', () => {
    (dashboardApi.getDashboard as jest.Mock).mockReturnValue(new Promise(() => {}));
    render(<DashboardPage />);
    expect(document.querySelector('.animate-spin')).toBeInTheDocument();
  });

  it('renders metrics after data loads', async () => {
    (dashboardApi.getDashboard as jest.Mock).mockResolvedValue({ data: mockDashboardData });
    render(<DashboardPage />);

    await waitFor(() => {
      expect(screen.getByText('5')).toBeInTheDocument();
    });
    expect(screen.getByText('Active Proposals')).toBeInTheDocument();
    expect(screen.getByText('12')).toBeInTheDocument();
    expect(screen.getByText('68%')).toBeInTheDocument();
  });

  it('displays org name in welcome header', async () => {
    (dashboardApi.getDashboard as jest.Mock).mockResolvedValue({ data: mockDashboardData });
    render(<DashboardPage />);

    await waitFor(() => {
      expect(screen.getByText('Acme Corp Dashboard')).toBeInTheDocument();
    });
  });

  it('renders pipeline stages', async () => {
    (dashboardApi.getDashboard as jest.Mock).mockResolvedValue({ data: mockDashboardData });
    render(<DashboardPage />);

    await waitFor(() => {
      expect(screen.getByText('Pipeline Overview')).toBeInTheDocument();
      expect(screen.getAllByText('Draft').length).toBeGreaterThanOrEqual(1);
      expect(screen.getAllByText('In Progress').length).toBeGreaterThanOrEqual(1);
      expect(screen.getAllByText('Submitted').length).toBeGreaterThanOrEqual(1);
    });
  });

  it('renders recent proposals in table', async () => {
    (dashboardApi.getDashboard as jest.Mock).mockResolvedValue({ data: mockDashboardData });
    render(<DashboardPage />);

    await waitFor(() => {
      expect(screen.getByText('DoD Cyber Contract')).toBeInTheDocument();
      expect(screen.getByText('Department of Defense')).toBeInTheDocument();
    });
  });

  it('shows empty state when no org selected', async () => {
    Storage.prototype.getItem = jest.fn(() => null);
    render(<DashboardPage />);

    await waitFor(() => {
      expect(screen.getByText("Here's what's happening with your proposals")).toBeInTheDocument();
    });
  });

  it('shows empty pipeline message when no proposals', async () => {
    (dashboardApi.getDashboard as jest.Mock).mockResolvedValue({
      data: { ...mockDashboardData, pipeline: [], recent_proposals: [] },
    });
    render(<DashboardPage />);

    await waitFor(() => {
      expect(screen.getByText('No proposals in pipeline yet')).toBeInTheDocument();
    });
  });
});
