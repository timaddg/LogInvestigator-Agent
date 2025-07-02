'use client';

import { useState } from 'react';
import FileUpload from '@/components/FileUpload';
import LogSources from '@/components/LogSources';
import AnalysisResults from '@/components/AnalysisResults';
import { AnalysisData } from '@/types';

export default function Home() {
  const [analysisData, setAnalysisData] = useState<AnalysisData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalysisComplete = (data: AnalysisData) => {
    setAnalysisData(data);
    setError(null);
  };

  const handleError = (errorMessage: string) => {
    setError(errorMessage);
    setAnalysisData(null);
  };

  const handleLoading = (loading: boolean) => {
    setIsLoading(loading);
  };

  return (
    <div className="min-h-screen bg-black">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-white mb-4">
            Log Investigator
          </h1>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            AI-powered log analysis for cybersecurity and system administration. 
            Upload your log files or download from online sources for instant insights.
          </p>
        </div>

        {/* Main Content */}
        <div className="grid lg:grid-cols-2 gap-8 mb-8">
          {/* File Upload Section */}
          <div className="bg-gray-900 rounded-2xl p-8 border border-gray-700">
            <h2 className="text-2xl font-semibold text-white mb-6">
              Upload Log File
            </h2>
            <FileUpload 
              onAnalysisComplete={handleAnalysisComplete}
              onError={handleError}
              onLoading={handleLoading}
            />
          </div>

          {/* Log Sources Section */}
          <div className="bg-gray-900 rounded-2xl p-8 border border-gray-700">
            <h2 className="text-2xl font-semibold text-white mb-6">
              Download Sample Logs
            </h2>
            <LogSources 
              onAnalysisComplete={handleAnalysisComplete}
              onError={handleError}
              onLoading={handleLoading}
            />
          </div>
        </div>

        {/* Loading State */}
        {isLoading && (
          <div className="bg-gray-900 rounded-2xl p-8 border border-gray-700 mb-8">
            <div className="flex items-center justify-center space-x-4">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white"></div>
              <p className="text-white text-lg">Analyzing logs with AI...</p>
            </div>
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className="bg-red-900/50 rounded-2xl p-8 border border-red-700 mb-8">
            <div className="flex items-center space-x-3">
              <div className="flex-shrink-0">
                <svg className="h-6 w-6 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <h3 className="text-lg font-medium text-red-200">Error</h3>
                <p className="text-red-100">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Analysis Results */}
        {analysisData && (
          <AnalysisResults data={analysisData} />
        )}
      </div>
    </div>
  );
}
