import { render, screen, waitFor } from '@testing-library/react';
import CompliancePage from '@/app/(dashboard)/compliance/page';

jest.mock('@/lib/api', () => ({
  complianceApi: {
    getSummary: jest.fn(),
    listItems: jest.fn(),
    listCertifications: jest.fn(),
  },
}));

import { complianceApi } from '@/lib/api';

const mockSummary = {
  overall_compliance_percentage: 85,
  total_items: 10,
  compliant_items: 7,
  partial_items: 2,
  non_compliant_items: 1,
  action_required: 3,
  total_certifications: 5,
  active_certifications: 4,
};

const mockItems = [
  {
    id: 'ci-1',
    framework: 'far',
    clause_number: '52.204-21',
    title: 'Basic Safeguarding of CUI',
    status: 'compliant',
    evidence_notes: 'Policy documented',
    due_date: null,
  },
  {
    id: 'ci-2',
    framework: 'dfars',
    clause_number: '252.204-7012',
    title: 'Safeguarding Covered Defense Information',
    status: 'partial',
    evidence_notes: null,
    due_date: '2026-06-15',
  },
];

const mockCertifications = [
  {
    id: 'cert-1',
    certification_type: 'sam',
    identifier: 'SAM-12345',
    status: 'compliant',
    expiry_date: '2027-01-01',
    notes: 'Annual renewal',
  },
  {
    id: 'cert-2',
    certification_type: 'cmmc',
    identifier: null,
    status: 'pending_review',
    expiry_date: null,
    notes: 'Level 2 assessment pending',
  },
];

beforeEach(() => {
  jest.clearAllMocks();
  Storage.prototype.getItem = jest.fn((key) => {
    if (key === 'currentOrgId') return 'org-1';
    return null;
  });
});

describe('CompliancePage', () => {
  it('shows loading spinner initially', () => {
    (complianceApi.getSummary as jest.Mock).mockReturnValue(new Promise(() => {}));
    (complianceApi.listItems as jest.Mock).mockReturnValue(new Promise(() => {}));
    (complianceApi.listCertifications as jest.Mock).mockReturnValue(new Promise(() => {}));
    render(<CompliancePage />);
    expect(document.querySelector('.animate-spin')).toBeInTheDocument();
  });

  it('renders summary cards after fetch', async () => {
    (complianceApi.getSummary as jest.Mock).mockResolvedValue({ data: mockSummary });
    (complianceApi.listItems as jest.Mock).mockResolvedValue({ data: { items: mockItems } });
    (complianceApi.listCertifications as jest.Mock).mockResolvedValue({ data: { items: mockCertifications } });

    render(<CompliancePage />);

    await waitFor(() => {
      expect(screen.getByText('85%')).toBeInTheDocument();
    });
    expect(screen.getByText('Overall Compliance')).toBeInTheDocument();
    expect(screen.getByText('7')).toBeInTheDocument();
    expect(screen.getByText('Items Compliant')).toBeInTheDocument();
    expect(screen.getByText('3')).toBeInTheDocument();
    expect(screen.getByText('Action Required')).toBeInTheDocument();
  });

  it('renders compliance items', async () => {
    (complianceApi.getSummary as jest.Mock).mockResolvedValue({ data: mockSummary });
    (complianceApi.listItems as jest.Mock).mockResolvedValue({ data: { items: mockItems } });
    (complianceApi.listCertifications as jest.Mock).mockResolvedValue({ data: { items: mockCertifications } });

    render(<CompliancePage />);

    await waitFor(() => {
      expect(screen.getByText('Basic Safeguarding of CUI')).toBeInTheDocument();
    });
    expect(screen.getByText('Safeguarding Covered Defense Information')).toBeInTheDocument();
  });

  it('renders certifications with correct labels', async () => {
    (complianceApi.getSummary as jest.Mock).mockResolvedValue({ data: mockSummary });
    (complianceApi.listItems as jest.Mock).mockResolvedValue({ data: { items: mockItems } });
    (complianceApi.listCertifications as jest.Mock).mockResolvedValue({ data: { items: mockCertifications } });

    render(<CompliancePage />);

    await waitFor(() => {
      expect(screen.getByText('SAM.gov Registration')).toBeInTheDocument();
    });
    expect(screen.getByText('CMMC Certification')).toBeInTheDocument();
  });

  it('shows empty state when no items', async () => {
    (complianceApi.getSummary as jest.Mock).mockResolvedValue({ data: mockSummary });
    (complianceApi.listItems as jest.Mock).mockResolvedValue({ data: { items: [] } });
    (complianceApi.listCertifications as jest.Mock).mockResolvedValue({ data: { items: [] } });

    render(<CompliancePage />);

    await waitFor(() => {
      expect(screen.getByText('No compliance items tracked yet')).toBeInTheDocument();
      expect(screen.getByText('No certifications tracked yet')).toBeInTheDocument();
    });
  });

  it('shows defaults when no org selected', async () => {
    Storage.prototype.getItem = jest.fn(() => null);
    render(<CompliancePage />);

    await waitFor(() => {
      expect(screen.getByText('0%')).toBeInTheDocument();
    });
  });
});
