# KPIs & Metrics Framework — Vueling Inflight Experience
### How We Measure Success, Report Progress, and Prove ROI

---

## Metrics Philosophy

Every metric must answer one of three questions:
1. **Are passengers using it?** (Engagement)
2. **Are passengers happier?** (Satisfaction)
3. **Is it making money / saving money?** (Revenue & Operations)

If a metric doesn't answer one of these, we don't track it.

---

## Dashboard Overview

```
+===========================================================================+
|                    VUELING INFLIGHT EXPERIENCE DASHBOARD                   |
|                                                                           |
|  ENGAGEMENT           REVENUE              SATISFACTION    OPERATIONS     |
|  +-----------+        +-----------+        +-----------+  +-----------+  |
|  | 27.3%     |        | 9.1%      |        | +6 pts    |  | -18%      |  |
|  | Activation|        | Pre-order |        | NPS Delta |  | Aisle     |  |
|  | Rate      |        | Conv.     |        |           |  | Time      |  |
|  +-----------+        +-----------+        +-----------+  +-----------+  |
|                                                                           |
|  +-----------+        +-----------+        +-----------+  +-----------+  |
|  | 14.2 min  |        | +34%      |        | 4.3 / 5   |  | -22%      |  |
|  | Avg.      |        | AOV       |        | Sat.      |  | Food      |  |
|  | Session   |        | Uplift    |        | Score     |  | Waste     |  |
|  +-----------+        +-----------+        +-----------+  +-----------+  |
+===========================================================================+
```

---

## 1. ENGAGEMENT METRICS

### Primary Metrics

| Metric | Definition | Target (6mo) | Target (12mo) | How We Measure |
|---|---|---|---|---|
| **Activation Rate** | % of passengers who open the experience per flight | >25% | >40% | App analytics + WiFi portal logins |
| **Average Session Duration** | Time spent in the experience per passenger | >12 min | >18 min | In-app time tracking |
| **Return Rate** | % of passengers who use it on their next Vueling flight | >50% | >65% | Cross-booking analysis |
| **Content Depth** | Avg. number of pillars explored per session (out of 8) | >3 | >5 | Section view events |

### Pillar-Specific Engagement

| Pillar | Metric | Target |
|---|---|---|
| **Destination Guide** | % who open highlights section | >60% of users |
| **Destination Guide** | % who read a long description (scroll depth) | >30% of users |
| **Flight Tracker** | % who view the live map | >50% of users |
| **Flight Tracker** | Avg. time on map screen | >3 min |
| **Your Aircraft** | % who view aircraft info | >25% of users |
| **Your Crew** | % who view crew names | >20% of users |
| **Weather & News** | % who check weather | >40% of users |
| **Weather & News** | % who read news headlines | >30% of users |
| **Digital Magazine** | % who open at least one article | >20% of users |
| **Digital Magazine** | Avg. articles read per session | >1.5 |
| **Music & Audio** | % who play at least one track | >15% of users |
| **Music & Audio** | Avg. listening time | >20 min |
| **Food & Snacks** | % who browse the digital menu | >30% of users |
| **Food & Snacks** | % who add item to cart | >15% of users |
| **Food & Snacks** | Conversion: cart to purchase | >55% |

### Engagement Segmentation

Track engagement by:
- **Route type**: Domestic vs. International vs. Island routes
- **Flight duration**: Short-haul (<1.5h) vs. Medium (1.5-3h) vs. Long (3h+)
- **Passenger type**: Business vs. Economy | Frequent flyer vs. Occasional
- **Language**: Are certain language cohorts more engaged?
- **Time of day**: Morning vs. Afternoon vs. Evening flights
- **Access method**: App (pre-cached) vs. WiFi portal (browser)

---

## 2. REVENUE METRICS

### Food & Beverage Revenue

| Metric | Definition | Target (6mo) | Target (12mo) | Notes |
|---|---|---|---|---|
| **Pre-order Conversion Rate** | % of passengers who pre-order food (T-24h to T-1h) | >8% | >15% | Primary revenue KPI |
| **Onboard Order Conversion** | % of passengers who order food digitally during flight | >12% | >20% | Complementary to pre-order |
| **Total Digital F&B Conversion** | Pre-order + onboard combined | >18% | >30% | vs. current aisle cart: ~10-15% |
| **Average Order Value (AOV)** | Avg. EUR per digital food order | 10-12 EUR | 12-15 EUR | Target: +30% vs. aisle cart |
| **AOV Uplift vs. Aisle** | % increase in basket size for digital orders | +30% | +40% | Photos + descriptions = higher AOV |
| **Revenue Per Available Seat (RPAS)** | F&B revenue / total seats | Track monthly | +25% vs. baseline | Industry-standard metric |
| **Pre-order Revenue Share** | % of total F&B revenue from pre-orders | >30% | >45% | Pre-orders = guaranteed revenue |

