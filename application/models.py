from application import APP, DB

class AppData(DB.Model):
    dummy_pk = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(32), nullable=False)
    password = DB.Column(DB.String(256), nullable=False)

#class Documents(DB.Model):
#    filename = DB.Column(DB.String(128), primary_key=True)
#    public = DB.Column(DB.Boolean())
