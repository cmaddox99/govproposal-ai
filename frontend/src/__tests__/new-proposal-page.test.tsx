import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import NewProposalPage from '@/app/(dashboard)/proposals/new/page';

const mockPush = jest.fn();

jest.mock('next/navigation', () => ({
  useRouter: () => ({ push: mockPush, replace: jest.fn() }),
}));

jest.mock('next/link', () => {
  return ({ children, href }: { children: React.ReactNode; href: string }) => (
    <a href={href}>{children}</a>
  );
});

jest.mock('@/lib/api', () => ({
  proposalsApi: {
    create: jest.fn(),
  },
}));

import { proposalsApi } from '@/lib/api';

beforeEach(() => {
  jest.clearAllMocks();
  Storage.prototype.getItem = jest.fn((key) => {
    if (key === 'currentOrgId') return 'org-1';
    return null;
  });
});

describe('NewProposalPage', () => {
  it('renders the form with all fields', () => {
    render(<NewProposalPage />);

    expect(screen.getByText('New Proposal')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Enter proposal title')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Brief description of the proposal')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('e.g., Department of Defense')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('e.g., W911NF-24-R-0001')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('e.g., 541512')).toBeInTheDocument();
  });

  it('has disabled submit button when title is empty', () => {
    render(<NewProposalPage />);
    const submitButton = screen.getByText('Create Proposal');
    expect(submitButton).toBeDisabled();
  });

  it('enables submit button when title is filled', async () => {
    const user = userEvent.setup();
    render(<NewProposalPage />);

    await user.type(screen.getByPlaceholderText('Enter proposal title'), 'Test Proposal');
    expect(screen.getByText('Create Proposal')).toBeEnabled();
  });

  it('submits form and redirects on success', async () => {
    const user = userEvent.setup();
    (proposalsApi.create as jest.Mock).mockResolvedValue({ data: { id: 'new-id' } });

    render(<NewProposalPage />);

    await user.type(screen.getByPlaceholderText('Enter proposal title'), 'My Proposal');
    await user.click(screen.getByText('Create Proposal'));

    await waitFor(() => {
      expect(proposalsApi.create).toHaveBeenCalledWith(
        expect.objectContaining({ title: 'My Proposal', organization_id: 'org-1' })
      );
      expect(mockPush).toHaveBeenCalledWith('/proposals/new-id');
    });
  });

  it('shows error when no org selected', async () => {
    Storage.prototype.getItem = jest.fn(() => null);
    const user = userEvent.setup();

    render(<NewProposalPage />);
    await user.type(screen.getByPlaceholderText('Enter proposal title'), 'Test');
    await user.click(screen.getByText('Create Proposal'));

    await waitFor(() => {
      expect(screen.getByText('No organization selected')).toBeInTheDocument();
    });
  });

  it('shows error on API failure', async () => {
    const user = userEvent.setup();
    (proposalsApi.create as jest.Mock).mockRejectedValue({
      response: { data: { detail: 'Validation failed' } },
    });

    render(<NewProposalPage />);
    await user.type(screen.getByPlaceholderText('Enter proposal title'), 'Test');
    await user.click(screen.getByText('Create Proposal'));

    await waitFor(() => {
      expect(screen.getByText('Validation failed')).toBeInTheDocument();
    });
  });

  it('has cancel link back to proposals', () => {
    render(<NewProposalPage />);
    const cancelLink = screen.getByText('Cancel');
    expect(cancelLink.closest('a')).toHaveAttribute('href', '/proposals');
  });
});
