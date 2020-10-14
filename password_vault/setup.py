import getpass
import sys
import uuid

from .base import Base, get_session, get_engine
from .Secret import SecretModel  # Imported for schema creation
from .carry import global_scope
from .users import validation_key_new
from .Encryption import Encryption
from colored import fg, bg, attr

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


def s_initialize(key, salt):
    if key:
        # Create Encryption instance and set it to the global scope
        global_scope['enc'] = Encryption(key.encode())

        # Create db
        create_db()

        # Create validation key
        validation_key_new()

        print(green + "\n>>> " + reset +
              "Your vault has been created and encrypted with your master key. Your unique salt is: %s. Write it down. If you lose your config file you will need it to unlock your vault." % (salt))

        return True


def create_db():
    """
        Create db
    """

    session = get_session()
    Base.metadata.create_all(get_engine())
    session.commit()

    return True
