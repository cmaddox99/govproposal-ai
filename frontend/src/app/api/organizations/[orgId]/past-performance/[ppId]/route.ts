import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = 'https://backend-production-d1d1.up.railway.app';

export async function PUT(
  request: NextRequest,
  { params }: { params: { orgId: string; ppId: string } }
) {
  try {
    const authHeader = request.headers.get('authorization');
    const body = await request.json();
    const response = await fetch(
      `${BACKEND_URL}/api/v1/organizations/${params.orgId}/past-performance/${params.ppId}`,
      {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          ...(authHeader ? { Authorization: authHeader } : {}),
        },
        body: JSON.stringify(body),
      }
    );
    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error: any) {
    return NextResponse.json({ detail: error.message }, { status: 500 });
  }
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: { orgId: string; ppId: string } }
) {
  try {
    const authHeader = request.headers.get('authorization');
    const response = await fetch(
      `${BACKEND_URL}/api/v1/organizations/${params.orgId}/past-performance/${params.ppId}`,
      {
        method: 'DELETE',
        headers: {
          ...(authHeader ? { Authorization: authHeader } : {}),
        },
      }
    );
    if (response.status === 204) {
      return new NextResponse(null, { status: 204 });
    }
    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error: any) {
    return NextResponse.json({ detail: error.message }, { status: 500 });
  }
}
