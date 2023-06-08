#MR-ROBOT: 1

**Today, we'll be looking at the MR-ROBOT machine on vulnhub.
You can download the machine here:**

<https://www.vulnhub.com/entry/mr-robot-1,151/>

Let's scan the machine with nmap.
```
┌──(root㉿kali)-[~]
└─# nmap 192.168.56.102
Starting Nmap 7.93 ( https://nmap.org ) at 2023-06-08 09:06 EET
Nmap scan report for 192.168.56.102
Host is up (0.00027s latency).
Not shown: 997 filtered tcp ports (no-response)
PORT    STATE  SERVICE
22/tcp  closed ssh
80/tcp  open   http
443/tcp open   https
MAC Address: 08:00:27:0E:F1:57 (Oracle VirtualBox virtual NIC)

Nmap done: 1 IP address (1 host up) scanned in 10.25 seconds
```
Browsing the machine at port 80, we have a terminal like page with commands to use.
Let's navigate to **robots.txt**

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/mrRobot/pics/pic1.png)

We can see that we have two files. 

One of them is the first key.

Let's download them to our machine.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/mrRobot/pics/pic2.png)

Let's perform a nikto scan.

![nikto scan](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/mrRobot/pics/pic3.png)

From the results of the scan, we can see it's running wordpress.
Let's go to the login page.
I'll login as **test** with the password **123** and capture the request with Burp suite with the proxy on.

![test_login](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/mrRobot/pics/pic4.png)

Let's send that request to intruder and try to brute force the login.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/mrRobot/pics/pic5.png)

Now, we'll clear the positions and add one to the log parameter.
We can use the file **fsociety.dic** we found earlier to brute force the login.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/mrRobot/pics/pic6.png)

Now, click on **Start attack**.
We can see that the username **Elliot** has a diffrent response length.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/mrRobot/pics/pic7.png)

Let's check that in the response tab.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/mrRobot/pics/pic8.png)

Now, let's brute force the password.
We'll use the same file we used before but we need to remove duplicates from it.

```cat fsociety.dic | uniq > fsociety.txt```

I'll use wpscan for the brute force but you can use any tool you like.

```wpscan --url http://192.168.56.102 -U Elliot -P fsocity.txt```

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/mrRobot/pics/pic9.png)

Great! We found the password.
Now, we can go back to the login page and login as Elliot.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/mrRobot/pics/pic10.png)

Now, let's upload a reverse shell on the target machine.
Go to Appearance -> Editor and add your php shell code to the 404.php file.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/mrRobot/pics/pic11.png)

Now, set up a netcat lisnter and go to http://192.168.56.102/404.php to execute the shell.

We got a shell!

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/mrRobot/pics/pic12.png)

You can stable your shell with those two commands.

```python -c 'import pty;pty.spawn("/bin/bash")'```

```export TERM=xterm```

Let's check the home dirctory.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/mrRobot/pics/pic13.png)

We found the second key but we can't read it.

We also found a file that contains the password for the user **robot**.

Let's decode the password.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/mrRobot/pics/pic14.png)

Now, let's switch user to **robot**.

We can now read the second key.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/mrRobot/pics/pic15.png)

Now, let's enumerate the machine more and try to get root.

I'll use the linpeas script.

I'll transfer it to the target machine using python http server.

But first you need to navigate to the **tmp** directory in order to run the script.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/mrRobot/pics/pic16.png)

Let's check SUID section.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/mrRobot/pics/pic17.png)

We can go to gtfobins and search for nmap.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/mrRobot/pics/pic18.png)

Let's try option (b)

We have successfully become root.

Now, we can view the third key.

![](https://raw.githubusercontent.com/user3016/vulnhub-writepus/main/mrRobot/pics/pic19.png)