### Revenue Projection Model

```
CONSERVATIVE SCENARIO (Year 1):
  34M passengers/year
  x 8% pre-order conversion = 2.72M pre-orders
  x 10 EUR avg. order = 27.2M EUR pre-order revenue

  34M passengers/year
  x 12% onboard order conversion = 4.08M onboard orders
  x 8 EUR avg. order = 32.6M EUR onboard revenue

  TOTAL INCREMENTAL F&B = ~60M EUR
  (vs. current aisle-only model)
  NET NEW (after cannibalization) = estimated 25-35M EUR incremental

OPTIMISTIC SCENARIO (Year 2, mature):
  x 15% pre-order + 20% onboard = ~100M EUR digital F&B
  + Ancillary commerce (restaurant bookings, transfers) = TBD
```

### Future Commerce Metrics (Phase 4+)

| Metric | Definition | Target |
|---|---|---|
| **Restaurant Booking Conversion** | % who book a restaurant through the experience | >2% of users |
| **Transfer Booking Conversion** | % who book airport transfer | >3% of users |
| **Commission Revenue** | Avg. commission per booking | 2-5 EUR |
| **Commerce ARPU** | Avg. revenue per user across all commerce | Track and grow |

---

## 3. SATISFACTION METRICS

### Core Satisfaction

| Metric | Definition | Target (6mo) | How We Measure |
|---|---|---|---|
| **NPS Delta** | NPS of experience users vs. non-users on same flight | +5 points | Post-flight survey split |
| **NPS Absolute** | NPS score of experience users | >45 | In-app NPS prompt at landing |
| **Satisfaction Score** | "How would you rate your inflight experience?" (1-5) | >4.2 / 5.0 | Post-flight survey |
| **Effort Score** | "How easy was it to use the inflight experience?" (1-5) | >4.5 / 5.0 | In-app prompt |
| **Recommendation Rate** | "Would you recommend Vueling to a friend?" (1-10) | >7.5 | Part of NPS |

### Qualitative Feedback

| Signal | Source | Frequency |
|---|---|---|
| In-app star rating | Prompt at landing | Per flight |
| Free-text feedback | Optional field in rating | Per flight |
| Social media mentions | Social listening tools | Continuous |
| App store reviews mentioning inflight | App store monitoring | Weekly |
| Customer service ticket analysis | CS platform | Monthly |

### Satisfaction Segmentation

Compare satisfaction across:
- Users vs. non-users (same flight, same route)
- First-time users vs. repeat users
- App users vs. WiFi portal users
- Pre-order customers vs. onboard order vs. no order
- By route and flight duration

---

## 4. OPERATIONAL METRICS

### Cabin Crew Efficiency

| Metric | Definition | Target | How We Measure |
|---|---|---|---|
| **Aisle Service Time Reduction** | Time cabin crew spends on food cart service per flight | -15% | Crew reporting + time tracking |
| **Pre-order Fulfillment Time** | Time from cabin crew start to all pre-orders delivered | <15 min | Crew tablet timestamps |
| **Digital Order Fulfillment Time** | Avg. time from order placed to delivered | <10 min | App + crew tablet timestamps |
| **Cart Passes Reduced** | Number of aisle cart passes per flight | -1 pass per flight | Crew reporting |
| **Turnaround Time Impact** | Impact on aircraft turnaround time | Neutral or better | Ops tracking |

### Food Waste & Catering

| Metric | Definition | Target | How We Measure |
|---|---|---|---|
| **Food Waste Reduction** | % reduction in unsold food per flight | -20% | Catering reconciliation |
| **Catering Accuracy** | % of pre-orders correctly loaded | >99% | Crew + passenger reports |
| **Stock Optimization** | Reduction in overstock per route | -15% | Catering data vs. orders |
| **Catering Cost per Pax** | Total catering cost / passengers | -10% | Finance reporting |

### Sustainability

