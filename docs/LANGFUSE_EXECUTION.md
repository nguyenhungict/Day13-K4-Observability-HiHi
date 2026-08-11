# Runbook Langfuse: trace và prompt versioning

Tài liệu này là checklist thao tác để tạo evidence thật trên Langfuse. Không ghi
giả `prompt_version` trong code và không commit `.env` hoặc key.

## 1. Cấu hình cục bộ

Tạo `.env` từ `.env.example`, sau đó điền key của project Langfuse được Lab
Coach cung cấp:

```dotenv
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
LANGFUSE_PROMPT_NAME=day13-chat
LANGFUSE_PROMPT_LABEL=production
```

Khởi động API bằng môi trường này:

```bash
source .venv/bin/activate
uvicorn app.main:app --reload --env-file .env
```

Không có key, app vẫn chạy nhưng trace sẽ dùng `prompt_source=local` hoặc
`local-fallback`; trạng thái này không thay thế evidence prompt managed.

## 2. Tạo hai prompt version trên Langfuse

Tạo text prompt tên `day13-chat`. Cả hai version phải có đúng ba biến:

```text
Feature={{feature}}
Docs={{docs}}
Question={{message}}
```

1. Lưu version 1, gắn labels `baseline` và `production`.
2. Tạo version 2 với thay đổi nhỏ, chẳng hạn thêm yêu cầu trả lời ngắn gọn;
   gắn label `candidate`.
3. Chụp danh sách hai version vào
   `submission/evidence/prompt-versions.png`.

## 3. Tạo trace có metadata đúng

Với API vẫn đang chạy, đặt `LANGFUSE_PROMPT_LABEL=baseline` trong `.env`, khởi
động lại API và chạy:

```bash
python scripts/load_test.py --concurrency 5
```

Lặp lại với `LANGFUSE_PROMPT_LABEL=candidate`. Mở một trace cho mỗi lượt và
kiểm tra trace metadata có:

- `prompt_name=day13-chat`
- `prompt_label=baseline` hoặc `candidate`
- `prompt_version=<version thật trên Langfuse>`

Lưu một ảnh trace waterfall tại
`submission/evidence/trace-waterfall.png`; lưu hai trace ID vào report. Mười
request từ load test thỏa yêu cầu tối thiểu 10 traces nếu Langfuse đã kết nối.

## 4. Chuyển label và rollback

1. Trên Langfuse, chuyển label `production` sang version 2.
2. Khởi động lại API với `LANGFUSE_PROMPT_LABEL=production`, gửi một request và
   chụp trace chứng minh version 2.
3. Chuyển `production` về version 1, gửi thêm một request và chụp màn hình
   trước/sau tại `submission/evidence/prompt-rollback.png`.

## 5. Kiểm tra trước khi bàn giao

- Có ít nhất 10 trace và một waterfall có thể mở được.
- Hai trace baseline/candidate có label/version khác nhau.
- Không có trace nào dùng `local` hoặc `local-fallback` làm bằng chứng managed.
- Cập nhật tên prompt, label, version, trace ID và các đường dẫn ảnh vào
  `submission/REPORT.md`.
