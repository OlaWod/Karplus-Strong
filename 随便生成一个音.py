import numpy as np
import matplotlib.pyplot as plt
import wave


def save_to_file(fname,rate,y): # 保存
    f = wave.open(fname, 'wb')
    f.setnchannels(1)   # 声道
    f.setsampwidth(2)   # 采样宽度
    f.setframerate(rate) 
    f.writeframes(y.astype(np.short).tostring())
    f.close()
    

def KS(b, N, alpha=0.99, REF_LEN=50):
    M = len(b)
    y = b
    beta = alpha ** (M / REF_LEN)
    # alpha越大，REF_LEN越大，衰减越慢
    beta2 = beta
    
    while len(y) < N:    
        y = np.append(y, beta2*b)
        beta2 *= beta
             
    return y[0:N+1]*100000


if __name__ == '__main__':
    sr = 16000 # 设置采样频率，16Khz

    b = np.random.randn(50) # 一个随机的初始化序列
    print(b)
    plt.figure(1)
    plt.plot(b)

    y = KS(b, sr*2)
    print(y)
    plt.figure(2)
    plt.plot(y)
    
    save_to_file('xx.wav',sr,y)
    plt.show()

