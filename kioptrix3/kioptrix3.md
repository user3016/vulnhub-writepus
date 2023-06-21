# Kioptrix: Level 1.2 (#3)

Today, we'll be looking at the Kioptrix level 3 machine on vulnhub.

You can download the machine [here](https://www.vulnhub.com/entry/kioptrix-level-12-3,24/).

Let's scan the machine with nmap.
```
┌──(root㉿kali)-[~/kioptrix3]
└─# nmap 172.16.243.132           
Starting Nmap 7.93 ( https://nmap.org ) at 2023-06-13 08:23 EET
Nmap scan report for 172.16.243.132
Host is up (0.0018s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
MAC Address: 00:0C:29:1D:5C:C5 (VMware)

Nmap done: 1 IP address (1 host up) scanned in 6.46 seconds
```
Let's use dirsearch to discover dirctories.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix3/pics/pic5.png)

Browsing the machine on port 80, we can see that the login page is running **LotusCMS**.

We found a vulnerability on exploitdb.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix3/pics/pic1.png)

Let's fire up metasploit.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix3/pics/pic2.png)

Now, let's set the options.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix3/pics/pic3.png)

We got a shell!

You can make it stable with these two commands.

```
python -c 'import pty;pty.spawn("/bin/bash")'
export TERM=xterm
```

Now, I'll use linpeas for enumeration.

And we found a password.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix3/pics/pic4.png)

Let's use the password to login in the phpmyadmin dirctory.

We successfully logged in as root.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix3/pics/pic6.png)

Searching in the database, we found two users and their passwords.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix3/pics/pic7.png)

Let's encode the passwords.

You can use this website: <https://hashes.com/en/tools/hash_identifier>

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix3/pics/pic8.png)


![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix3/pics/pic9.png)

Now, let's ssh into the machine.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix3/pics/pic10.png)

Let's use ```sudo -l```

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix3/pics/pic11.png)

You can also find it written in the company policy file.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix3/pics/pic12.png)

We can privesc is by editing the sudoers file using ht.

```sudo ht```

Now press F3 and type **/etc/sudoers**

Now, we can add /bin/bash to the user loneferret.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix3/pics/pic13.png)

press F2 to save.

Now, we can run /bin/bash and get a root shell.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix3/pics/pic14.png)