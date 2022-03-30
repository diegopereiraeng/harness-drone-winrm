from ast import If
import winrm
from winrm.protocol import Protocol
import os
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ.get('PLUGIN_ENDPOINT') 
TRANSPORT = os.environ.get('PLUGIN_TRANSPORT') 
USERNAME = os.environ.get('PLUGIN_USERNAME')
PASSWORD = os.environ.get('PLUGIN_PASSWORD')
SERVER_CERT_VALIDATION = os.environ.get('PLUGIN_SERVER_CERT_VALIDATION') or "ignore"
REPO = os.environ.get('PLUGIN_REPO') or "ignore"
REPO_FOLDER = os.environ.get('PLUGIN_REPO').rsplit('/', 1)[-1] or "ignore"
GIT_CLONE_FOLDER = os.environ.get('PLUGIN_GIT_CLONE_FOLDER') or "ignore"
COMMAND = os.environ.get('PLUGIN_COMMAND')
COMMAND2 = os.environ.get('PLUGIN_COMMAND2') or "ignore"
COMMAND3 = os.environ.get('PLUGIN_COMMAND3') or "ignore"
COMMAND4 = os.environ.get('PLUGIN_COMMAND4') or "ignore"

def winRMCommand(name,command):
    # NTLM Auth
    p = Protocol(
        endpoint=ENDPOINT,
        transport=TRANSPORT,
        username=USERNAME,
        password=PASSWORD,
        server_cert_validation=SERVER_CERT_VALIDATION)
    shell_id = p.open_shell()
    command_id = p.run_command(shell_id, command)
    std_out, std_err, status_code = p.get_command_output(shell_id, command_id)
    p.cleanup_command(shell_id, command_id)
    print(name+" Status Code: "+str(status_code))
    print(name+" Output: "+std_out.decode('UTF-8'))
    print(name+" Error Output: "+std_err.decode('UTF-8'))
    return std_out, std_err, status_code


def main():
    if TRANSPORT != 'basic':
        # NTLM Auth
        p = Protocol(
            endpoint=ENDPOINT,
            transport=TRANSPORT,
            username=USERNAME,
            password=PASSWORD,
            server_cert_validation=SERVER_CERT_VALIDATION)
        shell_id = p.open_shell()
        if REPO != 'ignore' and REPO_FOLDER != 'ignore':
            print('Deleting Existing Temp Folder: rmdir c:\\temp\\'+REPO_FOLDER+' /s /q')
            std_out, std_err, status_code = winRMCommand("Temp Cleaner", 'rmdir "c:\\temp\\'+REPO_FOLDER+'" /s /q')

            print('Moving Existing App Folder: '+GIT_CLONE_FOLDER+'\\'+REPO_FOLDER+' to c:/Temp: ')
            std_out, std_err, status_code =  winRMCommand("Temp Cleaner", 'move '+GIT_CLONE_FOLDER+'\\'+REPO_FOLDER+' C:\\temp')

            if status_code != 0:
                print("Error on step: Move to Temp")
                exit(2)


            print('Cloning Repo: '+REPO) 
            std_out, std_err, status_code = winRMCommand("Git Clone", 'powershell -command "$result = git clone '+REPO+' '+GIT_CLONE_FOLDER+'\\'+REPO_FOLDER+' 2>&1 ; if ($LASTEXITCODE) { Throw \\"git failed (exit code: $LASTEXITCODE):`n$($result -join \\"`n\\")\\" }; $result | % ToString  "')

            if status_code != 0:
                print("Error on step: Git Clone")
                exit(3)
        
        print('Running Command: '+COMMAND) 
        std_out, std_err, status_code = winRMCommand("COMMAND", COMMAND)
        if status_code != 0:
            print("Error on step: COMMAND")
            exit(4)

        if COMMAND2 != 'ignore':
            print('Running Command 2: '+COMMAND2) 
            std_out, std_err, status_code = winRMCommand("COMMAND2", COMMAND2)
            if status_code != 0:
                print("Error on step: COMMAND2")
                exit(4)
        
        if COMMAND3 != 'ignore':
            print('Running Command 3: '+COMMAND3) 
            std_out, std_err, status_code = winRMCommand("COMMAND3", COMMAND3)
            if status_code != 0:
                print("Error on step: COMMAND3")
                exit(4)
        
        if COMMAND4 != 'ignore':
            print('Running Command 4: '+COMMAND4) 
            std_out, std_err, status_code = winRMCommand("COMMAND4", COMMAND)
            if status_code != 0:
                print("Error on step: COMMAND4")
                exit(4)
        
        p.close_shell(shell_id)


    if TRANSPORT == 'basic':
        # Basic Auth
        session = winrm.Session(ENDPOINT, auth=(USERNAME,PASSWORD))

        result = session.run_ps("hostname\r\nwhoami\r\nipconfig")

        print(result.status_code)
        print(result.std_out)

        result = session.run_ps(COMMAND)

        print(result.status_code)
        print(result.std_out)
        if status_code != 0:
            exit(11)

if __name__ == "__main__":
    main()




