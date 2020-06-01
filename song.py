from chord import *


rhythm = [  {'C2' : 0},
            {'C2' : 10}, # do-si
            {'D2' : 10},
            {'E2' : 10},
            {'F2' : 10},
            {'G2' : 10},
            {'A2' : 10},
            {'B2' : 10}]

star = [1,1,5,5,6,6,5,0, # 小星星的歌的简谱
        4,4,3,3,2,2,1]


if __name__ == '__main__':
    sr = 16000 # 设置采样频率，16Khz
    time = 10 # 持续时间10秒

    y = np.zeros(sr*time)
    for i in range(len(star)):
        singley = ks_chord(rhythm[star[i]], sr*time, sr, i)
        y = y + singley

    save_to_file('xx.wav',sr,y)
    
    plt.plot(y)
    plt.show()
