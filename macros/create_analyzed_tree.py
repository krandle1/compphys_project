#Author: Kirsten Randle
#Take data and turn into histograms

import ROOT

# define file directories and locations
in_dir = '/Users/kirstenrandle/CMS_work/compphysproj/data/'
out_dir = '/Users/kirstenrandle/CMS_work/compphysproj/outputs/'

file_1 = in_dir + 'Timing_bias_rings_etr28_PU50_S1.99_2.01.root'
file_2 = in_dir + 'Timing_samplesandweights.root'

out_file = out_dir + 'analyzed_tree.root'

#open files and load tree
df1 = ROOT.TFile.Open(file_1)
df2 = ROOT.TFile.Open(file_2)

bt1 = df1.Get('bias')
bt2 = df2.Get('samples')

#define cuts
bx15cut = "BX0==15"

"""
1D histograms, a list of [hname,title,[nxbins, xlow, xhigh],parameter,cuts]
"""
#file 1 associated histograms
reco_list = [['bias_1','Reconstucted Amplitude Bias',[80,-2,2],'bias_1',bx15cut],['recoA_1','Reconstructed Amplitude from Amplitude Weights',[520,-100,160],'recoA_1',bx15cut],['recoA_2','Reconstructed Amplitude from Timing Weights',[220,-50,60],'recoA_2',bx15cut]]

#file 2 associated histograms
weights_list = [['w_1_{}'.format(i),'Amplitude Weight {}'.format(i),[400,-2.0,2.0],'w_1_{}'.format(i),bx15cut] for i in range(5)]+[['w_2_{}'.format(i),'Timing Weight {}'.format(i),[400,-2.0,2.0],'w_2_{}'.format(i),bx15cut] for i in range(5)]
digis_list = [['digis_{}'.format(i),'Total digis[{}]'.format(i),[800,-10,70],'digis[{}]'.format(i),bx15cut] for i in range(10)] + [['pileup_digis_{}'.format(i),'Pileup digis[{}]'.format(i),[800,-10,70],'pileup_digis[{}]'.format(i),bx15cut] for i in range(10)] + [['noise_digis_{}'.format(i),'Noise digis[{}]'.format(i),[800,-10,70],'noise_digis[{}]'.format(i),bx15cut] for i in range(10)]+ [['signal_digis_{}'.format(i),'Signal digis[{}]'.format(i),[800,-10,70],'signal_digis[{}]'.format(i),bx15cut] for i in range(10)]

"""
2D histograms, a list of [hname, title, [[nxbins, xlow, xhigh],[nybins, ylow, yhigh]],[x parameter, y parameter],cuts]
"""
#file 1
recoa_compare_list = [['recoA_2_vs_recoA_1','Comparison of Reconstructed Amplitudes',[[520,-100,160],[220,-50,60]],['recoA_1','recoA_2'],bx15cut],['recoA_2_vs_bias_1','Comparison of Timing recoA and Bias of Amplitude recoA ',[[80,-2,2],[220,-50,60]],['bias_1','recoA_2'],bx15cut]]
#file 2
weights_compare_list = [['w_{}_compare'.format(i),'Timing weight vs. amplitude weight [{}]'.format(i),[[400,-2.0,2.0],[400,-2.0,2.0]],['w_1_{}'.format(i),'w_2_{}'.format(i)],bx15cut] for i in range(5)]


"""
Define functions for plotting, iteratively if needed
"""
ROOT.gROOT.SetBatch(1) #don't output on Draw function

#Use root to create a 1-D histogram from parameters set above
def create_1Dhisto(tree_,hname_,title_,binparams_,parameter_,cuts_):
    h = ROOT.TH1F(hname_,title_,binparams_[0],binparams_[1],binparams_[2])
    h.GetXaxis().SetTitle(parameter_)
    h.GetYaxis().SetTitle('Entries')
    drawstatement = parameter_ + ' >> ' + hname_
    tree_.Draw(drawstatement,cuts_,'hist')
    h.SetDirectory(0)
    return h

