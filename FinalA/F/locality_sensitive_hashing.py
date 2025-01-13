import numpy as np
import pandas as pd
import hashlib
import itertools
import time
import sys
from scipy.sparse import csr_matrix, csc_matrix, coo_matrix, lil_matrix
import argparse
def candidates(user_movie, h, b, seed):

    # sparse matrix
    movies_num = len(np.unique(user_movie[:, 1]))
    users_num = len(np.unique(user_movie[:, 0]))
    
    '''movies_num = int(np.max(user_movie[:, 1]))
    users_num = int(np.max(user_movie[:, 0]))'''

    sparse_matrix = coo_matrix((np.ones(len(user_movie)), (user_movie[:, 1] - 1, user_movie[:, 0] - 1)))
    sparse_matrix = sparse_matrix.tocsc()

    # signature matrix
    signature_matrix = np.full((h, users_num), np.inf)
    np.random.seed(seed)
    hash_permutations = np.array([np.random.permutation(movies_num) for _ in range(h)])
    rows, cols = sparse_matrix.nonzero()
    for i in range(h):
        permuted_rows = hash_permutations[i, rows]
        np.minimum.at(signature_matrix[i], cols, permuted_rows + 1)

    # print(signature_matrix)
    r = h // b

    # hash into bucket
    bucket_dict_list = []
    for b_ in range(b):
      bucket_dict = dict()
      for u in range(users_num):
        start = r*b_
        end = r*(b_+1)
        data = str(tuple(signature_matrix[start:end, u])).encode('utf-8')
        # bucket_id = hash(data)
        bucket_id = hashlib.sha256(data).hexdigest()
        if bucket_id not in bucket_dict.keys():
          bucket_dict[bucket_id] = [u+1]
        else:
          bucket_dict[bucket_id].append(u+1)
      bucket_dict_list.append(bucket_dict)


    # candidate pairs
    candidate_pairs = set()
    for bucket_dict in bucket_dict_list:
      for bucket_id, bucket in bucket_dict.items():
        if len(bucket) > 1 and len(bucket) < 20:
          candidate_pairs.update(itertools.combinations(bucket, 2))

    candidate_pairs = list(candidate_pairs)
    return candidate_pairs, signature_matrix, sparse_matrix


def calculate_similarity(candidate_pairs):
    pair_counts = []
    user_rated_movies = {user: user_movie[user_movie[:, 0] == user][:,1] for user in np.unique(user_movie[:, 0])}
    for candidates in candidate_pairs:
      pair_count = 0
      for candidate in candidates:
          C1 = user_rated_movies[candidate[0]]
          C2 = user_rated_movies[candidate[1]]
          jsim = len(np.intersect1d(C1, C2)) / len(np.union1d(C1, C2))
          if jsim > 0.5:
              pair_count += 1
      pair_counts.append(pair_count)
    return pair_counts



def calculate_jaccard_similarity(sparse_matrix, candidate_pairs):
    users = []
    for i, candidates in enumerate(candidate_pairs):
        pair_count = 0
        candidates = np.array(candidates)
        user1_indices = candidates[:, 0] - 1
        user2_indices = candidates[:, 1] - 1

        for user1, user2 in zip(user1_indices, user2_indices):
            C1 = sparse_matrix[:, user1]
            C2 = sparse_matrix[:, user2]
            intersection = C1.minimum(C2).sum()
            union = C1.maximum(C2).sum()
            jsim = intersection / union if union > 0 else 0


            if jsim > 0.5:
                pair_count += 1
                users.append((user1+1, user2+1))
    return pair_count, users


def calculate_signature_similarity(signature_matrices, candidate_pairs):
    pair_counts = []
    for signature_matrix, candidates in zip(signature_matrices, candidate_pairs):
        pair_count = 0

        candidates = np.array(candidates)
        user1_indices = candidates[:, 0] - 1
        user2_indices = candidates[:, 1] - 1

        C1 = signature_matrix[:, user1_indices]
        C2 = signature_matrix[:, user2_indices]

        agree_matrix = C1 == C2
        agree_counts = np.sum(agree_matrix, axis=0)
        total_rows = signature_matrix.shape[0]

        jsim_values = agree_counts / total_rows

        for jsim in jsim_values:
            if jsim > 0.5:
                pair_count += 1
        pair_counts.append(pair_count)
    return pair_counts


'''def calculate_signature_similarity(signature_matrices, candidate_pairs):
    pair_counts = []
    for signature_matrix, candidates in zip(signature_matrices, candidate_pairs):
        pair_count = 0
        for candidate in candidates:
            user1, user2 = candidate
            C1 = signature_matrix[:, user1 - 1]
            C2 = signature_matrix[:, user2 - 1]
            agree_rows = np.sum(C1 == C2)
            total_rows = signature_matrix.shape[0]
            jsim = agree_rows/total_rows
            if jsim > 0.5:

                pair_count += 1
        pair_counts.append(pair_count)
    return pair_counts'''



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LSH")
    parser.add_argument("--seed", default=2024, type=int)
    args = parser.parse_args()
    seed = args.seed
    start_time = time.time()

    user_movie = np.load("user_movie_rating.npy")
    
    # candidate b
    bs = [30] #, 30, 40, 50
    hs = [150] # 80,
    num_candidates = []
    candidate_pairs = []
    signature_matrices = []
    labels = []


    for h in hs:
        for b in bs:
            candidate_pair, signature_matrix, sparse_matrix = candidates(user_movie, h=h, b=b, seed=seed)
            num_candidates.append(len(candidate_pair))
            candidate_pairs.append(candidate_pair)
            signature_matrices.append(signature_matrix)


    pair_count, users = calculate_jaccard_similarity(sparse_matrix, candidate_pairs)
    
    with open("user_pairs.txt", "w") as f:
        for u1, u2 in users:
            f.write(f"{u1},{u2}\n")
    
    end_time = time.time()
    total_time = (end_time - start_time) / 60

    print(f"Execution time: {total_time:.2f} minutes")
    print(f"Number of user pairs with Jaccard similarity > 0.5: {pair_count}")
    
    '''pair_count = calculate_similarity(candidate_pairs)
    print(pair_count)'''
    '''pair_count = calculate_signature_similarity(signature_matrices, candidate_pairs)
    print(pair_count)'''

