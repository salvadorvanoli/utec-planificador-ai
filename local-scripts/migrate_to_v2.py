"""
Migration script from V1 to V2

This script helps migrate from the in-memory session storage to database storage.
Since V1 stored sessions in memory, there's nothing to migrate, but this script
ensures the database is properly initialized.
"""
import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database.models import init_database
from app.core.config import get_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Initialize database for V2."""
    logger.info("=" * 60)
    logger.info("UTEC Planificador AI - V2 Database Initialization")
    logger.info("=" * 60)

    settings = get_settings()
    logger.info(f"Database URL: {settings.database_url}")

    try:
        # Initialize database (creates tables if they don't exist)
        init_database()
        logger.info("✅ Database initialized successfully!")
        logger.info("Tables created:")
        logger.info("  - chat_messages")
        logger.info("  - session_metadata")

        logger.info("\n" + "=" * 60)
        logger.info("Migration complete! V2 is ready to use.")
        logger.info("=" * 60)

        return 0

    except Exception as e:
        logger.error(f"❌ Error initializing database: {e}")
        logger.exception(e)
        return 1


if __name__ == "__main__":
    sys.exit(main())

