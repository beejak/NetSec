"""Traffic Analyzer implementation using scapy."""

from typing import List, Dict, Any, Optional
from datetime import datetime
from collections import defaultdict
import threading
import queue


try:
    from scapy.all import sniff, IP, TCP, UDP, DNS, HTTP, Raw
    from scapy.layers import http
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False


class TrafficAnalyzer:
    """Traffic Analyzer for packet capture and analysis."""

    def __init__(self):
        """Initialize Traffic Analyzer."""
        if not SCAPY_AVAILABLE:
            raise ImportError("scapy is required for traffic analysis. Install with: pip install scapy")
        self.capturing = False
        self.packets = []
        self.flows = defaultdict(lambda: {"packets": [], "bytes": 0, "start_time": None, "end_time": None})

    def capture_traffic(
        self,
        interface: Optional[str] = None,
        count: Optional[int] = None,
        timeout: Optional[int] = None,
        filter_str: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Capture network traffic.

        Args:
            interface: Network interface to capture on (None = default)
            count: Number of packets to capture (None = unlimited)
            timeout: Capture timeout in seconds (None = no timeout)
            filter_str: BPF filter string

        Returns:
            Dictionary containing capture statistics
        """
        if self.capturing:
            return {"error": "Already capturing traffic"}

        self.packets = []
        self.flows = defaultdict(lambda: {"packets": [], "bytes": 0, "start_time": None, "end_time": None})

        try:
            self.capturing = True

            def packet_handler(packet):
                """Handle captured packet."""
                if not self.capturing:
                    return False
                self.packets.append(packet)
                self._analyze_packet(packet)
                if count and len(self.packets) >= count:
                    return False
                return True

            # Start capture
            sniff(
                iface=interface,
                prn=packet_handler,
                stop_filter=lambda x: not self.capturing,
                timeout=timeout,
                filter=filter_str,
            )

            self.capturing = False

            return {
                "packets_captured": len(self.packets),
                "flows_detected": len(self.flows),
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            self.capturing = False
            return {"error": str(e)}

    def _analyze_packet(self, packet):
        """Analyze a single packet and update flow information."""
        try:
            if IP in packet:
                ip_layer = packet[IP]
                src_ip = ip_layer.src
                dst_ip = ip_layer.dst
                protocol = ip_layer.proto

                # Create flow key
                if TCP in packet:
                    tcp_layer = packet[TCP]
                    flow_key = (
                        min(src_ip, dst_ip),
                        max(src_ip, dst_ip),
                        tcp_layer.sport,
                        tcp_layer.dport,
                        "tcp",
                    )
                    payload_size = len(packet[Raw].load) if Raw in packet else 0
                elif UDP in packet:
                    udp_layer = packet[UDP]
                    flow_key = (
                        min(src_ip, dst_ip),
                        max(src_ip, dst_ip),
                        udp_layer.sport,
                        udp_layer.dport,
                        "udp",
                    )
                    payload_size = len(packet[Raw].load) if Raw in packet else 0
                else:
                    flow_key = (min(src_ip, dst_ip), max(src_ip, dst_ip), 0, 0, "other")
                    payload_size = len(packet[Raw].load) if Raw in packet else 0

                # Update flow
                flow = self.flows[flow_key]
                flow["packets"].append(packet)
                flow["bytes"] += payload_size
                if flow["start_time"] is None:
                    flow["start_time"] = datetime.utcnow()
                flow["end_time"] = datetime.utcnow()

        except Exception:
            pass  # Skip malformed packets

    def analyze_traffic(self, pcap_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze captured traffic or pcap file.

        Args:
            pcap_file: Path to pcap file (None = use captured packets)

        Returns:
            Dictionary containing analysis results
        """
        if pcap_file:
            # Load from file (would need rdpcap from scapy)
            return {"error": "PCAP file analysis not yet implemented"}

        if not self.packets:
            return {"error": "No packets captured"}

        analysis = {
            "total_packets": len(self.packets),
            "total_flows": len(self.flows),
            "protocols": defaultdict(int),
            "top_flows": [],
            "timestamp": datetime.utcnow().isoformat(),
        }

        # Analyze protocols
        for packet in self.packets:
            if TCP in packet:
                analysis["protocols"]["TCP"] += 1
            elif UDP in packet:
                analysis["protocols"]["UDP"] += 1
            if IP in packet:
                analysis["protocols"]["IP"] += 1
            if DNS in packet:
                analysis["protocols"]["DNS"] += 1
            if HTTP in packet or http.HTTPRequest in packet or http.HTTPResponse in packet:
                analysis["protocols"]["HTTP"] += 1

        # Get top flows by packet count
        sorted_flows = sorted(
            self.flows.items(),
            key=lambda x: len(x[1]["packets"]),
            reverse=True,
        )[:10]

        for flow_key, flow_data in sorted_flows:
            analysis["top_flows"].append({
                "src_ip": flow_key[0],
                "dst_ip": flow_key[1],
                "src_port": flow_key[2],
                "dst_port": flow_key[3],
                "protocol": flow_key[4],
                "packets": len(flow_data["packets"]),
                "bytes": flow_data["bytes"],
            })

        return analysis

    def get_flows(self) -> List[Dict[str, Any]]:
        """Get all detected flows."""
        flows_list = []
        for flow_key, flow_data in self.flows.items():
            flows_list.append({
                "src_ip": flow_key[0],
                "dst_ip": flow_key[1],
                "src_port": flow_key[2],
                "dst_port": flow_key[3],
                "protocol": flow_key[4],
                "packets": len(flow_data["packets"]),
                "bytes": flow_data["bytes"],
                "start_time": flow_data["start_time"].isoformat() if flow_data["start_time"] else None,
                "end_time": flow_data["end_time"].isoformat() if flow_data["end_time"] else None,
            })
        return flows_list

    def stop_capture(self):
        """Stop packet capture."""
        self.capturing = False
