from os import environ
from os.path import isfile, join, isdir
import json
import base64
import uuid
import secrets
import string
from cryptography.fernet import Fernet
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import warnings
import click

class envision:
    def __init__(self, root : str = './'):

        ''' Envision constructor. '''
        self.root = root
        self.ENVISION_FILE = join(root,'.envision')
        self.ENVISION_LOCK_FILE = join(root,'.envision.lock')
        self.ENVISION_KEY_FILE = join(root,'.envision.key')
        self.GITIGNORE_FILE = join(root,'.gitignore')

        #Detect if gitignore is correct
        self.__gitignore_detect()
        
        #Detect the current environment mode
        self.__detect()

        #Validate environment mode
        self.__validate_mode()

        #Validate the data in the json
        self.__validate_json()

        #Load the key and algorithm
        self.__load_key()
        
        #Load the JSON
        self.__load_json()

    #############GITIGNORE################
    def __gitignore_detect(self):
        gitignore = join(self.root,".gitignore");
        if isfile(gitignore):
            if not '.envision' in open(gitignore).read():
                warnings.warn('.gitignore file at {} does not include exclusion of .envision file.')
            if not '.envision.key' in open(gitignore).read():
                warnings.warn('.gitignore file at {} does not include exclusion of .envision.key file.'.format(str(self.root)))

    ######################################

    #############DETECTION################
    
    def __detect(self):
        if not isdir(self.root):
            raise EnvironmentError('No directory found at {} .'.format(str(self.root)))
        elif self.__has_envision():
            self.is_development = True
        elif self.__has_envision_lock():
            self.is_development = False
        else:
            raise EnvironmentError('No ENVISION files found in the directory {} .'.format(str(self.root)))

    def __has_envision(self):
        return isfile(self.ENVISION_FILE)
    
    def __has_envision_lock(self):
        return isfile(self.ENVISION_LOCK_FILE)

    ######################################

    ############VALIDATE MODE#############
    
    def __validate_mode(self):
        if self.is_development:
            if self.__has_envision_key_env_var():
                warnings.warn("ENVISION key variable is set on local enviroment running development mode. Ignored.")
        else:
            if not self.__has_envision_key_env_var():
                raise EnvironmentError("ENVISION key variable is NOT set on local environment running production mode.")
            elif self.__has_envision_key_file():
                warnings.warn("ENVISION key file is present on local environment running production mode.")

    def __has_envision_key_env_var(self):
        return environ.get('ENVISION') is not None

    def __has_envision_key_file(self):
        return isfile(self.ENVISION_KEY_FILE)
        
    ######################################

    ############VALIDATE JSONS############

    def __validate_json(self):
        if self.is_development:
            self.__validate_envision_json(self.ENVISION_FILE)
        else:
            self.__validate_envision_json(self.ENVISION_LOCK_FILE)

    def __validate_envision_json(self,filepath):
        with open(filepath) as json_file:
            try:
                json_obj = json.load(json_file)
            except:
                raise EnvironmentError('Could not parse a valid json object from file: {} .'.format(str(filepath)))
            for k in json_obj:
                if not isinstance(json_obj[k],str):
                    raise EnvironmentError('Value {0} of type {1} under key {2} of Envision file {3} is not a string.'.format(str(json_obj[k]),type(json_obj[k]),str(k),str(filepath)))

    ######################################
 
    ##########LOAD ENVISION KEY###########

    def __load_key(self):
        if self.is_development:
            self.__load_key_development()
        else:
            self.__load_key_production()

        self.__encryption_algorithm = Fernet(self.__get_fernet_key())

    def __load_key_development(self):
        try:
            with open(self.ENVISION_KEY_FILE, 'r') as key_file:
                self.key = key_file.read() or self.__generate_key()
                key_file.close()
        except:
            self.key = self.__generate_key()

    def __load_key_production(self):
        self.key = environ.get('ENVISION')

    def __get_fernet_key(self):
            kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=b'envision',iterations=100000,backend=default_backend())
            return base64.urlsafe_b64encode(kdf.derive(self.key.encode()))

    def __generate_key(self):
        return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16))


    ######################################
   
    #########LOAD ENVISION JSON###########

    def __load_json(self):
        if self.is_development:
            self.__load_json_development()
        else:
            self.__load_json_production()
    
    def __load_json_development(self):
        with open(self.ENVISION_FILE) as json_file:
            self.ENVISION_JSON = json.load(json_file)
        
    def __load_json_production(self):
        with open(self.ENVISION_LOCK_FILE) as json_file:
            enc_json = json.load(json_file)            
            data = {}
            for k in enc_json:
                data[k] = self.__decrypt_value(enc_json[k])
            self.ENVISION_JSON = data

    def __decrypt_value(self,v:str):
        try:
            return self.__encryption_algorithm.decrypt(v.encode()).decode()
        except:
            raise EnvironmentError('The provided env key token: {} is not valid for file {} .'.format(self.key,str(self.ENVISION_LOCK_FILE)))

    #######################################

    ############### UPDATE ###############
    def __update(self):
        if self.is_development:
            self.__update_file()
        else:
            warnings.warn('Updates to environment variables must be done in development mode. Ignored.')
    
    def __update_file(self):
        with open(self.ENVISION_FILE, 'w') as lock_file:
            json.dump(self.ENVISION_JSON, lock_file, sort_keys = True, indent=0)
            lock_file.close()

    ############### LOCK ################
    def __lock(self,token = None):
        if token:
            self.key = token

        if self.is_development:
            self.__lock_lock_file()
            self.__lock_key_file()
        else:
            warnings.warn('Locking environment variables must be done in development mode. Ignored.')

    def __lock_lock_file(self):
        enc_data = {}
        for k in self.ENVISION_JSON:
            enc_data[k] = self.__encrypt_value(self.ENVISION_JSON[k])
        with open(self.ENVISION_LOCK_FILE, 'w') as lock_file:
            json.dump(enc_data, lock_file, sort_keys = True, indent=0)
            lock_file.close()

    def __encrypt_value(self,v:str):
        return self.__encryption_algorithm.encrypt(v.encode()).decode()

    def __lock_key_file(self):
        with open(self.ENVISION_KEY_FILE, 'w') as key_file:
            key_file.write(self.key) 
            key_file.close()

    ########################################

    ################ USER ##################

    def get(self, key : str, default = None):
        try:
            return self.ENVISION_JSON[key]
        except:
            return default

    ########################################

    ################# CLI ##################

    def __add(self, key:str, value:str, override:bool):
        if not self.get(key):
            self.ENVISION_JSON[key] = value
        elif override:
            self.ENVISION_JSON[key] = value
        else:
            raise EnvironmentError('The key {} is already in the ENVISION configuration file. Add --override parameter to override.'.format(key))

        self.__update()
        self.__lock()

    def __remove(self,key):
        if self.get(key):
            del self.ENVISION_JSON[key]
        else:
            warnings.warn('The key {} is NOT in the ENVISION configuration file. Ignored.'.format(key))
            
        self.__update()
        self.__lock()

        

    #########################################

