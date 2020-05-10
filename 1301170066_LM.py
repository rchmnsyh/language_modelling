#import library
import numpy as np
import math
import pandas as pd
import re
from collections import Counter
import os




def buildUnigramModel(Text):
    '''
    BUILD UNIGRAM MODEL
    IS : Diberikan input sebuah data berisi text
    FS : Meng-outputkan hasil dari model unigram yang dibuat dalam bentuk dictionary (key: kata; value: probabilitas kemunculan kata tersebut)
    Note : Lakukan proses cleaning dengan menghapus punctuation dan mengubah teks menjadi lower case.
    '''
    kata = []
    for i in Text:
        # lower case setiap kata
        i = i.strip().lower()
        # pisah kata
        kata += re.split(r'\W+', i)
        
    # jadiin dictionary buat kata sama jumlah kemunculannya
    count = dict(Counter(kata))
    total = len(kata)
    
    prob = {}

    for key, value in count.items():
        # masukin kata sama probabilitasnya ke dictionary baru
        prob[key] = value / total 
    return prob
   

def buildBigramModel(Text):
    '''
    BUILD BIGRAM MODEL
    IS : Diberikan input sebuah data berisi text
    FS : Meng-outputkan hasil dari model bigram yang dibuat dalam bentuk dictionary (key: pasangan kata; value: probabilitas kemunculan pasangan kata tersebut)
    Note : Lakukan proses cleaning dengan menghapus punctuation dan mengubah teks menjadi lower case.
    '''
    kalimat, kata = [], []

    for i in Text:
        # split per kalimat
        kalimat += re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<!vs.)(?<=\.|\?)\s", i)

    for i in range (len(kalimat)):
        # lower case setiap kata
        kalimat[i] = kalimat[i].strip().lower()
        # pemisahan per kata sekalian tambah token
        kata += ['<s>'] + re.split(r'\W+', kalimat[i]) + ['</s>']

    # hapus isi kosong
    kata = [x for x in kata if x != '']
    kata_unigram = kata.copy()

    # bikin kamus buat unigram
    count_unigram = dict(Counter(kata_unigram))

    # jadiin bigram
    bigram = [(kata[i], kata[i+1]) for i in range(len(kata)-1)]
    
    # hapus bigram yang isi bigramnya dua-duanya token
    bigram.remove(('</s>', '<s>'))

    # dictionary buat bigram dan jumlah kemunculannya
    count_bigram = dict(Counter(bigram))

    prob = {}
    for key, value in count_bigram.items():
        # masukin bigram sama probabilitasnya ke dictionary baru
        prob[key] = value / count_unigram[key[0]]
    return prob



def nextBestWord(bigramModel, currentWord):
    '''
    MENAMPILKAN NEXT BEST WORD
    IS : Menerima input sebuah kata
    FS : Meng-outputkan kata berikutnya yang memiliki probabilitas tertinggi berdasarkan model bigram
    '''
    prob = []
    for key, value in bigramModel.items():
        # kalau kata nya sama, masukin list
        if key[0] == currentWord:
            prob.append((key[1], value))
    # sort by kemungkinan munculnya
    prob = sorted(prob, key=lambda x: x[1], reverse=True)
    # return nomor 1
    return prob[0]
   


def nextTenBestWords(bigramModel, currentWord):
    '''
    MENYIMPAN TOP 10 NEXT BEST WORD
    IS : Menerima input sebuah kata
    FS : Menghasilkan list berisi 10 kata berikutnya (beserta probabilitasnya) dengan probabilitas tertinggi berdasarkan model bigram. 
    '''
    prob = []
    for key, value in bigramModel.items():
        # kalau kata nya sama, masukin list
        if key[0] == currentWord:
            prob.append((key[1], value))
    # sort by kemungkinan munculnya
    prob = sorted(prob, key=lambda x: x[1], reverse=True)
    # return 10 teratas
    return prob[:10]
    


def generateSentence(bigramModel, length):
    '''
    GENERATE SENTENCE
    IS : Menerima input model bigram dan panjang kalimat yang ingin di-generate
    FS : Mengembalikan kalimat dengan panjang sesuai inputan
    Note : Generate sentence
    '''
    threshold = 0.3
    current = "<s>"
    sentence = ""
    for i in range (length):
        if np.random.uniform(0,1) < threshold:
            current = nextBestWord(bigramModel, current)[0]
            sentence += current + " "
        else:
            top10 = nextTenBestWords(bigramModel, current)
            current = top10[np.random.randint(0,len(top10))][0]
            sentence += current + " "
    return sentence


if __name__ == '__main__':
    print("TUGAS LANGUAGE MODELING NLP - SFY")
    print("SILAKAN MASUKKAN IDENTITAS ANDA")
    Nama = input("NAMA : ")
    NIM = input("NIM : ")

    os.system("pause")
    os.system("cls")

    #import dataset
    data = pd.read_csv('text.csv')

    print("TUGAS 1. TAMPILKAN 5 BARIS PERTAMA DARI DATASET")
    print()
    print("HASIL : ")
    print(data.head())

    os.system("pause")
    os.system("cls")

    print("TUGAS 2. BUAT MODEL UNIGRAM")
    print()
    print("HASIL : ")
    print(buildUnigramModel(data['text']))

    os.system("pause")
    os.system("cls")

    print("TUGAS 3. BUAT MODEL BIGRAM")
    print()
    print("HASIL : ")
    bigramModel = buildBigramModel(data['text'])
    print(bigramModel)    

    os.system("pause")
    os.system("cls")

    print("TUGAS 4. MENAMPILKAN NEXT BEST WORD")
    print()
    print("HASIL : ")
    print("of -> ",nextBestWord(bigramModel,"of"))
    print("update -> ",nextBestWord(bigramModel,"update"))
    print("hopes -> ",nextBestWord(bigramModel,"hopes"))

    os.system("pause")
    os.system("cls")

    print("TUGAS 5. TOP 10 BEST NEXT WORD")
    print()
    print("HASIL : ")
    print("of -> ",nextTenBestWords(bigramModel,"of"))
    print("update -> ",nextTenBestWords(bigramModel,"update"))
    print("hopes -> ",nextTenBestWords(bigramModel,"hopes"))

    os.system("pause")
    os.system("cls")

    print("TUGAS 6. GENERATE KALIMAT")
    print()
    n = int(input("Panjang Kalimat : "))
    print("HASIL : ")
    print(generateSentence(bigramModel, n))

    os.system("pause")
    os.system("cls")

    print("SELAMAT", Nama ,"ANDA SUDAH MENYELESAIKAN TUGAS LANGUAGE MODELING NLP-SFY")