This package will allow for easy building of yield curves using various methodologies found in academic literature. 
Currently, this package only has the Nelson Siegal function programmed but other functions are being worked on at the moment.

To use:
Make sure your dataframe consists of yields with column names denoting the maturity of the security in months.
Initiate the function as such:
  curve = NelsonSiegal(est_l=True)
  curve.fit(data, params=[1,1,1,1], l=none)

The NelsonSiegal function contains one argument. est_l - this argument is basically asking if you would like to have the lambda estimated
from the data using a non-linear least squares optimizer. Setting this to true will do so. Setting this to false means you will have to 
provide your own value of lambda into the fit function.
The fit function contains three arguments. Data - this is just your dataframe, params - this is an array of parameters used as starting 
values in the optimisation function. Finally, l is just the value for lambda if you chose this option in the initiation function.