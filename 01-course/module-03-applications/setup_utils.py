"""
Module 3: Shared Setup Utilities
This file contains all setup code to avoid repetition across notebooks.
Run setup once, then import these functions in any notebook.
"""

import os
import re
import json
from pathlib import Path

# Load .env file FIRST before reading environment variables
try:
    from dotenv import load_dotenv
    # Try loading .env from project root (three levels up from this file)
    env_path = Path(__file__).parent.parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path, override=True)  # override=True ensures .env values take precedence
except ImportError:
    pass  # dotenv not available, skip loading

import anthropic
import openai

# ============================================
# 🎯 CONFIGURATION
# ============================================

AVAILABLE_PROVIDERS = ("openai", "claude", "circuit")

# Set your preference: "openai", "claude", or "circuit"
# Can be overridden via environment variable
PROVIDER = os.getenv("MODULE3_PROVIDER", "claude").lower()

# Available models by provider (customisable via environment variables)
OPENAI_DEFAULT_MODEL = os.getenv("MODULE3_OPENAI_MODEL", "gpt-5")  # Works with OpenAI API, GitHub Copilot
CIRCUIT_DEFAULT_MODEL = os.getenv("MODULE3_CIRCUIT_MODEL", "gpt-4.1")  # Free tier (also: gpt-4o-mini, or gpt-4o with paid access)
CLAUDE_DEFAULT_MODEL = os.getenv("MODULE3_CLAUDE_MODEL", "claude-sonnet-4")

# ============================================
# 🤖 AI CLIENT INITIALIZATION
# ============================================

# OPTION A: GitHub Copilot Proxy (Default - Recommended for Course)
# Use local proxy that routes through GitHub Copilot
# Supports both OpenAI and Claude models via single proxy
# GitHub Copilot proxy defaults (can be overridden via environment variables)
_MODULE3_OPENAI_BASE_URL = os.getenv("MODULE3_OPENAI_BASE_URL", "http://localhost:7711/v1")
_MODULE3_CLAUDE_BASE_URL = os.getenv("MODULE3_CLAUDE_BASE_URL", "http://localhost:7711")
_MODULE3_PROXY_API_KEY = os.getenv("MODULE3_PROXY_API_KEY", "dummy-key")

# Initialize clients AFTER loading .env to ensure correct configuration
openai_client = openai.OpenAI(
    base_url=_MODULE3_OPENAI_BASE_URL,
    api_key=_MODULE3_PROXY_API_KEY
)

claude_client = anthropic.Anthropic(
    api_key=_MODULE3_PROXY_API_KEY,
    base_url=_MODULE3_CLAUDE_BASE_URL
)

# Placeholder for CircuIT client (will be set if Option C is uncommented)
circuit_client = None
circuit_app_key = None

# OPTION B: Direct OpenAI API
# IMPORTANT: Comment out Option A (lines 27-38) before using this option
# Setup: Add your API key to .env file, then uncomment and run
# from dotenv import load_dotenv
# 
# load_dotenv()
# 
# openai_client = openai.OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY")  # Set this in your .env file
# )
# 


# OPTION C: CircuIT APIs (Azure OpenAI)
# IMPORTANT: Comment out Option A (lines 27-38) before using this option
# Supported models: gpt-4, gpt-4.1, gpt-4o-mini (free tier), gpt-4o (paid access)
# Setup: Configure environment variables in .env file:
#   - CISCO_CLIENT_ID
#   - CISCO_CLIENT_SECRET  
#   - CISCO_OPENAI_APP_KEY
# Get values from: https://ai-chat.cisco.com/bridgeit-platform/api/home
# Then uncomment and run (also change PROVIDER to "circuit" at the top):
# import traceback
# import requests
# import base64
# from dotenv import load_dotenv
# from openai import AzureOpenAI
# 
# # Load environment variables
# load_dotenv()
# 
# # OpenAI version to use
# openai.api_type = "azure"
# openai.api_version = "2024-12-01-preview"
# 
# # Get API_KEY wrapped in token - using environment variables
# client_id = os.getenv("CISCO_CLIENT_ID")
# client_secret = os.getenv("CISCO_CLIENT_SECRET")
# 
# url = "https://id.cisco.com/oauth2/default/v1/token"
# 
# payload = "grant_type=client_credentials"
# value = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")
# headers = {
#     "Accept": "*/*",
#     "Content-Type": "application/x-www-form-urlencoded",
#     "Authorization": f"Basic {value}",
# }
# 
# token_response = requests.request("POST", url, headers=headers, data=payload)
# print(token_response.text)
# token_data = token_response.json()
# 
# circuit_client = AzureOpenAI(
#     azure_endpoint="https://chat-ai.cisco.com",
#     api_key=token_data.get("access_token"),
#     api_version="2024-12-01-preview",
# )
# 
# circuit_app_key = os.getenv("CISCO_OPENAI_APP_KEY")
# 
# print("✅ CircuIT API configured successfully!")


# ============================================
# 🔧 HELPER FUNCTIONS
# ============================================

def _extract_text_from_blocks(blocks):
    """Extract text content from response blocks returned by the API."""
    parts = []
    for block in blocks:
        text_val = getattr(block, "text", None)
        if isinstance(text_val, str):
            parts.append(text_val)
        elif isinstance(block, dict):
            t = block.get("text")
            if isinstance(t, str):
                parts.append(t)
    return "\n".join(parts)


def get_openai_completion(messages, model=None, temperature=0.0):
    """Get completion from OpenAI models via GitHub Copilot."""
    if model is None:
        model = OPENAI_DEFAULT_MODEL
    try:
        # GPT-5 doesn't support temperature parameter
        kwargs = {
            "model": model,
            "messages": messages,
        }
        if not model.lower().startswith("gpt-5"):
            kwargs["temperature"] = temperature
        
        response = openai_client.chat.completions.create(**kwargs)
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}\n💡 Make sure GitHub Copilot proxy is running on port 7711"


