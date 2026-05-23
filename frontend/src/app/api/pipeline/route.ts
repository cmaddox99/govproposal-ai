import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = 'https://backend-production-d1d1.up.railway.app';

export async function GET(request: NextRequest) {
  try {
    const authHeader = request.headers.get('authorization');
    const searchParams = request.nextUrl.searchParams;
    const response = await fetch(`${BACKEND_URL}/api/v1/pipeline?${searchParams.toString()}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...(authHeader ? { Authorization: authHeader } : {}),
      },
    });
    const data = await response.json();
    if (!response.ok) return NextResponse.json(data, { status: response.status });
    return NextResponse.json(data);
  } catch (error: any) {
    return NextResponse.json({ detail: error.message || 'Failed to fetch pipeline' }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    const authHeader = request.headers.get('authorization');
    const body = await request.json();
    const response = await fetch(`${BACKEND_URL}/api/v1/pipeline`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(authHeader ? { Authorization: authHeader } : {}),
      },
      body: JSON.stringify(body),
    });
    const data = await response.json();
    if (!response.ok) return NextResponse.json(data, { status: response.status });
    return NextResponse.json(data);
  } catch (error: any) {
    return NextResponse.json({ detail: error.message || 'Failed to add to pipeline' }, { status: 500 });
  }
}
