"""Ad-hoc check: run the multi-record past-performance extraction parser
against canned model output shapes, and (if a key is configured) the real
DKW docx. Run from backend/: py -3.12 scripts/test_multi_extract.py [path-to-docx]
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from govproposal.config import settings  # noqa: E402
from govproposal.identity.past_performance_extraction import (  # noqa: E402
    extract_past_performance,
    extract_text,
)


def check_parser_shapes() -> None:
    """The post-API parsing logic, exercised inline (mirrors the function body)."""
    import json

    cases = {
        "records-object": '{"records": [{"contract_name": "A"}, {"contract_name": "B"}]}',
        "bare-list": '[{"contract_name": "A"}, {"contract_name": "B"}]',
        "single-object-legacy": '{"contract_name": "A"}',
        "missing-name-filtered": '{"records": [{"contract_name": "A"}, {"agency": "no name"}]}',
    }
    expected = {"records-object": 2, "bare-list": 2, "single-object-legacy": 1, "missing-name-filtered": 1}

    for label, raw in cases.items():
        parsed = json.loads(raw)
        if isinstance(parsed, dict) and isinstance(parsed.get("records"), list):
            records = parsed["records"]
        elif isinstance(parsed, list):
            records = parsed
        elif isinstance(parsed, dict):
            records = [parsed]
        else:
            records = []
        records = [r for r in records if isinstance(r, dict) and r.get("contract_name")]
        status = "PASS" if len(records) == expected[label] else "FAIL"
        print(f"  [{status}] {label}: {len(records)} record(s), expected {expected[label]}")


async def run_real_extraction(docx_path: str) -> None:
    text = extract_text(docx_path, None, docx_path)
    print(f"Document text: {len(text)} chars")
    records = await extract_past_performance(text)
    print(f"Extracted {len(records)} past performance record(s):")
    for i, r in enumerate(records, 1):
        print(f"  {i}. {r.get('contract_name')} | {r.get('agency')} | ${r.get('contract_value')}")


if __name__ == "__main__":
    print("Parser shape checks:")
    check_parser_shapes()

    docx = sys.argv[1] if len(sys.argv) > 1 else None
    if docx and settings.anthropic_api_key:
        asyncio.run(run_real_extraction(docx))
    elif docx:
        print("\nNo ANTHROPIC_API_KEY configured — skipping live extraction.")
        text = extract_text(docx, None, docx)
        print(f"(docx text extraction still works: {len(text)} chars)")
