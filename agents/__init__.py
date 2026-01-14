"""
Research Agents Module

This module contains specialized research agents for analyzing
existing network security tools and identifying gaps.
"""

from agent_network_monitoring import NetworkMonitoringAgent
from agent_vulnerability_scanner import VulnerabilityScannerAgent
from agent_ids import IDSAgent
from agent_dns import DNSAgent
from agent_ssl import SSLSecurityAgent
from agent_trends import TrendsAgent
from agent_cloud_security import CloudSecurityAgent
from agent_compliance import ComplianceAgent
from agent_governance import GovernanceAgent
from agent_risk import RiskAgent
from agent_container_security import ContainerSecurityAgent

__all__ = [
    'NetworkMonitoringAgent',
    'VulnerabilityScannerAgent',
    'IDSAgent',
    'DNSAgent',
    'SSLSecurityAgent',
    'TrendsAgent',
    'CloudSecurityAgent',
    'ComplianceAgent',
    'GovernanceAgent',
    'RiskAgent',
    'ContainerSecurityAgent'
]
