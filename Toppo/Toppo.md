<h1>Toppo: 1</h1>

Today, we'll be looking at the Toppo 1 machine on vulnhub.

You can download the machine [here](https://www.vulnhub.com/entry/toppo-1,245/).


Let's scan the machine with nmap.
```
┌──(root㉿kali)-[~/toppo]
└─# nmap 172.16.243.133           
Starting Nmap 7.93 ( https://nmap.org ) at 2023-06-12 10:58 EET
Nmap scan report for 172.16.243.133
Host is up (0.00020s latency).
Not shown: 997 closed tcp ports (reset)
PORT    STATE SERVICE
22/tcp  open  ssh
80/tcp  open  http
111/tcp open  rpcbind
MAC Address: 00:0C:29:76:1A:E1 (VMware)

Nmap done: 1 IP address (1 host up) scanned in 5.82 seconds
```
Now, lets' use dirsearch to discover directories.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/Toppo/pics/pic1.png)

Let's check the admin directory.

We found an interesting file: **notes.txt**.

Great! We got a password.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/Toppo/pics/pic2.png)

And looking at the password, we can guess that the username is **ted**.

Let's ssh into the machine.

We got in!

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/Toppo/pics/pic3.png)

Now, I'll use linpeas for enumeration.

Looking at the suid section, we have two ways to gain root access.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/Toppo/pics/pic4.png)

You can use the following command to get a root shell with python:

```python2 -c 'import pty;pty.spawn("/bin/sh")'```

We became root and got the flag.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/Toppo/pics/pic5.png)

You can also use **mawk** to get root.

Let's search for **mawk** on gtfobins.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/Toppo/pics/pic6.png)

Let's use the command.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/Toppo/pics/pic7.png)