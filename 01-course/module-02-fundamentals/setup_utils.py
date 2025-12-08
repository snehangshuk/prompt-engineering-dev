"""
Module 2: Shared setup utilities
--------------------------------
Provides a single place to configure AI providers and helper functions that
each notebook can import. Mirrors the Module 3 helper style while keeping the
surface area focused on the tactics taught in this module.
"""

from __future__ import annotations

import base64
import os
from pathlib import Path
from typing import Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple

import asyncio
import concurrent.futures

# Load .env file FIRST before reading environment variables
try:
    from dotenv import load_dotenv
    # Try loading .env from project root (two levels up from this file)
    env_path = Path(__file__).parent.parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path, override=True)  # override=True ensures .env values take precedence
except ImportError:
    pass  # dotenv not available, skip loading

import anthropic
import openai

try:
    import requests
except ImportError:  # pragma: no cover - requests is part of requirements but guard just in case
    requests = None  # type: ignore


# ============================================
# 🎯 PROVIDER CONFIGURATION
# ============================================

AVAILABLE_PROVIDERS: Tuple[str, ...] = ("openai", "claude", "circuit")

# Default provider can be overridden via environment variable
PROVIDER: str = os.getenv("MODULE2_PROVIDER", "claude").lower()

# Default models per provider (customisable via environment variables)
OPENAI_DEFAULT_MODEL: str = os.getenv("MODULE2_OPENAI_MODEL", "gpt-5")
CLAUDE_DEFAULT_MODEL: str = os.getenv("MODULE2_CLAUDE_MODEL", "claude-sonnet-4")
CIRCUIT_DEFAULT_MODEL: str = os.getenv("MODULE2_CIRCUIT_MODEL", "gpt-4.1")

# GitHub Copilot proxy defaults (Option A)
_OPENAI_BASE_URL = os.getenv("MODULE2_OPENAI_BASE_URL", "http://localhost:7711/v1")
_CLAUDE_BASE_URL = os.getenv("MODULE2_CLAUDE_BASE_URL", "http://localhost:7711")
_PROXY_API_KEY = os.getenv("MODULE2_PROXY_API_KEY", "dummy-key")

# Initialize clients AFTER loading .env to ensure correct configuration
openai_client: openai.OpenAI = openai.OpenAI(
    base_url=_OPENAI_BASE_URL,
    api_key=_PROXY_API_KEY,
)

claude_client: anthropic.Anthropic = anthropic.Anthropic(
    base_url=_CLAUDE_BASE_URL,
    api_key=_PROXY_API_KEY,
)

circuit_client: Optional["openai.AzureOpenAI"] = None
circuit_app_key: Optional[str] = None


# ============================================
# 🔧 OPTIONAL CONFIG HELPERS
# ============================================

def configure_openai_from_env(api_key_env: str = "OPENAI_API_KEY") -> openai.OpenAI:
    """
    Configure the OpenAI client directly using an API key from the environment.

    1. Add your key to `.env` (or export it in your shell)
    2. Run `configure_openai_from_env()` in a notebook cell
    3. Optionally call `set_provider("openai")` if you want to switch providers
    """
    try:
        from dotenv import load_dotenv  # type: ignore
    except ImportError as exc:  # pragma: no cover - dotenv is in requirements but guard just in case
        raise RuntimeError("python-dotenv is required for configure_openai_from_env") from exc

    load_dotenv()
    api_key = os.getenv(api_key_env)
    if not api_key:
        raise RuntimeError(
            f"Environment variable '{api_key_env}' not set. "
            "Add it to your .env file or export it in your shell."
        )

    global openai_client
    openai_client = openai.OpenAI(api_key=api_key)
    return openai_client


def configure_circuit_from_env() -> "openai.AzureOpenAI":
    """
    Configure CircuIT (Azure OpenAI) access using the environment variables:

    - CISCO_CLIENT_ID
    - CISCO_CLIENT_SECRET
    - CISCO_OPENAI_APP_KEY

    These values can be generated from https://ai-chat.cisco.com/bridgeit-platform/api/home
    """
    if requests is None:
        raise RuntimeError("The 'requests' package is required to configure CircuIT access")

    try:
        from dotenv import load_dotenv  # type: ignore
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("python-dotenv is required for configure_circuit_from_env") from exc

    from openai import AzureOpenAI

    load_dotenv()

    client_id = os.getenv("CISCO_CLIENT_ID")
    client_secret = os.getenv("CISCO_CLIENT_SECRET")
    app_key = os.getenv("CISCO_OPENAI_APP_KEY")

    if not client_id or not client_secret or not app_key:
        raise RuntimeError(
            "CISCO_CLIENT_ID, CISCO_CLIENT_SECRET, and CISCO_OPENAI_APP_KEY "
            "must be set in your environment to use CircuIT."
        )

    url = "https://id.cisco.com/oauth2/default/v1/token"
    payload = "grant_type=client_credentials"
    creds = f"{client_id}:{client_secret}".encode("utf-8")
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {base64.b64encode(creds).decode('utf-8')}",
    }

    token_response = requests.post(url, headers=headers, data=payload, timeout=30)
    token_response.raise_for_status()
    token_data = token_response.json()

    client = AzureOpenAI(
        azure_endpoint="https://chat-ai.cisco.com",
        api_key=token_data.get("access_token"),
        api_version="2024-12-01-preview",
    )

    global circuit_client, circuit_app_key
    circuit_client = client
    circuit_app_key = app_key
    return client