def get_claude_completion(messages, model=None, temperature=0.0):
    """Get completion from Claude models via GitHub Copilot."""
    if model is None:
        model = CLAUDE_DEFAULT_MODEL
    try:
        response = claude_client.messages.create(
            model=model,
            max_tokens=8192,
            messages=messages,
            temperature=temperature
        )
        return _extract_text_from_blocks(getattr(response, "content", []))
    except Exception as e:
        return f"❌ Error: {e}\n💡 Make sure GitHub Copilot proxy is running on port 7711"


def get_circuit_completion(messages, model=None, temperature=0.0):
    """Get completion from CircuIT APIs (Azure OpenAI via Cisco)."""
    if circuit_client is None or circuit_app_key is None:
        return "❌ Error: CircuIT not configured\n💡 Uncomment Option C in setup_utils.py and set your CircuIT credentials"
    
    if model is None:
        model = CIRCUIT_DEFAULT_MODEL
    try:
        response = circuit_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            user=f'{{"appkey": "{circuit_app_key}"}}'  # CircuIT requires app_key in user field
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}\n💡 Check your CircuIT credentials and connection"


def get_chat_completion(messages, model=None, temperature=0.0):
    """
    Generic function to get chat completion from any provider.
    Routes to the appropriate provider-specific function based on PROVIDER setting.
    """
    # print(f"Using {PROVIDER.upper()} with {get_default_model()}")

    if PROVIDER.lower() == "claude":
        return get_claude_completion(messages, model, temperature)
    elif PROVIDER.lower() == "circuit":
        return get_circuit_completion(messages, model, temperature)
    else:  # Default to OpenAI
        return get_openai_completion(messages, model, temperature)


def get_default_model():
    """Get the default model for the current provider."""
    if PROVIDER.lower() == "claude":
        return CLAUDE_DEFAULT_MODEL
    elif PROVIDER.lower() == "circuit":
        return CIRCUIT_DEFAULT_MODEL
    else:  # Default to OpenAI
        return OPENAI_DEFAULT_MODEL


def get_provider():
    """Return the currently configured provider."""
    return PROVIDER


def set_provider(provider_name):
    """Set the active provider for requests."""
    provider_normalized = provider_name.lower()
    if provider_normalized not in AVAILABLE_PROVIDERS:
        raise ValueError(f"Unknown provider '{provider_name}'. Choose from {AVAILABLE_PROVIDERS}.")
    global PROVIDER
    PROVIDER = provider_normalized
    return PROVIDER


def configure_openai_from_env(api_key_env="OPENAI_API_KEY"):
    """
    Configure the OpenAI client directly using an API key from the environment.

    1. Add your key to `.env` (or export it in your shell)
    2. Run `configure_openai_from_env()` in a notebook cell
    3. Optionally call `set_provider("openai")` if you want to switch providers
    """
    try:
        from dotenv import load_dotenv
    except ImportError as exc:
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
    print("✅ OpenAI API configured successfully!")
    return openai_client


def configure_circuit_from_env():
    """
    Configure CircuIT (Azure OpenAI) access using the environment variables:

    - CISCO_CLIENT_ID
    - CISCO_CLIENT_SECRET
    - CISCO_OPENAI_APP_KEY

    These values can be generated from https://ai-chat.cisco.com/bridgeit-platform/api/home
    """
    try:
        from dotenv import load_dotenv
    except ImportError as exc:
        raise RuntimeError("python-dotenv is required for configure_circuit_from_env") from exc

    try:
        import requests
        import base64
        from openai import AzureOpenAI
    except ImportError as exc:
        raise RuntimeError("requests and openai[azure] are required for CircuIT configuration") from exc

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
    print("✅ CircuIT API configured successfully!")
    return client


# ============================================
# 🧪 ACTIVITY and SOLUTION TESTING FUNCTIONS
# ============================================

def extract_template_from_activity(activity_file):
    """
    Extract the prompt template from an activity markdown file.
    Looks for content between: <!-- TEMPLATE START --> and <!-- TEMPLATE END -->
    
    Args:
        activity_file: Path to the activity .md file
        
    Returns:
        tuple: (template_text, error_message)
    """
    try:
        file_path = Path(activity_file)
        if not file_path.exists():
            return None, f"❌ File not found: {activity_file}"
        
        if file_path.suffix == ".ipynb":
            try:
                notebook = json.loads(file_path.read_text())
            except json.JSONDecodeError as e:
                return None, f"❌ Error decoding notebook JSON: {e}"
            
            for cell in notebook.get("cells", []):
                if cell.get("cell_type") != "markdown":
                    continue
                source = "".join(cell.get("source", []))
                match = re.search(
                    r'<!-- TEMPLATE START -->(.*?)<!-- TEMPLATE END -->',
                    source,
                    re.DOTALL
                )
                if match:
                    template = match.group(1).strip()
                    return template, None
            return None, "⚠️ Template markers not found in notebook markdown cells. Make sure your template is between:\n   <!-- TEMPLATE START -->\n   <!-- TEMPLATE END -->"
        
        content = file_path.read_text()
        match = re.search(
            r'<!-- TEMPLATE START -->(.*?)<!-- TEMPLATE END -->',
            content,
            re.DOTALL
        )
        
        if match:
            template = match.group(1).strip()
            return template, None
        else:
            return None, "⚠️ Template markers not found. Make sure your template is between:\n   <!-- TEMPLATE START -->\n   <!-- TEMPLATE END -->"
            
    except Exception as e:
        return None, f"❌ Error reading file: {e}"


