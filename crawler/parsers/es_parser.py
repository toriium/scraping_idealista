from crawler.parsers.abs_parser import ABCParser


class IdealistaESParser(ABCParser):


    @staticmethod
    def get_kitchen_and_furnished(text) -> tuple[bool | None, bool | None]:
        if 'Amueblado y cocina equipada' in text:
            kitchen = True
            furnished = True
        elif 'Cocina equipada y casa sin amueblar' in text:
            kitchen = True
            furnished = False
        elif 'Cocina no equipada y casa sin amueblar' in text:
            kitchen = False
            furnished = False
        else:
            kitchen = None
            furnished = None
        return kitchen, furnished
