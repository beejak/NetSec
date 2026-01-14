"""Setup configuration for NetSec-Core."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="netsec-core",
    version="0.1.0",
    author="NetSec Toolkit Team",
    description="Network Security Foundation Toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/netsec-core",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
        "Topic :: System :: Networking :: Monitoring",
    ],
    python_requires=">=3.10",
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "scapy>=2.5.0",
        "dnspython>=2.4.0",
        "cryptography>=41.0.0",
        "click>=8.1.0",
        "pydantic>=2.5.0",
        "python-multipart>=0.0.6",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
            "mypy>=1.5.0",
            "httpx>=0.25.0",
        ],
        "llm": [
            "openai>=1.0.0",
            "anthropic>=0.7.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "netsec-core=netsec_core.cli.main:cli",
        ],
    },
)
