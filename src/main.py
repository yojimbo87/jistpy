from jist import JIST
from utils import Secret
from pprint import pprint

secret = Secret("secret.ini", "Credentials2")

jist = JIST(secret.hostname, secret.username, secret.password)
structures = jist.get_structures()

pprint(structures)
print(len(structures))