def test_activity(activity_file, test_code=None, variables=None, auto_save=True):
    """
    Test your activity template directly from the .md file.
    
    IMPORTANT: Complete your activity template BEFORE running this function!
    - Open the activity file (e.g., 'activities/activity-3.2-code-review.md')
    - Replace all <!-- TODO: ... --> comments with your actual content
    - Fill in role, guidelines, tasks, and output format sections
    - Save the file, then run this test function
    
    Args:
        activity_file: Path to your activity file (e.g., 'activities/activity-3.2-code-review.md')
        test_code: Optional code sample to review (uses example from file if not provided)
        variables: Optional dict of template variables (e.g., {'tech_stack': 'Python', 'repo_name': 'my-app'})
        auto_save: If True, prompts to save result back to activity file
    
    Returns:
        The AI's response
    """
    print("="*70)
    print("🧪 TESTING YOUR ACTIVITY TEMPLATE")
    print("="*70)
    print("\n⚠️  REMINDER: Make sure you've completed your template first!")
    print("   (Replace all <!-- TODO: ... --> comments with actual content)")
    
    # Extract template
    print(f"\n📖 Reading template from: {activity_file}")
    template, error = extract_template_from_activity(activity_file)
    
    if error or template is None:
        print(error if error else "❌ Error: Template extraction failed")
        return None
    
    print("✅ Template loaded successfully!")
    print(f"📏 Template length: {len(template)} characters\n")
    
    # Substitute variables if provided
    if variables:
        print("🔄 Substituting template variables...")
        for key, value in variables.items():
            placeholder = "{{" + key + "}}"
            template = template.replace(placeholder, str(value))
            print(f"   • {placeholder} → {value}")
        print()
    
    # Add test code if provided
    if test_code:
        print("📝 Using provided test code\n")
        # Replace common placeholders
        template = template.replace("{{code_diff}}", test_code)
        template = template.replace("{{code}}", test_code)
        template = template.replace("{{code_sample}}", test_code)
    
    # Execute prompt
    print("🤖 Sending to AI model...")
    print("-"*70)
    
    try:
        messages = [{"role": "user", "content": template}]
        response = get_chat_completion(messages)
        
        # Check if response contains error message
        if response and ("❌ Error" in response or "Error:" in response):
            print("\n" + response)
            print("-"*70)
            print("\n⚠️ AI request failed. Please check:")
            print("   • GitHub Copilot proxy is running (for Option A)")
            print("   • API keys are configured correctly (for Options B/C)")
            print("   • PROVIDER setting matches your active option")
            print("   • Template contains valid content")
            return None
        
        print(response)
        print("-"*70)
        
        # Save result back to activity file
        if auto_save and response:
            print("\n" + "="*70)
            print("📝 SAVE RESULT")
            print("="*70)
            print("⬆️  LOOK AT THE TOP OF YOUR IDE FOR THE INPUT BOX! ⬆️")
            print("    Type 'y' or 'n' in the input field at the top of the screen")
            print("="*70)
            try:
                save_result = input("💾 Save this result to your activity file? (y/n): ")
                if save_result.lower() == 'y':
                    save_test_result(activity_file, test_code, response)
                    print("✅ Result saved to activity file!")
                else:
                    print("⏭️  Result not saved. You can run this test again anytime.")
            except Exception as save_error:
                print(f"⚠️ Could not save result: {save_error}")
        
        return response
        
    except Exception as e:
        print(f"\n❌ Unexpected error during AI request: {e}")
        print("-"*70)
        print("\n💡 Troubleshooting:")
        print("   • Verify your API configuration is correct")
        print("   • Check that template placeholders are properly filled")
        print("   • Ensure your selected provider is available")
        return None


def save_test_result(activity_file, test_code, response):  # noqa: ARG001
    """Save test results back to the activity file."""
    file_path = Path(activity_file)
    content = file_path.read_text()
    original_content = content

    # Find the test results section and update it
    timestamp = __import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cleaned_response = response.strip()
    result_block = (
        f"<!-- TEST RESULT - Last Updated: {timestamp} -->\n"
        f"{cleaned_response}\n"
        f"<!-- TEST RESULT END -->"
    )
    updated = False

    # Replace existing result or insert after "Your template's output:"
    if '<!-- TEST RESULT' in content:
        content = re.sub(
            r'<!-- TEST RESULT.*?TEST RESULT END -->',
            result_block,
            content,
            flags=re.DOTALL
        )
        updated = True
    else:
        # Find where to insert (after various possible markers)
        patterns = [
            r"(\*\*Your template's output:\*\*\s*```[^\n]*\n)",
            r"(\*\*Output:\*\*\s*```[^\n]*\n)",
            r"(### Test Results\s*\n)"
        ]
        for pattern in patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, r'\1' + result_block + '\n', content)
                updated = True
                break

    if not updated:
        # Append a new Test Results section at the end if no markers were found
        append_block = "\n\n### Test Results\n" + result_block + "\n"
        content = content.rstrip() + append_block
        updated = True

    if content == original_content:
        raise RuntimeError("No changes were applied while attempting to save the test result.")

    file_path.write_text(content)


def list_activities():
    """Show available activities to test."""
    activities_dir = Path('activities')
    
    if not activities_dir.exists():
        print("❌ Activities directory not found")
        print("💡 Make sure you're running from the module-03-applications directory")
        return
    
    print("="*70)
    print("📚 AVAILABLE ACTIVITIES")
    print("="*70)
    
    activity_files = sorted(activities_dir.glob('activity-*.md'))
    
    if not activity_files:
        print("⚠️ No activity files found")
        return
    
    for i, file in enumerate(activity_files, 1):
        # Extract title from file
        try:
            content = file.read_text()
            title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
            title = title_match.group(1) if title_match else file.name
            
            print(f"{i}. {file.name}")
            print(f"   {title}")
            print()
        except:
            print(f"{i}. {file.name}")
            print()
    
    print("="*70)
    print("💡 Usage: test_activity('activities/activity-3.2-code-review.md')")


# Quick access functions for each activity
def test_activity_3_2(test_code=None, variables=None):
    """
    Quick helper for Activity 3.2: Comprehensive Code Review
    
    IMPORTANT: Complete your template in the activity file BEFORE running this!
    """
    return test_activity('activities/activity-3.2-code-review.md', test_code=test_code, variables=variables)


