"""Script para verificar el estado de la base de datos."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database.models import init_database, SessionLocal, ChatMessage, SessionMetadata


def main():
    """Verificar estado de la base de datos."""
    print("=" * 60)
    print("🔍 UTEC Planificador AI - Verificación de Base de Datos")
    print("=" * 60)
    print()

    try:
        # Inicializar base de datos
        from app.database.models import SessionLocal as SL
        init_database()
        from app.database.models import SessionLocal
        db = SessionLocal()

        # Contar mensajes y sesiones
        message_count = db.query(ChatMessage).count()
        session_count = db.query(SessionMetadata).count()

        print("✅ Conexión a base de datos exitosa")
        print()
        print(f"📊 Estadísticas:")
        print(f"   - Total de mensajes: {message_count}")
        print(f"   - Total de sesiones: {session_count}")
        print()

        # Mostrar últimos mensajes si existen
        if message_count > 0:
            print("📝 Últimos 5 mensajes:")
            messages = db.query(ChatMessage).order_by(
                ChatMessage.created_at.desc()
            ).limit(5).all()

            for msg in messages:
                content_preview = msg.content[:60] + "..." if len(msg.content) > 60 else msg.content
                timestamp = msg.created_at.strftime("%Y-%m-%d %H:%M:%S")
                print(f"   [{msg.role:10}] {content_preview}")
                print(f"                 Session: {msg.session_id} | {timestamp}")
                print()
        else:
            print("ℹ️  No hay mensajes en la base de datos aún.")
            print("   Los mensajes se guardarán automáticamente al usar el chatbot.")
            print()

        # Mostrar sesiones activas
        if session_count > 0:
            print("👥 Sesiones activas:")
            sessions = db.query(SessionMetadata).order_by(
                SessionMetadata.last_activity.desc()
            ).limit(5).all()

            for session in sessions:
                last_activity = session.last_activity.strftime("%Y-%m-%d %H:%M:%S")
                print(f"   - {session.session_id}")
                print(f"     Mensajes: {session.message_count} | Última actividad: {last_activity}")

        db.close()

        print()
        print("=" * 60)
        print("✅ Verificación completada exitosamente")
        print("=" * 60)

        return 0

    except Exception as e:
        print(f"❌ Error al verificar la base de datos:")
        print(f"   {str(e)}")
        print()
        print("💡 Solución: Ejecuta primero el script de inicialización:")
        print("   python scripts\\migrate_to_v2.py")
        return 1


if __name__ == "__main__":
    sys.exit(main())

