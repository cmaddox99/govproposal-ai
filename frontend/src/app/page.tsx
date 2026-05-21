'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import {
  FileText,
  Mail,
  Lock,
  AlertCircle,
  Search,
  Target,
  Sparkles,
  Shield,
  ArrowRight,
  Check,
  TrendingUp,
  Bot,
  Zap,
  Clock,
  Award,
} from 'lucide-react';
import { authApi } from '@/lib/api';
import { MfaChallenge } from '@/components/auth/mfa-challenge';

export default function LandingPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [mfaRequired, setMfaRequired] = useState(false);
  const [mfaToken, setMfaToken] = useState('');
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      router.replace('/dashboard');
    } else {
      setChecking(false);
    }
  }, [router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const response = await authApi.login(email, password);
      const data = response.data;
      if (data.mfa_required) {
        setMfaToken(data.mfa_token);
        setMfaRequired(true);
      } else {
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('refreshToken', data.refresh_token);
        router.push('/dashboard');
      }
    } catch (err: any) {
      const detail = err.response?.data?.detail;
      if (typeof detail === 'string') setError(detail);
      else if (detail?.message) setError(detail.message);
      else setError('Invalid email or password');
    } finally {
      setLoading(false);
    }
  };

  const handleMfaSuccess = (tokens: any) => {
    localStorage.setItem('token', tokens.access_token);
    localStorage.setItem('refreshToken', tokens.refresh_token);
    router.push('/dashboard');
  };

  if (checking) {
    return (
      <div className="min-h-screen bg-[#0a0a0f] flex items-center justify-center">
        <div className="w-10 h-10 border-2 border-emerald-500/30 border-t-emerald-500 rounded-full animate-spin" />
      </div>
    );
  }

  if (mfaRequired) {
    return (
      <div className="min-h-screen bg-[#0a0a0f] flex items-center justify-center p-4">
        <MfaChallenge
          mfaToken={mfaToken}
          onSuccess={handleMfaSuccess}
          onCancel={() => setMfaRequired(false)}
        />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0a0a0f] text-white overflow-x-hidden">
      {/* Animated gradient background */}
      <div className="fixed inset-0 -z-10 pointer-events-none">
        <div className="absolute top-0 left-1/4 w-[600px] h-[600px] bg-emerald-500/10 rounded-full blur-[120px] animate-pulse-slow" />
        <div className="absolute bottom-0 right-1/4 w-[600px] h-[600px] bg-blue-500/10 rounded-full blur-[120px] animate-pulse-slow" style={{ animationDelay: '2s' }} />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-purple-500/5 rounded-full blur-[140px]" />
      </div>

      {/* Subtle grid overlay */}
      <div
        className="fixed inset-0 -z-10 opacity-[0.03] pointer-events-none"
        style={{
          backgroundImage: 'linear-gradient(rgba(255,255,255,0.5) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.5) 1px, transparent 1px)',
          backgroundSize: '60px 60px',
        }}
      />

      {/* Nav */}
      <nav className="relative z-10 max-w-7xl mx-auto px-6 py-5 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-9 h-9 bg-gradient-to-br from-emerald-500 to-blue-500 rounded-lg flex items-center justify-center shadow-lg shadow-emerald-500/20">
            <FileText className="w-5 h-5 text-white" />
          </div>
          <span className="font-bold text-lg tracking-tight">GovProposalAI</span>
        </div>
        <div className="flex items-center gap-2">
          <a
            href="#features"
            className="hidden md:block text-sm text-gray-400 hover:text-white px-3 py-2 transition-colors"
          >
            Features
          </a>
          <a
            href="#how-it-works"
            className="hidden md:block text-sm text-gray-400 hover:text-white px-3 py-2 transition-colors"
          >
            How it works
          </a>
          <a
            href="#login"
            className="text-sm text-gray-300 hover:text-white px-3 py-2 transition-colors"
          >
            Sign in
          </a>
          <Link
            href="/register"
            className="text-sm bg-white text-black hover:bg-gray-200 font-medium px-4 py-2 rounded-lg transition-colors"
          >
            Start free
          </Link>
        </div>
      </nav>

      {/* Hero + Login */}
      <section className="relative z-10 max-w-7xl mx-auto px-6 pt-12 pb-24">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left: Marketing */}
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 bg-emerald-500/10 border border-emerald-500/20 rounded-full text-xs text-emerald-300 mb-6">
              <Sparkles className="w-3.5 h-3.5" />
              AI-native proposal platform
            </div>

            <h1 className="text-5xl md:text-6xl lg:text-7xl font-extrabold tracking-tight leading-[1.05] mb-6">
              Bid Smarter.
              <br />
              <span className="bg-gradient-to-r from-emerald-400 via-cyan-400 to-blue-400 bg-clip-text text-transparent">
                Win More.
              </span>
            </h1>

            <p className="text-lg md:text-xl text-gray-400 leading-relaxed mb-8 max-w-xl">
              The AI co-pilot for government contractors. Discover opportunities on{' '}
              <span className="text-white font-medium">SAM.gov</span> and{' '}
              <span className="text-white font-medium">GSA eBuy</span>, score them against your
              past performance, and generate winning proposals in hours — not weeks.
            </p>

            <div className="flex flex-wrap items-center gap-3 mb-10">
              <Link
                href="/register"
                className="group flex items-center gap-2 bg-gradient-to-r from-emerald-500 to-blue-500 hover:from-emerald-600 hover:to-blue-600 text-white font-medium px-6 py-3.5 rounded-lg shadow-lg shadow-emerald-500/20 transition-all"
              >
                Start free — no credit card
                <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
              </Link>
              <a
                href="#features"
                className="flex items-center gap-2 bg-white/[0.04] border border-white/[0.08] hover:bg-white/[0.08] text-white font-medium px-6 py-3.5 rounded-lg transition-colors"
              >
                See how it works
              </a>
            </div>

            {/* Trust strip */}
            <div className="grid grid-cols-3 gap-6 pt-8 border-t border-white/[0.06] max-w-lg">
              <div>
                <div className="text-2xl font-bold text-white">12×</div>
                <div className="text-xs text-gray-500 mt-1">Faster proposals</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-white">95%+</div>
                <div className="text-xs text-gray-500 mt-1">Target score</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-white">SOC-2</div>
                <div className="text-xs text-gray-500 mt-1">Ready</div>
              </div>
            </div>
          </div>

          {/* Right: Login card */}
          <div id="login" className="lg:justify-self-end w-full max-w-md scroll-mt-24">
            <div className="relative">
              <div className="absolute -inset-0.5 bg-gradient-to-r from-emerald-500 to-blue-500 rounded-2xl opacity-20 blur-md" />
              <div className="relative bg-[#0d0d14] border border-white/[0.08] rounded-2xl p-8 backdrop-blur-sm">
                <div className="mb-6">
                  <h2 className="text-2xl font-bold text-white">Welcome back</h2>
                  <p className="text-gray-400 mt-1 text-sm">Sign in to continue to your dashboard</p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1.5">Email</label>
                    <div className="relative">
                      <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
                      <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="you@company.com"
                        required
                        autoComplete="email"
                        className="w-full pl-10 pr-4 py-3 bg-white/[0.04] border border-white/[0.08] rounded-lg text-white placeholder-gray-600 focus:ring-2 focus:ring-emerald-500/40 focus:border-emerald-500/30 transition-colors text-sm"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1.5">Password</label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
                      <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="••••••••"
                        required
                        autoComplete="current-password"
                        className="w-full pl-10 pr-4 py-3 bg-white/[0.04] border border-white/[0.08] rounded-lg text-white placeholder-gray-600 focus:ring-2 focus:ring-emerald-500/40 focus:border-emerald-500/30 transition-colors text-sm"
                      />
                    </div>
                  </div>

                  {error && (
                    <div className="flex items-start gap-2 text-red-400 text-sm bg-red-500/10 border border-red-500/20 p-3 rounded-lg">
                      <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
                      <span>{error}</span>
                    </div>
                  )}

                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-emerald-500 to-blue-500 hover:from-emerald-600 hover:to-blue-600 text-white py-3 px-4 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed font-medium transition-all shadow-lg shadow-emerald-500/10"
                  >
                    {loading ? (
                      <>
                        <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                        Signing in...
                      </>
                    ) : (
                      <>
                        Sign in
                        <ArrowRight className="w-4 h-4" />
                      </>
                    )}
                  </button>
                </form>

                <div className="mt-6 pt-6 border-t border-white/[0.06] text-center text-sm text-gray-500">
                  New to GovProposalAI?{' '}
                  <Link href="/register" className="text-emerald-400 hover:text-emerald-300 font-medium">
                    Create an account
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Logos / Trust bar */}
      <section className="relative z-10 max-w-7xl mx-auto px-6 pb-16">
        <div className="text-center text-xs uppercase tracking-widest text-gray-500 mb-6">
          Built for contractors targeting
        </div>
        <div className="flex flex-wrap items-center justify-center gap-x-12 gap-y-4 opacity-60">
          {['Department of Defense', 'GSA', 'NASA', 'Department of Veterans Affairs', 'Homeland Security', 'HHS'].map((agency) => (
            <span key={agency} className="text-gray-400 text-sm font-medium tracking-wide">
              {agency}
            </span>
          ))}
        </div>
      </section>

      {/* Features */}
      <section id="features" className="relative z-10 max-w-7xl mx-auto px-6 py-24 scroll-mt-24">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 bg-blue-500/10 border border-blue-500/20 rounded-full text-xs text-blue-300 mb-4">
            <Zap className="w-3.5 h-3.5" />
            Built for SMB government contractors
          </div>
          <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-4">
            Every step. <span className="bg-gradient-to-r from-emerald-400 to-blue-400 bg-clip-text text-transparent">Automated.</span>
          </h2>
          <p className="text-lg text-gray-400">
            From discovery to submission — replace four tools and a dozen spreadsheets with one AI-powered workspace.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-5">
          <FeatureCard
            icon={Search}
            iconBg="from-cyan-500 to-blue-500"
            title="Smart opportunity discovery"
            description="Live sync with SAM.gov and GSA eBuy filtered to your NAICS codes and set-asides. No more midnight scrolling through federal portals."
          />
          <FeatureCard
            icon={Target}
            iconBg="from-emerald-500 to-teal-500"
            title="AI match scoring"
            description="Every pursuit gets a Good / Low / No-Bid tier based on your past performance, NAICS fit, set-aside eligibility, and contract value. Stop chasing bad fits."
          />
          <FeatureCard
            icon={Bot}
            iconBg="from-purple-500 to-pink-500"
            title="AI proposal generator"
            description="Generate executive summary, technical approach, management approach, past performance, and pricing — all targeting 95%+ scores on every factor."
          />
          <FeatureCard
            icon={Shield}
            iconBg="from-orange-500 to-red-500"
            title="Compliance built-in"
            description="Section L/M tracking, certifications dashboard, audit trail for every AI interaction, MFA, and SOC-2-ready security posture."
          />
        </div>
      </section>

      {/* How it works */}
      <section id="how-it-works" className="relative z-10 max-w-7xl mx-auto px-6 py-24 scroll-mt-24">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-4">
            From SAM.gov to submission in <span className="bg-gradient-to-r from-emerald-400 to-blue-400 bg-clip-text text-transparent">three steps</span>
          </h2>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          <StepCard
            num="01"
            icon={Search}
            title="Discover"
            description="Sync opportunities from SAM.gov and GSA eBuy. Filter by NAICS, set-aside, value, and deadline."
          />
          <StepCard
            num="02"
            icon={Target}
            title="Qualify"
            description="Promote winners into your Pipeline. Get an instant Good/Low/No-Bid score with a breakdown of why."
          />
          <StepCard
            num="03"
            icon={Award}
            title="Win"
            description="Generate a full proposal with AI, score it against Section L/M, iterate to 95%+, export to DOCX. Submit."
          />
        </div>
      </section>

      {/* Pipeline showcase */}
      <section className="relative z-10 max-w-7xl mx-auto px-6 py-24">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 bg-emerald-500/10 border border-emerald-500/20 rounded-full text-xs text-emerald-300 mb-4">
              <TrendingUp className="w-3.5 h-3.5" />
              New: Pipeline scoring
            </div>
            <h2 className="text-3xl md:text-4xl font-bold tracking-tight mb-4">
              Know which RFPs to actually go after.
            </h2>
            <p className="text-gray-400 text-lg mb-6">
              Every opportunity in your pipeline gets an instant fit score across four dimensions:
              NAICS, past performance, set-aside, and contract value. Color-coded so you can triage at a glance.
            </p>
            <ul className="space-y-3">
              {[
                { label: 'Good', desc: 'Strong fit — go pursue', dot: 'bg-emerald-400' },
                { label: 'Low', desc: 'Stretch goal — consider', dot: 'bg-yellow-400' },
                { label: 'No Bid', desc: 'Walk away — save the time', dot: 'bg-red-400' },
              ].map((row) => (
                <li key={row.label} className="flex items-center gap-3">
                  <span className={`w-2 h-2 rounded-full ${row.dot}`} />
                  <span className="text-white font-medium">{row.label}</span>
                  <span className="text-gray-500">— {row.desc}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="relative">
            <div className="absolute -inset-1 bg-gradient-to-r from-emerald-500/20 to-blue-500/20 rounded-2xl blur-xl" />
            <div className="relative bg-[#0d0d14] border border-white/[0.08] rounded-2xl p-6 space-y-3">
              <MockPipelineRow tier="green" score={87} title="IDEAS Tier 2/Tier 3 Support" agency="DOD" value="$8.5M" />
              <MockPipelineRow tier="yellow" score={62} title="Enterprise Statistician Services" agency="USAC" value="$2.1M" />
              <MockPipelineRow tier="red" score={34} title="Aerospace Component Manufacturing" agency="NASA" value="$15M" />
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="relative z-10 max-w-5xl mx-auto px-6 py-24">
        <div className="relative overflow-hidden bg-gradient-to-br from-emerald-500/10 via-blue-500/10 to-purple-500/10 border border-white/[0.08] rounded-3xl p-12 md:p-16 text-center">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(16,185,129,0.1),transparent_70%)]" />
          <div className="relative">
            <Clock className="w-12 h-12 text-emerald-400 mx-auto mb-6" />
            <h2 className="text-3xl md:text-5xl font-bold tracking-tight mb-4">
              Stop spending weeks on proposals you might not win.
            </h2>
            <p className="text-lg text-gray-400 mb-8 max-w-2xl mx-auto">
              Free to start. Sync your first opportunities in under five minutes.
            </p>
            <div className="flex flex-wrap items-center justify-center gap-3">
              <Link
                href="/register"
                className="group flex items-center gap-2 bg-gradient-to-r from-emerald-500 to-blue-500 hover:from-emerald-600 hover:to-blue-600 text-white font-medium px-7 py-4 rounded-lg shadow-lg shadow-emerald-500/20 transition-all"
              >
                Get started free
                <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
              </Link>
              <a
                href="#login"
                className="text-gray-400 hover:text-white px-7 py-4 transition-colors font-medium"
              >
                Or sign in →
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative z-10 border-t border-white/[0.06]">
        <div className="max-w-7xl mx-auto px-6 py-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 bg-gradient-to-br from-emerald-500 to-blue-500 rounded-md flex items-center justify-center">
              <FileText className="w-4 h-4 text-white" />
            </div>
            <span className="text-sm font-medium">GovProposalAI</span>
            <span className="text-gray-600 text-xs ml-2">© {new Date().getFullYear()}</span>
          </div>
          <div className="flex items-center gap-6 text-sm text-gray-500">
            <a href="#features" className="hover:text-white transition-colors">Features</a>
            <a href="#how-it-works" className="hover:text-white transition-colors">How it works</a>
            <a href="#login" className="hover:text-white transition-colors">Sign in</a>
          </div>
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({
  icon: Icon,
  iconBg,
  title,
  description,
}: {
  icon: any;
  iconBg: string;
  title: string;
  description: string;
}) {
  return (
    <div className="group relative bg-white/[0.02] border border-white/[0.06] hover:border-white/[0.12] rounded-2xl p-6 transition-all hover:bg-white/[0.04]">
      <div className={`inline-flex items-center justify-center w-11 h-11 bg-gradient-to-br ${iconBg} rounded-lg mb-4 shadow-lg`}>
        <Icon className="w-5 h-5 text-white" />
      </div>
      <h3 className="text-lg font-semibold text-white mb-2">{title}</h3>
      <p className="text-gray-400 text-sm leading-relaxed">{description}</p>
    </div>
  );
}

function StepCard({
  num,
  icon: Icon,
  title,
  description,
}: {
  num: string;
  icon: any;
  title: string;
  description: string;
}) {
  return (
    <div className="relative bg-white/[0.02] border border-white/[0.06] rounded-2xl p-8">
      <div className="text-sm font-mono text-emerald-400 mb-4">{num}</div>
      <Icon className="w-7 h-7 text-white mb-4" />
      <h3 className="text-xl font-semibold text-white mb-2">{title}</h3>
      <p className="text-gray-400 leading-relaxed">{description}</p>
    </div>
  );
}

function MockPipelineRow({
  tier,
  score,
  title,
  agency,
  value,
}: {
  tier: 'green' | 'yellow' | 'red';
  score: number;
  title: string;
  agency: string;
  value: string;
}) {
  const tierLabels = { green: 'Good', yellow: 'Low', red: 'No Bid' };
  const tierColors = {
    green: 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30',
    yellow: 'bg-yellow-500/15 text-yellow-300 border-yellow-500/30',
    red: 'bg-red-500/15 text-red-400 border-red-500/30',
  };
  const dotColors = { green: 'bg-emerald-400', yellow: 'bg-yellow-400', red: 'bg-red-400' };

  return (
    <div className="bg-white/[0.02] border border-white/[0.06] rounded-lg p-4 flex items-center gap-4">
      <div className={`flex items-center gap-1.5 px-2 py-0.5 ${tierColors[tier]} border text-xs font-medium rounded`}>
        <span className={`w-1.5 h-1.5 rounded-full ${dotColors[tier]}`} />
        {score}% {tierLabels[tier]}
      </div>
      <div className="flex-1 min-w-0">
        <div className="text-white text-sm font-medium truncate">{title}</div>
        <div className="text-gray-500 text-xs">{agency}</div>
      </div>
      <div className="text-emerald-400 text-sm font-medium">{value}</div>
    </div>
  );
}
