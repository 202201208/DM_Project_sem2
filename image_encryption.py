import hashlib
import math
from PIL import Image


def get_matrix(im, plane):
  image = []
  width = im.shape[0]
  height = im.shape[1]
  for i in range(width):
    row = []
    for j in range(height):
      try:
        row.append(im.item(i, j, plane))
      except:
        row = [im.item(i, j, plane)]
    try:
      image.append(row)
    except:
      image = [row]

  return image

def assign_matrix_image(img, mat2, mat1, mat):
  for i in range(len(mat)):
    for j in range(len(mat[i])):
      img[j, i] = (mat[i][j], mat1[i][j], mat2[i][j])
  
  return img



def toDecimal(binary):
    decimal = 0
    for bit in binary:
        decimal = decimal * 2 + bit
    return decimal

def toBinary(n):
  counter=8
  bitseq=[]
  while(True):
      q=n/2
      r=n%2
      n=q
      counter = counter-1
      try:
        bitseq.append(int(r))
      except:
        bitseq = [r]
      if(counter<=0):
        break
  try:
    bitseq.reverse()
  except:
    bitseq= []

  return bitseq


def renyi_seq(x, a, b, alpha, n):
  arr = []
  xn = x
  for i in range(n):
    f = math.tan(x)*(1+x)*b + (1-x)*x*a
    xn , temp = math.modf(f)
    xn = int(xn * alpha)
    x = xn
    try:
      arr.append(f) 
    except:
      arr = [f]

  return arr


def renyi_key_img(rs, mat):
  kmat = []
  x = 0
  for i in range(len(mat)):
    row = []
    for j in range(len(mat[i])):
      try:
        row.append(int(rs[x]%256))
      except:
        row = [int(rs[x]%256)]
      x = x + 1

    try:
      kmat.append(row)
    except:
      kmat = [row]
  
  return kmat

def tent_seq(x, r, n):
  xn = x
  arr = []
  for i in range(n):
    xn = min(x, 1-x) * r
    x = xn
    try:
      arr.append(xn)
    except:
      arr = [xn]

  return arr


Rule = [
  ["A", "G", "C", "T"],
  ["A", "C", "G", "T"],
  ["G", "A", "T", "C"],
  ["C", "A", "T", "G"],
  ["G", "T", "A", "C"],
  ["C", "T", "A", "G"],
  ["T", "G", "C", "A"],
  ["T", "C", "G", "A"]
]

Rule_reverse = [
  {"A":0, "G":1, "C":2, "T":3},
  {"A":0, "C":1, "G":2, "T":3},
  {"G":0, "A":1, "T":2, "C":3},
  {"C":0, "A":1, "T":2, "G":3},
  {"G":0, "T":1, "A":2, "C":3},
  {"C":0, "T":1, "A":2, "G":3},
  {"T":0, "G":1, "C":2, "A":3},
  {"T":0, "C":1, "G":2, "A":3}
]

def dna_code_to_map(st, rule):
  num = []
  for i in range(4):
    for j in range(4):
      if(Rule[rule][j] == st[i]):
        try:
          num.append(j)
        except:
          num = [j]
  
  return num

def map_to_dna_code(num, rule):
  st = ""
  for i in range(4):
    st = st + Rule[rule][num[i]]
  return st

def dna_oper_encode(s1, s2, oper, rule):
  n1 = dna_code_to_map(s1, rule)  
  n2 = dna_code_to_map(s2, rule)  
  n3 = []
  for i in range(4):
    if(oper == 0):
      a = (n1[i]+n2[i])%4
    elif(oper == 1):
      a = (n1[i]-n2[i])%4
    else:
      a = n1[i] ^ n2[i]
    try:
      n3.append(a)
    except:
      n3 = [a]
  s3 = map_to_dna_code(n3, rule)
  return s3

def dna_oper_decode(s1, s2, oper, rule):
  n1 = dna_code_to_map(s1, rule)  
  n2 = dna_code_to_map(s2, rule)  
  n3 = []
  for i in range(4):
    if(oper == 0):
      a = (n1[i]-n2[i])%4
    elif(oper == 1):
      a = (n1[i]+n2[i])%4
    else:
      a = n1[i] ^ n2[i]
    try:
      n3.append(a)
    except:
      n3 = [a]
  s3 = map_to_dna_code(n3, rule)
  return s3