def test_activity_3_2_solution(test_code=None, variables=None):
    """
    Test the provided solution for Activity 3.2: Comprehensive Code Review
    
    Use this to see how the solution template works before building your own.
    Note: auto_save is disabled for solution files to keep them as clean references.
    """
    return test_activity('solutions/activity-3.2-code-review-solution.md', test_code=test_code, variables=variables, auto_save=False)


def test_activity_3_3(test_code=None, variables=None):
    """
    Quick helper for Activity 3.3: Test Generation
    
    IMPORTANT: Complete your template in the activity file BEFORE running this!
    """
    return test_activity('activities/activity-3.3-test-generation.md', test_code=test_code, variables=variables)


def test_activity_3_3_solution(test_code=None, variables=None):
    """
    Test the provided solution for Activity 3.3: Test Generation
    
    Use this to see how the solution template works before building your own.
    Note: auto_save is disabled for solution files to keep them as clean references.
    """
    return test_activity('solutions/activity-3.3-test-generation-solution.md', test_code=test_code, variables=variables, auto_save=False)


def get_refactor_judge_scenario():
    """
    Returns the complete scenario data for Activity 3.4 judge testing.
    This keeps the notebook clean while providing all necessary test data.
    """
    return {
        'service_name': 'Ledger API',
        'refactor_brief': 'Refactor cache service to extract eviction policy while preserving metrics and alerts.',
        'code_before': 'def get_session(key, cache, stats):\n    if key in cache:\n        stats[\'hits\'] += 1\n        return cache[key]\n    stats[\'misses\'] += 1\n    value = load_from_store(key)\n    if len(cache) > 5000:\n        evict_oldest(cache, stats)\n    cache[key] = value\n    stats[\'writes\'] += 1\n    return value',
        'code_after': 'def get_session(key, cache, stats):\n    cached = cache.get(key)\n    if cached is not None:\n        stats[\'hits\'] += 1\n        return cached\n    stats[\'misses\'] += 1\n    value = load_from_store(key)\n    maybe_evict(cache, stats)\n    cache[key] = value\n    stats[\'writes\'] += 1\n    return value',
        'refactor_goal': 'Reduce duplicate eviction logic, tighten cache branch handling, keep behaviour identical.',
        'test_summary': 'pytest::tests/cache/test_session.py::TestCacheSession PASSED; contract-suite pending',
        'analysis_findings': 'ruff: clean; bandit: clean; mypy: missing return type for maybe_evict',
        'critical_regression': 'Eviction stats update removed for rare eviction branch',
        'security_findings': 'None observed',
        'escalation_channel': '#refactor-review',
        'ai_refactor_output': '''Refactored code extracts eviction logic into _ensure_cache_capacity helper.

Key changes:
- Extracted eviction condition into helper function
- Replaced direct key lookup with cache.get()
- Added docstrings clarifying behavior
- Preserved all stats counter mutations

Regression risks:
- Eviction semantics must preserve > 5000 threshold (not >=)
- Cache hit path: only stats['hits'] increments
- Cache miss: stats['misses'] and stats['writes'] both increment
- Exception path: stats['writes'] must not increment if load_from_store fails

Suggested test cases:
- test_hit_increments_hits_only()
- test_miss_increments_misses_and_writes()
- test_no_eviction_at_threshold()
- test_eviction_when_exceeding_threshold()
- test_exception_does_not_write()
'''
    }


def test_activity_3_4(test_code=None, variables=None):
    """
    Quick helper for Activity 3.4: Evaluation Template Quality Gate.
    
    IMPORTANT: Complete your template in the activity notebook BEFORE running this!
    
    Usage:
        # Use default scenario
        test_activity_3_4(variables=get_refactor_judge_scenario())
        
        # Or provide your own
        test_activity_3_4(variables={...})
    """
    return test_activity('activities/activity-3.4-evaluation-templates.md', test_code=test_code, variables=variables)


def test_activity_3_4_solution(test_code=None, variables=None):
    """
    Test the provided solution for Activity 3.4: Evaluation Template.
    
    Use this to see the reference implementation before finalising your own.
    Note: auto_save is disabled for solution files so they remain untouched.
    
    Usage:
        # Use default scenario
        test_activity_3_4_solution(variables=get_refactor_judge_scenario())
    """
    return test_activity('solutions/activity-3.4-evaluation-templates-solution.md', test_code=test_code, variables=variables, auto_save=False)


def test_activity_3_1(test_code=None, variables=None):
    """
    Backwards-compatible helper for the former Activity 3.1 (now Activity 3.2).
    """
    print("⚠️ Activity 3.1 has been renumbered to Activity 3.2. Routing to test_activity_3_2().")
    return test_activity_3_2(test_code=test_code, variables=variables)


def test_activity_3_1_solution(test_code=None, variables=None):
    """
    Backwards-compatible helper for the former Activity 3.1 solution (now Activity 3.2).
    """
    print("⚠️ Activity 3.1 solution has been renumbered to Activity 3.2. Routing to test_activity_3_2_solution().")
    return test_activity_3_2_solution(test_code=test_code, variables=variables)


# ============================================
# 🧪 CONNECTION TEST
# ============================================

# ============================================
# 📊 PROMPT EVALUATION (Enhanced with Module 3 features)
# ============================================

def _extract_section(text, section_name):
    """Extract content between XML-style tags."""
    import re
    pattern = rf'<{section_name}>(.*?)</{section_name}>'
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""


