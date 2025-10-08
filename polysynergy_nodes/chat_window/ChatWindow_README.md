# ChatWindow Node

The ChatWindow node serves as the entry point for chat window flows. This is a system node that is automatically placed when a chat window is created.

## Purpose

This node provides user context and permissions to the chat window flow, allowing the flow to adapt based on:
- Who the user is (identity)
- What permissions they have (view/edit capabilities)

## Output Variables

### User Identity
- **user_id**: The unique identifier of the user
- **user_email**: The user's email address
- **user_name**: The user's full name

### User Permissions
- **can_view_flow**: Whether the user can see the flow editor (boolean)
- **can_edit_flow**: Whether the user can edit the flow (boolean)
- **can_view_output**: Whether the user can see execution outputs (boolean)
- **show_response_transparency**: Whether the user can see AI reasoning steps (boolean)

## Usage

This node is automatically added to every chat window flow. You cannot manually add or remove it. Use its output variables to:

1. **Personalize responses** - Use user_name to address the user personally
2. **Conditional logic** - Show different content based on permissions
3. **Logging/Analytics** - Track which users interact with the chat
4. **Access control** - Restrict certain actions based on permissions

## Example

```
ChatWindow node outputs:
- user_id: "123e4567-e89b-12d3-a456-426614174000"
- user_email: "john@example.com"
- user_name: "John Doe"
- can_view_flow: true
- can_edit_flow: false
- can_view_output: true
- show_response_transparency: false

You can use these in your flow to customize behavior:
- Greet: "Hello, {{user_name}}!"
- Conditional: If can_edit_flow == false, hide advanced options
```

## Notes

- This node is system-managed and cannot be deleted
- It's similar to Route and Schedule entrypoint nodes
- User permissions are configured via the Chat Window settings in the portal
