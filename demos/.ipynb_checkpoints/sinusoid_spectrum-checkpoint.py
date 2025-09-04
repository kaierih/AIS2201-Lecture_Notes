from numpy import sin, cos, pi, exp, real, imag
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, fixed, FloatSlider, IntSlider, HBox, VBox, interactive_output, Layout
import ipywidgets as widget

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

class timeSeriesPlot:
    def __init__(self, ax, t, A_max, N=1, t_unit='s'):
        res  = len(t)
        self.N = N
        t_nd = np.outer(t, np.ones(self.N))
        x_t = np.zeros((res, self.N))          

        self.ax = ax
        self.lines = self.ax.plot(t_nd, x_t)
        
        # avgrensning av akser, rutenett, merkede punkt på aksene, tittel, aksenavn
        self.ax.axis([t[0], t[-1], -A_max, A_max])
        self.ax.grid(True)
        self.ax.set_xticks(np.linspace(t[0],t[-1],11))
        self.ax.set_xlabel("Tid (" + t_unit + ")")
        
    def update(self, new_lines):
        assert self.N == len(new_lines), "Error: Parameter lenght different from number of sines."
        for i in range(self.N):
            self.lines[i].set_ydata(new_lines[i])
            
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

# Frekvensmiksing      
class SinusoidSpectrumDemo:
    def __init__(self, fig_num=1, fig_size=(9,5)):
        # Set up canvas
        plt.close(fig_num)
        self.fig = plt.figure(fig_num, figsize=fig_size)
        
        
        # Set up subplot with sine waves
        ax1 = plt.subplot(3, 1,1)
        ax1.set_title(r"Sinusoide i Tidsplan")
        ax1.set_ylabel(r'x(t)')
        
        self.t = np.linspace(0, 1, 501)
        self.SineWaves = timeSeriesPlot(ax1, self.t, A_max = 1,  N = 1)
        
        self.SineWaves.setStyles([{'color': 'tab:blue'}])
        
       # Set up subplot with amplitude spectrum
        ax2 = plt.subplot(3, 1,2)
        ax2.set_title(r"Styrkegradsspekter til sinussignal")
        ax2.set_ylabel(r'$\left|X\left( f \right)\right|$')
        
        self.AmpSpectrum = dualSpectrumPlot(ax2, f_max=20, A_max = 1,  N = 1)
        
        self.AmpSpectrum.setStyles([{'color': 'tab:blue'}])
        
        # Set up subplot with phase spectrum
        ax3 = plt.subplot(3, 1,3)
        ax3.set_title(r"Fasespekter til sinussignal")
        ax3.set_ylabel(r'$\angle X\left(f \right)$')
        ax3.set_yticks(pi*np.linspace(-1, 1, 9))
        ax3.set_yticklabels([f'${x:.2f}\pi$' for x in np.linspace(-1, 1, 9)])
        self.PhaseSpectrum = dualSpectrumPlot(ax3, f_max=20, A_max = pi, A_min=-pi,  N = 1)
        
        self.PhaseSpectrum.setStyles([{'color': 'tab:blue'}])


        # Adjust figure layout
        self.fig.tight_layout(pad=0.1, w_pad=1.0, h_pad=1.0)

        # Set up UI panel
        signal_amp = widget.FloatSlider(
                                        value = 1.0,
                                        min=0,
                                        max=1,
                                        step = 0.05,
                                        description='Ampltiude $A$:',
                                        disabled=False,
                                        style = {'description_width': '25%'},
                                        layout=Layout(width='95%'),
                                        continuous_update=True
        )
        signal_freq = widget.FloatSlider(
                                        value = 1,
                                        min=0,
                                        max=20,
                                        step = 1,
                                        description=r'Frekvens $f$:',
                                        disabled=False,
                                        style = {'description_width': '25%'},
                                        layout=Layout(width='95%'),
                                        continuous_update=True
        )
        signal_phase = widget.FloatSlider(
                                        value = 0,
                                        min=-1,
                                        max=1,
                                        step = 1/12,
                                        description=r'Phase $\phi \ \ (\times \pi)$:',
                                        disabled=False,
                                        style = {'description_width': '25%'},
                                        layout=Layout(width='95%'),
                                        continuous_update=True
        )
        self.layout = HBox([VBox([signal_amp, signal_freq, signal_phase], layout=Layout(width='90%'))])
        self.userInput = {
            'F': signal_freq,
            'A': signal_amp,
            'phi': signal_phase
        }
        # Run demo
        out = interactive_output(self.update, self.userInput)
        display(self.layout, out)
        
    def update(self, A, F, phi):

        x1 = A*cos(2*pi*F*self.t + phi*pi)

        self.SineWaves.ax.set_title(r'Sinussignal: $x(t) = '+str(round(A,1))+'\cdot \cos(2\pi \cdot'+str(round(F))+'\cdot t + '+str(round(phi,2))+'\pi)$')
        self.SineWaves.update([x1])
        if F==0:
            f1_line, A1_line = getImpulseLines([0],[A*cos(phi*pi)], self.AmpSpectrum.f_max)
            f1_line, phi1_line = getImpulseLines([0], [0], self.PhaseSpectrum.f_max)
        else:
            f1_line, A1_line = getImpulseLines([-F, F],[A/2, A/2], self.AmpSpectrum.f_max)
            f1_line, phi1_line = getImpulseLines([-F, F],[-phi*pi, phi*pi], self.AmpSpectrum.f_max)
                                            
        self.AmpSpectrum.update([f1_line],[A1_line])
        self.PhaseSpectrum.update([f1_line],[phi1_line])