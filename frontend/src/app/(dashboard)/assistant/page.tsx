'use client';

/**
 * AI Assistant Page — Constitution-compliant UI
 *
 * Art. IV 4.4: Dark-first (#0a0a0f), emerald→blue gradients,
 *   glass morphism, pulsing AI indicators, confidence scores
 * Art. VII 7.4: Displays context confidence indicators
 */

import { useState, useEffect, useRef, useCallback } from 'react';
import { Send, Bot, User, Sparkles, ChevronDown, Loader2, FileText, Search, Info, Check, Zap } from 'lucide-react';
import { assistantApi, proposalsApi, opportunitiesApi } from '@/lib/api';
import type { Proposal, Opportunity } from '@/types';

interface ContextUsed {
  org: boolean;
  opportunities_count: number;
  proposals_count: number;
  focused_proposal: boolean;
  focused_opportunity: boolean;
}

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  contextUsed?: ContextUsed;
}

const WELCOME_MESSAGE: ChatMessage = {
  id: 'welcome',
  role: 'assistant',
  content:
    "Hello! I'm your AI proposal advisor. I have access to your organization's profile, opportunities, proposals, and scores. I can help you:\n\n" +
    "- **Analyze opportunities** and recommend go/no-go decisions\n" +
    "- **Review proposals** and identify improvements to boost scores\n" +
    "- **Rewrite sections** targeting 95%+ on all scoring criteria\n" +
    "- **Compare capabilities** against opportunity requirements\n\n" +
    "Select a proposal or opportunity from the dropdowns above to focus our conversation, or just ask me anything!",
};

const GENERAL_SUGGESTIONS = [
  'Which opportunities match our capabilities?',
  'What proposals need improvement?',
  'Summarize our organization profile',
  'What are our strongest NAICS codes?',
];

const PROPOSAL_SUGGESTIONS = [
  'What should I improve first?',
  'Rewrite the executive summary for 95%+',
  "What's my score breakdown?",
  'Fix all sections for 95%+ score',
];

const OPPORTUNITY_SUGGESTIONS = [
  'Should we pursue this opportunity?',
  'What past performance is relevant?',
  'Draft a proposal outline for this',
  'What are the key requirements?',
];

/* ---------- Markdown renderer ---------- */