def int_to_dna_code(l, rule):
  a = toBinary(l)
  st = ""
  for i in range(0, 8, 2):
    if(a[i]==0 and a[i+1]==0):
      st = st + Rule[rule][0]
    elif(a[i]==0 and a[i+1]==1):
      st = st + Rule[rule][1]
    elif(a[i]==1 and a[i+1]==0):
      st = st + Rule[rule][2]
    else:
      st = st + Rule[rule][3]

  return st

def dna_code_to_int(s, rule):
  b = []
  for i in range(4):
    a = Rule_reverse[rule][s[i]]
    if(a == 0):
      try:
        b.append(0)
        b.append(0)
      except:
        b = [0]
        b = [0]
    elif(a==1):
      try:
        b.append(0)
        b.append(1)
      except:
        b = [0]
        b = [1]
    elif(a==2):
      try:
        b.append(1)
        b.append(0)
      except:
        b = [1]
        b = [0]
    else:
      try:
        b.append(1)
        b.append(1)
      except:
        b = [1]
        b = [1]
  a = toDecimal(b)
  return a

def encode_dna_mat(mat, tr):
  emat = []
  x = 0
  for i in range(len(mat)):
    row = []
    
    for j in range(len(mat[0])):
      rule = int(tr[x]*x)%8
      st = int_to_dna_code(mat[i][j], rule)
      try:
        row.append(st)
      except:
        row = []
      x = x + 1
    try:
      emat.append(row)
    except:
      emat = [row]
  
  return emat

def decode_dna_mat(mat, tr):
  emat = []
  x = 0
  for i in range(len(mat)):
    row = []
    
    for j in range(len(mat[0])):
      rule = int(tr[x]*x)%8
      n = dna_code_to_int(mat[i][j], rule)
      try:
        row.append(n)
      except:
        row = []
      x = x + 1
    try:
      emat.append(row)
    except:
      emat = [row]
  
  return emat

def dna_opers_encode(mat, mat1, ts):
  omat = []
  x = 0
  for i in range(len(mat)):
    row = []
    rule = int(ts[x]*x)%8
    oper = int(ts[x]*x)%3
    for j in range(len(mat[i])):
      val = dna_oper_encode(mat[i][j], mat1[i][j], oper, rule)
      try:
        row.append(val)
      except:
        row = [val]
    x = x + 1 
    try:
      omat.append(row)
    except:
      row = [omat]
  
  return omat

def dna_opers_decode(mat, mat1, ts):
  omat = []
  x = 0
  for i in range(len(mat)):
    row = []
    rule = int(ts[x]*x)%8
    oper = int(ts[x]*x)%3
    for j in range(len(mat[i])):
      val = dna_oper_decode(mat[i][j], mat1[i][j], oper, rule)
      try:
        row.append(val)
      except:
        row = [val]
    x = x + 1 
    try:
      omat.append(row)
    except:
      row = [omat]
  
  return omat

def get_initial_values(hash):
  strings = [(hash[i:i+8]) for i in range(0, len(hash), 8)]
  values = []
  for i in range(len(strings)):
    s = strings[i]
    xor = 0
    sum = 0
    for j in range(len(s)):
      xor = xor ^ (ord(s[j]) * j)
      sum = sum + ord(s[j])

    val = (xor + sum) / 8192
    try:
      values.append(val)
    except:
      values = [val]
  
  values.append((values[0] + values[4] + values[7])/3)
  return values

