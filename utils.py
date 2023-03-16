import os
from application.utils import hash_string
from application.models import AppData

def check_setup():
    """
    Checks whether this is the first time running (or new directory).
    Runs the setup script if necessary.
    """
    try:
        check = os.environ["SECRET"]
        check = os.environ["ENABLE_HTTPS"]
    except KeyError:
        raise RuntimeError("Ensure environment variables SECRET and ENABLE_HTTPS are set.")
    if not os.path.exists("/data/database.db"):
        new_setup()

def new_setup():
    from application import DB, APP
    print("Setting up...")
    with APP.app_context():
        DB.create_all()
        DB.session.add(AppData(username="user", password=hash_string("password")))
        DB.session.commit()
    print("New setup complete. The username is 'user' and the password is 'password'. \
           The user should be change this ASAP.")