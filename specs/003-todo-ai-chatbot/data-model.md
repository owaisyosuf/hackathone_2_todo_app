# Data Model: Phase III - Todo AI Chatbot

## Entities

### User (Existing)
*Extended from Phase II*
- `id`: UUID (Primary Key)
- `email`: String (Unique)

### Task (Existing)
*Extended from Phase II*
- `id`: UUID (Primary Key)
- `user_id`: UUID (Foreign Key -> User.id)
- `title`: String
- `description`: String (Optional)
- `completed`: Boolean (Default: False)
- `created_at`: DateTime
- `updated_at`: DateTime

### Conversation
*New in Phase III*
- `id`: UUID (Primary Key)
- `user_id`: UUID (Foreign Key -> User.id)
- `created_at`: DateTime
- `updated_at`: DateTime

### Message
*New in Phase III*
- `id`: UUID (Primary Key)
- `conversation_id`: UUID (Foreign Key -> Conversation.id)
- `role`: String (Enum: "user", "assistant", "system", "tool")
- `content`: Text
- `tool_call_id`: String (Optional, for tool-related messages)
- `created_at`: DateTime

## Relationships
- **User (1) <-> (*) Task**: A user owns multiple tasks.
- **User (1) <-> (*) Conversation**: A user can have multiple chat sessions.
- **Conversation (1) <-> (*) Message**: A conversation consists of an ordered sequence of messages.

## Validation Rules
- `Task.title`: Minimum 1 character, Maximum 255.
- `Message.role`: Must be one of the defined roles.
- `Conversation.user_id`: Must match the authenticated user context.
