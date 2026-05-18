import re


# ==========================================
# BLOCKED PATTERNS
# ==========================================
BLOCKED_PATTERNS = [
    "ignore previous instructions",
    "ignore all instructions",
    "reveal system prompt",
    "show your prompt",
    "show system prompt",
    "show environment variables",
    "openai_api_key",
    "secret_key",
    "os.getenv",
    "subprocess",
    "eval(",
    "exec(",
    "rm -rf",
    "drop table",
    "delete from",
    "<script",
    "</script>",
]


# ==========================================
# INPUT SANITIZATION
# ==========================================
def sanitize_input(text):
    text = str(text)

    # Remove null bytes
    text = text.replace("\x00", "")

    # Remove leading/trailing spaces
    text = text.strip()

    # Limit input size
    if len(text) > 10000:
        text = text[:10000]

    return text


# ==========================================
# MALICIOUS INPUT DETECTION
# ==========================================
def is_malicious_input(text):
    text = str(text).lower()

    for pattern in BLOCKED_PATTERNS:
        if pattern in text:
            return True

    return False