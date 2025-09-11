from numpy import sin, cos, pi, exp, real, imag
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, fixed, FloatSlider, IntSlider, HBox, VBox, interactive_output, Layout
import ipywidgets as widget

# Funksjoner og klassedefinisjoner tilhørende demoer om frekvensanalyse    

def getImpulseLines(f, A, f_max):
    assert len(f)==len(A), "Error, arrays must be same length"
    f_line = np.concatenate(([-f_max], np.outer(f, np.ones(3)).flatten(), [f_max]))
    A_line = np.concatenate(([0], np.outer(A, [0, 1, 0]).flatten(), [0]))   
    return [f_line, A_line]


class dualSpectrumPlot:
    def __init__(self, ax, f_max, A_max=1, A_min=0, N=1):
        self.N = N
        self.ax = ax
        self.f_max =f_max
        self.A_max = A_max
        
        f_nd = np.outer([-f_max, f_max], np.ones(N))
        A_nd = np.zeros((2, self.N))
   
        self.lines = plt.plot(f_nd, A_nd, linewidth=2)
    
        self.ax.axis([-f_max, f_max, A_min, A_max])
        self.ax.grid(True)
        self.ax.set_xlabel("Frekvens $f$ (Hz)")
    
    def update(self, new_x, new_y):
        assert self.N == len(new_x) == len(new_y), "Error: Parameter lenght different from number of sines."
        for i in range(self.N):
            self.lines[i].set_xdata(new_x[i])  
            self.lines[i].set_ydata(new_y[i])  
            
    def setLabels(self, names):
        self.ax.legend(self.lines, names, loc='upper right')
        
    def setStyles(self, styles):
        for i in range(min(len(styles), len(self.lines))):
            try:
                self.lines[i].set_color(styles[i]['color'])
            except:
                pass
            
            try:
                self.lines[i].set_linestyle(styles[i]['linestyle'])
            except:
                pass    


def make_stem_segments(n, xn):
    """
    Create list of line segments from x and y coordinates, in the correct format
    for LineCollection: an array of the form numlines x (points per line) x 2 (x
    and y) array
    """

    points = np.array([n, xn]).T.reshape(-1, 1, 2)
    start_points = np.array([n, np.zeros(len(n))]).T.reshape(-1, 1, 2)

    segments = np.concatenate([start_points, points], axis=1)
    return segments

class interactiveStem:
    def __init__(self, ax, N = 1, A_max=1, A_min=-1):
        self.N = N
        self.ax = ax
        self.n = np.arange(self.N)
        self.samples = self.ax.stem(self.n, # 
                                    np.zeros(self.N), # Nullsampler
                                    linefmt='C3', # Linjestil stolper
                                    markerfmt='xC3', # Punktstil for stem-markere. Default er 'o' (stor prikk)
                                    basefmt='black' # Farge på y=0 aksen
                                    )
        self.samples.baseline.set_linewidth(0.5)
        # avgrensning av akser, rutenett, merkede punkt på aksene, tittel, aksenavn
        self.ax.axis([0, self.N, A_min, A_max])
        #self.ax.set_xticks(np.arange(N+1))
        #self.ax.grid(True)
        self.ax.set_xlabel("Samplenummer $n$")
        
    def update(self, n, xn):
        self.N = len(n)
        
        # Adjust stemlines, markerline, baseline in stemcontainer
        segments = make_stem_segments(n, xn)
        self.samples.stemlines.set_segments(segments)
        self.samples.markerline.set_xdata(n)
        self.samples.markerline.set_ydata(xn)
        self.samples.baseline.set_xdata([0, self.N])
        self.samples.baseline.set_ydata([0, 0])
        
        # Adjust sample markers
        #self.ax.set_xticks(np.arange(self.N+1))
        
        # Adjust axis limits
        #self.ax.set_xlim([-0.0, self.N])

