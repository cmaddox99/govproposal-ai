import axios from 'axios';

const API_BASE_URL = 'https://backend-production-d1d1.up.railway.app';

console.log('API Base URL:', API_BASE_URL);

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 second timeout
});

// Auto-add auth token to all requests
api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('token');
    console.log('Request interceptor - Token exists:', !!token);
    console.log('Request URL:', config.baseURL + config.url);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// Auto-redirect on 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('refreshToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authApi = {
  login: (email: string, password: string) =>
    api.post('/api/v1/auth/login', { email, password }),
  register: (email: string, password: string) =>
    api.post('/api/v1/auth/register', { email, password }),
  refresh: (refreshToken: string) =>
    api.post('/api/v1/auth/refresh', { refresh_token: refreshToken }),
  me: () => api.get('/api/v1/auth/me'),
  changePassword: (currentPassword: string, newPassword: string) =>
    api.post('/api/v1/auth/password/change', {
      current_password: currentPassword,
      new_password: newPassword,
    }),
  // MFA
  setupMfa: () => api.post('/api/v1/auth/mfa/setup'),
  verifyMfaSetup: (code: string) =>
    api.post('/api/v1/auth/mfa/verify', { code }),
  mfaChallenge: (mfaToken: string, code: string) =>
    api.post('/api/v1/auth/mfa/challenge', { mfa_token: mfaToken, code }),
  useRecoveryCode: (mfaToken: string, recoveryCode: string) =>
    api.post('/api/v1/auth/mfa/recovery', {
      mfa_token: mfaToken,
      recovery_code: recoveryCode,
    }),
  regenerateRecoveryCodes: () =>
    api.post('/api/v1/auth/mfa/recovery-codes/regenerate'),
  disableMfa: (password: string) =>
    api.post('/api/v1/auth/mfa/disable', { password }),
};

// Organizations API
export const organizationsApi = {
  list: () => api.get('/api/v1/organizations'),
  create: (name: string, slug: string) =>
    api.post('/api/v1/organizations', { name, slug }),
  get: (orgId: string) => api.get(`/api/v1/organizations/${orgId}`),
  getMembers: (orgId: string) =>
    api.get(`/api/v1/organizations/${orgId}/members`),
};

// Organization Admin API
export const orgAdminApi = {
  listUsers: (orgId: string) => api.get(`/api/v1/organizations/${orgId}/users`),
  inviteUser: (orgId: string, email: string, role: string) =>
    api.post(`/api/v1/organizations/${orgId}/users/invite`, { email, role }),
  changeRole: (orgId: string, userId: string, role: string) =>
    api.put(`/api/v1/organizations/${orgId}/users/${userId}/role`, { role }),
  removeUser: (orgId: string, userId: string) =>
    api.delete(`/api/v1/organizations/${orgId}/users/${userId}`),
  getAuditLogs: (orgId: string, params?: Record<string, unknown>) =>
    api.get(`/api/v1/organizations/${orgId}/audit-logs`, { params }),
};

// Platform Admin API
export const platformApi = {
  listTenants: () => api.get('/api/v1/platform/tenants'),
  getTenant: (orgId: string) => api.get(`/api/v1/platform/tenants/${orgId}`),
  updateTenantStatus: (orgId: string, isActive: boolean) =>
    api.put(`/api/v1/platform/tenants/${orgId}/status`, { is_active: isActive }),
  getFeatures: () => api.get('/api/v1/platform/features'),
  updateFeature: (feature: string, enabled: boolean) =>
    api.put(`/api/v1/platform/features/${feature}`, { enabled }),
  getAuditLogs: (params?: Record<string, unknown>) =>
    api.get('/api/v1/platform/audit-logs', { params }),
};

// Scoring API
export const scoringApi = {
  calculateScore: (proposalId: string, forceRecalculate = false) =>
    api.post(`/api/v1/proposals/${proposalId}/score/calculate`, {
      force_recalculate: forceRecalculate,
    }),
  getScore: (proposalId: string) =>
    api.get(`/api/v1/proposals/${proposalId}/score`),
  getScoreHistory: (proposalId: string, limit = 10) =>
    api.get(`/api/v1/proposals/${proposalId}/score/history`, {
      params: { limit },
    }),
  getImprovements: (proposalId: string) =>
    api.get(`/api/v1/proposals/${proposalId}/score/improvements`),
  getBenchmarks: (proposalId: string) =>
    api.get(`/api/v1/proposals/${proposalId}/score/benchmarks`),
  calculateBenchmarks: (proposalId: string) =>
    api.post(`/api/v1/proposals/${proposalId}/score/benchmarks/calculate`),
  getReadiness: (proposalId: string, teamType: string) =>
    api.get(`/api/v1/proposals/${proposalId}/score/readiness/${teamType}`),
  checkReadiness: (proposalId: string, teamType: string, forceRecheck = false) =>
    api.post(`/api/v1/proposals/${proposalId}/score/readiness/${teamType}/check`, {
      force_recheck: forceRecheck,
    }),
  getGoNoGo: (proposalId: string) =>
    api.get(`/api/v1/proposals/${proposalId}/score/go-no-go`),
};

// Proposals API
export const proposalsApi = {
  list: (params?: { org_id?: string; status_filter?: string; limit?: number; offset?: number }) =>
    api.get('/api/v1/proposals', { params }),
  get: (proposalId: string) =>
    api.get(`/api/v1/proposals/${proposalId}`),
  create: (data: {
    organization_id: string;
    title: string;
    description?: string;
    solicitation_number?: string;
    agency?: string;
    naics_code?: string;
    due_date?: string;
    estimated_value?: number;
  }) => api.post('/api/v1/proposals', data),
  update: (proposalId: string, data: Record<string, any>) =>
    api.put(`/api/v1/proposals/${proposalId}`, data),
  delete: (proposalId: string) =>
    api.delete(`/api/v1/proposals/${proposalId}`),
  createFromOpportunity: (data: { opportunity_id: string; organization_id: string; generate_all_content?: boolean }) =>
    api.post('/api/v1/proposals/from-opportunity', data),
  generateContent: (proposalId: string, sections?: string[]) =>
    api.post(`/api/v1/proposals/${proposalId}/generate`, { sections: sections || null }, { timeout: 120000 }),
  exportDocx: (proposalId: string) =>
    api.get(`/api/v1/proposals/${proposalId}/export?format=docx`, { responseType: 'blob' }),
};

// Past Performance API
export const pastPerformanceApi = {
  list: (orgId: string) =>
    api.get(`/api/v1/organizations/${orgId}/past-performance`),
  create: (orgId: string, data: Record<string, any>) =>
    api.post(`/api/v1/organizations/${orgId}/past-performance`, data),
  update: (orgId: string, ppId: string, data: Record<string, any>) =>
    api.put(`/api/v1/organizations/${orgId}/past-performance/${ppId}`, data),
  delete: (orgId: string, ppId: string) =>
    api.delete(`/api/v1/organizations/${orgId}/past-performance/${ppId}`),
};

export default api;
