import { useState, useEffect } from 'react';
import { Sparkles, CheckCircle, AlertCircle, Loader } from 'lucide-react';
import { api } from '../utils/api';

interface ResumePolisherProps {
  userData: any;
}

export function ResumePolisher({ userData }: ResumePolisherProps) {
  const [polishData, setPolishData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [appliedSuggestions, setAppliedSuggestions] = useState<Set<number>>(new Set());

  useEffect(() => {
    if (userData) {
      loadPolish();
    }
  }, [userData]);

  const loadPolish = async () => {
    setLoading(true);
    try {
      const result = await api.polishResume(userData);
      setPolishData(result);
    } catch (error) {
      console.error('Failed to load polish suggestions:', error);
    } finally {
      setLoading(false);
    }
  };

  const toggleSuggestion = (idx: number) => {
    setAppliedSuggestions(prev => {
      const newSet = new Set(prev);
      if (newSet.has(idx)) {
        newSet.delete(idx);
      } else {
        newSet.add(idx);
      }
      return newSet;
    });
  };

  if (!userData) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
        <Sparkles className="mx-auto mb-4 text-gray-400" size={64} />
        <h3 className="text-gray-900 mb-2">No CV Data Available</h3>
        <p className="text-gray-600">Please upload your CV first to get polishing suggestions</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
        <Loader className="animate-spin mx-auto mb-4 text-blue-600" size={48} />
        <p className="text-gray-600">Analyzing your resume for improvements...</p>
      </div>
    );
  }

  if (!polishData) return null;

  const getPriorityColor = (priority: string) => {
    if (priority === 'high') return 'border-red-400 bg-red-50';
    if (priority === 'medium') return 'border-yellow-400 bg-yellow-50';
    return 'border-blue-400 bg-blue-50';
  };

  const getPriorityBadge = (priority: string) => {
    if (priority === 'high') return 'bg-red-100 text-red-700';
    if (priority === 'medium') return 'bg-yellow-100 text-yellow-700';
    return 'bg-blue-100 text-blue-700';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-pink-600 to-purple-600 rounded-xl shadow-lg p-8 text-white">
        <div className="flex items-center gap-3 mb-2">
          <Sparkles size={32} />
          <h2 className="text-white">Resume Polish</h2>
        </div>
        <p className="text-white/80">AI-powered suggestions to enhance your resume impact</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="text-purple-600 mb-2">Total Suggestions</div>
          <div className="text-gray-900 text-3xl">{polishData.suggestions.length}</div>
        </div>
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="text-green-600 mb-2">Applied</div>
          <div className="text-gray-900 text-3xl">{appliedSuggestions.size}</div>
        </div>
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="text-orange-600 mb-2">High Priority</div>
          <div className="text-gray-900 text-3xl">
            {polishData.suggestions.filter((s: any) => s.priority === 'high').length}
          </div>
        </div>
      </div>

      {/* Suggestions */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-gray-900 mb-6">Improvement Suggestions</h3>
        <div className="space-y-4">
          {polishData.suggestions.map((suggestion: any, idx: number) => (
            <div
              key={idx}
              className={`border-2 rounded-lg p-5 transition-all ${getPriorityColor(suggestion.priority)} ${
                appliedSuggestions.has(idx) ? 'opacity-50' : ''
              }`}
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  {appliedSuggestions.has(idx) ? (
                    <CheckCircle className="text-green-600 shrink-0" size={24} />
                  ) : (
                    <AlertCircle className="text-orange-600 shrink-0" size={24} />
                  )}
                  <div>
                    <div className="text-gray-900 mb-1">{suggestion.section}</div>
                    <span className={`text-xs px-2 py-1 rounded-full ${getPriorityBadge(suggestion.priority)}`}>
                      {suggestion.priority} priority
                    </span>
                  </div>
                </div>
                <button
                  onClick={() => toggleSuggestion(idx)}
                  className={`px-4 py-2 rounded-lg transition-colors ${
                    appliedSuggestions.has(idx)
                      ? 'bg-gray-200 text-gray-600'
                      : 'bg-purple-600 text-white hover:bg-purple-700'
                  }`}
                >
                  {appliedSuggestions.has(idx) ? 'Undo' : 'Apply'}
                </button>
              </div>

              <div className="space-y-3">
                <div>
                  <div className="text-sm text-gray-600 mb-2">Original:</div>
                  <div className="bg-white p-3 rounded border border-gray-300 text-gray-700">
                    {suggestion.original}
                  </div>
                </div>
                <div className="flex items-center justify-center">
                  <div className="text-purple-600">↓</div>
                </div>
                <div>
                  <div className="text-sm text-gray-600 mb-2">Improved:</div>
                  <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-3 rounded border border-purple-300 text-gray-900">
                    {suggestion.improved}
                  </div>
                </div>
                <div className="pt-3 border-t border-gray-300">
                  <div className="text-sm text-gray-600 mb-1">Why this improves your resume:</div>
                  <p className="text-gray-700">{suggestion.reason}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Enhanced Preview */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-gray-900">Enhanced Resume Preview</h3>
          <button className="bg-gradient-to-r from-pink-600 to-purple-600 text-white px-4 py-2 rounded-lg hover:from-pink-700 hover:to-purple-700 transition-all">
            Download Enhanced Version
          </button>
        </div>
        <div className="bg-gray-50 rounded-lg p-6 border border-gray-200">
          <div className="text-gray-700 whitespace-pre-line">
            {polishData.enhancedVersion}
          </div>
          <div className="mt-4 p-4 bg-blue-50 rounded border border-blue-200 text-blue-700 text-sm">
            This is a preview of your enhanced resume with all high-priority suggestions applied.
          </div>
        </div>
      </div>

      {/* Quick Tips */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-gray-900 mb-4">✨ Quick Polish Tips</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="flex gap-3 p-4 bg-purple-50 rounded-lg border border-purple-200">
            <div className="text-2xl shrink-0">💪</div>
            <div>
              <div className="text-gray-900 mb-1">Use Action Verbs</div>
              <p className="text-gray-600 text-sm">Start bullet points with powerful action verbs like "Led," "Optimized," "Architected"</p>
            </div>
          </div>
          <div className="flex gap-3 p-4 bg-purple-50 rounded-lg border border-purple-200">
            <div className="text-2xl shrink-0">📊</div>
            <div>
              <div className="text-gray-900 mb-1">Quantify Achievements</div>
              <p className="text-gray-600 text-sm">Add numbers, percentages, and metrics to demonstrate impact</p>
            </div>
          </div>
          <div className="flex gap-3 p-4 bg-purple-50 rounded-lg border border-purple-200">
            <div className="text-2xl shrink-0">🎯</div>
            <div>
              <div className="text-gray-900 mb-1">Be Specific</div>
              <p className="text-gray-600 text-sm">Replace vague terms with specific technologies, methodologies, and outcomes</p>
            </div>
          </div>
          <div className="flex gap-3 p-4 bg-purple-50 rounded-lg border border-purple-200">
            <div className="text-2xl shrink-0">✂️</div>
            <div>
              <div className="text-gray-900 mb-1">Be Concise</div>
              <p className="text-gray-600 text-sm">Remove unnecessary words while keeping all essential information</p>
            </div>
          </div>
        </div>
      </div>

      {/* Polish Methodology */}
      <div className="bg-gradient-to-r from-pink-50 to-purple-50 rounded-xl border border-pink-200 p-6">
        <h3 className="text-gray-900 mb-3">✨ AI-Powered Resume Polishing</h3>
        <p className="text-gray-700 mb-4">
          Our polishing engine uses natural language processing and industry best practices to enhance your resume. Each suggestion is prioritized and explained, helping you make informed decisions about your resume content.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white rounded-lg p-4">
            <div className="text-pink-600 mb-2">🔍 Deep Analysis</div>
            <p className="text-gray-600 text-sm">Examines language, structure, and impact</p>
          </div>
          <div className="bg-white rounded-lg p-4">
            <div className="text-pink-600 mb-2">💡 Smart Suggestions</div>
            <p className="text-gray-600 text-sm">Context-aware improvements</p>
          </div>
          <div className="bg-white rounded-lg p-4">
            <div className="text-pink-600 mb-2">⚡ Instant Iteration</div>
            <p className="text-gray-600 text-sm">Apply and preview changes immediately</p>
          </div>
        </div>
      </div>
    </div>
  );
}
