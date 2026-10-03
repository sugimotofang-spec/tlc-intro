"""Procedural 30s soundtrack for the TLC film, synced to film.src.html timeline.
120 BPM, A minor -> resolves to C major at the closing card."""
import numpy as np, wave

SR = 48000
DUR = 30.0
N = int(SR * DUR)
rng = np.random.default_rng(7)
L = np.zeros(N); R = np.zeros(N)          # dry bus
RL = np.zeros(N); RR = np.zeros(N)        # reverb send

def note(n):  # midi -> hz
    return 440.0 * 2 ** ((n - 69) / 12)

def env_adsr(n, a, d, s, r, sus_len):
    a_n, d_n, r_n = int(a*SR), int(d*SR), int(r*SR)
    s_n = max(0, int(sus_len*SR) - a_n - d_n)
    e = np.concatenate([np.linspace(0, 1, max(a_n,1), endpoint=False),
                        np.linspace(1, s, max(d_n,1), endpoint=False),
                        np.full(s_n, s),
                        np.linspace(s, 0, max(r_n,1))])
    return e[:n] if len(e) >= n else np.pad(e, (0, n-len(e)))

def fft_filter(x, lo=None, hi=None, order=2):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1/SR); H = np.ones_like(f)
    if hi: H *= 1/np.sqrt(1+(f/hi)**(2*order))
    if lo: H *= 1/np.sqrt(1+(lo/np.maximum(f,1e-3))**(2*order))
    return np.fft.irfft(X*H, len(x))

def add(sig, t, gain=1.0, pan=0.0, send=0.0):
    i = int(t*SR)
    if i >= N: return
    sig = sig[:N-i]
    gl = gain*np.cos((pan+1)*np.pi/4); gr = gain*np.sin((pan+1)*np.pi/4)
    L[i:i+len(sig)] += sig*gl; R[i:i+len(sig)] += sig*gr
    if send:
        RL[i:i+len(sig)] += sig*gl*send; RR[i:i+len(sig)] += sig*gr*send

def saw(freq, n, phase=0.0):
    t = np.arange(n)/SR
    # band-limited-ish saw via additive (up to 8k)
    out = np.zeros(n); k = 1
    while freq*k < 9000 and k < 40:
        out += ((-1)**(k+1)) * np.sin(2*np.pi*freq*k*t + phase*k) / k; k += 1
    return out * (2/np.pi)

# ---------------------------------------------------------------- instruments
def pad_chord(notes, t0, t1, gain, bright=1800, attack=.35, release=.6):
    n = int((t1-t0+release)*SR); sig_l = np.zeros(n); sig_r = np.zeros(n)
    for m in notes:
        for det, pan in ((-7, -.6), (0, 0), (7, .6)):
            f = note(m) * 2**(det/1200)
            s = saw(f, n, phase=rng.uniform(0, 6.28))
            sig_l += s*np.cos((pan+1)*np.pi/4); sig_r += s*np.sin((pan+1)*np.pi/4)
    e = env_adsr(n, attack, .4, .85, release, t1-t0)
    sig_l = fft_filter(sig_l*e, hi=bright, order=2); sig_r = fft_filter(sig_r*e, hi=bright, order=2)
    i = int(t0*SR); m = min(n, N-i)
    L[i:i+m] += sig_l[:m]*gain; R[i:i+m] += sig_r[:m]*gain
    RL[i:i+m] += sig_l[:m]*gain*.5; RR[i:i+m] += sig_r[:m]*gain*.5

def kick(t, gain=1.0):
    n = int(.45*SR); tt = np.arange(n)/SR
    f = 46 + 110*np.exp(-tt*38)
    ph = 2*np.pi*np.cumsum(f)/SR
    s = np.sin(ph)*np.exp(-tt*7.5) + 0.25*np.exp(-tt*400)*rng.standard_normal(n)
    add(np.tanh(s*1.6), t, gain)

def clap(t, gain=1.0):
    n = int(.3*SR); tt = np.arange(n)/SR; s = np.zeros(n)
    for k, d in enumerate((0, .011, .022)):
        j = int(d*SR); nb = rng.standard_normal(n-j)*np.exp(-np.arange(n-j)/SR*(60 if k<2 else 18))
        s[j:] += nb
    s = fft_filter(s, lo=900, hi=4200)
    add(s, t, gain, 0, .35)

