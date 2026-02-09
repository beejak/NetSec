"""Unit tests for AssetDiscovery (no network for parse and inventory)."""

import pytest
from netsec_core.core.asset_discovery import AssetDiscovery


@pytest.mark.unit
def test_asset_discovery_init():
    """AssetDiscovery initializes."""
    discovery = AssetDiscovery()
    assert discovery is not None
    assert discovery.max_workers == 50


@pytest.mark.unit
def test_parse_network_single_ip():
    """_parse_network with single IP returns list with one host."""
    discovery = AssetDiscovery()
    hosts = discovery._parse_network("192.168.1.1")
    assert hosts == ["192.168.1.1"]


@pytest.mark.unit
def test_parse_network_cidr_24():
    """_parse_network with /24 returns list of hosts."""
    discovery = AssetDiscovery()
    hosts = discovery._parse_network("192.168.1.0/24")
    assert len(hosts) == 254
    assert "192.168.1.1" in hosts
    assert "192.168.1.254" in hosts


@pytest.mark.unit
def test_parse_network_range():
    """_parse_network with range returns list."""
    discovery = AssetDiscovery()
    hosts = discovery._parse_network("192.168.1.1-192.168.1.5")
    assert len(hosts) == 5
    assert "192.168.1.1" in hosts
    assert "192.168.1.5" in hosts


@pytest.mark.unit
def test_generate_inventory_empty():
    """generate_inventory with empty list returns zero counts."""
    discovery = AssetDiscovery()
    inv = discovery.generate_inventory([])
    assert inv["total_assets"] == 0
    assert inv["total_open_ports"] == 0
    assert "timestamp" in inv


@pytest.mark.unit
def test_generate_inventory_with_assets():
    """generate_inventory aggregates services and ports."""
    discovery = AssetDiscovery()
    assets = [
        {"ip": "1.2.3.4", "services": [{"port": 80, "service": "http"}], "open_ports": [80], "os_fingerprint": None},
        {"ip": "1.2.3.5", "services": [{"port": 443, "service": "https"}], "open_ports": [443], "os_fingerprint": None},
    ]
    inv = discovery.generate_inventory(assets)
    assert inv["total_assets"] == 2
    assert inv["total_open_ports"] == 2
    assert inv["assets_by_service"]["http"] == 1
    assert inv["assets_by_service"]["https"] == 1
