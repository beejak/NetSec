"""Setup configuration for NetSec-Cloud."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="netsec-cloud",
    version="0.1.0",
    author="NetSec Toolkit Team",
    description="Cloud Security Scanner - Multi-cloud security scanning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/netsec-cloud",
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
        "Topic :: System :: Networking",
    ],
    python_requires=">=3.10",
    install_requires=[
        "boto3>=1.28.0",
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "pydantic>=2.5.0",
        "click>=8.1.0",
    ],
    extras_require={
        "azure": [
            "azure-identity>=1.15.0",
            "azure-mgmt-resource>=23.0.0",
            "azure-mgmt-storage>=21.0.0",
            "azure-mgmt-network>=24.0.0",
        ],
        "gcp": [
            "google-cloud-resource-manager>=1.10.0",
            "google-cloud-storage>=2.10.0",
            "google-cloud-compute>=1.14.0",
        ],
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
            "mypy>=1.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "netsec-cloud=netsec_cloud.cli.main:cli",
        ],
    },
)
