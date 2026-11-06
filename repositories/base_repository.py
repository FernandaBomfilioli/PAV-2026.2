from sqlalchemy.exc import IntegrityError


class BaseRepository:
    """CRUD genérico; as subclasses herdam e especializam."""

    def __init__(self, session, model):
        self.session = session
        self.model = model

    def get_all(self):
        return self.session.query(self.model).all()

    def get_by_id(self, identificador):
        return self.session.get(self.model, identificador)

    def create(self, obj):
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def update(self, obj):
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, obj):
        self.session.delete(obj)
        self.session.commit()


class RepositoryIntegrityError(IntegrityError):
    pass