def hat(t, gain=1.0, open_=False, pan=.25):
    n = int((.22 if open_ else .05)*SR); tt = np.arange(n)/SR
    s = rng.standard_normal(n)*np.exp(-tt*(18 if open_ else 90))
    s = fft_filter(s, lo=7000)
    add(s, t, gain, pan, .1)

def pluck(m, t, gain=1.0, pan=0, send=.4, dec=5.0):
    n = int(1.2*SR); tt = np.arange(n)/SR; f = note(m)
    s = (np.sin(2*np.pi*f*tt) + .45*np.sin(2*np.pi*2*f*tt)*np.exp(-tt*6) + .2*np.sin(2*np.pi*3*f*tt)*np.exp(-tt*10))
    s *= np.exp(-tt*dec) * np.minimum(1, tt/0.003)
    add(s, t, gain, pan, send)

def bell(m, t, gain=1.0, pan=0, send=.6, dec=1.6):
    n = int(3.5*SR); tt = np.arange(n)/SR; f = note(m)
    mod = np.sin(2*np.pi*f*3.5*tt) * 2.2*np.exp(-tt*3)
    s = np.sin(2*np.pi*f*tt + mod) * np.exp(-tt*dec) * np.minimum(1, tt/0.002)
    s += .3*np.sin(2*np.pi*f*2*tt)*np.exp(-tt*dec*1.8)
    add(s, t, gain, pan, send)

def bass_note(m, t, length, gain=1.0):
    n = int((length+.05)*SR); tt = np.arange(n)/SR; f = note(m)
    s = np.sin(2*np.pi*f*tt) + .35*np.sin(2*np.pi*2*f*tt) + .12*saw(f, n)
    e = np.minimum(1, tt/.006) * np.exp(-tt*2.2) * np.clip((length+.05-tt)/.04, 0, 1)
    add(np.tanh(s*e*1.3), t, gain, 0, 0)

def noise_sweep(t0, t1, f0, f1, gain, pan=0, send=.3, shape='rise'):
    """noise through moving bandpass (STFT overlap-add)."""
    n = int((t1-t0)*SR); x = rng.standard_normal(n + 4096)
    hop, win = 1024, np.hanning(2048); out = np.zeros(n + 4096)
    freqs = np.fft.rfftfreq(2048, 1/SR)
    for k in range(0, n, hop):
        u = k/max(n-1, 1)
        fc = f0 * (f1/f0)**u
        H = np.exp(-0.5*(np.log2(np.maximum(freqs, 1)/fc)/0.7)**2)
        seg = x[k:k+2048]*win
        out[k:k+2048] += np.fft.irfft(np.fft.rfft(seg)*H, 2048)*win
    out = out[:n]; u = np.linspace(0, 1, n)
    if shape == 'rise': e = u**2.2
    elif shape == 'whoosh': e = np.sin(np.pi*u)**1.6
    else: e = (1-u)**2
    add(out*e/ (np.abs(out).max()+1e-9), t0, gain, pan, send)

def sub_boom(t, gain=1.0):
    n = int(2.0*SR); tt = np.arange(n)/SR
    f = 34 + 40*np.exp(-tt*6); s = np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*2.2)*np.minimum(1, tt/.004)
    add(s, t, gain, 0, .15)

def drop(t, gain=1.0, pan=0):  # water drop plink
    n = int(.25*SR); tt = np.arange(n)/SR
    f = 1500*np.exp(-tt*18) + 700
    s = np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*22)*np.minimum(1, tt/.001)
    add(s, t, gain, pan, .5)

def tick(t, gain=1.0, pan=0, f=2600):
    n = int(.04*SR); tt = np.arange(n)/SR
    s = np.sin(2*np.pi*f*tt)*np.exp(-tt*160) + .4*rng.standard_normal(n)*np.exp(-tt*300)
    add(s, t, gain, pan, .2)

def boing(t, gain=1.0):
    n = int(.7*SR); tt = np.arange(n)/SR
    f = 190*(1 + .18*np.exp(-tt*5)*np.sin(2*np.pi*11*tt)) + 60*np.exp(-tt*9)
    s = np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*5.5)*np.minimum(1, tt/.004)
    add(s, t, gain, 0, .25)

