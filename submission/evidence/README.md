# Evidence cần nộp

Không đưa secret hoặc PII chưa redact vào thư mục này. Sau mỗi thao tác, lưu
ảnh/kết quả với tên dưới đây và dẫn link tương đối trong `submission/REPORT.md`.

| Tệp đề xuất | Nội dung cần thấy |
|---|---|
| `validate-logs.txt` | Kết quả cuối `python scripts/validate_logs.py` (mục tiêu ≥80/100) |
| `correlation-id.png` | JSON log và response header có cùng `correlation_id` |
| `pii-redaction.png` | Email/phone/CCCD/card đã thành `[REDACTED_*]` |
| `traces-list.png` | Danh sách tối thiểu 10 trace thật trên Langfuse |
| `trace-waterfall.png` | Một trace waterfall có span rõ ràng |
| `prompt-versions.png` | Hai version prompt `day13-chat` |
| `prompt-baseline-candidate.png` | Hai trace cùng input, label/version khác nhau |
| `prompt-rollback.png` | Chuyển `production` và rollback về v1 |
| `dashboard.png` | Sáu panel, time range 60 phút, unit và threshold |
| `validate-dashboard.txt` | Kết quả `HỢP LỆ: 6/6 panel` |
| `challenge-metrics.png` | Triệu chứng trên dashboard/metrics |
| `challenge-trace.png` | Trace/span bất thường của challenge |
| `challenge-log.png` | Log có cùng correlation ID, chứng minh root cause |

## Chuỗi điều tra incident

1. Ghi time range và metric thể hiện triệu chứng.
2. Chọn trace bất thường trong cùng time range, ghi trace ID và span chậm/lỗi.
3. Tìm log có `correlation_id` tương ứng; chỉ kết luận root cause khi ba tín
   hiệu khớp nhau.
4. Ghi rõ fix action, preventive measure và evidence vào mục 6 của report.

Challenge chính thức chỉ dùng `config/challenge.json` do Lab Coach release;
tuyệt đối không sửa file này.
