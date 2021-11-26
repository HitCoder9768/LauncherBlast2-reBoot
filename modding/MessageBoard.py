from lxml import html
import requests

class MessageBoard:
    """
    Class containing methods for querying the SRB2 Message Board.
    Do not put any methods for downloading content in here, put them in Downloader.py
    :var self.mb_link: contains the base URL for the mb
    """

    def __init__(self):
        self.mb_link = "https://mb.srb2.org"
        self.maps_sublink = self.mb_link + "/addons/categories/maps.4/"
        self.characters_sublink = self.mb_link + "/addons/categories/characters.5/"
        self.lua_sublink = self.mb_link + "/addons/categories/lua.7/"
        self.misc_sublink = self.mb_link + "/addons/categories/miscellaneous.8/"
        self.assets_sublink = self.mb_link + "/addons/categories/assets.6/"
        # Oh so sneaky:
        self.headers = {'User-Agent':
                            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/39.0.2171.95 Safari/537.36'}

        # Store request responses for mods, so we don't have to repeat requests:
        self.maps = []
        self.lua = []
        self.misc = []
        self.assets = []
        self.characters = []

    def get_maps(self):
        self.maps = self.get_mods(self.maps_sublink)
        return self.maps

    def get_lua(self):
        self.lua = self.get_mods(self.lua_sublink)
        return self.lua

    def get_characters(self):
        self.characters = self.get_mods(self.characters_sublink)
        return self.characters

    def get_misc(self):
        self.misc = self.get_mods(self.misc_sublink)
        return self.misc

    def get_assets(self):
        self.assets = self.get_mods(self.assets_sublink)
        return self.assets

    def get_mods(self, addons_subforum_url):
        """
        Gets a list of all mods from addons subforum URL
        :param url: The URL of the SRB2 MB sub-forum to search
        :return: Returns a list containing Mod class instances
        """
        last_page = False
        mod_list = []
        mod_links = []
        mod_names = []
        page_counter = 1
        previous_data = None
        # Iterate through pages grabbing thread names and their links:
        while not last_page:
            tree = self.get_addons_page_html(addons_subforum_url, page_counter)
            current_mod_links = self.get_list_of_thread_links(tree)
            current_mod_names = self.get_list_of_thread_names(tree)
            if current_mod_names == previous_data:
                # This works because if you go past the real number of pages,
                #   the MB will send you back to the last valid page,
                #   making you get the same data twice
                last_page = True
            else:
                mod_names.extend(current_mod_names)
                mod_links.extend(current_mod_links)
            previous_data = current_mod_names
            page_counter += 1

        # Make our list of mods
        for index in range(len(mod_names)):
            mod = Mod(mod_names[index])
            mod.thread_url = mod_links[index]
            mod_list.append(mod)

        return mod_list

    def get_addons_page_html(self, url, page_num):
        """
        SRB2 MB is broken up into subforums that sometimes have multiple pages.
        This function returns the html tree for a specified page.
        :param url: The base url for the subforum, not including the specific page.
        :param page_num: The page number as an integer
        :return: HTML tree: the results of html.parse(requests.get(url))
        """
        response = requests.get(url + "?page={}".format(str(page_num)),
                                stream=True,
                                headers=self.headers)
        response.raw.decode_content = True
        return html.parse(response.raw)

    def get_mod_download_url(self, mod_thread_name, mod_list):
        mod_download_url = None
        for mod in mod_list:
            if mod.name == mod_thread_name:
                mod_download_url = mod.set_download_url()
        return mod_download_url

    def get_list_of_thread_names(self, parsed_html):
        """
        Get list of all thread names from a page on the MB
        :param request_response: The results of html.parse(response.raw)
        :return: List containing all thread names on the page
        """
        return parsed_html.xpath('.//div[@class="structItem-title"]/*[@data-tp-primary="on"]/text()')

    def get_list_of_thread_links(self, parsed_html):
        return parsed_html.xpath('.//div[@class="structItem-title"]/*[@data-tp-primary="on"]/@href')

    def get_mod_description(self):
        pass

    def get_mod_version(self):
        pass

    def get_mod_srb2_version(self):
        pass

    def get_github_versions(self):
        pass

    def get_gitlab_versions(self):
        pass

    def get_history_list(self):
        pass


class Mod:
    def __init__(self, name, thread_url=None, description=None, download_url=None):
        self.name = name
        self.thread_url = thread_url
        self.description = description
        self.download_url = download_url

    def set_download_url(self, mb_link="https://mb.srb2.org"):
        if not self.thread_url:
            return None
        self.download_url = mb_link + self.thread_url + "download"
        return self.download_url


def main():
    mb = MessageBoard()
    mb.get_maps()
    print(mb.get_mod_download_url("The Confused Maps [Addon for BattleMod]", mb.maps))
    pass

main()