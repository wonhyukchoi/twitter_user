from utils import json_files_to_list
from datetime import datetime
from matplotlib import pyplot as plt


class FbMessageAnalyzer:
    def __init__(self):
        self._messages = []
        self._sender_messages = {}
        self._senders = set()
        self._time = []

    def load_from_dir(self, path: str, sender='sender_name',
                      content='content', time='timestamp_ms') -> None:
        self._messages = json_files_to_list(path=path)
        self._parse_messages(sender=sender, content=content)
        self._parse_time(time=time)

    def count_by_person(self) -> dict:
        return {sender: len(messages) for sender, messages
                in self._sender_messages}

    def time_series(self, timestamp_div=1000) -> list:
        datetime_list = []
        for timestamp in self._time:
            timestamp = timestamp / timestamp_div
            datetime_list += datetime.fromtimestamp(timestamp)
        return datetime_list

    def _parse_messages(self, sender='sender_name',
                        content='content') -> None:
        for msg in self._messages:
            if content in msg.keys():
                self._sender_messages.\
                    setdefault(msg[sender], []).append(msg[content])
            else:
                self._sender_messages.\
                    setdefault(msg[sender], []).append('<other>')
        self._senders = set(self._sender_messages.keys())

    def _parse_time(self, time='timestamp_ms'):
        for msg in self._messages:
            self._time += msg[time]


if __name__ == "__main__":
    import os
    json_path = os.path.join(os.getcwd(), 'data')

    analyzer = FbMessageAnalyzer()
    analyzer.load_from_dir(path=json_path)
