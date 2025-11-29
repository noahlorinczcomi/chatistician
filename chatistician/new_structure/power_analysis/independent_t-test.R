library(optparse)
optlist = list(
    make_option('--n1', type='integer', help='Sample size in group 1'),
    make_option('--n2', type='integer', help='Sample size in group 2'),
    make_option('--type-1', type='numeric', default=0.05, help='Type 1 error / significance threshold'),
    make_option('--variance-1', type='numeric', default=1, help='Variance in group 1'),
    make_option('--variance-2', type='numeric', default=1, help='Variance in group 2'),
    make_option('--number-simulations', type='integer', default=1000, help='Number of simulation replicates')
)

opts = parse_args(OptionParser(option_list=optlist))

# simpler names
k = opts$`number-simulations`
ds = c(0.1, 0.3, 0.5, 0.7, 0.9)
alpha = opts$`type-1`
n1 = opts$n1
n2 = opts$n2

sigma2_1 = opts$`variance-1`
sigma2_2 = opts$`variance-2`
pooled_sd = sqrt((sigma2_1 + sigma2_2) / 2)

l = 40
results = c()
for(i in 1:length(ds)) {
    r = c()
    for(iter in 1:k) {
        # draw raw data
        x1 = rnorm(n1, 0, sqrt(sigma2_1))
        x2 = rnorm(n2, ds[i] * pooled_sd, sqrt(sigma2_2))
        # perform t-test
        fit = t.test(x1, x2, var.equal=sigma2_1 == sigma2_2)
        r[iter] = fit$p.value < alpha
    }
    results[i] = mean(r)
}

# clean results
pad_message=function(message, l) {
    pad = l - nchar(message) - 3
    cat('| ', message, rep(' ', pad), '|\n', sep='')
}
cat('\n')
cat('|', rep('=', l - 2), '|\n', sep='')
pad_message('Independent T-test power analysis', l)
cat('|', rep('=', l - 2), '|\n', sep='')
pad_message(paste0('Sample sizes = ', n1, ', ', n2), l)
pad_message(paste0('Variances = ', sigma2_1, ', ', sigma2_2), l)
pad_message(paste0('Significance threshold = ', alpha), l)
cat('|', rep('-', l - 2), '|\n', sep='')
pad_message("    Cohen's d         Power", l)
for(i in 1:length(ds)) {
    ps = sprintf("%.3f", results[i]) 
    pad_message(paste0('       ', ds[i], "            ", ps), l)
}
cat('|', rep('=', l - 2), '|\n', sep='')