def _calculate_traditional_metrics(messages, expected_tactics):  # noqa: ARG001
    """
    Calculate objective, quantitative metrics for prompt evaluation.

    Args:
        messages: List of message dictionaries or string representation
        expected_tactics: List of tactics that should be present

    Returns:
        Dictionary with metric scores and evidence
    """
    # Handle both message format and string format
    if isinstance(messages, str):
        prompt_text = messages
    else:
        prompt_text = str(messages)

    metrics = {}

    # 1. Structure Detection
    has_system_message = "role" in prompt_text.lower() and "system" in prompt_text.lower()
    if isinstance(messages, list):
        has_system_message = any(msg.get("role") == "system" for msg in messages)
    metrics["has_system_message"] = has_system_message

    # 2. XML Tag Detection (for structured inputs)
    xml_tags = []
    common_tags = ["code", "requirements", "context", "example", "document", "thinking", "output",
                   "test_file", "source_code", "analysis", "quotes", "evaluation", "role", "guidelines",
                   "tasks", "code_diff", "rubric", "criterion", "judge_profile"]
    for tag in common_tags:
        if f"<{tag}>" in prompt_text.lower():
            xml_tags.append(tag)
    metrics["xml_tags_found"] = xml_tags
    metrics["uses_xml_structure"] = len(xml_tags) > 0

    # 3. Few-Shot Pattern Detection
    if isinstance(messages, list):
        assistant_messages = [msg for msg in messages if msg.get("role") == "assistant"]
        # Also check for examples in content (e.g., "EXAMPLE 1:", "Example:", etc.)
        example_keywords = ["example 1:", "example 2:", "example 3:", "example:"]
        example_count_in_content = sum(1 for kw in example_keywords if kw in prompt_text.lower())
        # Check for <example> XML tags
        example_tag_count = prompt_text.lower().count("<example>")
        # Use the highest count (assistant messages, inline examples, or XML tags)
        metrics["example_count"] = max(len(assistant_messages), example_count_in_content, example_tag_count)
        metrics["uses_few_shot"] = metrics["example_count"] >= 2
    else:
        example_indicators = prompt_text.lower().count("example:")
        metrics["example_count"] = example_indicators
        metrics["uses_few_shot"] = example_indicators >= 2

    # 4. Chain-of-Thought Keywords
    cot_keywords = ["step-by-step", "think through", "reasoning", "analyze", "before", "first", "then", "step 1", "step 2"]
    cot_found = [kw for kw in cot_keywords if kw in prompt_text.lower()]
    metrics["cot_keywords_found"] = cot_found
    metrics["uses_cot"] = len(cot_found) > 0

    # 5. Role Prompting Detection
    role_indicators = ["you are a", "you are an", "act as", "role:", "persona:", "senior", "engineer", "specialist"]
    role_found = [ind for ind in role_indicators if ind in prompt_text.lower()]
    metrics["role_indicators"] = role_found
    metrics["uses_role_prompting"] = len(role_found) > 0

    # 6. Tree of Thoughts Detection (multiple approaches/alternatives)
    tot_keywords = ["approach a", "approach b", "approach c", "alternative", "option 1", "option 2", "multiple approaches", "different solutions"]
    tot_tags = ["<approach_a>", "<approach_b>", "<approach_c>", "<option_1>", "<option_2>", "<alternative_"]
    tot_found = [kw for kw in tot_keywords if kw in prompt_text.lower()]
    tot_tags_found = [tag for tag in tot_tags if tag in prompt_text.lower()]
    metrics["tot_keywords_found"] = tot_found + tot_tags_found
    metrics["uses_tree_of_thoughts"] = len(tot_found) >= 2 or len(tot_tags_found) >= 2

    # 7. Evaluation Rubric Detection (evaluation rubrics, scoring, weighted criteria)
    judge_keywords = ["rubric", "evaluate", "score", "rate", "criteria", "weighted", "judge", "assessment", "compare", "0-10", "1-10", "verdict", "weight"]
    judge_found = [kw for kw in judge_keywords if kw in prompt_text.lower()]
    has_percentages = "%" in prompt_text
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


def _calculate_semantic_similarity(student_template, reference_template, activity_name):
    """
    Calculate semantic similarity between student and reference templates.
    Uses LLM to perform deep semantic comparison.

    Args:
        student_template: Student's prompt template (string)
        reference_template: Reference solution template (string)
        activity_name: Name of the activity for context

    Returns:
        Dictionary with similarity scores and detailed comparison
    """
    similarity_prompt = f"""You are an expert prompt engineering evaluator. Compare the student's template against the reference solution.

<activity>
{activity_name}
</activity>

<student_template>
{student_template[:2000]}  # Limit to 2000 chars for efficiency
</student_template>

<reference_template>
{reference_template[:2000]}  # Limit to 2000 chars for efficiency
</reference_template>

Analyze semantic similarity across these dimensions:

1. **Role Definition** (0-100%): How closely does the student's role match the reference's intent and expertise areas?
2. **Guidelines Completeness** (0-100%): Are all critical review dimensions/criteria covered?
3. **Output Structure** (0-100%): Does the output format match the reference's organization and clarity?
4. **Task Workflow** (0-100%): Are the evaluation steps and reasoning process similar?

For each dimension, provide:
- **Score** (0-100%)
- **Evidence**: Quote specific parts showing alignment or gaps
- **Gap Analysis**: What's missing compared to the reference?

Format your response as:

<similarity_analysis>
**Role Definition**: X%
Evidence: [Quote from both]
Gap Analysis: [What's different]

**Guidelines Completeness**: X%
Evidence: [Quote from both]
Gap Analysis: [What's different]

**Output Structure**: X%
Evidence: [Quote from both]
Gap Analysis: [What's different]

**Task Workflow**: X%
Evidence: [Quote from both]
Gap Analysis: [What's different]

**Overall Semantic Similarity**: X% (average of above)
**Key Strengths**: [What student did well]
**Critical Gaps**: [Most important missing elements]
</similarity_analysis>"""

    try:
        messages = [{"role": "user", "content": similarity_prompt}]
        response = get_chat_completion(messages, temperature=0.0)

        # Extract overall similarity score
        import re
        overall_match = re.search(r'\*\*Overall Semantic Similarity\*\*:\s*(\d+)%', response or "")
        overall_score = int(overall_match.group(1)) if overall_match else 50

        return {
            "overall_similarity": overall_score,
            "detailed_analysis": response,
            "has_reference": True
        }
    except Exception as e:
        return {
            "overall_similarity": 0,
            "detailed_analysis": f"Error calculating similarity: {e}",
            "has_reference": False
        }


