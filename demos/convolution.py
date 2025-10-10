from numpy import sin, cos, pi, exp, real, imag
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, fixed, FloatSlider, IntSlider, HBox, VBox, interactive_output, Layout, Output
import ipywidgets as widget

# Interactive stem plot with matlab-ish default config
class interactiveStem:
    def __init__(self, ax, n, xn, color='tab:blue', marker='o', label=None, filled=False):
        self.ax = ax
        self.samples = self.ax.stem(n, # 
                                    xn, # Nullsampler
                                    basefmt='black', # Farge på y=0 aksen
                                    label=label
                                    )
        self.samples.baseline.set_linewidth(0.5)
        self.samples.baseline.set_xdata([0, len(n)])
        self.samples.markerline.set_color(color)
        self.samples.markerline.set_marker(marker)
        if not filled:
            self.samples.markerline.set_markerfacecolor('none')
        self.samples.stemlines.set_color(color)
        self.ax.grid(True)
        
    def update(self, n, xn):
        self.N = len(n)
        
        # Make new line collection
        points = np.array([n, xn]).T.reshape(-1, 1, 2)
        start_points = np.array([n, np.zeros(len(n))]).T.reshape(-1, 1, 2)
        segments = np.concatenate([start_points, points], axis=1)
        
        # Adjust markers and lines
        self.samples.stemlines.set_segments(segments)
        self.samples.markerline.set_xdata(n)
        self.samples.markerline.set_ydata(xn)
        
