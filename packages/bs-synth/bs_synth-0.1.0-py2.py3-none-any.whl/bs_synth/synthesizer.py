import numpy as np

from bs_synth.electron_sampler import ElectronSampler
from bs_synth.synch_peak_sampler import SynchPeakSampler
from bs_synth.blazar_sampler import BlazarPopulation


class BSSynthesizer(object):
    def __init__(self, r0, Lmin, alpha=3, beta=-1.5, k=7.0, r_max=5.0, B=0.015):

        base_sampler = BlazarPopulation(
            r0=r0, Lmin=Lmin, alpha=alpha, beta=beta, k=k, r_max=r_max
        )

        electron_sampler = ElectronSampler()

        peak_sampler = SynchPeakSampler(B=B)

        peak_sampler.set_secondary_sampler(electron_sampler)

        base_sampler.add_observed_quantity(peak_sampler)


        self._base_sampler = base_sampler


    @property
    def population_gen(self):

        return self._base_sampler
    
