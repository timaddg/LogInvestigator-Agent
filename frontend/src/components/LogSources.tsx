'use client';

import { useState, useEffect } from 'react';
import { LogSource, AnalysisData } from '@/types';

interface LogSourcesProps {
  onAnalysisComplete: (data: AnalysisData) => void;
  onError: (error: string) => void;
  onLoading: (loading: boolean) => void;
}

export default function LogSources({ onAnalysisComplete, onError, onLoading }: LogSourcesProps) {
  const [sources, setSources] = useState<LogSource[]>([]);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState<string | null>(null);

  useEffect(() => {
    fetchSources();
  }, []);

  const fetchSources = async () => {
    try {
      const response = await fetch('/api/sources');
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || 'Failed to fetch sources');
      }
      
      setSources(data.sources);
    } catch (error) {
      onError(error instanceof Error ? error.message : 'Failed to fetch sources');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async (sourceName: string) => {
    setDownloading(sourceName);
    onLoading(true);

    try {
      const response = await fetch(`/api/download/${sourceName}`, {
        method: 'POST',
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Download failed');
      }

      onAnalysisComplete(data);
    } catch (error) {
      onError(error instanceof Error ? error.message : 'Download failed');
    } finally {
      setDownloading(null);
      onLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-400"></div>
        <span className="ml-3 text-gray-300">Loading sources...</span>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <p className="text-gray-300 text-sm">
        Download and analyze sample logs from various sources:
      </p>
      
      <div className="space-y-3 max-h-96 overflow-y-auto">
        {sources.map((source) => (
          <div
            key={source.name}
            className="bg-white/5 border border-white/10 rounded-lg p-4 hover:bg-white/10 transition-colors"
          >
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <h3 className="font-medium text-white">{source.name}</h3>
                <p className="text-sm text-gray-400 mt-1">{source.description}</p>
                <div className="flex items-center mt-2 space-x-2">
                  <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-purple-500/20 text-purple-300">
                    {source.category}
                  </span>
                  <span className="text-xs text-gray-500">
                    {source.url}
                  </span>
                </div>
              </div>
              
              <button
                onClick={() => handleDownload(source.name)}
                disabled={downloading === source.name}
                className={`
                  ml-4 px-4 py-2 rounded-lg font-medium text-sm transition-colors
                  ${downloading === source.name
                    ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                    : 'bg-purple-600 hover:bg-purple-700 text-white'
                  }
                `}
              >
                {downloading === source.name ? (
                  <div className="flex items-center space-x-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    <span>Downloading...</span>
                  </div>
                ) : (
                  'Download & Analyze'
                )}
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-green-500/10 border border-green-500/20 rounded-lg p-4">
        <div className="flex items-start space-x-3">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div className="text-sm text-green-200">
            <p className="font-medium">Free sample logs</p>
            <p className="mt-1">Download and analyze logs from web servers, big data systems, and infrastructure monitoring.</p>
          </div>
        </div>
      </div>
    </div>
  );
} 