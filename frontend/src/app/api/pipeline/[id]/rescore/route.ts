import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = 'https://backend-production-d1d1.up.railway.app';

export async function POST(request: NextRequest, { params }: { params: { id: string } }) {
  try {
    const authHeader = request.headers.get('authorization');
    const response = await fetch(`${BACKEND_URL}/api/v1/pipeline/${params.id}/rescore`, {
      method: 'POST',
      headers: { ...(authHeader ? { Authorization: authHeader } : {}) },
    });
    const data = await response.json();
    if (!response.ok) return NextResponse.json(data, { status: response.status });
    return NextResponse.json(data);
  } catch (error: any) {
    return NextResponse.json({ detail: error.message || 'Failed to rescore' }, { status: 500 });
  }
}
