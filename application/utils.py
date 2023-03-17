import bcrypt, os, datetime
from application import APP, DB
from application.models import AppData
import markdown
import pymdownx

salt = bcrypt.gensalt()

DATA_DIR = "/data"
UNSAFE_CHARS = "`~!@#$%^&*:;}{][\/|<>?"

def hash_string(string):
    return bcrypt.hashpw(string.encode(), salt).decode()

def process_login(user, pwd):
    with APP.app_context():
        r = AppData.query.all()
        if r and bcrypt.checkpw(pwd.encode(), r[0].password.encode()) and user == r[0].username:
            return True
        else:
            return False

def list_mds():
    return sorted([e[:-3] for e in os.listdir(DATA_DIR) if e[-3:] == ".md"], key=str.casefold)

def get_md(title):
    with open(os.path.join(DATA_DIR, f"{title}.md")) as f:
        return f.read()

def md_to_html(title):
    with open(os.path.join(DATA_DIR, f"{title}.md")) as f:
        return markdown.markdown("[TOC]\n\n" + f.read(),
            extensions=['toc', 'pymdownx.arithmatex', 'pymdownx.extra'], 
            extension_configs={
                'toc':{'toc_depth':'2-6', 'title':'Contents'},
                'pymdownx.arithmatex':{'generic':True}
            }
        )

def delete_md(title):
    os.remove(os.path.join(DATA_DIR, f"{title}.md"))

def sanitise_string(s):
    s = "".join(c for c in s if c not in UNSAFE_CHARS)
    if s:
        return s
    else:
        return datetime.datetime.now().strftime("%d%m%y_%H%M%S")

def overwrite_md(curr_title, new_title, new_content):
    new_title = sanitise_string(new_title)
    new_title = os.path.join(DATA_DIR, f"{new_title}.md")
    if curr_title:
        os.remove(os.path.join(DATA_DIR, f"{curr_title}.md"))
    with open(new_title, 'w') as f:
        f.write(new_content)

def get_settings_data():
    # omits password
    with APP.app_context():
        r = AppData.query.all()
        data = {"username":r[0].username}
        return data

def update_settings_data(username, password):
    with APP.app_context():
        r = AppData.query.all()
        if username:
            r[0].username = username
        if password:
            r[0].password = hash_string(password)
        DB.session.commit()
