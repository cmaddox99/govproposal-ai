import { render, screen, waitFor } from '@testing-library/react';
import ProposalDetailPage from '@/app/(dashboard)/proposals/[id]/page';

jest.mock('next/navigation', () => ({
  useRouter: () => ({ push: jest.fn(), replace: jest.fn(), back: jest.fn() }),
  useParams: () => ({ id: 'proposal-123' }),
}));

jest.mock('next/link', () => {
  return ({ children, href }: { children: React.ReactNode; href: string }) => (
    <a href={href}>{children}</a>
  );
});

jest.mock('@/lib/api', () => ({
  proposalsApi: {
    get: jest.fn(),
    update: jest.fn(),
    delete: jest.fn(),
    generateContent: jest.fn(),
    generateSection: jest.fn(),
    exportDocx: jest.fn(),
  },
}));

import { proposalsApi } from '@/lib/api';

const mockProposal = {
  id: 'proposal-123',
  organization_id: 'org-1',
  title: 'Test Proposal',
  description: 'A test proposal',
  status: 'draft' as const,
  agency: 'NASA',
  solicitation_number: 'SOL-001',
  naics_code: '541512',
  due_date: '2026-06-01T00:00:00Z',
  estimated_value: 500000,
  proposed_value: null,
  executive_summary: 'Summary text',
  technical_approach: '',
  management_approach: '',
  past_performance: '',
  pricing_summary: '',
  created_at: '2026-01-01T00:00:00Z',
  updated_at: '2026-01-01T00:00:00Z',
};

beforeEach(() => {
  jest.clearAllMocks();
  Storage.prototype.getItem = jest.fn((key) => {
    if (key === 'currentOrgId') return 'org-1';
    if (key === 'token') return 'fake-token';
    return null;
  });
});

describe('ProposalDetailPage', () => {
  it('shows loading state initially', () => {
    (proposalsApi.get as jest.Mock).mockReturnValue(new Promise(() => {}));
    render(<ProposalDetailPage />);
    expect(screen.getByText('Loading proposal...')).toBeInTheDocument();
  });

  it('renders proposal details after fetch', async () => {
    (proposalsApi.get as jest.Mock).mockResolvedValue({ data: mockProposal });
    render(<ProposalDetailPage />);

    await waitFor(() => {
      expect(screen.getByDisplayValue('Test Proposal')).toBeInTheDocument();
    });
  });

  it('shows status badge', async () => {
    (proposalsApi.get as jest.Mock).mockResolvedValue({ data: mockProposal });
    render(<ProposalDetailPage />);

    await waitFor(() => {
      const badges = screen.getAllByText('Draft');
      expect(badges.length).toBeGreaterThanOrEqual(1);
    });
  });

  it('renders overview and content tabs', async () => {
    (proposalsApi.get as jest.Mock).mockResolvedValue({ data: mockProposal });
    render(<ProposalDetailPage />);

    await waitFor(() => {
      expect(screen.getByText('Overview')).toBeInTheDocument();
      expect(screen.getByText('Content')).toBeInTheDocument();
    });
  });

  it('shows error on fetch failure', async () => {
    (proposalsApi.get as jest.Mock).mockRejectedValue({
      response: { data: { detail: 'Not found' } },
    });
    render(<ProposalDetailPage />);

    await waitFor(() => {
      expect(screen.getByText('Not found')).toBeInTheDocument();
    });
  });
});
