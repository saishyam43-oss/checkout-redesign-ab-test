# E-commerce Checkout Redesign — A/B Test Analysis

> *A statistically well-powered experiment that failed, and why that matters.*

---

## ⚡ Executive Snapshot

**Problem**  
A redesigned checkout experience was proposed to improve purchase conversion.

**Decision**  
❌ **Do Not Ship.**

**Why**  
In a large, well-powered experiment (~289k users), the treatment failed to show any statistically significant uplift and exhibited a slight negative directional effect.

**Bottom Line**  
The redesign introduces risk without evidence of benefit. Shipping would be irresponsible.

---

## 📊 Dashboard Summary

> *Executive-facing view of the experiment outcome*

![Checkout A/B Test Dashboard](images/dashboard_summary.png)

---

## 🏢 Business Context

This project is framed around a fictional high-volume **e-commerce platform** where checkout conversion directly impacts revenue.

Checkout is a **high-leverage surface**:
- Small regressions scale quickly
- User tolerance for friction is low
- “Neutral” changes are often negative in practice

My responsibility as a Product Analyst was to determine whether the redesigned checkout should replace the existing experience.

---

## 🎯 Objective & Hypothesis

### Objective  
Evaluate whether the redesigned checkout page produces a **statistically significant increase** in conversion rate compared to the existing checkout.

### Hypotheses  
- **Null Hypothesis (H₀):** Treatment ≤ Control  
- **Alternative Hypothesis (H₁):** Treatment > Control  

A one-sided hypothesis reflects the real product decision rule. Shipping only occurs if the redesign is strictly better.

---

## 🧪 Experiment Details

- **Experiment Type:** Randomized A/B Test  
- **Primary Metric:** Checkout Conversion Rate  
- **Statistical Test:** One-sided z-test for two proportions  
- **Significance Level (α):** 0.05  

### Sample Size
- **Control:** 144,252 users  
- **Treatment:** 144,349 users  
- **Total:** 288,601 users  

This sample size provides sufficient power to detect even small practical effects.

---

## 🔍 Data Integrity & Cleaning

Before analysis, experimental correctness was enforced:

- Removed invalid group–landing page mismatches  
- Deduplicated users, treating conversion as binary  
- Ensured one valid experimental exposure per user  

These steps prevent biased estimates and inflated significance.

---

## 📊 Results

| Group      | Conversion Rate |
|-----------|-----------------|
| Control   | **12.11%** |
| Treatment | **11.95%** |

- **Relative Lift:** −1.4%  
- **p-value:** 0.913  
- **Statistical Significance:** ❌ No  

### Interpretation  
The observed difference is fully consistent with random variation. Given the scale of the experiment, the absence of lift strongly suggests the redesign provides no meaningful benefit.

---

## 📌 Decision Rationale

This is a clear **Do Not Ship** decision.

- No statistical evidence of improvement  
- Directional movement is negative  
- Checkout is too critical to accept unproven changes  

A failed experiment at this scale is a valid and valuable outcome. It prevents a costly mistake.

---

## 🔍 Post-Test Diagnostics

A senior experiment does not end at “the test failed.”

While the aggregate result was flat, I recommended **post-test segmentation analysis** to rule out asymmetric harm, particularly in high-risk segments.

Key follow-up questions:
- Did the redesign disproportionately hurt **mobile users**, where checkout friction is highest?
- Were effects different for **new vs. returning customers**?
- Did conversion drop at specific funnel steps (payment entry, address confirmation)?

These diagnostics help distinguish between:
- A universally weak design  
- Versus a design that fails overall but hides **segment-specific regressions**

Although the redesign was not shipped, these insights would directly inform future iteration and UX improvements.

---

## 📂 Repository Structure
```
ecommerce-checkout-ab-test/
│
├── data/ # Raw datasets
├── sql/ # Validation, cleaning, and aggregation queries
├── python/ # Data cleaning and statistical testing
├── powerbi/ # Dashboard and documented DAX measures
├── images/ # Dashboard screenshots
└── README.md
```

---

## 🛠️ Tech Stack

- **SQL** — data validation and aggregation  
- **Python** — data cleaning and statistical testing  
- **Power BI** — executive reporting and decision communication  

---

## ⚠️ Limitations

- No segmented results included in the final analysis  
- No secondary guardrail metrics (e.g., latency, errors)  
- Short-term conversion only  

These limitations do not weaken the primary decision, given the strength of the null result.

---

## 📣 Final Note

This project demonstrates a core product analytics skill:

> Knowing when **not** to ship.

Strong experimentation is not about finding wins. It is about preventing confident mistakes, especially on high-impact surfaces like checkout.