# ============================================
# 🤖 COMPLETION HELPERS
# ============================================

def _extract_text_from_blocks(blocks: Iterable) -> str:
    """Extract text content from response blocks returned by Anthropic."""
    parts: List[str] = []
    for block in blocks:
        text_val = getattr(block, "text", None)
        if isinstance(text_val, str):
            parts.append(text_val)
        elif isinstance(block, Mapping):
            text = block.get("text")
            if isinstance(text, str):
                parts.append(text)
    return "\n".join(parts)


def _ensure_messages(messages: Sequence[MutableMapping[str, object]]) -> List[MutableMapping[str, object]]:
    if not isinstance(messages, Sequence):
        raise TypeError("messages must be a sequence of {'role': ..., 'content': ...} dictionaries")
    normalized: List[MutableMapping[str, object]] = []
    for message in messages:
        if not isinstance(message, MutableMapping):
            raise TypeError("Each message must be a dict-like object")
        if "role" not in message or "content" not in message:
            raise ValueError("Each message must contain 'role' and 'content' keys")
        normalized.append(message)  # shallow copy is fine
    return normalized


def get_provider() -> str:
    """Return the currently configured provider."""
    return PROVIDER


def set_provider(provider_name: str) -> str:
    """Set the active provider for requests."""
    provider_normalized = provider_name.lower()
    if provider_normalized not in AVAILABLE_PROVIDERS:
        raise ValueError(f"Unknown provider '{provider_name}'. Choose from {AVAILABLE_PROVIDERS}.")
    global PROVIDER
    PROVIDER = provider_normalized
    return PROVIDER


def get_default_model(provider: Optional[str] = None) -> str:
    """Get the default model for the given provider (or the active provider)."""
    provider = (provider or PROVIDER).lower()
    if provider == "claude":
        return CLAUDE_DEFAULT_MODEL
    if provider == "circuit":
        return CIRCUIT_DEFAULT_MODEL
    return OPENAI_DEFAULT_MODEL


def get_openai_completion(
    messages: Sequence[MutableMapping[str, object]],
    model: Optional[str] = None,
    temperature: float = 0.0,
) -> str:
    """Get a chat completion from OpenAI (GitHub Copilot proxy or direct)."""
    if openai_client is None:
        raise RuntimeError("OpenAI client is not configured. Run configure_openai_from_env() first.")

    cleaned_messages = _ensure_messages(messages)
    model_name = model or get_default_model("openai")
    
    # GPT-5 doesn't support temperature parameter
    kwargs = {
        "model": model_name,
        "messages": cleaned_messages,
    }
    if not model_name.lower().startswith("gpt-5"):
        kwargs["temperature"] = temperature
    
    response = openai_client.chat.completions.create(**kwargs)
    return response.choices[0].message.content or ""


def get_claude_completion(
    messages: Sequence[MutableMapping[str, object]],
    model: Optional[str] = None,
    temperature: float = 0.0,
) -> str:
    """Get a chat completion from Claude (via GitHub Copilot proxy)."""
    if claude_client is None:
        raise RuntimeError("Claude client is not configured.")

    cleaned_messages = _ensure_messages(messages)
    response = claude_client.messages.create(
        model=model or get_default_model("claude"),
        max_tokens=8192,
        messages=cleaned_messages,
        temperature=temperature,
    )
    return _extract_text_from_blocks(getattr(response, "content", []))


def get_circuit_completion(
    messages: Sequence[MutableMapping[str, object]],
    model: Optional[str] = None,
    temperature: float = 0.0,
) -> str:
    """Get a chat completion from CircuIT (Azure OpenAI)."""
    if circuit_client is None or circuit_app_key is None:
        raise RuntimeError(
            "CircuIT client not configured. Call configure_circuit_from_env() and set_provider('circuit')."
        )

    cleaned_messages = _ensure_messages(messages)
    response = circuit_client.chat.completions.create(
        model=model or get_default_model("circuit"),
        messages=cleaned_messages,
        temperature=temperature,
        user=f'{{"appkey": "{circuit_app_key}"}}',
    )
    return response.choices[0].message.content or ""


def get_chat_completion(
    messages: Sequence[MutableMapping[str, object]],
    model: Optional[str] = None,
    temperature: float = 0.0,
) -> str:
    """Route to the correct provider-specific completion helper."""
    provider = PROVIDER.lower()
    if provider == "claude":
        return get_claude_completion(messages, model, temperature)
    if provider == "circuit":
        return get_circuit_completion(messages, model, temperature)
    return get_openai_completion(messages, model, temperature)


# ============================================
# 🧪 CONNECTION TEST
# ============================================

