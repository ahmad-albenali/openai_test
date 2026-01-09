# Plan

## Save Gemini responses to database
- Extend database schema to support Gemini response format
- Add `provider` column to distinguish between OpenAI/Gemini responses
- Implement `save_gemini_response()` in db.py

## Add Claude and Grok APIs
- Add `anthropic` package for Claude
- Add Grok API client (xAI)
- Create `send_claude_hello()` and `send_grok_hello()` functions
- Extend database schema for Claude and Grok response formats

## Enable model selection
- Add CLI argument to select provider (openai, gemini, claude, grok)
- Add CLI argument to select specific model within provider
- Default to a sensible model per provider

## Enable customized inputs
- Accept user input via CLI argument or interactive prompt
- Replace hardcoded "Hello, world!" with user-provided input
- Support multi-turn conversations (future)
