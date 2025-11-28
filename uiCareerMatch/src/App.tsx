import { useState } from 'react';
import { Dashboard } from './components/Dashboard';
import { CVParser } from './components/CVParser';
import { ResumeScorer } from './components/ResumeScorer';
import { BiasAudit } from './components/BiasAudit';
import { Recommendations } from './components/Recommendations';
import { SkillTree } from './components/SkillTree';
import { ProjectGenerator } from './components/ProjectGenerator';
import { CourseRecommendations } from './components/CourseRecommendations';
import { KnowledgeGraph } from './components/KnowledgeGraph';
import { ResumePolisher } from './components/ResumePolisher';
import { CareerRoadmap } from './components/CareerRoadmap';
import { Menu, X } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [userData, setUserData] = useState<any>(null);

  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
    { id: 'cv-parser', label: 'Upload CV', icon: '📄' },
    { id: 'scorer', label: 'Resume Score', icon: '⭐' },
    { id: 'bias-audit', label: 'Bias Audit', icon: '⚖️' },
    { id: 'recommendations', label: 'Recommendations', icon: '💡' },
    { id: 'skill-tree', label: 'Skill Tree', icon: '🌳' },
    { id: 'projects', label: 'Projects', icon: '🚀' },
    { id: 'courses', label: 'Courses', icon: '📚' },
    { id: 'knowledge-graph', label: 'Knowledge Graph', icon: '🕸️' },
    { id: 'polish', label: 'Resume Polish', icon: '✨' },
    { id: 'roadmap', label: 'Career Roadmap', icon: '🗺️' },
  ];

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard userData={userData} setActiveTab={setActiveTab} />;
      case 'cv-parser':
        return <CVParser setUserData={setUserData} setActiveTab={setActiveTab} />;
      case 'scorer':
        return <ResumeScorer userData={userData} />;
      case 'bias-audit':
        return <BiasAudit userData={userData} />;
      case 'recommendations':
        return <Recommendations userData={userData} />;
      case 'skill-tree':
        return <SkillTree userData={userData} />;
      case 'projects':
        return <ProjectGenerator userData={userData} />;
      case 'courses':
        return <CourseRecommendations userData={userData} />;
      case 'knowledge-graph':
        return <KnowledgeGraph userData={userData} />;
      case 'polish':
        return <ResumePolisher userData={userData} />;
      case 'roadmap':
        return <CareerRoadmap userData={userData} />;
      default:
        return <Dashboard userData={userData} setActiveTab={setActiveTab} />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <span className="text-white">🎯</span>
              </div>
              <div>
                <h1 className="text-blue-600">CareerMatch</h1>
                <p className="text-gray-500 text-xs">AI-Driven Career Assistant</p>
              </div>
            </div>
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="lg:hidden p-2 rounded-lg hover:bg-gray-100"
            >
              {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col lg:flex-row gap-6">
          {/* Sidebar Navigation */}
          <aside
            className={`${
              mobileMenuOpen ? 'block' : 'hidden'
            } lg:block w-full lg:w-64 shrink-0`}
          >
            <nav className="bg-white rounded-xl shadow-sm border border-gray-200 p-2 sticky top-24">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => {
                    setActiveTab(tab.id);
                    setMobileMenuOpen(false);
                  }}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                    activeTab === tab.id
                      ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-md'
                      : 'text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  <span className="text-xl">{tab.icon}</span>
                  <span>{tab.label}</span>
                </button>
              ))}
            </nav>
          </aside>

          {/* Main Content */}
          <main className="flex-1 min-w-0">
            {renderContent()}
          </main>
        </div>
      </div>
    </div>
  );
}
