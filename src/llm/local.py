"""
Local LLM delegation via llamafile.
Claude delegates simple tasks here to save tokens.
"""
import subprocess
import json
from pathlib import Path

LLAMAFILE = Path(r"C:\Users\user\.openclaw\workspace\bin\llamafile.exe")
MODEL = Path(r"C:\Users\user\.openclaw\workspace\models\qwen2.5-7b-instruct-q3_k_m.gguf")

def ask_local(prompt: str, max_tokens: int = 200, temperature: float = 0.7) -> str:
    """
    Delegate a simple task to local Qwen via llamafile.
    
    Good for:
    - Text formatting/cleanup
    - Simple summaries (<500 words)
    - JSON/YAML generation
    - Template filling
    - Data extraction
    
    NOT for:
    - Complex reasoning
    - Multi-step planning
    - Tool use decisions
    - Code with context
    """
    # Wrap in chat template for Qwen
    chat_prompt = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
    
    cmd = [
        str(LLAMAFILE),
        "-m", str(MODEL),
        "-p", chat_prompt,
        "-n", str(max_tokens),
        "--temp", str(temperature),
        "--no-display-prompt",
        "-ngl", "99",  # GPU layers
        "-r", "<|im_end|>",  # Stop at end token
    ]
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=60
    )
    
    return result.stdout.strip()


def format_for_platform(text: str, platform: str) -> str:
    """Have local LLM adapt content for a platform."""
    prompt = f"""Reformat this text for {platform}. Follow platform conventions:
- Discord: No markdown tables, wrap links in <>
- WhatsApp: No headers, use *bold* for emphasis
- Telegram: Markdown OK, keep concise
- Twitter: Max 280 chars, add hashtags

Text: {text}

Output only the reformatted text:"""
    return ask_local(prompt, max_tokens=300)


def generate_json(description: str) -> dict:
    """Have local LLM generate JSON from description."""
    prompt = f"""Generate valid JSON for: {description}
Output only the JSON, no explanation:"""
    response = ask_local(prompt, max_tokens=500, temperature=0.3)
    # Extract JSON from response
    try:
        # Find JSON in response
        start = response.find('{')
        end = response.rfind('}') + 1
        if start >= 0 and end > start:
            return json.loads(response[start:end])
    except json.JSONDecodeError:
        pass
    return {"error": "Failed to parse JSON", "raw": response}


def summarize(text: str, max_words: int = 100) -> str:
    """Have local LLM summarize text."""
    prompt = f"""Summarize this in {max_words} words or less:

{text}

Summary:"""
    return ask_local(prompt, max_tokens=max_words * 2)


if __name__ == "__main__":
    # Test
    print("Testing local LLM delegation...")
    result = ask_local("Say 'Local LLM ready' in exactly 3 words.")
    print(f"Response: {result}")
