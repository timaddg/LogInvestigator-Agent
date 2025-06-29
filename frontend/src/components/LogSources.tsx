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
  const [selectedCategory, setSelectedCategory] = useState<string>('');

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
      
      // Set the first category as default if available
      const categories = Array.from(new Set(data.sources.map((s: LogSource) => s.category)));
      if (categories.length > 0) {
        setSelectedCategory(categories[0] as string);
      }
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

  // Get unique categories (excluding 'all')
  const categories = Array.from(new Set(sources.map(s => s.category)));
  
  // Filter sources by selected category
  const filteredSources = selectedCategory 
    ? sources.filter(source => source.category === selectedCategory)
    : [];

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-purple-400 mx-auto mb-4"></div>
          <p className="text-gray-300 text-lg">Loading log sources...</p>
          <p className="text-gray-500 text-sm mt-2">Fetching available sample logs</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header Section */}
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-white mb-2">Sample Log Sources</h2>
        <p className="text-gray-400 max-w-md mx-auto">
          Download and analyze real-world logs from various systems and services. 
          All sources are free and open for testing and analysis.
        </p>
      </div>

      {/* Category Filter */}
      <div className="flex flex-wrap gap-2 justify-center">
        {categories.map((category) => (
          <button
            key={category}
            onClick={() => setSelectedCategory(category)}
            className={`
              px-4 py-2 rounded-full text-sm font-medium transition-all duration-200
              ${selectedCategory === category
                ? 'bg-purple-600 text-white shadow-lg'
                : 'bg-gray-700 text-gray-300 hover:bg-gray-600 hover:text-white'
              }
            `}
          >
            {category}
          </button>
        ))}
      </div>

      {/* Sources Grid */}
      <div className="space-y-4 max-h-96 overflow-y-auto pr-2">
        {filteredSources.length === 0 ? (
          <div className="text-center py-8">
            <div className="text-gray-500 text-lg mb-2">No sources found</div>
            <p className="text-gray-600 text-sm">Try selecting a different category</p>
          </div>
        ) : (
          filteredSources.map((source) => (
            <div
              key={source.name}
              className="bg-gray-800 border border-gray-700 rounded-xl p-6 hover:bg-gray-750 hover:border-gray-600 transition-all duration-200 group"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  {/* Source Header */}
                  <div className="flex items-center space-x-3 mb-3">
                    <div className="flex-shrink-0">
                      <div className="w-10 h-10 bg-purple-500/20 rounded-lg flex items-center justify-center group-hover:bg-purple-500/30 transition-colors">
                        <svg className="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                      </div>
                    </div>
                    <div className="min-w-0 flex-1">
                      <h3 className="text-lg font-semibold text-white group-hover:text-purple-200 transition-colors">
                        {source.name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      </h3>
                      <div className="flex items-center space-x-2 mt-1">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-500/20 text-purple-300 border border-purple-500/30">
                          {source.category}
                        </span>
                        <span className="text-xs text-gray-500">•</span>
                        <span className="text-xs text-gray-500">Ready to download</span>
                      </div>
                    </div>
                  </div>

                  {/* Description */}
                  <p className="text-gray-300 text-sm leading-relaxed mb-4">
                    {source.description}
                  </p>

                  {/* Source URL */}
                  <div className="flex items-center space-x-2 text-xs text-gray-500">
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                    </svg>
                    <span className="truncate">Source: {source.url}</span>
                  </div>
                </div>
                
                {/* Download Button */}
                <div className="flex-shrink-0 ml-4">
                  <button
                    onClick={() => handleDownload(source.name)}
                    disabled={downloading === source.name}
                    className={`
                      px-6 py-3 rounded-lg font-medium text-sm transition-all duration-200 flex items-center space-x-2
                      ${downloading === source.name
                        ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                        : 'bg-purple-600 hover:bg-purple-700 text-white shadow-lg hover:shadow-xl transform hover:scale-105'
                      }
                    `}
                  >
                    {downloading === source.name ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                        <span>Downloading...</span>
                      </>
                    ) : (
                      <>
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                        </svg>
                        <span>Download & Analyze</span>
                      </>
                    )}
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
} 