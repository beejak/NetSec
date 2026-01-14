# Project Organization

## Overview

This repository contains **3 separate, independent projects** that are organized into their own directories:

1. **NetSec-Core** 🛡️ - Network Security Foundation
2. **NetSec-Cloud** ☁️ - Cloud Security, Compliance, Governance & Risk
3. **NetSec-Container** 🐳 - Container & Kubernetes Security

## Directory Structure

```
Netsec-Toolkit/
├── netsec-core/              # Network Security Project
│   ├── src/
│   ├── tests/
│   ├── docs/
│   └── README.md
│
├── netsec-cloud/             # Cloud Security Project
│   ├── src/
│   ├── tests/
│   ├── docs/
│   └── README.md
│
├── netsec-container/         # Container Security Project
│   ├── src/
│   ├── tests/
│   ├── docs/
│   │   ├── research/        # Research documents
│   │   └── README.md
│   ├── README.md
│   └── IMPLEMENTATION_SUMMARY.md
│
├── agents/                   # Research agents (shared)
├── scripts/                 # Setup scripts
└── *.md                     # Root-level planning/research docs
```

## Project Separation

Each project is **self-contained** and can be:
- ✅ Developed independently
- ✅ Deployed separately
- ✅ Used standalone
- ✅ Has its own dependencies
- ✅ Has its own documentation

## NetSec-Container Project

**Location**: `netsec-container/`

**Contains**:
- All container security scanner code
- Research documents in `docs/research/`
- Implementation documentation
- CI/CD examples
- Complete README

**Key Files**:
- `README.md` - Main project documentation
- `IMPLEMENTATION_SUMMARY.md` - Technical implementation details
- `docs/CONTAINER_SCANNER_COMPLETE.md` - Complete feature overview
- `docs/research/` - Research findings and analysis

## Root-Level Files

The root directory contains:
- **Planning documents** - Project planning and consolidation
- **Research agents** - Shared research tools
- **Setup scripts** - Initialization scripts for each project
- **Cross-project documentation** - Documents that apply to all projects

## Moving Forward

Each project should:
1. Be developed in its own directory
2. Have its own documentation
3. Be independently deployable
4. Not depend on other projects (unless explicitly designed)

## Notes

- Container-related research and documentation is now in `netsec-container/docs/`
- Each project has its own `README.md` for quick reference
- Root-level docs are for overall project planning and coordination
