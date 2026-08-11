# Template Alert và Runbook

Mỗi alert phải dựa trên triệu chứng người dùng hoặc SLO, không dựa trực tiếp vào tên implementation nội bộ.

## Alert 1

- Tên: AI API latency SLO breach.
- Severity: High.
- SLI/SLO liên quan: `latency_p95_ms`, objective ≤ 3000 ms, target 99.5%.
- Điều kiện và thời gian duy trì: P95 của `response_sent.latency_ms` > 3000 ms trong 5 phút.
- Ảnh hưởng tới người dùng: Câu trả lời chậm, có thể timeout hoặc bỏ dở phiên chat.
- Ba bước kiểm tra đầu tiên:
  1. Xác nhận P95/P99 và time range trên dashboard, so sánh với traffic cùng thời điểm.
  2. Mở một trace chậm trong Langfuse, xác định span có thời gian bất thường.
  3. Tìm log bằng `correlation_id` của trace để xác nhận feature, incident và lỗi liên quan.
- Mitigation tạm thời: Tắt incident hoặc giảm tải/giảm concurrency; nếu span retrieval chậm, dùng cache hoặc giới hạn số tài liệu trả về.
- Owner: Trần Bảo Phúc.

## Alert 2

- Tên: AI API error-rate SLO breach.
- Severity: Critical.
- SLI/SLO liên quan: `error_rate_pct`, objective ≤ 2%, target 99.0%.
- Điều kiện và thời gian duy trì: `request_failed / request_received * 100` > 2% trong 5 phút.
- Ảnh hưởng tới người dùng: Người dùng nhận lỗi 500 hoặc không nhận được câu trả lời.
- Ba bước kiểm tra đầu tiên:
  1. Xem error-rate và breakdown `error_type` theo time range bị cảnh báo.
  2. Mở trace và log của một request failed bằng `correlation_id`.
  3. Kiểm tra trạng thái incident, dependency/tracing và thay đổi cấu hình mới nhất.
- Mitigation tạm thời: Disable incident đang gây lỗi, rollback cấu hình/prompt mới hoặc chuyển sang local fallback khi dependency ngoài lỗi.
- Owner: Trần Bảo Phúc.

## Alert 3

- Tên: AI answer quality degradation.
- Severity: Medium.
- SLI/SLO liên quan: `quality_score_avg`, objective ≥ 0.75, target 95.0%.
- Điều kiện và thời gian duy trì: Trung bình `response_sent.quality_score` < 0.75 trong 15 phút.
- Ảnh hưởng tới người dùng: Câu trả lời ít liên quan, thiếu căn cứ hoặc không hoàn thành yêu cầu.
- Ba bước kiểm tra đầu tiên:
  1. Xác nhận quality proxy giảm trong khi traffic và error rate ổn định.
  2. So sánh trace dùng prompt label/version hiện tại với baseline.
  3. Kiểm tra `doc_count`, retrieval span và sample answer đã được redact trong log.
- Mitigation tạm thời: Rollback label `production` về prompt baseline, hoặc giới hạn feature bị ảnh hưởng trong khi đánh giá retrieval.
- Owner: Trần Bảo Phúc.
