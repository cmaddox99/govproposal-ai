import { render, screen, waitFor } from '@testing-library/react';
import ProposalsPage from '@/app/(dashboard)/proposals/page';

// Mock next/navigation
jest.mock('next/navigation', () => ({
  useRouter: () => ({ push: jest.fn(), replace: jest.fn() }),
  usePathname: () => '/proposals',
}));

// Mock next/link
jest.mock('next/link', () => {
  return ({ children, href }: { children: React.ReactNode; href: string }) => (
    <a href={href}>{children}</a>
  );
});

// Mock the API module
jest.mock('@/lib/api', () => ({
  proposalsApi: {
    list: jest.fn(),
  },
}));

import { proposalsApi } from '@/lib/api';

const mockProposals = [
  {
    id: '1',
    organization_id: 'org-1',
    title: 'Test Proposal Alpha',
    status: 'draft' as const,
    agency: 'Department of Defense',
    due_date: '2026-06-01',
    estimated_value: 500000,
    created_at: '2026-01-15T00:00:00Z',
    updated_at: '2026-01-15T00:00:00Z',
  },
  {
    id: '2',
    organization_id: 'org-1',
    title: 'Test Proposal Beta',
    status: 'submitted' as const,
    agency: 'NASA',
    due_date: '2026-07-01',
    estimated_value: 1200000,
    created_at: '2026-02-01T00:00:00Z',
    updated_at: '2026-02-01T00:00:00Z',
  },
];

beforeEach(() => {
  jest.clearAllMocks();
  Storage.prototype.getItem = jest.fn((key) => {
    if (key === 'currentOrgId') return 'org-1';
    if (key === 'token') return 'fake-token';
    return null;
  });
});

describe('ProposalsPage', () => {
  it('renders loading state initially', () => {
    (proposalsApi.list as jest.Mock).mockReturnValue(new Promise(() => {}));
    render(<ProposalsPage />);
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it('renders proposals after fetch', async () => {
    (proposalsApi.list as jest.Mock).mockResolvedValue({
      data: { proposals: mockProposals, total: 2, limit: 20, offset: 0 },
    });

    render(<ProposalsPage />);

    await waitFor(() => {
      expect(screen.getByText('Test Proposal Alpha')).toBeInTheDocument();
    });

    expect(screen.getByText('Test Proposal Beta')).toBeInTheDocument();
  });

  it('shows error when no organization is selected', async () => {
    Storage.prototype.getItem = jest.fn(() => null);

    render(<ProposalsPage />);

    await waitFor(() => {
      expect(screen.getByText(/no organization selected/i)).toBeInTheDocument();
    });
  });

  it('displays correct status labels', async () => {
    (proposalsApi.list as jest.Mock).mockResolvedValue({
      data: { proposals: mockProposals, total: 2, limit: 20, offset: 0 },
    });

    render(<ProposalsPage />);

    await waitFor(() => {
      expect(screen.getByText('Draft')).toBeInTheDocument();
      expect(screen.getByText('Submitted')).toBeInTheDocument();
    });
  });
});
