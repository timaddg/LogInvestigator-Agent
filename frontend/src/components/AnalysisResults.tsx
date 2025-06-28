'use client';

import { useState } from 'react';
import { AnalysisData } from '@/types';

interface AnalysisResultsProps {
  data: AnalysisData;
}

export default function AnalysisResults({ data }: AnalysisResultsProps) {
  const [activeTab, setActiveTab] = useState<'analysis' | 'statistics'>('analysis');

  const formatNumber = (num: number) => {
    return new Intl.NumberFormat().format(num);
  };

  const getStatusColor = (status: string) => {
    const code = parseInt(status);
    if (code >= 200 && code < 300) return 'text-green-400';
    if (code >= 300 && code < 400) return 'text-yellow-400';
    if (code >= 400 && code < 500) return 'text-orange-400';
    if (code >= 500) return 'text-red-400';
    return 'text-gray-400';
  };

  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-2xl border border-white/20 overflow-hidden">
      {/* Header */}
      <div className="bg-white/5 px-8 py-6 border-b border-white/10">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-semibold text-white">Analysis Results</h2>
            <p className="text-gray-400 mt-1">
              {data.filename && `File: ${data.filename}`}
              {data.source && `Source: ${data.source}`}
            </p>
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold text-purple-400">
              {formatNumber(data.log_count)}
            </div>
            <div className="text-sm text-gray-400">Log Entries</div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-white/10">
        <button
          onClick={() => setActiveTab('analysis')}
          className={`
            flex-1 px-6 py-4 text-sm font-medium transition-colors
            ${activeTab === 'analysis'
              ? 'text-purple-400 border-b-2 border-purple-400 bg-white/5'
              : 'text-gray-400 hover:text-white hover:bg-white/5'
            }
          `}
        >
          AI Analysis
        </button>
        <button
          onClick={() => setActiveTab('statistics')}
          className={`
            flex-1 px-6 py-4 text-sm font-medium transition-colors
            ${activeTab === 'statistics'
              ? 'text-purple-400 border-b-2 border-purple-400 bg-white/5'
              : 'text-gray-400 hover:text-white hover:bg-white/5'
            }
          `}
        >
          Statistics
        </button>
      </div>

      {/* Content */}
      <div className="p-8">
        {activeTab === 'analysis' && (
          <div className="space-y-6">
            <div className="bg-gradient-to-r from-purple-500/10 to-blue-500/10 border border-purple-500/20 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-white mb-4">AI Insights</h3>
              <div className="prose prose-invert max-w-none">
                <div className="whitespace-pre-wrap text-gray-200 leading-relaxed">
                  {data.analysis}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'statistics' && (
          <div className="space-y-8">
            {/* Overview Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white/5 border border-white/10 rounded-lg p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-blue-500/20 rounded-lg flex items-center justify-center">
                      <svg className="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                      </svg>
                    </div>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-400">Total Entries</p>
                    <p className="text-2xl font-semibold text-white">
                      {formatNumber(data.statistics.total_entries)}
                    </p>
                  </div>
                </div>
              </div>

              <div className="bg-white/5 border border-white/10 rounded-lg p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-green-500/20 rounded-lg flex items-center justify-center">
                      <svg className="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                      </svg>
                    </div>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-400">Unique IPs</p>
                    <p className="text-2xl font-semibold text-white">
                      {formatNumber(data.statistics.unique_ips)}
                    </p>
                  </div>
                </div>
              </div>

              <div className="bg-white/5 border border-white/10 rounded-lg p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-purple-500/20 rounded-lg flex items-center justify-center">
                      <svg className="w-4 h-4 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                      </svg>
                    </div>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-400">User Agents</p>
                    <p className="text-2xl font-semibold text-white">
                      {formatNumber(data.statistics.unique_user_agents)}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Status Codes */}
            <div className="bg-white/5 border border-white/10 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-white mb-4">HTTP Status Codes</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
                {Object.entries(data.statistics.status_codes)
                  .sort(([,a], [,b]) => b - a)
                  .slice(0, 12)
                  .map(([status, count]) => (
                    <div key={status} className="text-center">
                      <div className={`text-2xl font-bold ${getStatusColor(status)}`}>
                        {status}
                      </div>
                      <div className="text-sm text-gray-400">
                        {formatNumber(count)}
                      </div>
                    </div>
                  ))}
              </div>
            </div>

            {/* Top Endpoints */}
            <div className="bg-white/5 border border-white/10 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-white mb-4">Top Endpoints</h3>
              <div className="space-y-3">
                {data.statistics.top_endpoints.slice(0, 10).map((endpoint, index) => (
                  <div key={index} className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="w-6 h-6 bg-purple-500/20 rounded flex items-center justify-center">
                        <span className="text-xs font-medium text-purple-400">{index + 1}</span>
                      </div>
                      <span className="text-gray-200 font-mono text-sm truncate">
                        {endpoint.endpoint}
                      </span>
                    </div>
                    <span className="text-gray-400 font-medium">
                      {formatNumber(endpoint.count)}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Time Range */}
            {data.statistics.time_range.start && data.statistics.time_range.end && (
              <div className="bg-white/5 border border-white/10 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-white mb-4">Time Range</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-400">Start</p>
                    <p className="text-white font-mono">{data.statistics.time_range.start}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-400">End</p>
                    <p className="text-white font-mono">{data.statistics.time_range.end}</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
} 