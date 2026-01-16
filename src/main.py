from jist import JIST
from utils import Secret
from devtools import pprint

secret = Secret("secret.ini", "Credentials2")

jist = JIST(secret.hostname, secret.username, secret.password)

#data = jist.get_structures()
#data = jist.get_structure(600)
data = jist.get_forest(600)

pprint(data.components)