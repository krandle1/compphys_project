#Author: Kirsten Randle
#Take histograms and turn into plots

import ROOT
from array import array

dir = '/Users/kirstenrandle/CMS_work/compphysproj/data/'
digis_dir = dir + 'digis/'
infile = dir + 'analyzed_tree_1.root'

hf = ROOT.TFile.Open(infile)

avg_digis = ROOT.TH1F('avg_digis','Average digi values',10,-0.5,9.5)
avg_pileup_digis = ROOT.TH1F('avg_digis','Average digi values',10,-0.5,9.5)

for i in range(10):
    c = ROOT.TCanvas('c','c',600,800)
    digi = hf.Get('digis_{}'.format(i))
    digi.Draw('hist')
    c.SaveAs(digis_dir + 'digis_{}.png'.format(i))
    d = ROOT.TCanvas('d','d',600,800)
    p_digi = hf.Get('pileup_digis_{}'.format(i))
    p_digi.Draw('hist')
    d.SaveAs(digis_dir + 'pileup_digis_{}.png'.format(i))
    e = ROOT.TCanvas('e','e',600,800)
    n_digi = hf.Get('noise_digis_{}'.format(i))
    n_digi.Draw('hist')
    e.SaveAs(digis_dir + 'noise_digis_{}.png'.format(i))
    f = ROOT.TCanvas('f','f',600,800)
    s_digi = hf.Get('signal_digis_{}'.format(i))
    s_digi.Draw('hist')
    f.SaveAs(digis_dir + 'signal_digis_{}.png'.format(i))
    
    
