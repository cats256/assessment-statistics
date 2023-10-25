## https://cats256.github.io/assessment-statistics/build/

Have you ever wondered how to visualize a grade distribution given only their quantiles (lower quartile, median, upper quartile)? Or how well you actually perform on your exam relative to your classmates? Then this page is perfect for you.

The original Python and R files used for estimating the logit-normal parameters are in the original folder. However, they are not the most updated so please take a look at the server.py and production.py in assessment-statistics/flask-server folder for more updated and readable code.

Below is a general explanation for my method and my justifications for them

Note: Just a warning that since I don't have that much of a background in statistics, my explanations may be oversimplified / inaccurate so please excuse any of my mistake and let me know XD. Also I'm not that good at explaining so please feel free to hit me up at nhatbui@tamu.edu

## Questions and Answers:

### What is the method of estimating the grade distribution?

I first calculate the logit-transform of the observed values / grade scale (logit_transform_observations = logit(observed_values / scale) where each observed value is a grade such as 66, 80, and 89 and the scale can be a 100). Then, I calculate the standard normal quantile of the cumulative probabilities (standard_norm_quantiles = norm.ppf(probs, 0, 1) where each cumulative probabillity is a value such as 0.25, 0.50, and 0.75). After all the transformations are done, I simply fit a weighted linear regression (obligatory it's all linear regression meme https://biol607.github.io/2020/lectures/t_as_lm.html#1) of logit-transformed-observations against standardard-norm-quantiles to get mu and sigma, where mu is the intercept and sigma is the slope of the logit-normal distribution, which is the assumed distribution of the grade distribution. The weight is calculated through 1 / raw sample quantile variance where raw sample quantile variance = p (1 - p) / norm.pdf(norm.ppf(p))**2. Then, all I had to do is to scale the estimated logit-normal distribution to the correct range (since the logit-normal support is x ∈ (0, 1) while grade distribution support can be any arbitrary range).

### Why is grade distribution assumed to follow a scaled logit-normal distribution?

Short-answer: The scaled logit-normal has been shown to be one of, if not, the best fit to exam distribution according to Stanford Computer Science and GradeScope researchers (https://files.eric.ed.gov/fulltext/ED599204.pdf). It outperforms the normal, truncated normal, and beta distribution with regard to fitting grade distribution. The scaled logit-normal is bounded, allows for skewness, and takes into account diminishing returns. It being the underlying distribution of grade distribution also matches up with item response theory, further giving justification to its usage.

Long answer:
There are many distributions that may come to mind when people think about the supposed distribution of grades. The most commonly being the normal. However, the normal is unbounded, range [-infinity, infinity], while grades are bounded, range [min_possible_score, max_possible_score]. One must then narrow down to bounded distributions, some of which are the truncated normal, the beta distribution, the binomial distribution, continuous analog of the binomial, and the logit-normal. The truncated normal is, then, eliminated due to its lack of skewness, whereas grade distribution is often skewed and asymmetric. The binomial is also eliminated due to its discrete nature, which lacks flexibillity. This left us with the beta distribution, the continuous analog of the binomial, and the logit-normal. The logit-normal, reasoning wise, is the best among the three considering that it is characterized by the logistic function, which takes into account diminishing return. This is reinforced by a research paper from Stanford Computer Science, in collaboration with GradeScope, [insert link] showing that the logit-normal outperforms the normal, truncated normal, and beta distribution. Anecdotally, I have also tested the logit-normal against the distributions mentioned including the continuous binomial analog, and found that is it the superior distribution in terms of goodness of fit.

Intuitively, one can think of students' abilities distribution as an approximate normal distribution but with range from [0, infinity], where it is converted into the grade distribution through an unknown function. This function takes into account diminishing return (think about the amount of effort it would take to go from a 50 to a 70 on exam, as opposed to from a 70 to a 90) and compresses an infinite range [0, infinity] into a bounded range [min_possible_score, max_possible_score]. The logistic function, similarly, also represents a function characterized by diminishing return and transform an infinite range into a bounded range, albeit from [-infinity, infinity] to [0, 1]. One can intuitively understand and see the similarity between the grade distribution and the logit-normal distribution, which arises from applying the logistic function (resembling the unknown function characterized by diminishing returns and bounded range) onto a normal distribution (resembling the students' abilities distribution).

### Why weighted least squares over ordinary least squares?

Weighted least squares is done to combat combat heteroskedasticity since sample quantile variance depends on the quantile examined, which is asymptotically normal around the p-th population quantile with variance equal to p * (1 - p) / (N * norm.pdf(norm.ppf(p))^2), where N is the sample size (https://www.math.mcgill.ca/~dstephens/OldCourses/556-2006/Math556-Median.pdf). The weight is calculated through doing 1 / raw_variance, where raw variance is simply sample quantile variance calculated without the sample size, N. Weight is 1 / variance since b is proven to to be the best linear unbiased estimator when weighted sum of residuals is minimized, where weight is equal to the reciprocal of the variance of the measurement. 

### Why least squares instead of maximum likelihood estimation?

Weighted least squares and MLE as I interpret it in this specific case should produce the same result (too lazy to show proof XD so you will have to take me at my face value). Although, least squares tend to produce slightly better result experimentally, perhaps, due to numerical instabillity and floating point error associated with doing log-likelihood optimization.

### Why transform the grades into the normal distribution for weighted least squares instead of just doing it on the original data? And what's logic behind estimating mu and sigma using weighted linear regression on standard normal quantile of the cumulative probabilities?

The loss function associated with doing least squares quantile matching estimation on grades, or just simply the logit-normal is not exactly convex, while least squares on the normal distribution is smoother and convex (I don't have a proof, I simply plotted the loss function so you will have to take me at my face value again XD). The sample quantile variance associated with the normal distribution is also more homogenous and normal (lol) than the logit-normal, which means the estimated parameter will also be more efficient doing least squares QME on data transformed to the normal as opposed to the logit-normal (again, i don't have proof but this should be the case if you run a simulation). As for the logic behind doing weighted linear regression, you may notice that the quantile function for the normal distribution is simply mu + sigma * sqrt(2) * erfinv(2p - 1) and the loss function is defined as sum from 1 to n (logit_transformed_observations - predicted_quantile_values)^2 = sum from 1 to n (logit_transformed_observations - mu + sigma * sqrt(2) * erfinv(2p - 1))^2. These functions are suspiciously similar to a linear model, yi = b0 + b1xi and its loss function, sum from 1 to n (yi - (b0 + b1xi))^2. And indeed they are! To get to the linear model, you will have to linearize the the data by calculating standard_normal_quantiles = sqrt(2) * erfinv(2 * cumulative_probabilities - 1). You may notice that sqrt(2) * erfinv(2 * cumulative_probabilities - 1) is the standard normal quantile function. Hence, why I call the linearized variable standard_normal_quantiles. This will give us the equation Q(p) = mu + sigma * standard_normal_quantiles, where mu is the intercept, sigma is the slope, and xi is the standard_normal_quantiles! And now all you have to do is do a weighted linear regression of the logit_transformed_observations against standard_normal_quantiles to get mu and sigma.

## To do:
Refactor code
Add collapsible FAQ part
Add examples of how well this fits
Promote the site
Add source code link
Add predicted quantiles
Add contact page
Add hover over to see more description abillity

Probably don't do:
Do leave one out cross validation

Done:
Add citations