def _load_reference_template(activity_file):
    """
    Load the corresponding reference solution template for an activity.

    Args:
        activity_file: Path to the activity file (e.g., 'activities/activity-3.2-code-review.md')

    Returns:
        tuple: (reference_template_text, solution_file_path) or (None, None) if not found
    """
    try:
        activity_path = Path(activity_file)

        # Determine solution file path
        # Convert 'activities/activity-3.2-code-review.md' -> 'solutions/activity-3.2-code-review-solution.md'
        solution_file = activity_path.name.replace('activity-', 'activity-').replace('.md', '-solution.md')
        solution_path = activity_path.parent.parent / 'solutions' / solution_file

        if not solution_path.exists():
            return None, None

        # Extract template from solution file
        template, error = extract_template_from_activity(str(solution_path))

        if error or not template:
            return None, None

        return template, str(solution_path)

    except Exception as e:
        print(f"⚠️ Could not load reference template: {e}")
        return None, None


def _save_evaluation_history(activity_name, scores, tactic_scores, eval_metadata):
    """
    Save evaluation results to history for progress tracking.

    Args:
        activity_name: Name of the activity
        scores: Dictionary of overall scores
        tactic_scores: Dictionary of per-tactic scores
        eval_metadata: Additional metadata (timestamp, etc.)
    """
    try:
        import datetime
        import json

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


def view_progress(activity_name=None):
    """
    View evaluation progress over time.

    Args:
        activity_name: Optional - filter to specific activity, or None for all
    """
    try:
        import json

        history_dir = Path('.eval_history')
        if not history_dir.exists():
            print("📊 No evaluation history found yet.")
            print("💡 Complete an activity evaluation to start tracking progress!")
            return

        # Load all history files
        all_evaluations = []
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
                        if quality >= 8:  # High quality (8-10/10)
                            print(f"      • {tactic} (Quality: {quality}/10)")
            if 'semantic_similarity' in scores:  # type: ignore
                print(f"   Semantic Similarity: {scores['semantic_similarity']}%")  # type: ignore

        print("\n" + "="*70)
        print(f"Total Evaluations: {len(all_evaluations)}")

        # Show improvement trend if multiple evaluations
        if len(all_evaluations) >= 2:
            first_score = all_evaluations[0]['scores'].get('combined_score', 0)  # type: ignore
            last_score = all_evaluations[-1]['scores'].get('combined_score', 0)  # type: ignore
            improvement = last_score - first_score  # type: ignore

            if improvement > 0:
                print(f"📈 Improvement: +{improvement} points since first attempt!")
            elif improvement < 0:
                print(f"📉 Change: {improvement} points since first attempt")
            else:
                print(f"➡️  Score unchanged since first attempt")

        print("="*70)

    except Exception as e:
        print(f"❌ Error loading progress: {e}")


