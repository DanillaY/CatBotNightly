from logger import print_message


class Radio:
    def __init__(self, id, title, country):
        self.id:str = id
        self.title:str = title
        self.country:str= country

def list_tuple_to_radio_list(list: list[tuple]) -> list:
    result_list = []
    for streamer in list:
        try:
            result_list.append(Radio(streamer[0],streamer[1],streamer[2]))
        except:
            print('The list is not in the correct format')
            return []
    return result_list