def test_connection(
    expected_phrase: str = "Module 2 setup verified! Ready to learn core techniques.",
    temperature: float = 0.0,
) -> Tuple[bool, str]:
    """
    Run a simple round-trip request to confirm connectivity.

    Returns:
        tuple (success: bool, response: str)
    """
    messages = [
        {
            "role": "system",
            "content": "You are a prompt engineering instructor.",
        },
        {
            "role": "user",
            "content": f"Respond with exactly: '{expected_phrase}'",
        },
    ]

    response = get_chat_completion(messages, temperature=temperature)
    normalized = response.lower() if response else ""
    success = expected_phrase.lower() in normalized

    print("🧪 Connection Test")
    print(f"🤖 Provider: {PROVIDER.upper()} (model: {get_default_model()})")
    print(f"📝 Response: {response}")
    if success:
        print("✅ Connection looks good!")
    else:
        print("⚠️ Unexpected response. Double-check your provider configuration.")

    return success, response


# ============================================
# ⚡ PARALLEL EXECUTION HELPERS
# ============================================

async def get_chat_completion_async(
    messages: Sequence[MutableMapping[str, object]],
    model: Optional[str] = None,
    temperature: float = 0.0,
) -> str:
    """
    Async wrapper for get_chat_completion to enable parallel execution.
    
    Use this when you want to generate multiple completions concurrently using asyncio.gather().
    
    Example:
        >>> async def generate_multiple():
        ...     results = await asyncio.gather(
        ...         get_chat_completion_async([{"role": "user", "content": "Approach A"}]),
        ...         get_chat_completion_async([{"role": "user", "content": "Approach B"}]),
        ...         get_chat_completion_async([{"role": "user", "content": "Approach C"}])
        ...     )
        ...     return results
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None, 
        lambda: get_chat_completion(messages, model=model, temperature=temperature)
    )


def run_async(coro):
    """
    Run an async coroutine in Jupyter notebooks or regular Python.
    
    Jupyter notebooks already have a running event loop, so asyncio.run() won't work.
    This function handles both cases by running the coroutine in a separate thread if needed.
    
    Args:
        coro: An async coroutine to execute
        
    Returns:
        The result of the coroutine
        
    Example:
        >>> async def my_async_function():
        ...     return await asyncio.gather(...)
        >>> result = run_async(my_async_function())
    """
    def run():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()
    
    try:
        # Check if we're in a running event loop (Jupyter case)
        asyncio.get_running_loop()
        # Run in a separate thread with its own event loop
        with concurrent.futures.ThreadPoolExecutor() as executor:
            return executor.submit(run).result()
    except RuntimeError:
        # No running loop - safe to use asyncio.run() directly
        return asyncio.run(coro)


# ============================================
# 🔖 MISC HELPERS
# ============================================

def read_markdown(path: str | Path) -> str:
    """Convenience helper: read a markdown file as text."""
    file_path = Path(path)
    return file_path.read_text()


def save_markdown(path: str | Path, content: str) -> None:
    """Save text to a markdown file."""
    file_path = Path(path)
    file_path.write_text(content)


# ============================================
# 📊 PROMPT EVALUATION (Traditional Metrics + Quality Assessment)
# ============================================

def _extract_section(text: str, section_name: str) -> str:
    """Extract content between XML-style tags."""
    import re
    pattern = rf'<{section_name}>(.*?)</{section_name}>'
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""


def _calculate_traditional_metrics(
    messages: Sequence[MutableMapping[str, object]],
    expected_tactics: Sequence[str],  # noqa: ARG001
) -> Mapping[str, object]:
    """
    Calculate objective, quantitative metrics for prompt evaluation.

    Returns:
        Dictionary with metric scores and evidence
    """
    prompt_text = str(messages)
    metrics = {}

    # 1. Structure Detection
    has_system_message = any(msg.get("role") == "system" for msg in messages)
    metrics["has_system_message"] = has_system_message

    # 2. XML Tag Detection (for structured inputs)
    xml_tags = []
    common_tags = ["code", "requirements", "context", "example", "document", "thinking", "output",
                   "test_file", "source_code", "analysis", "quotes", "evaluation"]
    for tag in common_tags:
        if f"<{tag}>" in prompt_text.lower():
            xml_tags.append(tag)
    metrics["xml_tags_found"] = xml_tags
    metrics["uses_xml_structure"] = len(xml_tags) > 0

    # 3. Few-Shot Pattern Detection
    assistant_messages = [msg for msg in messages if msg.get("role") == "assistant"]
    # Also check for examples in content (e.g., "EXAMPLE 1:", "Example:", etc.)
    example_keywords = ["example 1:", "example 2:", "example 3:", "example:"]
    example_count_in_content = sum(1 for kw in example_keywords if kw in prompt_text.lower())
    # Check for <example> XML tags
    example_tag_count = prompt_text.lower().count("<example>")
    # Use the highest count (assistant messages, inline examples, or XML tags)
    metrics["example_count"] = max(len(assistant_messages), example_count_in_content, example_tag_count)
    metrics["uses_few_shot"] = metrics["example_count"] >= 2

    # 4. Chain-of-Thought Keywords
    cot_keywords = ["step-by-step", "think through", "reasoning", "analyze", "before", "first", "then"]
    cot_found = [kw for kw in cot_keywords if kw in prompt_text.lower()]
    metrics["cot_keywords_found"] = cot_found
    metrics["uses_cot"] = len(cot_found) > 0

    # 5. Role Prompting Detection
    role_indicators = ["you are a", "you are an", "act as", "role:", "persona:"]
    role_found = [ind for ind in role_indicators if ind in prompt_text.lower()]
    metrics["role_indicators"] = role_found
    metrics["uses_role_prompting"] = len(role_found) > 0

    # 6. Tree of Thoughts Detection (multiple approaches/alternatives)
    # Includes parallel exploration pattern detection
    tot_keywords = ["approach a", "approach b", "approach c", "alternative", "option 1", "option 2", "multiple approaches", "different solutions"]
    tot_tags = ["<approach_a>", "<approach_b>", "<approach_c>", "<option_1>", "<option_2>", "<alternative_"]
    parallel_keywords = ["parallel", "simultaneously", "concurrent", "asyncio.gather", "all at once", "in parallel"]
    tot_found = [kw for kw in tot_keywords if kw in prompt_text.lower()]
    tot_tags_found = [tag for tag in tot_tags if tag in prompt_text.lower()]
    parallel_found = [kw for kw in parallel_keywords if kw in prompt_text.lower()]
    metrics["tot_keywords_found"] = tot_found + tot_tags_found + parallel_found
    # Parallel exploration: multiple approaches OR parallel keywords + at least one approach
    metrics["uses_tree_of_thoughts"] = len(tot_found) >= 2 or len(tot_tags_found) >= 2 or (len(parallel_found) > 0 and (len(tot_found) >= 1 or len(tot_tags_found) >= 1))
    metrics["uses_parallel_execution"] = len(parallel_found) > 0 and (len(tot_found) >= 2 or len(tot_tags_found) >= 2)

    # 7. Evaluation Rubric Detection (evaluation rubrics, scoring, weighted criteria)
    judge_keywords = ["rubric", "evaluate", "score", "rate", "criteria", "weighted", "judge", "assessment", "compare", "0-10", "1-10"]
    judge_found = [kw for kw in judge_keywords if kw in prompt_text.lower()]
    has_percentages = "%" in prompt_text  # Weighted criteria like "40%", "30%"
    metrics["judge_keywords_found"] = judge_found
    metrics["uses_llm_as_judge"] = len(judge_found) >= 3 or (len(judge_found) >= 2 and has_percentages)

    # 8. Document Structure Detection (for citations)
    has_doc_structure = "<documents>" in prompt_text.lower() or "<document>" in prompt_text.lower()
    has_source_tags = "<source>" in prompt_text.lower()
    metrics["uses_document_structure"] = has_doc_structure and has_source_tags

    # 9. Prompt Length Analysis
    total_chars = len(prompt_text)
    metrics["total_characters"] = total_chars
    metrics["complexity"] = "high" if total_chars > 1000 else "medium" if total_chars > 300 else "low"

    return metrics


def evaluate_prompt(
    messages: Sequence[MutableMapping[str, object]],
    activity_name: str,
    expected_tactics: Sequence[str],
    track_progress: bool = True,
    return_results: bool = False,
) -> Optional[Mapping[str, object]]:
    """
    Evaluate a student's prompt using Traditional Metrics + Quality Assessment.

    This function provides comprehensive automated feedback by combining:
    1. Traditional eval metrics (objective, fast, deterministic)
    2. Quality Assessment (subjective, nuanced, educational)
    3. Progress tracking (optional, saves evaluation history)

    Args:
        messages: The student's prompt (list of message dictionaries)
        activity_name: Name of the activity (e.g., "Activity 2.1")
        expected_tactics: List of tactics that should be present
                         (e.g., ["Role Prompting", "Structured Inputs"])
        track_progress: Whether to save evaluation to history (default: True)
        return_results: Whether to return evaluation data dict (default: False)
                       Set to True if you want to inspect/save results programmatically

    Returns:
        None by default (prints output only)
        If return_results=True: Dictionary with evaluation data

    Example:
        >>> messages = [
        ...     {"role": "system", "content": "You are a QA engineer..."},
        ...     {"role": "user", "content": "<test_file>...</test_file>"}
        ... ]
        >>> evaluate_prompt(
        ...     messages=messages,
        ...     activity_name="Activity 2.1",
        ...     expected_tactics=["Role Prompting", "Structured Inputs"]
        ... )
    """

    # STEP 1: Calculate Traditional Metrics (Fast & Objective)
    metrics = _calculate_traditional_metrics(messages, expected_tactics)

    # Convert messages to string for LLM analysis
    prompt_text = str(messages)

    # STEP 2: Format Traditional Metrics for Display
    xml_tags: List[str] = metrics.get('xml_tags_found', [])  # type: ignore
    cot_keywords: List[str] = metrics.get('cot_keywords_found', [])  # type: ignore
    role_indicators: List[str] = metrics.get('role_indicators', [])  # type: ignore
    complexity = str(metrics.get('complexity', 'unknown'))

    tot_keywords: List[str] = metrics.get('tot_keywords_found', [])  # type: ignore
    judge_keywords: List[str] = metrics.get('judge_keywords_found', [])  # type: ignore

    # Build tactic detection lines dynamically based on expected_tactics
    parallel_execution = metrics.get('uses_parallel_execution', False)
    parallel_note = " (parallel execution detected)" if parallel_execution else ""
    
    tactic_mapping = {
        "Few-Shot Examples": f"- Few-shot examples: {metrics.get('example_count', 0)} examples {'✅' if metrics.get('uses_few_shot') else '❌'}",
        "Chain-of-Thought": f"- Chain-of-thought keywords: {', '.join(cot_keywords) if cot_keywords else 'None'} {'✅' if metrics.get('uses_cot') else '❌'}",
        "Role Prompting": f"- Role indicators: {', '.join(role_indicators) if role_indicators else 'None'} {'✅' if metrics.get('uses_role_prompting') else '❌'}",
        "Tree of Thoughts": f"- Tree of Thoughts indicators: {', '.join(tot_keywords) if tot_keywords else 'None'} {'✅' if metrics.get('uses_tree_of_thoughts') else '❌'}{parallel_note}",
        "Evaluation Rubric": f"- Evaluation rubric indicators: {', '.join(judge_keywords) if judge_keywords else 'None'} {'✅' if metrics.get('uses_llm_as_judge') else '❌'}",
        "Reference Citations": f"- Document structure: {'✅ Yes' if metrics.get('uses_document_structure') else '❌ No'}",
        "Structured Inputs": f"- XML tags detected: {', '.join(xml_tags) if xml_tags else 'None'}\n- Uses structured inputs: {'✅ Yes' if metrics.get('uses_xml_structure') else '❌ No'}",
    }

    # Only include tactics that are expected for this activity
    tactic_lines = []
    for tactic in expected_tactics:
        if tactic in tactic_mapping:
            tactic_lines.append(tactic_mapping[tactic])

    tactic_detection_section = "\n".join(tactic_lines) if tactic_lines else "- No specific tactics to detect"

    metrics_summary = f"""
