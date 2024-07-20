from logger import print_message


class Radio:
    def __init__(self, id, title, country):
        self.id:str = id
        self.title:str = title
        self.country:str= country

def list_tuple_to_radio_list(list: list[tuple]) -> list[Radio]:
    result_list = []
    for radio in list:
        try:
            result_list.append(Radio(radio[0],radio[1],radio[2]))
        except:
            print_message(message='The list is not in the correct format',error='format error',came_from='Radio_Class')
            return []
    return result_list