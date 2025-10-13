from typing import Any
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.node_error import NodeError


@node(name="Confirm / Reject", category="human_in_loop", version=1.0)
class ConfirmReject(Node):
    """
    Human-in-the-Loop node that pauses flow execution until user confirms or rejects.

    Flow pattern:
    1. First execution: sends action (email/event) and stops flow (true_path remains None)
    2. User responds via API which updates user_response in DynamoDB
    3. Resume execution: reads user_response and continues via true_path or false_path
    """

    message: str = NodeVariableSettings(
        label="Message",
        dock=True,
        has_in=True,
        info="Message to display to user for confirmation"
    )

    user_response: str | None = NodeVariableSettings(
        label="User Response",
        dock=False,  # Not shown in dock, set programmatically
        has_in=False,
        has_out=True,
        info="User's response (confirm/reject) - populated during resume"
    )

    request_id: str | None = NodeVariableSettings(
        label="Request ID",
        dock=False,
        has_out=True,
        info="Unique ID for this confirmation request"
    )

    true_path: Any = PathSettings(
        label="Confirmed",
        info="Path taken when user confirms"
    )

    false_path: Any = PathSettings(
        label="Rejected",
        info="Path taken when user rejects"
    )

    async def execute(self):
        try:
            # Check if we're resuming with user response
            if self.user_response:
                # RESUME PATH: We have user response, continue flow
                if self.user_response.lower() in ['yes', 'confirm', 'approved', 'true']:
                    self.true_path = True
                    self.false_path = False
                else:
                    self.true_path = False
                    self.false_path = True
                return

            # FIRST EXECUTION PATH: No user response yet
            # Generate unique request ID
            import uuid
            self.request_id = f"confirm_{uuid.uuid4()}"

            # TODO: Send action (email/redis event) here
            # For now, just log
            print(f"[HIL] Confirmation requested: {self.message}")
            print(f"[HIL] Request ID: {self.request_id}")
            print(f"[HIL] Flow will pause here until user responds")

            # DO NOT set true_path or false_path
            # This causes connections to become killers and flow stops
            # Lambda will exit normally after this

        except Exception as e:
            self.true_path = False
            self.false_path = NodeError.format(str(e))