function renderMarkdown(text: string, proposalId?: string | null) {
  const lines = text.split('\n');
  const elements: JSX.Element[] = [];
  let inCodeBlock = false;
  let codeContent: string[] = [];
  let codeLabel = '';

  lines.forEach((line, i) => {
    if (line.startsWith('```')) {
      if (inCodeBlock) {
        // Check if this is a section rewrite block
        if (isSectionBlock(codeLabel)) {
          elements.push(
            <ApplySectionBlock
              key={`section-${i}`}
              label={codeLabel}
              content={codeContent.join('\n')}
              proposalId={proposalId || null}
            />
          );
        } else {
          elements.push(
            <div key={`code-${i}`} className="my-3">
              {codeLabel && (
                <div className="text-xs text-white/40 bg-white/[0.03] px-3 py-1 rounded-t border border-b-0 border-white/[0.08] font-mono">
                  {codeLabel}
                </div>
              )}
              <pre className={`bg-white/[0.03] text-gray-200 p-3 ${codeLabel ? 'rounded-b' : 'rounded'} border border-white/[0.08] text-sm overflow-x-auto`}>
                <code>{codeContent.join('\n')}</code>
              </pre>
            </div>
          );
        }
        codeContent = [];
        codeLabel = '';
        inCodeBlock = false;
      } else {
        inCodeBlock = true;
        codeLabel = line.slice(3).trim();
      }
      return;
    }

    if (inCodeBlock) {
      codeContent.push(line);
      return;
    }

    if (line.startsWith('### ')) {
      elements.push(<h3 key={i} className="text-base font-semibold text-white mt-4 mb-1">{line.slice(4)}</h3>);
      return;
    }
    if (line.startsWith('## ')) {
      elements.push(<h2 key={i} className="text-lg font-semibold text-white mt-4 mb-1">{line.slice(3)}</h2>);
      return;
    }
    if (line.startsWith('# ')) {
      elements.push(<h1 key={i} className="text-xl font-bold text-white mt-4 mb-2">{line.slice(2)}</h1>);
      return;
    }

    if (line.startsWith('|')) {
      if (line.match(/^\|[\s-|]+$/)) return;
      const cells = line.split('|').filter(c => c.trim() !== '');
      const isHeader = i + 1 < lines.length && lines[i + 1]?.match(/^\|[\s-|]+$/);
      elements.push(
        <div key={i} className={`grid gap-2 text-sm py-1 border-b border-white/[0.06] ${isHeader ? 'font-semibold text-gray-200' : 'text-white/60'}`}
          style={{ gridTemplateColumns: `repeat(${cells.length}, minmax(0, 1fr))` }}>
          {cells.map((cell, ci) => (
            <span key={ci} className="truncate px-1">{cell.trim()}</span>
          ))}
        </div>
      );
      return;
    }

    if (line.match(/^[-*] /)) {
      const content = line.slice(2);
      elements.push(
        <div key={i} className="flex gap-2 text-sm text-white/60 ml-2 my-0.5">
          <span className="text-white/30 mt-0.5">&#8226;</span>
          <span dangerouslySetInnerHTML={{ __html: inlineFormat(content) }} />
        </div>
      );
      return;
    }

    if (line.match(/^\d+\. /)) {
      const num = line.match(/^(\d+)\. /)![1];
      const content = line.replace(/^\d+\. /, '');
      elements.push(
        <div key={i} className="flex gap-2 text-sm text-white/60 ml-2 my-0.5">
          <span className="text-white/40 font-mono text-xs mt-0.5 min-w-[1.2rem]">{num}.</span>
          <span dangerouslySetInnerHTML={{ __html: inlineFormat(content) }} />
        </div>
      );
      return;
    }

    if (line.trim() === '') {
      elements.push(<div key={i} className="h-2" />);
      return;
    }

    elements.push(
      <p key={i} className="text-sm text-white/60 my-1" dangerouslySetInnerHTML={{ __html: inlineFormat(line) }} />
    );
  });

  return <div>{elements}</div>;
}

