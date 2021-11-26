import os
from urllib.request import urlretrieve
from urllib.parse import urlparse
import requests
import unicodedata
import re
from pathlib import Path
import zipfile

# Global variables
github_repo = "STJr/SRB2"
github_releases = "https://github.com/STJr/SRB2/releases/tag/"
git_url = "https://github.com/{}/releases/".format(github_repo)
history_url = "https://files.srb2.org/srb2.org/history/"
gitlab = "https://git.do.srb2.org/STJr/SRB2"

# Major versions are decided by whether SRB2MB has mods specifically for that version.
# We don't need every minor patch release to be available,
# just major releases that break mod compatibility with previous versions.
# This variable will need updated manually for every major release of SRB2.
major_versions = [""]

class Downloader:
    """
    Class for managing mods and SRB2 versions in various folders.
    An example of the folder structure is as follows:
    - /SRB2
        - /2.2
            - /mods
                - /Multiplayer Map Pack
        - /1.09
            - /mods
                - /I Cant Think Of A Name Zone

    Subdirectories of /mods will be named after their MB thread name,
    scrapped free of special characters that Windows/Linux does not allow in folder names.
    """

    def __init__(self, home_dir="./SRB2"):
        self.home_dir = home_dir
        self.executable_list = []
        self.version_dirs = []
        self.mod_dir = "/mods"
        # Github API has a request limit. See set_github_response()
        self.github_response = None
        self.version_num_regex = '(?:(\d+)\.)?(?:(\d+)\.)?(?:(\d+)\.\d+)'
        self.latest_version = None  # see get_latest_version_number()

    def slugify(self, mod_name, allow_unicode=False):
        """
        Convert spaces or repeated dashes to single dashes.
        Remove characters that aren't alphanumerics, underscores, or hyphens.
        Convert to lowercase. Also strip leading and trailing whitespace, dashes, and underscores.

        Used for converting SRB2 MB thread names to valid file/folder names,
        for organizing mod downloads.
        """
        value = str(mod_name)
        if allow_unicode:
            value = unicodedata.normalize('NFKC', value)
        else:
            value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
        value = re.sub(r'[^\w\s-]', '', value.lower())
        return re.sub(r'[-\s]+', '-', value).strip('-_')

    def create_version_dir(self, srb2_version):
        full_path = self.home_dir + "/" + srb2_version
        Path(full_path).mkdir(parents=True, exist_ok=True)
        return full_path

    def get_latest_version_number(self, github=True, gitlab=False, srb2org=False):
        match = None
        if github:
            response = self.set_github_response()
            latest = response.json()["name"]
            try:
                match = re.search(self.version_num_regex, latest, re.IGNORECASE).group()
            except:
                # TODO - create logging and exception handling?
                match = None
        elif gitlab:  # TODO - implement gitlab
            pass
        elif srb2org:  # TODO - implement srb2_org
            pass
        else:
            raise Exception("One flag must be set to true for get_latest_version_number()")
        self.latest_version = match
        return match

    def download_version(self, version="latest", system="windows", github=True, gitlab=False, srb2org=False):
        # TODO - use github only for downloading latest release.
        # TODO - use srb2.org for downloading historical releases
        # TODO - remove capability for downloading minor patch releases. To hard and pointless to maintain.
        # TODO - add code to utilize custom base directory (instead of ./SRB2)
        # "regex_version" is used to match the filename. "version" is used for github API.
        if version == "latest":
            regex_version = self.get_latest_version_number()
        else:
            regex_version = version
        # TODO - regex_version is unused.
        # Fuzzy search os_regex
        os_regex = {
            "windows": ".*Full.zip|.*Installer.exe",
            "macos": ".*.dmg",
            "linux": ".*.tar.gz"  # TODO - not sure if tar.gz is right, that's probably for source code
        }
        current_os_regex = [os_regex[key] for key in os_regex if system in key.lower()][0]
        version_path = self.create_version_dir(regex_version)

        url = None
        if github:
            url = self.get_github_download_url(current_os_regex, version)
        elif gitlab:  # TODO - gitlab
            url = self.get_gitlab_download_url(current_os_regex, regex_version)
        elif srb2org:  # TODO - srb2org
            url = self.get_srb2org_download_url(current_os_regex, regex_version)

        full_path = self.download_url_to_path(version_path, url)
        self.unzip_no_subdirs(full_path)
        return version_path

    def get_github_download_url(self, regex, version="latest"):
        self.set_github_response(version)
        # TODO - make the following code cleaner:
        release_urls = [item["browser_download_url"] for item in self.github_response.json()['assets']]
        release_matches = [re.findall(regex, item) or None for item in release_urls]
        release_match = list(filter(None, release_matches))[0][0]
        return release_match

    def get_gitlab_download_url(self, regex, version):  # TODO
        return

    def get_srb2org_download_url(self, regex, version):  # TODO
        return

    def get_github_api_url_from_version(self, version):  # TODO
        return ""

    def set_github_response(self, version="latest"):
        response = None
        if version == "latest":
            response = requests.get("https://api.github.com/repos/{}/releases/{}"
                                    .format(github_repo, version))
        else:
            response = requests.get("https://api.github.com/repos/{}/releases/SRB2_release_{}"
                                    .format(github_repo, version))
        self.github_response = response
        return response

    def download_url_to_path(self, path, url):
        parsed_url = urlparse(url)
        full_path = path + "/" + os.path.basename(parsed_url.path)
        print(full_path)
        urlretrieve(url, full_path)
        return full_path

    def unzip_no_subdirs(self, full_path):
        with zipfile.ZipFile(full_path, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(full_path))

    def get_version_dirs(self):
        """
        Gets a list of SRB2 directories for different versions
        :return:
        """
        base_dir = self.home_dir
        version_dirs = next(os.walk(base_dir))[1]
        return version_dirs

    def get_mod_subdirs(self, srb2_version):
        version_dir = "/" + srb2_version
        base_dir = self.home_dir + version_dir + self.mod_dir
        mod_subdirs = next(os.walk(base_dir))[1]
        return mod_subdirs

    def create_mod_subdir(self, mod_key, mod_list, srb2_version):
        version_dir = "/" + srb2_version
        mod_name = mod_key
        mod_subdir = "/" + self.slugify(mod_key)
        mod_url = mod_list[mod_key]
        mod_download_url = ''
        full_path = self.home_dir + version_dir + self.mod_dir + mod_subdir
        Path(full_path).mkdir(parents=True, exist_ok=True)

    def is_srb2_update(self, github=True, gitlab=False, srb2org=False):
        """
        Returns bool for whether SRB2 needs updated or not.
        Checks latest github version against version folder names.
        :param github:
        :param gitlab:
        :param srb2org:
        :return:
        """
        latest_version = self.get_latest_version_number(github=github,
                                                        gitlab=gitlab,
                                                        srb2org=srb2org)
        version_dirs = self.get_version_dirs()
        is_update = False
        if latest_version not in version_dirs:
            is_update = True
        return is_update

    def download_latest(self, system="windows"):
        self.download_version("latest", system=system)


def main():
    d = Downloader()
    #d.download_version("latest", "windows")
    d.download_version("2.2.8", "windows")
    if d.is_srb2_update():
        d.download_latest()


main()
