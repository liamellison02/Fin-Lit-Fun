from collections import defaultdict


class Tagger(object):
    def __init__(self):
        self._tagMap = defaultdict(list)

    def __call__(self, tag):
        if tag not in self._tagMap:
            self._tagMap[tag] = []

        def tag_decorator(method):
            self._tagMap[tag].append(method)
            method._tag = tag
            return method

        return tag_decorator


tag = Tagger()
