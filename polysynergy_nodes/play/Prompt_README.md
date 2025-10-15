# 💬 Prompt Node

The `Prompt` node captures user prompts with associated files, session, and user context. Designed for AI agent interactions and chat-based workflows.

---

## 📂 Category

**flow**

---

## ⚙️ Inputs

| Name     | Type       | Required | Description                              |
|----------|------------|----------|------------------------------------------|
| name     | str        | ❌        | Name for this prompt node                |
| prompt   | str        | ❌        | The prompt text (rich text supported)    |
| files    | list       | ❌        | File URLs/paths (images, audio, video, docs) |
| session  | dict       | ❌        | Session data associated with prompt      |
| user     | list       | ❌        | List of user IDs associated              |

---

## 🔌 Outputs

| Name           | Type   | Description                              |
|----------------|--------|------------------------------------------|
| prompt         | str    | The prompt text (pass-through)           |
| active_session | str    | Currently selected session ID            |
| active_user    | str    | Currently selected user ID               |

---

## 🎯 Purpose

The Prompt node serves as a **data collection point** for:
- User input text (prompts)
- Associated files (multimodal input)
- Session management
- User context tracking

It's a **passive node** that doesn't execute logic but organizes input for downstream processing.

---

## ✅ Example Usage

### Simple Text Prompt:
```json
{
  "name": "User Query",
  "prompt": "What's the weather like today?"
}
```

### Prompt with Image:
```json
{
  "name": "Image Analysis",
  "prompt": "Describe this image in detail",
  "files": ["https://example.com/photo.jpg"]
}
```

### Prompt with Session:
```json
{
  "name": "Chat Message",
  "prompt": "Continue our previous conversation",
  "session": {
    "session_id": "sess_123",
    "tenant_id": "tenant_456"
  },
  "user": ["user_789"]
}
```

---

## 🔄 Common Patterns

### Agent Interaction:
```
Prompt → Agent (uses prompt + files) → Response
```

### Multi-turn Conversation:
```
Prompt (with session) → Agent → Store Response → Next Prompt
```

### Multimodal Processing:
```
Prompt (text + images) → Vision Agent → Analysis
```

### User Context Tracking:
```
Prompt (with user list) → Process → Track Activity
```

---

## 📎 File Support

The `files` parameter supports various file types:
- **Images**: JPG, PNG, GIF, WebP
- **Audio**: MP3, WAV, M4A
- **Video**: MP4, MOV, AVI
- **Documents**: PDF, DOCX, TXT

Files can be:
- URLs (`https://...`)
- S3 paths (`s3://...`)
- Local file paths

---

## 👥 Session & User Management

### Session Structure:
```json
{
  "session_id": "unique_session_id",
  "tenant_id": "tenant_identifier",
  "metadata": {...}
}
```

### User Tracking:
```json
{
  "user": ["user_id_1", "user_id_2"]
}
```

Multiple users can be associated for shared prompts.

---

## 💡 Use Cases

- **Chatbots**: Capture user messages with context
- **AI Agents**: Provide prompts to intelligent agents
- **Multimodal AI**: Combine text and file inputs
- **Conversational Flows**: Maintain session continuity
- **User Analytics**: Track prompt patterns by user

---

## ⚠️ Notes

- **No Execution Logic**: This node doesn't process data, only stores it
- **Pass-through**: Prompt text is available as both input and output
- **Rich Text**: Supports rich text formatting in prompt field
- **Cannot be Disabled**: Node has `has_enabled_switch=False`
- **Integration Point**: Designed to work with Agent nodes
