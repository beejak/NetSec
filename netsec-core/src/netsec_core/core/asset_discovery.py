"""Asset Discovery implementation."""

from typing import List, Dict, Any, Optional
from datetime import datetime
from collections import defaultdict
import socket
import subprocess
import platform
from concurrent.futures import ThreadPoolExecutor, as_completed


class AssetDiscovery:
    """Asset Discovery for network asset identification."""

    def __init__(self):
        """Initialize Asset Discovery."""
        self.max_workers = 50

    def discover_network(
        self,
        network: str,
        ports: Optional[List[int]] = None,
    ) -> Dict[str, Any]:
        """
        Discover assets on a network.

        Args:
            network: Network CIDR (e.g., "192.168.1.0/24") or IP range
            ports: Ports to scan for service detection

        Returns:
            Dictionary containing discovered assets
        """
        if ports is None:
            ports = [22, 80, 443, 3389, 5900]  # Common ports

        assets = []
        network_hosts = self._parse_network(network)

        # Scan hosts in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_host = {
                executor.submit(self._discover_host, host, ports): host
                for host in network_hosts
            }

            for future in as_completed(future_to_host):
                host = future_to_host[future]
                try:
                    asset = future.result()
                    if asset:
                        assets.append(asset)
                except Exception:
                    pass

        return {
            "network": network,
            "assets_discovered": len(assets),
            "assets": assets,
            "timestamp": datetime.utcnow().isoformat(),
        }

    def _parse_network(self, network: str) -> List[str]:
        """Parse network CIDR or range into list of IPs."""
        hosts = []

        try:
            # Handle CIDR notation (simplified)
            if "/" in network:
                # For now, just return the network address
                # Full CIDR parsing would require ipaddress module
                base_ip = network.split("/")[0]
                # Simple /24 network
                if network.endswith("/24"):
                    base = ".".join(base_ip.split(".")[:-1])
                    hosts = [f"{base}.{i}" for i in range(1, 255)]
                else:
                    hosts = [base_ip]
            elif "-" in network:
                # IP range (e.g., 192.168.1.1-192.168.1.10)
                start, end = network.split("-")
                start_parts = start.split(".")
                end_parts = end.split(".")
                # Simple range (same subnet)
                if start_parts[:3] == end_parts[:3]:
                    start_last = int(start_parts[3])
                    end_last = int(end_parts[3])
                    base = ".".join(start_parts[:3])
                    hosts = [f"{base}.{i}" for i in range(start_last, end_last + 1)]
                else:
                    hosts = [start, end]
            else:
                # Single IP or hostname
                hosts = [network]

        except Exception:
            hosts = [network]

        return hosts

    def _discover_host(self, host: str, ports: List[int]) -> Optional[Dict[str, Any]]:
        """Discover information about a single host."""
        asset = {
            "ip": host,
            "hostname": None,
            "open_ports": [],
            "services": [],
            "os_fingerprint": None,
        }

        # Try to resolve hostname
        try:
            hostname = socket.gethostbyaddr(host)[0]
            asset["hostname"] = hostname
        except Exception:
            pass

        # Check if host is alive (ping)
        if not self._is_host_alive(host):
            return None

        # Scan ports
        for port in ports:
            if self._is_port_open(host, port):
                asset["open_ports"].append(port)
                service = self._detect_service(host, port)
                if service:
                    asset["services"].append({
                        "port": port,
                        "service": service,
                    })

        # Only return asset if it has open ports or hostname
        if asset["open_ports"] or asset["hostname"]:
            return asset

        return None

    def _is_host_alive(self, host: str) -> bool:
        """Check if host is alive (ping)."""
        try:
            # Use ping command (platform-specific)
            if platform.system().lower() == "windows":
                result = subprocess.run(
                    ["ping", "-n", "1", "-w", "1000", host],
                    capture_output=True,
                    timeout=2,
                )
            else:
                result = subprocess.run(
                    ["ping", "-c", "1", "-W", "1", host],
                    capture_output=True,
                    timeout=2,
                )
            return result.returncode == 0
        except Exception:
            # Fallback to port scan
            return self._is_port_open(host, 80) or self._is_port_open(host, 443)

    def _is_port_open(self, host: str, port: int, timeout: float = 1.0) -> bool:
        """Check if port is open."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except Exception:
            return False

    def _detect_service(self, host: str, port: int) -> Optional[str]:
        """Detect service on port."""
        # Common port mappings
        port_services = {
            22: "ssh",
            23: "telnet",
            25: "smtp",
            80: "http",
            443: "https",
            3389: "rdp",
            5900: "vnc",
        }
        return port_services.get(port)

    def generate_inventory(self, assets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate asset inventory report."""
        inventory = {
            "total_assets": len(assets),
            "assets_by_service": defaultdict(int),
            "assets_by_os": defaultdict(int),
            "total_open_ports": 0,
            "timestamp": datetime.utcnow().isoformat(),
        }

        for asset in assets:
            # Count services
            for service in asset.get("services", []):
                service_name = service.get("service", "unknown")
                inventory["assets_by_service"][service_name] += 1

            # Count OS
            if asset.get("os_fingerprint"):
                inventory["assets_by_os"][asset["os_fingerprint"]] += 1

            # Count ports
            inventory["total_open_ports"] += len(asset.get("open_ports", []))

        return inventory
