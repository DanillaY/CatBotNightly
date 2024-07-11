class Streamer:
    def __init__(self, id:str, query:str, stream_link:str, start_stream:str):
        #take id variable from api call
        self.id:str = id
        self.query:str = query
        self.stream_link:str= stream_link
        self.start_stream:str = start_stream

def list_tuple_to_streamer_list(list: list[tuple]) -> list:
    result_list = []
    for streamer in list:
        try:
            result_list.append(Streamer(streamer[0],streamer[1],streamer[2],streamer[3]))
        except:
            return []
    return result_list