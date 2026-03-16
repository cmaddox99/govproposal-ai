import { render, screen } from '@testing-library/react';
import SecurityPage from '@/app/(dashboard)/security/page';

describe('SecurityPage', () => {
  it('renders all security sections', () => {
    render(<SecurityPage />);

    expect(screen.getByText('Security')).toBeInTheDocument();
    expect(screen.getByText('Two-Factor Authentication')).toBeInTheDocument();
    expect(screen.getByText('API Keys')).toBeInTheDocument();
    expect(screen.getByText('Active Sessions')).toBeInTheDocument();
    expect(screen.getByText('Login History')).toBeInTheDocument();
  });

  it('renders enable 2FA button', () => {
    render(<SecurityPage />);
    expect(screen.getByText('Enable 2FA')).toBeInTheDocument();
  });

  it('shows active session count', () => {
    render(<SecurityPage />);
    expect(screen.getByText('1 active session')).toBeInTheDocument();
  });

  it('renders manage keys and view history buttons', () => {
    render(<SecurityPage />);
    expect(screen.getByText('Manage Keys')).toBeInTheDocument();
    expect(screen.getByText('View History')).toBeInTheDocument();
  });
});
