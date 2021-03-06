import fastText # for sentence embeddings
import numpy as np
from utils import Configuration
logger = Configuration.get_logger()

class ContentUtil:

    def __init__(self, path='../data/songs.bin.bin', matrix_path=None): 
        self.model_ft = fastText.load_model(path)
        self.model_path = path
        self.matrix_math = matrix_path
        if matrix_path:
            logger.info(f'matrix path is None, budiling index')
            self.create_index(matrix_path)

    def find_nearest_neighbor(self, sentence, ban_set=[], cossims=None):
        """
        query is a 1d numpy array corresponding to the vector to which you want to
        find the closest vector
        vectors is a 2d numpy array corresponding to the vectors you want to consider
        cossims is a 1d numpy array of size len(vectors), which can be passed for efficiency
        returns the index of the closest match to query within vectors

        """
        query = self.model_ft.get_sentence_vector(sentence)
        if cossims is None:
            cossims = np.matmul(self.vectors, query, out=cossims)
        else:
            np.matmul(self.vectors, query, out=cossims)
        rank = len(cossims) - 1
        result_i = np.argpartition(cossims, rank)[rank]
        while result_i in ban_set:
            rank -= 1
            result_i = np.argpartition(cossims, rank)[rank]
        return result_i, cossims[result_i]

    def encode_songs(self, songs_file='./all_songs.txt'):
        vectors = []
        k = 0
        with open(songs_file, 'r', encoding='UTF-8') as file:
            for line in file.readlines():
                vectors.append(self.normalize(self.model_ft.get_sentence_vector(line.strip())))
                print(k)
        print(len(vectors))
        vector_matrix = np.asmatrix(vectors)
        np.save("vector_matrix.npy", vector_matrix)

    def encode_query(self, topic):
        return self.model_ft.get_sentence_vector(topic)

    def create_index(self, matrix):
        import faiss  # for similarity search
        normed_matrix = np.load(matrix)
        self.index = faiss.IndexFlatIP(normed_matrix.shape[1])
        self.index.add(normed_matrix)

    def normalize(self, x):
        return x / np.linalg.norm(x)

    def get_songs(self, query, n=5):
        """
        Get similarity scores and indices for n closest songs to query
        P.S
        ids for songs currently start from 0, need to account for that
        :param query: processed query from user
        :param n: number of required NN
        :return: tuple of arrays (indices, similarity)
        """
        query_encoded = self.normalize(self.encode_query(query))
        D, I = self.index.search(query_encoded.reshape(1, query_encoded.shape[0]), n)
        return I, D

    def add_song(self, song):
        """
        Index new song for retrieval. Has to be preprocessed
        :param song: str
        """
        song_encoded = self.normalize(self.encode_query(song))
        self.index.add(song_encoded.reshape(1, song_encoded.shape[0]))

    def train_embeddings(self, path_to_songs):
        """
        Train fastText embeddings based on input file
        :param path_to_songs:
        :return:
        """
        self.model_ft = fastText.train_unsupervised(
            input=path_to_songs,
            model='skipgram',
        )
        self.model_ft.save_model(self.model_path+'1.bin')


if __name__ == '__main__':
    util = ContentUtil(matrix_path='../data/vector_matrix.npy')
    #util.encode_songs()
    print(util.get_songs('love'))
    print(util.index.ntotal)
    util.add_song('tru tutu tra la la nastia bababa')
    print(util.index.ntotal)
    print(util.get_songs('tru tutu tra la la'))
    util.train_embeddings('./all_songs.txt')

"""
Example of output
(array([[206161, 221387, 152593,  64153, 199581]]), array([[0.61498034, 0.5754149 , 0.5745163 , 0.5721062 , 0.57194483]],
      dtype=float32))
"""