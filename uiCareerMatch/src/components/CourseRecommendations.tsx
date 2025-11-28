import { useState, useEffect } from 'react';
import { BookOpen, Star, Clock, TrendingUp, Loader } from 'lucide-react';
import { api } from '../utils/api';

interface CourseRecommendationsProps {
  userData: any;
}

export function CourseRecommendations({ userData }: CourseRecommendationsProps) {
  const [courses, setCourses] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [selectedLevel, setSelectedLevel] = useState('all');

  useEffect(() => {
    if (userData) {
      loadCourses();
    }
  }, [userData]);

  const loadCourses = async () => {
    setLoading(true);
    try {
      const skillGaps = ['TypeScript', 'GraphQL', 'Terraform', 'System Design', 'Leadership'];
      const result = await api.getCourseRecommendations(skillGaps);
      setCourses(result);
    } catch (error) {
      console.error('Failed to load courses:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!userData) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
        <BookOpen className="mx-auto mb-4 text-gray-400" size={64} />
        <h3 className="text-gray-900 mb-2">No CV Data Available</h3>
        <p className="text-gray-600">Please upload your CV first to get course recommendations</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
        <Loader className="animate-spin mx-auto mb-4 text-blue-600" size={48} />
        <p className="text-gray-600">Finding courses for you...</p>
      </div>
    );
  }

  if (!courses) return null;

  const filteredCourses = selectedLevel === 'all'
    ? courses.courses
    : courses.courses.filter((c: any) => c.level === selectedLevel);

  const getLevelColor = (level: string) => {
    if (level === 'Beginner') return 'bg-green-100 text-green-700 border-green-200';
    if (level === 'Intermediate') return 'bg-yellow-100 text-yellow-700 border-yellow-200';
    return 'bg-red-100 text-red-700 border-red-200';
  };

  const getProviderColor = (provider: string) => {
    if (provider === 'Coursera') return 'text-blue-600';
    if (provider === 'Udemy') return 'text-purple-600';
    return 'text-orange-600';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl shadow-lg p-8 text-white">
        <div className="flex items-center gap-3 mb-2">
          <BookOpen size={32} />
          <h2 className="text-white">Course Recommendations</h2>
        </div>
        <p className="text-white/80">Personalized learning paths to bridge your skill gaps</p>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-center gap-3 mb-4">
          <TrendingUp className="text-blue-600" size={20} />
          <h3 className="text-gray-900">Filter by Level</h3>
        </div>
        <div className="flex flex-wrap gap-3">
          {['all', 'Beginner', 'Intermediate', 'Advanced'].map((level) => (
            <button
              key={level}
              onClick={() => setSelectedLevel(level)}
              className={`px-4 py-2 rounded-lg border-2 transition-all ${
                selectedLevel === level
                  ? 'border-blue-500 bg-blue-50 text-blue-700'
                  : 'border-gray-300 bg-white text-gray-700 hover:border-blue-300'
              }`}
            >
              {level === 'all' ? 'All Levels' : level}
            </button>
          ))}
        </div>
      </div>

      {/* Courses Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {filteredCourses.map((course: any, idx: number) => (
          <div key={idx} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-lg transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <h4 className="text-gray-900 mb-2">{course.title}</h4>
                <div className={`text-sm ${getProviderColor(course.provider)}`}>
                  {course.provider}
                </div>
              </div>
              <div className="text-right">
                <div className="flex items-center gap-1 mb-1">
                  <Star className="text-yellow-500 fill-yellow-500" size={16} />
                  <span className="text-gray-900">{course.rating.toFixed(1)}</span>
                </div>
                <div className="text-xs text-gray-500">rating</div>
              </div>
            </div>

            <div className="flex flex-wrap gap-2 mb-4">
              <span className={`text-xs px-2 py-1 rounded-full border ${getLevelColor(course.level)}`}>
                {course.level}
              </span>
              <span className="text-xs px-2 py-1 rounded-full border border-gray-300 bg-gray-50 text-gray-700 flex items-center gap-1">
                <Clock size={12} />
                {course.duration}
              </span>
            </div>

            <div className="mb-4">
              <div className="text-xs text-gray-500 mb-2">Skills Covered</div>
              <div className="flex flex-wrap gap-1">
                {course.skills.map((skill: string, skillIdx: number) => (
                  <span key={skillIdx} className="text-xs bg-blue-50 text-blue-700 px-2 py-1 rounded">
                    {skill}
                  </span>
                ))}
              </div>
            </div>

            <div className="flex items-center justify-between pt-4 border-t border-gray-200">
              <div>
                <div className="text-xs text-gray-500">Match Score</div>
                <div className="text-gray-900">{course.matchScore}%</div>
              </div>
              <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                View Course
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Learning Path */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-gray-900 mb-4">Recommended Learning Path</h3>
        <div className="relative">
          {/* Path Line */}
          <div className="absolute left-6 top-8 bottom-8 w-0.5 bg-gradient-to-b from-blue-400 to-purple-400" />
          
          <div className="space-y-6">
            {filteredCourses.slice(0, 3).map((course: any, idx: number) => (
              <div key={idx} className="flex gap-4">
                <div className="relative z-10 w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white shrink-0">
                  {idx + 1}
                </div>
                <div className="flex-1 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-4 border border-blue-200">
                  <div className="text-gray-900 mb-1">{course.title}</div>
                  <div className="text-sm text-gray-600 mb-2">{course.provider} • {course.duration}</div>
                  <div className="text-xs text-gray-500">
                    {idx === 0 ? 'Start here to build foundations' : idx === 1 ? 'Build on core concepts' : 'Advanced mastery'}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Skill Gap Courses Info */}
      <div className="bg-gradient-to-r from-purple-50 to-indigo-50 rounded-xl border border-purple-200 p-6">
        <h3 className="text-gray-900 mb-3">📚 Skill Gap Course Recommendations</h3>
        <p className="text-gray-700 mb-4">
          Our AI analyzes your current skills against industry requirements and target roles to identify skill gaps. We then match you with the most relevant courses from top platforms, optimized for your learning style and career goals.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white rounded-lg p-4">
            <div className="text-purple-600 mb-2">🎯 Targeted</div>
            <p className="text-gray-600 text-sm">Courses matched to your specific skill gaps</p>
          </div>
          <div className="bg-white rounded-lg p-4">
            <div className="text-purple-600 mb-2">📊 Match Scored</div>
            <p className="text-gray-600 text-sm">AI calculates relevance to your goals</p>
          </div>
          <div className="bg-white rounded-lg p-4">
            <div className="text-purple-600 mb-2">🗺️ Path Optimized</div>
            <p className="text-gray-600 text-sm">Ordered learning sequence for best results</p>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="text-blue-600 mb-2">Total Courses</div>
          <div className="text-gray-900 text-3xl">{courses.courses.length}</div>
        </div>
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="text-green-600 mb-2">Avg. Match Score</div>
          <div className="text-gray-900 text-3xl">
            {Math.round(courses.courses.reduce((acc: number, c: any) => acc + c.matchScore, 0) / courses.courses.length)}%
          </div>
        </div>
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="text-purple-600 mb-2">Total Learning Hours</div>
          <div className="text-gray-900 text-3xl">
            {courses.courses.reduce((acc: number, c: any) => acc + parseInt(c.duration), 0)}h
          </div>
        </div>
      </div>
    </div>
  );
}
