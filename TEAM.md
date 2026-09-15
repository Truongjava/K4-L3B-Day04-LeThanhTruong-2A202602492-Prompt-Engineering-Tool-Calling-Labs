# TEAM — Day04, K4-L3B

**Làm nhóm.** Mỗi người tự viết và commit phần INDIVIDUAL của mình.

## Thông tin bài nộp

- Tên nhóm: LeThanhTruong
- Người đại diện / MSSV: Lê Thanh Trường — 2A202602492
- Tên repo: `K4-L3-DAY04-LeThanhTruong-2A202602492-PromptEngineeringToolCalling`
- URL repo, nhánh nộp, commit chốt: _(chờ điền khi push lên GitHub)_
- Deadline áp dụng và link thông báo đổi hạn nếu có: Không

## Thành viên

| Họ và tên | MSSV | GitHub | Vai trò và công việc | File/commit/PR |
|---|---|---|---|---|
| Lê Thanh Trường | 2A202602492 | _(chờ điền)_ | Setup env, chạy eval v0/v1, cải thiện system_prompt, phân tích failure patterns, viết REPORT.md | Các file trong `starter_v0/artifacts/`, `starter_v0/providers/ai_box_provider.py` |

## Nhận xét chung

- Kết quả và bằng chứng: Base accuracy tăng dần 73.3% (v0) → 76.7% (v1) → 80.0% (v2) → **90.0% (v3)**. Extension 60% → 80%. Group 60%. Adversarial 41.7%. Evidence đầy đủ trong `runs/*.json`.
- Thay đổi hiệu quả nhất: (1) v1 thêm 9 sections vào system prompt giúp fix H12/H17/H19. (2) v2 cải thiện descriptions trong tools.yaml fix H10/H13 sai args. (3) v3 nhấn mạnh refuse/cancel không gọi tool + map check_type fix H16/M07/M09, đưa base lên 90%.
- Giới hạn còn lại: Model nhỏ qwen3.7-flash vẫn gọi `clarify` thay vì trả lời trực tiếp cho out_of_scope (H08/H14) và meta (H09). Adversarial 41.7% — prompt injection/role spoofing vẫn là thách thức.
- Cách phân công và tích hợp: Một người thực hiện toàn bộ pipeline từ setup → eval → analysis → report trong session này.

## INDIVIDUAL

Sao chép mục này cho từng thành viên.

### Lê Thanh Trường — 2A202602492

- Phần việc và file/commit/PR: Cài đặt môi trường virtualenv + pip; Tạo provider adapter AI Box (`providers/ai_box_provider.py`); Chạy preflight + baseline eval v0; Cải thiện qua 3 vòng v1/v2/v3 (system_prompt.md + tools.yaml); Viết 10 group eval cases; Chạy đầy đủ 4 suite (base/extension/adversarial/group); Hoàn thiện REPORT.md và version_log.csv. Files: `artifacts/system_prompt.md`, `artifacts/tools.yaml`, `providers/ai_box_provider.py`, `providers/__init__.py`, `data/eval_group.json`, `artifacts/REPORT.md`, `artifacts/version_log.csv`.
- Quyết định, khó khăn và cách xử lý: Chọn provider AI Box (qwen3.7-flash). Đối mặt OpenAI SDK v3 bị PermissionDeniedError → switch sang `requests` trực tiếp. Debug tool_choice format: API không hỗ trợ `"any"` → omit hẳn. Chia nhỏ cải thiện thành 3 giả thuyết riêng (prompt → tools → prompt tinh chỉnh) để có evidence so sánh rõ ràng qua từng version.
- Điều đã học: Prompt engineering cho tool calling hoạt động qua nhiều vòng lặp — routing table + confirmation boundary + check_type mapping lần lượt fix các nhóm lỗi khác nhau. Model nhỏ có xu hướng gọi clarify thay vì trả lời trực tiếp cho out-of-scope/meta, cần nhấn mạnh "when NOT to call any tool". Evidence định lượng (case_accuracy) quan trọng hơn nhận xét chủ quan.
- AI/công cụ đã dùng và cách kiểm tra: Claude Code để debug, phân tích JSON run files, so sánh metrics qua versions. Test curl trực tiếp đến API xác định root cause SDK incompatibility. Verify mọi run JSON với `provider_error_cases == 0` trước khi đưa vào evidence.
- Thời điểm đã tự nộp URL repo chung trên VLearn: _(chờ điền)_
