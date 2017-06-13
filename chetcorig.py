import re

SPACES = re.compile("\s+")
GLOBALS = re.compile("%g\d")
LINE_SPLIT = re.compile("\s+=\s+")
MAKE_ID = re.compile("(%mkID\d+)")
MAKE_ID_LB = re.compile("lb n=\"%mkID(\d)\"")
MAKE_ID_W = re.compile("%mkIDW")
DOLLAR_TARGET = re.compile("($\d)+")


class Epigraph2Markup(object):
    def __init__(self, replacements):
        self.replacements = []
        self.lineNum = 0
        self.wNum = 0
        self.id = 0
        self.ignoreLB = False

        for line in replacements.split("\n"):
            if not line.startswith("#") and "=" in line:
                pattern, replacement = tuple(LINE_SPLIT.split(line, maxsplit=1))
                pattern, replacement = pattern.strip(), replacement.strip()
                if replacement == "null":
                    replacement = ""
                self.replacements.append((re.compile(pattern), replacement))

    def reset(self):
        self.lineNum = 0
        self.id = 0
        self.wNum = 0

    def count(self, text, find):
        """ Count the number of match of find in text or the length of characters of find

        :param text:
        :param find:
        :return:
        """
        if text == find:
            return len(SPACES.sub("", text))
        else:
            return text.count(find)

    def lb(self, match):
        self.lineNum += 1
        return "lb n=\"{}\"".format(str(self.lineNum))

    def w(self, match):
        self.wNum += 1
        return str(self.wNum)

    def replace(self, replacement_string):
        def temp(sub_output):
            output = ""+replacement_string
            groups = sub_output.groups()
            for i in range(len(groups)):
                output = output.replace("$"+str(i+1), groups[i] or "")
            return output
        return temp

    def convert(self, text, debug=False):
        result = "" + text
        for pattern, replacement in self.replacements:  # For each replacement

            if "%g" in replacement:  # If we have a replacement variable in replacement
                for match in pattern.findall(result):
                    print(match)
            else:
                result = pattern.sub(self.replace(replacement), result)

            result = MAKE_ID_W.sub(self.w, result)
            result = MAKE_ID_LB.sub(self.lb, result)

            lbs = []
            make_ids = [unit for match in MAKE_ID.findall(result) for unit in match.groups() if unit is not None]
            if debug is True:
                print(result)

        return result

if __name__ == "__main__":
    with open("replacements.txt") as f:
        replacements = f.read()
    obj = Epigraph2Markup(replacements)
    x = obj.convert("Sittium a[e]d(ilem) [o(ro) v(os)] f(aciatis)", debug=True)
    print(x)