# FileGenius AI Proxy (Cloudflare Worker)

This Worker lets FileGenius call OpenAI without distributing the raw API key. FileGenius sends the cleanup prompt to the Worker, and the Worker authenticates, calls OpenAI, and returns the response.

## Prerequisites
1. [Install Wrangler](https://developers.cloudflare.com/workers/wrangler/install-and-update/)
2. Log in: `wrangler login`
3. Have an OpenAI API key with access to `gpt-4o-mini` (or adjust the model in `src/index.js`).

## Configure
```bash
cd CloudflareAIProxy
wrangler secret put OPENAI_API_KEY
wrangler secret put FILEGENIUS_AI_TOKEN   # choose any strong string; must match client env
```

## Deploy
```bash
wrangler deploy
```
Wrangler will output a URL such as `https://filegenius-ai-proxy.<subdomain>.workers.dev`. Use that in FileGenius.

## FileGenius configuration
Set these on the client machine (env vars or `.env` next to `filegenius.py`):
```
FILEGENIUS_AI_PROVIDER=proxy
FILEGENIUS_AI_ENDPOINT=https://filegenius-ai-proxy.<subdomain>.workers.dev
FILEGENIUS_AI_TOKEN=<same token you stored as secret>
```
Restart FileGenius—AI suggestions will now route through the Worker.

## Testing
You can curl the Worker directly:
```bash
curl -X POST \
  -H "Authorization: Bearer $FILEGENIUS_AI_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Summarize the benefits of FileGenius"}' \
  https://filegenius-ai-proxy.<subdomain>.workers.dev
```
You should receive `{ "content": "..." }` with the AI response.
