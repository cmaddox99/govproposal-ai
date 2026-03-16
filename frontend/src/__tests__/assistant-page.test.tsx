import { render, screen, waitFor, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import AssistantPage from '@/app/(dashboard)/assistant/page';

// jsdom doesn't implement scrollIntoView
Element.prototype.scrollIntoView = jest.fn();

jest.mock('@/lib/api', () => ({
  assistantApi: {
    chat: jest.fn(),
    applySection: jest.fn(),
  },
  proposalsApi: {
    list: jest.fn().mockResolvedValue({ data: { proposals: [] } }),
    improve: jest.fn(),
  },
  opportunitiesApi: {
    list: jest.fn().mockResolvedValue({ data: { opportunities: [] } }),
  },
}));

import { assistantApi, proposalsApi, opportunitiesApi } from '@/lib/api';

const mockProposals = [
  { id: 'p1', title: 'Cyber Defense Proposal', status: 'draft' },
  { id: 'p2', title: 'Cloud Migration RFP', status: 'in_progress' },
];

const mockOpportunities = [
  { id: 'o1', title: 'DoD IT Modernization' },
  { id: 'o2', title: 'NASA Data Analytics' },
];

function setupMocks(withOrg = true) {
  jest.clearAllMocks();
  Storage.prototype.getItem = jest.fn((key) => {
    if (withOrg && key === 'selectedOrganization') return JSON.stringify({ id: 'org-1', name: 'Acme' });
    return null;
  });
  (proposalsApi.list as jest.Mock).mockResolvedValue({ data: { proposals: mockProposals } });
  (opportunitiesApi.list as jest.Mock).mockResolvedValue({ data: { opportunities: mockOpportunities } });
}

async function renderAndWait() {
  let result: ReturnType<typeof render>;
  await act(async () => {
    result = render(<AssistantPage />);
  });
  // Wait for async data to settle
  await act(async () => {
    await new Promise((r) => setTimeout(r, 0));
  });
  return result!;
}

beforeEach(() => setupMocks());

describe('AssistantPage', () => {
  it('renders the assistant header', async () => {
    await renderAndWait();
    expect(screen.getByText('AI Assistant')).toBeInTheDocument();
  });

  it('shows welcome message on load', async () => {
    await renderAndWait();
    expect(screen.getByText(/I'm your AI proposal advisor/)).toBeInTheDocument();
  });

  it('renders general suggestion buttons', async () => {
    await renderAndWait();
    expect(screen.getByText('Which opportunities match our capabilities?')).toBeInTheDocument();
    expect(screen.getByText('What proposals need improvement?')).toBeInTheDocument();
  });

  it('renders proposal and opportunity dropdowns', async () => {
    await renderAndWait();
    expect(screen.getByText('No proposal focus')).toBeInTheDocument();
    expect(screen.getByText('No opportunity focus')).toBeInTheDocument();
  });

  it('populates proposal dropdown from API', async () => {
    await renderAndWait();
    expect(screen.getByText(/Cyber Defense Proposal/)).toBeInTheDocument();
    expect(screen.getByText(/Cloud Migration RFP/)).toBeInTheDocument();
  });

  it('populates opportunity dropdown from API', async () => {
    await renderAndWait();
    expect(screen.getByText(/DoD IT Modernization/)).toBeInTheDocument();
    expect(screen.getByText(/NASA Data Analytics/)).toBeInTheDocument();
  });

  it('has a chat input field', async () => {
    await renderAndWait();
    expect(screen.getByPlaceholderText('Ask me anything about government proposals...')).toBeInTheDocument();
  });

  it('sends a message and displays response', async () => {
    const user = userEvent.setup();
    (assistantApi.chat as jest.Mock).mockResolvedValue({
      data: {
        message: 'Here is my analysis of your proposals.',
        context_used: {
          org: true,
          opportunities_count: 5,
          proposals_count: 3,
          focused_proposal: false,
          focused_opportunity: false,
        },
      },
    });

    await renderAndWait();

    const input = screen.getByPlaceholderText('Ask me anything about government proposals...');
    await user.type(input, 'Analyze my proposals');
    await user.keyboard('{Enter}');

    await waitFor(() => {
      expect(screen.getByText('Analyze my proposals')).toBeInTheDocument();
    });

    await waitFor(() => {
      expect(screen.getByText(/Here is my analysis/)).toBeInTheDocument();
    });

    expect(assistantApi.chat).toHaveBeenCalledWith(
      expect.arrayContaining([
        expect.objectContaining({ role: 'user', content: 'Analyze my proposals' }),
      ]),
      expect.objectContaining({ org_id: 'org-1' })
    );
  });

  it('shows error when no org is selected', async () => {
    setupMocks(false);
    const user = userEvent.setup();

    await renderAndWait();

    const input = screen.getByPlaceholderText('Ask me anything about government proposals...');
    await user.type(input, 'Hello');
    await user.keyboard('{Enter}');

    await waitFor(() => {
      expect(screen.getByText(/No organization selected/)).toBeInTheDocument();
    });
  });

  it('shows error on API failure', async () => {
    const user = userEvent.setup();
    (assistantApi.chat as jest.Mock).mockRejectedValue({
      response: { data: { detail: 'Service unavailable' } },
    });

    await renderAndWait();

    const input = screen.getByPlaceholderText('Ask me anything about government proposals...');
    await user.type(input, 'Test message');
    await user.keyboard('{Enter}');

    await waitFor(() => {
      expect(screen.getByText('Service unavailable')).toBeInTheDocument();
    });
  });

  it('shows proposal-specific suggestions when proposal selected', async () => {
    const user = userEvent.setup();
    await renderAndWait();

    const proposalSelect = screen.getAllByRole('combobox')[0];
    await user.selectOptions(proposalSelect, 'p1');

    expect(screen.getByText('What should I improve first?')).toBeInTheDocument();
    expect(screen.getByText('Rewrite the executive summary for 95%+')).toBeInTheDocument();
  });

  it('shows improve all button when proposal selected', async () => {
    const user = userEvent.setup();
    await renderAndWait();

    const proposalSelect = screen.getAllByRole('combobox')[0];
    await user.selectOptions(proposalSelect, 'p1');

    expect(screen.getByText('Improve All Sections')).toBeInTheDocument();
  });

  it('displays context badge on assistant response', async () => {
    const user = userEvent.setup();
    (assistantApi.chat as jest.Mock).mockResolvedValue({
      data: {
        message: 'Response with context info',
        context_used: {
          org: true,
          opportunities_count: 3,
          proposals_count: 2,
          focused_proposal: false,
          focused_opportunity: false,
        },
      },
    });

    await renderAndWait();

    const input = screen.getByPlaceholderText('Ask me anything about government proposals...');
    await user.type(input, 'Test');
    await user.keyboard('{Enter}');

    await waitFor(() => {
      expect(screen.getByText(/Context:/)).toBeInTheDocument();
    });
  });
});
