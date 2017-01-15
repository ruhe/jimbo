import copy
import json
import logging
import os

import yaml

log = logging.getLogger(__name__)


class Config(object):
    def __init__(self):
        self._repositories = []

    def init(self, config_path):
        defaults_local = Config._load_defaults("local")
        defaults_remote = Config._load_defaults("remote")
        defaults_virtual = Config._load_defaults("virtual")

        config = Config._read_config_file(config_path)
        self._read_config_group(config, "local", defaults_local)
        self._read_config_group(config, "remote", defaults_remote)
        self._read_config_group(config, "virtual", defaults_virtual)

    def get_repositories(self):
        return self._repositories

    def _read_config_group(self, config, group_name, defaults):
        for repo in config[group_name]:
            log.info("Reading configuration for {0} "
                     "repository {1}".format(group_name, repo["key"]))

            repo_config = copy.copy(defaults)
            for k, v in repo.items():
                repo_config[k] = v

            self._repositories.append(repo_config)

    @staticmethod
    def _read_config_file(path):
        log.info("Reading config file from {0}".format(path))
        with open(path, 'r') as f:
            return yaml.load(f)

    @staticmethod
    def _load_defaults(repository_type):
        dirname = os.path.dirname(__file__)
        path = os.path.join(dirname,
                            "defaults/{0}.json".format(repository_type))

        log.info("Reading '{0}' defaults from {1}".format(repository_type,
                                                          path))
        with open(path, "r") as f:
            return json.load(f)
