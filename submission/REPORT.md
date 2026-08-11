# Báo cáo Day 13 Observability

## 1. Thông tin nhóm

- Tên nhóm:
- Repository URL:
- Commit SHA cuối:
- Thành viên và vai trò:

| Thành viên | MSSV | Vai trò |
|---|---|---|
| Nguyễn Duy Hưng | 2A202601702 | Logging & Correlation ID |
| Nguyễn Hoàng Thảo Tiên | 2A202601650 | PII Redaction & Request Metadata |
| Đoàn Duy Chiến | 2A202601366 | Langfuse Tracing & Prompt Versioning |
| Trần Bảo Phúc | 2A202601148 | Dashboard, SLO & Alerts |
| Nguyễn Xuân Kiên | 2A202601398 | Incident Investigation, Report & Demo |

## 2. Kết quả kỹ thuật

- Điểm `validate_logs.py`:
- Tổng số traces:
- Số PII leak còn lại:
- Link/đường dẫn dashboard:

## 3. Logging và tracing

- Evidence correlation ID:
- Evidence PII redaction:
- Evidence trace waterfall:
- Giải thích một span đáng chú ý:

## 4. Prompt versioning

- Prompt name:
- Version/label baseline:
- Version/label candidate:
- Trace ID của mỗi version:
- Bằng chứng đổi label hoặc rollback:

## 5. Dashboard, SLO và alerts

- Kết quả `validate_dashboard.py`:
- Evidence dashboard:
- SLO đã chọn và lý do:
- Alert rules và runbook:

## 6. Điều tra challenge

- Challenge ID:
- Triệu chứng từ metrics:
- Trace ID liên quan:
- Log line/correlation ID liên quan:
- Root cause:
- Fix action:
- Preventive measure:

## 7. Đóng góp cá nhân

Với mỗi thành viên, ghi rõ nhiệm vụ và link commit/PR tương ứng.

| Thành viên | Phần việc | Commit/PR | Điều đã học |
|---|---|---|---|
| Nguyễn Duy Hưng | Correlation ID, contextvars và response headers | `hung` / _điền commit SHA_ | Correlation ID giúp nối log của cùng một request. |
| Nguyễn Hoàng Thảo Tiên | PII redaction và request metadata | `tien` / _điền commit SHA_ | PII phải được che trước khi JSON log được render. |
| Đoàn Duy Chiến | Langfuse trace, prompt version và rollback | `chien` / _điền commit SHA_ | Trace phải ghi label/version thật của prompt đã dùng. |
| Trần Bảo Phúc | Dashboard, SLO, alert và runbook | `phuc` / _điền commit SHA_ | P95, error rate và quality proxy phải có threshold rõ ràng. |
| Nguyễn Xuân Kiên | Incident, evidence, report và demo | `kien` / _điền commit SHA_ | Kết luận incident cần khớp metrics, trace và log. |
