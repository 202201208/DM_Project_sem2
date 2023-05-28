import math
import cv2
import numpy as np

BITS = 2

HIGH_BITS = 256 - (1 << BITS)
LOW_BITS = (1 << BITS) - 1
BYTES_PER_BYTE = math.ceil(8 / BITS)
FLAG = '%'


def encode_image(img_path, msg, path, filename):
    img = cv2.imread(img_path, cv2.IMREAD_ANYCOLOR)
    ori_shape = img.shape
    print(ori_shape)
    max_bytes = ori_shape[0] * ori_shape[1] // BYTES_PER_BYTE
    msg = '{}{}{}'.format(len(msg), FLAG, msg)
    assert max_bytes >= len(
        msg), "Message greater than capacity:{}".format(max_bytes)
    data = np.reshape(img, -1)
    for (idx, val) in enumerate(msg):
        encode(data[idx*BYTES_PER_BYTE: (idx+1) * BYTES_PER_BYTE], val)

    img = np.reshape(data, ori_shape)
    filename = filename.split('.')[0]
    path += filename + '.png'
    cv2.imwrite(path, img)
    return filename+'.png'

def encode(block, data):
    data = ord(data)
    for idx in range(len(block)):
        block[idx] &= HIGH_BITS
        block[idx] |= (data >> (BITS * idx)) & LOW_BITS

def decode_image(path):
    img = cv2.imread(path, cv2.IMREAD_ANYCOLOR)
    data = np.reshape(img, -1)
    total = data.shape[0]
    res = ''
    idx = 0
    # Decode message length
    while idx < total // BYTES_PER_BYTE:
        ch = decode(data[idx*BYTES_PER_BYTE: (idx+1)*BYTES_PER_BYTE])
        idx += 1
        if ch == FLAG:
            break
        res += ch
    end = int(res) + idx
    assert end <= total // BYTES_PER_BYTE, "Input image isn't correct."

    secret = ''
    while idx < end:
        secret += decode(data[idx*BYTES_PER_BYTE: (idx+1)*BYTES_PER_BYTE])
        idx += 1
    return secret

def decode(block):
    val = 0
    for idx in range(len(block)):
        val |= (block[idx] & LOW_BITS) << (idx * BITS)
    return chr(val)