📏 TRADITIONAL EVAL METRICS (Objective Analysis)
{'=' * 70}

**Structure Analysis:**
- Has system message: {'✅ Yes' if metrics.get('has_system_message') else '❌ No'}

**Tactic Detection (Expected Tactics Only):**
{tactic_detection_section}

**Complexity:**
- Total characters: {metrics.get('total_characters', 0)}
- Complexity level: {complexity.upper()}

{'=' * 70}
"""

    # Build tactic descriptions dynamically based on expected_tactics
    tactic_descriptions = {
        "Role Prompting": "Check for specific, relevant persona with clear expertise domain",
        "Structured Inputs": "Check for meaningful organization and clear section boundaries",
        "Few-Shot Examples": "Check for high-quality examples that teach the desired pattern",
        "Chain-of-Thought": "Check for systematic reasoning instructions",
        "Reference Citations": "Check for proper document structure and quote extraction",
        "Prompt Chaining": "Check for multi-step workflow with clear dependencies. For Activity 2.4 (Parallel Exploration), look for: (1) Multiple approach prompts (A, B, C) that generate alternatives, (2) Evaluation prompt with weighted criteria to compare approaches, (3) Selection logic to pick the best. Sequential and self-correction patterns are also valid.",
    }

    # Only include expected tactics in the evaluation criteria
    criteria_list = []
    for i, tactic in enumerate(expected_tactics, 1):
        if tactic in tactic_descriptions:
            criteria_list.append(f"{i}. **{tactic}**: {tactic_descriptions[tactic]}")

    criteria_text = "\n".join(criteria_list)

    # STEP 3: Quality Assessment (Subjective & Nuanced) with Confidence Scores
    evaluation_prompt = f"""You are an expert prompt engineering instructor evaluating a student's work.

