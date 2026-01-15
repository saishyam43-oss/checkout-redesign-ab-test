# Power BI Measures — Checkout A/B Test

This document lists and explains all calculated measures used in the Power BI dashboard.
Measures are grouped by purpose to reflect analytical intent, not creation order.

---

## 1. Statistical Configuration

### Alpha Threshold
Defines the statistical significance cutoff used across the dashboard.
```
Alpha_Threshold = 0.05
```
---

## 2. Core Conversion Metrics

### Control Conversion Rate (CVR)
```
Control_CVR =
DIVIDE(
    CALCULATE(SUM('Table'[Converted_users]), 'Table'[Group] = "Control"),
    CALCULATE(SUM('Table'[Total_users]), 'Table'[Group] = "Control")
)

Treatment_CVR =
DIVIDE(
    CALCULATE(SUM('Table'[Converted_users]), 'Table'[Group] = "treatment"),
    CALCULATE(SUM('Table'[Total_users]), 'Table'[Group] = "treatment")
)
```

## 3. Sample Size Metrics

Sample sizes are exposed explicitly to ensure experimental transparency.
```
Control_Sample_Size = 144,252
Treatment_Sample_Size = 144,349
Total_Sample_Size = 288,601
```

## 4. Lift Calculation
### CVR Lift (Numeric) - Used for calculations and validation.
```
CVR_Lift_1 =
DIVIDE(
    [Treatment_CVR] - [Control_CVR],
    [Control_CVR]
)
```

### CVR Lift (Formatted for Display) - Adds directional arrows for executive readability.
```
CVR_Lift =
VAR _perc =
    DIVIDE(
        [Treatment_CVR] - [Control_CVR],
        [Control_CVR]
    )
RETURN
    SWITCH(
        TRUE(),
        _perc > 0, FORMAT(_perc, "0.0%") & " ▲",
        _perc < 0, FORMAT(ABS(_perc), "0.0%") & " ▼",
        FORMAT(_perc, "0.0%")
    )
```

## 5. Statistical Test Results
### P-Value
Derived externally and surfaced for decision-making.
```
P_Value = 0.913
```
### Test Result Status
Textual interpretation of the p-value relative to alpha.
```
Test_Result_Status =
VAR PValue = [P_Value]
VAR Alpha = [Alpha_Threshold]
RETURN
    IF(
        PValue > Alpha,
        "> than alpha (0.05)",
        "< than alpha (0.05)"
    )
```

## 6. Conditional Formatting Logic
## Comparison Color
```
Comparison_Color =
VAR PValue = [P_Value]
VAR Alpha = [Alpha_Threshold]
RETURN
    IF(
        PValue > Alpha,
        "#e8d166",   -- Not significant
        "#00FF00"    -- Significant
    )
```
Used to visually indicate statistical significance.

## Design Note

Statistical computation (z-test and p-value) is intentionally performed outside Power BI
to avoid false precision and ensure reproducibility. Power BI is used strictly for
interpretation, communication, and decision support.