class ConvolutionDemo:
    def __init__(self, xn, hn, fig_num = 1, figsize=(8, 6)):
        self.xn = xn
        self.L = len(xn)
        self.hn = hn
        self.M = len(hn)
        self.yn = np.convolve(self.hn, self.xn)
        self.yn_circular = self.yn[:self.L].copy()
        self.yn_circular[0:self.M-1] += self.yn[self.L:]
        
        plt.close(fig_num)
        self.fig = plt.figure(fig_num, figsize=figsize)
             
        ### Subplot 1
        # Plot Input signal x[k]
        ax1 = plt.subplot(3,1,1)

        xn_samples = ax1.stem(xn, 
                               linefmt='C0', # Linjestil stolper
                               markerfmt='oC0', # Punktstil for stem-markere. Default er 'o' (stor prikk)
                               basefmt='black', # Farge på y=0 aksen
                               label=r'$x[k]$'
                               )
        xn_samples.baseline.set_linewidth(0.5)
        xn_samples.baseline.set_xdata([-self.M, self.L+self.M])
        xn_samples.markerline.set_markerfacecolor('none')
        ax1.set_xlim([-self.M, self.L+self.M-1])
        
        
        # Plot reversed impulse response h[n-k]
        self.hn_samples = interactiveStem(ax1, -np.arange(len(self.hn)), self.hn, color='C3', marker='x', label=r'$h[n-k]$')
        ax1.legend(loc='upper left')
        ax1.grid(True)
        self.ax1 = ax1
        self.update_title(0)
        
        ### Subplot 2
        # Plot x[k]*h[n-k]
        ax2 = plt.subplot(3,1,2)
        ax2.grid(True)
        self.xn_hn = interactiveStem(ax2, [0], [self.hn[0]*self.xn[0]], color='C4', label=r'$x[k]\cdot x[n-k]$', filled=True)
        self.xn_hn.ax.set_xlim([-self.M, self.L+self.M-1])
        self.xn_hn.samples.baseline.set_xdata([-self.M, self.L+self.M])
        self.xn_hn.ax.set_ylim([-max(abs(xn))*max(abs(hn))*1.05, max(abs(xn))*max(abs(hn))*1.05])
        self.xn_hn.ax.legend(loc='upper left')
        ax2.set_xlabel(r'$k$')

        
        ### Subplot 3
        # Plot y[n]
        ax3 = plt.subplot(3,1,3)
        self.yn_samples = interactiveStem(ax3,
                                          np.arange(len(self.yn)),
                                          self.yn,
                                          color='C2', # Linjestil stolper
                                          label=r'$y[n]$'
                                          )
        ax3.set_xlim([-self.M, self.M+self.L-1])
        ax3.grid(True)
        ax3.set_xlabel(r'$n$')
        self.yn_active = interactiveStem(ax3, [0], [self.yn[0]], color='C3', label=r'$y[n]$', filled=True)
        ax3.legend(loc='upper left')
        if max(np.abs(ax3.get_ylim())) < max(np.abs(ax1.get_ylim())):
            ax3.set_ylim(np.array(ax1.get_ylim()))
        
        # Confiugre Layout
        self.fig.tight_layout(pad=0.1, w_pad=1.0, h_pad=1.0)
        
        #Set up slider panel
        # Set up UI panel
        self.sample_num = widget.IntSlider(value = 0,
                                          min=0,
                                          max=self.L+self.M-2,
                                          step = 1,
                                          description='Sample number n:',
                                          disabled=False,
                                          style = {'description_width': 'initial'},
                                          layout=Layout(width='70%'),
                                          continuous_update=True
                                          )

        self.conv_mode = widget.Dropdown(options=['full', 'same', 'valid', 'circular'],
                                         value='full',
                                         description='Mode:',
                                         disabled=False,
                                         layout=Layout(width='20%'))

        self.sample_num.observe(lambda change: self.update_n(change['new']), names='value')
        self.conv_mode.observe(lambda change: self.update_mode(change['new']), names='value')

        self.layout = HBox([self.sample_num, self.conv_mode])
        

        display(self.layout, Output())
        
    def update_n(self, n):
        if self.conv_mode.value=='circular':
            n_array = np.arange(n-self.M+1, n+1)%self.L
            self.xn_hn.update(n=n_array, xn=self.xn[n_array]*np.flip(self.hn[::-1]))
            self.hn_samples.update(n_array, np.flip(self.hn))
            self.yn_active.update([n], [self.yn_circular[n]])
        else:
            n_1 = max(0, n-self.M+1)
            n_2 = min(self.L, n+1)
            k_1 = max(0, n-self.L+1)
            k_2 = min(self.M, n+1)
            n_array = np.arange(n_1, n_2)
            #noverlap = min(self.L, n_2-n_1)
            self.xn_hn.update(n=n_array, xn=self.xn[n_1:n_2]*np.flip(self.hn[k_1:k_2]))
            self.yn_active.update([n], [self.yn[n]])
            self.hn_samples.update(np.arange(n-self.M+1, n+1), np.flip(self.hn))
            
        self.hn_samples.samples.set_label(r'$h['+str(n)+'-k]$')
        self.hn_samples.ax.legend(loc='upper left')
        self.xn_hn.samples.set_label(r'$x[k]\cdot h['+str(n)+'-k]$')
        self.xn_hn.ax.legend(loc='upper left')
        self.yn_active.samples.set_label(r'$y['+str(n)+']$')
        self.yn_active.ax.legend(loc='upper left')
        self.update_title(n)
        
    def update_title(self, n):
        title_str = 'Convolution Sum: $y[n] = \\sum_{k=0}^{%d}x[k]\\cdot h[%d - k]$'%(self.L-1, n)
        self.ax1.set_title(title_str)
        
    def update_mode(self, mode):
        if mode=='full':
            self.sample_num.min=0
            self.sample_num.max=self.L+self.M-2
        elif mode=='same':
            self.sample_num.min=(self.M-1)//2
            self.sample_num.max=(self.M-1)//2+self.L-1
        elif mode=='valid':
            self.sample_num.min=self.M-1
            self.sample_num.max=self.L-1
        elif mode=='circular':
            self.sample_num.min=0
            self.sample_num.max=self.L-1
        else:
            raise Exception("Unrecognized Convolution Mode")

        if mode=='circular':
            self.yn_samples.update(np.arange(self.sample_num.min, self.sample_num.max+1), self.yn_circular)
        else:
            self.yn_samples.update(np.arange(self.sample_num.min, self.sample_num.max+1), self.yn[np.arange(self.sample_num.min, self.sample_num.max+1)])

        if self.sample_num.value < self.sample_num.min:
            self.sample_num.value = self.sample_num.min
            self.update_n(self.sample_num.value)
        elif self.sample_num.value > self.sample_num.max:
            self.sample_num.value = self.sample_num.max
            self.update_n(self.sample_num.value)
        else:
            self.update_n(self.sample_num.value)