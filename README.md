
![Terminal Screenshot](https://i.imgur.com/4psD58C.png)

# Disclaimer

Not responsible for misuse. Please don't be an asshole.

# What is Zoombo?
It's a Zoom meeting cloud-share brute force cracker and automatic video file downloader. 

### What are some use-cases for Zoombo?

- When acquiring Slack tokens during Red Team engagements, or gaining access to a user's slack instance, you can then search for `zoom.us/rec/share` or `zoom.us/rec/play` links and then, if they're password-protected, brute-force access. 
- When finding a password-protected Zoom share during pentests, you'll want to be able to brute force the share. 


# Installaton

### Option 1
```
pip3 install -r requirements.txt
```

### Option 2 (pending updates)
```
docker build -t . zoombo
```

# Formats

### meetings.txt

```
https://{org}.zoom.us/rec/share/{id}
https://{org}.zoom.us/rec/share/{id}
https://{org}.zoom.us/rec/share/{id}
```

Note that the `{org}` info is just an example of what the target org could be, e.g.: `zoomorg`. Then the `{id}` is the 54-character share token at the end of the URL.

### passwords.txt

```
line
separated
password
list
```

# Example Usage

```
python3 zoombo.py -m meetings.txt -w rockyou.txt
```


# Help output

```
$ python3 zoombo.py -h

usage: zoombo.py [-h] -m MEETINGS -w WORDLIST

optional arguments:
  -h, --help            show this help message and exit
  -m MEETINGS, --meetings MEETINGS
                        A list of recording URLs to crack. e.g.: --meetings
                        company-a.txt
  -w WORDLIST, --wordlist WORDLIST
                        Any wordlist with passwords. e.g.: --wordlist
                        rockyou.txt

```


