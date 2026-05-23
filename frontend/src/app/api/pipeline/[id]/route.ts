import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = 'https://backend-production-d1d1.up.railway.app';

export async function PATCH(request: NextRequest, { params }: { params: { id: string } }) {
  try {
    const authHeader = request.headers.get('authorization');
    const body = await request.json();
    const response = await fetch(`${BACKEND_URL}/api/v1/pipeline/${params.id}`, {
      method: 'PATCH',
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
    return NextResponse.json({ detail: error.message || 'Failed to update pipeline item' }, { status: 500 });
  }
}

export async function DELETE(request: NextRequest, { params }: { params: { id: string } }) {
  try {
    const authHeader = request.headers.get('authorization');
    const response = await fetch(`${BACKEND_URL}/api/v1/pipeline/${params.id}`, {
      method: 'DELETE',
      headers: { ...(authHeader ? { Authorization: authHeader } : {}) },
    });
    const data = await response.json();
    if (!response.ok) return NextResponse.json(data, { status: response.status });
    return NextResponse.json(data);
  } catch (error: any) {
    return NextResponse.json({ detail: error.message || 'Failed to delete pipeline item' }, { status: 500 });
  }
}
