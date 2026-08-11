# Phân công nhóm — Day 13 AI Observability

## Thành viên

| STT | Thành viên | MSSV | Vai trò |
|---:|---|---|---|
| 1 | Nguyễn Duy Hưng | 2A202601702 | Logging & Correlation ID |
| 2 | Nguyễn Hoàng Thảo Tiên | 2A202601650 | PII Redaction & Request Metadata |
| 3 | Đoàn Duy Chiến | 2A202601366 | Langfuse Tracing & Prompt Versioning |
| 4 | Trần Bảo Phúc | 2A202601148 | Dashboard, SLO & Alerts |
| 5 | Nguyễn Xuân Kiên | 2A202601398 | Incident Investigation, Report & Demo |

> README quy định tối đa bốn vai trò chính. Thành viên 1 và 2 cùng thuộc mảng
> **Logging & PII**, nhưng tách đầu ra và commit để chứng minh đóng góp cá nhân.

## Phân công chi tiết

### 1. Nguyễn Duy Hưng — Logging & Correlation ID

- Hoàn thiện `app/middleware.py`:
  - xóa `contextvars` trước mỗi request;
  - đọc `x-request-id` từ header hoặc sinh ID dạng `req-<8-char-hex>`;
  - bind `correlation_id` vào log context;
  - trả `x-request-id` và `x-response-time-ms` trên response.
- Kiểm tra correlation ID xuyên suốt các log của cùng một request.
- Hỗ trợ chạy load test để sinh log baseline.

**Bàn giao/evidence:** commit phần middleware; ảnh hoặc trích đoạn log JSON có
`correlation_id`; ảnh response header; cập nhật đường dẫn evidence vào report.

### 2. Nguyễn Hoàng Thảo Tiên — PII Redaction & Request Metadata

- Hoàn thiện `app/main.py` để bind metadata chung cho request:
  `user_id_hash`, `session_id`, `feature`, `model`, `env`.
- Hoàn thiện `app/logging_config.py` để processor `scrub_event` chạy trước khi
  log được render/ghi ra `data/logs.jsonl`.
- Kiểm tra không lộ email, số điện thoại Việt Nam, CCCD hoặc số thẻ trong log;
  chỉ dùng `hash_user_id`, không ghi user ID thô.
- Chạy `python scripts/validate_logs.py`, mục tiêu tối thiểu 80/100.

**Bàn giao/evidence:** commit logging/PII; kết quả validator; log đã redact;
log có đầy đủ request metadata; cập nhật đường dẫn evidence vào report.

### 3. Đoàn Duy Chiến — Langfuse Tracing & Prompt Versioning

- Cấu hình Langfuse bằng `.env` cục bộ, không commit key/secret.
- Tạo prompt text tên `day13-chat` với ba biến:
  `{{feature}}`, `{{docs}}`, `{{message}}`.
- Tạo version 1 với label `baseline` và `production`; tạo version 2 với label
  `candidate`.
- Chạy ít nhất 10 request có trace; xác nhận trace có `prompt_name`,
  `prompt_label`, `prompt_version`.
- Chạy cùng input với `baseline` và `candidate`; chuyển `production` sang v2,
  sau đó rollback về v1.

**Bàn giao/evidence:** danh sách ít nhất 10 trace; 1 trace waterfall; ảnh hai
prompt version; hai trace ID của hai label; ảnh đổi label/rollback; cập nhật
ID và đường dẫn evidence vào report.

### 4. Trần Bảo Phúc — Dashboard, SLO & Alerts

- Dựng dashboard dùng `data/logs.jsonl` và đúng contract
  `config/dashboard.yaml`.
- Hiển thị sáu nhóm panel: latency P50/P95/P99, traffic, error rate/breakdown,
  cost, input/output tokens, quality proxy.
- Giữ time range 60 phút, refresh 15–30 giây (nếu công cụ hỗ trợ), đơn vị và
  threshold/SLO line rõ ràng.
- Hoàn thiện `config/alert_rules.yaml` với 3 alert symptom-based có severity,
  điều kiện, owner và runbook.
- Hoàn thiện ba runbook trong `docs/alerts.md`; rà soát mục tiêu ở
  `config/slo.yaml`.
- Chạy `python scripts/validate_dashboard.py` và phải nhận `HỢP LỆ: 6/6 panel`.

**Bàn giao/evidence:** commit dashboard/SLO/alert; kết quả validator; ảnh
dashboard nhìn rõ panel, time range, đơn vị, threshold; alert rules và runbook;
cập nhật đường dẫn evidence vào report.

### 5. Nguyễn Xuân Kiên — Incident Investigation, Report & Demo

- Chạy baseline và practice incident `rag_slow`; khi dùng challenge chính thức,
  chỉ chạy file `config/challenge.json` do Lab Coach release, tuyệt đối không
  sửa file này.
- Điều tra theo luồng **Metrics → Trace → Log**: nêu triệu chứng, trace/span
  bất thường, correlation ID/log line, root cause, fix action và preventive
  measure.
- Tổng hợp evidence trong `submission/evidence/` và hoàn thiện
  `submission/REPORT.md`, bao gồm bảng đóng góp/commit của cả năm thành viên.
- Kiểm tra cuối: `python -m pytest -q`, `python scripts/validate_logs.py`,
  `python scripts/validate_dashboard.py`, `git status --short`.
- Chuẩn bị demo luồng Metrics → Traces → Logs → Root cause; mỗi thành viên giải
  thích được phần việc mình phụ trách.

**Bàn giao/evidence:** evidence challenge (metric, trace ID, log/correlation
ID); report hoàn chỉnh; kịch bản demo; commit tổng hợp cuối.

## Mốc phối hợp đề xuất

| Mốc | Người chính | Điều kiện hoàn thành |
|---|---|---|
| Setup & baseline | Cả nhóm | API `/health`, load test và `data/logs.jsonl` hoạt động |
| Logging & PII | Hưng, Thảo Tiên | Log hợp lệ, không lộ PII, validator logs ≥80 |
| Trace & prompt | Chiến | ≥10 traces, v1/v2, label và rollback có evidence |
| Dashboard & alert | Bảo Phúc | Validator dashboard 6/6, dashboard/alert/runbook hoàn chỉnh |
| Challenge & nộp bài | Xuân Kiên + cả nhóm | Evidence, report, test và commit cuối hoàn tất |

## Quy ước nộp bài

- Mỗi thành viên tạo ít nhất một commit rõ phần việc của mình; ghi hash/link vào
  bảng đóng góp của `submission/REPORT.md`.
- Lưu ảnh và kết quả kiểm tra tại `submission/evidence/`, rồi dẫn bằng đường
  dẫn tương đối trong report.
- Không commit `.env`, API key/secret, log chứa PII chưa che, hoặc tự ý sửa
  `config/challenge.json`.
