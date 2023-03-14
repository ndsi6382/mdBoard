# Runner code



import application
from utils import check_setup

def main():
    check_setup()
    application.APP.run(host="0.0.0.0", port=5000, debug=True, ssl_context='adhoc')

if __name__ == "__main__":
    main()
