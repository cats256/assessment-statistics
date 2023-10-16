from bqme.distributions import Normal, Gamma
from bqme.models import NormalQM

N, q, X = 100, [0.25, 0.5, 0.75], [-0.1, 0.3, 0.8]

# define priors
mu = Normal(0, 1, name="mu")
sigma = Gamma(1, 1, name="sigma")

# define likelihood
model = NormalQM(mu, sigma)

# sample the posterior
fit = model.sampling(N, q, X)

# extract posterior samples
mu_posterior = fit.mu
sigma_posterior = fit.sigma

# get stan sample object
stan_samples = fit.stan_obj

# get pdf and cdf of x_new
x_new = 1.0
pdf_x = fit.pdf(x_new)
cdf_x = fit.cdf(x_new)

# get percent point function of q_new (inverse of cdf)
# default return values are samples from posterior predictive p(x|q)
q_new = 0.2
ppf_q = fit.ppf(q_new)
