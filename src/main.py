from jist import JIST
import os
from configparser import ConfigParser

thisfolder = os.path.dirname(os.path.abspath(__file__))
initfile = os.path.join(thisfolder, 'secret.ini')
config = ConfigParser()
config.read(initfile)

section = "Credentials2"

hostname = config[section]["hostname"]
username = config[section]["username"]
password = config[section]["password"]

jist = JIST(hostname, username, password)

structures = jist.get_structures()

print(structures)
#pretty_json = json.loads(res.text)
#print (json.dumps(pretty_json, indent=2))