__author__ = 'dstogsdill'
"""Class for interacting with Panorama"""

import pan.xapi
import sys
import xmltodict


class Panorama:

    def __init__(self, hostname, username, password, DEBUG=False):
        self.DEBUG = DEBUG
        self.xpaths = self._get_xpaths()
        self.api = self._login(hostname, username, password)
        self.address_types = ['ip-netmask', 'ip-range', 'fqdn']
        self.shared_address = None
        self.shared_addressgroups = None

    @staticmethod
    def _get_xpaths():
        xpaths = {}
        xpaths['shared'] = {}
        xpaths['shared']['addressobjects'] = "/config/shared/address"
        xpaths['shared']['addressgroups'] = "/config/shared/address-group"
        return xpaths

    @staticmethod
    def _login(hostname, username, password):
        """
        :param hostname: Panorama hostname or IP
        :param username: username to login to Panorama
        :param password: password to login to Panorama
        :return: API Client
        """
        try:
            pan_api = pan.xapi.PanXapi(
                api_username=username,
                api_password=password,
                hostname=hostname
            )
            return pan_api
        except pan.xapi.PanXapiError as msg:
            print('pan.xapi.PanXapi:', msg)
            sys.exit(1)

    def get_config_by_xpath(self, xpath):
        """
        :param xpath: The configuration URI path
        :return: Dictionary formatted configuration
        """
        try:
            self.api.get(xpath=xpath)
            result = self.api.xml_result()
            if result:
                return xmltodict.parse(result)
            else:
                return None
        except pan.xapi.PanXapiError as msg:
            print('pan.xapi.PanXapi:', msg)
            sys.exit(1)

    def add_shared_addressgroup(self, groupname, addresses):
        """
        Creates an address group in the Shared context
        :param groupname:
        :param addresses:  A list of addresses to add to the group
        :return:
        """
        if not isinstance(addresses, list):
            if self.DEBUG:
                print("Addresses must be a list")
            sys.exit(1)

        # Get existing address groups and validate the new group name does not exist
        if not self.shared_address:
            self.shared_addressgroups = self.get_config_by_xpath(self.xpaths['shared']['addressgroups'])
            for groups in self.shared_addressgroups['address-group']['entry']:
                if groupname == groups['@name']:
                    if self.DEBUG:
                        print("Group already exists: ", groupname)
                    return

        # Create the group
        xpath = self.xpaths['shared']['addressgroups'] + "/entry[@name='%s']" % groupname
        element = '<static>'
        for address in addresses:
            element = element + '<member>%s</member>' % address
        element = element + '</static>'
        try:
            self.api.set(xpath=xpath, element=element)
            if self.DEBUG:
                print("Group created: ", groupname)
        except pan.xapi.PanXapiError as msg:
            print('pan.xapi.PanXapi:', msg)

    def add_shared_address(self, addressname, address_type, address):
        """
        Create an address object
        :param name: Address object name
        :param address_type: ip-netmask, ip-range, fqdn
        :param address: ip address, range or fqdn
        :return:
        """
        if address_type not in self.address_types:
            if self.DEBUG:
                print("Invalid address type: ", address_type)
            return

        if not self.shared_address:
            self.shared_address = self.get_config_by_xpath(self.xpaths['shared']['addressobjects'])

        # validate if the object already exists
        for item in self.shared_address['address']['entry']:
            if addressname == item['@name']:
                if self.DEBUG:
                    print("Address already exists: ", addressname)
                return

        # Create the address object
        xpath = self.xpaths['shared']['addressobjects'] + "/entry[@name='%s']" % addressname
        element = "<%s>%s</%s>" % (address_type, address, address_type)
        try:
            self.api.set(xpath=xpath, element=element)
            if self.DEBUG:
                print('Created Address Object: ', addressname)
        except pan.xapi.PanXapiError as msg:
            print('pan.xapi.PanXapi:', msg)
