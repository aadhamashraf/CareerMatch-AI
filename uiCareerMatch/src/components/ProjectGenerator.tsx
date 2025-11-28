import { useState } from 'react';
import { Rocket, Code, Loader, ChevronDown, ChevronRight } from 'lucide-react';
import { api } from '../utils/api';

interface ProjectGeneratorProps {
  userData: any;
}

export function ProjectGenerator({ userData }: ProjectGeneratorProps) {
  const [selectedSkills, setSelectedSkills] = useState<string[]>([]);
  const [difficulty, setDifficulty] = useState('intermediate');
  const [generating, setGenerating] = useState(false);
  const [project, setProject] = useState<any>(null);
  const [expandedFolders, setExpandedFolders] = useState<Set<string>>(new Set());

  const availableSkills = userData?.skills || ['JavaScript', 'React', 'Node.js', 'Python', 'AWS'];

  const handleSkillToggle = (skill: string) => {
    setSelectedSkills(prev =>
      prev.includes(skill) ? prev.filter(s => s !== skill) : [...prev, skill]
    );
  };

  const handleGenerate = async () => {
    if (selectedSkills.length === 0) return;

    setGenerating(true);
    try {
      const result = await api.generateProject(selectedSkills, difficulty);
      setProject(result);
      setExpandedFolders(new Set(['root']));
    } catch (error) {
      console.error('Failed to generate project:', error);
    } finally {
      setGenerating(false);
    }
  };

  const toggleFolder = (path: string) => {
    setExpandedFolders(prev => {
      const newSet = new Set(prev);
      if (newSet.has(path)) {
        newSet.delete(path);
      } else {
        newSet.add(path);
      }
      return newSet;
    });
  };

  const renderFileTree = (structure: any, path = '') => {
    return Object.entries(structure).map(([key, value]) => {
      const currentPath = path ? `${path}/${key}` : key;
      const isFolder = typeof value === 'object' && !key.includes('.');
      const isExpanded = expandedFolders.has(currentPath);

      return (
        <div key={currentPath} className="ml-4">
          <div
            className={`flex items-center gap-2 py-1 px-2 rounded cursor-pointer hover:bg-gray-100 ${
              isFolder ? 'text-blue-600' : 'text-gray-700'
            }`}
            onClick={() => isFolder && toggleFolder(currentPath)}
          >
            {isFolder ? (
              <>
                {isExpanded ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
                📁 {key}
              </>
            ) : (
              <>
                <span className="w-4" />
                📄 {key}
              </>
            )}
          </div>
          {isFolder && isExpanded && (
            <div className="border-l-2 border-gray-200 ml-2">
              {renderFileTree(value, currentPath)}
            </div>
          )}
        </div>
      );
    });
  };

  if (!userData) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
        <Rocket className="mx-auto mb-4 text-gray-400" size={64} />
        <h3 className="text-gray-900 mb-2">No CV Data Available</h3>
        <p className="text-gray-600">Please upload your CV first to generate personalized projects</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-orange-600 to-red-600 rounded-xl shadow-lg p-8 text-white">
        <div className="flex items-center gap-3 mb-2">
          <Rocket size={32} />
          <h2 className="text-white">Project Generator</h2>
        </div>
        <p className="text-white/80">Auto-generate hands-on project skeletons tailored to your skills</p>
      </div>

      {/* Configuration */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-gray-900 mb-4">Configure Your Project</h3>
        
        {/* Skills Selection */}
        <div className="mb-6">
          <label className="text-gray-700 mb-3 block">Select Skills to Practice</label>
          <div className="flex flex-wrap gap-2">
            {availableSkills.map((skill: string) => (
              <button
                key={skill}
                onClick={() => handleSkillToggle(skill)}
                className={`px-4 py-2 rounded-lg border-2 transition-all ${
                  selectedSkills.includes(skill)
                    ? 'border-blue-500 bg-blue-50 text-blue-700'
                    : 'border-gray-300 bg-white text-gray-700 hover:border-blue-300'
                }`}
              >
                {selectedSkills.includes(skill) && '✓ '}
                {skill}
              </button>
            ))}
          </div>
        </div>

        {/* Difficulty Selection */}
        <div className="mb-6">
          <label className="text-gray-700 mb-3 block">Difficulty Level</label>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {['beginner', 'intermediate', 'advanced'].map((level) => (
              <button
                key={level}
                onClick={() => setDifficulty(level)}
                className={`p-4 rounded-lg border-2 transition-all ${
                  difficulty === level
                    ? level === 'beginner'
                      ? 'border-green-500 bg-green-50'
                      : level === 'intermediate'
                      ? 'border-yellow-500 bg-yellow-50'
                      : 'border-red-500 bg-red-50'
                    : 'border-gray-300 bg-white hover:border-gray-400'
                }`}
              >
                <div className="text-center">
                  <div className="text-2xl mb-2">
                    {level === 'beginner' ? '🌱' : level === 'intermediate' ? '🌿' : '🌳'}
                  </div>
                  <div className="text-gray-900 capitalize">{level}</div>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Generate Button */}
        <button
          onClick={handleGenerate}
          disabled={selectedSkills.length === 0 || generating}
          className="w-full bg-gradient-to-r from-orange-600 to-red-600 text-white py-3 rounded-lg hover:from-orange-700 hover:to-red-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          {generating ? (
            <>
              <Loader className="animate-spin" size={20} />
              Generating Project...
            </>
          ) : (
            <>
              <Code size={20} />
              Generate Project Skeleton
            </>
          )}
        </button>
      </div>

      {/* Generated Project */}
      {project && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 space-y-6">
          <div>
            <h3 className="text-gray-900 mb-2">{project.title}</h3>
            <p className="text-gray-600">{project.description}</p>
          </div>

          {/* Project Structure */}
          <div>
            <h4 className="text-gray-700 mb-3">Project Structure</h4>
            <div className="bg-gray-900 rounded-lg p-4 text-green-400 font-mono text-sm overflow-x-auto">
              <div className="flex items-center gap-2 mb-2">
                <ChevronDown size={16} />
                📦 {project.title.toLowerCase().replace(/\s+/g, '-')}
              </div>
              {renderFileTree(project.structure)}
            </div>
          </div>

          {/* Tasks */}
          <div>
            <h4 className="text-gray-700 mb-3">Implementation Tasks</h4>
            <div className="space-y-2">
              {project.tasks.map((task: string, idx: number) => (
                <div key={idx} className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                  <div className="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm shrink-0">
                    {idx + 1}
                  </div>
                  <p className="text-gray-700">{task}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Resources */}
          <div>
            <h4 className="text-gray-700 mb-3">Learning Resources</h4>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              {project.resources.map((resource: string, idx: number) => (
                <div key={idx} className="p-3 bg-blue-50 rounded-lg border border-blue-200 text-blue-700">
                  📚 {resource}
                </div>
              ))}
            </div>
          </div>

          {/* Actions */}
          <div className="flex gap-3">
            <button className="flex-1 bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition-colors">
              Download Skeleton
            </button>
            <button className="flex-1 border-2 border-blue-600 text-blue-600 py-3 rounded-lg hover:bg-blue-50 transition-colors">
              Save to My Projects
            </button>
          </div>
        </div>
      )}

      {/* Info */}
      <div className="bg-gradient-to-r from-orange-50 to-red-50 rounded-xl border border-orange-200 p-6">
        <h3 className="text-gray-900 mb-3">🚀 Auto-Generated Project Skeletons</h3>
        <p className="text-gray-700 mb-4">
          Our AI generates complete project structures with boilerplate code, configuration files, and implementation guides. Each project is customized based on your selected skills and difficulty level, giving you hands-on experience with real-world scenarios.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white rounded-lg p-4">
            <div className="text-orange-600 mb-2">📁 Complete Structure</div>
            <p className="text-gray-600 text-sm">Full directory layout and file organization</p>
          </div>
          <div className="bg-white rounded-lg p-4">
            <div className="text-orange-600 mb-2">✅ Task Breakdown</div>
            <p className="text-gray-600 text-sm">Step-by-step implementation guide</p>
          </div>
          <div className="bg-white rounded-lg p-4">
            <div className="text-orange-600 mb-2">📚 Resources</div>
            <p className="text-gray-600 text-sm">Curated learning materials</p>
          </div>
        </div>
      </div>
    </div>
  );
}