| Metric | Definition | Target | How We Measure |
|---|---|---|---|
| **Paper Magazine Elimination** | % of flights without paper magazines | 100% (Phase 1+) | Operations tracking |
| **Paper Saved (tons/year)** | Weight of paper magazines eliminated | Full weight | Procurement data |
| **Fuel Savings from Weight** | Fuel saved from removing paper | Calculated | Weight x fuel formula |
| **Carbon Offset** | CO2 reduction from paper + fuel savings | Report annually | ESG calculation |

---

## 5. TECHNICAL / PLATFORM METRICS

### Performance

| Metric | Target | Alert Threshold |
|---|---|---|
| Content pre-cache success rate (silent push) | >95% | <90% |
| App experience load time (pre-cached) | <1 second | >3 seconds |
| WiFi portal load time (edge cache) | <3 seconds | >6 seconds |
| Food order submission latency | <5 seconds | >10 seconds |
| Payment processing time | <8 seconds | >15 seconds |
| Flight tracker update frequency | Every 30 seconds | >60 seconds gap |
| API uptime (backend) | 99.9% | <99.5% |
| Edge cache hit rate (onboard) | >98% | <95% |

### Content Quality

| Metric | Target | How We Monitor |
|---|---|---|
| AI content safety compliance | 100% (no violations) | Automated safety filter + spot checks |
| Translation accuracy score | >4.5 / 5.0 | Periodic human review |
| News content freshness | <6 hours old | Automated monitoring |
| Weather accuracy (vs. actual) | >85% | Post-flight comparison |
| Content generation success rate | >99% per refresh cycle | Pipeline monitoring |

---

## Reporting Cadence

| Report | Audience | Frequency | Contents |
|---|---|---|---|
| **Daily Dashboard** | Product & Engineering | Daily | Activation rate, orders, errors |
| **Weekly Business Review** | VP level | Weekly | All KPI categories, trends, anomalies |
| **Monthly Board Report** | C-suite | Monthly | Revenue impact, NPS delta, engagement trends |
| **Quarterly Business Review** | Board / Investors | Quarterly | Full P&L impact, ROI analysis, roadmap progress |
| **Route Performance** | Commercial team | Bi-weekly | Per-route engagement, F&B conversion, top content |
| **A/B Test Results** | Product | As needed | Feature experiments, conversion optimization |

---

## A/B Testing Strategy

### Phase 1 Tests

| Test | Hypothesis | Metric | Duration |
|---|---|---|---|
| Pre-order push timing | T-24h vs. T-12h vs. T-6h — which drives more pre-orders? | Pre-order conversion rate | 4 weeks |
| Menu photo quality | Professional photos vs. standard — impact on AOV | Average order value | 4 weeks |
| Notification copy | "Pre-order your lunch" vs. "Your menu is ready" | Push open rate + conversion | 2 weeks |
| Experience entry point | Destination-first vs. Flight-info-first | Content depth + session time | 4 weeks |

### Phase 2 Tests

| Test | Hypothesis | Metric | Duration |
|---|---|---|---|
| Music auto-play | Auto-play vs. opt-in — impact on listening time | Music engagement rate | 4 weeks |
| Picnic bag pricing | 8 EUR vs. 10 EUR vs. 12 EUR — price sensitivity | Conversion rate + revenue | 6 weeks |
| NPS timing | Landing prompt vs. 2h after landing vs. next day | Response rate + score | 4 weeks |
| Magazine personalization | Same articles for all vs. personalized by destination | Read rate + time | 4 weeks |

---

## Success Milestones

| Milestone | Criteria | Target Date |
|---|---|---|
| **POC Validated** | Live demo works, 3 destinations, 6 languages | Feb 2026 (DONE) |
| **First Real Passengers** | 1,000 passengers use the experience on pilot routes | Q2 2026 |
| **Engagement Threshold** | >25% activation rate on pilot routes | Q2 2026 |
| **First Pre-order Revenue** | Food pre-orders live on pilot routes | Q3 2026 |
| **Revenue Positive** | Platform revenue exceeds platform cost | Q4 2026 |
| **Network Rollout** | Experience available on >80% of routes | Q1 2027 |
| **NPS Impact Confirmed** | Statistically significant NPS lift measured | Q1 2027 |
| **Full Commerce** | Restaurant + transfer bookings live | Q2 2027 |

---

**Every metric in this framework is designed to prove one thing: the Vueling Inflight Experience creates value for passengers and revenue for the business.**

**We measure it. We report it. We optimize it. We win.**
