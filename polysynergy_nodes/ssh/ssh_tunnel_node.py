import io
import select
import socket
import threading

import paramiko

from polysynergy_node_runner.setup_context.dock_property import dock_property
from polysynergy_node_runner.setup_context.service_node import ServiceNode
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings

from polysynergy_nodes.ssh.ssh_tunnel_instance import SshTunnelInstance


@node(
    name="SSH Tunnel",
    category="ssh",
    icon="ssh.svg",
    version=1.0
)
class SshTunnelNode(ServiceNode):
    """
    SSH Tunnel service node for port-forwarding over an SSH connection.

    Establishes an SSH tunnel to a remote host and exposes a local endpoint
    that other nodes (e.g. MongoDB, SQL connections) can use to reach services
    on the remote network.

    **Authentication:**
    Provide either a password or a private key (PEM/OpenSSH format). If both
    are supplied the private key takes precedence.
    """

    ssh_host: str = NodeVariableSettings(
        label="SSH Host",
        dock=dock_property(placeholder="bastion.example.com"),
        has_in=True,
        required=True,
        info="Hostname or IP address of the SSH server"
    )

    ssh_port: int = NodeVariableSettings(
        label="SSH Port",
        dock=True,
        has_in=True,
        default=22,
        info="SSH server port (default: 22)"
    )

    ssh_username: str = NodeVariableSettings(
        label="SSH Username",
        dock=dock_property(placeholder="ec2-user"),
        has_in=True,
        required=True,
        info="Username for SSH authentication"
    )

    ssh_password: str = NodeVariableSettings(
        label="SSH Password",
        dock=dock_property(secret=True),
        has_in=True,
        required=False,
        info="SSH password (leave empty when using private key authentication)"
    )

    ssh_private_key: str = NodeVariableSettings(
        label="SSH Private Key",
        dock=dock_property(secret=True, text_area=True),
        has_in=True,
        required=False,
        info="PEM/OpenSSH private key content for key-based authentication"
    )

    remote_host: str = NodeVariableSettings(
        label="Remote Host",
        dock=dock_property(placeholder="127.0.0.1"),
        has_in=True,
        required=True,
        default="127.0.0.1",
        info="Host to forward to on the remote side of the tunnel (relative to the SSH server)"
    )

    remote_port: int = NodeVariableSettings(
        label="Remote Port",
        dock=True,
        has_in=True,
        required=True,
        info="Port to forward to on the remote side of the tunnel (e.g. 27017 for MongoDB)"
    )

    instance: SshTunnelInstance | None = NodeVariableSettings(
        label="Tunnel Instance",
        has_out=True,
        info="SSH tunnel instance exposing local_host and local_port for downstream nodes"
    )

    async def provide_instance(self) -> SshTunnelInstance:
        """Open the SSH tunnel using paramiko and return a SshTunnelInstance."""
        ssh_port = int(self.ssh_port or 22)
        remote_host = self.remote_host or "127.0.0.1"
        remote_port = int(self.remote_port or 27017)

        # Set up SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        connect_kwargs = {
            "hostname": self.ssh_host,
            "port": ssh_port,
            "username": self.ssh_username,
        }

        if self.ssh_private_key:
            pkey = paramiko.RSAKey.from_private_key(io.StringIO(self.ssh_private_key))
            connect_kwargs["pkey"] = pkey
        elif self.ssh_password:
            connect_kwargs["password"] = self.ssh_password

        client.connect(**connect_kwargs)

        # Get a transport and request port forwarding
        transport = client.get_transport()

        # Bind a local socket to a random port
        local_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        local_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        local_server.bind(("127.0.0.1", 0))
        local_server.listen(5)
        local_port = local_server.getsockname()[1]

        # Forward connections in a background thread
        def forward_tunnel():
            while True:
                try:
                    local_conn, _ = local_server.accept()
                except OSError:
                    break
                try:
                    channel = transport.open_channel(
                        "direct-tcpip",
                        (remote_host, remote_port),
                        local_conn.getpeername(),
                    )
                except Exception:
                    local_conn.close()
                    continue

                if channel is None:
                    local_conn.close()
                    continue

                # Shuttle data between local_conn and channel using select
                def shuttle(sock, chan):
                    try:
                        while True:
                            r, _, _ = select.select([sock, chan], [], [], 60)
                            if chan in r:
                                data = chan.recv(4096)
                                if not data:
                                    break
                                sock.sendall(data)
                            if sock in r:
                                data = sock.recv(4096)
                                if not data:
                                    break
                                chan.sendall(data)
                    except Exception:
                        pass
                    finally:
                        chan.close()
                        sock.close()

                threading.Thread(target=shuttle, args=(local_conn, channel), daemon=True).start()

        tunnel_thread = threading.Thread(target=forward_tunnel, daemon=True)
        tunnel_thread.start()

        print(f"[SSHTunnel] Tunnel open: 127.0.0.1:{local_port} -> {remote_host}:{remote_port} via {self.ssh_host}:{ssh_port}")

        self.instance = SshTunnelInstance(
            local_host="127.0.0.1",
            local_port=local_port,
            tunnel=client,
        )

        return self.instance
