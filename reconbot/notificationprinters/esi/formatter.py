import re

class Formatter(object):

    def __init__(self, printer, notification):
        self.printer = printer
        self.notification = notification

    def __format__(self, format):
        pattern = r'([a-zA-Z_]+)\(([a-zA-Z_]+)(?:\s*,\s*([a-zA-Z_]+))?\)'
        matches = re.match(pattern, format)
        if not matches:
            return format
        groups = matches.groups()

        if not hasattr(self.printer, groups[0]):
            raise Exception('Unknown method "%s" in format "%s"' % (matches.group(1), format))

        method = getattr(self.printer, groups[0])

        keys = list(filter(lambda k: k is not None, groups[1:]))

        for key in keys:
            if key not in self.notification:
                raise Exception('Unknown attribute "%s" in notification "%s"' % (key, repr(self.notification)))

        args = list(map(lambda key: self.notification[key], keys))

        return method(*args)
