import logging
import threading

import requests


class AbnormalReport:

    # 一般错误
    GENERAL_ERROR = 1_016_001
    # 严重错误
    SERIOUS_ERROR = 1_016_002
    # 致命错误
    FATAL_ERROR = 1_016_003

    def __init__(self, project_name, env_flag, url=None, timeout=15):
        self._project_name = project_name
        self._env_flag = env_flag
        self._url = url
        self._timeout = timeout

    def get_url(self):
        if callable(self._url):
            return self._url()
        return self._url

    def _send(self, cid, title, content):
        try:
            response = requests.post(
                self.get_url(), json={"cid": cid, "title": title, "content": content}, timeout=self._timeout
            )
            if not response.status_code == requests.codes.ok:
                logging.error("report exception failed. response: {}".format(response.text))
            else:
                logging.info("report exception success. response: {}".format(response.text))

        except Exception as e:
            logging.error("report exception failed. error: {}".format(e))

    def report(self, title, content, cid=GENERAL_ERROR):
        # 如果配置了 url ，就上报
        if self.get_url():
            title = "{flag}-{project_name}:{title}".format(
                flag=self._env_flag, project_name=self._project_name, title=title
            )
            threading.Thread(target=self._send, args=(cid, title, content)).start()
