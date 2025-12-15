"""Script interactivo para consultar la base de datos."""
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from app.database.models import Base, ChatMessage, SessionMetadata


def get_database_session():
    """Initialize database connection without requiring OpenAI settings."""
    # Default database path
    db_path = Path(__file__).parent.parent / "utec_planificador.db"
    database_url = f"sqlite:///{db_path}"

    # Create engine and session
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False}
    )

    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    # Create session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def show_statistics(db):
    """Show general statistics."""
    print_header("ESTADÍSTICAS GENERALES")

    total_messages = db.query(ChatMessage).count()
    total_sessions = db.query(SessionMetadata).count()

    # Messages by role
    user_messages = db.query(ChatMessage).filter(ChatMessage.role == "user").count()
    assistant_messages = db.query(ChatMessage).filter(ChatMessage.role == "assistant").count()

    # Recent activity
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    messages_today = db.query(ChatMessage).filter(
        ChatMessage.created_at >= today
    ).count()

    print(f"📊 Total de mensajes:      {total_messages}")
    print(f"   - Usuario:              {user_messages}")
    print(f"   - Asistente:            {assistant_messages}")
    print(f"👥 Total de sesiones:      {total_sessions}")
    print(f"📅 Mensajes hoy:           {messages_today}")


def show_recent_messages(db, limit=10):
    """Show recent messages."""
    print_header(f"ÚLTIMOS {limit} MENSAJES")

    messages = db.query(ChatMessage).order_by(
        ChatMessage.created_at.desc()
    ).limit(limit).all()

    if not messages:
        print("ℹ️  No hay mensajes en la base de datos.")
        return

    for i, msg in enumerate(messages, 1):
        timestamp = msg.created_at.strftime("%Y-%m-%d %H:%M:%S")
        content_preview = msg.content[:80] + "..." if len(msg.content) > 80 else msg.content

        print(f"\n{i}. [{msg.role.upper()}] {timestamp}")
        print(f"   Session: {msg.session_id}")
        print(f"   Content: {content_preview}")


def show_sessions(db, limit=10):
    """Show active sessions."""
    print_header(f"ÚLTIMAS {limit} SESIONES")

    sessions = db.query(SessionMetadata).order_by(
        SessionMetadata.last_activity.desc()
    ).limit(limit).all()

    if not sessions:
        print("ℹ️  No hay sesiones en la base de datos.")
        return

    for i, session in enumerate(sessions, 1):
        created = session.created_at.strftime("%Y-%m-%d %H:%M:%S")
        last_activity = session.last_activity.strftime("%Y-%m-%d %H:%M:%S")

        print(f"\n{i}. {session.session_id}")
        print(f"   Mensajes: {session.message_count}")
        print(f"   Creada: {created}")
        print(f"   Última actividad: {last_activity}")


def show_session_details(db, session_id):
    """Show details of a specific session."""
    print_header(f"DETALLES DE SESIÓN: {session_id}")

    # Get session metadata
    session = db.query(SessionMetadata).filter(
        SessionMetadata.session_id == session_id
    ).first()

    if not session:
        print(f"❌ No se encontró la sesión: {session_id}")
        return

    print(f"📊 Información de la sesión:")
    print(f"   ID: {session.session_id}")
    print(f"   Mensajes: {session.message_count}")
    print(f"   Creada: {session.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Última actividad: {session.last_activity.strftime('%Y-%m-%d %H:%M:%S')}")

    # Get messages
    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).order_by(ChatMessage.created_at).all()

    print(f"\n💬 Conversación ({len(messages)} mensajes):")
    for i, msg in enumerate(messages, 1):
        timestamp = msg.created_at.strftime("%H:%M:%S")
        print(f"\n{i}. [{timestamp}] {msg.role.upper()}:")
        print(f"   {msg.content}")


def search_messages(db, keyword):
    """Search messages by keyword."""
    print_header(f"BÚSQUEDA: '{keyword}'")

    messages = db.query(ChatMessage).filter(
        ChatMessage.content.like(f"%{keyword}%")
    ).order_by(ChatMessage.created_at.desc()).limit(20).all()

    if not messages:
        print(f"ℹ️  No se encontraron mensajes con '{keyword}'")
        return

    print(f"✅ Se encontraron {len(messages)} mensajes (mostrando máximo 20):")

    for i, msg in enumerate(messages, 1):
        timestamp = msg.created_at.strftime("%Y-%m-%d %H:%M:%S")
        content_preview = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content

        print(f"\n{i}. [{msg.role}] {timestamp} - Session: {msg.session_id}")
        print(f"   {content_preview}")


