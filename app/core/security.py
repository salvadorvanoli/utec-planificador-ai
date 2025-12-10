"""Security utilities for input sanitization and validation."""
import re
import logging

logger = logging.getLogger(__name__)

# SQL injection patterns to detect and block
SQL_INJECTION_PATTERNS = [
    r"(\bUNION\b.*\bSELECT\b)",
    r"(\bDROP\b.*\bTABLE\b)",
    r"(\bINSERT\b.*\bINTO\b)",
    r"(\bDELETE\b.*\bFROM\b)",
    r"(\bUPDATE\b.*\bSET\b)",
    r"(\bEXEC\b|\bEXECUTE\b)",
    r"(;.*(-{2}|#|\\/\\*))",  # SQL comments after semicolon
    r"(\bOR\b.*=.*)",
    r"(\bAND\b.*=.*)",
    r"('.*OR.*'.*=.*')",
    r"(1.*=.*1)",
    r"(\bSELECT\b.*\bFROM\b)",
    r"(\bSHOW\b.*\bTABLES\b)",
    r"(\bDESCRIBE\b|\bDESC\b)",
    r"(xp_.*\()",  # SQL Server extended procedures
    r"(\bINFORMATION_SCHEMA\b)",
]

# Characters that are commonly used in SQL injection
SUSPICIOUS_CHARS = ["'--", "';--", '"--', '";--', "/*", "*/", "@@", "@", "xp_"]

# Maximum safe lengths for different fields
MAX_SESSION_ID_LENGTH = 255
MAX_MESSAGE_LENGTH = 50000  # 50KB for a single message
MAX_ROLE_LENGTH = 20


class SecurityViolation(Exception):
    """Exception raised when a security violation is detected."""
    pass


def sanitize_session_id(session_id: str) -> str:
    """
    Sanitize session ID to prevent SQL injection.

    Args:
        session_id: Session identifier to sanitize

    Returns:
        Sanitized session ID

    Raises:
        SecurityViolation: If session ID is suspicious or invalid
    """
    if not session_id:
        raise SecurityViolation("Session ID cannot be empty")

    if len(session_id) > MAX_SESSION_ID_LENGTH:
        raise SecurityViolation(f"Session ID too long (max {MAX_SESSION_ID_LENGTH})")

    # Session IDs can be emails (user@domain.com), UUIDs, or simple IDs
    # Allow: letters, numbers, hyphens, underscores, @ and dots
    if not re.match(r'^[a-zA-Z0-9._@-]+$', session_id):
        logger.warning(f"Suspicious session ID format: {session_id[:50]}")
        raise SecurityViolation("Session ID contains invalid characters")

    # Block SQL injection attempts
    if "'" in session_id or '"' in session_id or ';' in session_id or '--' in session_id:
        logger.warning(f"SQL injection attempt in session_id: {session_id[:50]}")
        raise SecurityViolation("Session ID contains dangerous patterns")

    return session_id


def sanitize_role(role: str) -> str:
    """
    Sanitize role field to ensure it's one of the allowed values.

    Args:
        role: Role to validate

    Returns:
        Sanitized role

    Raises:
        SecurityViolation: If role is invalid
    """
    allowed_roles = ["user", "assistant", "system"]

    if not role:
        raise SecurityViolation("Role cannot be empty")

    if len(role) > MAX_ROLE_LENGTH:
        raise SecurityViolation(f"Role too long (max {MAX_ROLE_LENGTH})")

    role_lower = role.lower().strip()

    if role_lower not in allowed_roles:
        logger.warning(f"Invalid role: {role}")
        raise SecurityViolation(f"Role must be one of: {', '.join(allowed_roles)}")

    return role_lower


def detect_sql_injection(text: str) -> bool:
    """
    Detect potential SQL injection attempts in text.

    Args:
        text: Text to analyze

    Returns:
        True if SQL injection is detected, False otherwise
    """
    if not text:
        return False

    text_upper = text.upper()

    # Check for SQL injection patterns
    for pattern in SQL_INJECTION_PATTERNS:
        if re.search(pattern, text_upper, re.IGNORECASE):
            logger.warning(f"SQL injection pattern detected: {pattern}")
            return True

    # Check for suspicious character sequences
    for suspicious in SUSPICIOUS_CHARS:
        if suspicious in text:
            logger.warning(f"Suspicious character sequence detected: {suspicious}")
            return True

    return False


def sanitize_message_content(content: str, allow_sql_keywords: bool = True) -> str:
    """
    Sanitize message content to prevent SQL injection.

    Args:
        content: Message content to sanitize
        allow_sql_keywords: If True, allows SQL keywords in educational context
                           (for teaching SQL). If False, blocks them.

    Returns:
        Sanitized content

    Raises:
        SecurityViolation: If content is suspicious or too long
    """
    if not content:
        raise SecurityViolation("Message content cannot be empty")

    if len(content) > MAX_MESSAGE_LENGTH:
        raise SecurityViolation(f"Message too long (max {MAX_MESSAGE_LENGTH} chars)")

    # Only check for SQL injection if we're NOT allowing SQL keywords
    # (for educational contexts like teaching SQL, we need to be permissive)
    if not allow_sql_keywords:
        if detect_sql_injection(content):
            raise SecurityViolation("Potential SQL injection detected in message")

    # Even in educational context, block obvious injection attempts
    # that have no educational value (like actual SQL comments)
    dangerous_patterns = [
        r"';.*DROP.*TABLE",
        r"';.*DELETE.*FROM",
        r"';.*UPDATE.*SET",
        r"1=1.*--",
        r"OR.*1=1.*--",
    ]

    content_upper = content.upper()
    for pattern in dangerous_patterns:
        if re.search(pattern, content_upper):
            logger.error(f"Dangerous SQL injection pattern detected: {pattern}")
            raise SecurityViolation("Dangerous SQL injection pattern detected")

    return content


def validate_all_inputs(session_id: str, role: str, content: str) -> tuple:
    """
    Validate all inputs for database operations.

    Args:
        session_id: Session identifier
        role: Message role
        content: Message content

    Returns:
        Tuple of (sanitized_session_id, sanitized_role, sanitized_content)

    Raises:
        SecurityViolation: If any input is invalid or suspicious
    """
    try:
        clean_session_id = sanitize_session_id(session_id)
        clean_role = sanitize_role(role)

        # For educational AI, we allow SQL keywords in content
        # (teachers might be discussing SQL), but we still check
        # for dangerous patterns
        clean_content = sanitize_message_content(content, allow_sql_keywords=True)

        return clean_session_id, clean_role, clean_content

    except SecurityViolation as e:
        logger.error(f"Security validation failed: {e}")
        raise


def log_security_event(event_type: str, details: dict):
    """
    Log security-related events for monitoring.

    Args:
        event_type: Type of security event
        details: Additional details about the event
    """
    logger.warning(
        f"SECURITY EVENT: {event_type}",
        extra={
            "event_type": event_type,
            "details": details,
            "severity": "WARNING"
        }
    )