# ---------------------------------------------------------------- arrangement
BEAT = 0.5
A, C, D, E, F, G = 57, 60, 62, 64, 65, 67    # around A3
CH = {'Am': [57, 60, 64, 69], 'F': [53, 60, 65, 69], 'C': [55, 60, 64, 67], 'G': [55, 59, 62, 67], 'Cadd9': [48, 55, 62, 64, 67]}
BASS = {'Am': 33, 'F': 29, 'C': 36, 'G': 31}
prog = ['Am', 'F', 'C', 'G', 'Am', 'F', 'C', 'G', 'Am', 'F', 'G']   # 4.0 -> 26.0 (2s each)

# intro pad (Am, filter opening) 0-4
pad_chord([45, 57, 64, 69], 0.0, 4.0, .10, bright=900, attack=1.6, release=.4)
noise_sweep(2.4, 4.0, 300, 7000, .22, send=.4, shape='rise')
# loom shuttle ticks: 8ths -> 16ths
tk = 0.5
while tk < 3.95:
    tick(tk, .10 + .12*(tk/4), pan=np.sin(tk*3)*.5, f=2200 + 400*np.sin(tk*5))
    tk += .25 if tk < 2.0 else .125
# reverse swell into impact
noise_sweep(3.55, 4.0, 1200, 9000, .28, shape='rise', send=.2)

# impact 4.0
sub_boom(4.0, .9); kick(4.0, .9)
noise_sweep(4.0, 4.9, 6000, 400, .25, shape='fall', send=.5)
for m in (69, 72, 76, 81): pluck(m, 4.0, .16, send=.7, dec=2.2)
# stripe plucks (landing)
pent = [69, 72, 74, 76, 79, 81]
for k in range(6): pluck(pent[k] + 12, 4.0 + k*.07 + .24, .13, pan=(-.5 if k%2 else .5), dec=6)
bell(81, 4.42, .10)                     # blob pop
for k in range(3): tick(4.66 + k*.09, .14, f=1800 + k*300)
for t0, m in ((6.70, 76), (7.00, 79), (7.30, 81)): bell(m+12, t0, .11, pan=(t0-7)*1.5)

# chords + bass + drums 4.0 -> 26.0
for b, ch in enumerate(prog):
    t0 = 4.0 + b*2
    pad_chord(CH[ch], t0, t0+2.0, .055 if t0 < 8 else .05, bright=1400 if t0 < 8 else 2200)
    root = BASS[ch]
    for k in range(4 if t0 < 8 else 8):
        step = (2.0/(4 if t0 < 8 else 8))
        bass_note(root + (12 if (k % 4 == 3 and t0 >= 8) else 0), t0 + k*step + (0.0 if t0 < 8 else .25*0), step*.8, .30)

t = 4.0
while t < 25.99:
    full = t >= 8.0
    if full or abs((t-4.0) % 1.0) < 1e-6:
        kick(t, .75 if full else .55)
    beat_idx = int(round((t-4.0)/BEAT))
    if full and beat_idx % 2 == 1: clap(t, .30)
    if full:
        hat(t + .25, .10, open_=(beat_idx % 4 == 3))
        if t >= 14: hat(t + .125, .045, pan=-.3); hat(t + .375, .045, pan=-.3)
    t += BEAT

