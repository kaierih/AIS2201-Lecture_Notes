from numpy import cos, pi
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interactive_output, FloatSlider, HBox, VBox, Layout


def sliderPanelSetup(set_details, n_of_sets=1, slider_type='float'):
    panel_col = []
    sliders = {}
    for i in range(n_of_sets):
        panel_row = []
        for item in set_details:
            mathtext = item['description']
            mathtext = mathtext.strip('$')
            if n_of_sets > 1:
                if mathtext.find(" ") == -1:
                    mathtext = '$' + mathtext + '_' + str(i+1) + '$' 
                else:
                    mathtext = '$' + mathtext.replace(" ", '_'+str(i+1)+'\\ ', 1) + '$'
            else:
                mathtext = '$' + mathtext + '$'
            #mathtext = r'{}'.format(mathtext)

            panel_row.append(FloatSlider(value=item['value'], 
                                         min=item['min'],
                                         max = item['max'], 
                                         step = item['step'], 
                                         description=mathtext, 
                                         layout=Layout(width='95%')))
            
            sliders[item['keyword']+str(i+1)] = panel_row[-1]
        panel_col.append(HBox(panel_row, layout = Layout(width='100%')))
    layout = VBox(panel_col, layout = Layout(width='90%'))
    return sliders, layout

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
# Demo 1
# Visualisering av en sinusbølge
class SineWaveDemo():
    def __init__(self, fig_num=1, fig_size = (9, 4)):
        # Set up canvas
        plt.close(fig_num)
        self.fig = plt.figure(fig_num, figsize=fig_size)
        
        # Set up subplot with sine wave
        ax = plt.subplot()
        ax.set_title(" ")
        
        self.t = np.linspace(-1, 1, 501)
        self.SineWave = timeSeriesPlot(ax, self.t, A_max = 2)
        
        # Tilpass figur-layout
        self.fig.tight_layout(pad=0.1, w_pad=1.0, h_pad=1.0)
        
        # Set up slider panel
        self.sliders, self.layout = sliderPanelSetup(
            [{'keyword': 'A', 'value': 1, 'min': 0, 'max': 2, 'step': 0.1, 'description': r'A'},
             {'keyword': 'f', 'value': 1, 'min': 0.5, 'max': 15, 'step': 0.5, 'description': r'f'},
             {'keyword': 'phi', 'value': 0.5, 'min': -1, 'max': 1, 'step': 1/12, 'description': r'\phi (\times \pi)'}])
        
        # Run demo
        out = interactive_output(self.update, self.sliders)
        display(self.layout, out)
        
    def update(self, **kwargs):
        x1 = kwargs['A1']*cos(2*pi*self.t*kwargs['f1'] + kwargs['phi1']*pi)
        titleStr = '$x(t)='+str(kwargs['A1'])+f"\\cdot\\cos(2\\pi\\cdot {kwargs['f1']:.1f} \\cdot t +"+str(round(kwargs['phi1'],2))+"\\pi)$" # Plot-tittel
        titleStr = titleStr.replace("+-", "-")
        self.SineWave.ax.set_title(titleStr)
        self.SineWave.update([x1])