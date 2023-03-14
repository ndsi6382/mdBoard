import os
from application.utils import hash_string
from application.models import AppData

def check_setup():
    """
    Checks whether this is the first time running (or new directory).
    Runs the setup script if necessary.
    """
    try:
        if not os.path.exists(os.environ["MDB_DIR"]):
            os.makedirs(os.environ["MDB_DIR"])
        check = os.environ["MDB_SECRET"]
    except KeyError:
        raise RuntimeError("Environment variable not set! Ensure MDB_DIR, MDB_CONFIGS, and MDB_SECRET are set.")
    if not os.path.exists(os.path.join(os.environ["MDB_DIR"], "database.db")):
        new_setup()

def new_setup():
    from application import DB, APP
    print("Setting up...")
    with APP.app_context():
        DB.create_all()
        DB.session.add(AppData(username="user", password=hash_string("password")))
        DB.session.commit()
