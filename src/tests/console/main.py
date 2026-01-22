from devtools import pprint
from jist import JIST
from jist.utils import Secret


def main():
    secret = Secret("../../secret.ini", "Credentials2")
    jist = JIST(secret.hostname, secret.username, secret.password)

    data = jist.rest_api.get_structures()
    # data = jist.get_structure(600)
    # data = jist.get_forest(600)

    pprint(data)


if __name__ == '__main__':
    main()