function inlineFormat(text: string): string {
  return text
    .replace(/\*\*(.+?)\*\*/g, '<strong class="text-white font-semibold">$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/`(.+?)`/g, '<code class="bg-white/[0.06] text-emerald-400 px-1 py-0.5 rounded text-xs">$1</code>');
}

/* ---------- Section code block names ---------- */

const SECTION_LABELS: Record<string, string> = {
  'section:executive_summary': 'Executive Summary',
  'section:technical_approach': 'Technical Approach',
  'section:management_approach': 'Management Approach',
  'section:past_performance': 'Past Performance',
  'section:pricing_summary': 'Pricing Summary',
};

function isSectionBlock(label: string): boolean {
  return label in SECTION_LABELS;
}

function getSectionName(label: string): string {
  return label.replace('section:', '');
}

/* ---------- Apply section block component ---------- */

function ApplySectionBlock({
  label,
  content,
  proposalId,
}: {
  label: string;
  content: string;
  proposalId: string | null;
}) {
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [errorMsg, setErrorMsg] = useState('');

  const handleApply = async () => {
    if (!proposalId) {
      setErrorMsg('Select a proposal first');
      setStatus('error');
      return;
    }
    setStatus('loading');
    setErrorMsg('');
    try {
      await assistantApi.applySection(proposalId, getSectionName(label), content);
      setStatus('success');
    } catch (err: any) {
      setErrorMsg(err.response?.data?.detail || 'Failed to apply section');
      setStatus('error');
    }
  };

  return (
    <div className="my-3 border border-emerald-500/20 rounded-lg overflow-hidden">
      <div className="flex items-center justify-between bg-emerald-500/10 px-3 py-1.5">
        <span className="text-xs text-emerald-400 font-semibold">
          {SECTION_LABELS[label] || label}
        </span>
        {status === 'success' ? (
          <span className="flex items-center gap-1 text-xs text-emerald-400">
            <Check className="w-3.5 h-3.5" /> Applied!
          </span>
        ) : (
          <button
            onClick={handleApply}
            disabled={status === 'loading'}
            className="flex items-center gap-1 text-xs px-2 py-0.5 bg-emerald-500 text-white rounded hover:bg-emerald-600 disabled:opacity-50 transition-colors"
          >
            {status === 'loading' ? (
              <Loader2 className="w-3 h-3 animate-spin" />
            ) : (
              <Check className="w-3 h-3" />
            )}
            Apply to Proposal
          </button>
        )}
      </div>
      {status === 'error' && errorMsg && (
        <div className="px-3 py-1 text-xs text-red-400 bg-red-900/20">{errorMsg}</div>
      )}
      <pre className="bg-white/[0.03] text-gray-200 p-3 text-sm overflow-x-auto max-h-96 overflow-y-auto">
        <code>{content}</code>
      </pre>
    </div>
  );
}

/* ---------- Context confidence badge (Art. VII 7.4) ---------- */

function ContextBadge({ ctx }: { ctx: ContextUsed }) {
  const items: string[] = [];
  if (ctx.org) items.push('Org');
  if (ctx.opportunities_count > 0) items.push(`${ctx.opportunities_count} opps`);
  if (ctx.proposals_count > 0) items.push(`${ctx.proposals_count} props`);
  if (ctx.focused_proposal) items.push('Focused proposal');
  if (ctx.focused_opportunity) items.push('Focused opp');

  if (items.length === 0) return null;

  return (
    <div className="flex items-center gap-1 mt-2 text-[11px] text-white/30">
      <Info className="w-3 h-3" />
      <span>Context: {items.join(' · ')}</span>
    </div>
  );
}

/* ---------- Main component ---------- */

export default function AssistantPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([WELCOME_MESSAGE]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [proposals, setProposals] = useState<Proposal[]>([]);
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [selectedProposal, setSelectedProposal] = useState<string | null>(null);
  const [selectedOpportunity, setSelectedOpportunity] = useState<string | null>(null);
  const [orgId, setOrgId] = useState<string>('');
  const [isImproving, setIsImproving] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const storedOrg = localStorage.getItem('selectedOrganization');
    if (storedOrg) {
      try {
        const org = JSON.parse(storedOrg);
        setOrgId(org.id);
      } catch { /* ignore */ }
    }
  }, []);

  useEffect(() => {
    if (!orgId) return;
    proposalsApi.list({ org_id: orgId, limit: 50 }).then((res) => {
      setProposals(res.data.proposals || []);
    }).catch(() => {});
    opportunitiesApi.list({ org_id: orgId, limit: 50 }).then((res) => {
      const opps = res.data.opportunities || res.data;
      setOpportunities(Array.isArray(opps) ? opps : []);
    }).catch(() => {});
  }, [orgId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleSend = useCallback(async (text?: string) => {
    const messageText = text || input.trim();
    if (!messageText || isLoading) return;

    setError(null);
    setInput('');

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: messageText,
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const history = [...messages.filter(m => m.id !== 'welcome'), userMessage].map(m => ({
        role: m.role,
        content: m.content,
      }));

      const response = await assistantApi.chat(history, {
        org_id: orgId,
        proposal_id: selectedProposal,
        opportunity_id: selectedOpportunity,
      });

      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.data.message,
        contextUsed: response.data.context_used,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err: any) {
      const detail = err.response?.data?.detail || err.message || 'Failed to get response';
      setError(detail);
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  }, [input, isLoading, messages, orgId, selectedProposal, selectedOpportunity]);

  const handleImproveAll = useCallback(async () => {
    if (!selectedProposal || isImproving) return;
    setIsImproving(true);
    setError(null);

    // Add a system-like message
    const infoMsg: ChatMessage = {
      id: Date.now().toString(),
      role: 'assistant',
      content: '**Improving all sections...** This may take a minute. I\'m regenerating each section with score feedback to target 95%+ on all factors.',
    };
    setMessages((prev) => [...prev, infoMsg]);

    try {
      const response = await proposalsApi.improve(selectedProposal);
      const data = response.data;
      const resultMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content:
          `**Improvement complete!**\n\n` +
          `- **Sections improved:** ${data.improved_sections?.join(', ') || 'none'}\n` +
          `- **Previous score:** ${data.previous_score ?? 'N/A'}/100\n` +
          `- **New score:** ${data.new_score ?? 'N/A'}/100\n\n` +
          `The proposal has been updated with improved content. You can ask me to review specific sections or make further adjustments.`,
      };
      setMessages((prev) => [...prev, resultMsg]);
    } catch (err: any) {
      const detail = err.response?.data?.detail || err.message || 'Failed to improve proposal';
      setError(detail);
    } finally {
      setIsImproving(false);
    }
  }, [selectedProposal, isImproving]);

  const suggestions = selectedProposal
    ? PROPOSAL_SUGGESTIONS
    : selectedOpportunity
      ? OPPORTUNITY_SUGGESTIONS
      : GENERAL_SUGGESTIONS;

  const selectedProposalObj = proposals.find(p => p.id === selectedProposal);
  const selectedOpportunityObj = opportunities.find(o => o.id === selectedOpportunity);

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)]">
      {/* Header */}
      <div className="mb-4">
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <span className="bg-gradient-to-r from-emerald-500 to-blue-500 bg-clip-text text-transparent">
            AI Assistant
          </span>
        </h1>
        <p className="text-white/60 mt-1">Context-aware advisor for proposals, opportunities, and scoring</p>
      </div>

      {/* Context Selectors — Art. IV 4.4: glass morphism cards */}
      <div className="flex gap-3 mb-4 flex-wrap">
        <div className="relative">
          <select
            value={selectedProposal || ''}
            onChange={(e) => setSelectedProposal(e.target.value || null)}
            className="appearance-none bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] text-gray-200 text-sm rounded-lg pl-9 pr-8 py-2 focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500/30 cursor-pointer min-w-[240px] transition-colors"
          >
            <option value="">No proposal focus</option>
            {proposals.map((p) => (
              <option key={p.id} value={p.id}>
                {p.title.length > 40 ? p.title.slice(0, 40) + '...' : p.title} ({p.status})
              </option>
            ))}
          </select>
          <FileText className="absolute left-3 top-2.5 w-4 h-4 text-white/40 pointer-events-none" />
          <ChevronDown className="absolute right-2 top-2.5 w-4 h-4 text-white/40 pointer-events-none" />
        </div>

        <div className="relative">
          <select
            value={selectedOpportunity || ''}
            onChange={(e) => setSelectedOpportunity(e.target.value || null)}
            className="appearance-none bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] text-gray-200 text-sm rounded-lg pl-9 pr-8 py-2 focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500/30 cursor-pointer min-w-[240px] transition-colors"
          >
            <option value="">No opportunity focus</option>
            {opportunities.map((o) => (
              <option key={o.id} value={o.id}>
                {o.title.length > 40 ? o.title.slice(0, 40) + '...' : o.title}
              </option>
            ))}
          </select>
          <Search className="absolute left-3 top-2.5 w-4 h-4 text-white/40 pointer-events-none" />
          <ChevronDown className="absolute right-2 top-2.5 w-4 h-4 text-white/40 pointer-events-none" />
        </div>

        {(selectedProposalObj || selectedOpportunityObj) && (
          <div className="flex items-center gap-2 text-xs text-white/40">
            {selectedProposalObj && (
              <span className="bg-emerald-500/10 text-emerald-400 px-2 py-1 rounded border border-emerald-500/20">
                Proposal: {selectedProposalObj.title.slice(0, 30)}
              </span>
            )}
            {selectedOpportunityObj && (
              <span className="bg-blue-500/10 text-blue-400 px-2 py-1 rounded border border-blue-500/20">
                Opportunity: {selectedOpportunityObj.title.slice(0, 30)}
              </span>
            )}
          </div>
        )}

        {selectedProposal && (
          <button
            onClick={handleImproveAll}
            disabled={isImproving || isLoading}
            className="flex items-center gap-1.5 px-3 py-2 bg-gradient-to-r from-emerald-600 to-blue-600 text-white text-sm rounded-lg hover:from-emerald-500 hover:to-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            {isImproving ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Zap className="w-4 h-4" />
            )}
            {isImproving ? 'Improving...' : 'Improve All Sections'}
          </button>
        )}
      </div>

      {/* Chat Container — Art. IV 4.4: glass morphism + gradient border for AI */}
      <div className="flex-1 bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl flex flex-col overflow-hidden relative">
        {/* Gradient glow effect on border */}
        <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-emerald-500/5 to-blue-500/5 pointer-events-none" />

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4 relative z-10">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex gap-3 ${message.role === 'user' ? 'justify-end' : ''}`}
            >
              {message.role === 'assistant' && (
                <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-br from-emerald-500 to-blue-500 rounded-lg flex items-center justify-center mt-1">
                  <Bot className="w-5 h-5 text-white" />
                </div>
              )}
              <div className="max-w-[75%]">
                <div
                  className={`p-4 rounded-xl ${
                    message.role === 'user'
                      ? 'bg-gradient-to-r from-emerald-600 to-blue-600 text-white'
                      : 'bg-white/[0.04] border border-white/[0.06] text-gray-100'
                  }`}
                >
                  {message.role === 'assistant' ? (
                    renderMarkdown(message.content, selectedProposal)
                  ) : (
                    <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                  )}
                </div>
                {/* Art. VII 7.4: Confidence/context indicator */}
                {message.role === 'assistant' && message.contextUsed && (
                  <ContextBadge ctx={message.contextUsed} />
                )}
              </div>
              {message.role === 'user' && (
                <div className="flex-shrink-0 w-8 h-8 bg-white/[0.06] rounded-lg flex items-center justify-center mt-1">
                  <User className="w-5 h-5 text-white/60" />
                </div>
              )}
            </div>
          ))}

          {/* Typing indicator — Art. IV 4.4: pulsing dots for active agent */}
          {isLoading && (
            <div className="flex gap-3">
              <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-br from-emerald-500 to-blue-500 rounded-lg flex items-center justify-center mt-1 animate-pulse">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <div className="bg-white/[0.04] border border-white/[0.06] p-4 rounded-xl">
                <div className="flex gap-1.5">
                  <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" style={{ animationDelay: '0ms' }} />
                  <div className="w-2 h-2 bg-emerald-400/70 rounded-full animate-pulse" style={{ animationDelay: '200ms' }} />
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse" style={{ animationDelay: '400ms' }} />
                </div>
              </div>
            </div>
          )}

          {error && (
            <div className="mx-auto max-w-md bg-red-900/20 border border-red-500/20 text-red-400 text-sm p-3 rounded-lg">
              {error}
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Suggestions — Art. IV 4.4: gradient accent on AI interaction elements */}
        <div className="px-6 py-3 border-t border-white/[0.06] relative z-10">
          <div className="flex gap-2 overflow-x-auto pb-1">
            {suggestions.map((suggestion) => (
              <button
                key={suggestion}
                onClick={() => handleSend(suggestion)}
                disabled={isLoading}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-white/[0.04] border border-white/[0.06] text-white/60 text-sm rounded-full whitespace-nowrap hover:bg-white/[0.08] hover:text-white hover:border-emerald-500/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                <Sparkles className="w-3 h-3 text-emerald-400" />
                {suggestion}
              </button>
            ))}
          </div>
        </div>

        {/* Input Area */}
        <div className="p-4 border-t border-white/[0.06] relative z-10">
          <div className="flex gap-3">
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
              placeholder={
                selectedProposal
                  ? 'Ask about this proposal...'
                  : selectedOpportunity
                    ? 'Ask about this opportunity...'
                    : 'Ask me anything about government proposals...'
              }
              disabled={isLoading}
              className="flex-1 px-4 py-3 bg-white/[0.03] border border-white/[0.08] rounded-lg text-white placeholder-white/30 focus:ring-2 focus:ring-emerald-500/40 focus:border-emerald-500/30 disabled:opacity-50 transition-colors"
            />
            <button
              onClick={() => handleSend()}
              disabled={isLoading || !input.trim()}
              className="px-4 py-3 bg-gradient-to-r from-emerald-500 to-blue-500 text-white rounded-lg hover:from-emerald-600 hover:to-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Send className="w-5 h-5" />
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
