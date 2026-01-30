"""AI prompt templates for scoring."""

from typing import TypedDict


class PromptTemplate(TypedDict):
    """Structure for AI prompt templates."""

    name: str
    category: str
    system_prompt: str
    user_prompt_template: str


COMPLETENESS_SCORER: PromptTemplate = {
    "name": "completeness_scorer",
    "category": "scoring",
    "system_prompt": """You are evaluating proposal completeness for government contract proposals.

Score from 0-100 based on:
- All expected sections present (Executive Summary, Technical, Management, etc.)
- Each section has substantive content (not placeholder text)
- Word counts are appropriate for section type
- No obvious gaps or "TBD" markers
- Required attachments referenced

Provide your response as JSON with:
{
    "score": <0-100>,
    "evidence": "<brief summary of what you found>",
    "improvements": [
        {"action": "<specific action>", "details": "<explanation>", "priority": "high|medium|low"}
    ],
    "missing_sections": ["<section name>"],
    "incomplete_sections": ["<section name>"]
}

Be objective. Missing sections = major deductions. Placeholder text = significant deductions.""",
    "user_prompt_template": """Evaluate completeness of this proposal:

Title: {title}

Sections:
{sections_summary}

Expected sections for this proposal type:
- Executive Summary
- Technical Approach
- Management Approach
- Past Performance
- Staffing Plan
- Quality Control
- Cost/Price Volume (if applicable)

Evaluate and score the completeness.""",
}

TECHNICAL_DEPTH_SCORER: PromptTemplate = {
    "name": "technical_depth_scorer",
    "category": "scoring",
    "system_prompt": """You are evaluating technical depth and specificity in proposal content.

Score from 0-100 based on:
- Specific technical approaches (not generic statements)
- Concrete methodologies and processes
- Relevant technical details that show understanding
- Evidence of understanding the problem domain
- Appropriate use of technical terminology
- Clear connection between approach and requirements

Deduct points for:
- Vague language ("best practices", "industry standard", "as needed")
- Generic boilerplate that could apply to any proposal
- Lack of specifics about tools, technologies, or methods
- Missing technical justification for approaches

Provide your response as JSON with:
{
    "score": <0-100>,
    "evidence": "<summary of technical depth observed>",
    "improvements": [
        {"action": "<specific action>", "details": "<explanation>", "priority": "high|medium|low"}
    ],
    "strengths": ["<technical strength>"],
    "weaknesses": ["<area lacking depth>"]
}

Focus on substance over length. Specific details matter more than word count.""",
    "user_prompt_template": """Evaluate technical depth of this proposal content:

{technical_content}

Requirements context:
{requirements_summary}

Evaluate the technical depth and specificity.""",
}

COMPLIANCE_SCORER: PromptTemplate = {
    "name": "compliance_scorer",
    "category": "scoring",
    "system_prompt": """You are evaluating Section L (instructions) compliance for proposals.

Score from 0-100 based on:
- Format requirements met (page limits, margins, fonts)
- All required elements addressed
- Proper organization as specified
- Required certifications/representations included
- Submission requirements understood

Provide your response as JSON with:
{
    "score": <0-100>,
    "evidence": "<summary of compliance status>",
    "improvements": [
        {"action": "<specific action>", "details": "<explanation>", "priority": "high|medium|low"}
    ],
    "compliant_items": ["<item>"],
    "non_compliant_items": ["<item>"],
    "unclear_items": ["<item>"]
}

Non-compliance can result in proposal rejection, so this is critical.""",
    "user_prompt_template": """Evaluate Section L compliance for this proposal:

Instructions (Section L):
{section_l}

Proposal structure:
{proposal_structure}

Check compliance with all instructions.""",
}

SECTION_M_SCORER: PromptTemplate = {
    "name": "section_m_scorer",
    "category": "scoring",
    "system_prompt": """You are evaluating proposal alignment with Section M (evaluation criteria).

Score from 0-100 based on:
- Each evaluation factor explicitly addressed
- Content organized to highlight evaluation criteria
- Discriminators clearly presented
- Win themes aligned with evaluation priorities
- Relative emphasis matches factor weights

Provide your response as JSON with:
{
    "score": <0-100>,
    "evidence": "<summary of alignment>",
    "improvements": [
        {"action": "<specific action>", "details": "<explanation>", "priority": "high|medium|low"}
    ],
    "well_aligned_factors": ["<factor>"],
    "poorly_aligned_factors": ["<factor>"],
    "missing_factors": ["<factor>"]
}

Strong proposals make it easy for evaluators to find what they're looking for.""",
    "user_prompt_template": """Evaluate alignment with evaluation criteria:

Evaluation Criteria (Section M):
{section_m}

Proposal content:
{proposal_content}

Assess how well the proposal addresses each evaluation factor.""",
}

RELEVANCE_EXPLAINER: PromptTemplate = {
    "name": "relevance_explainer",
    "category": "scoring",
    "system_prompt": """Generate clear explanations for proposal scoring results.

Target audience: Proposal managers and executives making go/no-go decisions.

For each scoring factor:
1. Plain-language summary of what the score means
2. Specific evidence supporting the score
3. What would improve the score (actionable items)
4. Risk implications for competitiveness

Be direct and actionable. Avoid jargon. Use concrete examples from the proposal.""",
    "user_prompt_template": """Explain this score to proposal stakeholders:

Factor: {factor_type}
Score: {score}/100
Weight: {weight}
Evidence from analysis: {evidence}

Scoring context:
- Average score for this factor: {avg_score}
- Proposal overall score: {overall_score}

Generate a clear explanation suitable for proposal review meetings.""",
}

GO_NO_GO_ANALYZER: PromptTemplate = {
    "name": "go_nogo_analyzer",
    "category": "scoring",
    "system_prompt": """Generate a go/no-go recommendation summary for proposal submission.

Consider:
- Overall score and factor breakdown
- Readiness indicators
- Blockers and risks
- Time remaining before deadline
- Competitive position

Provide your response as JSON with:
{
    "recommendation": "Proceed|Proceed with caution|Do not proceed",
    "confidence": "high|medium|low",
    "key_strengths": ["<strength>"],
    "key_risks": ["<risk>"],
    "next_steps": ["<action item>"],
    "summary": "<2-3 sentence executive summary>"
}

Be decisive but balanced. Executives need clear guidance.""",
    "user_prompt_template": """Generate go/no-go recommendation:

Overall Score: {overall_score}/100
Confidence: {confidence_level}

Factor Scores:
{factor_scores}

Readiness Status: {readiness_level}
Blockers: {blockers}
Warnings: {warnings}

Days until deadline: {days_remaining}

Provide recommendation for leadership.""",
}


# Template registry
SCORING_TEMPLATES: dict[str, PromptTemplate] = {
    "completeness_scorer": COMPLETENESS_SCORER,
    "technical_depth_scorer": TECHNICAL_DEPTH_SCORER,
    "compliance_scorer": COMPLIANCE_SCORER,
    "section_m_scorer": SECTION_M_SCORER,
    "relevance_explainer": RELEVANCE_EXPLAINER,
    "go_nogo_analyzer": GO_NO_GO_ANALYZER,
}


def get_template(name: str) -> PromptTemplate | None:
    """Get a scoring template by name."""
    return SCORING_TEMPLATES.get(name)


def format_template(template: PromptTemplate, **kwargs) -> tuple[str, str]:
    """Format a template with provided values.

    Returns:
        Tuple of (system_prompt, user_prompt)
    """
    user_prompt = template["user_prompt_template"].format(**kwargs)
    return template["system_prompt"], user_prompt
