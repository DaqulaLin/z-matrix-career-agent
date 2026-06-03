# 文件名: agent.py
import uuid
import json
import asyncio
import re
from google.adk.agents import LlmAgent
from google.adk.tools import VertexAiSearchTool
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# --- 1. 你真实的 Data Store 路径 ---
PROJECT_BASE = "projects/spatial-cargo-484310-t2/locations/global/collections/default_collection/dataStores/"

PATH_MODERN   = PROJECT_BASE + "zmatrix-compass-modern-strategy_1774113028464"
PATH_ORIENTAL = PROJECT_BASE + "zmatrix-compass-oriental-wisdom_1774112672636"
PATH_MACRO    = PROJECT_BASE + "zmatrix-compass-macro-trends_1774098671724"

# --- 2. 实例化搜索工具 ---
tool_modern   = VertexAiSearchTool(data_store_id=PATH_MODERN)
tool_oriental = VertexAiSearchTool(data_store_id=PATH_ORIENTAL)
tool_macro    = VertexAiSearchTool(data_store_id=PATH_MACRO)

def get_master_instruction(target_job, mode):
    mode_instructions = {
        "modern": "【视角】：使用现代商业博弈学、大厂敏捷体系、ROI杠杆进行推演。重点分析数据效率与绝对变现能力。",
        "oriental": "【视角】：运用东方传统谋略与职场因果论进行推演。重点分析该职位的'利他性'（积累优质人脉即种善因）与'反噬风险'（背锅即种恶因）。",
        "mixed": "【视角】：中西合璧，外圆内方。兼具商业的理性判断与东方智慧的大局观。"
    }
    current_perspective = mode_instructions.get(mode, mode_instructions["mixed"])

    return f"""你是"职道智途"底层的商业职业推演引擎(Oracle)。


    【🚨 绝密最高指令：禁止解释 🚨】
    1. 你的输出必须直接以 '{{' 开头，以 '}}' 结尾。
    2. 严禁在输出中包含任何“DevOps is a culture”、“Here's what that means”之类的解释文字、前言或后缀！
    3. 哪怕你识别到它是一种方法论，你也只能且必须输出下方的 JSON 结构，严禁废话！
    
    【前置核心指令：合法性校验】
    严格校验目标职位：【{target_job}】。如果是无意义字符或虚构职业（如修仙者、奥特曼），立即停止推演并输出特定的错误 JSON。
    如果该词汇在行业中更偏向于“文化”、“方法论”或“管理框架”（如 DevOps, Agile, Scrum, Lean），而非一个具体的独立职能岗位，请停止推演并输出：
    {{
        "status": "error",
        "error_type": "methodology_notice",
        "message": "Z-Matrix 识别到【{target_job}】在现代商业语境中更偏向于一种『文化方法论』或『协作框架』。罗盘推演建议针对具体的落地岗位（如：工程师、平台开发、运维经理）进行，以获得更精准的因果推演。"
    }}

    如果职位真实，严格按照以下要求推演：

    {current_perspective}

    【🚨 核心强制纪律 (System Override) 🚨】
    1. 你必须且只能输出一个合法的 JSON 对象。严禁在 JSON 之前或之后输出任何废话、问候语或思考过程，严禁任何 Markdown 标记。
    2. 即使你在知识库中检索到了几千字的“岗位职责”或“任职要求”，你也绝对不允许将其原文复述！你必须在脑海中将其高度浓缩，并严格填入下方的 JSON 字段中。
    3. JSON 内部严禁出现任何换行符 (\\n)、制表符 (\\t) 或 Markdown 加粗符号 (**)。
    4. 不要使用 ```json 代码块包裹你的输出，直接以 {{ 开头，以 }} 结尾。
    5. 【语言一致性】：无论检索到的知识库资料是英文还是其他语言，你必须且只能使用“简体中文”进行推演和输出。
    6. 【禁止摘要】：严禁将检索到的薪资数据（如 US$147,500）或岗位职责直接以自然语言段落形式输出！你必须将这些数据内化后，填入 `ai_risk_index` 或 `salary_trend` 等 JSON 字段中。
    7. 如果你无法生成 JSON，或者输出中包含了非 JSON 的文字段落，将被判定为任务失败。

    【JSON 强制输出结构】
    {{
        "status": "success",
        "data": {{
            "macro_environment": {{
                "survival_rate": "存活率判定",
                "salary_trend": "薪资走势预测",
                "ai_risk_index": 65,
                "macro_summary": "一句话宏观定性"
            }},
            "core_leverage": {{
                "key_competence": "最不可替代的核心筹码",
                "hidden_rule": "隐性晋升门槛（50字内）",
                "short_verdict": "【职道潜流解析】该职位在职场中容易积累何种'信用资产'或面临何种'反噬风险'及应对策略（50字内）"
            }},
            "lifecycle_position": {{
                "current_phase": "当前处于什么周期",
                "fortune_verdict": "定性的吉凶判词（控制在15字以内）"
            }},
            "evolution_paths": {{
                "upper_path": {{"name": "跃迁路线", "strategy": "策略", "success_rate": "概率"}},
                "middle_path": {{"name": "平替路线", "strategy": "策略", "success_rate": "概率"}},
                "lower_path": {{"name": "防御路线", "strategy": "策略", "success_rate": "概率"}}
            }}
        }}
    }}"""

