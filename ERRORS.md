# ERRORS.md - Automatic Error Tracking & Learning

## [2026-05-11 17:42] - JSON Structured Output Newline Formatting Collapse

- **Type**: Process / Logic
- **Severity**: High
- **File**: `scripts/generator.py:189`
- **Agent**: Javis
- **Root Cause**: The Gemini-3-Flash-Preview model returned JSON string content for the blog body where newlines were either double-escaped (producing literal `\\n` strings in the parsed output) or entirely stripped, leading to collapsed paragraphs on line 51 of the blog posts.
- **Error Message**: 
  ```
  Double-escaped newlines: content.replace('\\n', '\n')
  Empty/collapsed newlines: content.count('\n') < 10
  ```
- **Fix Applied**:
  1. Manually healed `src/data/blog/ko/posts/260511_agentops-autonomy-or-black-box.md` by replacing raw `\\n` with actual newlines.
  2. Restructured `src/data/blog/ko/posts/260511_ebpf-linux-kernel-semantic-gap.md` using a Gemini-based structure-aware reconstructor mapped against the healthy English version.
  3. Integrated an automatic Self-Healing Pipeline into `scripts/generator.py` that checks for literal `\\n` strings or collapsed content (newline count < 10) and automatically resolves or reconstructs layout structure using Gemini-2.5-flash.
- **Prevention**: Incorporate the Self-Healing Pipeline directly in the Multi-Agent orchestrator immediately after parsing the LLM's structured JSON output to catch formatting anomalies before saving to disk.
- **Status**: Fixed

---
