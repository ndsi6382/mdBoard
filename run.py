import application
from utils import check_setup
from waitress import serve

def main():
    check_setup()
    print("Serving mdBoard on: host=0.0.0.0, port=5000")
    serve(application.APP, host="0.0.0.0", port=5000, threads=10)

if __name__ == "__main__":
    main()
