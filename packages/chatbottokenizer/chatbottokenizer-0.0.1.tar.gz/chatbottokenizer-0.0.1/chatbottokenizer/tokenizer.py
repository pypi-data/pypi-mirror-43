class Tokenizer:
    DELIMITER = ' '

    last_tmpl = ''

    def __init__(self, name: str, inp: str):
        self.tokens = inp.split(self.DELIMITER)
        self.name = name

    def to_bot(self) -> bool:
        """
        If the bot name is the first word, then return True
        """
        return self.tokens[0] == self.name

    def _split(self, inp: str) -> list:
        """
        Custom splitter that puts the name of the bot before all other strings
        """
        return [self.name] + inp.split(self.DELIMITER)

    def match(self, tmpl: str) -> bool:
        self.last_tmpl = tmpl
        items = self._split(tmpl)
        if len(self.tokens) < len(items):
            return False
        items = self._non_variables(tmpl)
        return items == self.tokens[:len(items)]

    def _non_variables(self, items_str: str) -> list:
        """
        Gets target string without variables attached.
        Example:
        '!test start <name>' becomes '[!test, start]'
        """
        items = self._split(items_str)
        items = [i for i in items if len(i) > 0]
        items = ['' if i.startswith('<') else i for i in items]
        items = self._remove_last_blanks(items)
        return items

    def _remove_last_blanks(self, items: list) -> str:
        """
        Not going to lie, I don't know why this is here
        """
        for i, item in enumerate(items[::-1]):
            if item != '':
                return items[::-1][i:][::-1]

    def items(self) -> dict:
        template = self._split(self.last_tmpl)
        non_vars = self._non_variables(self.last_tmpl)

        var = template[len(non_vars):]
        var = [i[1:len(i) - 1] for i in var]
        args = self.tokens[len(non_vars):]
        # Case when last argument should be combined
        if len(args) > len(var):
            n = len(args) - len(var)
            last_msg = args[len(args) - n - 1:]
            last_msg = [' '.join(last_msg)]
            args = args[:len(args) - n - 1] + last_msg
        return {n: a for n, a in zip(var, args)}
