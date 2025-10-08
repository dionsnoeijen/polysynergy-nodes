# MockChatWindow Node

The MockChatWindow node is used for testing chat window flows without requiring actual user authentication or a deployed chat interface.

## Purpose

This mock node simulates the ChatWindow entrypoint node, allowing developers to:
- Test chat window flows locally
- Simulate different user identities and permissions
- Debug flow logic before deployment
- Test permission-based conditional logic

## Output Variables

### User Identity (Configurable for Testing)
- **user_id**: Mock user ID (default: "test-user-123")
- **user_email**: Mock user email (default: "test@example.com")
- **user_name**: Mock user name (default: "Test User")

### User Permissions (Configurable for Testing)
- **can_view_flow**: Whether the mock user can view the flow (default: true)
- **can_edit_flow**: Whether the mock user can edit the flow (default: false)
- **can_view_output**: Whether the mock user can view outputs (default: true)
- **show_response_transparency**: Whether to show AI reasoning (default: true)

## Usage

This node is automatically placed when you create a chat window. It allows you to:

1. **Test with different users** - Change the user_id, email, and name to simulate different users
2. **Test permission logic** - Toggle the permission checkboxes to test how your flow behaves with different access levels
3. **Use the Play button** - Click the play button to execute the flow with your mock configuration

## Example Test Scenarios

### Scenario 1: Limited User
- Set `can_view_flow` = false
- Set `can_edit_flow` = false
- Set `can_view_output` = false
- Test that your flow properly restricts information

### Scenario 2: Admin User
- Set all permissions to true
- Test that advanced features are available

### Scenario 3: Different User Identity
- Change `user_email` to "admin@company.com"
- Test user-specific logic or personalization

## Notes

- This is a system node automatically placed with every chat window
- It cannot be deleted
- In production, the real ChatWindow node will be used with actual user data
- The mock node is only for local testing via the play button