def clear_screen():
    """Clear the console screen."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    """Pause and wait for user input."""
    print("\n" + "-" * 70)
    input("Presiona ENTER para continuar...")


def interactive_menu():
    """Show interactive menu."""
    db = get_database_session()

    while True:
        clear_screen()
        print("=" * 70)
        print("  UTEC PLANIFICADOR AI - EXPLORADOR DE BASE DE DATOS")
        print("=" * 70)
        print("\n  MENÚ PRINCIPAL")
        print("\n  1. 📊 Ver estadísticas generales")
        print("  2. 💬 Ver últimos mensajes")
        print("  3. 👥 Ver sesiones activas")
        print("  4. 🔍 Ver detalles de una sesión específica")
        print("  5. 🔎 Buscar mensajes por palabra clave")
        print("  6. 🚪 Salir")
        print("\n" + "=" * 70)

        try:
            choice = input("\n  ➤ Selecciona una opción (1-6): ").strip()

            if choice == "1":
                clear_screen()
                show_statistics(db)
                pause()

            elif choice == "2":
                clear_screen()
                print("=" * 70)
                print("  VER ÚLTIMOS MENSAJES")
                print("=" * 70)
                limit_input = input("\n  ➤ ¿Cuántos mensajes mostrar? (presiona ENTER para 10): ").strip()
                limit = int(limit_input) if limit_input else 10
                show_recent_messages(db, limit)
                pause()

            elif choice == "3":
                clear_screen()
                print("=" * 70)
                print("  VER SESIONES ACTIVAS")
                print("=" * 70)
                limit_input = input("\n  ➤ ¿Cuántas sesiones mostrar? (presiona ENTER para 10): ").strip()
                limit = int(limit_input) if limit_input else 10
                show_sessions(db, limit)
                pause()

            elif choice == "4":
                clear_screen()
                print("=" * 70)
                print("  DETALLES DE SESIÓN")
                print("=" * 70)
                print("\n  Ejemplos de session_id:")
                print("    - juan.perez@utec.edu.uy")
                print("    - user-123")
                print("    - 550e8400-e29b-41d4-a716-446655440000")
                session_id = input("\n  ➤ Ingresa el session_id: ").strip()
                if session_id:
                    show_session_details(db, session_id)
                    pause()
                else:
                    print("\n  ⚠️  No ingresaste ningún session_id")
                    pause()

            elif choice == "5":
                clear_screen()
                print("=" * 70)
                print("  BUSCAR MENSAJES")
                print("=" * 70)
                print("\n  Busca mensajes que contengan la palabra clave especificada.")
                print("  Ejemplos: ODS, pedagogía, planificación, etc.")
                keyword = input("\n  ➤ Ingresa palabra clave: ").strip()
                if keyword:
                    search_messages(db, keyword)
                    pause()
                else:
                    print("\n  ⚠️  No ingresaste ninguna palabra clave")
                    pause()

            elif choice == "6":
                clear_screen()
                print("\n  👋 ¡Hasta luego!")
                print()
                break

            elif choice == "":
                continue

            else:
                print("\n  ❌ Opción inválida. Por favor elige 1-6.")
                pause()

        except KeyboardInterrupt:
            clear_screen()
            print("\n  👋 ¡Hasta luego!")
            print()
            break
        except ValueError as e:
            print(f"\n  ❌ Valor inválido: {e}")
            pause()
        except Exception as e:
            print(f"\n  ❌ Error: {e}")
            pause()

    db.close()


def main():
    """Main function."""
    try:
        # Show interactive menu by default (easier to use)
        if len(sys.argv) == 1:
            interactive_menu()
            return 0

        # Command-line mode (for advanced users or scripts)
        db = get_database_session()
        command = sys.argv[1].lower()

        if command == "stats":
            show_statistics(db)
        elif command == "messages":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            show_recent_messages(db, limit)
        elif command == "sessions":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            show_sessions(db, limit)
        elif command == "session":
            if len(sys.argv) < 3:
                print("❌ Debes proporcionar un session_id")
                print("Uso: python explorar_db.py session <session_id>")
            else:
                show_session_details(db, sys.argv[2])
        elif command == "search":
            if len(sys.argv) < 3:
                print("❌ Debes proporcionar una palabra clave")
                print("Uso: python explorar_db.py search <keyword>")
            else:
                search_messages(db, " ".join(sys.argv[2:]))
        elif command in ["help", "-h", "--help"]:
            print("\n" + "=" * 70)
            print("  EXPLORADOR DE BASE DE DATOS - MODO COMANDO")
            print("=" * 70)
            print("\nUSO:")
            print("  python explorar_db.py              - Menú interactivo (recomendado)")
            print("  python explorar_db.py <comando>    - Modo comando directo")
            print("\nCOMANDOS DISPONIBLES:")
            print("  stats                  - Ver estadísticas generales")
            print("  messages [N]           - Ver últimos N mensajes (default: 10)")
            print("  sessions [N]           - Ver últimas N sesiones (default: 10)")
            print("  session <id>           - Ver detalles de una sesión específica")
            print("  search <keyword>       - Buscar mensajes por palabra clave")
            print("  help                   - Mostrar esta ayuda")
            print("\nEJEMPLOS:")
            print("  python explorar_db.py stats")
            print("  python explorar_db.py messages 20")
            print("  python explorar_db.py session juan.perez@utec.edu.uy")
            print("  python explorar_db.py search ODS")
            print()
        else:
            print(f"❌ Comando desconocido: {command}")
            print("Usa 'python explorar_db.py help' para ver comandos disponibles")
            print("O ejecuta sin argumentos para el menú interactivo")

        db.close()
        return 0

    except Exception as e:
        print(f"\n❌ Error al conectar con la base de datos:")
        print(f"   {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

