# Báo cáo Day 13 Observability

## 1. Thông tin nhóm

- Tên nhóm: Day13-K4-Observability-HiHi
- Repository URL: https://github.com/nguyenhungict/Day13-K4-Observability-HiHi
- Commit SHA cuối: _Cập nhật bằng `git rev-parse HEAD` sau commit nộp bài cuối._
- Thành viên và vai trò:

| Thành viên | MSSV | Vai trò |
|---|---|---|
| Nguyễn Duy Hưng | 2A202601702 | Logging & Correlation ID |
| Nguyễn Hoàng Thảo Tiên | 2A202601650 | PII Redaction & Request Metadata |
| Đoàn Duy Chiến | 2A202601366 | Langfuse Tracing & Prompt Versioning |
| Trần Bảo Phúc | 2A202601148 | Dashboard, SLO & Alerts |
| Nguyễn Xuân Kiên | 2A202601398 | Incident Investigation, Report & Demo |

## 2. Kết quả kỹ thuật

- Điểm `validate_logs.py`: 100/100 (233 log records, 111 correlation IDs).
- Tổng số traces: ≥20 traces thật; xem `evidence/traces-list.png`.
- Số PII leak còn lại: 0.
- Link/đường dẫn dashboard: `evidence/dashboard.html` và `evidence/dashboard.png`.

## 3. Logging và tracing

- Evidence correlation ID: `evidence/correlation-id.png` — request `req-12b31be0` xuất hiện ở response header và log.
- Evidence PII redaction: `evidence/pii-redaction.png` — email và số điện thoại được thay bằng `[REDACTED_EMAIL]` và `[REDACTED_PHONE_VN]`.
- Evidence trace waterfall: `evidence/trace-baseline-waterfall.png`.
- Giải thích một span đáng chú ý: generation `run` của request candidate ghi model, token/cost, prompt metadata và thời gian end-to-end; đây là span dùng để so sánh latency giữa các prompt/incident.

## 4. Prompt versioning

- Prompt name: `day13-chat`.
- Version/label baseline: version 1 — labels `baseline`, `production`.
- Version/label candidate: version 2 — label `candidate`.
- Trace ID của mỗi version: baseline v1 `bfc029c2953e4db4d22a49470f8d37bd`; candidate v2 `0ac1bde3a2ba7820494cd8f667ba41dc`; production v2 `884547623d175a42e01496f8c5718619`; rollback production v1 `296d7db5385c4a085328815617adb3f2`.
- Bằng chứng đổi label hoặc rollback: `evidence/production-v2.png`, `evidence/prompt-rollback.png`, `evidence/trace-production-v2.png`, `evidence/trace-production-rollback-v1.png`.

## 5. Dashboard, SLO và alerts

- Kết quả `validate_dashboard.py`: HỢP LỆ: 6/6 panel.
- Evidence dashboard: `evidence/dashboard.png`, `evidence/validate-dashboard.png`.
- SLO đã chọn và lý do: P95 latency ≤3000 ms (99.5%), error rate ≤2% (99%), daily cost ≤$2.50 và quality average ≥0.75. Các mục tiêu này phản ánh trực tiếp trải nghiệm chat, độ tin cậy, ngân sách và chất lượng câu trả lời.
- Alert rules và runbook: `config/alert_rules.yaml`, `docs/alerts.md`; gồm latency SLO breach, error-rate SLO breach và quality degradation.

## 6. Điều tra challenge

- Challenge ID: `day13-k4-observability-v1`.
- Triệu chứng từ metrics: khi chạy 5 query `monitoring` với concurrency 5, HTTP tail latency tăng đến khoảng 14 giây; P95 latency trong log đạt 3358 ms, vượt SLO 3000 ms.
- Trace ID liên quan: `24e405d9bc2c59c066bc1d675442ee68` (session `k4-challenge-s01`).
- Log line/correlation ID liên quan: `req-f6bcd2c3`, `response_sent.latency_ms=3358`, feature `monitoring`; xem `evidence/challenge-log.png`.
- Root cause: incident `rag_slow` thêm 2.5 giây vào `retrieve()`; hàm agent chạy đồng bộ nên các request concurrent bị xếp hàng, làm tăng tail latency.
- Fix action: chuyển retrieval blocking sang threadpool/async worker và cache kết quả retrieval phù hợp.
- Preventive measure: alert P95 latency, theo dõi span retrieval, giới hạn concurrency và chạy load test concurrency trước deployment.

## 7. Đóng góp cá nhân

Với mỗi thành viên, ghi rõ nhiệm vụ và link commit/PR tương ứng.

| Thành viên | Phần việc | Commit/PR | Điều đã học |
|---|---|---|---|
| Nguyễn Duy Hưng | Correlation ID, contextvars và response headers | `5b9557b` / PR #1 | Correlation ID giúp nối log của cùng một request. |
| Nguyễn Hoàng Thảo Tiên | PII redaction và request metadata | `bf745e5` / PR #2 | PII phải được che trước khi JSON log được render. |
| Đoàn Duy Chiến | Langfuse trace, prompt version và rollback | `e5fb64b` / PR #4 | Trace phải ghi label/version thật của prompt đã dùng. |
| Trần Bảo Phúc | Dashboard, SLO, alert và runbook | `58c7259` / PR #3 | P95, error rate và quality proxy phải có threshold rõ ràng. |
| Nguyễn Xuân Kiên | Incident, evidence, report và demo | `3817c95` / PR #5 | Kết luận incident cần khớp metrics, trace và log. |
