import re

SPACES = re.compile("\s+")
GLOBALS = re.compile("%g\d")
LINE_SPLIT = re.compile("\s+=\s+")
MAKE_ID = re.compile("(%mkID\d+)")
MAKE_ID_LB = re.compile("%mkIDlb(\d)")
MAKE_ID_W = re.compile("%mkIDW")
DOLLAR_TARGET = re.compile("($\d)+")


class MANFRED:
    word_matcher_regularization = "[\w\(\)\?\!]"
    word_matcher_plus_square_brkcts = "[\w\[\]\?\!]"

    @staticmethod
    def replacements():
        x = [
            ##########################################
            # Normalization Phase
            ##########################################

            # When a line ends with an unknown content
            ("(\[\s*\/)", "[?] /"),

            # WHen a line ends with a provided character and an unknown loss
            ("(\[("+MANFRED.word_matcher_regularization+"*)\s*\/)",
                "[$1] [?] /"),
            ("\[("+MANFRED.word_matcher_regularization+"+)\s*$",
                "[$1] [?]"),

            # When a line starts with an unknown content
            ('(\/\s*\])',
                '/ [?]'),

            # When a line starts with a provided character and an unknown content
            ('(\/\s*('+MANFRED.word_matcher_regularization+'*)\])',
                '/ [?] [$1]'),
            ('^(\s*('+MANFRED.word_matcher_regularization+'*)\])',
                '[?] [$1]'),

            # When two words are spanning inside the same provided lqcuna : [abc(ade!) abc(e)x(z!)]
            ('\[('+MANFRED.word_matcher_regularization+'+) ('+MANFRED.word_matcher_regularization+'+)\]',
                '[$1] [$2]'),

            # When three words are spanning inside the same provided lqcuna : [abc(ade!) abc(e)x(z!) abc(e)x(z!)]
            ('\[('+MANFRED.word_matcher_regularization+'+) ('+MANFRED.word_matcher_regularization+'+) ('+MANFRED.word_matcher_regularization+'+)\]',
                '[$1] [$2] [$3]'),

            # Replace angular bracket by curved bracked
            ("<", "«"),
            (">", "»"),

            ##########################################
            # Word and line tagging
            ##########################################

            # Tag a word
            ('([^\s/]+)',
                '<w n="%mkIDW">$1</w>'),
            # Tag multiple lines
            ('(\/{2})(?!\w\>)',
             '<lb n="%mkIDlb1"/><gap extend="unknown" reason="lost" units="line" />'),
            # Tag a line
            ('(\/)(?![\w\>]+)',
                '<lb n="%mkIDlb1"/>'),

            ##########################################
            # Angular bracket markup
            ##########################################

            # Correction
            ("«(\w+)=(\w+)»",
                "<choice><supplied>$1</supplied><sic>$2</sic></choice>"),

            # Here texts are listed that have been created to fill erased passages
            ("««([\w\(\)\?\!])»»",
                "<del>$1</del>"), # Not so sure about this one [Meaning of the legend]

            # Here text have been erased and something was filled by an ancient hand
            ("««\[\[([\w\(\)\?\!])\]\]»»}",
                "<add place=\"overstrike\">$1</add>"),

            ##########################################
            # Curly brackets
            ##########################################

            # Replace curly brackets
            ("\{((?:\w|\s)+)\}",
                "<sic>$1</sic>"),

            ##########################################
            # Parentheses in Brackets
            ##########################################

            # Abbreviation inside Parentheses, even with supplied inside
            ("\[("+MANFRED.word_matcher_plus_square_brkcts+"*)\((\w+)\)("+MANFRED.word_matcher_plus_square_brkcts+"*)\]",
                "<supplied reason=\"lost\"><expan><abbr>$1</abbr><ex>$2</ex><abbr>$3</abbr></expan></supplied>"),

            ##########################################
            # Parentheses
            ##########################################

            # Parentheses, even with supplied inside
            ("("+MANFRED.word_matcher_plus_square_brkcts+"*)\((\w+)\)("+MANFRED.word_matcher_plus_square_brkcts+"*)",
                "<expan><abbr>$1</abbr><ex>$2</ex><abbr>$3</abbr></expan>"),

            # Parentheses with uncertain
            ("("+MANFRED.word_matcher_plus_square_brkcts+"*)\((\w+)(?:(?:\?)|(?:\(\?\)))\)("+MANFRED.word_matcher_plus_square_brkcts+"*)",
                "<expan><abbr>$1</abbr><ex certain=\"low\">$2</ex><abbr>$3</abbr></expan>"),

            # Parentheses with unextended parentheses
            ("("+MANFRED.word_matcher_plus_square_brkcts+"*)\(\)("+MANFRED.word_matcher_plus_square_brkcts+"*)",
                "<expan><abbr>$1</abbr><abbr>$2</abbr></expan>"),

            ##########################################
            # Brackets
            ##########################################

            # When the loss' extent is unknown
            ("\[\?\]",
                '<gap reason="lost" extent="unknown" unit="character"/>'),

            # When the loss' extent is quantified
            ("\[(\d+)\]",
                '<gap reason="lost" extent="$1" unit="character"/>'),

            # When the loss' extent is quantified but unsure
            ("\[(\d+)\?\]",
                '<gap reason="lost" extent="$1" unit="character" certainty="low"/>'),
            ("\[(\d+)\(\?\)\]",
                '<gap reason="lost" extent="$1" unit="character" certainty="low"/>'),

            # When we supply an uncertain replacement
            ("\[(" + MANFRED.word_matcher_regularization + "+)\?\]",
             '<supplied reason="lost" certainty="low">$1</supplied>'),
            ("\[(" + MANFRED.word_matcher_regularization + "+)\(\?\)\]",
             '<supplied reason="lost" certainty="low">$1</supplied>'),
            ("(\w*)\[(" + MANFRED.word_matcher_regularization + "+)\](\w*)\(\?\)",
             '$1<supplied reason="lost" certainty="low">$2</supplied>$3'),

            # When we supply a replacement
            ("\[("+MANFRED.word_matcher_regularization+"+)\]",
                '<supplied reason="lost">$1</supplied>'),

            ##########################################
            # Clean Up
            ##########################################
            ("(<abbr></abbr>)", "")

        ]
        for pattern, replacement in x:
            yield re.compile(pattern), replacement


class Epigraph2Markup(object):
    def __init__(self, replacements=None):
        self.replacements = list(MANFRED.replacements())
        self.lineNum = 0
        self.wNum = 0
        self.id = 0
        self.ignoreLB = False

        if replacements is not None:
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
        return str(self.lineNum)

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

            result = pattern.sub(self.replace(replacement), result)

            lbs = []
            make_ids = [unit for match in MAKE_ID.findall(result) for unit in match.groups() if unit is not None]
            if debug is True:
                print(result)

        result = MAKE_ID_W.sub(self.w, result)
        result = MAKE_ID_LB.sub(self.lb, result)
        return result

if __name__ == "__main__":
    obj = Epigraph2Markup()
    x = obj.convert("Sittium a[e]d(ilem) [o(ro) v(os)] f(aciatis)", debug=False)
    print(x)
