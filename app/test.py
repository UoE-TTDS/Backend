from dataset import DatasetApi
d = DatasetApi()
print(list(k['name'] for k in d.get_songs_by_id([1,2,0])))