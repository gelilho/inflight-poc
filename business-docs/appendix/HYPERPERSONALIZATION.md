# Hyperpersonalization Vision — Vueling Inflight Experience

> **The long-term objective**: Transform the Inflight Experience from a content platform into an intelligence engine that knows every passenger and treats them like a VIP — whether they're flying for holidays, leisure, or business.

---

## Why This Matters

The Inflight Experience is not just a product. It's a **data flywheel**.

Every time a passenger pre-orders food, browses a destination guide, listens to music, reads a magazine article, or searches the FAQ — they're telling us who they are, what they care about, and how they travel.

Today, airlines know very little about passenger preferences beyond their booking class and frequent flyer tier. The Inflight Experience changes that. It gives us a direct, opt-in, high-engagement channel to understand passengers as individuals.

**The goal: treat every passenger like they're flying Business class — even if they're in Economy.**

---

## The Data We Collect (With Consent)

Every interaction within the Inflight Experience generates a preference signal:

| Interaction | What We Learn |
|---|---|
| Food pre-orders | Dietary preferences (Mediterranean, vegetarian, allergies) |
| Food order frequency | Engagement level with F&B — high-value passenger signal |
| Destination content browsed | Travel interests (culture, history, nightlife, family) |
| Restaurant clicks | Cuisine preferences (Italian, sushi, fine dining, budget) |
| Music listening | Mood, genre, local interest |
| Magazine articles read | Content preferences (adventure, wellness, food, city guides) |
| FAQ searches | Pain points, questions, concerns |
| Transport booking | Budget level, convenience preferences |
| Flight tracker usage | Engagement style (frequent checkers vs. casual) |
| NPS ratings | Overall satisfaction, flight-specific feedback |
| Session frequency | How often they use the experience across flights |

---

## Personalization Layers

### Layer 1 — Remembered Preferences (Phase 3)

The simplest form of personalization: remember what the passenger chose before.

| Scenario | What Happens |
|---|---|
| Maria always orders Mediterranean | Menu opens with "Your favorites" section — Mediterranean salad at the top |
| Carlos always reads culture articles | Magazine opens with culture stories first |
| Elena always checks transport first | Destination guide shows transport tab first |
| Pedro never orders food | No aggressive food push — instead, a gentle "Something new today?" |

**How**: Passenger profile stored server-side, keyed to frequent flyer ID or PNR history. Loaded at experience activation.

---

### Layer 2 — Frequency Recognition (Phase 3)

Recognize passengers who fly often and engage often. Make them feel seen.

| Signal | Recognition |
|---|---|
| Flew 5+ times this year | Personal welcome: "Welcome back, Maria! Your 7th flight this year" |
| Orders food on every flight | "Your usual? Mediterranean salad + coffee" — one-tap reorder |
| Always uses the experience | Priority content: early access to new magazine articles |
| First time using the experience | Guided tour: "Here's what you can do during your flight" |
| Family traveling together | Family-friendly content highlighted, kids' menu surfaced |

**How**: Flight history analysis. Order history aggregation. Simple rules engine at first, ML-powered later.

---

### Layer 3 — Predictive Personalization (Phase 4)

Go beyond remembering — start anticipating.

| Prediction | How |
|---|---|
| "Maria will probably order food on this flight" | She has ordered on 8 of her last 10 flights → pre-populate cart |
| "This route has high demand for vegetarian options" | Aggregate pre-order data → optimize catering stock |
| "Business travelers on Monday mornings want coffee + news" | Segment-based defaults → quick breakfast + news-first layout |
| "Families flying to Mallorca want beach tips" | Destination content weighted toward family activities |
| "Carlos hasn't flown in 6 months — win him back" | Re-engagement push with personalized offer |

**How**: ML models trained on aggregate behavior. Collaborative filtering (passengers like you also enjoyed...). Seasonal and route-based patterns.

---

## The VIP Treatment — For Everyone

The core philosophy: **every passenger should feel that Vueling knows them and cares about their experience**, regardless of booking class.

### What "VIP for Everyone" Looks Like

| Traditional VIP (Business only) | Our Vision (Everyone) |
|---|---|
| Lounge access | Personalized content before boarding |
| Priority boarding | Pre-ordered food waiting at seat |
| Premium meal | Menu that knows your preferences |
| Dedicated service | "Welcome back, Maria!" in the app |
| Concierge | Destination guide tailored to your interests |
| Post-flight follow-up | NPS + personalized next-trip suggestion |

