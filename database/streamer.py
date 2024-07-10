class Streamer:
    def __init__(self, id, query, streamer_link, start_stream):
        #take id variable from api call
        self.id:str = id
        self.query:str = query
        self.streamer_link:str= streamer_link
        self.start_stream:str = start_stream

def list_tuple_to_streamer_list(list: list[tuple]) -> list:
    result_list = []
    for streamer in list:
        try:
            result_list.append(Streamer(streamer[0],streamer[1],streamer[2],streamer[3]))
        except:
            return []
    return result_list