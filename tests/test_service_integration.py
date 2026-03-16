import pytest

from app.db import Base, get_engine, get_session_factory
from app.repository import StudentRepository
from app.service import StudentService


@pytest.fixture
def session():
    """
    Integračný test: reálna DB (SQLite in-memory) + reálne SQLAlchemy tabuľky.
    Každý test dostane čistú databázu.
    """
    engine = get_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = get_session_factory(engine)

    with SessionLocal() as session:
        yield session


def test_integration_create_then_list_students(session):
    """
    INTEGRATION TEST (bez Mock):
    - Vložíme študenta cez Service (tým pádom sa reálne volá Repository aj DB).
    - Potom ho vylistujeme cez Service.
    - Overíme, že DB naozaj obsahuje to, čo očakávame.
    """
    repo = StudentRepository(session)         # reálna repository vrstva
    service = StudentService(repo)            # reálna service vrstva

    created = service.create_student("Dominik", "DOMINIK@example.com")
    students = service.list_students()

    assert len(students) == 1
    assert students[0].id == created.id
    assert students[0].name == "Dominik"
    assert students[0].email == "dominik@example.com"   # lowercase je výsledok logiky v service


def test_integration_update_student_persists_in_db(session):
    """
    INTEGRATION TEST (bez Mock):
    - Vložíme študenta
    - Aktualizujeme ho cez Service
    - Následne ho načítame znova priamo cez Repository, aby sme dokázali,
      že zmena je reálne uložená v databáze (nie len v pamäti).
    """
    repo = StudentRepository(session)
    service = StudentService(repo)

    created = service.create_student("Dominik", "dominik@example.com")

    updated = service.update_student(
        created.id,
        "Dominik Halvonik",
        "DOMINIK.HALVONIK@example.com",
    )

    assert updated.id == created.id
    assert updated.name == "Dominik Halvonik"
    assert updated.email == "dominik.halvonik@example.com"

    # kľúčový integračný moment: reálne načítanie z DB po update
    reloaded = repo.get_by_id(created.id)
    assert reloaded is not None
    assert reloaded.name == "Dominik Halvonik"
    assert reloaded.email == "dominik.halvonik@example.com"