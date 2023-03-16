import application
from utils import check_setup
from waitress import serve

def main():
    check_setup()
    #application.APP.run(host="0.0.0.0", port=5000, debug=True)
    print("Serving mdBoard on: host=0.0.0.0, port=5000")
    serve(application.APP, host="0.0.0.0", port=5000, url_scheme='https')

if __name__ == "__main__":
    main()
