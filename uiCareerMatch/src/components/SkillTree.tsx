import { useState, useEffect } from 'react';
import { TreePine, Award, Lock, Check, Loader, Star } from 'lucide-react';
import { api } from '../utils/api';

interface SkillTreeProps {
  userData: any;
}

export function SkillTree({ userData }: SkillTreeProps) {
  const [skillTree, setSkillTree] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (userData) {
      loadSkillTree();
    }
  }, [userData]);

  const loadSkillTree = async () => {
    setLoading(true);
    try {
      const result = await api.getSkillTree('user-123');
      setSkillTree(result);
    } catch (error) {
      console.error('Failed to load skill tree:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!userData) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
        <TreePine className="mx-auto mb-4 text-gray-400" size={64} />
        <h3 className="text-gray-900 mb-2">No CV Data Available</h3>
        <p className="text-gray-600">Please upload your CV first to view your skill tree</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
        <Loader className="animate-spin mx-auto mb-4 text-blue-600" size={48} />
        <p className="text-gray-600">Loading your skill tree...</p>
      </div>
    );
  }

  if (!skillTree) return null;

  const progressPercentage = (skillTree.totalPoints / skillTree.nextLevelPoints) * 100;

  return (
    <div className="space-y-6">
      {/* Header with Progress */}
      <div className="bg-gradient-to-r from-green-600 to-emerald-600 rounded-xl shadow-lg p-8 text-white">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-white mb-2">Skill Tree Progress</h2>
            <p className="text-white/80">Level {skillTree.level} Developer</p>
          </div>
          <div className="text-right">
            <div className="flex items-center gap-2 justify-end mb-2">
              <Star className="text-yellow-300 fill-yellow-300" size={24} />
              <span className="text-3xl text-white">{skillTree.totalPoints}</span>
            </div>
            <div className="text-white/80 text-sm">Total Points</div>
          </div>
        </div>
        <div className="space-y-2">
          <div className="flex justify-between text-sm text-white/80">
            <span>Progress to Level {skillTree.level + 1}</span>
            <span>{skillTree.totalPoints} / {skillTree.nextLevelPoints}</span>
          </div>
          <div className="w-full bg-white/20 rounded-full h-4">
            <div
              className="bg-white h-4 rounded-full transition-all duration-500 flex items-center justify-end pr-2"
              style={{ width: `${progressPercentage}%` }}
            >
              <span className="text-green-600 text-xs">{Math.round(progressPercentage)}%</span>
            </div>
          </div>
        </div>
      </div>

      {/* Skill Categories */}
      {skillTree.categories.map((category: any, catIdx: number) => (
        <div key={catIdx} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-500 rounded-lg flex items-center justify-center text-white">
              {catIdx === 0 ? '🎨' : catIdx === 1 ? '⚙️' : '☁️'}
            </div>
            <h3 className="text-gray-900">{category.name}</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {category.skills.map((skill: any, skillIdx: number) => {
              const isMaxLevel = skill.level === skill.maxLevel;
              const isUnlocked = skill.unlocked;
              
              return (
                <div
                  key={skillIdx}
                  className={`border-2 rounded-lg p-5 transition-all ${
                    !isUnlocked
                      ? 'border-gray-300 bg-gray-50 opacity-60'
                      : isMaxLevel
                      ? 'border-green-400 bg-green-50'
                      : 'border-blue-300 bg-blue-50 hover:shadow-md'
                  }`}
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-2">
                      {!isUnlocked ? (
                        <Lock size={20} className="text-gray-400" />
                      ) : isMaxLevel ? (
                        <Check size={20} className="text-green-600" />
                      ) : (
                        <Award size={20} className="text-blue-600" />
                      )}
                      <h4 className="text-gray-900">{skill.name}</h4>
                    </div>
                  </div>

                  {/* Level Dots */}
                  <div className="flex gap-1 mb-3">
                    {Array.from({ length: skill.maxLevel }).map((_, idx) => (
                      <div
                        key={idx}
                        className={`w-full h-2 rounded-full ${
                          idx < skill.level
                            ? isMaxLevel
                              ? 'bg-green-500'
                              : 'bg-blue-500'
                            : 'bg-gray-300'
                        }`}
                      />
                    ))}
                  </div>

                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-600">
                      Level {skill.level}/{skill.maxLevel}
                    </span>
                    <span className="text-gray-600 flex items-center gap-1">
                      <Star size={14} className="text-yellow-500" />
                      {skill.points}
                    </span>
                  </div>

                  {!isUnlocked && (
                    <div className="mt-3 text-xs text-gray-500 text-center">
                      🔒 Complete prerequisites to unlock
                    </div>
                  )}
                  {isMaxLevel && (
                    <div className="mt-3 text-xs text-green-600 text-center">
                      ✓ Mastered
                    </div>
                  )}
                  {isUnlocked && !isMaxLevel && (
                    <button className="mt-3 w-full bg-blue-600 text-white text-sm py-2 rounded hover:bg-blue-700 transition-colors">
                      Level Up
                    </button>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      ))}

      {/* Gamification Info */}
      <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl border border-purple-200 p-6">
        <h3 className="text-gray-900 mb-3">🎮 Gamified Learning System</h3>
        <p className="text-gray-700 mb-4">
          Your skill tree visualizes your career development journey. Earn points by completing projects, courses, and challenges. Unlock new skills as you progress and master your craft!
        </p>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-white rounded-lg p-4">
            <div className="text-2xl mb-2">⭐</div>
            <div className="text-gray-900 mb-1">Earn Points</div>
            <p className="text-gray-600 text-sm">Complete activities to gain XP</p>
          </div>
          <div className="bg-white rounded-lg p-4">
            <div className="text-2xl mb-2">🔓</div>
            <div className="text-gray-900 mb-1">Unlock Skills</div>
            <p className="text-gray-600 text-sm">Progress through prerequisites</p>
          </div>
          <div className="bg-white rounded-lg p-4">
            <div className="text-2xl mb-2">📈</div>
            <div className="text-gray-900 mb-1">Level Up</div>
            <p className="text-gray-600 text-sm">Advance your expertise</p>
          </div>
          <div className="bg-white rounded-lg p-4">
            <div className="text-2xl mb-2">🏆</div>
            <div className="text-gray-900 mb-1">Master Skills</div>
            <p className="text-gray-600 text-sm">Achieve maximum proficiency</p>
          </div>
        </div>
      </div>

      {/* Achievements */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-gray-900 mb-4">🏅 Recent Achievements</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="flex items-center gap-4 p-4 bg-gradient-to-r from-yellow-50 to-orange-50 rounded-lg border border-yellow-200">
            <div className="w-12 h-12 bg-yellow-400 rounded-full flex items-center justify-center text-2xl">
              🌟
            </div>
            <div>
              <div className="text-gray-900">Frontend Master</div>
              <p className="text-gray-600 text-sm">Maxed out all frontend skills</p>
            </div>
          </div>
          <div className="flex items-center gap-4 p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border border-blue-200">
            <div className="w-12 h-12 bg-blue-400 rounded-full flex items-center justify-center text-2xl">
              💎
            </div>
            <div>
              <div className="text-gray-900">Level 12 Reached</div>
              <p className="text-gray-600 text-sm">Accumulated 2,450 skill points</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
