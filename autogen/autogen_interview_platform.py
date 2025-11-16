"""
AutoGen Multi-Agent Workflow: AI-Powered Interview Platform Product Plan

This script implements a four-agent collaborative workflow to build a comprehensive
product plan for an AI-powered interview platform using Microsoft's AutoGen framework.

Agents:
1. ResearchAgent: Market researcher analyzing competitors and trends
2. AnalysisAgent: Product analyst identifying market gaps and opportunities
3. BlueprintAgent: Product designer creating features and user flows
4. ReviewerAgent: Product reviewer suggesting improvements and next steps

Configuration:
- Uses shared configuration from parent directory (.env and shared_config.py)
- No local .env file needed - uses parent directory configuration
"""

import os
from datetime import datetime
from typing import Dict, List, Any
import autogen
from config import Config


# ============================================================================
# AGENT DEFINITIONS
# ============================================================================

class InterviewPlatformAgents:
    """Manages all agents for the interview platform product planning workflow"""

    def __init__(self, config_list: List[Dict[str, Any]]):
        self.config_list = config_list
        self.agents = {}
        self.conversation_history = []

    def create_research_agent(self) -> autogen.ConversableAgent:
        """
        ResearchAgent: Market Researcher
        Role: Find and summarize current market competitors and trends
        """
        system_message = """You are an expert market research analyst specializing in AI-powered
        interview platforms and recruitment technology. Your task is to:

        1. Research and identify 3-4 major competitors in the AI interview space
           (e.g., HireVue, Pymetrics, Codility, etc.)
        2. Summarize their key features and market positioning
        3. Identify current trends in AI-powered recruiting
        4. Note any unmet market needs

        Provide a comprehensive competitive landscape analysis. Be specific with competitor names,
        features, and market gaps you identify.

        Format your response as a structured analysis with clear sections."""

        agent = autogen.ConversableAgent(
            name="ResearchAgent",
            system_message=system_message,
            llm_config={"config_list": self.config_list, "temperature": 0.7},
            human_input_mode="NEVER",
        )

        self.agents["research"] = agent
        return agent

    def create_analysis_agent(self) -> autogen.ConversableAgent:
        """
        AnalysisAgent: Product Analyst
        Role: Analyze research findings and extract key opportunities
        """
        system_message = """You are a strategic product analyst with expertise in SaaS product
        development. Based on market research findings, your task is to:

        1. Analyze the competitive landscape provided
        2. Identify 3 key market gaps or opportunities
        3. For each opportunity, explain:
           - What the gap is
           - Why it matters
           - How it can be addressed
           - Potential market size/impact

        Focus on opportunities that are:
        - Underserved by competitors
        - Valuable to customers
        - Technically feasible

        Provide structured analysis with numbered opportunities."""

        agent = autogen.ConversableAgent(
            name="AnalysisAgent",
            system_message=system_message,
            llm_config={"config_list": self.config_list, "temperature": 0.7},
            human_input_mode="NEVER",
        )

        self.agents["analysis"] = agent
        return agent

    def create_blueprint_agent(self) -> autogen.ConversableAgent:
        """
        BlueprintAgent: Product Designer
        Role: Create feature list and user flow
        """
        system_message = """You are an experienced product designer and UX strategist.
        Based on the market analysis and identified opportunities, create a product blueprint:

        1. Core Features (MVP):
           - List 5-7 essential features
           - Include feature descriptions
           - Explain how each addresses identified opportunities

        2. User Journey:
           - Map the main user flow for a hiring manager
           - Include key touchpoints
           - Describe the interview scheduling and analysis flow

        3. Differentiation:
           - Highlight how this product stands out
           - Key competitive advantages

        4. Target User Personas:
           - Hiring managers
           - Recruiters
           - Candidates

        Format as a comprehensive product blueprint document."""

        agent = autogen.ConversableAgent(
            name="BlueprintAgent",
            system_message=system_message,
            llm_config={"config_list": self.config_list, "temperature": 0.7},
            human_input_mode="NEVER",
        )

        self.agents["blueprint"] = agent
        return agent

    def create_reviewer_agent(self) -> autogen.ConversableAgent:
        """
        ReviewerAgent: Product Reviewer
        Role: Review blueprint and suggest improvements
        """
        system_message = """You are an experienced product executive and business strategist.
        Your role is to review the product blueprint and provide strategic recommendations:

        1. Feasibility Assessment:
           - Is the feature set realistic to build?
           - What might be missing?

        2. Market Viability:
           - Will this product succeed?
           - Any market risks?

        3. Business Model Suggestions:
           - Pricing strategy recommendations
           - Revenue streams

        4. Implementation Roadmap:
           - Phased launch approach
           - Key milestones

        5. Next Steps & Action Items:
           - Top 5 priorities for next phase
           - Resource requirements

        Provide constructive feedback and actionable recommendations."""

        agent = autogen.ConversableAgent(
            name="ReviewerAgent",
            system_message=system_message,
            llm_config={"config_list": self.config_list, "temperature": 0.7},
            human_input_mode="NEVER",
        )

        self.agents["reviewer"] = agent
        return agent


