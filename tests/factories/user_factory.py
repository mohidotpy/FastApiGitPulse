import factory
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, create_access_token
from app.entities.user import User


class UserEntityFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    email = factory.Faker('email')
    password = factory.LazyAttribute(
        lambda x: get_password_hash(factory.Faker('password', length=12).evaluate(None, None, {"locale": True})))
    user_token = factory.Faker('uuid4')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        if 'password' in kwargs:
            plain_password = kwargs.pop('password')
            hashed_password = get_password_hash(plain_password)
            kwargs['password'] = hashed_password

        return super(UserEntityFactory, cls)._create(model_class, *args, **kwargs)


class UserFactory(UserEntityFactory, factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        logged_in = kwargs.pop('logged_in', False)
        session = kwargs.pop('session', None)  # Extract the session from kwargs

        if session:
            assert isinstance(session, Session), "Provided session is not an instance of SQLAlchemy Session"
            cls._meta.sqlalchemy_session = session

        user = super(UserFactory, cls)._create(model_class, *args, **kwargs)

        if logged_in:
            access_token, expiration = create_access_token({'id': user.id, 'email': user.email})
            user.access_token = access_token

        return user
