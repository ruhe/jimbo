import logging

import requests

log = logging.getLogger(__name__)


class ArtifactoryClient(object):
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    def get_repositories(self):
        query = "{0}/api/{1}".format(self.url, 'repositories')

        resp = self._send_request(query)
        return sorted([r['key'] for r in resp.json()])

    def get_repository(self, repo_name):
        query = "{0}/api/{1}/{2}".format(self.url, 'repositories', repo_name)

        resp = self._send_request(query)
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 400:
            return None
        else:
            raise

    def create_repository(self, repo_name, repo_config):
        query = "{0}/api/{1}/{2}".format(self.url, 'repositories', repo_name)

        resp = self._send_request(query, method='put', json=repo_config)
        log.info(resp.content)

    def update_repository(self, repo_name, repo_config):
        query = "{0}/api/{1}/{2}".format(self.url, 'repositories', repo_name)

        resp = self._send_request(query, method='post', json=repo_config)
        log.info(resp.content)

    def create_or_update_repository(self, repo_name, repo_config):
        orig_repo = self.get_repository(repo_name)

        if orig_repo:
            self._compare_and_update(orig_repo, repo_name, repo_config)
        else:
            self.create_repository(repo_name, repo_config)

    def _compare_and_update(self, orig_repo, repo_name, repo_config):
        should_update = False

        for k, v in repo_config.items():
            if orig_repo[k] != v:
                data = {"repository": repo_name, "key": k,
                        "old_val": orig_repo[k], "new_val": v}
                log.info(
                    "{repository}: {key} will be updated from "
                    "\"{old_val}\" to \"{new_val}\" ".format(**data))
                should_update = True

        if should_update:
            self.update_repository(repo_name, repo_config)
        else:
            log.info("{0}: nothing to update. Skipping.".format(repo_name))

    def delete_repository(self, repo):
        query = "{0}/api/{1}/{2}".format(self.url, 'repositories', repo)

        resp = self._send_request(query, method='delete')
        log.info(resp.content)

    def _send_request(self, query, method='get', json=None):
        auth = (self.username, self.password)
        headers = {'Content-type': 'application/json'}

        log.info("Sending {0} request to {1}".format(method.upper(), query))

        if json:
            resp = requests.request(method, query, auth=auth,
                                    headers=headers, json=json)
        else:
            resp = requests.request(method, query, auth=auth, headers=headers)

        log.info(
            "Received response. status_code = {0}".format(resp.status_code))

        return resp
