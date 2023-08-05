
import numpy as np
import matplotlib.pyplot as plt

def unwrap_phase(phase):
    for i in range(1,phase.size):
        #print i
        if np.abs(phase[i] - phase[i-1]) >= 179 :
            if phase[i] > 0:
                phase[i] -= 360
            else:
                phase[i] += 360
    return

def plotResponse(response, freqs, title, **kwargs):
    rad2deg = 180./np.pi
    amp  = np.abs(response)
    pha  = np.arctan2(response.imag, response.real) * rad2deg
    unwrap_phase(pha)

#defaults:
    xmin = 1e-5
    xmax = 40
    ymin = 1e2
    ymax = 1e10
    ymax = 1.1 * amp.max()
    ymin = amp.min()

    title_font_size = 12
    if kwargs is not None:
        for key, value in kwargs.items():
        #for key, value in kwargs.iteritems():
            if key == 'xmin':
                xmin = value
            elif key == 'xmax':
                xmax = value
            elif key == 'ymin':
                ymin = value
            elif key == 'ymax':
                ymax = value
            elif key == 'title_font_size':
                title_font_size = value


    # For this to work in general, need to test for high vs. low pass
    #  eg, if dB_max - dB_amp[0] < 1: probably have a low pass
    #  so need to count down from flat band to -3dB

    #dB_max = 20*np.log10(amp.max())
    #print("Max amp=%12.8g --> dB_max=%.2f" % (amp.max(), dB_max))
    #for i in range( len(freqs) ):
        #dB = 20*np.log10(amp[i])
        #if np.abs(dB_max - dB) <= 3:
            #print("Found corner frequency: f[%d]=%f" % (i, freqs[i]) )
            #break

    fig, axs = plt.subplots(nrows=2, ncols=1, sharex=False)

    ax = axs[0]
    ax.grid(True, which='major', axis='x', linewidth=0.75, ls='-', color='0.75')
    ax.grid(True, which='minor', axis='x', linewidth=0.75, ls='--', color='0.75')
    ax.grid(True, which='major', axis='y', linewidth=0.75, ls='-', color='0.75')
    ax.grid(True, which='minor', axis='y', linewidth=0.75, ls='--', color='0.75')

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])
    ax.set_ylabel('response amp')
    ax.plot(freqs, amp, 'g')

    ax.set_title(title, fontsize=title_font_size)
#
    ax = axs[1]
    ax.grid(True, which='major', axis='x', linewidth=0.75, ls='-', color='0.75')
    ax.grid(True, which='minor', axis='x', linewidth=0.75, ls='--', color='0.75')
    ax.grid(True, which='major', axis='y', linewidth=0.75, ls='-', color='0.75')
    ax.grid(True, which='minor', axis='y', linewidth=0.75, ls='--', color='0.75')

    ymin = -200
    ymax = 200

    ax.set_xscale('log')
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])
    ax.set_ylabel('response phase [deg]')
    ax.set_xlabel('Frequency [Hz]')
    ax.plot(freqs, pha, 'g')
#

    save = False
    if save:
        pdf        = PdfPages(outfile)
        pdf.savefig()
        pdf.close()

    else:
        plt.show()



def plotResponse2(response1, response2, freqs, title, **kwargs):

    rad2deg = 180./np.pi
    amp  = np.abs(response1)
    pha  = np.arctan2(response1.imag, response1.real) * rad2deg
#defaults:
    xmin = 1e-5
    xmax = 40
    ymin = 1e2
    ymax = 1e10
    ymax = 1.1 * amp.max()
    ymin = amp.min()

    if kwargs is not None:
        for key, value in kwargs.iteritems():
            if key == 'xmin':
                xmin = value
            elif key == 'xmax':
                xmax = value
            elif key == 'ymin':
                ymin = value
            elif key == 'ymax':
                ymax = value

    rad2deg = 180./np.pi
    amp1 = np.abs(response1)
    pha1 = np.arctan2(response1.imag, response1.real) * rad2deg
    amp2 = np.abs(response2)
    pha2 = np.arctan2(response2.imag, response2.real) * rad2deg

    #xmin = .0009
    #xmax = 20
    #ymin = .001
    #ymax = 10000

    fig, axs = plt.subplots(nrows=2, ncols=1, sharex=False)

    ax = axs[0]
    ax.grid(True, which='major', axis='x', linewidth=0.75, ls='-', color='0.75')
    ax.grid(True, which='minor', axis='x', linewidth=0.75, ls='--', color='0.75')
    ax.grid(True, which='major', axis='y', linewidth=0.75, ls='-', color='0.75')
    ax.grid(True, which='minor', axis='y', linewidth=0.75, ls='--', color='0.75')

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])
    ax.set_ylabel('response mod [dB V/Pa]')
    ax.plot(freqs, amp1, 'g')
    ax.plot(freqs, amp2, 'r')

    ax.set_title(title)
#
    ax = axs[1]
    ax.grid(True, which='major', axis='x', linewidth=0.75, ls='-', color='0.75')
    ax.grid(True, which='minor', axis='x', linewidth=0.75, ls='--', color='0.75')
    ax.grid(True, which='major', axis='y', linewidth=0.75, ls='-', color='0.75')
    ax.grid(True, which='minor', axis='y', linewidth=0.75, ls='--', color='0.75')

    ymin = -200
    ymax = 200

    ax.set_xscale('log')
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])
    ax.set_ylabel('response phase [deg]')
    ax.plot(freqs, pha1, 'g')
    ax.plot(freqs, pha2, 'r')
#

    save = False
    if save:
        pdf        = PdfPages(outfile)
        pdf.savefig()
        pdf.close()

    else:
        plt.show()

    return
