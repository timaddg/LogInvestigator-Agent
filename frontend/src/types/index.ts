export interface LogSource {
  name: string;
  description: string;
  category: string;
  url: string;
}

export interface LogStatistics {
  total_entries: number;
  unique_ips: number;
  unique_user_agents: number;
  status_codes: Record<string, number>;
  top_endpoints: Array<{ endpoint: string; count: number }>;
  time_range: {
    start?: string;
    end?: string;
  };
}

export interface AnalysisData {
  success: boolean;
  filename?: string;
  source?: string;
  log_count: number;
  statistics: LogStatistics;
  analysis: string;
}

export interface UploadResponse {
  success: boolean;
  filename: string;
  log_count: number;
  statistics: LogStatistics;
  analysis: string;
}

export interface DownloadResponse {
  success: boolean;
  source: string;
  filename: string;
  log_count: number;
  statistics: LogStatistics;
  analysis: string;
}

export interface SourcesResponse {
  sources: LogSource[];
} 