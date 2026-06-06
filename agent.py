# Filename: agent.py
import uuid
import json
import asyncio
import re
from google.adk.agents import LlmAgent
from google.adk.tools import VertexAiSearchTool
from google.adk.tools.discovery_engine_search_tool import DiscoveryEngineSearchTool
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# --- 1. Your actual Data Store paths ---
PROJECT_BASE = "projects/spatial-cargo-484310-t2/locations/global/collections/default_collection/dataStores/"

PATH_MODERN   = PROJECT_BASE + "zmatrix-compass-modern-strategy_1774113028464"
PATH_ORIENTAL = PROJECT_BASE + "zmatrix-compass-oriental-wisdom_1774112672636"
PATH_MACRO    = PROJECT_BASE + "zmatrix-compass-macro-trends_1774098671724"

class CustomSearchTool(DiscoveryEngineSearchTool):
    def __init__(self, name: str, description: str, data_store_id: str):
        super().__init__(data_store_id=data_store_id)
        self.name = name
        self.description = description

    def _get_declaration(self):
        decl = super()._get_declaration()
        if decl:
            decl.name = self.name
            decl.description = self.description
        return decl

# --- 2. Instantiate search tools ---
tool_modern = CustomSearchTool(
    name="search_modern_strategy",
    description="Search modern business strategy, agile frameworks, and data-driven decision making guidelines.",
    data_store_id=PATH_MODERN
)
tool_oriental = CustomSearchTool(
    name="search_oriental_wisdom",
    description="Search strategic foresight, relationship dynamics, and career risk mitigation wisdom.",
    data_store_id=PATH_ORIENTAL
)
tool_macro = CustomSearchTool(
    name="search_macro_trends",
    description="Search macroeconomic trends, labor market reports, and salary data.",
    data_store_id=PATH_MACRO
)

def get_master_instruction(target_job, mode):
    mode_instructions = {
        "modern": "[PERSPECTIVE] Use modern business strategy, agile frameworks, and data-driven decision making for deduction. Focus on sustainable growth, efficiency, and professional value optimization.",
        "oriental": "[PERSPECTIVE] Apply strategic foresight and relationship dynamics for deduction. Focus on analyzing the position's collaborative network, long-term professional harmony, and mitigating potential career risks.",
        "mixed": "[PERSPECTIVE] Blend rational optimization with macro-level strategic timing and holistic thinking."
    }
    current_perspective = mode_instructions.get(mode, mode_instructions["mixed"])

    return f"""You are the core backend deduction engine of "Z-Matrix AI".


    [SYSTEM REQUIREMENT: STRICT JSON FORMATTING]
    1. Your output must strictly start with '{{' and end with '}}'.
    2. Please do not use any markdown code blocks (e.g., ```json) or conversational prefaces.
    3. You must return the specific JSON structure below.
    
    [STEP 1: INPUT VALIDATION]
    Verify target job: 【{target_job}】. If it represents a cultural methodology or collaboration framework (e.g., DevOps, Agile, Scrum, Lean) rather than an independent execution role, please output:
    {{
        "status": "error",
        "error_type": "methodology_notice",
        "message": "Z-Matrix identified that 【{target_job}】 leans more toward a 'cultural methodology' or 'collaboration framework'. The Career Compass recommends focusing deduction on a specific execution role (e.g., Software Engineer, Platform Developer) to achieve highly precise deduction."
    }}

    If the job role is a valid execution role, perform deduction based on the following perspective:

    {current_perspective}

    [CORE OUTPUT DISCIPLINE]
    1. Output a single, valid JSON object. No prefaces or conversational responses.
    2. Abstract and summarize retrieved information into precise, high-density outputs fitting the specific JSON schema.
    3. Please avoid newline characters (\\n), tab characters (\\t), or Markdown formatting.
    4. Start directly with {{ and end with }}.
    5. [Language Requirement]: All generated text values inside the JSON fields MUST be strictly in English.
    6. [No Summary Paragraphs]: Parse and integrate data into the specific JSON fields (e.g., `ai_risk_index` or `salary_trend`) rather than writing natural language paragraphs.

    [MANDATORY OUTPUT JSON SCHEMA]
    {{
        "status": "success",
        "data": {{
            "macro_environment": {{
                "survival_rate": "Define quantitative or qualitative survival rate for this job role",
                "salary_trend": "Predict future salary trajectory",
                "ai_risk_index": "Generate an integer between 0 and 100 calculating the AI replacement risk",
                "macro_summary": "One-line macroeconomic verdict"
            }},
            "core_leverage": {{
                "key_competence": "The most non-substitutable core leverage of this position",
                "hidden_rule": "Implicit promotion barriers (within 50 words)",
                "short_verdict": "[Career Undertones Analysis] Explain career assets or risks (within 50 words)"
            }},
            "lifecycle_position": {{
                "current_phase": "What lifecycle phase this role is in",
                "fortune_verdict": "Qualitative rating (within 15 words, e.g. Auspicious, Resilient, etc.)"
            }},
            "evolution_paths": {{
                "upper_path": {{"name": "Upper Path Job Title", "strategy": "Breakthrough Strategy", "success_rate": "Probability"}},
                "middle_path": {{"name": "Middle Path Job Title", "strategy": "Alignment Strategy", "success_rate": "Probability"}},
                "lower_path": {{"name": "Lower Path Job Title", "strategy": "Survival Strategy", "success_rate": "Probability"}}
            }}
        }}
    }}"""

