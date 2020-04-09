
![Terminal Screenshot](https://i.imgur.com/4psD58C.png)

# What is Zoombo?
It's a Zoom meeting cloud-share brute force cracker and automatic video file downloader. 

# Installaton

## Option 1
```
pip3 install -r requirements.txt
```

## Option 2 (pending updates)
```
docker build -t . zoombo
```

# Formats

## meetings.txt

```
https://{org}.zoom.us/rec/share/{id}
https://{org}.zoom.us/rec/share/{id}
https://{org}.zoom.us/rec/share/{id}
```

## rockyou.txt

```
line
separated
password
list
```


# Usage

```
$ python3 zoombo.py -h
usage: zoombo.py [-h] -m MEETINGS -w WORDLIST

optional arguments:
  -h, --help            show this help message and exit
  -m MEETINGS, --meetings MEETINGS
                        A list of recording URLs to crack. e.g.: --meeting-
                        list company-a.txt
  -w WORDLIST, --wordlist WORDLIST
                        Any wordlist with passwords. e.g.: --word-list
                        rockyou.txt

```