def encrypt_image(im, target_file_name, key):
  hash = hashlib.sha256(key.encode())
  hash = hash.hexdigest()
  print(hash)
  v = get_initial_values(hash)
  mat = get_matrix(im, 0)
  rs = renyi_seq(v[0], (v[2]+v[4])*10, (v[5]+v[6])*10, (v[1]+v[7])*12345, len(mat)*len(mat[0]))
  ts_r = (v[6] + 1.4)
  if(ts_r - 2 > 0):
    ts_r = ts_r - 2
  ts = tent_seq(v[3], ts_r, len(mat)*len(mat[0]))
  key_img = renyi_key_img(rs, mat)
  encoded_key_image = encode_dna_mat(key_img, ts)
  encoded_img = encode_dna_mat(mat, ts)
  output_img = dna_opers_encode(encoded_img, encoded_key_image, ts)
  decoded_output_img = decode_dna_mat(output_img, ts)

  mat = get_matrix(im, 1)
  rs = renyi_seq(v[1], (v[0]+v[6])*10, (v[2]+v[4])*10, (v[3]+v[5])*12345, len(mat)*len(mat[0]))
  ts_r = (v[5] + 1.4)
  if(ts_r - 2 > 0):
    ts_r = ts_r - 2
  ts = tent_seq(v[7], ts_r, len(mat)*len(mat[0]))
  key_img = renyi_key_img(rs, mat)
  encoded_key_image = encode_dna_mat(key_img, ts)
  encoded_img = encode_dna_mat(mat, ts)
  output_img = dna_opers_encode(encoded_img, encoded_key_image, ts)
  decoded_output_img1 = decode_dna_mat(output_img, ts)

  mat = get_matrix(im, 2)
  rs = renyi_seq(v[2], (v[3]+v[5])*10, (v[1]+v[7])*10, (v[0]+v[4])*12345, len(mat)*len(mat[0]))
  ts_r = (v[4] + 1.4)
  if(ts_r - 2 > 0):
    ts_r = ts_r - 2
  ts = tent_seq(v[8], ts_r, len(mat)*len(mat[0]))
  key_img = renyi_key_img(rs, mat)
  encoded_key_image = encode_dna_mat(key_img, ts)
  encoded_img = encode_dna_mat(mat, ts)
  output_img = dna_opers_encode(encoded_img, encoded_key_image, ts)
  decoded_output_img2 = decode_dna_mat(output_img, ts)

  img = Image.new("RGB", (im.shape[1], im.shape[0]))
  pix = img.load()
  pix = assign_matrix_image(pix, decoded_output_img, decoded_output_img1, decoded_output_img2)
  img.save(target_file_name, "BMP")

def decrypt_image(im, target_file_name, key):
  hash = hashlib.sha256(key.encode())
  hash = hash.hexdigest()
  print(hash)
  v = get_initial_values(hash)
  print(v)
  mat = get_matrix(im, 0)
  rs = renyi_seq(v[0], (v[2]+v[4])*10, (v[5]+v[6])*10, (v[1]+v[7])*12345, len(mat)*len(mat[0]))
  ts_r = (v[6] + 1.4)
  if(ts_r - 2 > 0):
    ts_r = ts_r - 2
  ts = tent_seq(v[3], ts_r, len(mat)*len(mat[0]))
  key_img = renyi_key_img(rs, mat)
  encode_img = encode_dna_mat(mat, ts)
  encoded_key_image = encode_dna_mat(key_img, ts)
  output_img = dna_opers_decode(encode_img, encoded_key_image, ts)
  decoded_output_img = decode_dna_mat(output_img, ts)

  mat = get_matrix(im, 1)
  rs = renyi_seq(v[1], (v[0]+v[6])*10, (v[2]+v[4])*10, (v[3]+v[5])*12345, len(mat)*len(mat[0]))
  ts_r = (v[5] + 1.4)
  if(ts_r - 2 > 0):
    ts_r = ts_r - 2
  ts = tent_seq(v[7], ts_r, len(mat)*len(mat[0]))
  key_img = renyi_key_img(rs, mat)
  encode_img = encode_dna_mat(mat, ts)
  encoded_key_image = encode_dna_mat(key_img, ts)
  output_img = dna_opers_decode(encode_img, encoded_key_image, ts)
  decoded_output_img1 = decode_dna_mat(output_img, ts)

  mat = get_matrix(im, 2)
  rs = renyi_seq(v[2], (v[3]+v[5])*10, (v[1]+v[7])*10, (v[0]+v[4])*12345, len(mat)*len(mat[0]))
  ts_r = (v[4] + 1.4)
  if(ts_r - 2 > 0):
    ts_r = ts_r - 2
  ts = tent_seq(v[8], ts_r, len(mat)*len(mat[0]))
  key_img = renyi_key_img(rs, mat)
  encode_img = encode_dna_mat(mat, ts)
  encoded_key_image = encode_dna_mat(key_img, ts)
  output_img = dna_opers_decode(encode_img, encoded_key_image, ts)
  decoded_output_img2 = decode_dna_mat(output_img, ts)

  img = Image.new("RGB", (im.shape[1], im.shape[0]))
  pix = img.load()
  pix = assign_matrix_image(pix, decoded_output_img, decoded_output_img1, decoded_output_img2)
  img.save(target_file_name, "BMP")