# Spektral lekasje demo
class SpectralLeakageDemo:
    def __init__(self, fig_num=4, figsize=(8,6)):
        # Set up canvas
        plt.close(fig_num)
        self.fig = plt.figure(fig_num, figsize=figsize)

        # Set up subplot with amplitude spectrum
        ax1 = plt.subplot(1, 1, 1)
        #ax2.set_title(r"Amplitudespekter til sinussignal")
        #ax2.set_ylabel(r'$\left|X\left(e^{j 2\pi f}\right)\right|$')
        
        self.AmpSpectrum = dualSpectrumPlot(ax1, f_max=1, A_max = 1,  N = 1)
        self.AmpSpectrum.ax.set_xticks(np.pi*np.linspace(-1,1,9))
        self.AmpSpectrum.ax.set_xticklabels([str(round(x, 2)) + '$\pi$' for x in np.linspace(-1,1,9)])
        self.AmpSpectrum.ax.set_xlabel(r'Digital Frekvens $\hat{\omega}$')
        self.AmpSpectrum.ax.set_ylabel('Styrkegrad   (Magnitude)')
        self.AmpSpectrum.setStyles([{'color': 'tab:blue'}])
        self.AmpSpectrum.lines[0].set_label(r'"Ekte" frekvensinnhold for $x[n]$')
        self.AmpSpectrum.ax.set_title("blablabla\n")
        # Set up subplot with phase spectrum
        ax2 = ax1.twiny()
        
        self.DFT_Amp = interactiveStem(ax2, A_max=1, A_min=0)
        self.DFT_Amp.ax.set_xlabel("Frekvens-indeks $k$")
        self.DFT_Amp.samples.set_label(r'$|X[k]|$ for $N$-punkts DFT')
        self.fig.legend(bbox_to_anchor=(0.42, 0.80), loc=1)
        # Adjust figure layout
        self.fig.tight_layout(pad=0.1, w_pad=1.0, h_pad=1.0)

        # Set up UI panel
        window_len = widget.BoundedIntText(
                                        value = 16,
                                        min=0,
                                        max=64,
                                        step = 1,
                                        description='DFT window length $N$:',
                                        disabled=False,
                                        style = {'description_width': 'initial'},
                                        layout=Layout(width='95%'),
                                        continuous_update=False
        )
        signal_freq = widget.FloatSlider(
                                        value = 0.2,
                                        min=0,
                                        max=1,
                                        step = 0.01,
                                        description=r'Digital Frekvens $\hat{\omega}\ (\times \pi)$:',
                                        disabled=False,
                                        style = {'description_width': '30%'},
                                        layout=Layout(width='95%'),
                                        continuous_update=False
        )

        self.layout = HBox([VBox([signal_freq], layout=Layout(width='140%')), window_len])
        self.userInput = {
            'N': window_len,
            'F': signal_freq,
        }

        
        # Run demo
        out = interactive_output(self.update, self.userInput)
        display(self.layout, out)
        
    def update(self, F, N):
        n = np.arange(N)
        xn = cos(np.pi*F*n)
        Xk = np.fft.fft(xn)
        Xk_amp = np.absolute(np.fft.fftshift(Xk))

        k = np.arange(-(N//2), (N+1)//2)
        self.DFT_Amp.ax.set_xlim([-N/2, N/2])
        self.DFT_Amp.update(k, Xk_amp)
        self.AmpSpectrum.ax.set_title(r'$x[n] = \cos ('+str(F)+'\pi \cdot n)$ \n')
               
        
        if F==0:
            f_line, A_line = getImpulseLines([0],[N], self.AmpSpectrum.f_max)
        else:
            f_line, A_line = getImpulseLines([-F*np.pi, F*np.pi],[N/2, N/2], self.AmpSpectrum.f_max)
                                            
        self.AmpSpectrum.update([f_line],[A_line])
        self.AmpSpectrum.ax.set_ylim(ymax=N/1.7)
        
def getArrow(x, y, dx, dy, arrowhead_scale=1):
    r = np.hypot(dx, dy)
    theta = np.arctan2(dy,dx)
    len_arrowhead = min(arrowhead_scale/16, r/2)
    x_arrow = np.array([x, x+dx, x+dx+len_arrowhead*cos(theta-4*pi/5), x+dx, x+dx+len_arrowhead*cos(theta+4*pi/5)])
    y_arrow = np.array([y, y+dy, y+dy+len_arrowhead*sin(theta-4*pi/5), y+dy, y+dy+len_arrowhead*sin(theta+4*pi/5)])
    return x_arrow, y_arrow

class vectorPlot:
    def __init__(self, ax, A_max, N=1, arrowhead_scale=1):
        self.ax = ax
        self.N = N
        self.arrowhead_scale=arrowhead_scale
        init_values = np.zeros((2, N))
        self.lines = self.ax.plot(init_values, init_values)
        self.ax.grid(True)
        self.ax.set_xlabel("Reell akse")
        self.ax.set_ylabel("Imaginær akse")
        self.ax.axis([-A_max, A_max, -A_max, A_max])
        
    def update(self, x_new_lines, y_new_lines):
        assert len(x_new_lines)==len(y_new_lines)==self.N, 'Error: mismatch between x and y dimensions.'
        for i in range(self.N):
            x_line = x_new_lines[i]
            y_line = y_new_lines[i]
            L = len(x_line)
            assert len(y_line)==L, 'Error: mismatch between x and y dimensions.'
            x_arrows = np.zeros((L-1)*5)
            y_arrows = np.zeros((L-1)*5)
            for j in range(1, L):
                b = j*5
                a = b-5
                x_arrows[a:b], y_arrows[a:b] = getArrow(x_line[j-1], y_line[j-1], x_line[j]-x_line[j-1], y_line[j]-y_line[j-1], arrowhead_scale = self.arrowhead_scale)
            self.lines[i].set_xdata(x_arrows)
            self.lines[i].set_ydata(y_arrows)
            
    def setLabels(self, names):
        self.ax.legend(self.lines, names, loc='upper right')
        
    def setStyles(self, styles):
        for i in range(min(len(styles), len(self.lines))):
            try:
                self.lines[i].set_color(styles[i]['color'])
            except:
                pass
            
            try:
                self.lines[i].set_linestyle(styles[i]['linestyle'])
            except:
                pass 

# Vektorrepresentasjon av komplekst tall på polarform        
class DTFT_demo:
    def __init__(self, xn, fig_num=5, figsize=(12,8)):
        self.xn = xn
        self.N = len(xn)
        self.f = np.linspace(-1, 1, 501)
        self.H_f = np.fft.fftshift(np.fft.fft(xn, 501))
        
        
        # Set up canvas
        plt.close(fig_num)
        self.fig = plt.figure(fig_num, figsize=figsize)
        
        ax = plt.subplot(2,3, (1, 5))
    
     
        ax.set_title(r"$\sum_{n=0}^{N-1} x[n]\cdot e^{j\hat{\omega}\cdot n}$")
        ax.set_aspect(1)
        self.VectorFig = vectorPlot(ax, A_max = sum(np.absolute(xn)), N = 2, arrowhead_scale = self.N/2)
        
        self.VectorFig.setStyles([{'color': 'tab:blue'}])
        self.VectorFig.lines[1].set_color('C3')
        self.VectorFig.ax.plot(np.real(self.H_f), np.imag(self.H_f), ':C0')
        
        ax2 = plt.subplot(2,3,3)
        ax2.plot(self.f, np.abs(self.H_f))
        ax2.set_xlim([-1, 1])
        ax2.set_ylim(ymin=0)
        ax2.grid(True)
        ax2.set_ylabel(r'$\left|X\left(\hat{\omega} \right) \right|$')
        ax2.set_xticks(np.linspace(-1, 1, 5))
        ax2.set_xticklabels([str(round(f,1))+'$\pi$' for f in np.linspace(-1, 1, 5)])
        
        self.MagHighlight, = ax2.plot([0,0], [0,0], 'C3')
        self.MagHighlight.set_ydata([0, 100])
        
      
        ax3 = plt.subplot(2,3,6)
        ax3.plot(self.f, np.angle(self.H_f)*(np.abs(self.H_f)>1e-10))
        ax3.set_xlim([-1, 1])
        ax3.set_ylim([-pi, pi])
        ax3.set_yticks(np.linspace(-1, 1, 9)*pi)
        ax3.set_yticklabels([str(round(f,1))+'$\pi$' for f in np.linspace(-1, 1, 9)])
        ax3.set_ylabel(r'$\angle X\left(\hat{\omega} \right)$')
        ax3.set_xticks(np.linspace(-1, 1, 5))
        ax3.set_xticklabels([str(round(f,1))+'$\pi$' for f in np.linspace(-1, 1, 5)])
        ax3.set_xlabel(r'Digital Frekvens $\hat{\omega}$')
        
        self.AngleHighlight, = ax3.plot([0,0], [0,0], 'C3')
        self.AngleHighlight.set_ydata([-100, 100])
        
        ax3.grid(True)
        
        # Tilpass figur-layout
        self.fig.tight_layout(pad=0.1, w_pad=1.0, h_pad=1.0)

        signal_freq = widget.FloatSlider(
                                        value = 0.0,
                                        min=-1,
                                        max=1,
                                        step = 1/60,
                                        description=r'Digital Frekvens $\hat{\omega}\ (\times \pi)$:',
                                        disabled=False,
                                        style = {'description_width': '30%'},
                                        layout=Layout(width='95%'),
                                        continuous_update=True
        )
        layout = HBox([signal_freq])
        # Run Demo:
        out = interactive_output(self.update, {'omega': signal_freq})
        display(layout, out)
        
    def update(self, omega):
        vectors = self.xn*np.exp(1j*omega*pi*np.arange(self.N))
        vectorSums = np.array([np.sum(vectors[0:i]) for i in range(self.N+1)])
        x = np.append(np.array([0]), np.real(vectorSums))
        y = np.append(np.array([0]), np.imag(vectorSums))
        self.VectorFig.update([x, np.array([0, x[-1]])], [y, np.array([0, y[-1]])])
        
        self.MagHighlight.set_xdata([omega, omega])
        self.AngleHighlight.set_xdata([omega, omega])