<traditional_metrics>
{metrics_summary}
</traditional_metrics>

<student_prompt>
{prompt_text}
</student_prompt>

<expected_tactics>
{', '.join(expected_tactics)}
</expected_tactics>

<evaluation_criteria>
The traditional metrics above show WHAT patterns exist. Your job is to evaluate HOW WELL they're implemented.

Analyze whether the student successfully applied ONLY THE EXPECTED TACTICS listed above:

{criteria_text}

IMPORTANT: Only evaluate the tactics listed above. Do not evaluate other tactics that are not in the expected list.

Use the traditional metrics as a starting point, but evaluate the QUALITY and EFFECTIVENESS of implementation.
</evaluation_criteria>

For each expected tactic (and ONLY the expected tactics), provide:

**Tactic Name**: ✅/⚠️/❌ (Quality Score: X/10, Confidence: Y%)

**Evidence**: [Quote specific parts showing implementation]

**Quality Assessment**: [Why this score? What's good/what needs work?]

**Confidence Rationale**: [Why are you Y% confident in this assessment? What makes you more or less certain?]

**Improvement Suggestions**: [Specific actionable advice if score < 10]

---

CRITICAL FORMATTING REQUIREMENT: Your response MUST include ALL 4 sections below in the EXACT order shown.
Do NOT skip any section. Do NOT combine sections. Do NOT start with scores.
The response must follow this EXACT structure:

<evaluation>
**Tactic Name**: ✅/⚠️/❌ (Quality Score: X/10, Confidence: Y%)

**Evidence**: [Quote specific parts showing implementation]

**Quality Assessment**: [Why this score? What's good/what needs work?]

**Confidence Rationale**: [Why are you Y% confident in this assessment?]

**Improvement Suggestions**: [Specific actionable advice if score < 10]

---

[Repeat for each tactic]
</evaluation>

<skills_demonstrated>
List the specific skills (from Module 2 Skills Checklist) they can check off.

Activity skill mappings:
- Activity 2.1 (Role Prompting + Structured Inputs): Skills #1-4
- Activity 2.2 (Few-Shot + Chain-of-Thought): Skills #5-8
- Activity 2.3 (Reference Citations + Prompt Chaining): Skills #9-12
- Activity 2.4 (Parallel Exploration - Prompt Chaining Pattern 3): Skills #13-16

Based on the activity name and tactics evaluated, list appropriate skill numbers with specific descriptions.
Format: "- Skill #X: [Specific description of what the student demonstrated]"

Only list skills where the tactic received ✅ (8-10/10) or strong ⚠️ (7/10).

Example format:
- Skill #1: Created effective QA Engineer persona with specific expertise areas (Role Prompting)
- Skill #3: Used XML tags to organize test_file and source_code inputs (Structured Inputs)

IMPORTANT:
- Be specific about what the student did well in each skill description
- For Activity 2.4, use skills #13-16 and mention Parallel Exploration (Prompt Chaining Pattern 3)
- Include the tactic name in parentheses at the end of each skill
</skills_demonstrated>

<combined_score>
IMPORTANT: Complete ALL sections above BEFORE calculating scores.

Now calculate scores based on your evaluation:

1. Traditional Metrics = (tactics with pattern indicators / total tactics) * 100
2. Quality Assessment = average(quality scores from evaluation) * 10
3. Confidence Score = average(confidence % from evaluation)
4. Overall Score = (Traditional * 0.40) + (Quality * 0.60)

Note: Confidence is informational only - NOT included in overall score.

Output in EXACTLY this format:

Traditional Metrics: X/100
Quality Assessment: Y/100
Confidence Score: Z/100
Overall Score: W/100
</combined_score>

<overall_feedback>
Provide 3-4 sentences of encouraging, actionable feedback:
1. Strongest aspect demonstrated (be specific)
2. Most important area for improvement (with concrete suggestion)
3. One advanced technique to try next
4. Encouragement about their progress
</overall_feedback>
"""

    # Get AI evaluation
    evaluation_messages: List[MutableMapping[str, object]] = [{"role": "user", "content": evaluation_prompt}]
    llm_judgment = get_chat_completion(evaluation_messages)

    # STEP 4: Save to history (if enabled)
    if track_progress:
        try:
            # Extract scores from LLM judgment for history
            import re

            # Extract scores from the final output format (not from calculation steps)
            # Look for the final format lines: "Traditional Metrics: X/100", "Quality Assessment: Y/100", "Confidence Score: Z/100"

            # Extract Traditional Metrics score (final format only)
            traditional_match = re.search(r'Traditional\s+Metrics:\s*(\d+)/100', llm_judgment or "", re.IGNORECASE)
            traditional_score = int(traditional_match.group(1)) if traditional_match else 0

            # Extract Quality Assessment score (final format only)
            quality_match = re.search(r'Quality\s+Assessment:\s*(\d+)/100', llm_judgment or "", re.IGNORECASE)
            quality_score = int(quality_match.group(1)) if quality_match else 0

            # Extract Confidence Score (final format only)
            confidence_match = re.search(r'Confidence\s+Score:\s*(\d+)/100', llm_judgment or "", re.IGNORECASE)
            confidence_score = int(confidence_match.group(1)) if confidence_match else 0

            # Extract Overall/Combined score
            # Pattern 1: "Overall Score: 88/100" (enforced format)
            combined_match = re.search(r'Overall Score:\s*(\d+)/100', llm_judgment or "", re.IGNORECASE)

            # Fallback patterns for legacy/variant outputs
            if not combined_match:
                # Pattern 2: "Weighted Combined Score = ... = 81/100"
                combined_match = re.search(r'(?:Weighted Combined|Overall)\s+Score[:\s=]*.*?=\s*(\d+)/100', llm_judgment or "", re.IGNORECASE)
            if not combined_match:
                # Pattern 3: Any "= XX/100" at end of line
                combined_match = re.search(r'=\s*(\d+)/100\s*$', (llm_judgment or "").strip(), re.MULTILINE)

            combined_score = int(combined_match.group(1)) if combined_match else 70

            # Extract per-tactic scores with confidence
            tactic_scores = {}

            # Try to find quality scores with confidence (new format)
            for tactic in expected_tactics:
                # Pattern: **Tactic Name**: ... Quality Score: X/10, Confidence: Y%
                tactic_pattern = rf'\*\*{re.escape(tactic)}\*\*.*?Quality Score:\s*(\d+)/10.*?Confidence:\s*(\d+)%'
                match = re.search(tactic_pattern, llm_judgment or "", re.DOTALL | re.IGNORECASE)
                if match:
                    tactic_scores[tactic] = {
                        "quality": int(match.group(1)),
                        "confidence": int(match.group(2))
                    }

            # Fallback: try old format without confidence
            if not tactic_scores:
                for tactic in expected_tactics:
                    tactic_pattern = rf'{re.escape(tactic)}.*?(?:Quality Score|Quality|Score):\s*(\d+)/10'
                    match = re.search(tactic_pattern, llm_judgment or "", re.DOTALL | re.IGNORECASE)
                    if match:
                        tactic_scores[tactic] = {
                            "quality": int(match.group(1)),
                            "confidence": 85  # Default confidence
                        }

            # If no quality scores found, parse skills_demonstrated section
            if not tactic_scores:
                skills_section = re.search(r'<skills_demonstrated>(.*?)</skills_demonstrated>', llm_judgment or "", re.DOTALL | re.IGNORECASE)
                if skills_section:
                    skills_text = skills_section.group(1)
                    for tactic in expected_tactics:
                        # Check if tactic is mentioned in any skill line
                        if re.search(re.escape(tactic), skills_text, re.IGNORECASE):
                            # Tactic is demonstrated - mark as high quality (9/10)
                            tactic_scores[tactic] = {
                                "quality": 9,
                                "confidence": 90
                            }

            # Use extracted scores from LLM output
            # Fallback: calculate traditional metrics if not found in output
            if not traditional_score:
                tactic_presence = sum(1 for t in expected_tactics if metrics.get(f'uses_{t.lower().replace(" ", "_")}', False))
                traditional_score = (tactic_presence * 100 // len(expected_tactics)) if expected_tactics else 0

            # Fallback: use combined score if quality not found
            if not quality_score:
                quality_score = combined_score

            scores = {
                "combined_score": combined_score,
                "traditional_metrics": traditional_score,
                "llm_judge_quality": quality_score,
                "confidence_score": confidence_score
            }

            _save_evaluation_history(activity_name, scores, tactic_scores, {
                "tactics_evaluated": list(expected_tactics),
                "module": "Module 2"
            })
        except Exception:
            pass  # Silently fail progress tracking to not disrupt evaluation

    # STEP 5: Print Combined Results
    print("\n" + "=" * 70)
    print(f"📊 COMPREHENSIVE EVALUATION: {activity_name}")
    print("=" * 70)
    print(metrics_summary)
    print("\n👨‍⚖️ QUALITY ASSESSMENT (With Confidence Scores)")
    print("=" * 70)
    print(llm_judgment)
    print("\n" + "=" * 70)
    print("💡 Next Steps:")
    print("  1. Review traditional metrics (objective indicators)")
    print("  2. Read LLM judge feedback (quality + confidence assessment)")
    print("  3. Check specific skills you demonstrated in Skills Checklist")
    print("  4. Focus on high-confidence, low-score items first (clear improvements)")
    print("  5. For low-confidence items, seek clarification or examples")
    print("  6. Revise and re-evaluate to see score improvement")
    if track_progress:
        print(f"  7. View progress: view_progress('{activity_name}')")
    print("=" * 70)

    # Return full evaluation results only if requested
    if return_results:
        return {
            "activity_name": activity_name,
            "traditional_metrics": metrics,
            "llm_judgment": llm_judgment,
            "llm_judgment_sections": {
                "evaluation": _extract_section(llm_judgment, "evaluation"),
                "skills_demonstrated": _extract_section(llm_judgment, "skills_demonstrated"),
                "combined_score": _extract_section(llm_judgment, "combined_score"),
                "overall_feedback": _extract_section(llm_judgment, "overall_feedback"),
            }
        }
    return None


# ============================================
# 📊 PROGRESS TRACKING (Enhanced for Module 2)
# ============================================

def _save_evaluation_history(activity_name: str, scores: Mapping[str, object], tactic_scores: Mapping[str, object], eval_metadata: Mapping[str, object]) -> bool:
    """
    Save evaluation results to history for progress tracking.

    Args:
        activity_name: Name of the activity
        scores: Dictionary of overall scores
        tactic_scores: Dictionary of per-tactic scores
        eval_metadata: Additional metadata (timestamp, etc.)

    Returns:
        bool: True if saved successfully, False otherwise
    """
    try:
        import datetime
        import json
        from pathlib import Path

        # Create .eval_history directory if it doesn't exist
        history_dir = Path('.eval_history')
        history_dir.mkdir(exist_ok=True)

        # Create history entry
        timestamp = datetime.datetime.now().isoformat()
        history_entry = {
            "timestamp": timestamp,
            "activity": activity_name,
            "scores": scores,
            "tactic_scores": tactic_scores,
            "metadata": eval_metadata
        }

        # Append to history file (one JSON object per line)
        history_file = history_dir / f"{activity_name.replace(' ', '_').lower()}_history.jsonl"
        with open(history_file, 'a') as f:
            f.write(json.dumps(history_entry) + '\n')

        return True
    except Exception as e:
        print(f"⚠️ Could not save evaluation history: {e}")
        return False


def view_progress(activity_name: Optional[str] = None) -> None:
    """
    View evaluation progress over time.

    Args:
        activity_name: Optional - filter to specific activity, or None for all

    Example:
        >>> view_progress("Activity 2.1")  # View specific activity
        >>> view_progress()  # View all activities
    """
    try:
        import json
        from pathlib import Path

        history_dir = Path('.eval_history')
        if not history_dir.exists():
            print("📊 No evaluation history found yet.")
            print("💡 Complete an activity evaluation to start tracking progress!")
            return

        # Load all history files
        all_evaluations: List[MutableMapping[str, object]] = []
        pattern = f"{activity_name.replace(' ', '_').lower()}_history.jsonl" if activity_name else "*.jsonl"

        for history_file in history_dir.glob(pattern):
            with open(history_file, 'r') as f:
                for line in f:
                    if line.strip():
                        all_evaluations.append(json.loads(line))

        if not all_evaluations:
            print(f"📊 No evaluation history found for: {activity_name or 'any activity'}")
            return

        # Sort by timestamp
        all_evaluations.sort(key=lambda x: x['timestamp'])  # type: ignore

        print("="*70)
        print(f"📊 EVALUATION PROGRESS{' - ' + activity_name if activity_name else ''}")
        print("="*70)
        print("\nℹ️  Score Formula: (Traditional × 0.40) + (Quality × 0.60)")
        print("   Confidence scores shown below are informational only\n")

        for i, eval_entry in enumerate(all_evaluations, 1):
            timestamp = str(eval_entry['timestamp'])[:19].replace('T', ' ')
            activity = eval_entry['activity']
            scores = eval_entry['scores']  # type: ignore
            combined = scores.get('combined_score', 0)  # type: ignore

            print(f"\n{i}. {activity} - {timestamp}")
            print(f"   Combined Score: {combined}/100", end='')

            # Show achievement badge if score >= 80
            if isinstance(combined, (int, float)) and combined >= 80:
                print(" 🏆 SKILLS ACQUIRED!")
            else:
                print()

            print(f"   • Traditional Metrics: {scores.get('traditional_metrics', 'N/A')}/100 (40% weight)")  # type: ignore
            print(f"   • LLM Judge Quality: {scores.get('llm_judge_quality', 'N/A')}/100 (60% weight)")  # type: ignore
            if 'confidence_score' in scores and scores['confidence_score']:  # type: ignore
                print(f"   • Confidence Score: {scores.get('confidence_score', 'N/A')}/100 (info only)")  # type: ignore

            # Show skills acquired for passing scores
            if isinstance(combined, (int, float)) and combined >= 80:
                tactic_scores = eval_entry.get('tactic_scores', {})  # type: ignore
                if tactic_scores:
                    print(f"   ✅ Skills Mastered:")
                    for tactic, tactic_data in tactic_scores.items():  # type: ignore
                        quality = tactic_data.get('quality', 0)  # type: ignore
                        confidence = tactic_data.get('confidence', 0)  # type: ignore
                        if quality >= 8:  # High quality (8-10/10)
                            if confidence:
                                print(f"      • {tactic} (Quality: {quality}/10, Confidence: {confidence}%)")
                            else:
                                print(f"      • {tactic} (Quality: {quality}/10)")

        print("\n" + "="*70)
        print(f"Total Evaluations: {len(all_evaluations)}")

        # Show improvement trend if multiple evaluations
        if len(all_evaluations) >= 2:
            first_score = all_evaluations[0]['scores'].get('combined_score', 0)  # type: ignore
            last_score = all_evaluations[-1]['scores'].get('combined_score', 0)  # type: ignore

            # Handle potential type issues
            try:
                if isinstance(first_score, str):
                    first_score = float(first_score)
                if isinstance(last_score, str):
                    last_score = float(last_score)

                improvement = last_score - first_score

                if improvement > 0:
                    print(f"📈 Improvement: +{improvement:.1f} points since first attempt!")
                elif improvement < 0:
                    print(f"📉 Change: {improvement:.1f} points since first attempt")
                else:
                    print(f"➡️  Score unchanged since first attempt")
            except (ValueError, TypeError):
                pass  # Skip improvement calculation if scores aren't numeric

        print("="*70)

    except Exception as e:
        print(f"❌ Error loading progress: {e}")


# ============================================
# 📦 MODULE REGISTRATION
# ============================================

__all__ = [
    "AVAILABLE_PROVIDERS",
    "CLAUDE_DEFAULT_MODEL",
    "CIRCUIT_DEFAULT_MODEL",
    "OPENAI_DEFAULT_MODEL",
    "configure_circuit_from_env",
    "configure_openai_from_env",
    "evaluate_prompt",
    "view_progress",
    "get_chat_completion",
    "get_chat_completion_async",
    "get_claude_completion",
    "get_circuit_completion",
    "get_default_model",
    "get_openai_completion",
    "get_provider",
    "read_markdown",
    "run_async",
    "save_markdown",
    "set_provider",
    "test_connection",
]

# Allow notebooks to check that setup has been imported
import sys

sys.modules["__module2_setup__"] = sys.modules[__name__]

print("✅ Module 2 setup utilities loaded successfully!")
print(f"🤖 Provider: {get_provider().upper()}")
print(f"📝 Default model: {get_default_model()}")