# arp 8 -> 26
arp_t = 8.0
while arp_t < 25.99:
    b = int((arp_t-4.0)//2); ch = CH[prog[min(b, len(prog)-1)]]
    k = int(round((arp_t-8.0)/.125))
    m = ch[[0, 1, 2, 3, 2, 1, 3, 2][k % 8]] + 12
    pluck(m, arp_t, .045 if arp_t < 20 else .06, pan=(.45 if k % 2 else -.45), send=.45, dec=9)
    arp_t += .125

# transitions
for tw in (8.0, 14.0, 20.0):
    noise_sweep(tw-.35, tw+.35, 500, 8000, .30, pan=-.3, shape='whoosh', send=.3)
# S3 steps
for t0 in (8.35, 9.7, 11.0, 12.3): tick(t0, .22, f=3200); bell(88, t0, .035, send=.5)
# weaving shuttle micro ticks
tk = 8.4
while tk < 9.7: tick(tk, .05, pan=np.sin(tk*9)*.6, f=4200); tk += .0625
# dye wash
noise_sweep(9.7, 11.0, 300, 2500, .07, shape='whoosh', send=.6)
# droplets
for i in range(7): drop(11.55 + i*.075 + (i*37 % 7)*.01, .16, pan=((i*53) % 10)/5-1)
# lamination press
noise_sweep(12.9, 13.45, 200, 1200, .10, shape='rise'); kick(13.45, .5); sub_boom(13.45, .35)
# labels
for i in range(5): tick(14.75 + i*.11 + .2, .12, f=2400 + i*200)
# physics
noise_sweep(16.9, 17.3, 150, 900, .14, shape='rise', send=.1)
kick(17.3, .35); boing(17.5, .30)
kick(18.45, .55); boing(18.5, .22)
for i in range(5): tick(16.95 + i*.17 + .2, .10, f=1900 + i*150, pan=.6)
# map sparkle + pins
noise_sweep(20.1, 20.9, 4000, 11000, .05, shape='whoosh', send=.6)
for t0, m in ((21.0, 76), (21.35, 81), (21.7, 84), (22.05, 88)): bell(m, t0, .10, pan=(t0-21.5), dec=2.2)
# ESG badges
for i in range(4): pluck(81 + [0, 3, 5, 7][i], 23.25 + i*.2, .08, pan=-.4 + i*.27, dec=7)
bell(76, 24.25, .06, dec=1.4)

# closing 26 -> 30
noise_sweep(25.6, 26.75, 400, 9000, .32, shape='whoosh', send=.5)
pad_chord(CH['Cadd9'] + [72, 76], 26.0, 30.0, .07, bright=2600, attack=.5, release=.2)
bass_note(36, 26.0, 3.5, .22)
for m in (72, 79, 84, 88): bell(m, 27.3, .08, dec=1.0, send=.8)
sub_boom(27.3, .30)
for k in range(3): tick(27.3 + .42 + k*.09, .10, f=1900 + k*250)

# ---------------------------------------------------------------- mix
# sidechain duck on pad/arp: approximate by global envelope keyed to kick times
duck = np.ones(N)
t = 8.0
while t < 26.0:
    i = int(t*SR); n = int(.22*SR)
    duck[i:i+n] = np.minimum(duck[i:i+n], 1 - .35*np.exp(-np.arange(n)/SR*14))
    t += BEAT
# reverb (convolution with synthetic IR)
ir_n = int(2.4*SR); tt = np.arange(ir_n)/SR
irL = rng.standard_normal(ir_n)*np.exp(-6.9*tt/2.4); irR = rng.standard_normal(ir_n)*np.exp(-6.9*tt/2.4)
irL[:int(.018*SR)] = 0; irR[:int(.024*SR)] = 0
irL = fft_filter(irL, hi=6000); irR = fft_filter(irR, hi=6000)
irL /= np.sqrt((irL**2).sum()); irR /= np.sqrt((irR**2).sum())
def conv(x, h):
    m = 1 << int(np.ceil(np.log2(len(x)+len(h))))
    return np.fft.irfft(np.fft.rfft(x, m)*np.fft.rfft(h, m), m)[:len(x)]
wetL = conv(RL, irL)*.55; wetR = conv(RR, irR)*.55
outL = (L + wetL)*duck**.5; outR = (R + wetR)*duck**.5
# master fade
fade = np.ones(N); fi = int(.25*SR); fade[:fi] = np.linspace(0, 1, fi)
fo0 = int(28.4*SR); fade[fo0:] = np.linspace(1, 0, N-fo0)**1.5
outL *= fade; outR *= fade
# gentle glue + limiter
outL = np.tanh(outL*1.2)/np.tanh(1.2); outR = np.tanh(outR*1.2)/np.tanh(1.2)
peak = max(np.abs(outL).max(), np.abs(outR).max())
outL *= .89/peak; outR *= .89/peak
pcm = (np.stack([outL, outR], 1)*32767).astype('<i2')
with wave.open('music.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('music.wav written', pcm.shape, 'peak', peak)
