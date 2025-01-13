# No external libraries are allowed to be imported in this file
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import multiprocessing
import random
from scipy.sparse import csr_matrix, csc_matrix


"""The u.data dataset contains the ranking assigned by the users 
of a streaming platform to the movies available on the platform."""
# Importing dataset: paste your path to u.data in the following line:
path = "u.data"       
df = pd.read_table(path, sep="\t", names=["UserID", "MovieID", "Rating", "Timestamp"])
df = np.array(df)

num_movies = len(np.unique(df[:,1]))
# print(num_movies)
# print(np.random.permutation(num_movies).shape)
unique_users = len(np.unique(df[:,0]))
# value, row, column
sparse_matrix = csr_matrix((np.ones(len(df)), (df[:,1], df[:,0])))
# print(sparse_matrix)
sig_mat = np.array(range(unique_users))

index = np.random.permutation(num_movies) 
# print(sparse_matrix[index,:])
sparse_matrixcsc = sparse_matrix[index,:].tocsc()
print(sparse_matrixcsc.indptr[:-1])  

first_nonzero_row = sparse_matrixcsc.indices[sparse_matrixcsc.indptr[:-1]]
print(first_nonzero_row)
sig_mat = np.vstack((sig_mat, first_nonzero_row[1:]))




# print(df.head())  # to check the correct import of the dataset
# df = df.pivot_table(index = 'UserID', columns = 'MovieID', values = 'Rating')


def similarity_matrix(matrix, k=5, axis=0):
    """
    This function should contain the code to compute the cosine similarity (according to the
    formula seen in the lecture) between users (axis=0) or items (axis=1) and return a dictionary 
    where each key represents a user (or item) and the value is a list of the top k most similar
    users or items, along with their similarity scores.
    
    Args:
        matrix (pd.DataFrame) : user-item rating matrix (df)
        k (int): number of top k similarity rankings to return for each entity (default=5)
        axis (int): 0: calculate similarity scores between users (rows of the matrix), 
                    1: calculate similarity scores between items (columns of the matrix)
    
    Returns:
        similarity_dict (dictionary): dictionary where the keys are users (or items) and 
        the values are lists of tuples containing the most similar users (or items) along 
        with their similarity scores.

    Note that is NOT allowed to automatically compute cosine similarity using an existing 
    function from any package, the computation should follow the formula that has been
    discussed during the lecture and that can be found in the slides.

    Note that it is allowed to convert the DataFrame into a Numpy array for faster computation.
    """

'''    similarity_dict= {}
    # TO DO: Handle the absence of ratings (missing values in the matrix)
    matrix = np.nan_to_num(np.array(matrix))
    m, n = matrix.shape
    # TO DO: If axis is 1, what do you need to do to calculate the similarity between 
    # items (columns)
    
    if axis==1:
        dis_matrix = np.zeros(shape=(n, n))
    # TO DO: loop through each couple of entities to calculate their cosine similarity 
    # and store these results
        for i in range(n):
            for j in range(n):
                a = matrix[:, i].reshape(1, -1)
                b = matrix[:, j].reshape(1, -1)
                dis_matrix[i, j] = cosine_similarity(a, b)[0][0]
    else:
        dis_matrix = np.zeros(shape=(m, m))
        for i in range(m):
            for j in range(m):
                a = matrix[i].reshape(1, -1)
                b = matrix[j].reshape(1, -1)
                dis_matrix[i, j] = cosine_similarity(a, b)[0][0]
                # print(dis_matrix[i, j])
    # TO DO: sort the similarity scores for each entity and add the top k most similar 
    # entities to the similarity_dict
    for i, m in enumerate(dis_matrix):
        value = []
        k_list = m.argsort()[-(k+1):][::-1]
        for l in k_list:
            if l != i:
                value.append((l, m[l]))
        similarity_dict[i] = value
    return similarity_dict

user_similarity_matrix = similarity_matrix(df, k=5, axis=0)
print(user_similarity_matrix.get(3,[]))
item_similarity_matrix = similarity_matrix(df, k=3, axis=1)
print(item_similarity_matrix.get(10,[]))'''

'''U = np.random.normal(size=(5, 3))
print(U)
u_index = list(np.ndindex(U.shape))
print(np.ndindex(U.shape))
print(u_index)'''

'''data_train = df[['UserID', 'MovieID', 'Rating']].to_numpy()
print(data_train)
U = np.random.normal(size=(5, 3))
print(list(np.ndindex(U.shape)))'''