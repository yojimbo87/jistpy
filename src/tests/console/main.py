from jist import JIST
from utils import Secret
from devtools import pprint
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))


def main():
    secret = Secret("secret.ini", "Credentials2")

    jist = JIST(secret.hostname, secret.username, secret.password)

    # data = jist.get_structures()
    # data = jist.get_structure(600)
    data = jist.get_forest(600)

    pprint(data.components)


if __name__ == "__main__":
    main()
