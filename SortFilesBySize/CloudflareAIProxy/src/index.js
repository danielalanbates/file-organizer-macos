export default {
  async fetch(request, env) {
    if (request.method !== 'POST') {
      return new Response(
        JSON.stringify({ error: 'Use POST with JSON body.' }),
        {
          status: 405,
          headers: { 'Content-Type': 'application/json' },
        },
      );
    }

    const authHeader = request.headers.get('Authorization') || '';
    const token = authHeader.replace(/^Bearer\s+/i, '').trim();
    if (!token || token !== env.FILEGENIUS_AI_TOKEN) {
      return new Response(JSON.stringify({ error: 'Unauthorized' }), {
        status: 401,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    let body;
    try {
      body = await request.json();
    } catch (err) {
      return new Response(JSON.stringify({ error: 'Invalid JSON body' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    const prompt = body?.prompt;
    if (!prompt || typeof prompt !== 'string') {
      return new Response(JSON.stringify({ error: 'Missing prompt string' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    const payload = {
      model: 'gpt-4o-mini',
      max_tokens: 700,
      messages: [
        {
          role: 'system',
          content:
            'You are a cautious macOS disk cleanup assistant helping a user decide what to delete or move.',
        },
        {
          role: 'user',
          content: prompt,
        },
      ],
    };

    const openaiResp = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${env.OPENAI_API_KEY}`,
      },
      body: JSON.stringify(payload),
    });

    if (!openaiResp.ok) {
      const text = await openaiResp.text();
      return new Response(JSON.stringify({ error: 'OpenAI error', detail: text }), {
        status: 502,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    const data = await openaiResp.json();
    const content = data?.choices?.[0]?.message?.content || '';

    return new Response(JSON.stringify({ content }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  },
};
