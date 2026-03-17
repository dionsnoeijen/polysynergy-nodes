"""SSH Tunnel instance dataclass for holding tunnel state."""

from dataclasses import dataclass


@dataclass
class SshTunnelInstance:
    """Holds the active SSH tunnel forwarder and local endpoint details.

    Attributes:
        local_host: The local bind address of the tunnel (typically '127.0.0.1').
        local_port: The local port the tunnel is listening on.
        tunnel: The underlying SSHTunnelForwarder instance.
    """

    local_host: str
    local_port: int
    tunnel: object  # sshtunnel.SSHTunnelForwarder
