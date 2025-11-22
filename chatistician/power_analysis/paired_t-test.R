library(optparse)
library(MASS)

optlist = list(
    make_option('-n', type='integer', help='Sample size'),
    make_option('--type-1', type='numeric', default=0.05, help='Type 1 error / significance threshold'),
    make_option('--variance-pre', type='numeric', default=1, help='Variance in pre-treatment condition'),
    make_option('--variance-post', type='numeric', default=1, help='Variance in post-treatment condition'),
    make_option('--correlation', type='numeric', default=0.5, help='Correlation between paired observations'),
    make_option('--number-simulations', type='integer', default=10000, help='Number of simulation replicates')
)

opts = parse_args(OptionParser(option_list=optlist))

# simpler names
k = opts$`number-simulations`
ds = c(0.1, 0.3, 0.5, 0.7, 0.9)
alpha = opts$`type-1`
n = opts$n
variance_pre = opts$`variance-pre`
variance_post = opts$`variance-post`
rho = opts$correlation
D = diag(sqrt(c(variance_pre, variance_post)))
R = matrix(c(1, rho, rho, 1), 2, 2)
Sigma = D %*% R %*% D

l = 40
results = c()
for(i in 1:length(ds)) {
    r = c()
    for(iter in 1:k) {
        setTxtProgressBar(pb, s)
        # draw raw data
        X = MASS::mvrnorm(n, c(0, ds[i]), Sigma)
        fit = t.test(X[,1], X[,2], paired=TRUE)
        r[iter] = fit$p.value < alpha
    }
    results[i] = mean(r)
}

# clean results
pad_message=function(message, l) {
    pad = l - nchar(message) - 3
    cat('| ', message, rep(' ', pad), '|\n', sep='')
}
l = 40
cat('\n')
cat('|', rep('=', l - 2), '|\n', sep='')
pad_message('Paired samples T-test power analysis', l)
cat('|', rep('=', l - 2), '|\n', sep='')
pad_message(paste0('Sample size = ', n), l)
pad_message(paste0('Pre/post variances = ', variance_pre, ', ', variance_post), l)
pad_message(paste0('Significance threshold = ', alpha), l)
cat('|', rep('-', l - 2), '|\n', sep='')
pad_message("    Cohen's d         Power", l)
for(i in 1:length(ds)) {
    ps = sprintf("%.3f", results[i]) 
    pad_message(paste0('       ', ds[i], "            ", ps), l)
}
cat('|', rep('=', l - 2), '|\n', sep='')

