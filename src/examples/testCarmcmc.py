import sys, os
import yamcmcpp
import carmcmc
import numpy as np
import matplotlib.pyplot as plt

infile = sys.argv[1]
x, y, dy = np.loadtxt(sys.argv[1], unpack=True)

nSample = 25000
nBurnin = 5000
nThin = 1
nWalkers = 10
pModel = 4

logpost, params = carmcmc.run_mcmc(nSample, nBurnin, x, y, dy, pModel, nWalkers, nThin)
sample = carmcmc.CarSample(x, y, dy, logpost=logpost, trace=params)

#sample.autocorr_timescale(sample._samples["ar_coefs"])
sample.posterior_summaries("log_centroid")
#sample.plot_trace("ar_coefs")
#sample.plot_1dpdf("ar_coefs")
#sample.plot_autocorr("ar_coefs")
#sample.plot_2dpdf("log_centroid", 0, "log_centroid", 1)
#sample.plot_2dkde("ar_roots", 1, 2)
for i in range(pModel // 2):
    sample.plot_2dkde("log_centroid", i, "log_width", i, doShow=True)

# for i in range(pModel - 1):
#     sample.plot_2dpdf("ar_roots", i, "ar_roots", i + 1, doShow=True)
#     sample.plot_2dpdf("ar_coefs", i, "ar_coefs", i + 1, doShow=True)

# import pdb;

# pdb.set_trace()

sample.plot_power_spectrum(doShow=True)

print "Calculating interpolated values..."
sample.assess_fit()

print "Calculating forecasted and simulated lightcurve..."
tpredict = np.linspace(580.0, 640.0, 200)
tsim = tpredict
pmean, pvar = sample.predict_lightcurve(tpredict)
ysim = sample.simulate_lightcurve(tsim)
plt.fill_between(tpredict, pmean - np.sqrt(pvar), pmean + np.sqrt(pvar), alpha=0.25)
plt.plot(x, y, 'k.', label='Measured')
plt.plot(tsim, ysim, 'b-', label='Simulated 1')
ysim = sample.simulate_lightcurve(tsim)
plt.plot(tsim, ysim, 'r-', label='Simulated 2')
plt.xlim(tsim.min(), tsim.max())
plt.legend()
plt.show()

# kalman_filter(sample.time, sample.y - self.y.mean(), sample.dy,
#               sample._samples["var"][100], sample._samples["ar_roots"][100])
#
# kmean, kvar = carmcmc.kalman_filter(sample.time, sample.y - sample.y.mean(), sample.ysig ** 2,
#                                     sample._samples["var"][100], sample._samples["ar_roots"][100])
# chi2 = (sample.y - sample.y.mean() - kmean) ** 2 / kvar
# print -0.5 * np.sum(chi2)
# plt.errorbar(sample.time, sample.y, yerr=sample.ysig, fmt="ro")
# plt.plot(sample.time, kmean, "k-")