# ============================================================================
# WORKFLOW EXECUTION
# ============================================================================

class InterviewPlatformWorkflow:
    """Orchestrates the multi-agent conversation workflow"""

    def __init__(self, agents_manager: InterviewPlatformAgents):
        self.agents_manager = agents_manager
        self.outputs = {}

    def initiate_research_phase(self) -> str:
        """Start the workflow with market research"""
        print("\n" + "="*80)
        print("PHASE 1: MARKET RESEARCH")
        print("="*80)

        research_agent = self.agents_manager.agents["research"]

        initial_message = """Please conduct a comprehensive market analysis for AI-powered
        interview platforms. Focus on:

        1. Current market leaders and their key features
        2. Market trends and innovations
        3. Unmet needs and gaps

        Provide your analysis in a structured format."""

        # Get research output
        research_output = research_agent.generate_reply(
            messages=[{"content": initial_message, "role": "user"}]
        )

        print("\nResearch Agent Output:")
        print(research_output)
        self.outputs["research"] = research_output

        return research_output

    def conduct_analysis_phase(self, research_output: str) -> str:
        """Analyze research findings for opportunities"""
        print("\n" + "="*80)
        print("PHASE 2: MARKET GAP ANALYSIS")
        print("="*80)

        analysis_agent = self.agents_manager.agents["analysis"]

        analysis_message = f"""Based on the following market research, identify 3 key
        opportunities for an AI-powered interview platform:

        RESEARCH FINDINGS:
        {research_output}

        Please provide detailed analysis of market gaps and opportunities."""

        analysis_output = analysis_agent.generate_reply(
            messages=[{"content": analysis_message, "role": "user"}]
        )

        print("\nAnalysis Agent Output:")
        print(analysis_output)
        self.outputs["analysis"] = analysis_output

        return analysis_output

    def create_blueprint_phase(self, research_output: str, analysis_output: str) -> str:
        """Create product blueprint based on analysis"""
        print("\n" + "="*80)
        print("PHASE 3: PRODUCT BLUEPRINT")
        print("="*80)

        blueprint_agent = self.agents_manager.agents["blueprint"]

        blueprint_message = f"""Based on the market research and opportunity analysis below,
        create a comprehensive product blueprint for an AI-powered interview platform:

        MARKET RESEARCH:
        {research_output}

        OPPORTUNITY ANALYSIS:
        {analysis_output}

        Please create a detailed product blueprint with features, user journey, and differentiation."""

        blueprint_output = blueprint_agent.generate_reply(
            messages=[{"content": blueprint_message, "role": "user"}]
        )

        print("\nBlueprint Agent Output:")
        print(blueprint_output)
        self.outputs["blueprint"] = blueprint_output

        return blueprint_output

    def conduct_review_phase(self, blueprint_output: str) -> str:
        """Review blueprint and provide recommendations"""
        print("\n" + "="*80)
        print("PHASE 4: PRODUCT REVIEW & RECOMMENDATIONS")
        print("="*80)

        reviewer_agent = self.agents_manager.agents["reviewer"]

        review_message = f"""Please review the following product blueprint and provide
        strategic recommendations, feasibility assessment, and next steps:

        PRODUCT BLUEPRINT:
        {blueprint_output}

        Provide comprehensive review with actionable recommendations."""

        review_output = reviewer_agent.generate_reply(
            messages=[{"content": review_message, "role": "user"}]
        )

        print("\nReviewer Agent Output:")
        print(review_output)
        self.outputs["review"] = review_output

        return review_output

    def execute_workflow(self) -> Dict[str, str]:
        """Execute the complete four-phase workflow"""
        print("\n" + "="*80)
        print("AI-POWERED INTERVIEW PLATFORM - PRODUCT PLANNING WORKFLOW")
        print("="*80)
        print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Phase 1: Research
        research_output = self.initiate_research_phase()

        # Phase 2: Analysis
        analysis_output = self.conduct_analysis_phase(research_output)

        # Phase 3: Blueprint
        blueprint_output = self.create_blueprint_phase(research_output, analysis_output)

        # Phase 4: Review
        review_output = self.conduct_review_phase(blueprint_output)

        return self.outputs


