# Quickstart: Phase III - Todo AI Chatbot

## Setup

1. **Environment Variables**:
   Add the following to `.env`:
   ```env
   OPENAI_API_KEY=sk-...
   CHATKIT_WORKFLOW_ID=wf_...
   BETTER_AUTH_SECRET=your_secret
   DATABASE_URL=postgresql://...
   ```

2. **Backend**:
   ```bash
   cd backend
   pip install fastapi openai-agents-python mcp-sdk-python sqlmodel pyjwt
   python -m src.main
   ```

3. **Frontend**:
   ```bash
   cd frontend
   npm install @openai/chatkit-react
   npm run dev
   ```

## Key Endpoints

- `POST /api/chatkit/session`: Initializes the AI session and returns a client secret for ChatKit.
- `POST /api/chat`: (Optional) Direct endpoint for chat without ChatKit UI.

## Testing the AI
1. Login via frontend.
2. Open the ChatWidget.
3. Type: "Add a task to prepare the demo for Friday".
4. Check the task list to see the update.
