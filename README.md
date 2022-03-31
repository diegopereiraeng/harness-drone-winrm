# harness-drone-winrm
Plugin to run CI commands in Windows Remote Machines

WinRM allows you to perform various management tasks remotely. These include, 
but are not limited to: running batch scripts, powershell scripts, and fetching 
WMI variables.

Used by [Harness](https://www.harness.io/) for CIE Windows Onprem support.

For more information on WinRM, please visit
[Microsoft's WinRM site](http://msdn.microsoft.com/en-us/library/aa384426.aspx).


For more information on PLUGIN and ADVANCED settings, please visit
[DOCUMENTATION](https://github.com/diegopereiraeng/harness-drone-winrm/blob/main/DOCS.MD).



### CIE Pipeline example
```commandline
- step:
    type: Plugin
    name: "Windows Remote Execution"
    identifier: WinRM_Command
    spec:
        connectorRef: account.DockerHubDiego
        image: diegokoala/harness-drone-winrm:stable
        privileged: false
        settings:
            endpoint: "https://10.15.17.52:5986/wsman"
            transport: "ntlm"
            username: "diego-windows\diego_pereira"
            password: "."
            COMMAND: "netstat -an | findstr 5986"
            COMMAND2: 'powershell -command "$result = Invoke-WebRequest -URI https://www.harness.io/; $result | % ToString"'
            repo: "https://github.com/diegopereiraeng/DiegoFrameworkWebApplication"
            git_clone_folder: "C:\Builds\diego_pereira"
```
### Testing the docker image:
```commandline
docker run --rm \
  -e PLUGIN_ENDPOINT="https://10.15.17.52:5986/wsman" \
  -e PLUGIN_TRANSPORT="ntlm" \
  -e PLUGIN_USERNAME="diego-windows\diego_pereira" \
  -e PLUGIN_PASSWORD="senha123$%^&" \
  -e PLUGIN_SERVER_CERT_VALIDATION="ignore" \
  -e PLUGIN_COMMAND="netstat -an | findstr 5986" \
  -e PLUGIN_COMMAND2="dir C:\Users\diego_pereira\Desktop\DiegoFrameworkWebApplication" \
  -e PLUGIN_COMMAND3="hostname" \
  -e PLUGIN_COMMAND4="ipconfig && msg * Hello Harness" \
  -e PLUGIN_REPO="https://github.com/diegopereiraeng/DiegoFrameworkWebApplication" \
  -e PLUGIN_REPO_FOLDER="DiegoFrameworkWebApplication" \
  -e PLUGIN_GIT_CLONE_FOLDER="C:\Users\diego_pereira\Desktop" \
  diegokoala/harness-drone-winrm:stable

