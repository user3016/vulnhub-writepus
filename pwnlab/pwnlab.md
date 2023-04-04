#PWNLAB: INIT
**Today, we'll be looking at the PwnLab machine on vulnhub.
You can download the machine here:**
<https://www.vulnhub.com/entry/pwnlab-init,158//>

Let's scan the machine with nmap.
![nmap scan](/pics/pic1.jpg)

We can see that it's running **http**, **rpcbind** and **mysql**.
Browsing the machine at port 80 we can see that we have three pages.
We need to be logged in to upload.

Let's perform a nikto scan. 
![nikto scan](/pics/pic2.png)


If we try to navigate to config file to view it's contents, we won't see anything.
After some research, I found this LFI method here:
<https://diablohorn.com/2010/01/16/interesting-local-file-inclusion-method/>
You can also find it here: <https://book.hacktricks.xyz/pentesting-web/file-inclusion/>

Applying that and capturing the request with burp suite, we can see the following.

![burp suite](/pics/pic3.png)

Let's change the **in.php** to **config** to view the config file.

![burp suite](/pics/pic4.png)

Looks like we have some **base64** encoded text.
Let's decode that.

![decoded](/pics/pic5.png)

Let's try and log in to mysql with these credentials.
We got in!

Let's check the databases in there.

![mysql](/pics/pic6.png)

We found three usernames and their passwords.
Let's decode the passwords

![decoded passwords](/pics/pic7.png)

It worked! 
Now we can upload a reverse shell.
And looks like it only accepts images.
Let's add the gif header to the top and change the file extension to png.

GIF header: **GIF87a**

![gif header](/pics/pic8.png)

If we use the command **file** on the shell we can see it's shown as png.

![file](/pics/pic9.png)

If we navigate to the upload folder we can see out shell is uploaded.

![shell uploaded](/pics/pic10.png)

But if we try to execute it we will get an error.
After some research, I found that we can replace the cookie with our shell in order to execute it.

![netcat shell](/pics/pic11.png)

Replace the cookie with **"lang=../upload/image_name"**
Forward that...
And we got a shell!

![netcat shell](/pics/pic12.png)

I switched user to kent but didn't find anything useful.
So, I switched user to kane.
In the home folder of kane, I found this executable file.

![msgmike](/pics/pic13.png)
Let's perform strings on it.
We can see that it uses the command cat.
We can make the cat command execute a bash shell.
But first, we need to cd into tmp.
We also need to modify the path variable to be able to execute our cat command.

![](/pics/pic14.png)
Executing that, we became mike.

![](/pics/pic15.png)
In mike's home directory, we found an executable file called **msg2root**.
As expected, this file is vulnerable to command injection.
Let's use that to get a root shell.
Trying to open a bash shell won't work.

![](/pics/pic16.png)
So let's try sh instead.
And it worked.
![root](/pics/pic17.png)
We are now root.
**Note: you need to remove the cat command we created earlier to be able to use the normal cat command and view the flag.**
![](/pics/pic18.png)