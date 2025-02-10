# Model Validation Automation Script

This repository contains a Python script that automates the validation process for model performance metrics based on multiple checks. The script processes input CSVs, computes specific metrics, and compares them against predefined thresholds to flag any discrepancies or issues.

## Purpose

The purpose of this script is to automate the validation of model results. It checks key model metrics, validates prior information, assesses data influence, and ensures consistency in variable classifications and transformations. The output will help determine if the model meets the required thresholds or if further adjustments are necessary.

## Features

The script validates the following metrics:

### 1. **Goodness-of-Fit Criteria: R-squares and MAPE**
   - **R-squares**: Measures the proportion of variance explained by the model. A threshold of 75% is considered acceptable. If the R-squared value is below 75%, the model will be flagged.
   - **MAPE (Mean Absolute Percentage Error)**: Measures the accuracy of the model’s predictions. A threshold of 10% is used—if the MAPE exceeds 10%, the model will be flagged.

### 2. **Priors within 90% Bounds**
   - This validation checks if the priors lie within 90% of the credible interval. If the posterior point estimate is outside this range, it could suggest a potential outlier in the model.

### 3. **Variance Inflation Factor (VIF) and T-score**
   - **VIF**: Measures how much the variance of a regression coefficient is inflated due to multicollinearity. A threshold of 10 is set to flag models with high multicollinearity.
   - **T-score**: Measures the statistical significance of variables. A threshold is set to flag values lower than -1 or greater than 1.

### 4. **Data Influence**
   - This metric evaluates whether the model is data-driven or prior-driven. A score greater than 1 indicates that priors are dominating the model. Ideally, this score should be close to 1 after a few iterations, showing a balanced model driven by data.

### 5. **Contribution-Group Labeling**
   - Input variables are categorized into groups like base, incentives, and National Media. This validation ensures variables are classified into the correct groups. Misclassification (e.g., Ibotta coupons categorized under "Others" instead of "National Media") will be flagged for correction.

### 6. **Variable Transformation Consistency**
   - Ensures that mathematical transformations (e.g., STA, SUB) are applied consistently across all variables. The script checks for any discrepancies in transformations (e.g., different transformations for the same variable across brands) and flags them.

## Usage

### Prerequisites
- Python 3.x
- Required Python packages:
    - `pandas`
    - `numpy`
    - `scipy`
    - `statsmodels`

You can install the required packages using the following command:

```bash
pip install -r requirements.txt
```

### Input

The script expects the following CSV files as input:

- **model_results.csv**: Contains the model output metrics.
- **variable_data.csv**: Includes the variables and their transformations, contributions, and classifications.
- **priors.csv**: Contains prior information for the model.

Make sure the CSVs follow the correct structure as specified in the documentation.

### Running the Script

To run the script, use the following command:

```bash
python validate_model.py --model-results model_results.csv --variable-data variable_data.csv --priors priors.csv
```

This will process the data, perform the validations, and output the results in a report.

### Output

The script generates a report summarizing the validation results, including:

- Whether each metric is within the acceptable threshold.
- Flags for any issues detected (e.g., priors outside bounds, high VIF, misclassified variables).
- Recommendations for adjustments or further investigation.

## Thresholds

The script uses the following thresholds for validation:

- **R-squared**: 75% (Flag if lower)
- **MAPE**: 10% (Flag if higher)
- **VIF**: 10 (Flag if higher)
- **T-score**: -1 or 1 (Flag if outside this range)
- **Data Influence**: Greater than 1 indicates prior-dominant model (aim for balance after iterations)
  
## Contributing

If you would like to contribute to this project, feel free to fork the repository, create a branch, and submit a pull request with your changes.
