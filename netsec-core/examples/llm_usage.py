"""Examples of using LLM integration with NetSec-Core."""

import os
from netsec_core.llm.analyzer import LLMAnalyzer


def example_openai():
    """Example: Using OpenAI (bring your own key)."""
    print("=" * 60)
    print("OpenAI Example")
    print("=" * 60)
    
    # Option 1: Use environment variable
    os.environ["OPENAI_API_KEY"] = "your-key-here"
    analyzer = LLMAnalyzer(provider="openai", model="gpt-3.5-turbo")
    
    # Option 2: Pass API key directly
    # analyzer = LLMAnalyzer(
    #     provider="openai",
    #     model="gpt-4",
    #     api_key="sk-...",
    # )
    
    finding = {
        "finding_id": "test-1",
        "type": "weak_cipher",
        "severity": "high",
        "description": "TLS connection uses weak cipher suite",
    }
    
    result = analyzer.explain_finding(finding)
    print(f"Explanation: {result}")


def example_ollama():
    """Example: Using Ollama (local, no API key needed)."""
    print("\n" + "=" * 60)
    print("Ollama Example")
    print("=" * 60)
    
    # Make sure Ollama is running: ollama serve
    # Pull a model: ollama pull llama2
    
    analyzer = LLMAnalyzer(
        provider="ollama",
        model="llama2",  # or "mistral", "codellama", etc.
        base_url="http://localhost:11434/v1",  # Optional, defaults to this
    )
    
    finding = {
        "finding_id": "test-2",
        "type": "certificate_expired",
        "severity": "critical",
        "description": "SSL certificate expired 30 days ago",
    }
    
    remediation = analyzer.generate_remediation(finding)
    print(f"Remediation: {remediation}")


def example_lm_studio():
    """Example: Using LM Studio (local, no API key needed)."""
    print("\n" + "=" * 60)
    print("LM Studio Example")
    print("=" * 60)
    
    # Make sure LM Studio server is running
    
    analyzer = LLMAnalyzer(
        provider="lmstudio",
        model="your-model-name",  # Model loaded in LM Studio
        base_url="http://localhost:1234/v1",  # LM Studio default
    )
    
    traffic_summary = {
        "total_packets": 1000,
        "suspicious_connections": 5,
        "protocols": ["TCP", "UDP"],
    }
    
    analysis = analyzer.analyze_traffic(traffic_summary)
    print(f"Analysis: {analysis}")


def example_anthropic():
    """Example: Using Anthropic Claude (bring your own key)."""
    print("\n" + "=" * 60)
    print("Anthropic Example")
    print("=" * 60)
    
    analyzer = LLMAnalyzer(
        provider="anthropic",
        model="claude-3-sonnet-20240229",
        api_key="sk-ant-...",  # Your Anthropic API key
    )
    
    findings = [
        {
            "finding_id": "f1",
            "type": "dns_tunneling",
            "severity": "medium",
            "description": "Possible DNS tunneling detected",
        },
        {
            "finding_id": "f2",
            "type": "weak_cipher",
            "severity": "high",
            "description": "Weak cipher in use",
        },
    ]
    
    filtered = analyzer.reduce_false_positives(findings)
    print(f"Filtered findings: {len(filtered)}")


def example_environment_config():
    """Example: Using environment variables for configuration."""
    print("\n" + "=" * 60)
    print("Environment Configuration Example")
    print("=" * 60)
    
    # Set environment variables
    os.environ["LLM_PROVIDER"] = "ollama"
    os.environ["LLM_MODEL"] = "mistral"
    os.environ["OLLAMA_BASE_URL"] = "http://localhost:11434/v1"
    
    # Analyzer will use environment variables
    analyzer = LLMAnalyzer()  # Uses env vars automatically
    
    finding = {
        "finding_id": "test-3",
        "type": "open_port",
        "severity": "medium",
        "description": "Port 22 is open",
    }
    
    explanation = analyzer.explain_finding(finding)
    print(f"Explanation: {explanation}")


def example_api_usage():
    """Example: Using LLM via API."""
    print("\n" + "=" * 60)
    print("API Usage Example")
    print("=" * 60)
    
    import requests
    
    # Analyze traffic with OpenAI
    response = requests.post(
        "http://localhost:8000/api/v1/llm/analyze-traffic",
        json={
            "traffic_summary": {"packets": 1000},
            "provider": "openai",
            "model": "gpt-3.5-turbo",
            "api_key": "your-key-here",  # Bring your own key
        },
    )
    print(f"Response: {response.json()}")
    
    # Use local Ollama
    response = requests.post(
        "http://localhost:8000/api/v1/llm/generate-remediation",
        json={
            "finding": {
                "finding_id": "test-4",
                "type": "weak_cipher",
                "severity": "high",
            },
            "provider": "ollama",
            "model": "llama2",
            "base_url": "http://localhost:11434/v1",
        },
    )
    print(f"Remediation: {response.json()}")


if __name__ == "__main__":
    print("NetSec-Core LLM Integration Examples")
    print("\nNote: These examples require:")
    print("  - For OpenAI/Anthropic: API keys")
    print("  - For Ollama: Install and run 'ollama serve', then 'ollama pull llama2'")
    print("  - For LM Studio: Install and start server")
    print()
    
    # Uncomment the example you want to run:
    
    # example_openai()
    # example_ollama()
    # example_lm_studio()
    # example_anthropic()
    # example_environment_config()
    # example_api_usage()
    
    print("\nSee LLM_INTEGRATION.md for complete documentation.")
