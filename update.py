import os
import time
import shutil
import hashlib
import time
import subprocess
from subprocess import PIPE
from datetime import datetime
import logging
import requests

# CONFIGURATION
UPDATE_TO_SNAPSHOT = True
MANIFEST_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
BACKUP_DIR = 'world_backups'
JARBACKUP_DIR = 'previous_jars'
LOG_FILENAME = 'Update_Log.log'


logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO,format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',)
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())

# retrieve version manifest
response = requests.get(MANIFEST_URL)
data = response.json()

if UPDATE_TO_SNAPSHOT:
    minecraft_ver = data['latest']['snapshot']
else:
    minecraft_ver = data['latest']['release']
    
# Create dependency files if they don't exist
if not os.path.exists('eula.txt'):
    v = open('eula.txt', 'w')
    v.write('eula=true')
    v.close()
    
if not os.path.exists('Manual_Run.bat'):
    v = open('Manual_Run.bat', 'w')
    v.write('@ECHO OFF')
    v.write('\n')
    v.write('java -Xms4096M -Xmx4096M -jar minecraft_server.jar')
    v.write('\n')
    v.write('pause')
    v.close()

if not os.path.exists('minecraft_server.jar'):
    f = open('minecraft_server.jar', 'x')
    
if not os.path.exists('world'):
    os.makedirs('world')

# get checksum of running server
if os.path.exists('minecraft_server.jar'):
    sha = hashlib.sha1()
    f = open("minecraft_server.jar", 'rb')
    sha.update(f.read())
    cur_ver = sha.hexdigest()
else:
    cur_ver = ""

for version in data['versions']:
    if version['id'] == minecraft_ver:
        jsonlink = version['url']
        jar_data = requests.get(jsonlink).json()
        jar_sha = jar_data['downloads']['server']['sha1']

        
        if cur_ver != jar_sha:
            logging.info('Update Found.')
            print('='*78)
            print('Update Found.')
            print()
            logging.info('Your sha1 is ' + cur_ver + '. Latest version is ' + str(minecraft_ver) + " with sha1 of " + jar_sha)
            print('Your sha1 is ' + cur_ver + '. Latest version is ' + str(minecraft_ver) + " with sha1 of " + jar_sha)
            print('='*78)
            
            if process_exists('java.exe'):
                logging.info('Updating server...')
                print('Updating server...')
                
                logging.info('Stopping server.')
                print('Stopping server.')
                os.system("TASKKILL /IM java.exe")
                time.sleep(5)
            else:
                logging.info("Server isn't running...")
                print("Server isn't running...")
                
            if not os.path.exists(JARBACKUP_DIR):
                os.makedirs(JARBACKUP_DIR)

            backupPath2 = os.path.join(
                JARBACKUP_DIR,
                "minecraft_server_sha=" + cur_ver + ".jar")
            shutil.copy("minecraft_server.jar", backupPath2)
            
            link = jar_data['downloads']['server']['url']
            logging.info('Downloading minecraft_server.jar from ' + link + '...')
            print('Downloading minecraft_server.jar from ' + link + '...')
            response = requests.get(link)
            with open('minecraft_server.jar', 'wb') as jar_file:
                jar_file.write(response.content)
            logging.info('Downloaded.')
            print('Downloaded.')
            
            logging.info('Backing up world...')
            print('Backing up world...')

            if not os.path.exists(BACKUP_DIR):
                os.makedirs(BACKUP_DIR)

            backupPath = os.path.join(
                BACKUP_DIR,
                "world" + "_backup_" + datetime.now().isoformat().replace(':', '-') + "_sha=" + cur_ver)
            shutil.copytree("world", backupPath)
            
            logging.info('Backed up world.')
            print('Backed up world.')
            
            logging.info('Starting server...')
            print('Starting server...')
            logging.info('='*78)
            
            os.system('start call Manual_Run.bat')
        else:
            print("Server is already up to date.")
            print('Latest version is ' + str(minecraft_ver))
            time.sleep(5)
        break

