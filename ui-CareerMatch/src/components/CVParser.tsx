import { useState } from 'react';
import { Upload, FileText, Loader, CheckCircle, XCircle } from 'lucide-react';
import { api } from '../utils/api';

interface CVParserProps {
  setUserData: (data: any) => void;
  setActiveTab: (tab: string) => void;
}

export function CVParser({ setUserData, setActiveTab }: CVParserProps) {
  const [file, setFile] = useState<File | null>(null);
  const [parsing, setParsing] = useState(false);
  const [parsedData, setParsedData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      setError(null);
      setParsedData(null);
    }
  };

  const handleParse = async () => {
    if (!file) return;

    setParsing(true);
    setError(null);

    try {
      const result = await api.parseCV(file);
      if (result.success) {
        setParsedData(result.data);
        setUserData(result.data);
      } else {
        setError('Failed to parse CV. Please try again.');
      }
    } catch (err) {
      setError('An error occurred while parsing your CV.');
    } finally {
      setParsing(false);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && (droppedFile.type === 'application/pdf' || droppedFile.type === 'application/msword' || droppedFile.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')) {
      setFile(droppedFile);
      setError(null);
      setParsedData(null);
    } else {
      setError('Please upload a PDF or Word document');
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-center gap-3 mb-6">
          <FileText className="text-blue-600" size={28} />
          <div>
            <h2 className="text-gray-900">CV Parser & Section Detection</h2>
            <p className="text-gray-600 text-sm">Upload your resume for AI-powered parsing and analysis</p>
          </div>
        </div>

        {/* Upload Area */}
        <div
          onDragOver={handleDragOver}
          onDrop={handleDrop}
          className={`border-2 border-dashed rounded-xl p-12 text-center transition-colors ${
            file ? 'border-blue-400 bg-blue-50' : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
          }`}
        >
          <Upload className="mx-auto mb-4 text-gray-400" size={48} />
          <h3 className="text-gray-900 mb-2">
            {file ? 'File Selected' : 'Drop your CV here or click to browse'}
          </h3>
          <p className="text-gray-600 text-sm mb-4">
            Supports PDF, DOC, DOCX files
          </p>
          <input
            type="file"
            id="cv-upload"
            accept=".pdf,.doc,.docx"
            onChange={handleFileChange}
            className="hidden"
          />
          <label
            htmlFor="cv-upload"
            className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg cursor-pointer hover:bg-blue-700 transition-colors"
          >
            Choose File
          </label>
          {file && (
            <div className="mt-4 text-gray-700">
              <CheckCircle className="inline mr-2 text-green-600" size={20} />
              {file.name}
            </div>
          )}
        </div>

        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center gap-2 text-red-700">
            <XCircle size={20} />
            {error}
          </div>
        )}

        {file && !parsedData && (
          <button
            onClick={handleParse}
            disabled={parsing}
            className="mt-6 w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {parsing ? (
              <>
                <Loader className="animate-spin" size={20} />
                Parsing CV...
              </>
            ) : (
              'Parse CV'
            )}
          </button>
        )}
      </div>

      {/* Parsed Results */}
      {parsedData && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 space-y-6">
          <div className="flex items-center justify-between">
            <h3 className="text-gray-900">Parsed Results</h3>
            <button
              onClick={() => setActiveTab('scorer')}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              View Score →
            </button>
          </div>

          {/* Personal Info */}
          <div>
            <h4 className="text-gray-700 mb-3">Personal Information</h4>
            <div className="bg-gray-50 rounded-lg p-4 grid grid-cols-1 md:grid-cols-2 gap-3">
              <div>
                <span className="text-gray-500 text-sm">Name:</span>
                <div className="text-gray-900">{parsedData.personalInfo.name}</div>
              </div>
              <div>
                <span className="text-gray-500 text-sm">Email:</span>
                <div className="text-gray-900">{parsedData.personalInfo.email}</div>
              </div>
              <div>
                <span className="text-gray-500 text-sm">Phone:</span>
                <div className="text-gray-900">{parsedData.personalInfo.phone}</div>
              </div>
              <div>
                <span className="text-gray-500 text-sm">Location:</span>
                <div className="text-gray-900">{parsedData.personalInfo.location}</div>
              </div>
            </div>
          </div>

          {/* Summary */}
          <div>
            <h4 className="text-gray-700 mb-3">Summary</h4>
            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-gray-900">{parsedData.summary}</p>
            </div>
          </div>

          {/* Experience */}
          <div>
            <h4 className="text-gray-700 mb-3">Experience</h4>
            <div className="space-y-3">
              {parsedData.experience.map((exp: any, idx: number) => (
                <div key={idx} className="bg-gray-50 rounded-lg p-4">
                  <div className="text-gray-900 mb-1">{exp.title}</div>
                  <div className="text-gray-600 text-sm mb-2">{exp.company} • {exp.duration}</div>
                  <p className="text-gray-700 text-sm">{exp.description}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Education */}
          <div>
            <h4 className="text-gray-700 mb-3">Education</h4>
            <div className="space-y-3">
              {parsedData.education.map((edu: any, idx: number) => (
                <div key={idx} className="bg-gray-50 rounded-lg p-4">
                  <div className="text-gray-900">{edu.degree}</div>
                  <div className="text-gray-600 text-sm">{edu.institution} • {edu.year}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Skills */}
          <div>
            <h4 className="text-gray-700 mb-3">Skills</h4>
            <div className="flex flex-wrap gap-2">
              {parsedData.skills.map((skill: string, idx: number) => (
                <span key={idx} className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm">
                  {skill}
                </span>
              ))}
            </div>
          </div>

          {/* Certifications */}
          {parsedData.certifications && parsedData.certifications.length > 0 && (
            <div>
              <h4 className="text-gray-700 mb-3">Certifications</h4>
              <div className="space-y-2">
                {parsedData.certifications.map((cert: string, idx: number) => (
                  <div key={idx} className="bg-green-50 rounded-lg p-3 text-green-800 flex items-center gap-2">
                    <CheckCircle size={16} />
                    {cert}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
