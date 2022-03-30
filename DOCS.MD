### Plugin Settings

```yaml
ENDPOINT: Endpoint WinRM address. 
ex: "https://10.15.17.52:5986/wsman"

TRANSPORT: The Auth method to be used. 
ex: "ntlm"
obs: now basic auth will run direct ps commands instead of cmd commands, native git clone doesn't work for basic auth as well.

USERNAME: Windows username including that machine name or domain, 
ex: "diego-windows\diego_pereira"

PASSWORD: Windows user password. 
ex: <+secrets.getValue('account.diego_windows_pass')> or "senha123$%^&"

SERVER_CERT_VALIDATION: put ignore to skip Cert Verification. 
ex: "ignore"

COMMAND: Multiline Command 1. 
ex: "netstat -an | findstr 5986"

COMMAND2: Multiline Command 2. 
ex: "dir C:\Builds\DiegoFrameworkWebApplication"

COMMAND3: Multiline Command 3. 
ex: 'powershell -command "$result = Invoke-WebRequest -URI https://www.harness.io/; $result | % ToString"'

COMMAND4: Multiline Command 4

REPO: Git Repo. ex: "https://github.com/diegopereiraeng/DiegoFrameworkWebApplication"

GIT_CLONE_FOLDER: Folder to clone the repo. 
ex: "C:\Builds\diego_pereira"
```

### To use Kerberos authentication you need these optional dependencies (Add in requeriments.txt)

```bash
# for Debian/Ubuntu/etc:
$ sudo apt-get install gcc python-dev libkrb5-dev
$ pip install pywinrm[kerberos]

# for RHEL/CentOS/etc:
$ sudo yum install gcc python-devel krb5-devel krb5-workstation python-devel
$ pip install pywinrm[kerberos]
```

### To use CredSSP authentication you need these optional dependencies (Add in requeriments.txt)

```bash
# for Debian/Ubuntu/etc:
$ sudo apt-get install gcc python-dev libssl-dev
$ pip install pywinrm[credssp]

# for RHEL/CentOS/etc:
$ sudo yum install gcc python-devel openssl-devel
$ pip install pywinrm[credssp]
```

### Valid transport options (transport setting options)

harness-drone-winrm supports various transport methods in order to authenticate with the WinRM server. The options that are supported in the `transport` parameter are;
* `basic`: Basic auth only works for local Windows accounts not domain accounts. Credentials are base64 encoded when sending to the server.
* `plaintext`: Same as basic auth.
* `certificate`: Authentication is done through a certificate that is mapped to a local Windows account on the server.
* `ssl`: When used in conjunction with `cert_pem` and `cert_key_pem` it will use a certificate as above. If not will revert to basic auth over HTTPS.
* `kerberos`: Will use Kerberos authentication for domain accounts which only works when the client is in the same domain as the server and the required dependencies are installed. Currently a Kerberos ticket needs to be initialized outside of harness-drone-winrm using the `kinit` command.
* `ntlm`: Will use NTLM authentication for both domain and local accounts.
* `credssp`: Will use CredSSP authentication for both domain and local accounts. Allows double hop authentication. This only works over a HTTPS endpoint and not HTTP.






### Encryption

By default, WinRM will not accept unencrypted communication with a client. There are two ways
to enable encrypted communication with harness-drone-winrm:

1. Use an HTTPS endpoint instead of HTTP (Recommended)
2. Use NTLM, Kerberos, or CredSSP as the transport auth

Using an HTTPS endpoint is recommended, as it will encrypt all the data sent
to the server (including all headers), works securely with all
auth types, and can properly verify remote host identity (when used with certificates signed by a 
verifiable certificate authority). You can use [this script](https://github.com/ansible/ansible/blob/devel/examples/scripts/ConfigureRemotingForAnsible.ps1)
to easily set up a HTTPS endpoint on WinRM with a self-signed certificate, but
the use of a verifiable certificate authority is recommended in production environments.

The second option is to use NTLM, Kerberos, or CredSSP, and set the `message_encryption`
arg to protocol to `auto` (the default value) or `always`. This will use the authentication GSS-API
Wrap and Unwrap methods to encrypt the message contents sent to
the server. This form of encryption is independent of the transport layer, and the strength of the encryption
used varies with the underlying authentication type selected (NTLM generally being the weakest and CredSSP the
strongest). 

To configure message encryption you can use the `message_encryption` argument
when initialising protocol. This option has 3 values that can be set as shown
below.

* `auto`: Default, Will only use message encryption if it is available for the auth method and HTTPS isn't used.
* `never`: Will never use message encryption even when not over HTTPS.
* `always`: Will always use message encryption even when running over HTTPS (fails if encryption support is unavailable on the selected auth method).

If you set the value to `always` and the transport opt doesn't support message
encryption (e.g., `basic` auth or an old version of `pykerberos` without message 
encryption support is installed), harness-drone-winrm will throw an exception.

If you do not use an HTTPS endpoint or message encryption, a default-configured WinRM
server will automatically reject requests from harness-drone-winrm. Server settings can be modified
allow unencrypted messages and credentials, but this is highly
insecure and should only be used for diagnostic purposes. To allow unencrypted communications,
run the following on the WinRM server (cmd and powershell versions provided):

```
# from cmd
winrm set winrm/config/service @{AllowUnencrypted="true"}

# or from powershell
Set-Item -Path "WSMan:\localhost\Service\AllowUnencrypted" -Value $true
```

Again, this should *not* be used in production environments, as your credentials and WinRM 
messages can be trivially recovered.


### Enabling WinRM on remote host
Enable WinRM over HTTP and HTTPS with self-signed certificate (includes firewall rules):

```
# from powershell:
Invoke-Expression ((New-Object System.Net.Webclient).DownloadString('https://raw.githubusercontent.com/ansible/ansible/devel/examples/scripts/ConfigureRemotingForAnsible.ps1'))
```

Enable WinRM over HTTP for test usage (includes firewall rules):
```
winrm quickconfig
```

Enable WinRM basic authentication. For domain users, it is necessary to use NTLM, Kerberos, or CredSSP authentication (Kerberos and NTLM authentication are enabled by default, CredSSP is not).
```
# from cmd:
winrm set winrm/config/service/auth @{Basic="true"}
```

Enable WinRM CredSSP authentication. This allows double hop support so you can authenticate with a network service when running command son the remote host. This command is run in Powershell.
```powershell
Enable-WSManCredSSP -Role Server -Force
Set-Item -Path "WSMan:\localhost\Service\Auth\CredSSP" -Value $true
```