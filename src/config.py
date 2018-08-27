

import pytoml as toml

from defines import *
import os

class Config:

    def __init__(self, filename):
        """
        self.filename is the toml file for start
        """
        if not os.path.isfile(filename):
            print("Bad config file")

        abspath = os.path.abspath(filename)
        
        self.filename = os.path.basename(abspath)
        self.path = os.path.dirname(abspath)
        self.tomls = dict()
        self.toml_files = []
        self.toml_config = None
        self.status = ConfigState_Init
        

    def load(self):
        self.__parse_start_toml_files()


    def __parse_start_toml_files(self):

        path = os.path.dirname(os.path.abspath(self.filename))
        
        self.__parse_toml_files([self.filename])
        print(self.tomls)
        self.status = ConfigState_Parsed

        self.toml_config = self.__load_toml_files()
        print(self.toml_config)
        self.status = ConfigState_Loaded

    #
    def __parse_toml_files(self, toml_files):
        """
        Parse the toml files, especially against the 'requires'
        """
        for toml_file in toml_files:
            toml_file_path = os.path.join(self.path, toml_file)
            if toml_file_path in self.tomls:
                # Prevent loop require
                continue

            with open(toml_file_path, 'rb') as file:
                # tomls hold all the configs parsed from toml file.
                toml_config = toml.load(file)
                self.toml_files.append(toml_file_path)
                self.tomls[toml_file_path] = toml_config
                print(toml_config)
                if Requires in toml_config:
                    toml_files = toml_config[Requires]
                    self.__parse_toml_files(toml_files)

    def __load_toml_files(self):
        """

        """
        result = dict()
        for filename in self.toml_files:
            config = self.tomls[filename]
            self.__merge_dict(result, config)
        return result

    @staticmethod
    def __merge_dict(d1, d2):
        """
        Merge d2 into d1
        """
        for key, value in d2.items():
            if key == '__filename__':
                continue
            if key not in d1:
                d1[key] = value
            else:
                d1[key].update(value)

    def get_value(self, key):
        key_parts = key.split(".")
        return Config.__get_value(self.toml_config, key_parts)

    @staticmethod
    def __get_value(config_dict, key_parts):
        config = config_dict
        for key_part in key_parts:
            config = config[key_part]
        return config


    def __load_resources(self):
        pass

    def __load_resources(self):
        pass        



