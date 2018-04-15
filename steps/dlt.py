import numpy as np
from utils.timer import timer

def estimate_homography(first, second):
    M = []

    for j in range(0, int(int(first.size) / 2)):
        homogeneous_first = np.array([
            first[j][0],
            first[j][1],
            1
        ])

        homogeneous_second = np.array([
            second[j][0],
            second[j][1],
            1
        ])

        pr_1 = homogeneous_first
        pr_2 = homogeneous_second

        M.append(np.array([
            pr_1.item(0), pr_1.item(1), 1,
            0, 0, 0,
            -pr_1.item(0)*pr_2.item(0), -pr_1.item(1)*pr_2.item(0), -pr_2.item(0)
        ]))

        M.append(np.array([
            0, 0, 0, pr_1.item(0), pr_1.item(1),
            1, -pr_1.item(0)*pr_2.item(1), -pr_1.item(1)*pr_2.item(1), -pr_2.item(1)
        ]))

    U, S, Vh = np.linalg.svd(np.array(M).reshape((84, 9)))
    idx = list(filter(lambda i: S[i] == min(S), range(0, len(S))))[0]
    L = Vh[idx]

    H = L.reshape(3, 3)
    return H

def compute_homography(data):
    end = timer()
    real = data['real']
    es = []

    for i in range(0, len(data['sensed'])):
        sensed = data['sensed'][i]
        estimated = estimate_homography(real, sensed)
        es.append(estimated)
        end = timer()

    end("compute_homography")
    return np.array(es)