def evaluate_prompt(
    messages,
    activity_name,
    expected_tactics,
    activity_file=None,
    compare_with_reference=True,
    track_progress=True,
    return_results=False
):
    """
    Enhanced evaluation combining Traditional Metrics + Quality Assessment + Semantic Similarity.

    This function provides comprehensive automated feedback by combining:
    1. Traditional metrics (40% weight): Objective, fast, deterministic pattern detection
    2. Quality Assessment (40% weight): Subjective, nuanced quality assessment with confidence scores
    3. Semantic Similarity (20% weight): Comparison against reference solution

    Args:
        messages: The student's prompt (list of dicts, string, or template text)
        activity_name: Name of the activity (e.g., "Activity 3.2")
        expected_tactics: List of tactics to evaluate (e.g., ["Role Prompting", "Structured Inputs"])
        activity_file: Optional path to activity file for reference comparison
        compare_with_reference: Whether to compare against reference solution (default: True)
        track_progress: Whether to save evaluation to history (default: True)
        return_results: Whether to return evaluation data dict (default: False)
                       Set to True if you want to inspect/save results programmatically

    Returns:
        None by default (prints output only)
        If return_results=True: Dictionary with evaluation data

    Example:
        >>> template = extract_template_from_activity('activities/activity-3.2-code-review.md')[0]
        >>> evaluate_prompt(
        ...     messages=template,
        ...     activity_name="Activity 3.2",
        ...     expected_tactics=["Role Prompting", "Structured Inputs", "Output Format"],
        ...     activity_file='activities/activity-3.2-code-review.md'
        ... )
    """

    # STEP 1: Calculate Traditional Metrics (Fast & Objective)
    print("\n🔍 Calculating traditional metrics...")
    metrics = _calculate_traditional_metrics(messages, expected_tactics)

    # Convert messages to string for LLM analysis
    if isinstance(messages, str):
        prompt_text = messages
    else:
        prompt_text = str(messages)

    # STEP 2: Semantic Similarity (if reference available)
    semantic_results = None
    if compare_with_reference and activity_file:
        print("🔄 Loading reference solution for comparison...")
        reference_template, solution_path = _load_reference_template(activity_file)

        if reference_template:
            print(f"✅ Reference loaded from: {solution_path}")
            print("🧠 Calculating semantic similarity...")
            semantic_results = _calculate_semantic_similarity(prompt_text, reference_template, activity_name)
        else:
            print("⚠️ Reference solution not found, skipping semantic comparison")

    # STEP 3: Format Traditional Metrics for Display
    xml_tags: list = metrics.get('xml_tags_found', [])  # type: ignore
    cot_keywords: list = metrics.get('cot_keywords_found', [])  # type: ignore
    role_indicators: list = metrics.get('role_indicators', [])  # type: ignore
    complexity = str(metrics.get('complexity', 'unknown'))
    tot_keywords: list = metrics.get('tot_keywords_found', [])  # type: ignore
    judge_keywords: list = metrics.get('judge_keywords_found', [])  # type: ignore

    # Build tactic detection lines dynamically based on expected_tactics
    tactic_mapping = {
        "Few-Shot Examples": f"- Few-shot examples: {metrics.get('example_count', 0)} examples {'✅' if metrics.get('uses_few_shot') else '❌'}",
        "Chain-of-Thought": f"- Chain-of-thought keywords: {', '.join(cot_keywords[:3]) if cot_keywords else 'None'}{' ...' if len(cot_keywords) > 3 else ''} {'✅' if metrics.get('uses_cot') else '❌'}",
        "Role Prompting": f"- Role indicators: {', '.join(role_indicators[:3]) if role_indicators else 'None'}{' ...' if len(role_indicators) > 3 else ''} {'✅' if metrics.get('uses_role_prompting') else '❌'}",
        "Tree of Thoughts": f"- Tree of Thoughts: {', '.join(tot_keywords[:3]) if tot_keywords else 'None'}{' ...' if len(tot_keywords) > 3 else ''} {'✅' if metrics.get('uses_tree_of_thoughts') else '❌'}",
        "Evaluation Rubric": f"- Evaluation rubric indicators: {', '.join(judge_keywords[:3]) if judge_keywords else 'None'}{' ...' if len(judge_keywords) > 3 else ''} {'✅' if metrics.get('uses_llm_as_judge') else '❌'}",
        "Reference Citations": f"- Document structure: {'✅ Yes' if metrics.get('uses_document_structure') else '❌ No'}",
        "Structured Inputs": f"- XML tags detected: {', '.join(xml_tags[:5]) if xml_tags else 'None'}{' ...' if len(xml_tags) > 5 else ''}\n- Uses structured inputs: {'✅ Yes' if metrics.get('uses_xml_structure') else '❌ No'}",
        "Output Format Specification": f"- XML tags detected: {', '.join(xml_tags[:5]) if xml_tags else 'None'}{' ...' if len(xml_tags) > 5 else ''}",
        "Weighted Criteria": f"- Evaluation rubric indicators: {', '.join(judge_keywords[:3]) if judge_keywords else 'None'}{' ...' if len(judge_keywords) > 3 else ''}",
        "Evidence-Based Reasoning": f"- Uses structured inputs: {'✅ Yes' if metrics.get('uses_xml_structure') else '❌ No'}",
        "Decision Framework": f"- Evaluation rubric indicators: {', '.join(judge_keywords[:3]) if judge_keywords else 'None'}{' ...' if len(judge_keywords) > 3 else ''}",
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
- Has system message/role: {'✅ Yes' if metrics.get('has_system_message') else '❌ No'}

**Tactic Detection (Expected Tactics Only):**
{tactic_detection_section}

**Complexity:**
- Total characters: {metrics.get('total_characters', 0)}
- Complexity level: {complexity.upper()}

{'=' * 70}
"""

    # STEP 4: Build tactic descriptions for Module 3
    tactic_descriptions = {
        "Role Prompting": "Specific, relevant persona with clear expertise domain and responsibilities",
        "Structured Inputs": "Well-organized sections with clear boundaries and meaningful XML/Markdown structure",
        "Output Format Specification": "Explicit output structure with sections, formatting, and examples",
        "Few-Shot Examples": "High-quality examples demonstrating desired patterns and edge cases",
        "Chain-of-Thought": "Systematic reasoning instructions with step-by-step workflow",
        "Reference Citations": "Proper document structure with source attribution and quote extraction",
        "Prompt Chaining": "Multi-step workflow with clear dependencies and handoffs",
        "Evaluation Rubric": "Clear evaluation rubrics with weighted criteria and scoring guidance",
        "Tree of Thoughts": "Exploration of multiple solution approaches or alternatives in parallel",
        "Weighted Criteria": "Explicit weights/priorities for different evaluation dimensions",
        "Evidence-Based Reasoning": "Requirements to cite specific examples and provide rationale",
        "Decision Framework": "Clear decision rules mapping scores to actions (approve/revise/block)"
    }

    # Only include expected tactics in the evaluation criteria
    criteria_list = []
    for i, tactic in enumerate(expected_tactics, 1):
        if tactic in tactic_descriptions:
            criteria_list.append(f"{i}. **{tactic}**: {tactic_descriptions[tactic]}")
        else:
            criteria_list.append(f"{i}. **{tactic}**: Check for effective implementation")

    criteria_text = "\n".join(criteria_list)

    # STEP 5: AI Evaluation with Confidence Scores
    print("👨‍⚖️ Running AI evaluation...")
    evaluation_prompt = f"""You are an expert prompt engineering instructor evaluating Module 3 application work.

<traditional_metrics>
{metrics_summary}
</traditional_metrics>

<student_prompt>
{prompt_text[:3000]}  # Limit to 3000 chars for efficiency
</student_prompt>

<expected_tactics>
{', '.join(expected_tactics)}
</expected_tactics>

<evaluation_criteria>
The traditional metrics show WHAT patterns exist. Your job is to evaluate HOW WELL they're implemented.

Analyze the student's implementation of ONLY these expected tactics:

{criteria_text}

IMPORTANT: Only evaluate tactics listed above. Focus on Module 3 real-world application quality.
</evaluation_criteria>

For each expected tactic, provide:

**Tactic Name**: ✅/⚠️/❌ (Quality Score: X/10, Confidence: Y%)

**Evidence**: [Quote specific parts showing implementation]

**Quality Assessment**: [Why this score? What's good/what needs work?]

**Confidence Rationale**: [Why are you X% confident in this assessment? What factors affect certainty?]

**Improvement Suggestions**: [Specific actionable advice if score < 8]

---

CRITICAL FORMATTING REQUIREMENT: Your response MUST include ALL 4 sections below in the EXACT order shown.
Do NOT skip any section. Do NOT combine sections. Do NOT start with scores.
The response must follow this EXACT structure:

<evaluation>
**Tactic Name**: ✅/⚠️/❌ (Quality Score: X/10, Confidence: Y%)

**Evidence**: [Quote specific parts showing implementation]

**Quality Assessment**: [Why this score? What's good/what needs work?]

**Confidence Rationale**: [Why are you Y% confident in this assessment?]

**Improvement Suggestions**: [Specific actionable advice if score < 8]

---

[Repeat for each tactic]
</evaluation>

<skills_demonstrated>
List Module 3 skills demonstrated based on quality scores:
- Only list skills where tactic received ✅ (8-10/10) or strong ⚠️ (7/10)
- Format: "- Skill: [Tactic Name] - [What they did well]"
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
2-3 sentences of actionable feedback:
1. Strongest aspect to reinforce
2. Most important improvement area
3. Next step for mastery
</overall_feedback>"""

    # Get AI evaluation
    messages_for_judge = [{"role": "user", "content": evaluation_prompt}]
    llm_judgment = get_chat_completion(messages_for_judge, temperature=0.0)

    # STEP 6: Display Semantic Similarity (if available)
    similarity_section = ""
    if semantic_results and semantic_results.get('has_reference'):
        similarity_section = f"""
🔬 SEMANTIC SIMILARITY ANALYSIS (vs. Reference Solution)
{'=' * 70}

**Overall Similarity**: {semantic_results['overall_similarity']}%

{semantic_results['detailed_analysis']}

{'=' * 70}
"""

    # STEP 7: Save to history (if enabled)
    if track_progress:
        try:
            # Extract scores from LLM judgment for history
            import re

            # Extract scores from the final output format (not from calculation steps)
            # Look for the final format lines: "Traditional Metrics: X/100", "Quality Assessment: Y/100", etc.

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

            # Extract per-tactic scores
            tactic_scores = {}

            # First try Module 3 format with confidence scores
            for tactic in expected_tactics:
                tactic_pattern = rf'\*\*{re.escape(tactic)}\*\*.*?Quality Score:\s*(\d+)/10.*?Confidence:\s*(\d+)%'
                match = re.search(tactic_pattern, llm_judgment or "", re.DOTALL | re.IGNORECASE)
                if match:
                    tactic_scores[tactic] = {
                        "quality": int(match.group(1)),
                        "confidence": int(match.group(2))
                    }

            # If no scores found, try parsing skills_demonstrated section
            if not tactic_scores:
                skills_section = re.search(r'<skills_demonstrated>(.*?)</skills_demonstrated>', llm_judgment or "", re.DOTALL | re.IGNORECASE)
                if skills_section:
                    skills_text = skills_section.group(1)
                    for tactic in expected_tactics:
                        if re.search(re.escape(tactic), skills_text, re.IGNORECASE):
                            tactic_scores[tactic] = {
                                "quality": 9,
                                "confidence": 90
                            }

            # Use extracted scores from LLM output
            # Fallback: calculate traditional metrics if not found in output
            if not traditional_score:
                traditional_score = sum(1 for t in expected_tactics if metrics.get(f'uses_{t.lower().replace(" ", "_")}', False)) * 100 // len(expected_tactics) if expected_tactics else 0

            # Fallback: use combined score if quality not found
            if not quality_score:
                quality_score = combined_score

            scores = {
                "combined_score": combined_score,
                "traditional_metrics": traditional_score,
                "llm_judge_quality": quality_score,
                "confidence_score": confidence_score,
                "semantic_similarity": semantic_results['overall_similarity'] if semantic_results else None
            }

            _save_evaluation_history(activity_name, scores, tactic_scores, {
                "tactics_evaluated": expected_tactics,
                "has_reference_comparison": bool(semantic_results)
            })
            print("💾 Evaluation saved to history")
        except Exception:
            pass  # Silently fail progress tracking to not disrupt evaluation

    # STEP 8: Print Combined Results
    print("\n" + "=" * 70)
    print(f"📊 COMPREHENSIVE EVALUATION: {activity_name}")
    print("=" * 70)
    print(metrics_summary)

    if similarity_section:
        print(similarity_section)

    print("\n👨‍⚖️ QUALITY ASSESSMENT (With Confidence Scores)")
    print("=" * 70)
    print(llm_judgment)
    print("\n" + "=" * 70)
    print("💡 Next Steps:")
    print("  1. Review traditional metrics (objective indicators)")
    print("  2. Check semantic similarity (vs. reference solution)")
    print("  3. Read LLM judge feedback with confidence scores")
    print("  4. Focus on high-confidence, low-score items first")
    print("  5. Revise and re-evaluate to track improvement")
    print(f"  6. View progress: view_progress('{activity_name}')")
    print("=" * 70)

    # Return full evaluation results only if requested
    if return_results:
        return {
            "activity_name": activity_name,
            "traditional_metrics": metrics,
            "semantic_similarity": semantic_results,
            "llm_judgment": llm_judgment,
            "llm_judgment_sections": {
                "evaluation": _extract_section(llm_judgment, "evaluation"),
                "skills_demonstrated": _extract_section(llm_judgment, "skills_demonstrated"),
                "combined_score": _extract_section(llm_judgment, "combined_score"),
                "overall_feedback": _extract_section(llm_judgment, "overall_feedback"),
            }
        }
    return None


def test_connection():
    """Test connection to AI services. Returns (success, response) tuple."""
    print("🔄 Testing connection to GitHub Copilot proxy...")
    test_result = get_chat_completion([
        {"role": "user", "content": "Say 'Connection successful!' if you can read this."}
    ])

    if test_result and ("successful" in test_result.lower() or "success" in test_result.lower()):
        print(f"✅ Connection successful! Using {PROVIDER.upper()} provider with model: {get_default_model()}")
        print(f"📝 Response: {test_result}")
        return True, test_result
    else:
        print("⚠️ Connection test completed but response unexpected:")
        print(f"📝 Response: {test_result}")
        return False, test_result


# ============================================
# 📊 MODULE INITIALIZATION
# ============================================

# Mark module as loaded for checking in notebooks
import sys
sys.modules['__module3_setup__'] = sys.modules[__name__]

print("✅ Module 3 setup utilities loaded successfully!")
print(f"🤖 Provider: {PROVIDER.upper()}")
print(f"📝 Default model: {get_default_model()}")
