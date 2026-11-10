# AIS2201 – Digital Signal Processing: Lecture Notes

Lecture notes for the course [AIS2201 – Digital Signal Processing](https://www.ntnu.edu/studies/courses/AIS2201) at NTNU, written as Jupyter notebooks.

The notes lean heavily on computational examples, interactive demos and illustrations in Python, so that the theory is both approachable and directly connected to how it is applied. Each sub-chapter is meant to fit *roughly* into one 45-minute lecture. The notebooks double as [RISE](https://rise.readthedocs.io/) slideshows and are used as the actual presentation material in class.

> **Note:** The notes are updated continuously during the semester. Notebooks for upcoming lectures may be incomplete or subject to change.

**Start here: [`index.ipynb`](index.ipynb)** – the table of contents, with links to every lecture in course order.

## Contents

| Chapter | Folder |
|---|---|
| 1. Introduction | [`introduction/`](introduction/) |
| 2. Signals in the time and frequency domain | [`continuous_signals/`](continuous_signals/) |
| 3. Analog-to-digital conversion | [`sampling_and_aliasing/`](sampling_and_aliasing/) |
| 4. The Discrete Fourier Transform (DFT) | [`discrete_fourier_transform/`](discrete_fourier_transform/) |
| 5. Discrete-time filtering | [`digital_filters/`](digital_filters/) |
| 6. Sample rate conversion | [`sample_rate_conversion/`](sample_rate_conversion/) |
| 7. Advanced topics (teasers) | [`advanced_topics/`](advanced_topics/) |
| Appendix: embedded programming (STM32) and legacy material | [`appendix/`](appendix/) |

## Getting started

1. Clone the repository:
   ```bash
   git clone https://github.com/kaierih/AIS2201-Lecture_Notes.git
   ```
2. Install the Python packages (Python 3.10 or newer is recommended):
   ```bash
   pip install numpy scipy matplotlib ipywidgets ipympl jupyterlab
   ```
3. Open `index.ipynb` in **VS Code** (with the Jupyter extension) or **JupyterLab**, and pick a lecture.

Many notebooks contain interactive demos built with `ipywidgets` and the `%matplotlib ipympl` backend. Run the notebook cells in order, starting with the import cell at the top.

## Repository layout

```
AIS2201-Lecture_Notes/
├── index.ipynb               # Table of contents – start here
├── equations.ipynb           # Collection of key equations
├── symbols_notations.ipynb   # Symbols and notation used throughout
├── <chapter>/                # One folder per chapter
│   ├── *.ipynb               # Lecture notebooks
│   ├── figures/              # Figures + the notebook that generates them
│   └── rise.css              # Slideshow styling (some chapters)
├── demos/                    # Python package with the interactive widget demos
├── data/                     # Shared audio, ECG and vibration datasets
└── latex/                    # Shared TikZ style for figure generation
```

The lecture notebooks import the interactive demos from the top-level `demos` package (e.g. `from demos import ConvolutionDemo`).

## Regenerating figures (for maintainers)

The figures in each chapter's `figures/` folder are made with [jupyter-tikz](https://github.com/lucaslrodri/jupyter-tikz) and matplotlib, by the `generate_*.ipynb` notebook in the same folder. Students never need to do this; the generated SVG/PNG files are committed.

Requirements:
- A LaTeX distribution with `pdflatex` on the `PATH` ([MiKTeX](https://miktex.org/) or [TeX Live](https://tug.org/texlive/)). It must include `tikz`, `pgfplots` and `circuitikz`.
- A tool for PDF → SVG/PNG conversion as required by jupyter-tikz (see its documentation).
- `pip install jupyter-tikz`

All chapters share one TikZ style, [`latex/ss2-figures.sty`](latex/ss2-figures.sty), along with [`latex/prefix.tex`](latex/prefix.tex). The first cell of each `generate_*.ipynb` points LaTeX at this folder by setting `TEXINPUTS`, so the figure cells only need:

```
%%tikz -p=\input{prefix.tex} -sc=2 -S my_figure.svg
\begin{tikzpicture}
  ...
\end{tikzpicture}
```

Figures get a **white background by default** so they stay readable in dark editor themes (e.g. VS Code's default dark theme). Use `\usepackage[transparent]{ss2-figures}` to turn this off. Add any new shared styles to `latex/ss2-figures.sty` instead of making per-chapter copies.

## Acknowledgements

The structure and parts of the material are inspired by the excellent open lecture notes [*Digital Signal Processing – Lecture Notes*](https://github.com/spatialaudio/digital-signal-processing-lecture) by Sascha Spors (University of Rostock). The shared TikZ style is also based on material from there.

## License

*To be decided.*
