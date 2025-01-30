# GT_BDM_validation
This repository contains code that automates my key validation steps that I have now automated. Mainly there are 6 validation steps that I intend to validate. More details in README(coming soon !).

In the current process of model validation, these are the metrics that I will be checking: -

1.R-squares and MAPE:  Both of them together are categorized as a Goodness-of-fit criteria. While the initial models GT provided had r^2 always greater than 90% but with subsequent falls in this measure, GT gave the below thresholds. Thresholds for r^2 is 75% (flag if lower). For MAPE its 10% (flag if higher).

2.Priors within 90% bounds: To test if the priors lie within 90% of the credible interval. This check ensures that the posterior point estimate must always lie in a bounded vicinity of the prior, thus reducing the chances of outliers.
3.VIF and T-score: These variables account for the extra variance in the model. Again, due to interaction effect, variables like CPI will almost always have a high VIF, so agreed to include it whatsoever be the score. But this is not the case with variables with dummy/step variables that are included by the modeler to account for seasonality etc. Threshold: 1. VIF - greater than 20. 2. T-score: less than -1 or greater than 1.

4..Data Influence: This tells us what is driving the model more, data or priors. A score greater than 1 tells us that priors are taking precedence. While currently its prior driven model, I believe that after some iterations (2or 3) it should data centered.

5.Contribution-Group labelling: The input variables are classified in buckets like base, incentives, National Media etc. While this labelling doesn't affect the modelling results, but it will have an effect while giving overall scenario at contribution level.  I have observed multiple times that the variables are mis-classified. For example: Ibotta coupons classified as "Others" and not under "National Media".

6.Variable Transformation: There are some mathematical transformations that GT performs on variables as part of standardization like STA, SUB etc. This check is performed to maintain uniformity throughout the modelling. For example, CPI was had different transformation for 2 brands.
