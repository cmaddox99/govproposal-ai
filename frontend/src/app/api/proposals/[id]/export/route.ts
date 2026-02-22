import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = 'https://backend-production-d1d1.up.railway.app';

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const authHeader = request.headers.get('authorization');
    const { searchParams } = new URL(request.url);
    const format = searchParams.get('format') || 'docx';

    const response = await fetch(
      `${BACKEND_URL}/api/v1/proposals/${params.id}/export?format=${format}`,
      {
        method: 'GET',
        headers: {
          ...(authHeader ? { Authorization: authHeader } : {}),
        },
      }
    );

    if (!response.ok) {
      const text = await response.text();
      return NextResponse.json(
        { detail: text || 'Export failed' },
        { status: response.status }
      );
    }

    const blob = await response.blob();
    const headers = new Headers();
    headers.set('Content-Type', response.headers.get('content-type') || 'application/octet-stream');
    const disposition = response.headers.get('content-disposition');
    if (disposition) {
      headers.set('Content-Disposition', disposition);
    }

    return new NextResponse(blob, { status: 200, headers });
  } catch (error: any) {
    return NextResponse.json({ detail: error.message }, { status: 500 });
  }
}
