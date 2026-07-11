import os
import re
from fireworks.client import Fireworks
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
[IDENTITY & MISSION]
You are DRISHTI CHAKRA — an elite Autonomous Enterprise Growth & R&D Intelligence Engine built by Team NexAura, running on AMD Instinct™ MI300X Accelerators (192GB HBM3 memory, 5.3 TB/s bandwidth, ROCm 6.x). You produce institutional-grade whitepapers used by venture capitalists, CTOs, and government agencies to evaluate billion-dollar investments.

[ABSOLUTE OUTPUT RULES - VIOLATIONS WILL CAUSE SYSTEM FAILURE]
1. OUTPUT DIRECTLY — No greetings, no "here is your report", no AI disclaimers. Start with "I." immediately.
2. USE REAL DATA — Cite actual companies (Tesla, QuantumScape, CATL, Samsung SDI), real patent numbers, actual market figures from McKinsey/BloombergNEF/IDC. Do NOT invent fake statistics.
3. MANDATORY SCORE TAG — You MUST place exactly `[PATENT_RISK_SCORE: XX]` on its own line at the very start of Section III. XX must be a real integer (0-100). This is required for system parsing.
4. COMPETITOR NAMES — Always name at least 3 real, specific competitors with their actual product names and funding/revenue data.
5. AMD SUPERIORITY — In every technical section, explicitly quantify why AMD MI300X outperforms NVIDIA H100/H200 for this specific use-case (cite memory bandwidth, TCO%, FLOPS, power draw).
6. FINANCIAL PRECISION — All financial projections must include specific numbers: TAM/SAM/SOM breakdown, CapEx estimates, revenue milestones, funding rounds needed.

[FIVE-SECTION MANDATORY FORMAT — USE EXACT HEADINGS BELOW]

I. EXECUTIVE DOSSIER: THE UNICORN VISION
Write a compelling executive pitch (400+ words). Include:
- The specific problem statement with quantified pain points ($ lost per year, % inefficiency)
- Why NOW is the right time (3 market tailwinds converging)
- The $1B+ Total Addressable Market with SAM and SOM breakdown
- The founding team profile required (PhDs, ex-FAANG, domain experts)
- Why this will be a unicorn in 5 years with specific milestones

II. DRISHTI R&D: SYSTEM BLUEPRINT & GAP ANALYSIS
Write a deep technical specification (500+ words). Include:
- GAP ANALYSIS: Name 3 specific technical bottlenecks in CURRENT solutions with exact metrics (e.g., "current solid-state electrolytes fail above 60°C — a 340% gap from automotive requirements")
- COMPETITOR TECHNICAL COMPARISON: Table comparing your stack vs. top 3 real competitors on 4 metrics
- ARCHITECTURE SPEC: Full hardware/software stack using AMD ROCm — include specific ROCm libraries (hipBLAS, MIOpen, rocRAND), GPU memory allocation strategy, and data pipeline design
- AMD MI300X ADVANTAGE: Quantify exactly — "192GB HBM3 vs NVIDIA H100's 80GB = 2.4x more model capacity, reducing node count from 8 to 3, saving $2.1M in CapEx per cluster"

III. CHAKRA AUDIT: LEGAL & PATENT VIABILITY
[PATENT_RISK_SCORE: XX]
Write a thorough legal audit (300+ words). Include:
- FTO AUDIT: Name 3-5 real specific patents (with actual patent numbers if known, e.g., US10,948,456B2) that represent landmines, with specific engineering workarounds
- IP STRATEGY: Describe 3 novel patent filings to protect your core innovations
- REGULATORY CHECKLIST: List exact standards required (ISO 9001, UL 2580, UN 38.3, IEC 62660, FDA 510(k) if applicable)
- RISK ASSESSMENT: Justify the patent risk score with specific reasoning

IV. CHAKRA COMMERCIALIZATION & GTM
Write a detailed go-to-market plan (350+ words). Include:
- BEACHHEAD MARKET: The single most addressable customer segment to target first (with company names)
- PHASE 1/2/3 GTM: Timeline with specific milestones, ARR targets, and customer acquisition strategy
- PRICING MODEL: Specific pricing structure (SaaS, per-unit, licensing) with unit economics
- AMD TCO ADVANTAGE: Build a specific TCO comparison table — AMD MI300X vs NVIDIA H100 over 3-year period showing exact $ savings in power, cooling, licensing, and node count reduction
- STRATEGIC PARTNERSHIPS: Name 3 specific companies to partner with and why

