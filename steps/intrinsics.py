import numpy as np
import math

def cal_v(i, j, H):
    v = np.array([
        H[0, i] * H[0, j],
        H[0, i] * H[1, j] + H[1, i] * H[0, j],
        H[1, i] * H[1, j],
        H[2, i] * H[0, j] + H[0, i] * H[2, j],
        H[2, i] * H[1, j] + H[1, i] * H[2, j],
        H[2, i] * H[2, j]
    ])
    return v


def get_camera_intrinsics(homographies):

    h_count = len(homographies)

    vec = []

    for i in range(0, h_count):
        curr = np.reshape(homographies[i], (3, 3))

        vec.append(cal_v(0, 1, curr))
        vec.append(cal_v(0, 0, curr) - cal_v(1, 1, curr))

    vec = np.array(vec)

    ss, vv, dd = np.linalg.svd(np.dot(np.transpose(vec), vec))
    idx = list(filter(lambda i: vv[i] == min(vv), range(0, len(vv))))[0]
    #x = np.compress(vv < 1e-1, dd, axis=0)
    x = dd[idx]
    print(x)

    B = np.zeros([4, 4], dtype=np.float32)
    B[1, 1] = x[0]
    B[1, 2] = x[1]
    B[2, 2] = x[2]
    B[1, 3] = x[3]
    B[2, 3] = x[4]
    B[3, 3] = x[5]

    cy = (B[1, 2] * B[1, 3] - B[1, 1] * B[2, 3]) / (B[1, 1] * B[2, 2] - B[1, 2] * B[1, 2])
    lamb = B[3, 3] - (B[1, 3] * B[1, 3] + cy * (B[1, 2] * B[1, 3] - B[1, 1] * B[2, 3])) / B[1, 1]
    ax = math.sqrt(float(lamb / B[1, 1]))
    #print(ax)
    print((lamb * B[1, 1] / (B[1, 1] * B[2, 2] - B[1, 2] * B[1, 2])))
    ay = math.sqrt(float(lamb * B[1, 1] / (B[1, 1] * B[2, 2] - B[1, 2] * B[1, 2])))

    s = -B[1, 2] * ax * ax * ay / lamb
    cx = s * cy / ay - B[1, 3] * ax * ax / lamb
    # 相机矩阵求解结果
    K = np.zeros([3, 3], dtype=np.float32)
    K[0, 0] = ax
    K[0, 1] = s
    K[0, 2] = cx
    K[1, 1] = ay
    K[1, 2] = cy
    K[2, 2] = 1

    return  K
