<h1>KIOPTRIX: LEVEL 1</h1>
Today we'll be looking at the kioptrix 1 machine on vulnhub.

You can download the machine [here](https://www.vulnhub.com/entry/kioptrix-level-1-1,22/).

<h2>Nmap</h2>

```
┌──(root㉿kali)-[~]
└─# nmap -A -sV 192.168.1.109  
Starting Nmap 7.93 ( https://nmap.org ) at 2023-04-10 17:14 EET
Nmap scan report for 192.168.1.109
Host is up (0.00041s latency).
Not shown: 994 closed tcp ports (reset)
PORT     STATE SERVICE     VERSION
22/tcp   open  ssh         OpenSSH 2.9p2 (protocol 1.99)
|_sshv1: Server supports SSHv1
| ssh-hostkey: 
|   1024 b8746cdbfd8be666e92a2bdf5e6f6486 (RSA1)
|   1024 8f8e5b81ed21abc180e157a33c85c471 (DSA)
|_  1024 ed4ea94a0614ff1514ceda3a80dbe281 (RSA)
80/tcp   open  http        Apache httpd 1.3.20 ((Unix)  (Red-Hat/Linux) mod_ssl/2.8.4 OpenSSL/0.9.6b)
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Apache/1.3.20 (Unix)  (Red-Hat/Linux) mod_ssl/2.8.4 OpenSSL/0.9.6b
|_http-title: Test Page for the Apache Web Server on Red Hat Linux
111/tcp  open  rpcbind     2 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2            111/tcp   rpcbind
|   100000  2            111/udp   rpcbind
|   100024  1           1024/tcp   status
|_  100024  1           1024/udp   status
139/tcp  open  netbios-ssn Samba smbd (workgroup: MYGROUP)
443/tcp  open  ssl/https   Apache/1.3.20 (Unix)  (Red-Hat/Linux) mod_ssl/2.8.4 OpenSSL/0.9.6b
| ssl-cert: Subject: commonName=localhost.localdomain/organizationName=SomeOrganization/stateOrProvinceName=SomeState/countryName=--
| Not valid before: 2009-09-26T09:32:06
|_Not valid after:  2010-09-26T09:32:06
|_http-server-header: Apache/1.3.20 (Unix)  (Red-Hat/Linux) mod_ssl/2.8.4 OpenSSL/0.9.6b
|_http-title: 400 Bad Request
|_ssl-date: 2023-04-10T15:17:13+00:00; +1m57s from scanner time.
| sslv2: 
|   SSLv2 supported
|   ciphers: 
|     SSL2_DES_192_EDE3_CBC_WITH_MD5
|     SSL2_RC4_64_WITH_MD5
|     SSL2_RC4_128_EXPORT40_WITH_MD5
|     SSL2_RC2_128_CBC_EXPORT40_WITH_MD5
|     SSL2_RC2_128_CBC_WITH_MD5
|     SSL2_RC4_128_WITH_MD5
|_    SSL2_DES_64_CBC_WITH_MD5
1024/tcp open  status      1 (RPC #100024)
MAC Address: B0:A4:60:CC:CC:61 (Intel Corporate)
Device type: general purpose
Running: Linux 2.4.X
OS CPE: cpe:/o:linux:linux_kernel:2.4
OS details: Linux 2.4.9 - 2.4.18 (likely embedded)
Network Distance: 1 hop

Host script results:
|_clock-skew: 1m56s
|_smb2-time: Protocol negotiation failed (SMB2)
|_nbstat: NetBIOS name: KIOPTRIX, NetBIOS user: <unknown>, NetBIOS MAC: 000000000000 (Xerox)

TRACEROUTE
HOP RTT     ADDRESS
1   0.41 ms 192.168.1.109

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 28.75 seconds
```
<h2>smb enumeration</h2>

We can see that the machine is running smb.

Let's use metasploit to figure out the smb version running.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix1/pics/pic1.png)

Let's use **auxiliary/scanner/smb/smb_version**

Now, Set the rhosts to the machine's IP.

```set rhosts <MACHINE_IP>```

Now, type ```run```

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix1/pics/pic2.png)

Now, that we have the smb version, let's search for an exploit.

Let's use this module: **exploit/linux/samba/trans2open** and set the options.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix1/pics/pic3.png)

We also need to replace the default payload with 

Now, let's run it.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix1/pics/pic4.png)

Let's interact with any of the opened sessions.

```sessions -i 4```

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix1/pics/pic5.png)

Yes! we are now root.
