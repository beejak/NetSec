#!/usr/bin/env python3
"""
Run all research agents and generate consolidated report
"""

import json
import os
import sys
from datetime import datetime
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

def run_all_agents():
    """Run all research agents and consolidate findings"""
    
    print("🔍 Starting Multi-Agent Research...")
    print("=" * 60)
    
    agents = [
        NetworkMonitoringAgent(),
        VulnerabilityScannerAgent(),
        IDSAgent(),
        DNSAgent(),
        SSLSecurityAgent(),
        TrendsAgent(),
        CloudSecurityAgent(),
        ComplianceAgent(),
        GovernanceAgent(),
        RiskAgent(),
        ContainerSecurityAgent()
    ]
    
    all_findings = {
        "research_date": datetime.now().isoformat(),
        "agents_run": len(agents),
        "agents": []
    }
    
    for agent in agents:
        print(f"\n📊 Running {agent.name}...")
        findings = agent.research()
        all_findings["agents"].append(findings)
        print(f"✅ Completed {agent.name}")
        # Handle different agent data structures
        tools_count = (
            findings.get('tools_analyzed', 0) or
            findings.get('open_source_tools_analyzed', 0) or
            findings.get('enterprise_tools_analyzed', 0) or
            findings.get('frameworks_analyzed', 0) or
            findings.get('governance_aspects_analyzed', 0) or
            findings.get('risk_types_analyzed', 0) or
            findings.get('emerging_projects', 0) or
            0
        )
        gaps_count = findings.get('gaps_identified', 0)
        print(f"   - Tools/Frameworks analyzed: {tools_count}")
        print(f"   - Gaps identified: {gaps_count}")
    
    # Generate consolidated summary
    def count_tools(agent_data):
        """Count tools from various agent data structures"""
        return (
            agent_data.get('tools_analyzed', 0) or
            agent_data.get('open_source_tools_analyzed', 0) or
            agent_data.get('enterprise_tools_analyzed', 0) or
            agent_data.get('frameworks_analyzed', 0) or
            agent_data.get('governance_aspects_analyzed', 0) or
            agent_data.get('risk_types_analyzed', 0) or
            agent_data.get('emerging_projects', 0) or
            0
        )
    
    total_tools = sum(count_tools(a) for a in all_findings['agents'])
    total_gaps = sum(a.get('gaps_identified', 0) for a in all_findings['agents'])
    
    all_findings["summary"] = {
        "total_tools_analyzed": total_tools,
        "total_gaps_identified": total_gaps,
        "agents_run": len(agents)
    }
    
    # Save consolidated report in agents directory
    agents_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(agents_dir, "consolidated_research.json")
    md_path = os.path.join(agents_dir, "..", "CONSOLIDATED_REPORT.md")
    
    with open(json_path, 'w') as f:
        json.dump(all_findings, f, indent=2)
    
    print("\n" + "=" * 60)
    print("📋 Research Complete!")
    print(f"   Total tools analyzed: {total_tools}")
    print(f"   Total gaps identified: {total_gaps}")
    print(f"   Consolidated report saved to: {json_path}")
    
    # Generate markdown summary
    generate_markdown_summary(all_findings, md_path)
    
    return all_findings

def generate_markdown_summary(findings, output_path):
    """Generate a markdown summary of all research"""
    
    md = f"""# Consolidated Research Report
Generated: {findings['research_date']}

## Summary

- **Agents Run**: {findings['summary']['agents_run']}
- **Total Tools Analyzed**: {findings['summary']['total_tools_analyzed']}
- **Total Gaps Identified**: {findings['summary']['total_gaps_identified']}

## Agent Reports

"""
    
    def count_tools(agent_data):
        """Count tools from various agent data structures"""
        return (
            agent_data.get('tools_analyzed', 0) or
            agent_data.get('open_source_tools_analyzed', 0) or
            agent_data.get('enterprise_tools_analyzed', 0) or
            agent_data.get('frameworks_analyzed', 0) or
            agent_data.get('governance_aspects_analyzed', 0) or
            agent_data.get('risk_types_analyzed', 0) or
            agent_data.get('emerging_projects', 0) or
            0
        )
    
    for agent_data in findings['agents']:
        md += f"### {agent_data['agent']}\n\n"
        tools_count = count_tools(agent_data)
        md += f"- Tools/Frameworks Analyzed: {tools_count}\n"
        md += f"- Gaps Identified: {agent_data.get('gaps_identified', 0)}\n\n"
        
        # Handle different tool structures
        tools_to_show = []
        if 'tools' in agent_data:
            tools_to_show = agent_data['tools'][:3]
        elif 'open_source_tools' in agent_data:
            tools_to_show = agent_data['open_source_tools'][:3]
        elif 'enterprise_tools' in agent_data:
            tools_to_show = agent_data['enterprise_tools'][:3]
        elif 'frameworks' in agent_data:
            tools_to_show = agent_data['frameworks'][:3]
        
        if tools_to_show:
            md += "**Key Tools/Frameworks:**\n"
            for tool in tools_to_show:
                name = tool.get('name', tool.get('framework', tool.get('risk_type', 'Unknown')))
                tool_type = tool.get('type', tool.get('description', ''))
                md += f"- {name} ({tool_type})\n"
            md += "\n"
        
        if 'gaps' in agent_data:
            md += "**Key Gaps:**\n"
            for gap in agent_data['gaps'][:3]:  # Show first 3
                md += f"- {gap['gap']} ({gap['priority']})\n"
            md += "\n"
    
    md += "\n## Recommendations\n\n"
    md += "Based on all agent research, the following areas present the best opportunities:\n\n"
    md += "### Network Security\n"
    md += "1. **Unified Lightweight Toolkit** - Combine multiple security functions\n"
    md += "2. **API-First Architecture** - Make all tools programmable\n"
    md += "3. **DNS Security Analysis** - Underrepresented area\n"
    md += "4. **SSL/TLS Monitoring** - Limited open-source options\n"
    md += "5. **Container Security** - Cloud-native support needed\n"
    md += "6. **Developer Integration** - CI/CD friendly tools\n"
    md += "7. **Lightweight Anomaly Detection** - Statistical vs ML\n\n"
    md += "### Cloud Security\n"
    md += "8. **Lightweight Multi-Cloud CSPM** - Unified cloud security scanning\n"
    md += "9. **Cloud Compliance Automation** - Multi-framework compliance checking\n"
    md += "10. **Governance-as-Code** - Lightweight policy enforcement\n"
    md += "11. **Unified Risk Assessment** - Multi-risk-type assessment platform\n"
    md += "12. **Real-Time Cloud Security Monitoring** - Continuous cloud security\n"
    
    with open(output_path, 'w') as f:
        f.write(md)
    
    print(f"   Markdown summary saved to: {output_path}")

if __name__ == "__main__":
    findings = run_all_agents()
