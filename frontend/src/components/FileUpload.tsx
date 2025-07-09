'use client';

import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { AnalysisData } from '@/types';

interface FileUploadProps {
  onAnalysisComplete: (data: AnalysisData) => void;
  onError: (error: string) => void;
  onLoading: (loading: boolean) => void;
}

export default function FileUpload({ onAnalysisComplete, onError, onLoading }: FileUploadProps) {
  const [isUploading, setIsUploading] = useState(false);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    setIsUploading(true);
    onLoading(true);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('/upload', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Upload failed');
      }

      onAnalysisComplete(data);
    } catch (error) {
      onError(error instanceof Error ? error.message : 'Upload failed');
    } finally {
      setIsUploading(false);
      onLoading(false);
    }
  }, [onAnalysisComplete, onError, onLoading]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/json': ['.json'],
      'text/plain': ['.log', '.txt'],
      'text/csv': ['.csv'],
    },
    multiple: false,
    maxSize: 50 * 1024 * 1024, // 50MB
  });

  return (
    <div className="space-y-6">
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-200
          ${isDragActive 
            ? 'border-purple-400 bg-gray-800' 
            : 'border-gray-600 hover:border-purple-400 hover:bg-gray-800'
          }
          ${isUploading ? 'opacity-50 cursor-not-allowed' : ''}
        `}
      >
        <input {...getInputProps()} />
        
        {isUploading ? (
          <div className="space-y-4">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-400 mx-auto"></div>
            <p className="text-gray-300">Uploading and analyzing...</p>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="mx-auto w-16 h-16 bg-purple-500/20 rounded-full flex items-center justify-center">
              <svg className="w-8 h-8 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            
            <div>
              <p className="text-lg font-medium text-white">
                {isDragActive ? 'Drop your log file here' : 'Drag & drop your log file here'}
              </p>
              <p className="text-gray-400 mt-2">or click to browse</p>
            </div>
            
            <div className="text-sm text-gray-500">
              <p>Supported formats: JSON, LOG, TXT, CSV</p>
              <p>Maximum file size: 50MB</p>
            </div>
          </div>
        )}
      </div>

      <div className="bg-gray-800 border border-gray-600 rounded-lg p-4">
        <div className="flex items-start space-x-3">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div className="text-sm text-blue-200">
            <p className="font-medium">Upload your log files</p>
            <p className="mt-1">Our AI will analyze your logs and provide insights about security threats, performance issues, and system anomalies.</p>
          </div>
        </div>
      </div>
    </div>
  );
} 