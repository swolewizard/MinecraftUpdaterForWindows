# MinecraftUpdater
(Updated by swolewizard for windows from eclair4151)

This is a python package to automate the updating of your server. Its so annoying to try and download the jar,
ftp it over, stop the server, back up your world, etc. This automates alll that. just git clone this in the root of
your server. Then run python update.py in the server directory. it will check if you have the
latest version. If not if will download the latest jar, force close the servers GUI and save the world in the console. it will then backup your world/Previous server.jar into a new folder when it updates incase something goes wrong. then update the server jar and start the server back up in a new console.


## Scheduling Updates, Get your server updated within 1-5mins of an Minecraft update
           
This script is intended to be run as a cron job/Task.
           
https://www.windowscentral.com/how-create-automated-task-using-task-scheduler-windows-10
           
### Begin this script/task At startup, repeat task every 5mins, for a duration of Indefinitely.
           
This will update your server automatically when a new minecraft update is released within 1-5mins.
           
![Capture](https://user-images.githubusercontent.com/46814896/123729648-6fd2d600-d8e9-11eb-8d3d-aeebcfa4a15c.PNG)
           
## Make sure you have a .bat in your server directory where updater.py is located, called 'Manual_run.bat' with

```
@ECHO OFF

java -Xms4096M -Xmx4096M -jar minecraft_server.jar

pause
```
## Make sure your server starts with a GUI and console
           
The way this code works is it force closes java.exe to stop the server enabling the cmd prompt to save the world, so you probably can't host a server and play minecraft at the same time on the same computer. Haven't tested that though

![Minecraft-Server-Setup-GUI](https://user-images.githubusercontent.com/46814896/123729435-14084d00-d8e9-11eb-975e-a602d96b3fe8.png)
        
## Updated java
Make sure your java and java JDK SE is updated, if you're getting server starting errors.
           
https://www.oracle.com/java/technologies/javase-downloads.html


## Configuration

### Latest vs. Snapshot
UPDATE_TO_SNAPSHOT = <True,False>

### Backup Directory
BACKUP_DIR = <name of directory to save files>

### Backup Previous jars 
JARBACKUP_DIR = <name of directory to save files>
           
### Log File
LOG_FILENAME = <name of file to save log messages>

           
      
