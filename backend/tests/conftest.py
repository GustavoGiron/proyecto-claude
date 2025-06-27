import os
import pytest
from sqlalchemy.orm import scoped_session, sessionmaker

from app import create_app
from app.database import db as _db
from app.models.usuarios_model import Usuario
from app.models.roles_model import Role


@pytest.fixture(scope='session')
def app():
    """
    Crea la app en modo testing con la base de datos de test configurada en TEST_DATABASE_URI.
    """
    os.environ["FLASK_ENV"] = "testing"
    app = create_app(testing=True)

    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    """
    Cliente de prueba Flask.
    """
    return app.test_client()


@pytest.fixture(scope='session')
def db(app):
    """
    Crea todas las tablas en la base de datos de test (MySQL).
    """
    _db.app = app
    _db.create_all()
    yield _db
    _db.drop_all()

@pytest.fixture(scope='function')
def session(db):
    """
    Crea una nueva transacción para cada prueba y la revierte al final.
    """
    connection = db.engine.connect()
    transaction = connection.begin()

    session_factory = sessionmaker(bind=connection)
    Session = scoped_session(session_factory)

    db.session = Session

    yield db.session

    transaction.rollback()
    connection.close()
    Session.remove()

@pytest.fixture
def usuario_prueba(session):
    """
    Crea un usuario de prueba con un rol asociado.
    """
    rol = Role(nombre="Tester", descripcion="Rol de prueba")
    session.add(rol)
    session.flush()

    usuario = Usuario(
        username="testuser",
        email="test@example.com",
        nombre="Test",
        apellido="User",
        is_active=True,
        role_id=rol.id
    )
    usuario.set_password("12345678")
    session.add(usuario)
    session.commit()
    return usuario