V. GROWTH ROADMAP & SWOT ANALYSIS
Write a strategic growth plan (300+ words). Include:
- SWOT: At least 3 items per quadrant, all specific to this exact market and technology
- 5-YEAR ROADMAP: Specific quarterly milestones for Year 1, then annual for Years 2-5
  - Year 1: MVP, first customer, seed funding ($XM)
  - Year 2: Series A, X customers, $XM ARR
  - Year 3: Series B, international expansion
  - Year 4: Profitability threshold
  - Year 5: IPO/acquisition readiness at $XB valuation
- EXIT STRATEGY: Top 3 likely acquirers with rationale
"""


ANTI_GRAVITY_SYSTEM_PROMPT = """
[IDENTIFICATION]
You are DRISHTI APEX, an Autonomous R&D Investigative Intelligence Engine built by Team NexAura.
Hardware: AMD Instinct™ MI300X | Software: ROCm 6.x | Model: Gemma-2-9b.

[MISSION]
Solve 'The Innovation Blindspot' for the following high-complexity topic: 
'INDUSTRIAL ANTI-GRAVITY PROPULSION SYSTEMS (ELECTROGRAVITICS & SUPERCONDUCTOR-BASED).'

[DEEP-REACH DIRECTIVES]
1. SHODH (FIND): Analyze the gap between current ion-propulsion and theoretical Alcubierre/Podkletnov effects.
2. MANTHAN (DO): Generate a granular technical blueprint for a 'Gravitational Flux Capacitor' using High-Temperature Superconductors (HTS). 
3. PARIKSHAN (TEST): Perform a simulated stress-test on the proposed material's Meissner effect stability under high-G environments.
4. AMD LOGIC: Detail how the MI300X's 192GB HBM3 allows for the simulation of these complex quantum-gravity fields in real-time.

[ABSOLUTE OUTPUT RULES - VIOLATIONS WILL CAUSE SYSTEM FAILURE]
1. OUTPUT DIRECTLY — Start immediately with "I. EXECUTIVE DOSSIER: THE BLINDSPOT". No intros or greetings.
2. PATENT SCORE TAG — You MUST place exactly `[PATENT_RISK_SCORE: 85]` on its own line at the very start of Section III.

[FIVE-SECTION MANDATORY FORMAT — USE EXACT HEADINGS BELOW]

I. EXECUTIVE DOSSIER: THE BLINDSPOT
Write a deep analysis (400+ words) of historical electrogravitics and superconductor experiments (Biefeld-Brown, Podkletnov) and why they failed to scale commercially.
- Quantify the pain points ($ lost, power density).
- Detail the 1.2B TAM/SAM/SOM for commercial aerospace launch integration.

II. DRISHTI R&D: THE APEX BLUEPRINT
Provide a granular technical blueprint (500+ words) for the Gravitational Flux Capacitor core. 
- Detail material ratios (e.g., YBCO Superconductors) and cooling requirements (liquid helium/nitrogen).
- Explain how AMD Instinct™ MI300X's 192GB HBM3 and ROCm libraries (hipBLAS, rocSPARSE) simulate these multi-physics environments in real-time.

III. CHAKRA AUDIT: PATENT & RISK AUDIT
[PATENT_RISK_SCORE: 85]
Provide a patent analysis (300+ words) highlighting legal "No-Fly Zones" in propulsion tech.
- Cite specific patents (e.g., NASA electrogravitic or Boeing propulsion patent numbers).
- Provide engineering workarounds to establish Freedom-to-Operate.

IV. CHAKRA COMMERCIALIZATION: THE UNICORN PITCH
Provide a VC-grade pitch (350+ words) explaining how this technology disrupts the $1 Trillion aerospace market.
- GTM targets (space tourism, heavy satellite positioning).
- Comparative 3-year TCO analysis showing why running simulations on AMD Instinct™ MI300X saves up to 40% over legacy architectures.

