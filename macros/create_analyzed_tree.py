#Author: Kirsten Randle
#Take data and turn into histograms

import ROOT
from array import array

# define file directories and locations
in_dir = '../data/'
out_dir = '../outputs/'

file_1 = 'Timing_bias_rings_etr28_PU50_S1.99_2.01.root'
file_2 = 'Timing_samplesandweights.root'

#open files and load tree
df1 = ROOT.TFile.Open(file_1)
df2 = ROOT.TFile.Open(file_2)

bt1 = df1.Get('Bias')
bt2 = df2.Get('samples')

#define cuts
bx15cut = "BX0==15"

"""
1D histograms, a list of [hname,title,[nxbins, xlow, xhigh],parameter,cuts]
"""
#file 1 associated histograms
reco_list = [['bias_1','Reconstucted Amplitude Bias',[80,-2,2],'bias_1',bx15cut],['recoA_1','Reconstructed Amplitude from Amplitude Weights',[520,-100,160],'recoA_1',bx15cut],['recoA_2','Reconstructed Amplitude from Timing Weights',[220,-50,60],'recoA_2',bx15cut]]

#file 2 associated histograms
weights_list = [['w_1_{}'.format(i),'Amplitude Weight {}'.format{i},[400,-2.0,2.0],'w_1_{}'.format(i),bx15cut] for i in range(5)]+[['w_2_{}'.format(i),'Timing Weight {}'.format{i},[400,-2.0,2.0],'w_2_{}'.format(i),bx15cut] for i in range(5)]
digis_list = [['digis_{}'.format(i),'Total digis[{}]'.format(i),[800,-10,70],'digis[{}]'.format(i),bx15cut] for i in range(10)] + [['pileup_digis_{}'.format(i),'Pileup digis[{}]'.format(i),[800,-10,70],'pileup_digis[{}]'.format(i),bx15cut] for i in range(10)] + [['noise_digis_{}'.format(i),'Noise digis[{}]'.format(i),[800,-10,70],'noise_digis[{}]'.format(i),bx15cut] for i in range(10)]+ [['signal_digis_{}'.format(i),'Signal digis[{}]'.format(i),[800,-10,70],'signal_digis[{}]'.format(i),bx15cut] for i in range(10)]

"""
2D histograms, a list of [hname, title, [[nxbins, xlow, xhigh],[nybins, ylow, yhigh]],[x parameter, y parameter],cuts]
"""
weights_compare_list = [['w_{}_compare'.format(i),'Timing weights vs. amplitude weights',[[400,-2.0,2.0],[400,-2.0,2.0]],['w_1_{}'.format(i),'w_2_{}'.format(i)],bx15cut] for i in range(5)]
recoa_compare_list = [['recoAvs','Comparison of Reconstructed Amplitudes',[[520,-100,160],[220,-50,60]],['recoA_1','recoA_2'],bx15cut],['recoA2vsb1','Comparison of Timing recoA and Bias of Amplitude recoA ',[[80,-2,2],[220,-50,60]],['bias_1','recoA_2'],bx15cut]]

"""
Define functions for plotting, iteratively if needed
"""

def create_1Dhisto(tree_,hname_,title_,binparams_,parameter_,cuts_):
    h = ROOT.TH1F(hname_,title_,binparams_[0],binparams_[1],binparams_[2])
    h.GetXaxis().SetTitle(parameter_)
    h.GetYaxis().SetTitle('Entries')
    drawstatement = parameter_ + ' >> ' + hname_
    tree_.Draw(drawstatement,cuts,'hist')
    h.SetDirectory(0)
    return h

def create_2Dhisto(tree_,hname_,title_,binparams_,paramters_,cuts_):
    h = ROOT.TH2F(hname_,title_,binparams_[0][0],binparams_[0][1],binparams_[0][2],binparams_[1][0],binparams_[1][1],binparams_[1][2])
    h.GetXaxis().SetTitle(parameters_[0])
    h.GetYaxis().SetTitle(parameters_[1])
    drawstatement = paramters_[1] + ':' + parameters_[0] + ' >> ' + hname_
    tree_.Draw(drawstatement,cuts,'COLZ1')
    h.SetDirectory(0)
    return h

def slicefity(histo_,func_,slicebins_,options_)
    fitparams = ROOT.TObjArray()
    histo.FitSlicesY(func_,slicebins_[0],slicebins_[1],slicebins_[2],options_,fitparams)
    return fitparams

def iterate_curves(tree_,curvelist_,type_):
    list = [0 for i in range(len(curvelist))]
    for i,p in enumerate(curvelist):
        if type = 'TH1F':
            list[i] = create_1Dhisto(tree_,p[0],p[1],p[2],p[3],p[4])
        if type = 'TH2F':
            list[i] = create_2Dhisto(tree_,p[0],p[1],p[2],p[3],p[4])
            

