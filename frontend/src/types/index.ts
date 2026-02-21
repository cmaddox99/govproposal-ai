// User types
export interface User {
  id: string;
  email: string;
  is_active: boolean;
  is_verified: boolean;
  mfa_enabled: boolean;
  mfa_required: boolean;
  platform_role: string;
  created_at: string;
}

export interface OrgUser {
  id: string;
  user_id: string;
  email: string;
  role: string;
  is_active: boolean;
  mfa_enabled: boolean;
  invited_at: string;
  joined_at: string | null;
}

// Organization types
export interface Organization {
  id: string;
  name: string;
  slug: string;
  is_active: boolean;
  created_at: string;
}

export interface OrganizationMember {
  id: string;
  user_id: string;
  email: string;
  role: string;
  invited_at: string;
  joined_at: string | null;
}

// Auth types
export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface MfaSetupResponse {
  secret: string;
  provisioning_uri: string;
  qr_code_base64?: string;
}

export interface MfaCompleteResponse {
  recovery_codes: string[];
  message: string;
}

// Audit types
export interface AuditLog {
  id: string;
  event_type: string;
  event_time: string;
  actor_id: string | null;
  actor_email: string | null;
  organization_id: string | null;
  resource_type: string | null;
  resource_id: string | null;
  action: string;
  outcome: string;
  ip_address: string | null;
  details: Record<string, unknown> | null;
}

export interface AuditLogList {
  items: AuditLog[];
  total: number;
  limit: number;
  offset: number;
}

// Platform types
export interface Tenant {
  id: string;
  name: string;
  slug: string;
  is_active: boolean;
  member_count: number;
  created_at: string;
}

export interface FeatureToggle {
  feature: string;
  enabled: boolean;
  description: string | null;
}

// Scoring types
export interface ScoreFactor {
  id: string;
  factor_type: string;
  factor_weight: number;
  raw_score: number;
  weighted_score: number;
  evidence_summary: string | null;
  improvement_suggestions: Array<{
    action: string;
    details: string;
    priority: string;
  }> | null;
}

export interface ProposalScore {
  id: string;
  proposal_id: string;
  score_date: string;
  overall_score: number;
  confidence_level: string;
  ai_model_used: string | null;
  created_by: string;
  created_at: string;
  factors: ScoreFactor[];
}

export interface ScoreImprovement {
  priority: number;
  factor: string;
  current_score: number;
  potential_gain: number;
  action: string;
  details: string;
}

export interface ImprovementList {
  proposal_id: string;
  current_score: number;
  improvements: ScoreImprovement[];
}

export interface ScoreHistory {
  proposal_id: string;
  scores: Array<{
    id: string;
    proposal_id: string;
    score_date: string;
    overall_score: number;
    confidence_level: string;
  }>;
  trend: string;
}

export interface Benchmark {
  id: string;
  proposal_id: string;
  benchmark_date: string;
  completeness_score: number;
  technical_depth_score: number;
  compliance_score: number;
  org_percentile: number | null;
  org_avg_at_stage: number | null;
}

export interface BlockerItem {
  category: string;
  description: string;
  section: string | null;
}

export interface WarningItem {
  category: string;
  description: string;
  recommendation: string;
}

export interface Readiness {
  id: string;
  proposal_id: string;
  team_type: string;
  readiness_score: number;
  readiness_level: string;
  blockers: BlockerItem[];
  warnings: WarningItem[];
  checked_at: string;
  checked_by: string;
}

export interface GoNoGoSummary {
  proposal_id: string;
  overall_score: number;
  readiness_level: string;
  recommendation: string;
  key_strengths: string[];
  key_risks: string[];
  next_steps: string[];
}

// Color team types
export type ColorTeamType = 'pink_team' | 'red_team' | 'gold_team' | 'submission';

// Proposal types
export type ProposalStatus =
  | 'draft'
  | 'in_progress'
  | 'review'
  | 'submitted'
  | 'awarded'
  | 'not_awarded'
  | 'cancelled';

export interface Proposal {
  id: string;
  organization_id: string;
  opportunity_id: string | null;
  title: string;
  description: string | null;
  status: ProposalStatus;
  solicitation_number: string | null;
  agency: string | null;
  naics_code: string | null;
  due_date: string | null;
  submitted_at: string | null;
  estimated_value: number | null;
  proposed_value: number | null;
  awarded_value: number | null;
  executive_summary: string | null;
  technical_approach: string | null;
  management_approach: string | null;
  past_performance: string | null;
  pricing_summary: string | null;
  sections: Record<string, any> | null;
  ai_generated_content: Record<string, any> | null;
  created_by: string | null;
  updated_by: string | null;
  created_at: string;
  updated_at: string;
}

export interface ProposalListResponse {
  proposals: Proposal[];
  total: number;
  limit: number;
  offset: number;
}
