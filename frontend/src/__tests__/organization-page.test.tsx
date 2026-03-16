import { render, screen, waitFor } from '@testing-library/react';
import OrganizationPage from '@/app/(dashboard)/organization/page';

jest.mock('@/lib/api', () => ({
  pastPerformanceApi: {
    list: jest.fn().mockResolvedValue({ data: [] }),
    create: jest.fn(),
    update: jest.fn(),
    delete: jest.fn(),
  },
}));

const mockOrgData = {
  id: 'org-1',
  name: 'Acme Corp',
  slug: 'acme-corp',
  contact_email: 'info@acme.com',
  phone: '555-1234',
  address: '123 Main St',
  uei_number: 'UEI123',
  cage_code: 'CAGE1',
  duns_number: 'DUNS123',
  naics_codes: ['541512', '541511'],
  capabilities_summary: 'IT solutions provider',
  capabilities: [{ name: 'Cloud', description: 'AWS/Azure services' }],
};

beforeEach(() => {
  jest.clearAllMocks();
  Storage.prototype.getItem = jest.fn((key) => {
    if (key === 'currentOrgId') return 'org-1';
    if (key === 'token') return 'fake-token';
    return null;
  });

  global.fetch = jest.fn().mockResolvedValue({
    ok: true,
    json: () => Promise.resolve(mockOrgData),
  }) as jest.Mock;
});

afterEach(() => {
  (global.fetch as jest.Mock).mockRestore();
});

describe('OrganizationPage', () => {
  it('shows loading state initially', () => {
    global.fetch = jest.fn().mockReturnValue(new Promise(() => {})) as jest.Mock;
    render(<OrganizationPage />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('renders organization details after fetch', async () => {
    render(<OrganizationPage />);

    await waitFor(() => {
      expect(screen.getByText('Organization Details')).toBeInTheDocument();
    });
    expect(screen.getByDisplayValue('Acme Corp')).toBeInTheDocument();
    expect(screen.getByDisplayValue('info@acme.com')).toBeInTheDocument();
    expect(screen.getByDisplayValue('555-1234')).toBeInTheDocument();
  });

  it('renders government credentials', async () => {
    render(<OrganizationPage />);

    await waitFor(() => {
      expect(screen.getByText('Government Credentials')).toBeInTheDocument();
    });
    expect(screen.getByDisplayValue('UEI123')).toBeInTheDocument();
    expect(screen.getByDisplayValue('CAGE1')).toBeInTheDocument();
    expect(screen.getByDisplayValue('DUNS123')).toBeInTheDocument();
  });

  it('renders NAICS codes', async () => {
    render(<OrganizationPage />);

    await waitFor(() => {
      expect(screen.getByText('541512')).toBeInTheDocument();
      expect(screen.getByText('541511')).toBeInTheDocument();
    });
  });

  it('renders capabilities section', async () => {
    render(<OrganizationPage />);

    await waitFor(() => {
      expect(screen.getByText('Company Capabilities')).toBeInTheDocument();
    });
    expect(screen.getByDisplayValue('IT solutions provider')).toBeInTheDocument();
  });

  it('shows error when no org selected', async () => {
    Storage.prototype.getItem = jest.fn(() => null);
    render(<OrganizationPage />);

    await waitFor(() => {
      expect(screen.getByText('No organization selected')).toBeInTheDocument();
    });
  });

  it('renders save button', async () => {
    render(<OrganizationPage />);

    await waitFor(() => {
      expect(screen.getByText('Save Changes')).toBeInTheDocument();
    });
  });

  it('renders past performance section', async () => {
    render(<OrganizationPage />);

    await waitFor(() => {
      expect(screen.getByText('Past Performance')).toBeInTheDocument();
      expect(screen.getByText('Add Record')).toBeInTheDocument();
    });
  });
});