# ... 前面 import 不变 ...

def run_compass_engine(target_job, mode):
   
  

    active_tools = [tool_macro]
    # ... 工具选择逻辑保持不变 ...

    instruction = get_master_instruction(target_job, mode)

    # 2. 强制指定企业版后缀，确保走 Vertex 链路
    root_agent = LlmAgent(
        name="zmatrix_oracle",
        model="gemini-2.5-pro",  # 🌟 建议加 -001 后缀更稳
        instruction=instruction,
        tools=active_tools,
        
      
    )
    
    session_service = InMemorySessionService()
    runner = Runner(app_name="compass_app", agent=root_agent, session_service=session_service)
    
    query = f"请立即对【{target_job}】进行深度图谱推演，并严格返回JSON。"
    content = types.Content(role="user", parts=[types.Part.from_text(text=query)])
    
    session_id = str(uuid.uuid4())
    asyncio.run(session_service.create_session(app_name="compass_app", session_id=session_id, user_id="system_api"))
    
    events = runner.run(user_id="system_api", session_id=session_id, new_message=content)
    
    final_result = ""
    # 3. 增强版暴力捕鱼网：支持 2.5 全系列版本
    for event in events:
        try:
            # 路径 1: 直接 text (最常见)
            if hasattr(event, 'text') and event.text:
                final_result += event.text
            # 路径 2: 嵌套 content parts (2.5 新版常见)
            elif hasattr(event, 'content') and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        final_result += part.text
            # 路径 3: 兼容旧版 message 结构
            elif hasattr(event, 'message') and event.message.content:
                for part in event.message.content.parts:
                    if hasattr(part, 'text') and part.text:
                        final_result += part.text
        except:
            continue
    
    if not final_result.strip():
        return {"status": "error", "message": "引擎推演中途受阻，请检查知识库配置"}

    # 4. 暴力数据清洗器 (彻底解决长文本和转义符污染)
    clean_result = re.sub(r'\[\d+(?:,\s*\d+)*\]', '', final_result) # 去除角标
    clean_result = clean_result.replace("```json", "").replace("```", "").strip()
    
    # 🌟 核心修复：从后往前找真正的 JSON 起始点，彻底解决“文字+JSON”混合的问题
    # 优先寻找包含核心状态码的起始位置
    start_idx = clean_result.rfind('{"status":') 
    if start_idx == -1:
        start_idx = clean_result.find('{')
        
    end_idx = clean_result.rfind('}')
    
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        json_str = clean_result[start_idx:end_idx+1]
        
        # 移除可能破坏结构的非法转义
        json_str = json_str.replace('\n', '').replace('\t', '').replace('\\n', '').replace('\\t', '').replace('**', '')

        try:
            parsed_json = json.loads(json_str)
            # 兜底：处理嵌套层级
            if "data" in parsed_json and isinstance(parsed_json["data"], dict) and "status" in parsed_json["data"]:
                return parsed_json["data"]
            return parsed_json
        except Exception as e:
            print(f"❌ JSON 深度解析失败: {str(e)}")

    # 如果上述暴力挖掘都失败了，才返回原始文本
    return {"status": "success", "raw_text": final_result}

