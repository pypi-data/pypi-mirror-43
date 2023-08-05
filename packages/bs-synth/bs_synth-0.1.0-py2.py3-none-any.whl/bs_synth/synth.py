import numpy as np

from popsynth.populations.cosmological_population import CosmologicalPopulation
from popsynth.populations.pareto_population import ParetoPopulation


class PowerLawZPopulation(CosmologicalPopulation):
    def __init__(self, r0, k=7, beta=-1.5, r_max=5, seed=1234, name="_pzcosmo"):

        CosmologicalPopulation.__init__(self, r_max, seed, name)

        self.set_spatial_distribution_params(r0=r0, k=k, beta=beta)

        self._spatial_form = r"\rho_0(1+z)^{k+\beta z}}"

    def dNdV(self, z):

        return self.r0 * np.power(1 + z, self.k + self.beta * z)

    def __get_r0(self):
        """Calculates the 'r0' property."""
        return self._spatial_params["r0"]

    def ___get_r0(self):
        """Indirect accessor for 'r0' property."""
        return self.__get_r0()

    def __set_r0(self, r0):
        """Sets the 'r0' property."""
        self.set_spatial_distribution_params(r0=r0, k=self.k, beta=self.beta)

    def ___set_r0(self, r0):
        """Indirect setter for 'r0' property."""
        self.__set_r0(r0)

    r0 = property(___get_r0, ___set_r0, doc="""Gets or sets the r0.""")

    def __get_k(self):
        """Calculates the 'k' property."""
        return self._spatial_params["k"]

    def ___get_k(self):
        """Indirect accessor for 'k' property."""
        return self.__get_k()

    def __set_k(self, k):
        """Sets the 'k' property."""
        self.set_spatial_distribution_params(r0=self.r0, k=k, beta=self.beta)

    def ___set_k(self, k):
        """Indirect setter for 'k' property."""
        self.__set_k(k)

    k = property(___get_k, ___set_k, doc="""Gets or sets the k.""")

    def __get_beta(self):
        """Calculates the 'beta' property."""
        return self._spatial_params["beta"]

    def ___get_beta(self):
        """Indirect accessor for 'beta' property."""
        return self.__get_beta()

    def __set_beta(self, beta):
        """Sets the 'beta' property."""
        self.set_spatial_distribution_params(r0=self.r0, k=self.k, beta=beta)

    def ___set_beta(self, beta):
        """Indirect setter for 'beta' property."""
        self.__set_beta(beta)

    beta = property(___get_beta, ___set_beta, doc="""Gets or sets the beta.""")


class BlazarPopulation(ParetoPopulation, PowerLawZPopulation):
    def __init__(self, r0, Lmin, alpha=3, k=7, beta=-1.5, r_max=5.0, seed=1235):
        """FIXME! briefly describe function

        :param r0: 
        :param Lmin: 
        :param alpha: 
        :param k: 
        :param beta: 
        :param r_max: 
        :param seed: 
        :returns: 
        :rtype: 

        """
        
        ParetoPopulation.__init__(
            self,
            Lmin=Lmin,
            alpha=alpha,
            r_max=r_max,
            seed=seed,
            name="BlazarPopulation",
        )

        PowerLawZPopulation.__init__(
            self, r0=r0, k=k, beta=beta, r_max=r_max, seed=seed, name="BlazarPopulation"
        )
