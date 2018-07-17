import re

class Formatter(object):

    def __init__(self, printer, notification):
        self.printer = printer
        self.notification = notification

    def __format__(self, format):
        pattern = r'([a-zA-Z_]+)\(([a-zA-Z_]+)\)'
        matches = re.match(pattern, format)
        if not matches:
            return format

        if not hasattr(self.printer, matches.group(1)):
            raise Exception('Unknown method "%s" in format "%s"' % (matches.group(1), format))

        method = getattr(self.printer, matches.group(1))
        key = matches.group(2)

        if key not in self.notification:
            raise Exception('Unknown attribute "%s" in notification "%s"' % (key, repr(self.notification)))

        arg = self.notification[key]

        return method(arg)
