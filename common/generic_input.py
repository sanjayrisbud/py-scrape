# Type that will accept user input.

from framework.type import Type


class GenericInput(Type):

    def __init__(self):
        super().__init__()

        self.shortText1 = self.add_field("string")
        self.shortText2 = self.add_field("string")
        self.shortText3 = self.add_field("string")
        self.shortText4 = self.add_field("string")
        self.longText1 = self.add_field("text")
        self.longText2 = self.add_field("text")
        self.integer1 = self.add_field("integer")
        self.integer2 = self.add_field("integer")
        self.number1 = self.add_field("number")
        self.number2 = self.add_field("number")
        self.date = self.add_field("datetime")


