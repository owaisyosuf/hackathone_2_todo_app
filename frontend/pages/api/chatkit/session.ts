import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ detail: 'Method not allowed' });
  }

  // 1. Authenticate user (assuming JWT in cookies or state)
  // For basic phase III, we'll proxy the request to OpenAI ChatKit Sessions API

  const apiKey = process.env.OPENAI_API_KEY;
  const workflowId = process.env.CHATKIT_WORKFLOW_ID;

  if (!apiKey || !workflowId) {
    return res.status(500).json({ detail: 'OpenAI configuration missing' });
  }

  try {
    const response = await fetch('https://api.openai.com/v1/chatkit/sessions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        'OpenAI-Beta': 'chatkit_beta=v1',
      },
      body: JSON.stringify({
        workflow: { id: workflowId },
        // user: req.body.userId || 'anonymous-user', // Optional: ID for persistence
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      return res.status(response.status).json(errorData);
    }

    const data = await response.json();
    return res.status(200).json({
      client_secret: data.client_secret,
      session_id: data.id
    });
  } catch (error) {
    console.error('ChatKit Session Error:', error);
    return res.status(500).json({ detail: 'Failed to create ChatKit session' });
  }
}
