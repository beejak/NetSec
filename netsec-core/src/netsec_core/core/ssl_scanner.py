"""SSL/TLS Security Scanner implementation."""

import socket
import ssl
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from cryptography import x509
from cryptography.hazmat.backends import default_backend


class SSLScanner:
    """SSL/TLS Security Scanner for certificate and cipher analysis."""

    def __init__(self):
        """Initialize SSL Scanner."""
        self.weak_ciphers = [
            "RC4",
            "DES",
            "MD5",
            "SHA1",
            "NULL",
            "EXPORT",
            "ANON",
            "ADH",
            "LOW",
            "3DES",
        ]

    def check_certificate(
        self,
        hostname: str,
        port: int = 443,
        check_expiration: bool = True,
        check_ciphers: bool = True,
        check_chain: bool = True,
    ) -> Dict[str, Any]:
        """
        Check SSL/TLS certificate and configuration.

        Args:
            hostname: Hostname to check
            port: Port to check (default: 443)
            check_expiration: Check certificate expiration
            check_ciphers: Check for weak ciphers
            check_chain: Validate certificate chain

        Returns:
            Dictionary containing certificate info and findings
        """
        findings = []
        certificate_info = {}

        try:
            # Get certificate
            cert_data = self._get_certificate(hostname, port)
            certificate_info = self._parse_certificate(cert_data)

            # Check expiration
            if check_expiration:
                expiration_findings = self._check_expiration(cert_data, hostname)
                findings.extend(expiration_findings)

            # Check ciphers
            if check_ciphers:
                cipher_findings = self._check_ciphers(hostname, port)
                findings.extend(cipher_findings)

            # Check certificate chain
            if check_chain:
                chain_findings = self._check_certificate_chain(cert_data)
                findings.extend(chain_findings)

            # Check certificate validity
            validity_findings = self._check_certificate_validity(cert_data)
            findings.extend(validity_findings)

        except socket.gaierror as e:
            findings.append({
                "finding_id": f"ssl-error-{hostname}",
                "type": "ssl_error",
                "severity": "high",
                "description": f"Could not resolve hostname: {str(e)}",
                "timestamp": datetime.utcnow().isoformat(),
            })
        except ssl.SSLError as e:
            findings.append({
                "finding_id": f"ssl-error-{hostname}",
                "type": "ssl_error",
                "severity": "high",
                "description": f"SSL/TLS error: {str(e)}",
                "timestamp": datetime.utcnow().isoformat(),
            })
        except Exception as e:
            findings.append({
                "finding_id": f"ssl-error-{hostname}",
                "type": "ssl_error",
                "severity": "medium",
                "description": f"Error checking certificate: {str(e)}",
                "timestamp": datetime.utcnow().isoformat(),
            })

        return {
            "hostname": hostname,
            "port": port,
            "certificate_info": certificate_info,
            "findings": findings,
            "timestamp": datetime.utcnow().isoformat(),
        }

    def _get_certificate(self, hostname: str, port: int) -> bytes:
        """Get SSL certificate from hostname:port."""
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert_der = ssock.getpeercert(binary_form=True)
                return cert_der

    def _parse_certificate(self, cert_der: bytes) -> Dict[str, Any]:
        """Parse certificate and extract information."""
        try:
            cert = x509.load_der_x509_certificate(cert_der, default_backend())

            info = {
                "subject": {},
                "issuer": {},
                "serial_number": str(cert.serial_number),
                "not_valid_before": cert.not_valid_before.isoformat(),
                "not_valid_after": cert.not_valid_after.isoformat(),
                "version": cert.version.name,
            }

            # Parse subject
            for attr in cert.subject:
                info["subject"][attr.oid._name] = attr.value

            # Parse issuer
            for attr in cert.issuer:
                info["issuer"][attr.oid._name] = attr.value

            # Get common name
            info["common_name"] = info["subject"].get("commonName", "Unknown")
            info["issuer_name"] = info["issuer"].get("commonName", "Unknown")

            return info
        except Exception as e:
            return {"error": str(e)}

    def _check_expiration(self, cert_der: bytes, hostname: str) -> List[Dict[str, Any]]:
        """Check certificate expiration."""
        findings = []

        try:
            cert = x509.load_der_x509_certificate(cert_der, default_backend())
            now = datetime.utcnow()
            expires = cert.not_valid_after.replace(tzinfo=None)

            days_until_expiry = (expires - now).days

            if days_until_expiry < 0:
                findings.append({
                    "finding_id": f"ssl-expired-{hostname}",
                    "type": "certificate_expired",
                    "severity": "critical",
                    "description": f"Certificate expired {abs(days_until_expiry)} days ago",
                    "timestamp": datetime.utcnow().isoformat(),
                })
            elif days_until_expiry < 7:
                findings.append({
                    "finding_id": f"ssl-expiring-{hostname}",
                    "type": "certificate_expiring",
                    "severity": "high",
                    "description": f"Certificate expires in {days_until_expiry} days",
                    "timestamp": datetime.utcnow().isoformat(),
                })
            elif days_until_expiry < 30:
                findings.append({
                    "finding_id": f"ssl-expiring-soon-{hostname}",
                    "type": "certificate_expiring",
                    "severity": "medium",
                    "description": f"Certificate expires in {days_until_expiry} days",
                    "timestamp": datetime.utcnow().isoformat(),
                })

        except Exception as e:
            findings.append({
                "finding_id": f"ssl-expiration-check-error-{hostname}",
                "type": "ssl_error",
                "severity": "low",
                "description": f"Error checking expiration: {str(e)}",
                "timestamp": datetime.utcnow().isoformat(),
            })

        return findings

    def _check_ciphers(self, hostname: str, port: int) -> List[Dict[str, Any]]:
        """Check for weak SSL/TLS ciphers."""
        findings = []

        try:
            context = ssl.create_default_context()
            context.set_ciphers("ALL:@SECLEVEL=0")  # Allow all ciphers for testing

            with socket.create_connection((hostname, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cipher = ssock.cipher()
                    if cipher:
                        cipher_name = cipher[0]
                        cipher_version = cipher[1]

                        # Check for weak ciphers
                        for weak in self.weak_ciphers:
                            if weak.upper() in cipher_name.upper():
                                findings.append({
                                    "finding_id": f"ssl-weak-cipher-{hostname}",
                                    "type": "weak_cipher",
                                    "severity": "high",
                                    "description": f"Weak cipher detected: {cipher_name} ({cipher_version})",
                                    "timestamp": datetime.utcnow().isoformat(),
                                })
                                break

                        # Check TLS version
                        if "TLSv1" in cipher_version or "SSLv" in cipher_version:
                            if "TLSv1.3" not in cipher_version and "TLSv1.2" not in cipher_version:
                                findings.append({
                                    "finding_id": f"ssl-weak-version-{hostname}",
                                    "type": "weak_tls_version",
                                    "severity": "high",
                                    "description": f"Outdated TLS version: {cipher_version}",
                                    "timestamp": datetime.utcnow().isoformat(),
                                })

        except Exception as e:
            findings.append({
                "finding_id": f"ssl-cipher-check-error-{hostname}",
                "type": "ssl_error",
                "severity": "low",
                "description": f"Error checking ciphers: {str(e)}",
                "timestamp": datetime.utcnow().isoformat(),
            })

        return findings

    def _check_certificate_chain(self, cert_der: bytes) -> List[Dict[str, Any]]:
        """Check certificate chain validity."""
        findings = []

        try:
            cert = x509.load_der_x509_certificate(cert_der, default_backend())

            # Basic chain validation
            # In production, this would verify the full chain
            issuer = cert.issuer
            subject = cert.subject

            # Check if self-signed
            if issuer == subject:
                findings.append({
                    "finding_id": "ssl-self-signed",
                    "type": "self_signed_certificate",
                    "severity": "medium",
                    "description": "Self-signed certificate detected",
                    "timestamp": datetime.utcnow().isoformat(),
                })

        except Exception as e:
            findings.append({
                "finding_id": "ssl-chain-check-error",
                "type": "ssl_error",
                "severity": "low",
                "description": f"Error checking certificate chain: {str(e)}",
                "timestamp": datetime.utcnow().isoformat(),
            })

        return findings

    def _check_certificate_validity(self, cert_der: bytes) -> List[Dict[str, Any]]:
        """Check certificate validity (not before, not after)."""
        findings = []

        try:
            cert = x509.load_der_x509_certificate(cert_der, default_backend())
            now = datetime.utcnow()
            not_before = cert.not_valid_before.replace(tzinfo=None)
            not_after = cert.not_valid_after.replace(tzinfo=None)

            if now < not_before:
                findings.append({
                    "finding_id": "ssl-not-valid-yet",
                    "type": "certificate_not_valid",
                    "severity": "high",
                    "description": f"Certificate not valid until {not_before.isoformat()}",
                    "timestamp": datetime.utcnow().isoformat(),
                })

            if now > not_after:
                findings.append({
                    "finding_id": "ssl-expired",
                    "type": "certificate_expired",
                    "severity": "critical",
                    "description": f"Certificate expired on {not_after.isoformat()}",
                    "timestamp": datetime.utcnow().isoformat(),
                })

        except Exception as e:
            findings.append({
                "finding_id": "ssl-validity-check-error",
                "type": "ssl_error",
                "severity": "low",
                "description": f"Error checking validity: {str(e)}",
                "timestamp": datetime.utcnow().isoformat(),
            })

        return findings

    def list_certificates(self) -> List[Dict[str, Any]]:
        """List monitored certificates (placeholder for future implementation)."""
        return {
            "message": "Certificate monitoring requires database storage (to be implemented)",
            "certificates": [],
            "timestamp": datetime.utcnow().isoformat(),
        }
