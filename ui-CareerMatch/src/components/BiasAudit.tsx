import { useState, useEffect } from 'react';
import { Scale, CheckCircle, AlertTriangle, Info, Loader } from 'lucide-react';
import { api } from '../utils/api';

interface BiasAuditProps {
  userData: any;
}

export function BiasAudit({ userData }: BiasAuditProps) {
  const [auditData, setAuditData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (userData) {
      loadAudit();
    }
  }, [userData]);

  const loadAudit = async () => {
    setLoading(true);
    try {
      const result = await api.runBiasAudit(userData);
      setAuditData(result);
    } catch (error) {
      console.error('Failed to load audit:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!userData) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
        <Scale className="mx-auto mb-4 text-gray-400" size={64} />
        <h3 className="text-gray-900 mb-2">No CV Data Available</h3>
        <p className="text-gray-600">Please upload your CV first to run a bias audit</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
        <Loader className="animate-spin mx-auto mb-4 text-blue-600" size={48} />
        <p className="text-gray-600">Running fairness audit...</p>
      </div>
    );
  }

  if (!auditData) return null;

  const getStatusIcon = (status: string) => {
    if (status === 'pass') return <CheckCircle className="text-green-600" size={24} />;
    if (status === 'warning') return <AlertTriangle className="text-yellow-600" size={24} />;
    return <AlertTriangle className="text-red-600" size={24} />;
  };

  const getStatusColor = (status: string) => {
    if (status === 'pass') return 'border-green-200 bg-green-50';
    if (status === 'warning') return 'border-yellow-200 bg-yellow-50';
    return 'border-red-200 bg-red-50';
  };

  const getScoreColor = (score: number) => {
    if (score >= 85) return 'text-green-600';
    if (score >= 70) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="space-y-6">
      {/* Overall Fairness Score */}
      <div className="bg-gradient-to-r from-green-500 to-emerald-600 rounded-xl shadow-lg p-8 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-white mb-2">Fairness Score</h2>
            <p className="text-white/80">Comprehensive bias and fairness analysis</p>
          </div>
          <div className="text-right">
            <div className="text-6xl text-white mb-2">{auditData.overallFairnessScore}</div>
            <div className="text-white/80">out of 100</div>
          </div>
        </div>
      </div>

      {/* Audit Categories */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-center gap-2 mb-6">
          <Scale className="text-blue-600" size={24} />
          <h3 className="text-gray-900">Bias Audit Results</h3>
        </div>
        <div className="space-y-4">
          {auditData.audits.map((audit: any, idx: number) => (
            <div key={idx} className={`border rounded-lg p-5 ${getStatusColor(audit.status)}`}>
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-3">
                  {getStatusIcon(audit.status)}
                  <div>
                    <h4 className="text-gray-900">{audit.category}</h4>
                    <div className="flex items-center gap-2 mt-1">
                      <span className={`text-sm ${getScoreColor(audit.score)}`}>
                        Score: {audit.score}/100
                      </span>
                      <span className="text-gray-400">•</span>
                      <span className="text-sm text-gray-600 capitalize">{audit.status}</span>
                    </div>
                  </div>
                </div>
              </div>
              <p className="text-gray-700 ml-9">{audit.details}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Recommendations */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-center gap-2 mb-4">
          <Info className="text-blue-600" size={24} />
          <h3 className="text-gray-900">Recommendations</h3>
        </div>
        <div className="space-y-3">
          {auditData.recommendations.map((rec: string, idx: number) => (
            <div key={idx} className="flex gap-3 p-4 bg-blue-50 rounded-lg border border-blue-200">
              <div className="text-blue-600 shrink-0">{idx + 1}</div>
              <p className="text-gray-700">{rec}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Fairness Methodology */}
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-xl border border-purple-200 p-6">
        <h3 className="text-gray-900 mb-3">⚖️ Fairness Audit Methodology</h3>
        <p className="text-gray-700 mb-4">
          Our bias audit system evaluates your resume against multiple fairness criteria to ensure equitable evaluation. We check for potential biases related to:
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-white rounded-lg p-4">
            <div className="text-purple-600 mb-2">👥 Gender Bias</div>
            <p className="text-gray-600 text-sm">Detects gendered language and ensures neutral terminology</p>
          </div>
          <div className="bg-white rounded-lg p-4">
            <div className="text-purple-600 mb-2">📅 Age Bias</div>
            <p className="text-gray-600 text-sm">Checks for age-indicating information that may introduce bias</p>
          </div>
          <div className="bg-white rounded-lg p-4">
            <div className="text-purple-600 mb-2">🌍 Cultural Bias</div>
            <p className="text-gray-600 text-sm">Ensures inclusive language and cultural neutrality</p>
          </div>
          <div className="bg-white rounded-lg p-4">
            <div className="text-purple-600 mb-2">💼 Socioeconomic Bias</div>
            <p className="text-gray-600 text-sm">Focuses on skills over institutional prestige</p>
          </div>
        </div>
        <div className="mt-4 p-4 bg-white rounded-lg border border-purple-200">
          <p className="text-gray-600 text-sm">
            <strong className="text-gray-900">Why it matters:</strong> Fair evaluation systems lead to better hiring decisions and more diverse teams. Our audit helps ensure your resume is evaluated based on your skills and experience, not demographic factors.
          </p>
        </div>
      </div>

      {/* Trust & Transparency */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl shadow-lg p-6 text-white">
        <h3 className="text-white mb-3">🔒 Trust & Transparency</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <div className="text-2xl mb-2">✓</div>
            <div className="text-white/90 text-sm">Transparent evaluation criteria</div>
          </div>
          <div>
            <div className="text-2xl mb-2">✓</div>
            <div className="text-white/90 text-sm">Explainable AI decisions</div>
          </div>
          <div>
            <div className="text-2xl mb-2">✓</div>
            <div className="text-white/90 text-sm">Regular fairness audits</div>
          </div>
        </div>
      </div>
    </div>
  );
}