#Use root to create a 2-D histogram from parameters set above
def create_2Dhisto(tree_,hname_,title_,binparams_,parameters_,cuts_):
    h = ROOT.TH2F(hname_,title_,binparams_[0][0],binparams_[0][1],binparams_[0][2],binparams_[1][0],binparams_[1][1],binparams_[1][2])
    h.GetXaxis().SetTitle(parameters_[0])
    h.GetYaxis().SetTitle(parameters_[1])
    drawstatement = parameters_[1] + ':' + parameters_[0] + ' >> ' + hname_
    tree_.Draw(drawstatement,cuts_,'COLZ1')
    h.SetDirectory(0)
    return h

class HistogramWrongDimensions(Exception):
    pass

def means_of_several(hlist_,hname_,title_):
    nbins = len(hlist_)
    lowbin = -0.5
    highbin = lowbin+nbins
    newhist = ROOT.TH1F(hname_,title_,nbins,lowbin,highbin)
    for i,h in enumerate(hlist_):
        if h.ClassName() != 'TH1F':
            print('means_of_several only works with 1-D histograms at the moment')
            raise HistogramWrongDimensions
        else:
            newhist.SetBinContent(i+1,h.GetMean())
            newhist.SetBinError(i+1,h.GetStdDev())
    newhist.SetDirectory(0)
    return newhist
            
#take vertical slices and fit each with a gaussian and report mean and stdev
def slicefity(histo_,func_,slicebins_,options_):
    #slicebins are xlow,xhigh,nbins
    fitparams = ROOT.TObjArray()
    histo_.FitSlicesY(func_,slicebins_[0],slicebins_[1],slicebins_[2],options_,fitparams)
    return fitparams

#use list of inputs to create many histograms
def iterate_curves(tree_,curvelist_,type_):
    list = [0 for i in range(len(curvelist_))]
    for i,p in enumerate(curvelist_):
        if type_ == 'TH1F':
            list[i] = create_1Dhisto(tree_,p[0],p[1],p[2],p[3],p[4])
        if type_ == 'TH2F':
            list[i]= [create_2Dhisto(tree_,p[0],p[1],p[2],p[3],p[4])]
            fp = slicefity(list[i][0],0,[0,-1,0],'Q') #for every 2D histo report stats for slices
            list[i]+= [fp.At(1)]
            list[i]+= [fp.At(2)]
    return list



#create all the histograms specified above
reco_histos = iterate_curves(bt1,reco_list,'TH1F')
digis_histos = iterate_curves(bt2,digis_list,'TH1F')
avg_digis = means_of_several(digis_histos[:10],'avg_digis','Average Total Digis Values')
avg_p_digis = means_of_several(digis_histos[10:20],'avg_pileup_digis','Average Pileup Digis Values')
avg_n_digis = means_of_several(digis_histos[20:30],'avg_noise_digis','Average Noise Digis Values')
avg_s_digis = means_of_several(digis_histos[30:40],'avg_signal_digis','Average Signal Digis Values')
weights_histos = iterate_curves(bt2,weights_list,'TH1F')
avg_weights_1 = means_of_several(weights_histos[:5],'avg_weights_1','Average Amplitude Weights')
avg_weights_2 = means_of_several(weights_histos[5:],'avg_weights_2','Average Timing Weights')
weights_compare_histos = iterate_curves(bt2,weights_compare_list,'TH2F')
recoa_compare_histos = iterate_curves(bt1,recoa_compare_list,'TH2F')

#write all the histograms to a root tree for later processing
of = ROOT.TFile(out_file,'RECREATE')
for h in reco_histos:
    h.Write()
for h in digis_histos:
    h.Write()
for h in weights_histos:
    h.Write()

for l in weights_compare_histos: #save regular 2D histogram and statistics
    for h in l:
        h.Write()

for l in recoa_compare_histos:
    for h in l:
        h.Write()
avg_digis.Write()
avg_p_digis.Write()
avg_n_digis.Write()
avg_s_digis.Write()
avg_weights_1.Write()
avg_weights_2.Write()

of.Close()
