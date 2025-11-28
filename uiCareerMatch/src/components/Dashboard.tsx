import { FileText, Target, TrendingUp, Award, Upload } from 'lucide-react';

interface DashboardProps {
  userData: any;
  setActiveTab: (tab: string) => void;
}

export function Dashboard({ userData, setActiveTab }: DashboardProps) {
  const stats = [
    { label: 'Resume Score', value: userData ? '82/100' : '--', icon: Award, color: 'blue' },
    { label: 'Fairness Score', value: userData ? '91/100' : '--', icon: Target, color: 'green' },
    { label: 'Skill Level', value: userData ? 'Level 12' : '--', icon: TrendingUp, color: 'purple' },
    { label: 'Projects Completed', value: '0', icon: FileText, color: 'orange' },
  ];

  const quickActions = [
    { label: 'Upload New CV', tab: 'cv-parser', icon: '📄', color: 'from-blue-500 to-blue-600' },
    { label: 'View Recommendations', tab: 'recommendations', icon: '💡', color: 'from-purple-500 to-purple-600' },
    { label: 'Skill Tree', tab: 'skill-tree', icon: '🌳', color: 'from-green-500 to-green-600' },
    { label: 'Career Roadmap', tab: 'roadmap', icon: '🗺️', color: 'from-orange-500 to-orange-600' },
  ];

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl shadow-lg p-8 text-white">
        <h2 className="text-white mb-2">Welcome to CareerMatch</h2>
        <p className="text-blue-100 mb-6">
          Your AI-powered career assistant for resume analysis, skill development, and career growth
        </p>
        {!userData && (
          <button
            onClick={() => setActiveTab('cv-parser')}
            className="bg-white text-blue-600 px-6 py-3 rounded-lg hover:bg-blue-50 transition-colors flex items-center gap-2"
          >
            <Upload size={20} />
            Get Started - Upload Your CV
          </button>
        )}
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          const colorClasses = {
            blue: 'bg-blue-100 text-blue-600',
            green: 'bg-green-100 text-green-600',
            purple: 'bg-purple-100 text-purple-600',
            orange: 'bg-orange-100 text-orange-600',
          }[stat.color];

          return (
            <div key={index} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-4">
                <div className={`w-12 h-12 rounded-lg ${colorClasses} flex items-center justify-center`}>
                  <Icon size={24} />
                </div>
              </div>
              <div className="text-gray-500 text-sm mb-1">{stat.label}</div>
              <div className="text-gray-900">{stat.value}</div>
            </div>
          );
        })}
      </div>

      {/* Quick Actions */}
      <div>
        <h3 className="text-gray-900 mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {quickActions.map((action, index) => (
            <button
              key={index}
              onClick={() => setActiveTab(action.tab)}
              className={`bg-gradient-to-br ${action.color} rounded-xl shadow-md p-6 text-white hover:shadow-lg transition-all transform hover:-translate-y-1`}
            >
              <div className="text-4xl mb-3">{action.icon}</div>
              <div>{action.label}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Features Overview */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-gray-900 mb-4">Platform Features</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="flex gap-3">
            <div className="text-2xl">📊</div>
            <div>
              <div className="text-gray-900 mb-1">Resume Scoring & Analysis</div>
              <div className="text-gray-600 text-sm">Get detailed scoring with explainable AI insights</div>
            </div>
          </div>
          <div className="flex gap-3">
            <div className="text-2xl">⚖️</div>
            <div>
              <div className="text-gray-900 mb-1">Bias & Fairness Audits</div>
              <div className="text-gray-600 text-sm">Ensure equitable and unbiased resume evaluation</div>
            </div>
          </div>
          <div className="flex gap-3">
            <div className="text-2xl">🎯</div>
            <div>
              <div className="text-gray-900 mb-1">Personalized Recommendations</div>
              <div className="text-gray-600 text-sm">AI-driven projects and learning paths</div>
            </div>
          </div>
          <div className="flex gap-3">
            <div className="text-2xl">🌳</div>
            <div>
              <div className="text-gray-900 mb-1">Gamified Skill Tree</div>
              <div className="text-gray-600 text-sm">Track progress and unlock achievements</div>
            </div>
          </div>
          <div className="flex gap-3">
            <div className="text-2xl">🕸️</div>
            <div>
              <div className="text-gray-900 mb-1">Knowledge Graph</div>
              <div className="text-gray-600 text-sm">Visualize skill connections and career paths</div>
            </div>
          </div>
          <div className="flex gap-3">
            <div className="text-2xl">✨</div>
            <div>
              <div className="text-gray-900 mb-1">Resume Polishing</div>
              <div className="text-gray-600 text-sm">AI-powered suggestions for improvement</div>
            </div>
          </div>
        </div>
      </div>

      {/* API Integration Notice */}
      <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-6">
        <h3 className="text-yellow-900 mb-2">🔧 Flask Backend Integration</h3>
        <p className="text-yellow-800 text-sm mb-3">
          This frontend is ready to connect to your Flask backend. Update the <code className="bg-yellow-100 px-2 py-1 rounded">FLASK_API_URL</code> in <code className="bg-yellow-100 px-2 py-1 rounded">/utils/api.ts</code> to point to your Flask server.
        </p>
        <p className="text-yellow-800 text-sm">
          Currently using mock data for demonstration. Uncomment the actual API calls in the api.ts file once your Flask backend is running.
        </p>
      </div>
    </div>
  );
}
