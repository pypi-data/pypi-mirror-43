from popsynth.auxiliary_sampler import AuxiliarySampler
import scipy.stats as stats
import numpy as np


class SynchPeakSampler(AuxiliarySampler):
    def __init__(self, B = 0.15):
        """
        Samples the Doppler factor and combines with 
        A magnetic fiels
        """

        self._B = B # in Gauss

        
        super(SynchPeakSampler, self).__init__('log_synch_peak', sigma=1., observed=False)

        
        self._distribution = stats.skewnorm(loc=2.75,scale=.7,a=5)

        self._log_prefactor = np.log10(3.2E6)
        self._log_B = np.log10(B)
        
        
    def true_sampler(self, size):

        log_gamma2 = 2*self._secondary_samplers['log_gamma_el']


        doppler_factor = stats.normal(loc= 15, scale=2, size=size)

        log_doppler_factor = np.log10(doppler_factor)

        # this is the log of the synchrotron peak for numerical stability
        
        self._true_values = self._log_prefactor + log_gamma2 + self._log_B + log_doppler_factor
