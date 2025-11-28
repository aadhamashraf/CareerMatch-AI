import { useState, useEffect } from 'react';
import { Map, Target, TrendingUp, Loader, CheckCircle2 } from 'lucide-react';
import { api } from '../utils/api';

interface CareerRoadmapProps {
  userData: any;
}

export function CareerRoadmap({ userData }: CareerRoadmapProps) {
  const [roadmap, setRoadmap] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [currentRole, setCurrentRole] = useState('Senior Software Engineer');
  const [targetRole, setTargetRole] = useState('Tech Lead');
  const [showForm, setShowForm] = useState(!userData);

  useEffect(() => {
    if (userData && !showForm) {
      loadRoadmap();
    }
  }, [userData, showForm]);

  const loadRoadmap = async () => {
    setLoading(true);
    try {
      const result = await api.getCareerRoadmap(currentRole, targetRole);
      setRoadmap(result);
    } catch (error) {
      console.error('Failed to load roadmap:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = () => {
    setShowForm(false);
    loadRoadmap();
  };

  if (!userData) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
        <Map className="mx-auto mb-4 text-gray-400" size={64} />
        <h3 className="text-gray-900 mb-2">No CV Data Available</h3>
        <p className="text-gray-600">Please upload your CV first to generate your career roadmap</p>
      </div>
    );
  }

  if (showForm) {
    return (
      <div className="space-y-6">
        <div className="bg-gradient-to-r from-teal-600 to-cyan-600 rounded-xl shadow-lg p-8 text-white">
          <div className="flex items-center gap-3 mb-2">
            <Map size={32} />
            <h2 className="text-white">Career Roadmap</h2>
          </div>
          <p className="text-white/80">Plan your path from current role to dream career</p>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-gray-900 mb-6">Define Your Career Path</h3>
          <div className="space-y-6">
            <div>
              <label className="text-gray-700 mb-2 block">Current Role</label>
              <input
                type="text"
                value={currentRole}
                onChange={(e) => setCurrentRole(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="e.g., Senior Software Engineer"
              />
            </div>
            <div>
              <label className="text-gray-700 mb-2 block">Target Role</label>
              <input
                type="text"
                value={targetRole}
                onChange={(e) => setTargetRole(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="e.g., Engineering Manager"
              />
            </div>
            <button
              onClick={handleGenerate}
              className="w-full bg-gradient-to-r from-teal-600 to-cyan-600 text-white py-3 rounded-lg hover:from-teal-700 hover:to-cyan-700 transition-all"
            >
              Generate Roadmap
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
        <Loader className="animate-spin mx-auto mb-4 text-blue-600" size={48} />
        <p className="text-gray-600">Generating your personalized career roadmap...</p>
      </div>
    );
  }

  if (!roadmap) return null;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-teal-600 to-cyan-600 rounded-xl shadow-lg p-8 text-white">
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <Map size={32} />
              <h2 className="text-white">Career Roadmap</h2>
            </div>
            <p className="text-white/80">Your personalized path to {roadmap.targetRole}</p>
          </div>
          <button
            onClick={() => setShowForm(true)}
            className="bg-white text-teal-600 px-4 py-2 rounded-lg hover:bg-teal-50 transition-colors"
          >
            Change Goals
          </button>
        </div>
      </div>

      {/* Timeline Overview */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="text-gray-900">Career Transition Timeline</h3>
            <p className="text-gray-600 text-sm">Estimated: {roadmap.estimatedTimeline}</p>
          </div>
          <div className="flex items-center gap-2">
            <Target className="text-teal-600" size={24} />
            <span className="text-gray-900">{roadmap.targetRole}</span>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="relative">
          <div className="absolute left-8 top-0 bottom-0 w-1 bg-gradient-to-b from-teal-400 via-cyan-400 to-purple-400" />
          
          <div className="space-y-8">
            {roadmap.milestones.map((milestone: any, idx: number) => (
              <div key={idx} className="relative pl-20">
                <div className="absolute left-0 w-16 h-16 bg-gradient-to-br from-teal-500 to-cyan-500 rounded-full flex items-center justify-center text-white text-xl shadow-lg z-10">
                  {idx + 1}
                </div>
                <div className="bg-gradient-to-r from-teal-50 to-cyan-50 rounded-xl p-6 border-2 border-teal-200">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h4 className="text-gray-900 mb-1">{milestone.title}</h4>
                      <div className="flex items-center gap-2 text-sm text-gray-600">
                        <TrendingUp size={16} />
                        <span>{milestone.timeframe}</span>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-3 mb-4">
                    <div className="text-sm text-gray-700">Key Tasks:</div>
                    {milestone.tasks.map((task: string, taskIdx: number) => (
                      <div key={taskIdx} className="flex items-start gap-2 text-gray-700">
                        <CheckCircle2 size={16} className="text-teal-600 shrink-0 mt-0.5" />
                        <span className="text-sm">{task}</span>
                      </div>
                    ))}
                  </div>

                  <div>
                    <div className="text-sm text-gray-700 mb-2">Skills to Develop:</div>
                    <div className="flex flex-wrap gap-2">
                      {milestone.skills.map((skill: string, skillIdx: number) => (
                        <span key={skillIdx} className="text-xs bg-teal-100 text-teal-700 px-3 py-1 rounded-full">
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="text-teal-600 mb-2">Total Milestones</div>
          <div className="text-gray-900 text-3xl">{roadmap.milestones.length}</div>
        </div>
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="text-cyan-600 mb-2">Total Tasks</div>
          <div className="text-gray-900 text-3xl">
            {roadmap.milestones.reduce((acc: number, m: any) => acc + m.tasks.length, 0)}
          </div>
        </div>
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="text-purple-600 mb-2">Skills Required</div>
          <div className="text-gray-900 text-3xl">
            {new Set(roadmap.milestones.flatMap((m: any) => m.skills)).size}
          </div>
        </div>
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="text-orange-600 mb-2">Timeline</div>
          <div className="text-gray-900">{roadmap.estimatedTimeline}</div>
        </div>
      </div>

      {/* Skills Overview */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-gray-900 mb-4">All Skills to Master</h3>
        <div className="flex flex-wrap gap-2">
          {Array.from(new Set(roadmap.milestones.flatMap((m: any) => m.skills))).map((skill: any, idx: number) => (
            <span key={idx} className="bg-gradient-to-r from-teal-100 to-cyan-100 text-teal-700 px-4 py-2 rounded-lg border border-teal-300">
              {skill}
            </span>
          ))}
        </div>
      </div>

      {/* Transparent Roadmap Info */}
      <div className="bg-gradient-to-r from-teal-50 to-cyan-50 rounded-xl border border-teal-200 p-6">
        <h3 className="text-gray-900 mb-3">🗺️ Transparent Career Roadmap</h3>
        <p className="text-gray-700 mb-4">
          Our AI-generated roadmap analyzes your current skills, target role requirements, and industry trends to create a realistic, step-by-step plan. Each milestone includes specific tasks, required skills, and timeframes based on average career progression data.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white rounded-lg p-4">
            <div className="text-teal-600 mb-2">📊 Data-Driven</div>
            <p className="text-gray-600 text-sm">Based on real career transition timelines</p>
          </div>
          <div className="bg-white rounded-lg p-4">
            <div className="text-teal-600 mb-2">🎯 Personalized</div>
            <p className="text-gray-600 text-sm">Tailored to your current skills and goals</p>
          </div>
          <div className="bg-white rounded-lg p-4">
            <div className="text-teal-600 mb-2">✨ Actionable</div>
            <p className="text-gray-600 text-sm">Clear tasks and milestones</p>
          </div>
        </div>
      </div>

      {/* Export Options */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-gray-900 mb-4">Export Your Roadmap</h3>
        <div className="flex flex-wrap gap-3">
          <button className="bg-gradient-to-r from-teal-600 to-cyan-600 text-white px-6 py-3 rounded-lg hover:from-teal-700 hover:to-cyan-700 transition-all">
            Download as PDF
          </button>
          <button className="border-2 border-teal-600 text-teal-600 px-6 py-3 rounded-lg hover:bg-teal-50 transition-colors">
            Export to Calendar
          </button>
          <button className="border-2 border-cyan-600 text-cyan-600 px-6 py-3 rounded-lg hover:bg-cyan-50 transition-colors">
            Share with Mentor
          </button>
        </div>
      </div>
    </div>
  );
}