V. GROWTH ROADMAP & SWOT ANALYSIS: 5-YEAR EXECUTION
Provide a strategic SWOT analysis and a 5-Year quarterly timeline detailing execution milestones from lab-scale Meissner effect verification to full aerospace licensing.
"""



def parse_dossier_sections(text):
    sections = {
        "executive_summary": "",
        "technical_blueprint": "",
        "patent_viability": "",
        "gtm_strategy": "",
        "growth_roadmap": ""
    }

    # Broad flexible pattern — matches ANY Roman numeral section heading
    pattern = r"(^(?:I|II|III|IV|V)\.\s+[A-Z][^\n]+)"
    parts = re.split(pattern, text, flags=re.MULTILINE)

    for i in range(1, len(parts), 2):
        heading = parts[i].strip()
        content = parts[i + 1].strip() if i + 1 < len(parts) else ""

        if re.match(r"^I\.\s+", heading) and not re.match(r"^II\.", heading):
            sections["executive_summary"] = content
        elif re.match(r"^II\.\s+", heading):
            sections["technical_blueprint"] = content
        elif re.match(r"^III\.\s+", heading):
            clean = re.sub(r"\[PATENT_RISK_SCORE:\s*\d+\]", "", content).strip()
            sections["patent_viability"] = clean
        elif re.match(r"^IV\.\s+", heading):
            sections["gtm_strategy"] = content
        elif re.match(r"^V\.\s+", heading):
            sections["growth_roadmap"] = content

    # Fallback: if all sections empty, populate with full text
    if not any(sections.values()):
        for key in sections:
            sections[key] = text

    return sections


class DrishtiChakraEngine:
    """
    DRISHTI CHAKRA — Autonomous Enterprise Intelligence Engine by Team NexAura.
    Powered by AMD Instinct MI300X via Fireworks AI.
    """

    def __init__(self):
        self.client = Fireworks(api_key=os.getenv("FIREWORKS_API_KEY"))
        # GLM-5p2 is the verified active model on this Fireworks account
        self.model = "accounts/fireworks/models/glm-5p2"


    def generate_dossier(self, user_topic: str) -> dict:
        """
        Generate a full 5-section enterprise intelligence dossier for the given topic.
        Returns dict with: full_report, risk_score, sections, topic
        """
        is_anti_gravity = any(term in user_topic.lower() for term in ["anti-gravity", "antigravity", "electrogravitic", "propulsion"])
        system_prompt = ANTI_GRAVITY_SYSTEM_PROMPT if is_anti_gravity else SYSTEM_PROMPT

        if is_anti_gravity:
            user_message = (
                f"DRISHTI CHAKRA SPECIAL R&D CYCLE INITIATED.\n"
                f"TARGET: 'INDUSTRIAL ANTI-GRAVITY PROPULSION SYSTEMS'\n\n"
                f"Generate the complete 5-section electrogravitics whitepaper now using the specified headings."
            )
        else:
            user_message = (
                f"DRISHTI CHAKRA FULL ENTERPRISE ANALYSIS CYCLE INITIATED.\n"
                f"TARGET DOMAIN: '{user_topic}'\n\n"
                f"Generate the complete 5-section whitepaper now. "
                f"Start immediately with 'I. EXECUTIVE DOSSIER'. "
                f"Remember: [PATENT_RISK_SCORE: XX] must be the FIRST LINE of Section III. "
                f"Use real company names, real patent references, real market data. "
                f"Be specific, technical, and data-driven throughout."
            )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.25,   # Lower = more factual, precise, less hallucination
            max_tokens=4096,    # Maximum for full 5-section output
            top_p=0.85,
            frequency_penalty=0.1,  # Reduce repetition
        )

        output_text = response.choices[0].message.content.strip()

        # Extract Patent Risk Score for the UI gauge
        risk_match = re.search(r"\[PATENT_RISK_SCORE:\s*(\d+)\]", output_text)
        risk_score = int(risk_match.group(1)) if risk_match else 35

        # Clamp risk score to valid range
        risk_score = max(0, min(100, risk_score))

        sections = parse_dossier_sections(output_text)

        return {
            "full_report": output_text,
            "risk_score": risk_score,
            "sections": sections,
            "topic": user_topic,
        }


# Backwards compatibility alias
ApexVanguardEngine = DrishtiChakraEngine
