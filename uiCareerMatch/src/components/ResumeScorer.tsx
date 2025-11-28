import { useState, useEffect } from 'react';
import { Award, TrendingUp, Info, Loader } from 'lucide-react';
import { api } from '../utils/api';

interface ResumeScorerProps {
  userData: any;
}

export function ResumeScorer({ userData }: ResumeScorerProps) {
  const [scoreData, setScoreData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (userData) {
      loadScore();
    }
  }, [userData]);

  const loadScore = async () => {
    setLoading(true);
    try {
      const result = await api.scoreResume(userData);
      setScoreData(result);
    } catch (error) {
      console.error('Failed to load score:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!userData) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
        <Award className="mx-auto mb-4 text-gray-400" size={64} />
        <h3 className="text-gray-900 mb-2">No CV Data Available</h3>
        <p className="text-gray-600">Please upload your CV first to see your resume score</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
        <Loader className="animate-spin mx-auto mb-4 text-blue-600" size={48} />
        <p className="text-gray-600">Analyzing your resume...</p>
      </div>
    );
  }

  if (!scoreData) return null;

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreGradient = (score: number) => {
    if (score >= 80) return 'from-green-500 to-green-600';
    if (score >= 60) return 'from-yellow-500 to-yellow-600';
    return 'from-red-500 to-red-600';
  };

  return (
    <div className="space-y-6">
      {/* Overall Score */}
      <div className={`bg-gradient-to-r ${getScoreGradient(scoreData.overallScore)} rounded-xl shadow-lg p-8 text-white`}>
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-white mb-2">Resume Score</h2>
            <p className="text-white/80">Based on industry standards and AI analysis</p>
          </div>
          <div className="text-right">
            <div className="text-6xl text-white mb-2">{scoreData.overallScore}</div>
            <div className="text-white/80">out of 100</div>
          </div>
        </div>
      </div>

      {/* Score Breakdown */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-gray-900 mb-6">Detailed Breakdown</h3>
        <div className="space-y-4">
          {Object.entries(scoreData.breakdown).map(([key, data]: [string, any]) => (
            <div key={key} className="space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="text-gray-900 capitalize">{key.replace(/([A-Z])/g, ' $1').trim()}</span>
                  <div className="group relative">
                    <Info size={16} className="text-gray-400 cursor-help" />
                    <div className="absolute left-0 bottom-full mb-2 w-64 bg-gray-900 text-white text-xs rounded-lg p-3 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-10">
                      {data.explanation}
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-gray-500 text-sm">Weight: {data.weight}%</span>
                  <span className={`${getScoreColor(data.score)}`}>{data.score}/100</span>
                </div>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className={`h-2 rounded-full transition-all duration-500 ${
                    data.score >= 80 ? 'bg-green-500' : data.score >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                  }`}
                  style={{ width: `${data.score}%` }}
                />
              </div>
              <p className="text-gray-600 text-sm">{data.explanation}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Improvements */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-center gap-2 mb-4">
          <TrendingUp className="text-blue-600" size={24} />
          <h3 className="text-gray-900">Improvement Suggestions</h3>
        </div>
        <div className="space-y-3">
          {scoreData.improvements.map((improvement: string, idx: number) => (
            <div key={idx} className="flex gap-3 p-4 bg-blue-50 rounded-lg border border-blue-200">
              <div className="text-blue-600 shrink-0">{idx + 1}</div>
              <p className="text-gray-700">{improvement}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Explainability Section */}
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-xl border border-purple-200 p-6">
        <h3 className="text-gray-900 mb-3">🔍 Explainable AI Scoring</h3>
        <p className="text-gray-700 mb-4">
          Our scoring system uses transparent AI models to evaluate your resume. Each score component is weighted based on industry research and recruiter preferences. The explanations show exactly why you received each score, ensuring complete transparency in the evaluation process.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white rounded-lg p-4">
            <div className="text-purple-600 mb-2">🎯 Weighted Scoring</div>
            <p className="text-gray-600 text-sm">Each category is weighted by importance to employers</p>
          </div>
          <div className="bg-white rounded-lg p-4">
            <div className="text-purple-600 mb-2">📊 Data-Driven</div>
            <p className="text-gray-600 text-sm">Based on analysis of thousands of successful resumes</p>
          </div>
          <div className="bg-white rounded-lg p-4">
            <div className="text-purple-600 mb-2">💬 Actionable Feedback</div>
            <p className="text-gray-600 text-sm">Specific suggestions for improvement</p>
          </div>
        </div>
      </div>
    </div>
  );
}