The difference: **we scale the feeling of premium treatment through software, not through physical infrastructure.** No extra cost per passenger. Just smarter data usage.

---

## Frequent Flyer + Food Service = Loyalty Gold

One of the most powerful signals is the combination of **flight frequency** and **food ordering behavior**.

### The Insight

A passenger who flies frequently AND orders food regularly is among the most engaged and monetizable customers. They deserve special treatment:

| Frequent Flyer + Food User | What They Get |
|---|---|
| Flies monthly, orders every flight | "Gold Menu" — exclusive items, early access to seasonal specials |
| Orders the same thing repeatedly | One-tap reorder: "Your usual, Maria?" |
| High total spend on food | Loyalty discount: "Your 10th order is on us" |
| Tries new items | "Taste explorer" badge — personalized suggestions from new menu additions |
| Refers others to pre-order | Referral bonus: free coffee or snack upgrade |

### Why This Matters for Vueling

- **Retention**: Passengers who feel recognized come back
- **Spend**: Personalized suggestions increase basket size
- **Advocacy**: Delighted passengers recommend Vueling
- **Data**: Every order enriches the passenger profile for smarter personalization

---

## Aggregated Intelligence — Beyond Individual Personalization

The data doesn't just help individual passengers. In aggregate, it transforms operations:

### Predictive Catering

```
PRE-ORDERS (demand signal)     +     HISTORICAL PATTERNS     =     OPTIMAL STOCK
                                                                     PER FLIGHT
"42 pre-orders on VY71299"    +   "BCN→FCO averages 15%     =    "Load 60 meals
 (38 hot meals, 4 salads)          onboard orders on top          + 25% buffer
                                    of pre-orders"                  = 75 total"
```

**Impact**: Less food waste. Lower catering costs. Fresher food. Better passenger experience.

### Route-Level Insights

| Insight | Action |
|---|---|
| Rome flights: 70% want transport info first | Default to transport tab for FCO flights |
| London flights: music engagement 2x higher | Promote music pillar more prominently |
| Monday BCN→MAD: 90% skip destination content | Minimize destination, maximize news + food |
| Summer Mallorca flights: family content 3x more popular | Auto-curate family-friendly experience |

### Menu Optimization

| Insight | Action |
|---|---|
| Mediterranean salad sells 3x more on Italian routes | Stock more on FCO/MXP flights |
| Croissants peak on morning flights | Optimize morning catering load |
| Drinks-only orders dominate short flights (<1.5h) | Offer "Quick Drink" bundle for short-haul |
| Weekend flights: dessert attachment rate +40% | Suggest dessert add-on for weekend travelers |

---

## Privacy by Design

Hyperpersonalization only works if passengers trust us with their data.

| Principle | How We Implement It |
|---|---|
| **Opt-in** | Personalization is optional. Default experience works without any data |
| **Transparency** | Clear explanation of what data is used and why |
| **Control** | Passengers can view, export, and delete their preference profile |
| **GDPR compliance** | No personal data sent to external APIs. All profiling internal to Vueling systems |
| **Anonymization** | Aggregate analytics use anonymized data only |
| **Value exchange** | Personalization delivers visible value — passengers see why sharing data benefits them |

---

## Implementation Roadmap

| Phase | Capability | When |
|---|---|---|
| **POC** (now) | Anonymous experience — same for all passengers | Feb 2026 |
| **Phase 1** | Language preference remembered. Pre-order history stored | Q2 2026 |
| **Phase 2** | Food favorites, one-tap reorder. Basic frequency recognition | Q3 2026 |
| **Phase 3** | Full preference profile. "Welcome back" experience. Content prioritization by interests. Frequent flyer + food loyalty programs | Q4 2026 |
| **Phase 4** | Predictive personalization. Anticipatory catering. Route-level optimization. ML-powered recommendations | 2027 |

---

## The North Star Metric

**Passenger Lifetime Value (PLV) delta**: The difference in total revenue and rebooking rate between passengers who use the Inflight Experience regularly and those who don't.

If we can prove that passengers who engage with the experience **fly more often**, **spend more per flight**, and **recommend Vueling more** — the platform justifies itself many times over.

---

## In One Sentence

**The Vueling Inflight Experience starts as a content platform, evolves into a commerce engine, and matures into the most personal relationship a low-cost carrier has ever had with its passengers.**

---

_This is not just about flying. It's about knowing who's flying and making them feel extraordinary._
