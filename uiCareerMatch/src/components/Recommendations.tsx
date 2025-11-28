import { useState, useEffect } from 'react';
import { Lightbulb, Target, TrendingUp, Loader, Zap } from 'lucide-react';
import { api } from '../utils/api';

interface RecommendationsProps {
  userData: any;
}

export function Recommendations({ userData }: RecommendationsProps) {
  const [recommendations, setRecommendations] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (userData) {
      loadRecommendations();
    }
  }, [userData]);

  const loadRecommendations = async () => {
    setLoading(true);
    try {
      const result = await api.getRecommendations('user-123', userData);
      setRecommendations(result);
    } catch (error) {
      console.error('Failed to load recommendations:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!userData) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
        <Lightbulb className="mx-auto mb-4 text-gray-400" size={64} />
        <h3 className="text-gray-900 mb-2">No CV Data Available</h3>
        <p className="text-gray-600">Please upload your CV first to get personalized recommendations</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
        <Loader className="animate-spin mx-auto mb-4 text-blue-600" size={48} />
        <p className="text-gray-600">Generating personalized recommendations...</p>
      </div>
    );
  }

  if (!recommendations) return null;

  const getDifficultyColor = (difficulty: string) => {
    if (difficulty === 'beginner') return 'bg-green-100 text-green-700 border-green-200';
    if (difficulty === 'intermediate') return 'bg-yellow-100 text-yellow-700 border-yellow-200';
    return 'bg-red-100 text-red-700 border-red-200';
  };

  const getPriorityColor = (priority: string) => {
    if (priority === 'high') return 'bg-red-100 text-red-700';
    if (priority === 'medium') return 'bg-yellow-100 text-yellow-700';
    return 'bg-blue-100 text-blue-700';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-xl shadow-lg p-8 text-white">
        <div className="flex items-center gap-3 mb-2">
          <Lightbulb size={32} />
          <h2 className="text-white">Personalized Recommendations</h2>
        </div>
        <p className="text-white/80">AI-driven suggestions tailored to your career goals</p>
      </div>

      {/* Micro-Projects */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-center gap-2 mb-6">
          <Target className="text-blue-600" size={24} />
          <h3 className="text-gray-900">Recommended Micro-Projects</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {recommendations.microProjects.map((project: any, idx: number) => (
            <div key={idx} className="border border-gray-200 rounded-lg p-5 hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between mb-3">
                <h4 className="text-gray-900 flex-1">{project.title}</h4>
                <Zap className="text-yellow-500 shrink-0" size={20} />
              </div>
              <div className="flex items-center gap-2 mb-3">
                <span className={`text-xs px-2 py-1 rounded-full border ${getDifficultyColor(project.difficulty)}`}>
                  {project.difficulty}
                </span>
                <span className="text-xs text-gray-500">⏱️ {project.estimatedTime}</span>
              </div>
              <div className="flex flex-wrap gap-1 mb-3">
                {project.skills.map((skill: string, skillIdx: number) => (
                  <span key={skillIdx} className="text-xs bg-blue-50 text-blue-700 px-2 py-1 rounded">
                    {skill}
                  </span>
                ))}
              </div>
              <div className="flex items-center justify-between">
                <div className="text-xs text-gray-500">
                  Engagement Score: {project.engagementScore}%
                </div>
                <button className="text-blue-600 hover:text-blue-700 text-sm">
                  Start →
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Skill Gaps */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-center gap-2 mb-6">
          <TrendingUp className="text-orange-600" size={24} />
          <h3 className="text-gray-900">Skill Gap Analysis</h3>
        </div>
        <div className="space-y-4">
          {recommendations.skillGaps.map((gap: any, idx: number) => (
            <div key={idx} className="border border-gray-200 rounded-lg p-5">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-3">
                  <h4 className="text-gray-900">{gap.skill}</h4>
                  <span className={`text-xs px-2 py-1 rounded-full ${getPriorityColor(gap.priority)}`}>
                    {gap.priority} priority
                  </span>
                </div>
                <div className="text-gray-600 text-sm">
                  Target: {gap.targetLevel}%
                </div>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-xs text-gray-500">
                  <span>Current Level</span>
                  <span>Target Level</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3 relative">
                  <div
                    className="bg-blue-600 h-3 rounded-full transition-all"
                    style={{ width: `${gap.currentLevel}%` }}
                  />
                  <div
                    className="absolute top-0 h-3 border-r-2 border-green-500"
                    style={{ left: `${gap.targetLevel}%` }}
                  />
                </div>
                <div className="text-xs text-gray-600">
                  Gap: {gap.targetLevel - gap.currentLevel} points to target
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Next Steps */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-gray-900 mb-4">Recommended Next Steps</h3>
        <div className="space-y-3">
          {recommendations.nextSteps.map((step: string, idx: number) => (
            <div key={idx} className="flex items-start gap-3 p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border border-blue-200">
              <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center shrink-0">
                {idx + 1}
              </div>
              <p className="text-gray-700 pt-1">{step}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Adaptive System Info */}
      <div className="bg-gradient-to-r from-green-50 to-blue-50 rounded-xl border border-green-200 p-6">
        <h3 className="text-gray-900 mb-3">🎯 Adaptive Recommendation System</h3>
        <p className="text-gray-700 mb-4">
          Our AI-powered recommendation engine continuously learns from your progress and adapts suggestions to your learning style, career goals, and current skill level. Each recommendation is scored for engagement potential to keep you motivated.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white rounded-lg p-4">
            <div className="text-green-600 mb-2">🧠 Personalized</div>
            <p className="text-gray-600 text-sm">Tailored to your unique career path</p>
          </div>
          <div className="bg-white rounded-lg p-4">
            <div className="text-green-600 mb-2">📈 Adaptive</div>
            <p className="text-gray-600 text-sm">Updates based on your progress</p>
          </div>
          <div className="bg-white rounded-lg p-4">
            <div className="text-green-600 mb-2">🎮 Engaging</div>
            <p className="text-gray-600 text-sm">Optimized for motivation and completion</p>
          </div>
        </div>
      </div>
    </div>
  );
}
