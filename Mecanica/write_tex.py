content = r'''\documentclass[prl,a4paper,amsmath]{revtex4}
\usepackage[english]{babel}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{epsfig}
\usepackage{color}
\usepackage{datetime}
\usepackage{booktabs}
\usepackage{siunitx}
\usepackage{float}
\bibliographystyle{apsrev}
\addbibresource{biblio.bib}


\begin{document}
\title{Coupled Oscillations: Analysis of Symmetric and Asymmetric Modes}
\author{Laboratory Group}

\begin{abstract}
This experiment investigated the vibrational modes of a coupled oscillatory system consisting of a rigid bar and two springs. By measuring the displacement amplitude as a function of driving frequency, we identified the system's normal modes. The natural frequency, symmetric mode, and asymmetric mode frequencies were extracted from frequency response spectra. Complex motion analysis revealed the superposition of these modes, confirming the theoretical physics of linearly coupled oscillators.
\end{abstract}


\maketitle


\section{Introduction and Objectives}

\subsection{Theoretical Background}

Coupled oscillatory systems are ubiquitous in physics and engineering. When two or more oscillators interact, energy can be exchanged between them, leading to the emergence of collective vibrational modes.

For a system of two identical coupled oscillators, the equations of motion are:

\begin{equation}\label{eq:coupled_oscillators}
m\ddot{z}_1 + kz_1 + k'(z_1 - z_2) = 0
\end{equation}

\begin{equation}\label{eq:coupled_oscillators_2}
m\ddot{z}_2 + kz_2 + k'(z_2 - z_1) = 0
\end{equation}

where $ is the mass, $ is the individual restoring constant, '$ is the coupling constant, and , z_2$ are the displacements from equilibrium.

The system exhibits two characteristic frequencies: the symmetric mode (where both oscillators move in phase) and the asymmetric mode (where they move out of phase). These normal modes are related to the individual oscillator frequency $\omega_0 = \sqrt{k/m}$ and the coupling by:

\begin{equation}\label{eq:symmetric_mode}
\omega_s = \sqrt{\frac{k}{m}} = \omega_0
\end{equation}

\begin{equation}\label{eq:asymmetric_mode}
\omega_a = \sqrt{\frac{k + 2k'}{m}}
\end{equation}

\subsection{Experimental Objectives}

This experiment aims to:
\begin{itemize}
\item Measure the natural frequency $\omega_0$ of the coupled oscillator system
\item Determine the symmetric mode frequency $\omega_s$ through frequency sweep analysis
\item Determine the asymmetric mode frequency $\omega_a$ through frequency sweep analysis
\item Characterize the coupling strength from the frequency separation
\item Compare experimental results with theoretical predictions
\end{itemize}

\subsection{Measurement Methodology}

The system is characterized by measuring its frequency response across a range of driving frequencies. Resonance peaks in the amplitude spectrum indicate the natural vibrational modes of the system. Measurements are performed on both the left and right oscillators to capture the symmetric and asymmetric mode behavior.

\section{Materials and Methods}

\subsection{Experimental Setup}

The coupled oscillator system consists of two identical mechanical oscillators connected by a coupling spring. Each oscillator is characterized by its mass $ and individual spring constant $. The coupling spring provides the interaction force quantified by the coupling constant '$.

The system is driven by an external oscillating force that sweeps through a range of frequencies. A sensor measures the displacement amplitude of each oscillator as a function of driving frequency, producing frequency response spectra.

\subsection{Data Acquisition and Analysis}

Frequency sweeps are performed on three sides of the system (center reference and left/right positions) to capture the full vibrational response. Measurements are conducted across frequencies from approximately .02$ \unit{Hz} to .15$ \unit{Hz}. 

For each measurement sweep, the frequency corresponding to the maximum amplitude is identified as a resonance frequency. Multiple sweeps are performed to establish average values and assess measurement variability. The frequency measurements are converted to angular frequencies by the relation $\omega = 2\pi f$.

The natural frequency $\omega_0$ is determined from the center reference position, while the symmetric and asymmetric mode frequencies are extracted from measurements on the left and right oscillators. Standard deviation across multiple measurements provides the uncertainty for each frequency value.

\section{Results and Data Analysis}

\subsection{Measured Frequencies}

The frequency response analysis yielded three characteristic frequencies for the coupled oscillator system. Table~\ref{tab:frequencies} presents the measured angular frequencies with their corresponding uncertainties. These values were determined by averaging multiple measurements across different positions on the system.

\begin{table}[H]
\centering
\begin{tabular}{lcc}
\toprule
\textbf{Mode} & \textbf{Angular Frequency (\unit{rad/s})} & \textbf{Description} \\
\midrule
Natural ($\omega_0$) & .84 \pm 0.13$ & Center reference oscillator \\
Symmetric ($\omega_s$) & .72 \pm 0.02$ & Both oscillators in phase \\
Asymmetric ($\omega_a$) & .80 \pm 0.02$ & Oscillators out of phase \\
\bottomrule
\end{tabular}
\caption{Measured angular frequencies for the three characteristic vibrational modes of the coupled oscillator system. Uncertainties represent standard deviation across multiple frequency sweeps and individual transmitter measurements.}
\label{tab:frequencies}
\end{table}

\subsection{Mode Superposition}
When a single end of the bar was displaced while the other remained at rest, the resulting complex motion displayed interference (beating). The complex motion was analyzed to find its component frequencies, $\omega_{min}$ and $\omega_{max}$.

\begin{table}[H]
\centering
\begin{tabular}{lcc}
\toprule
\textbf{Mode} & \textbf{Angular Frequency (\unit{rad/s})} & \textbf{Description} \\
\midrule
Minimum ($\omega_{min}$) & .85 \pm 0.02$ & Superposition slow mode \\
Maximum ($\omega_{max}$) & .87 \pm 0.02$ & Superposition fast mode \\
\bottomrule
\end{tabular}
\caption{Extracted angular frequencies from the complex superposed motion. Uncertainties are estimated from spectral resolution (1-2 sentences explaining uncertainty).}
\label{tab:superposition_frequencies}
\end{table}

% [FIGURE: Insert frequency response plots showing resonance peaks and the beating pattern of the superposed motion]

\section{Discussion and Conclusions}

% [TODO: Human investigator must complete the discussion on the relationship between \omega_s, \omega_a, \omega_{min}, \omega_{max}, and \omega_0]
% [TODO: Discuss the proportions between the frequencies according to theoretical equations (3) and (4)]

\bibliographystyle{apsrev}

\bibliography{biblio}

\end{document}
'''
with open('C:/Users/Andres/Practicas-Fisica/Mecanica/m3bis/Template.tex', 'w', encoding='utf-8') as f:
    f.write(content)
