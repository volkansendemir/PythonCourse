import pandas as pd
import numpy as np
import pystan as ps
import matplotlib.pyplot as plt

church_df = pd.read_csv("C:/Users/vsendemir/Desktop/trend2.csv")

church_df = church_df.set_index(["country", "year"])

church_df = church_df.dropna()

#std_dict = {}

#for country in church_df.index.get_level_values("country").unique():
#    std_dict[country] = np.std(church_df["gini_net"][church_df.index.get_level_values("country") == country])

#for year in church_df.index.get_level_values("year").unique():
#    std_dict[year] = np.std(church_df["gini_net"][church_df.index.get_level_values("year") == year])


#church_df["std_country"] = np.array([std_dict[element] for element in church_df.index.get_level_values("country")])

#church_df["std_year"] = np.array([std_dict[element] for element in church_df.index.get_level_values("year")])

ch2 = np.array(church_df["church2"])
gini = np.array(church_df["gini_net"])
#std_country = np.array(church_df["std_country"])
#std_year = np.array(church_df["std_year"])


dummy_array = np.arange(1, (len(gini) + 1))

hierarchical_diffuse_model = """
data {
  int<lower=0> no_obs; 
  int<lower=1,upper=no_obs> dummy[no_obs];
  vector[no_obs] x;
  vector[no_obs] y;
} 
parameters {
  vector[no_obs] intc;
  vector[no_obs] slope;
  real mu_a;
  real mu_b;
  real<lower=0> sigma_intc;
  real<lower=0> sigma_slope;
  real<lower=0> sigma_y;
} 
transformed parameters {
  vector[no_obs] y_hat;
  for (i in 1:no_obs) {
    y_hat[i] = intc[dummy[i]] + x[i] * slope[dummy[i]];
  }
}
model {
  mu_a ~ normal(0, 1);
  mu_b ~ normal(0, 1);
  
  intc ~ normal(mu_a, sigma_intc);
  slope ~ normal(mu_a, sigma_slope);
  
  y ~ normal(y_hat, sigma_y);
}
"""

hierarchical_hi_model = """
data {
  int<lower=0> no_obs; 
  int<lower=1,upper=no_obs> dummy[no_obs];
  vector[no_obs] x;
  vector[no_obs] y;
} 
parameters {
  vector[no_obs] intc;
  vector[no_obs] slope;
  real mu_a;
  real mu_b;
  real<lower=0, upper=100> sigma_intc;
  real<lower=0, upper=100> sigma_slope;
  real<lower=0, upper=100> sigma_y;
} 
transformed parameters {
  vector[no_obs] y_hat;
  for (i in 1:no_obs) {
    y_hat[i] = intc[dummy[i]] + x[i] * slope[dummy[i]];
  }
}
model {
  mu_a ~ normal(0, 100);
  mu_b ~ normal(0, 100);

  intc ~ normal(mu_a, sigma_intc);
  slope ~ normal(mu_a, sigma_slope);

  y ~ normal(y_hat, sigma_y);
}
"""

hierarchical_data = {"no_obs": len(gini),
                          "dummy": dummy_array,
                          "x": ch2,
                          "y": gini}

hierarchical_diffuse_fit = ps.stan(model_code=hierarchical_diffuse_model, data=hierarchical_data,
                                         iter=1000, chains=4)


hierarchical_hi_fit = ps.stan(model_code=hierarchical_hi_model, data=hierarchical_data,
                                   iter=1000, chains=4)


diffuse_intc = pd.DataFrame(hierarchical_diffuse_fit["intc"])
diffuse_slope = pd.DataFrame(hierarchical_diffuse_fit["slope"])

hi_intc = pd.DataFrame(hierarchical_hi_fit["intc"])
hi_slope = pd.DataFrame(hierarchical_hi_fit["slope"])

diffuse_error = gini - (diffuse_intc.mean() + diffuse_slope.mean() * ch2)
hi_error = gini - (hi_intc.mean() + hi_slope.mean() * ch2)

plt.scatter(dummy_array, hi_error-diffuse_error)


#I suppose there is not much difference between my two models, both are bad at predicting gini.
#However, when we look at the differences of errors, the errors of the diffuse model seem to be larger at some instances, which suggests
#the highly informative model is performing better. I would infer that highly informative priors led to more accurate posteriors in this
#particular case.
