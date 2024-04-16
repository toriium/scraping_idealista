from crawler.parsers.abs_parser import ABCParser


class IdealistaPTParser(ABCParser):

    @staticmethod
    def get_kitchen_and_furnished(text) -> tuple[bool | None, bool | None]:
        if 'Mobilado e cozinha equipada' in text:
            kitchen = True
            furnished = True
        elif 'Cozinha equipada e casa sem mobília' in text:
            kitchen = True
            furnished = False
        elif 'Cozinha não equipada e casa sem mobília' in text:
            kitchen = False
            furnished = False
        else:
            kitchen = None
            furnished = None
        return kitchen, furnished
