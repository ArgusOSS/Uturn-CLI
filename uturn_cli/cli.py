import os
import signal
import psutil
import subprocess
import secrets
import click
import json
import requests
import pydriller

from .validate import validate_IP

config_dir = os.path.dirname(os.path.realpath(__file__))[:-3] + "server/"


@click.group()
def commands():
    pass

@click.command()
@click.option('--token', default=None, help="Set your own token to be used.")
@click.option('--port', type=click.INT,default=8001, help="Default port to start your Uturn server on.")
@click.option('--host', default="0.0.0.0",callback=validate_IP, help="Default host to start your Uturn server on.")
def init(token, port, host):
    """
        Initialise Uturn utils for your server.
    """
    if token is None:
        token = secrets.token_hex()
    with open(config_dir + "config.json", "w+") as file:
        json_to_save = {}
        json_to_save["port"] = port
        json_to_save["host"] = host
        json_to_save["token"] = token
        ip = requests.get('https://checkip.amazonaws.com').text.strip()
        json_to_save["IP"] = ip
        json_to_save["projects"] = {}
        file.write(json.dumps(json_to_save))

    print("Successfully configured the server. Use 'start' command to start the server now.")

@click.command()
@click.option('--name', help="A name for this project.")
@click.option('--projectpath', help="The root directory of your project. Must be the absolute path.", required=True)
@click.option('--stopprojectcommand', '--stop', help="Command to stop the project services before rollback.", required=True)
@click.option('--startprojectcommand', '--start', help="Command to start the project services after the rollback.", required=True)
@click.option('--mainbranch', help="The main branch of your project.", default="master")
def initproject(name, projectpath, mainbranch, stopprojectcommand,startprojectcommand, ):
    """
        Initialise Uturn support for a particular project.
    """
    if not name:
        name = projectpath.split('/')[-1]

    repo = pydriller.Repository(projectpath, only_in_branch=mainbranch)
    if projectpath[-1] != "/":
        projectpath += "/"

    with open(config_dir+"config.json", 'r') as file:
        json_read = json.loads(file.read())

    with open(config_dir+"config.json", 'w') as file:
        json_read["projects"][name] = {
            "path": projectpath, 
            "branch": mainbranch,
            "start": startprojectcommand,
            "stop": stopprojectcommand
        }
        json_to_write = json.dumps(json_read)
        file.write(json_to_write)
    
    print("Successfully mapped with your project.")

@click.command()
@click.option('--name', help="Name of your project.", required=True)
@click.option('--newpath', help="New path for your project.", required=True)
def updateprojectpath(name, newpath):
    """
        Update the path to the root directory for your project.
    """
    with open(config_dir+"config.json", 'r') as file:
        json_read = json.loads(file.read())
    
    with open(config_dir+"config.json", 'w') as file:
        project_json = json_read["projects"].get(name)
        if not project_json:
            raise Exception("This project doesn't exist!")    
        project_json["path"] = newpath
        json_read["projects"][name] = project_json
        file.write(json.dumps(json_read))
    print("Successfully updated the project!")

@click.command()
@click.option('--name', help="Name of your project.", required=True)
def deleteprojectpath(name):
    """
        Delete the path to the root directory for your project.
    """
    with open(config_dir+"config.json", 'r') as file:
        json_read = json.loads(file.read())

    with open(config_dir+"config.json", 'w') as file:
        project_json = json_read["projects"].get(name)
        if not project_json:
            raise Exception("This project doesn't exist!")
        json_read["projects"].pop(name, None)
        print("Successfully unmapped the project.")

@click.command()
@click.option('--name', help="Name of your project.", required=True)
def showprojectoptions(name):
    """
        Shows the configurations for your mapped project.
    """
    with open(config_dir+"config.json", '+') as file:
        json_read = json.loads(file.read())
        project_json = json_read["projects"].get(name)
        if not project_json:
            raise Exception("This project doesn't exist!")
        print(project_json)

@click.command()
def showoptions():
    """
        Shows the configurations for your Uturn server.
    """
    config_dir = os.path.dirname(os.path.realpath(__file__))[:-3] + "server/config.json"
    with open(config_dir, 'r') as file:
        print(file.read())

@click.command()
def start():
    """
        Start the Uturn server.
    """
    with open(config_dir+"config.json", 'r') as file:
        json_read = json.loads(file.read())

    log_file = config_dir+"gunicorn.log"
    if os.path.isfile(log_file):
        os.remove(log_file)

    if os.path.isfile(config_dir+"pid.txt"):
        print("Service already running.")
        return
    commands = ['gunicorn', '--chdir', config_dir,'main:app', '-b', json_read["host"]+":"+str(json_read["port"]), '--pid', config_dir+"pid.txt", '--daemon', '--access-logfile', log_file]
    subprocess.Popen(commands)
    print(f"Server started in the background! Visit http://{json_read['host']}:{json_read['port']}")

@click.command()
def stop():
    """
        Stop the Uturn server.
    """

    try:
        with open(config_dir+"pid.txt") as pidfile:
            pid = pidfile.read()
    except FileNotFoundError:
        print("Gunicorn process doesn't exist!")
        return

    try:
        process_name = psutil.Process(int(pid)).name()
    except psutil.NoSuchProcess:
        print("Gunicorn server has been stopped.")
        os.remove(config_dir+"pid.txt")
        return

    os.kill(int(pid), signal.SIGTERM)
    print("Stopped the flask server.")
    os.remove(config_dir+"pid.txt")

@click.command()
def logs():
    if not os.path.isfile(config_dir+"gunicorn.log"):
        print("Logs not found!")
        print("Remember that we wipe logs each run.")
        return
    with open(config_dir+"gunicorn.log", 'r') as file:
        content = file.read()
        print(content)

commands.add_command(init)
commands.add_command(initproject)

commands.add_command(updateprojectpath)
commands.add_command(deleteprojectpath)

commands.add_command(showoptions)
commands.add_command(showprojectoptions)

commands.add_command(start)
commands.add_command(logs)
commands.add_command(stop)

if __name__ == "__main__":
    commands()
