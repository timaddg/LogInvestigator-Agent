import { NextRequest, NextResponse } from 'next/server';

const FLASK_BACKEND_URL = process.env.FLASK_BACKEND_URL || 'http://backend:8000';

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const file = formData.get('file') as File;

    if (!file) {
      return NextResponse.json(
        { error: 'No file provided' },
        { status: 400 }
      );
    }

    // Create a new FormData to forward to Flask backend
    const flaskFormData = new FormData();
    flaskFormData.append('file', file);

    // Forward the request to Flask backend
    const response = await fetch(`${FLASK_BACKEND_URL}/upload`, {
      method: 'POST',
      body: flaskFormData,
    });

    const data = await response.json();

    if (!response.ok) {
      return NextResponse.json(
        { error: data.error || 'Upload failed' },
        { status: response.status }
      );
    }

    return NextResponse.json(data);
  } catch (error) {
    console.error('Upload error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
} 