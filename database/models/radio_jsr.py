from logger import print_message


class Radio_JSR():
    def __init__(self, id, song_name, link, station,game_title):
        self.id:str = id
        self.song_name:str = song_name
        self.song_link:str= link
        self.station:str = station
        self.game_title:str = game_title

def list_tuple_to_radio_jsr_list(list: list[tuple]) -> list[Radio_JSR]:
    result_list = []
    for radio_jsr in list:
        try:
            result_list.append(Radio_JSR(radio_jsr[0],radio_jsr[1],radio_jsr[2],radio_jsr[3], radio_jsr[4]))
        except:
            print_message('The list is not in the correct format')
            return []
    
    return result_list