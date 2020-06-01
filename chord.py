import numpy as np
import matplotlib.pyplot as plt
import wave


def generate_sine(sr, freq, t): # 正弦波
    x = np.zeros(sr//80)
    for i in range(len(x)):
      x[i] = np.sin(2*np.pi*i/len(x)*(freq/10))*10
    plt.figure(t+1)
    plt.plot(x)
    return x


def save_to_file(fname,rate,y):
    f = wave.open(fname, 'wb')
    f.setnchannels(1)   # 声道
    f.setsampwidth(2)   # 采样宽度
    f.setframerate(rate)
    f.writeframes(y.astype(np.short).tostring())
    f.close()
    

def KS(b, N, sr, alpha=0.99, REF_LEN=50, start_t=0):
    M = len(b)
    y = np.zeros(start_t*sr//2) # 1拍0.5秒
    y = np.append(y,b)
    beta = alpha ** (M / REF_LEN)
    # alpha越大，REF_LEN越大，衰减越慢
    beta2 = beta
    
    while len(y) < N:    
        y = np.append(y, beta2*b)
        beta2 *= beta
             
    return y[0:N]*1000


def freq(note): # 一些我不会的求音阶频率的乐理知识
    # general purpose function to convert a note  in standard notation 
    #  to corresponding frequency
    if len(note) < 2 or len(note) > 3 or \
        note[0] < 'A' or note[0] > 'G':
        return 0
    if len(note) == 3:
        if note[1] == 'b':
            acc = -1
        elif note[1] == '#':
            acc = 1
        else:
            return 0
        octave = int(note[2])
    else:
        acc = 0
        octave = int(note[1])
    SEMITONES = {'A': 0, 'B': 2, 'C': -9, 'D': -7, 'E': -5, 'F': -4, 'G': -2}
    n = 12 * (octave - 4) + SEMITONES[note[0]] + acc
    f = 440 * (2 ** (float(n) / 12.0))
    #print note, f
    return f


def ks_chord(chord, N, sr, start_t=0, alpha=0.995):
    y = np.zeros(N)
    for note, power in chord.items():
        # create an initial random-filled KS buffer the note
        x = generate_sine(sr, freq(note), start_t) # 每个音阶不一样
        y = y + power * KS(x, N, sr, alpha, start_t=start_t)
    return y  


if __name__ == '__main__':
    sr = 16000 # 设置采样频率，16Khz
    time = 4 # 持续时间4秒

    hdn_chord = {   # 音阶和响度
    'D2' : 2.2, 
    'D3' : 3.0, 
    'F3' : 1.0, 
    'G3' : 3.2, 
    'F4' : 1.0, 
    'A4' : 1.0, 
    'C5' : 1.0, 
    'G5' : 3.5,
    }

    y = ks_chord(hdn_chord, sr*time, sr)
    save_to_file('xx.wav',sr,y)
    
    plt.figure(2)
    plt.plot(y)
    plt.show()
