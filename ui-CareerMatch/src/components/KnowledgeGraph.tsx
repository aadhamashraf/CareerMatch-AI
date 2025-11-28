import { useState, useEffect } from 'react';
import { Network, Loader, Info } from 'lucide-react';
import { api } from '../utils/api';

interface KnowledgeGraphProps {
  userData: any;
}

export function KnowledgeGraph({ userData }: KnowledgeGraphProps) {
  const [graphData, setGraphData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [selectedNode, setSelectedNode] = useState<any>(null);

  useEffect(() => {
    if (userData) {
      loadGraph();
    }
  }, [userData]);

  const loadGraph = async () => {
    setLoading(true);
    try {
      const result = await api.getKnowledgeGraph('user-123');
      setGraphData(result);
    } catch (error) {
      console.error('Failed to load knowledge graph:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!userData) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
        <Network className="mx-auto mb-4 text-gray-400" size={64} />
        <h3 className="text-gray-900 mb-2">No CV Data Available</h3>
        <p className="text-gray-600">Please upload your CV first to view your knowledge graph</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
        <Loader className="animate-spin mx-auto mb-4 text-blue-600" size={48} />
        <p className="text-gray-600">Building your knowledge graph...</p>
      </div>
    );
  }

  if (!graphData) return null;

  const getNodeColor = (type: string) => {
    if (type === 'skill') return 'from-blue-500 to-blue-600';
    if (type === 'role') return 'from-green-500 to-green-600';
    return 'from-purple-500 to-purple-600';
  };

  const getNodeIcon = (type: string) => {
    if (type === 'skill') return '⚡';
    if (type === 'role') return '💼';
    return '📚';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-cyan-600 to-blue-600 rounded-xl shadow-lg p-8 text-white">
        <div className="flex items-center gap-3 mb-2">
          <Network size={32} />
          <h2 className="text-white">Knowledge Graph</h2>
        </div>
        <p className="text-white/80">Visual map of your skills, roles, and career connections</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Graph Visualization */}
        <div className="lg:col-span-2 bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-gray-900">Interactive Graph</h3>
            <div className="flex gap-2">
              <span className="text-xs px-2 py-1 rounded bg-blue-100 text-blue-700">⚡ Skills</span>
              <span className="text-xs px-2 py-1 rounded bg-green-100 text-green-700">💼 Roles</span>
            </div>
          </div>
          
          {/* Simplified Graph Visualization */}
          <div className="relative bg-gradient-to-br from-gray-50 to-blue-50 rounded-lg p-8 h-96 overflow-hidden">
            {/* Current Role - Center */}
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
              <button
                onClick={() => setSelectedNode(graphData.nodes.find((n: any) => n.current))}
                className="w-24 h-24 bg-gradient-to-br from-green-500 to-green-600 rounded-full shadow-lg flex flex-col items-center justify-center text-white hover:scale-110 transition-transform"
              >
                <span className="text-2xl">💼</span>
                <span className="text-xs mt-1">Current</span>
              </button>
            </div>

            {/* Skills - Left Side */}
            <div className="absolute top-1/2 left-12 transform -translate-y-1/2 space-y-4">
              {graphData.nodes.filter((n: any) => n.type === 'skill' && n.level > 70).map((node: any, idx: number) => (
                <button
                  key={node.id}
                  onClick={() => setSelectedNode(node)}
                  className="w-20 h-20 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full shadow-md flex flex-col items-center justify-center text-white text-xs hover:scale-110 transition-transform"
                  style={{ transform: `translateY(${(idx - 1) * 40}px)` }}
                >
                  <span className="text-lg">⚡</span>
                  <span className="mt-1 text-center px-1">{node.label}</span>
                </button>
              ))}
            </div>

            {/* Target Role - Right Side */}
            <div className="absolute top-1/2 right-12 transform -translate-y-1/2">
              <button
                onClick={() => setSelectedNode(graphData.nodes.find((n: any) => n.target))}
                className="w-24 h-24 bg-gradient-to-br from-purple-500 to-purple-600 rounded-full shadow-lg flex flex-col items-center justify-center text-white hover:scale-110 transition-transform"
              >
                <span className="text-2xl">🎯</span>
                <span className="text-xs mt-1">Target</span>
              </button>
            </div>

            {/* Skill Gaps - Top Right */}
            <div className="absolute top-12 right-1/4 space-y-3">
              {graphData.nodes.filter((n: any) => n.type === 'skill' && n.level < 70).map((node: any, idx: number) => (
                <button
                  key={node.id}
                  onClick={() => setSelectedNode(node)}
                  className="w-16 h-16 bg-gradient-to-br from-orange-400 to-orange-500 rounded-full shadow-md flex flex-col items-center justify-center text-white text-xs hover:scale-110 transition-transform opacity-70"
                >
                  <span>⚡</span>
                  <span className="text-xs">{node.label}</span>
                </button>
              ))}
            </div>

            {/* Connection Lines */}
            <svg className="absolute inset-0 w-full h-full pointer-events-none">
              <defs>
                <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                  <polygon points="0 0, 10 3.5, 0 7" fill="#94a3b8" />
                </marker>
              </defs>
              <line x1="50%" y1="50%" x2="20%" y2="30%" stroke="#94a3b8" strokeWidth="2" strokeDasharray="5,5" markerEnd="url(#arrowhead)" />
              <line x1="50%" y1="50%" x2="20%" y2="50%" stroke="#94a3b8" strokeWidth="2" strokeDasharray="5,5" markerEnd="url(#arrowhead)" />
              <line x1="50%" y1="50%" x2="20%" y2="70%" stroke="#94a3b8" strokeWidth="2" strokeDasharray="5,5" markerEnd="url(#arrowhead)" />
              <line x1="50%" y1="50%" x2="80%" y2="50%" stroke="#94a3b8" strokeWidth="3" markerEnd="url(#arrowhead)" />
              <line x1="75%" y1="25%" x2="80%" y2="50%" stroke="#fbbf24" strokeWidth="2" strokeDasharray="5,5" markerEnd="url(#arrowhead)" />
            </svg>
          </div>

          <div className="mt-4 p-4 bg-blue-50 rounded-lg border border-blue-200">
            <p className="text-blue-900 text-sm">
              <Info className="inline mr-2" size={16} />
              Click on any node to see details. Lines show relationships between skills and roles.
            </p>
          </div>
        </div>

        {/* Node Details */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-gray-900 mb-4">Node Details</h3>
          {selectedNode ? (
            <div className="space-y-4">
              <div className={`w-20 h-20 bg-gradient-to-br ${getNodeColor(selectedNode.type)} rounded-full shadow-lg flex items-center justify-center text-3xl mx-auto`}>
                {getNodeIcon(selectedNode.type)}
              </div>
              <div className="text-center">
                <h4 className="text-gray-900 mb-1">{selectedNode.label}</h4>
                <span className="text-xs px-2 py-1 rounded-full bg-gray-100 text-gray-700 capitalize">
                  {selectedNode.type}
                </span>
              </div>
              {selectedNode.level && (
                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-gray-600">Proficiency</span>
                    <span className="text-gray-900">{selectedNode.level}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div
                      className="bg-gradient-to-r from-blue-500 to-purple-500 h-3 rounded-full transition-all"
                      style={{ width: `${selectedNode.level}%` }}
                    />
                  </div>
                </div>
              )}
              {selectedNode.current && (
                <div className="p-3 bg-green-50 rounded-lg border border-green-200 text-green-700 text-sm text-center">
                  ✓ Your Current Role
                </div>
              )}
              {selectedNode.target && (
                <div className="p-3 bg-purple-50 rounded-lg border border-purple-200 text-purple-700 text-sm text-center">
                  🎯 Target Career Goal
                </div>
              )}
            </div>
          ) : (
            <div className="text-center text-gray-500 py-8">
              Click on a node to view details
            </div>
          )}
        </div>
      </div>

      {/* Relationships */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-gray-900 mb-4">Skill & Role Relationships</h3>
        <div className="space-y-3">
          {graphData.edges.map((edge: any, idx: number) => {
            const fromNode = graphData.nodes.find((n: any) => n.id === edge.from);
            const toNode = graphData.nodes.find((n: any) => n.id === edge.to);
            return (
              <div key={idx} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                <span className="text-blue-600">{fromNode?.label}</span>
                <span className="text-gray-400">→</span>
                <span className="text-xs px-2 py-1 rounded bg-purple-100 text-purple-700">
                  {edge.relationship}
                </span>
                <span className="text-gray-400">→</span>
                <span className="text-green-600">{toNode?.label}</span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Knowledge Graph Info */}
      <div className="bg-gradient-to-r from-cyan-50 to-blue-50 rounded-xl border border-cyan-200 p-6">
        <h3 className="text-gray-900 mb-3">🕸️ Dynamic Knowledge Graph</h3>
        <p className="text-gray-700 mb-4">
          Our knowledge graph connects your skills, target roles, and learning resources in a contextual network. It identifies prerequisite skills, related competencies, and optimal learning paths to reach your career goals.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white rounded-lg p-4">
            <div className="text-cyan-600 mb-2">🔗 Connected</div>
            <p className="text-gray-600 text-sm">Skills linked to roles and resources</p>
          </div>
          <div className="bg-white rounded-lg p-4">
            <div className="text-cyan-600 mb-2">🎯 Context-Aware</div>
            <p className="text-gray-600 text-sm">Recommendations based on relationships</p>
          </div>
          <div className="bg-white rounded-lg p-4">
            <div className="text-cyan-600 mb-2">📊 Visual Insights</div>
            <p className="text-gray-600 text-sm">Clear career progression pathways</p>
          </div>
        </div>
      </div>
    </div>
  );
}
