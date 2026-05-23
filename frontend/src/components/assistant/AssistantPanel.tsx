'use client';

import { useState, useCallback, useRef, useEffect } from 'react';
import {
  Bot,
  Send,
  Loader2,
  Sparkles,
  Upload,
  Check,
  X,
  ChevronRight,
  ChevronLeft,
  MessageSquare,
  Wand2,
  AlertCircle,
} from 'lucide-react';
import { assistantApi } from '@/lib/api';
import { useOrgId } from '@/lib/useOrgId';

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
}

interface FieldUpdate {
  field: string;
  value: string;
  note?: string | null;
}

interface PastPerformanceRecord {
  contract_name: string;
  agency?: string | null;
  contract_value?: number | null;
  description?: string | null;
  contact_name?: string | null;
  contact_email?: string | null;
}

interface ExtractResult {
  field_updates: FieldUpdate[];
  new_past_performance: PastPerformanceRecord[];
  summary: string;
}

interface AssistantPanelProps {
  proposalId: string;
  collapsed: boolean;
  onToggle: () => void;
  onFieldsApplied: () => void;
}

const FIELD_LABELS: Record<string, string> = {
  title: 'Title',
  description: 'Description',
  agency: 'Agency',
  solicitation_number: 'Solicitation Number',
  naics_code: 'NAICS Code',
  estimated_value: 'Estimated Value',
  proposed_value: 'Proposed Value',
  due_date: 'Due Date',
  executive_summary: 'Executive Summary',
  technical_approach: 'Technical Approach',
  management_approach: 'Management Approach',
  past_performance: 'Past Performance',
  pricing_summary: 'Pricing Summary',
};

export function AssistantPanel({ proposalId, collapsed, onToggle, onFieldsApplied }: AssistantPanelProps) {
  const [tab, setTab] = useState<'chat' | 'extract'>('chat');

  if (collapsed) {
    return (
      <button
        onClick={onToggle}
        className="fixed right-0 top-1/2 -translate-y-1/2 z-10 bg-gradient-to-r from-emerald-500 to-blue-500 text-white p-3 rounded-l-lg shadow-lg hover:from-emerald-600 hover:to-blue-600"
        title="Open AI Assistant"
      >
        <Bot className="w-5 h-5" />
      </button>
    );
  }

  return (
    <aside className="w-[420px] flex-shrink-0 bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl flex flex-col h-[calc(100vh-10rem)] sticky top-4">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-white/[0.06]">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-gradient-to-br from-emerald-500 to-blue-500 rounded-lg flex items-center justify-center">
            <Bot className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="text-white text-sm font-semibold">AI Assistant</h3>
            <p className="text-xs text-gray-500">Scoped to this proposal</p>
          </div>
        </div>
        <button
          onClick={onToggle}
          className="p-1.5 text-gray-400 hover:text-white hover:bg-white/[0.05] rounded transition-colors"
          title="Collapse"
        >
          <ChevronRight className="w-4 h-4" />
        </button>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-white/[0.06]">
        <button
          onClick={() => setTab('chat')}
          className={`flex-1 flex items-center justify-center gap-1.5 px-3 py-2.5 text-xs font-medium border-b-2 ${
            tab === 'chat'
              ? 'border-emerald-500 text-emerald-300'
              : 'border-transparent text-gray-400 hover:text-white'
          }`}
        >
          <MessageSquare className="w-3.5 h-3.5" />
          Chat
        </button>
        <button
          onClick={() => setTab('extract')}
          className={`flex-1 flex items-center justify-center gap-1.5 px-3 py-2.5 text-xs font-medium border-b-2 ${
            tab === 'extract'
              ? 'border-emerald-500 text-emerald-300'
              : 'border-transparent text-gray-400 hover:text-white'
          }`}
        >
          <Wand2 className="w-3.5 h-3.5" />
          Add Content
        </button>
      </div>

      {tab === 'chat' ? (
        <ChatTab proposalId={proposalId} />
      ) : (
        <ExtractTab proposalId={proposalId} onFieldsApplied={onFieldsApplied} />
      )}
    </aside>
  );
}

/* ---------- Chat tab ---------- */

const PROPOSAL_SUGGESTIONS = [
  'What should I improve first?',
  "What's my score breakdown?",
  'Rewrite the executive summary for 95%+',
];