@click.command()
@click.option("--root", default='./', help="The root directory of the python project.")
@click.option("--token", default=None, help="Desired encryption key token.")
def init(root, token):
    """Simple CLI for initialization of a ENVISION managed project."""
    if isdir(root):

        if isfile(join(root,'.envision')):

            raise EnvironmentError('ENVISION project already initialized.')

        else:
            if token:
                with open(join(root,'.envision.key'), 'w') as key_file:
                    key_file.write(token) 
                    key_file.close()
            
            with open(join(root,'.envision'),'w') as env_file:
                json.dump({}, env_file, sort_keys = True, indent=0)
                env_file.close()

            envision(root)
    else:

        raise EnvironmentError('No directory found at {} .'.format(str(root)))

@click.command()
@click.option("--root", default='./', help="The root directory of the python project.")
@click.option("--key", prompt="Please, write the key for the environment variable to be added", help="Desired environment variable key to add.")
@click.option("--value", prompt="Please, write the value for the environment variable to be added", help="Desired environment variable value to add.")
@click.option("--override", is_flag=True, help="Overriding existing keys.")
def add(root, key:str,value:str, override:bool):
    """Simple CLI for adding a environment variable to a ENVISION managed project."""
    envision(root)._envision__add(key,value,override)

@click.command()
@click.option("--root", default='./', help="The root directory of the python project.")
@click.option("--key", prompt="Please, write the key for the environment variable to be removed", help="Desired environment variable key to remove.")
def remove(root, key:str):
    """Simple CLI for removing a environment variable to a ENVISION managed project."""
    envision(root)._envision__remove(key)

@click.command()
@click.option("--root", default='./', help="The root directory of the python project.")
@click.option("--token", default=None, help="Desired encryption key token.")
def lock(root,token):
    """Simple CLI for lock a ENVISION managed project."""
    envision(root)._envision__lock(token)

@click.group()
def cli():
    pass

cli.add_command(init)
cli.add_command(add)
cli.add_command(remove)
cli.add_command(lock)