from jist import JIST
from utils import Secret
from pprint import pprint

secret = Secret("secret.ini", "Credentials2")

jist = JIST(secret.hostname, secret.username, secret.password)
#data = jist.get_structures()
data = jist.get_structure(600)

pprint(data)