function ChatTab({ proposalId }: { proposalId: string }) {
  const orgId = useOrgId() || '';
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      role: 'assistant',
      content:
        "Ask anything about this proposal. I have access to its content, scoring, your org profile, and past performance. Try one of the suggestions below, or paste new content over in the **Add Content** tab.",
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const send = useCallback(async (text?: string) => {
    const message = text || input.trim();
    if (!message || loading) return;
    if (!orgId) {
      setError('No organization selected.');
      return;
    }
    setError(null);
    setInput('');
    const userMsg: ChatMessage = { id: Date.now().toString(), role: 'user', content: message };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);
    try {
      const history = [...messages.filter((m) => m.id !== 'welcome'), userMsg].map((m) => ({
        role: m.role,
        content: m.content,
      }));
      const response = await assistantApi.chat(history, {
        org_id: orgId,
        proposal_id: proposalId,
      });
      setMessages((prev) => [
        ...prev,
        { id: (Date.now() + 1).toString(), role: 'assistant', content: response.data.message },
      ]);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to get response');
    } finally {
      setLoading(false);
    }
  }, [input, loading, messages, orgId, proposalId]);

  return (
    <div className="flex flex-col flex-1 overflow-hidden">
      <div className="flex-1 overflow-y-auto p-3 space-y-3">
        {messages.map((m) => (
          <div key={m.id} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div
              className={`max-w-[85%] p-2.5 rounded-lg text-sm ${
                m.role === 'user'
                  ? 'bg-gradient-to-r from-emerald-600 to-blue-600 text-white'
                  : 'bg-white/[0.04] border border-white/[0.06] text-gray-200'
              }`}
            >
              <p className="whitespace-pre-wrap break-words">{m.content}</p>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex gap-2">
            <div className="bg-white/[0.04] border border-white/[0.06] p-2.5 rounded-lg">
              <div className="flex gap-1.5">
                <div className="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-pulse" />
                <div className="w-1.5 h-1.5 bg-emerald-400/70 rounded-full animate-pulse" style={{ animationDelay: '150ms' }} />
                <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-pulse" style={{ animationDelay: '300ms' }} />
              </div>
            </div>
          </div>
        )}
        {error && (
          <div className="bg-red-900/20 border border-red-500/20 text-red-400 text-xs p-2 rounded">{error}</div>
        )}
        <div ref={endRef} />
      </div>

      <div className="px-3 py-2 border-t border-white/[0.06]">
        <div className="flex gap-1.5 overflow-x-auto pb-1">
          {PROPOSAL_SUGGESTIONS.map((s) => (
            <button
              key={s}
              onClick={() => send(s)}
              disabled={loading}
              className="flex items-center gap-1 px-2 py-1 bg-white/[0.04] border border-white/[0.06] text-white/60 text-xs rounded-full whitespace-nowrap hover:bg-white/[0.08] hover:text-white"
            >
              <Sparkles className="w-3 h-3 text-emerald-400" />
              {s}
            </button>
          ))}
        </div>
      </div>

      <div className="p-3 border-t border-white/[0.06]">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                send();
              }
            }}
            placeholder="Ask about this proposal..."
            disabled={loading}
            className="flex-1 px-3 py-2 bg-white/[0.03] border border-white/[0.08] rounded-lg text-white text-sm placeholder-white/30 focus:ring-2 focus:ring-emerald-500/40 focus:border-emerald-500/30 disabled:opacity-50"
          />
          <button
            onClick={() => send()}
            disabled={loading || !input.trim()}
            className="px-3 py-2 bg-gradient-to-r from-emerald-500 to-blue-500 text-white rounded-lg hover:from-emerald-600 hover:to-blue-600 disabled:opacity-50"
          >
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
          </button>
        </div>
      </div>
    </div>
  );
}

/* ---------- Extract tab ---------- */