# ============================================================================
# OUTPUT PROCESSING AND SAVING
# ============================================================================

class OutputManager:
    """Manages and saves workflow outputs"""

    def __init__(self, output_dir: str = None):
        # Use Config.OUTPUT_DIR if not provided
        self.output_dir = output_dir or Config.OUTPUT_DIR
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def save_outputs(self, outputs: Dict[str, str]) -> str:
        """Save all outputs to files"""
        output_file = os.path.join(self.output_dir, f"workflow_outputs_{self.timestamp}.txt")

        with open(output_file, "w") as f:
            f.write("="*80 + "\n")
            f.write("AI-POWERED INTERVIEW PLATFORM - PRODUCT PLAN\n")
            f.write("="*80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # Research Phase
            f.write("PHASE 1: MARKET RESEARCH & COMPETITIVE ANALYSIS\n")
            f.write("-"*80 + "\n")
            f.write(outputs.get("research", "No research output") + "\n\n")

            # Analysis Phase
            f.write("PHASE 2: MARKET GAP ANALYSIS & OPPORTUNITIES\n")
            f.write("-"*80 + "\n")
            f.write(outputs.get("analysis", "No analysis output") + "\n\n")

            # Blueprint Phase
            f.write("PHASE 3: PRODUCT BLUEPRINT\n")
            f.write("-"*80 + "\n")
            f.write(outputs.get("blueprint", "No blueprint output") + "\n\n")

            # Review Phase
            f.write("PHASE 4: PRODUCT REVIEW & RECOMMENDATIONS\n")
            f.write("-"*80 + "\n")
            f.write(outputs.get("review", "No review output") + "\n\n")

        return output_file

    def create_summary(self, outputs: Dict[str, str]) -> str:
        """Create a brief summary document"""
        summary_file = os.path.join(self.output_dir, f"summary_{self.timestamp}.txt")

        with open(summary_file, "w") as f:
            f.write("EXECUTIVE SUMMARY\n")
            f.write("="*80 + "\n")
            f.write("AI-Powered Interview Platform - Product Plan\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("WORKFLOW PHASES COMPLETED:\n")
            f.write("✓ Market Research & Competitive Analysis\n")
            f.write("✓ Market Gap & Opportunity Identification\n")
            f.write("✓ Product Blueprint Creation\n")
            f.write("✓ Strategic Review & Recommendations\n\n")

            f.write("KEY DELIVERABLES:\n")
            f.write("1. Competitive landscape analysis\n")
            f.write("2. Three identified market opportunities\n")
            f.write("3. Product features and user journey\n")
            f.write("4. Strategic recommendations and next steps\n\n")

            f.write("All outputs saved in workflow_outputs_{}.txt\n".format(self.timestamp))

        return summary_file


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""

    try:
        # Validate configuration
        print("Validating configuration...")
        if not Config.validate_setup():
            print("\n✗ Configuration validation failed")
            print("Please ensure OPENAI_API_KEY is set in the parent directory .env file")
            return False

        print(Config.get_summary())

        # Get configuration list
        config_list = Config.get_config_list()

        # Create agents
        print("Initializing agents...")
        agents_manager = InterviewPlatformAgents(config_list)

        agents_manager.create_research_agent()
        print("✓ ResearchAgent created")

        agents_manager.create_analysis_agent()
        print("✓ AnalysisAgent created")

        agents_manager.create_blueprint_agent()
        print("✓ BlueprintAgent created")

        agents_manager.create_reviewer_agent()
        print("✓ ReviewerAgent created")

        # Execute workflow
        print("\nInitiating workflow...")
        workflow = InterviewPlatformWorkflow(agents_manager)
        outputs = workflow.execute_workflow()

        # Save outputs
        print("\nSaving outputs...")
        output_manager = OutputManager()
        output_file = output_manager.save_outputs(outputs)
        summary_file = output_manager.create_summary(outputs)

        print("\n" + "="*80)
        print("WORKFLOW COMPLETED SUCCESSFULLY")
        print("="*80)
        print(f"Full outputs saved to: {output_file}")
        print(f"Summary saved to: {summary_file}")
        print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return True

    except Exception as e:
        print(f"\nError during workflow execution: {str(e)}")
        print("Please ensure:")
        print("  1. OPENAI_API_KEY is set in ../.env")
        print("  2. pyautogen is installed: pip install -r requirements.txt")
        print("  3. Parent directory .env file exists and is properly configured")
        raise


if __name__ == "__main__":
    main()
