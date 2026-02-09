import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = 'https://backend-production-d1d1.up.railway.app';

export async function POST(request: NextRequest) {
  try {
    const authHeader = request.headers.get('authorization');
    const body = await request.json();

    const response = await fetch(`${BACKEND_URL}/api/v1/proposals/from-opportunity`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(authHeader ? { Authorization: authHeader } : {}),
      },
      body: JSON.stringify(body),
    });

    const data = await response.json();

    if (!response.ok) {
      return NextResponse.json(data, { status: response.status });
    }

    return NextResponse.json(data);
  } catch (error: any) {
    console.error('Proxy error:', error);
    return NextResponse.json(
      { detail: error.message || 'Failed to create proposal from opportunity' },
      { status: 500 }
    );
  }
}