function ExtractTab({ proposalId, onFieldsApplied }: { proposalId: string; onFieldsApplied: () => void }) {
  const [content, setContent] = useState('');
  const [instruction, setInstruction] = useState('');
  const [loading, setLoading] = useState(false);
  const [applying, setApplying] = useState(false);
  const [result, setResult] = useState<ExtractResult | null>(null);
  const [selectedFields, setSelectedFields] = useState<Set<number>>(new Set());
  const [selectedPP, setSelectedPP] = useState<Set<number>>(new Set());
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  const onFileUpload = async (file: File) => {
    if (!file) return;
    if (file.size > 2_000_000) {
      setError('File too large (max 2MB). Paste text instead.');
      return;
    }
    setError(null);
    try {
      const text = await file.text();
      setContent((prev) => (prev ? `${prev}\n\n${text}` : text));
    } catch {
      setError('Could not read file as text');
    }
  };

  const runExtract = async () => {
    if (!content.trim()) {
      setError('Paste or upload content first');
      return;
    }
    setLoading(true);
    setError(null);
    setSuccess(null);
    setResult(null);
    setSelectedFields(new Set());
    setSelectedPP(new Set());
    try {
      const response = await assistantApi.extract(proposalId, content, instruction || undefined);
      const data: ExtractResult = response.data;
      setResult(data);
      // pre-select everything
      setSelectedFields(new Set(data.field_updates.map((_, i) => i)));
      setSelectedPP(new Set(data.new_past_performance.map((_, i) => i)));
      if (data.field_updates.length === 0 && data.new_past_performance.length === 0) {
        setError('No structured updates found in that content. Try being more specific or providing more context.');
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Extraction failed');
    } finally {
      setLoading(false);
    }
  };

  const applySelected = async () => {
    if (!result) return;
    const fieldUpdates = result.field_updates.filter((_, i) => selectedFields.has(i));
    const newPP = result.new_past_performance.filter((_, i) => selectedPP.has(i));
    if (fieldUpdates.length === 0 && newPP.length === 0) {
      setError('Select at least one update to apply');
      return;
    }
    setApplying(true);
    setError(null);
    try {
      const response = await assistantApi.applyExtract(proposalId, fieldUpdates, newPP);
      const data = response.data;
      setSuccess(
        `Applied ${data.applied_fields.length} field(s)` +
          (data.created_past_performance_ids.length
            ? ` and added ${data.created_past_performance_ids.length} past-performance record(s)`
            : '')
      );
      onFieldsApplied();
      setResult(null);
      setContent('');
      setInstruction('');
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Apply failed');
    } finally {
      setApplying(false);
    }
  };

  const toggleField = (i: number) => {
    setSelectedFields((prev) => {
      const next = new Set(prev);
      if (next.has(i)) next.delete(i);
      else next.add(i);
      return next;
    });
  };

  const togglePP = (i: number) => {
    setSelectedPP((prev) => {
      const next = new Set(prev);
      if (next.has(i)) next.delete(i);
      else next.add(i);
      return next;
    });
  };

  return (
    <div className="flex flex-col flex-1 overflow-hidden">
      <div className="flex-1 overflow-y-auto p-3 space-y-3">
        <div className="text-xs text-gray-400">
          Paste notes, past-performance write-ups, pricing tables, or RFP excerpts. The AI will extract field updates you can preview and apply.
        </div>

        <div>
          <label className="block text-xs text-gray-400 mb-1">Optional instruction</label>
          <input
            type="text"
            value={instruction}
            onChange={(e) => setInstruction(e.target.value)}
            placeholder='e.g. "Use the dollar figures for pricing only"'
            className="w-full px-2.5 py-1.5 bg-white/[0.03] border border-white/[0.08] rounded text-white text-xs placeholder-white/30 focus:ring-2 focus:ring-emerald-500/40"
          />
        </div>

        <div>
          <div className="flex items-center justify-between mb-1">
            <label className="text-xs text-gray-400">Content</label>
            <button
              onClick={() => fileRef.current?.click()}
              className="flex items-center gap-1 text-xs text-emerald-400 hover:text-emerald-300"
            >
              <Upload className="w-3 h-3" />
              Upload text file
            </button>
            <input
              ref={fileRef}
              type="file"
              accept=".txt,.md,.csv"
              onChange={(e) => e.target.files?.[0] && onFileUpload(e.target.files[0])}
              className="hidden"
            />
          </div>
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            rows={8}
            placeholder="Paste content here..."
            className="w-full px-2.5 py-2 bg-white/[0.03] border border-white/[0.08] rounded text-white text-xs placeholder-white/30 focus:ring-2 focus:ring-emerald-500/40 font-mono"
          />
        </div>

        <button
          onClick={runExtract}
          disabled={loading || !content.trim()}
          className="w-full flex items-center justify-center gap-2 px-3 py-2 bg-gradient-to-r from-emerald-500 to-blue-500 text-white text-sm rounded-lg hover:from-emerald-600 hover:to-blue-600 disabled:opacity-50"
        >
          {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Wand2 className="w-4 h-4" />}
          {loading ? 'Analyzing...' : 'Extract Updates'}
        </button>

        {error && (
          <div className="flex items-start gap-2 bg-red-900/20 border border-red-500/20 text-red-400 text-xs p-2 rounded">
            <AlertCircle className="w-3.5 h-3.5 flex-shrink-0 mt-0.5" />
            {error}
          </div>
        )}
        {success && (
          <div className="flex items-start gap-2 bg-emerald-900/20 border border-emerald-500/20 text-emerald-400 text-xs p-2 rounded">
            <Check className="w-3.5 h-3.5 flex-shrink-0 mt-0.5" />
            {success}
          </div>
        )}

        {result && (result.field_updates.length > 0 || result.new_past_performance.length > 0) && (
          <div className="space-y-2 pt-2 border-t border-white/[0.06]">
            <div className="flex items-center justify-between">
              <h4 className="text-xs font-semibold text-white">Proposed updates</h4>
              <span className="text-xs text-gray-500">
                {selectedFields.size + selectedPP.size} selected
              </span>
            </div>
            {result.summary && (
              <p className="text-xs text-gray-400 italic">{result.summary}</p>
            )}

            {result.field_updates.map((update, i) => (
              <button
                key={`f-${i}`}
                onClick={() => toggleField(i)}
                className={`w-full text-left p-2 rounded border transition-colors ${
                  selectedFields.has(i)
                    ? 'bg-emerald-500/10 border-emerald-500/30'
                    : 'bg-white/[0.03] border-white/[0.08] hover:bg-white/[0.05]'
                }`}
              >
                <div className="flex items-start gap-2">
                  <div
                    className={`mt-0.5 w-3.5 h-3.5 rounded flex items-center justify-center ${
                      selectedFields.has(i) ? 'bg-emerald-500 text-white' : 'border border-gray-500'
                    }`}
                  >
                    {selectedFields.has(i) && <Check className="w-2.5 h-2.5" />}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-xs font-semibold text-emerald-300">
                      {FIELD_LABELS[update.field] || update.field}
                    </div>
                    <div className="text-xs text-gray-300 mt-1 line-clamp-3 whitespace-pre-wrap">
                      {update.value.length > 200 ? `${update.value.slice(0, 200)}...` : update.value}
                    </div>
                    {update.note && (
                      <div className="text-xs text-gray-500 mt-1 italic">{update.note}</div>
                    )}
                  </div>
                </div>
              </button>
            ))}

            {result.new_past_performance.map((pp, i) => (
              <button
                key={`p-${i}`}
                onClick={() => togglePP(i)}
                className={`w-full text-left p-2 rounded border transition-colors ${
                  selectedPP.has(i)
                    ? 'bg-emerald-500/10 border-emerald-500/30'
                    : 'bg-white/[0.03] border-white/[0.08] hover:bg-white/[0.05]'
                }`}
              >
                <div className="flex items-start gap-2">
                  <div
                    className={`mt-0.5 w-3.5 h-3.5 rounded flex items-center justify-center ${
                      selectedPP.has(i) ? 'bg-emerald-500 text-white' : 'border border-gray-500'
                    }`}
                  >
                    {selectedPP.has(i) && <Check className="w-2.5 h-2.5" />}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-xs font-semibold text-blue-300">New Past Performance</div>
                    <div className="text-xs text-white mt-1">{pp.contract_name}</div>
                    <div className="text-xs text-gray-400">
                      {pp.agency && <span>{pp.agency}</span>}
                      {pp.contract_value && <span> · ${pp.contract_value.toLocaleString()}</span>}
                    </div>
                    {pp.description && (
                      <div className="text-xs text-gray-500 mt-1 line-clamp-2">{pp.description}</div>
                    )}
                  </div>
                </div>
              </button>
            ))}

            <button
              onClick={applySelected}
              disabled={applying || (selectedFields.size === 0 && selectedPP.size === 0)}
              className="w-full flex items-center justify-center gap-2 px-3 py-2 bg-emerald-600 text-white text-sm rounded-lg hover:bg-emerald-700 disabled:opacity-50"
            >
              {applying ? <Loader2 className="w-4 h-4 animate-spin" /> : <Check className="w-4 h-4" />}
              {applying ? 'Applying...' : `Apply ${selectedFields.size + selectedPP.size} update(s)`}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
