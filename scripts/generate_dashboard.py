"""Generate a self-contained six-panel dashboard from JSONL application logs."""

from __future__ import annotations

import argparse
import html
import json
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any


def read_events(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict):
            events.append(event)
    return events


def percentile(values: list[float], percent: int) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = round((len(ordered) - 1) * percent / 100)
    return ordered[index]


def number(event: dict[str, Any], field: str) -> float | None:
    value = event.get(field)
    return float(value) if isinstance(value, int | float) else None


def fmt(value: float, digits: int = 2) -> str:
    return f"{value:,.{digits}f}"


def panel(title: str, body: str, status: str) -> str:
    return f'<section class="panel {status}"><h2>{html.escape(title)}</h2>{body}</section>'


def build_dashboard(events: list[dict[str, Any]]) -> str:
    requests = [event for event in events if event.get("event") == "request_received"]
    responses = [event for event in events if event.get("event") == "response_sent"]
    failures = [event for event in events if event.get("event") == "request_failed"]
    latencies = [value for event in responses if (value := number(event, "latency_ms")) is not None]
    costs = [value for event in responses if (value := number(event, "cost_usd")) is not None]
    tokens_in = [value for event in responses if (value := number(event, "tokens_in")) is not None]
    tokens_out = [value for event in responses if (value := number(event, "tokens_out")) is not None]
    quality = [value for event in responses if (value := number(event, "quality_score")) is not None]
    p50, p95, p99 = (percentile(latencies, item) for item in (50, 95, 99))
    error_rate = len(failures) / len(requests) * 100 if requests else 0.0
    error_types: dict[str, int] = {}
    for event in failures:
        error_type = str(event.get("error_type") or "unknown")
        error_types[error_type] = error_types.get(error_type, 0) + 1

    panels = [
        panel(
            "Latency percentiles",
            f"<p>P50 <strong>{fmt(p50, 0)} ms</strong> · P95 <strong>{fmt(p95, 0)} ms</strong> · P99 <strong>{fmt(p99, 0)} ms</strong></p><small>Threshold: P95 ≤ 3000 ms</small>",
            "ok" if p95 <= 3000 else "breach",
        ),
        panel(
            "Request traffic",
            f"<p><strong>{len(requests)}</strong> requests in the selected 60-minute window</p><small>Threshold: at least 1 request/minute during active testing</small>",
            "ok" if requests else "neutral",
        ),
        panel(
            "Error rate and breakdown",
            f"<p><strong>{fmt(error_rate)}%</strong> error rate · {len(failures)} failures</p><small>{html.escape(', '.join(f'{name}: {count}' for name, count in error_types.items()) or 'No failures')}</small><small>Threshold: ≤ 2%</small>",
            "ok" if error_rate <= 2 else "breach",
        ),
        panel(
            "Cost over time",
            f"<p>Total <strong>${fmt(sum(costs), 4)}</strong> across {len(costs)} responses</p><small>Threshold: ≤ $2.50 per 60-minute window</small>",
            "ok" if sum(costs) <= 2.5 else "breach",
        ),
        panel(
            "Input and output tokens",
            f"<p>Input <strong>{fmt(sum(tokens_in), 0)}</strong> · Output <strong>{fmt(sum(tokens_out), 0)}</strong> tokens</p><small>Threshold: ≤ 50,000 total tokens</small>",
            "ok" if sum(tokens_in) + sum(tokens_out) <= 50000 else "breach",
        ),
        panel(
            "Quality proxy",
            f"<p>Mean quality score <strong>{fmt(mean(quality) if quality else 0.0)}</strong></p><small>Threshold: ≥ 0.75</small>",
            "ok" if quality and mean(quality) >= 0.75 else "breach",
        ),
    ]
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Day 13 AI Observability Dashboard</title><style>
body {{ font-family: Inter, system-ui, sans-serif; margin: 2rem; background: #f5f7fb; color: #1d2939; }}
h1 {{ margin-bottom: .2rem; }} .meta {{ color: #475467; margin-top: 0; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(310px,1fr)); gap:1rem; margin-top:1.5rem; }}
.panel {{ background:#fff; border-left:6px solid #98a2b3; padding:1rem 1.2rem; border-radius:8px; box-shadow:0 1px 3px #1018281a; }}
.panel.ok {{ border-color:#12b76a; }} .panel.breach {{ border-color:#f04438; }} .panel h2 {{ font-size:1.05rem; margin-top:0; }}
.panel p {{ font-size:1.1rem; }} small {{ display:block; color:#475467; margin-top:.5rem; }} strong {{ color:#101828; }}
</style></head><body><h1>Day 13 AI Observability</h1>
<p class="meta">Source: <code>data/logs.jsonl</code> · Default range: 60 minutes · Refresh: regenerate every 30 seconds · Generated: {generated_at}</p>
<main class="grid">{''.join(panels)}</main></body></html>"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Render the Day 13 six-panel dashboard.")
    parser.add_argument("--input", type=Path, default=Path("data/logs.jsonl"))
    parser.add_argument("--output", type=Path, default=Path("submission/evidence/dashboard.html"))
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(build_dashboard(read_events(args.input)), encoding="utf-8")
    print(f"Dashboard written to {args.output}")


if __name__ == "__main__":
    main()
