"""DNS Security Scanner implementation."""

import dns.resolver
import dns.query
import dns.message
import dns.exception
from typing import List, Dict, Any, Optional
from datetime import datetime
import re
import statistics


class DNSScanner:
    """DNS Security Scanner for detecting various DNS security issues."""

    def __init__(self):
        """Initialize DNS Scanner."""
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = 5.0
        self.resolver.lifetime = 10.0

    def scan_domain(
        self,
        domain: str,
        check_tunneling: bool = True,
        check_spoofing: bool = True,
        analyze_patterns: bool = True,
    ) -> Dict[str, Any]:
        """
        Scan domain for DNS security issues.

        Args:
            domain: Domain name to scan
            check_tunneling: Check for DNS tunneling
            check_spoofing: Check for DNS spoofing
            analyze_patterns: Analyze query patterns

        Returns:
            Dictionary containing scan results and findings
        """
        findings = []
        domain_info = {}

        try:
            # Basic DNS resolution
            domain_info = self._resolve_domain(domain)

            # Check for DNS tunneling
            if check_tunneling:
                tunneling_findings = self._detect_tunneling(domain)
                findings.extend(tunneling_findings)

            # Check for DNS spoofing
            if check_spoofing:
                spoofing_findings = self._detect_spoofing(domain)
                findings.extend(spoofing_findings)

            # Analyze query patterns
            if analyze_patterns:
                pattern_findings = self._analyze_patterns(domain)
                findings.extend(pattern_findings)

            # Check for malicious domain indicators
            malicious_findings = self._check_malicious_indicators(domain)
            findings.extend(malicious_findings)

        except dns.exception.DNSException as e:
            findings.append({
                "finding_id": f"dns-error-{domain}",
                "type": "dns_error",
                "severity": "medium",
                "description": f"DNS resolution error: {str(e)}",
                "timestamp": datetime.utcnow().isoformat(),
            })

        return {
            "domain": domain,
            "domain_info": domain_info,
            "findings": findings,
            "timestamp": datetime.utcnow().isoformat(),
        }

    def _resolve_domain(self, domain: str) -> Dict[str, Any]:
        """Resolve domain and get DNS records."""
        info = {
            "a_records": [],
            "aaaa_records": [],
            "mx_records": [],
            "ns_records": [],
            "txt_records": [],
        }

        try:
            # A records
            answers = self.resolver.resolve(domain, "A")
            info["a_records"] = [str(rdata) for rdata in answers]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            pass

        try:
            # AAAA records
            answers = self.resolver.resolve(domain, "AAAA")
            info["aaaa_records"] = [str(rdata) for rdata in answers]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            pass

        try:
            # MX records
            answers = self.resolver.resolve(domain, "MX")
            info["mx_records"] = [
                {"priority": rdata.preference, "exchange": str(rdata.exchange)}
                for rdata in answers
            ]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            pass

        try:
            # NS records
            answers = self.resolver.resolve(domain, "NS")
            info["ns_records"] = [str(rdata) for rdata in answers]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            pass

        try:
            # TXT records
            answers = self.resolver.resolve(domain, "TXT")
            info["txt_records"] = [str(rdata) for rdata in answers]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            pass

        return info

    def _detect_tunneling(self, domain: str) -> List[Dict[str, Any]]:
        """
        Detect potential DNS tunneling attempts.

        DNS tunneling indicators:
        - Very long subdomain names
        - High entropy in subdomain names
        - Unusual character patterns
        - Multiple subdomain levels
        """
        findings = []

        # Check for long subdomains (potential data exfiltration)
        parts = domain.split(".")
        if len(parts) > 4:  # More than 4 levels
            findings.append({
                "finding_id": f"dns-tunnel-1-{domain}",
                "type": "dns_tunneling",
                "severity": "medium",
                "description": f"Domain has {len(parts)} levels, which may indicate DNS tunneling",
                "timestamp": datetime.utcnow().isoformat(),
            })

        # Check for high entropy (random-looking strings)
        for part in parts[:-2]:  # Exclude TLD and domain
            if len(part) > 20:  # Long subdomain
                # Calculate entropy (simple version)
                entropy = self._calculate_entropy(part)
                if entropy > 4.0:  # High entropy threshold
                    findings.append({
                        "finding_id": f"dns-tunnel-2-{domain}",
                        "type": "dns_tunneling",
                        "severity": "high",
                        "description": f"High entropy subdomain '{part}' detected (entropy: {entropy:.2f})",
                        "timestamp": datetime.utcnow().isoformat(),
                    })

        # Check for unusual patterns
        unusual_patterns = re.findall(r"[^a-zA-Z0-9.-]", domain)
        if unusual_patterns:
            findings.append({
                "finding_id": f"dns-tunnel-3-{domain}",
                "type": "dns_tunneling",
                "severity": "medium",
                "description": f"Unusual characters detected in domain: {set(unusual_patterns)}",
                "timestamp": datetime.utcnow().isoformat(),
            })

        return findings

    def _detect_spoofing(self, domain: str) -> List[Dict[str, Any]]:
        """
        Detect potential DNS spoofing/poisoning.

        Checks:
        - Multiple authoritative nameservers
        - Nameserver consistency
        - Response time anomalies
        """
        findings = []

        try:
            # Get nameservers from different resolvers
            ns_records = self.resolver.resolve(domain, "NS")
            ns_list = [str(ns) for ns in ns_records]

            if len(ns_list) < 2:
                findings.append({
                    "finding_id": f"dns-spoof-1-{domain}",
                    "type": "dns_spoofing",
                    "severity": "low",
                    "description": f"Only {len(ns_list)} nameserver(s) found (recommended: 2+)",
                    "timestamp": datetime.utcnow().isoformat(),
                })

            # Check response times (simple check)
            import time
            start = time.time()
            try:
                self.resolver.resolve(domain, "A")
                response_time = time.time() - start
                if response_time > 2.0:  # Slow response
                    findings.append({
                        "finding_id": f"dns-spoof-2-{domain}",
                        "type": "dns_spoofing",
                        "severity": "medium",
                        "description": f"Slow DNS response time: {response_time:.2f}s (may indicate spoofing)",
                        "timestamp": datetime.utcnow().isoformat(),
                    })
            except Exception:
                pass

        except Exception as e:
            findings.append({
                "finding_id": f"dns-spoof-3-{domain}",
                "type": "dns_spoofing",
                "severity": "low",
                "description": f"Could not verify nameservers: {str(e)}",
                "timestamp": datetime.utcnow().isoformat(),
            })

        return findings

    def _analyze_patterns(self, domain: str) -> List[Dict[str, Any]]:
        """Analyze DNS query patterns for anomalies."""
        findings = []

        # Check for suspicious patterns
        suspicious_patterns = [
            (r"^[0-9a-f]{32,}", "hex_encoded", "high"),  # Long hex strings
            (r"^[A-Za-z0-9+/]{20,}={0,2}$", "base64_like", "medium"),  # Base64-like
            (r".*\.(tk|ml|ga|cf)$", "suspicious_tld", "low"),  # Suspicious TLDs
        ]

        for pattern, pattern_type, severity in suspicious_patterns:
            if re.match(pattern, domain, re.IGNORECASE):
                findings.append({
                    "finding_id": f"dns-pattern-{pattern_type}-{domain}",
                    "type": "dns_pattern",
                    "severity": severity,
                    "description": f"Suspicious pattern detected: {pattern_type}",
                    "timestamp": datetime.utcnow().isoformat(),
                })

        return findings

    def _check_malicious_indicators(self, domain: str) -> List[Dict[str, Any]]:
        """Check for indicators of malicious domains."""
        findings = []

        # Check for typosquatting patterns (simple check)
        common_domains = ["google", "microsoft", "amazon", "facebook", "twitter"]
        domain_lower = domain.lower()
        for common in common_domains:
            if common in domain_lower and domain_lower != f"{common}.com":
                # Potential typosquatting
                findings.append({
                    "finding_id": f"dns-malicious-typo-{domain}",
                    "type": "malicious_indicator",
                    "severity": "medium",
                    "description": f"Potential typosquatting: domain contains '{common}'",
                    "timestamp": datetime.utcnow().isoformat(),
                })

        return findings

    def _calculate_entropy(self, text: str) -> float:
        """Calculate Shannon entropy of a string."""
        if not text:
            return 0.0

        import math
        entropy = 0.0
        text_length = len(text)
        char_counts = {}

        for char in text:
            char_counts[char] = char_counts.get(char, 0) + 1

        for count in char_counts.values():
            probability = count / text_length
            entropy -= probability * math.log2(probability)

        return entropy

    def monitor_dns_queries(self, duration: int = 60) -> Dict[str, Any]:
        """
        Monitor DNS queries (placeholder for future implementation).

        This would require packet capture capabilities.
        """
        return {
            "status": "monitoring",
            "duration": duration,
            "message": "DNS monitoring requires packet capture (to be implemented)",
            "timestamp": datetime.utcnow().isoformat(),
        }
