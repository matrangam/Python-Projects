class Rule:
    """
    Base class for all rules.
    """
    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)
        return True

class HeadingRule(Rule):
    """
    A heading is a single line with no more than 70 characters
    and does not end in a colon.
    """

    type = 'heading'
    def condition(self, block):
        return not '\n' in block and len(block) <= 70 and not block[-1] ==':'

    
class TitleRule(HeadingRule):
    """
    the title is the first block in the document, provided that
    it is a heading...
    """

    type = 'title'
    first = True

    def condition(self, block):
        if not self.first: return False
        self.first = False
        return HeadingRule.condition(self, block)

    
class ListItemRule(Rule):
    """
    A list item is a paragraph that begind with a hyphen.
    the hyphen is replaced by a bullet point!
    """

    type = 'listen'
    def condition(self, block):
        return block[0] == '-'
    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block[1:].strip())
        handler.end(self.type)
        return True

class ListRule(ListItemRule):
    """
    A list begins within a block that is not a list item and
    a subsequent list item.  It ends after the last consecutive
    list item.
    """

    type = 'list'
    inside = False
    def condition(self, block):
        return True
    def action(self, block, handler):
        if not self.inside and ListItemRule.condition(self, block):
            handler.start(self.type)
            self.inside = True
        elif self.inside and not ListItemRule.condition(self, block):
            handler.end(self.type)
            self.inside = False
        return False

class ParagraphRule(Rule):
    """
    A paragraph is a block that does not fall in to any other rules
    """

    type = 'paragraph'
    def condition(self, block):
        return True
    
