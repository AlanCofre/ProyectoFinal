from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Configuración del motor de base de datos SQLite
DATABASE_URL = 'sqlite:///restaurante.db'  # Crea un archivo llamado restaurante.db en tu directorio actual
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Configuración de la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para definir los modelos
Base = declarative_base()

# Función para obtener la sesión de base de datos
def get_session():
    """
    Obtiene una instancia de la sesión de la base de datos.

    Returns:
        db (Session): La sesión de la base de datos.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
