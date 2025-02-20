# Me and My Girlfriend: 1

In this writeup, I will explain how I solved the *title* CTF challenge on vulnhub.
You can download the machine [here](https://www.vulnhub.com/entry/me-and-my-girlfriend-1,409/).

First, I'll start by scanning the network to find the target machine.
```
   nmap 192.168.100.1/24
   export ip=192.168.100.25
```

I'll scan the machine to get more details.

``` nmap -A $ip ```

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-02-20 21:03 EET
Nmap scan report for 192.168.100.25
Host is up (0.00071s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   1024 57:e1:56:58:46:04:33:56:3d:c3:4b:a7:93:ee:23:16 (DSA)
|   2048 3b:26:4d:e4:a0:3b:f8:75:d9:6e:15:55:82:8c:71:97 (RSA)
|   256 8f:48:97:9b:55:11:5b:f1:6c:1d:b3:4a:bc:36:bd:b0 (ECDSA)
|_  256 d0:c3:02:a1:c4:c2:a8:ac:3b:84:ae:8f:e5:79:66:76 (ED25519)
80/tcp open  http    Apache httpd 2.4.7 ((Ubuntu))
|_http-server-header: Apache/2.4.7 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
MAC Address: 08:00:27:47:9E:40 (Oracle VirtualBox virtual NIC)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running: Linux 3.X|4.X
OS CPE: cpe:/o:linux:linux_kernel:3 cpe:/o:linux:linux_kernel:4
OS details: Linux 3.2 - 4.9
Network Distance: 1 hop
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE
HOP RTT     ADDRESS
1   0.71 ms 192.168.100.25

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 21.21 seconds
```

From the Nmap scan, we can see that the target machine is running http and ssh.

I tried to access the machine's http server but I got this message.
![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/refs/heads/main/me-and-my-girlfriend/pics/pic1.png)

I viewed the page source and got this:
![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/refs/heads/main/me-and-my-girlfriend/pics/pic2.png)

This is a hint to use the X-Forwarded-For header to be able to access the page.

You can read about this header [here](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-For)

I intercepted the request with BurpSuite proxy and added this header: 
```X-Forwarded-For: localhost```
 And it worked!
![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/refs/heads/main/me-and-my-girlfriend/pics/pic3.png)

I then configured burp to added this header automatically to all requests.
You can do it by following these steps:
Proxy => Proxy Settings => search for "match and replace"
Then add the header as shown in the picture.
![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/refs/heads/main/me-and-my-girlfriend/pics/pic4.png)


I then got this page.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/refs/heads/main/me-and-my-girlfriend/pics/pic5.png)

I registered a new user and then logged in.
![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/refs/heads/main/me-and-my-girlfriend/pics/pic6.png)

I then visited the different pages here and noticed that the profile page identifies users by the parameter 'id' in the request.
I tried changing the parameter and I got access to other users creds.

I tried logging with these creds to the ssh server and I got in as the Alice.
![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/refs/heads/main/me-and-my-girlfriend/pics/pic7.png)

I then found the first flag and a note in a hidden directory inside alice's home directory.
![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/refs/heads/main/me-and-my-girlfriend/pics/pic8.png)

I then ran the command ```sudo -l``` to see if alice can run any commands with sudo.
![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/refs/heads/main/me-and-my-girlfriend/pics/pic9.png)

Great!
We can use php to run a bash shell as root.
I then used the system function to run ```/bin/bash``` and get a shell as root.
![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/refs/heads/main/me-and-my-girlfriend/pics/pic10.png)

It worked and I got the root flag.
