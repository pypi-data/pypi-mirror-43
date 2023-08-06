from abc import ABCMeta, abstractmethod
import os

class Interface(object):
    """Abstract class for filessytem objects"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def open(self, uuid, mode, file_hash=None, **kwargs):
        """
        Open a file like object

        :param self: self reference
        :param uuid: internal id of file reference
        :param mode: Mode to open file
        :param file_hash: hash of file contents for locating using CAS lookup
        :param kwargs: Options list to pass to underlying storage layer
        :type uuid: string
        :type file_hash: string
        :type mode: string
        :type kwargs: dict
        :raises ResourceNotFound: If the file could not be found
        :returns: An object implemeting a file like interface
        :rtype: File

        """

    @abstractmethod
    def remove_file(self, uuid, file_hash=None):
        """
        :param self: self reference
        :param uuid: internal id of file reference
        :param file_hash: hash of file contents for locating using CAS lookup
        :type uuid: string
        :type file_hash: string
        :returns: A boolean indicating status of the file removal
        :rtype: boolean
        """

    @abstractmethod
    def is_signed_url(self):
        """
        Return boolean if signed url is possible for this file type

        :param self: self reference
        :returns boolean:
        """

    @abstractmethod
    def get_signed_url(self, uuid, purpose, filename, attachment=True, response_type=None, file_hash=None):
        """
        Returns the signed url location of the file reference

        :param self: self reference
        :param string uuid: internal file uuid reference
        :param string purpose: stated reason for signed url: upload or download
        :param string filename: Name of the downloaded file, used in the content-disposition header
        :param boolean attachment: True/False, attachment or not
        :param string response_type: Content-Type header of the response
        :param string file_hash: hash of file contents for locating using CAS lookup
        :raises ResourceNotFound: If the file could not be found
        :return: string, the signed url string for accessing the referenced file
        :rtype: string

        """

    @abstractmethod
    def get_file_hash(self, uuid, file_path=None):
        """
        Returns the calculated hash for the current contents of the referenced file

        :param self: self reference
        :param string uuid: internal file uuid reference
        :param string file_path: path of file contents for locating using legacy CAS lookup
        :raises ResourceNotFound: If the file could not be found
        :returns: The hash value of the curreent file contents
        :rtype: string
        """

    @abstractmethod
    def get_file_info(self, uuid, file_hash=None):
        """
        Returns basic file info about the referenced file object, None if the file does not exist

        :param self: self reference
        :param string uuid: internal fild uuid reference
        :param string file_hash: hash of file contents for locating using CAS lookup
        :returns: Dict of file information with the following data attributes
            {
                'filesize': int,
            }
        :rtype: Dict | None

        """

    @abstractmethod
    def path_from_uuid(self, uuid):
        """
        create a filepath from a UUID
        filepath is determined by the storage plugin

        :param self: self reference
        :param string uudi: internal file uuid reference
        :returns: The internal filepath for resouce within this storage plugin
        :rtype: string

        e.g. for pyfs
        uuid_ = cbb33a87-6754-4dfd-abd3-7466d4463ebc
        will return
        cb/b3/cbb33a87-6754-4dfd-abd3-7466d4463ebc
        """
    @abstractmethod
    def path_from_hash(self, hash_):
        """
        create a filepath from a hash
        e.g.
        hash_ = v0-sha384-01b395a1cbc0f218
        will return
        v0/sha384/01/b3/v0-sha384-01b395a1cbc0f218
        """

    def format_hash(self, hash_alg, hash_):
        """
        format the hash including version and algorithm
        """
        return '-'.join(('v0', hash_alg, hash_))