def run_compass_engine(target_job, mode):
    # Dynamically select data stores based on mode
    if mode == "modern":
        active_tools = [tool_modern, tool_macro]
    elif mode == "oriental":
        active_tools = [tool_oriental, tool_macro]
    else:
        # Mixed mode selects all available data stores
        active_tools = [tool_modern, tool_oriental, tool_macro]

    instruction = get_master_instruction(target_job, mode)

    root_agent = LlmAgent(
        name="zmatrix_oracle",
        model="gemini-2.5-pro",
        instruction=instruction,
        tools=active_tools,
        generate_content_config=types.GenerateContentConfig(
            safety_settings=[
                types.SafetySetting(
                    category="HARM_CATEGORY_HARASSMENT",
                    threshold="BLOCK_NONE",
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_HATE_SPEECH",
                    threshold="BLOCK_NONE",
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    threshold="BLOCK_NONE",
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_DANGEROUS_CONTENT",
                    threshold="BLOCK_NONE",
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_CIVIC_INTEGRITY",
                    threshold="BLOCK_NONE",
                ),
            ]
        ),
    )
    
    session_service = InMemorySessionService()
    runner = Runner(app_name="compass_app", agent=root_agent, session_service=session_service)
    
    query = f"Please perform deep graph deduction on job role 【{target_job}】 immediately and strictly return the JSON object."
    content = types.Content(role="user", parts=[types.Part.from_text(text=query)])
    
    session_id = str(uuid.uuid4())
    asyncio.run(session_service.create_session(app_name="compass_app", session_id=session_id, user_id="system_api"))
    
    events = runner.run(user_id="system_api", session_id=session_id, new_message=content)
    
    final_result = ""
    has_error = False
    error_msg = ""
    
    for event in events:
        print(f"[Event Trace] Raw event received: {repr(event)}")
        if hasattr(event, 'error_code') and event.error_code:
            has_error = True
            error_msg = f"{event.error_code}: {event.error_message}"
            print(f"[Event Trace Error] Event contains error: {error_msg}")
        try:
            # Path 1: Direct text (most common)
            if hasattr(event, 'text') and event.text:
                final_result += event.text
            # Path 2: Nested content parts (common in newer 2.5 versions)
            elif hasattr(event, 'content') and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        final_result += part.text
            # Path 3: Compatible with older message structures
            elif hasattr(event, 'message') and event.message.content:
                for part in event.message.content.parts:
                    if hasattr(part, 'text') and part.text:
                        final_result += part.text
        except Exception as e:
            print(f"[Event Trace Error] Failed to parse event: {e}")
            continue
            
    print(f"[Agent Trace] Final extracted result length: {len(final_result)}")
    
    if not final_result.strip():
        if has_error:
            return {"status": "error", "message": f"Deduction engine error: {error_msg}"}
        return {"status": "error", "message": "Deduction engine blocked mid-way. Please check the knowledge base configuration."}

    # Data cleaning pipeline to neutralize Gemini non-deterministic output anomalies
    clean_result = re.sub(r'\[\d+(?:,\s*\d+)*\]', '', final_result) 
    clean_result = clean_result.replace("```json", "").replace("```", "").strip()
    
    # Heuristic anchor to find the absolute inner-bound JSON payload
    start_idx = clean_result.rfind('{"status":') 
    if start_idx == -1:
        start_idx = clean_result.find('{')
        
    end_idx = clean_result.rfind('}')
    
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        json_str = clean_result[start_idx:end_idx+1]
        
        # Remove illegal escape characters that might break the structure
        json_str = json_str.replace('\n', '').replace('\t', '').replace('\\n', '').replace('\\t', '').replace('**', '')

        try:
            parsed_json = json.loads(json_str)
            # Fallback: handle nested levels
            if "data" in parsed_json and isinstance(parsed_json["data"], dict) and "status" in parsed_json["data"]:
                return parsed_json["data"]
            return parsed_json
        except Exception as e:
            print(f"❌ JSON deep parsing failed: {str(e)}")

    # Return raw text only if all the extraction methods above failed
    return {"status": "success", "raw_text": final_result}
