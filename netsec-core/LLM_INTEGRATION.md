# LLM Integration Guide

## Overview

NetSec-Core supports multiple LLM providers with a "bring your own key" approach:

- **Cloud Providers**: OpenAI, Anthropic (requires API key)
- **Local Providers**: Ollama, LM Studio, vLLM, HuggingFace Transformers (no API key needed)

## Quick Start

### Cloud Providers (OpenAI/Anthropic)

```bash
# Set your API key
export OPENAI_API_KEY="your-key-here"
# or
export ANTHROPIC_API_KEY="your-key-here"

# Use in code
from netsec_core.llm.analyzer import LLMAnalyzer

analyzer = LLMAnalyzer(provider="openai", model="gpt-3.5-turbo")
# or pass API key directly
analyzer = LLMAnalyzer(provider="openai", model="gpt-4", api_key="your-key")
```

### Local Providers (Ollama)

```bash
# Install Ollama: https://ollama.ai
# Pull a model
ollama pull llama2

# Use in code
from netsec_core.llm.analyzer import LLMAnalyzer

analyzer = LLMAnalyzer(
    provider="ollama",
    model="llama2",
    base_url="http://localhost:11434/v1"  # Optional, defaults to this
)
```

### Local Providers (LM Studio)

```bash
# Install LM Studio: https://lmstudio.ai
# Start local server in LM Studio

# Use in code
from netsec_core.llm.analyzer import LLMAnalyzer

analyzer = LLMAnalyzer(
    provider="lmstudio",
    model="your-model-name",
    base_url="http://localhost:1234/v1"  # LM Studio default
)
```

## Configuration

### Environment Variables

```bash
# Provider selection
export LLM_PROVIDER="openai"  # or "anthropic", "ollama", "lmstudio", "vllm", "huggingface"

# Model selection
export LLM_MODEL="gpt-3.5-turbo"  # or any model name

# API keys (for cloud providers)
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"

# Base URLs (for local providers)
export OLLAMA_BASE_URL="http://localhost:11434/v1"
export LMSTUDIO_BASE_URL="http://localhost:1234/v1"
export VLLM_BASE_URL="http://localhost:8000/v1"
export LLM_BASE_URL="http://localhost:11434/v1"  # Generic
```

### Programmatic Configuration

```python
from netsec_core.llm.analyzer import LLMAnalyzer

# Cloud provider with API key
analyzer = LLMAnalyzer(
    provider="openai",
    model="gpt-4",
    api_key="sk-...",  # Bring your own key
)

# Local provider
analyzer = LLMAnalyzer(
    provider="ollama",
    model="mistral",
    base_url="http://localhost:11434/v1",
)
```

## Supported Providers

### 1. OpenAI (Cloud)

- **Requires**: API key
- **Models**: gpt-3.5-turbo, gpt-4, gpt-4-turbo, etc.
- **Install**: `pip install openai`
- **Usage**: Set `OPENAI_API_KEY` or pass `api_key` parameter

### 2. Anthropic (Cloud)

- **Requires**: API key
- **Models**: claude-3-opus, claude-3-sonnet, claude-3-haiku, etc.
- **Install**: `pip install anthropic`
- **Usage**: Set `ANTHROPIC_API_KEY` or pass `api_key` parameter

### 3. Ollama (Local)

- **Requires**: Ollama installed and running
- **Models**: llama2, mistral, codellama, etc.
- **Install**: https://ollama.ai
- **Usage**: Start Ollama, pull model, use provider="ollama"
- **Default URL**: `http://localhost:11434/v1`

### 4. LM Studio (Local)

- **Requires**: LM Studio installed and server running
- **Models**: Any model loaded in LM Studio
- **Install**: https://lmstudio.ai
- **Usage**: Start LM Studio server, use provider="lmstudio"
- **Default URL**: `http://localhost:1234/v1`

### 5. vLLM (Local)

- **Requires**: vLLM server running
- **Models**: Any model supported by vLLM
- **Install**: https://github.com/vllm-project/vllm
- **Usage**: Start vLLM server, use provider="vllm"
- **Default URL**: `http://localhost:8000/v1`

### 6. HuggingFace Transformers (Local)

- **Requires**: transformers, torch, accelerate
- **Models**: Any HuggingFace model
- **Install**: `pip install transformers torch accelerate`
- **Usage**: Use provider="huggingface", model="model-name"
- **Note**: Downloads model on first use

## API Usage

### Via API Routes

```bash
# Analyze traffic
curl -X POST "http://localhost:8000/api/v1/llm/analyze-traffic" \
  -H "Content-Type: application/json" \
  -d '{
    "traffic_summary": {...}
  }'

# Reduce false positives
curl -X POST "http://localhost:8000/api/v1/llm/reduce-false-positives" \
  -H "Content-Type: application/json" \
  -d '{
    "findings": [...],
    "context": {...}
  }'

# Generate remediation
curl -X POST "http://localhost:8000/api/v1/llm/generate-remediation" \
  -H "Content-Type: application/json" \
  -d '{
    "finding": {...},
    "context": {...}
  }'
```

### Via Python

```python
from netsec_core.llm.analyzer import LLMAnalyzer

# Initialize with your preferred provider
analyzer = LLMAnalyzer(
    provider="ollama",  # or "openai", "anthropic", etc.
    model="llama2",
    api_key="your-key" if provider in ["openai", "anthropic"] else None,
    base_url="http://localhost:11434/v1" if provider in ["ollama", "lmstudio"] else None,
)

# Analyze traffic
result = analyzer.analyze_traffic(traffic_summary)

# Reduce false positives
filtered = analyzer.reduce_false_positives(findings, context)

# Generate remediation
remediation = analyzer.generate_remediation(finding, context)

# Explain finding
explanation = analyzer.explain_finding(finding)
```

## Fallback Behavior

If LLM is unavailable or fails, the system automatically falls back to rule-based analysis:

- `LLMAnalyzerLocal` is used when no API keys are available
- Rule-based filtering and remediation templates are used
- No errors are raised, graceful degradation

## Best Practices

1. **API Keys**: Never commit API keys to version control
2. **Local Models**: Use local models for privacy-sensitive data
3. **Error Handling**: Always handle LLM failures gracefully
4. **Cost Management**: Monitor API usage for cloud providers
5. **Model Selection**: Choose appropriate model for task complexity

## Examples

See `examples/llm_usage.py` for complete examples.

## Troubleshooting

### OpenAI/Anthropic Issues

- Verify API key is set correctly
- Check API key has sufficient credits
- Verify network connectivity

### Ollama Issues

- Ensure Ollama is running: `ollama serve`
- Verify model is pulled: `ollama list`
- Check port 11434 is available

### LM Studio Issues

- Ensure LM Studio server is started
- Verify model is loaded in LM Studio
- Check port 1234 is available

### HuggingFace Issues

- Ensure sufficient disk space for model download
- Check GPU availability for faster inference
- Verify model name is correct
