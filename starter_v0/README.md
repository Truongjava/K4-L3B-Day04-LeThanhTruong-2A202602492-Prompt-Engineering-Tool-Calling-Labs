# Starter v0 — IT Helpdesk Agent Lab

## Cài đặt nhanh

```powershell
cd starter_v0
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Điền AIBOX_AUTH_TOKEN (hoặc provider key khác) vào .env
```

## Chạy các chế độ

### 1. Chat interactive
```powershell
python chat.py --provider ai-box --version v1
```

### 2. Eval tự động
```powershell
python run_eval.py --provider ai-box --version v1 --suite base --eval-cases data/eval_base.json
python run_eval.py --provider ai-box --version v1 --suite group --eval-cases data/eval_group.json
python run_eval.py --provider ai-box --version v1 --suite adversarial --eval-cases data/eval_adversarial.json
python run_eval.py --provider ai-box --version v1 --suite extension --eval-cases data/eval_helpdesk_extension.json
```

### 3. Preflight smoke test
```powershell
python scripts/preflight_provider.py --provider ai-box
```

## Cấu trúc thư mục

```
starter_v0/
├── agent.py                  # Core agent loop: LLM → tool calls → execute
├── chat.py                   # Interactive CLI chat với transcript logging
├── run_eval.py               # Tự động chạy eval, chấm điểm routing + args
├── env_loader.py             # Nạp biến môi trường từ .env
├── versioning.py             # SHA256 hash tracking cho artifacts
│
├── providers/                # Adapter cho từng LLM backend
│   ├── ai_box_provider.py    # AI Box endpoint (requests-based)
│   ├── openai_provider.py    # OpenAI Chat Completions
│   ├── anthropic_provider.py # Anthropic Messages API
│   ├── openrouter_provider.py# OpenRouter (OpenAI-compatible)
│   └── gemini_provider.py    # Google Gemini SDK
│
├── tools/                    # 9 công cụ helpdesk
│   ├── clarify/              # Hỏi lại khi thiếu thông tin
│   ├── check_service_status/ # Trạng thái dịch vụ
│   ├── inspect_device/       # Diagnostic thiết bị
│   ├── lookup_user/          # Employee directory
│   ├── create_ticket/        # Tạo ticket (có guard credential)
│   ├── format_incident_report/ # Format findings thành báo cáo
│   ├── search_kb/            # Knowledge base search
│   ├── policy/               # Company policy search
│   └── search_device_info/   # External device research (Tavily)
│
├── artifacts/                # Prompt & tool declarations
│   ├── system_prompt.md      # ← Cải thiện qua các versions
│   ├── tools.yaml            # Tool declarations schema
│   ├── REPORT.md             # Báo cáo hoàn chỉnh
│   └── version_log.csv       # Log thay đổi qua versions
│
├── helpdesk_data/            # Dữ liệu giả lập
│   ├── users.json            # 10 nhân viên
│   ├── assets.json           # 9 thiết bị
│   ├── service_status.json   # Trạng thái dịch vụ
│   ├── knowledge_base/       # 11 articles hướng dẫn
│   └── company_policy/       # 6 policies nội bộ
│
├── data/                     # Eval datasets
│   ├── eval_base.json        # 30 cases cố định (không sửa)
│   ├── eval_adversarial.json # 12 red-team cases
│   ├── eval_group.json       # 10 cases nhóm tự viết ← đây
│   └── eval_helpdesk_extension.json # Extension tham khảo
│
├── runs/                     # Kết quả eval JSON files (commit evidence)
├── transcripts/              # Chat transcript logs (commit evidence)
├── tickets/                  # Created tickets (gitignore'd)
└── scripts/                  # Utility scripts
    ├── preflight_provider.py # Smoke test connectivity
    └── parse_runs.py         # Parse run JSON output
```

## Provider hỗ trợ

| Provider | `--provider` | Env var Key | Model default |
|---|---|---|---|
| **AI Box** | `ai-box` | `AIBOX_AUTH_TOKEN` | `qwen3.7-flash` |
| OpenRouter | `openrouter` | `OPENROUTER_API_KEY` | `gpt-4o-mini` |
| OpenAI | `openai` | `OPENAI_API_KEY` | `gpt-4o-mini` |
| Anthropic | `anthropic` | `ANTHROPIC_API_KEY` | `claude-haiku-4-5-20251001` |
| Google Gemini | `gemini` | `GEMINI_API_KEY` | `gemini-3.5-flash` |

## Đánh giá

Eval scoring dựa trên:
- **routing_correct**: Model có gọi đúng tool không?
- **args_correct**: Args của tool call có khớp expected không?
- **case_accuracy**: Tổng % case PASS
- **multiturn_accuracy**: Chỉ áp dụng cho multi-turn cases

Run dùng làm evidence cần `provider_error_cases == 0`.
