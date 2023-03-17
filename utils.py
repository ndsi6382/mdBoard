import os
from application.utils import DATA_DIR, hash_string
from application.models import AppData

def check_setup():
    """
    Checks whether this is the first time running (or new directory).
    Runs the setup script if necessary.
    """
    try:
        check = os.environ["SECRET"]
        check = os.environ["SECURE_COOKIE"]
    except KeyError:
        raise RuntimeError("Ensure environment variables SECRET and SECURE_COOKIE are set.")
    if not os.path.exists(os.path.join(DATA_DIR, 'database.db')):
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