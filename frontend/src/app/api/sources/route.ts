import { NextResponse } from 'next/server';

const FLASK_BACKEND_URL = process.env.FLASK_BACKEND_URL || 'http://backend:8000';

export async function GET() {
  try {
    const response = await fetch(`${FLASK_BACKEND_URL}/sources`);

    if (!response.ok) {
      throw new Error('Failed to fetch sources');
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Sources error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch sources' },
      { status: 500 }
    );
  }
} 