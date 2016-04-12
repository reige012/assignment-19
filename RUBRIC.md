## Task 1

In the [amniote natural history database](http://esapubs.org/archive/ecol/E096/269/#data) (`task1-files`), there is a large CSV file containing attributes for a number of life history characteristics of amniotes.  Write a program that uses `pandas` to summarize attributes of this entire file **by order** (format below).  Write your output to a CSV file that looks like:

```
class,order,parameter,mean(parameter),95CI(parameter),min(parameter),max(parameter),median(parameter)
Aves,Accipitriformes,female_maturity_d,xxx,yyy,zzz,qqq,sss
```

where you create all of these lines for all of the following parameters (across all orders in the database):

```
female_maturity_d
litter_or_clutch_size_n
litters_or_clutches_per_y
adult_body_mass_g
maximum_longevity_y
longevity_y
female_body_mass_g
male_body_mass_g
```

and where the "95CI" is the 95% confidence interval of the parameter.  Use `argparse` to (1) get the input file name (the amniote natural history database), (2) to get the list of parameters to summarize, and (3) to get the output file name.  Be sure that your program is formatted correctly (PEP8).

- [ ] Program is correctly formatted [PEP8] (3.0 pt)
- [ ] Program functions as requested (12.0 pt)
