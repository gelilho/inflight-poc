# Vueling Inflight Experience — One Pager

> **In brief:** Vueling Inflight Experience is an AI-powered digital platform that transforms every flight into a personalized journey. From pre-ordering your meal the day before, to discovering your destination at 35,000 feet, to listening to curated music and reading a digital magazine — all delivered through the Vueling app and inflight WiFi. One booking number. Eight experience pillars. A complete ecosystem that delights passengers, drives ancillary revenue, and positions Vueling as the most innovative low-cost carrier in Europe.

---

## The Vision

**Transform every Vueling flight into a personalized, immersive digital journey** — from the moment a passenger checks in to the moment they land.

Not just a destination guide. A complete inflight ecosystem: curated content, live entertainment, real-time flight tracking, an onboard digital magazine, music playlists, and a food & snack pre-order and onboard ordering system that turns every seat into a personalized experience.

---

## The Problem

- Passengers sit idle for 1-3 hours with zero engagement
- No personalized content. No entertainment beyond what they bring
- Food service is reactive — cabin crew walks the aisle, passengers decide on the spot (or not at all)
- No connection between the airline and the passenger's destination
- Missed revenue: most passengers skip food purchases simply because the current ordering experience isn't convenient enough
- Competitors are investing in digital — Vueling risks falling behind

---

## The Solution: Vueling Inflight Experience

A single, unified digital experience delivered via the Vueling app and inflight WiFi portal.

### What the Passenger Gets

| Experience Pillar | What It Delivers |
|---|---|
| **Food & Snacks** | Browse the onboard menu, pre-order before the flight, order during the flight — delivered to your seat. No queues, no waiting. |
| **Your Aircraft** | Aircraft model, name ("Spirit of Barcelona"), registration, age — make flying personal and transparent |
| **Your Crew** | Captain and cabin crew names — humanize the experience, passengers feel they're in good hands |
| **Live Flight Tracker** | Real-time aircraft position on a map, altitude, speed, time to destination — see exactly where you are |
| **Discover Your Destination** | Top 5 highlights, 3 restaurant picks — AI-generated, in their language |
| **Getting to the City** | Airport-to-city transport options (train, bus, taxi) with times, costs, and practical tips — plus the option to book your transfer online |
| **Peace of Mind** | Emergency contacts (police, hospital, taxi) and Vueling helpline always at hand — because feeling safe matters |
| **Weather & News** | 3-day forecast + curated local news (sports, culture, events — inflight-safe) |
| **Music & Audio** | AI-curated playlists by mood and destination — mix of decades, local artists, chill vibes |
| **Digital Magazine** | Curated articles about destination, travel tips, Vueling stories — bringing back the spirit of the beloved Ling magazine, now in digital form |

---

## The Food & Snacks Game-Changer

This is the **monetization vertical** that pays for the entire platform.

### The Flow

1. **Day before the flight** — Passenger receives a push notification: "Flying to Rome tomorrow? Pre-order your onboard menu now"
2. **After check-in / security** — Second notification: "Your flight is in 2 hours. Want a snack bag ready for boarding?"
3. **Onboard, after takeoff** — Browse the digital menu, tap to order, pay in-app. Cabin crew delivers to your seat

### Why This Changes Everything

- **No friction**: Passengers order from their phone, not by flagging down crew
- **Pre-orders = guaranteed revenue**: Revenue captured before the plane even departs
- **Cabin crew efficiency**: Pre-orders are prepared in advance, reducing aisle service time
- **Higher basket size**: Digital menus with photos and descriptions increase average order value by 20-40%
- **Data**: Know what passengers want, optimize catering, reduce food waste

---

## Key Benefits

| For Passengers | For Vueling |
|---|---|
| Rich destination content before landing | Higher NPS and brand loyalty |
| Entertainment (music, magazine, news) | New ancillary revenue stream (food pre-orders) |
| Pre-order food — it's waiting for them | Competitive differentiator vs every LCC |
| Real-time flight info — feel in control | Cabin crew operational efficiency |
| Personalized in their language (6 languages) | Data-driven passenger insights |
| Emergency contacts always accessible | Scalable to entire route network via AI |
| Offline-ready — works without connectivity | Reduced paper waste (no physical magazine) |

---

## What Makes It Different

- **AI-generated content** — scales to any destination, no editorial team needed
- **Pre-order food system** — revenue captured before departure
- **Offline-first architecture** — content is pre-cached on device via silent push
- **Content safety** — all AI content follows strict inflight safety rules
- **Music curation** — AI-generated playlists refreshed weekly, mixing decades and local flavor
- **Real-time + cached hybrid** — flight tracker is live, content is pre-cached
- **6 languages from day one** — es, en, fr, it, ca, gl (expandable instantly)

---

## KPIs We Will Measure

| Category | Metric | Target |
|---|---|---|
| **Engagement** | % passengers using the experience | >25% in 6 months |
| **Engagement** | Avg. time spent in experience | >12 minutes per flight |
| **Engagement** | Content sections explored per session | >3 sections |
| **Revenue** | Food pre-order conversion rate | >8% of passengers |
| **Revenue** | Avg. order value (digital menu) | +30% vs. aisle service |
| **Revenue** | Incremental ancillary revenue per flight | Measured quarterly |
| **Satisfaction** | NPS lift (experience users vs. non-users) | +5 points |
| **Satisfaction** | Inflight satisfaction survey score | >4.2 / 5.0 |
| **Operational** | Cabin crew service time reduction | -15% per flight |
| **Operational** | Food waste reduction (pre-order accuracy) | -20% |
| **Sustainability** | Catering demand forecasting accuracy (pre-orders as demand signal) | >85% accuracy |
| **Sustainability** | Paper magazine elimination | 100% digital by Phase 1 |

---

## Technical Solution — How It All Works Under the Hood

The platform is built on an **offline-first, pre-computed architecture** designed to deliver a seamless experience even with limited inflight connectivity.

### Content Generation (Scheduled, Not On-Demand)

Content is **never generated per-request**. Instead, it is produced on scheduled cadences and cached:

| Content | Refresh Cadence | Source |
|---|---|---|
| Destination highlights, restaurants, transport | Every **2 weeks** per destination | Google Gemini AI |
| Flight details (crew, aircraft) | **Daily** — when crew and aircraft are allocated to flights | Airline operations systems |
| Weather forecast | Every **12 hours** | Google Gemini AI |
| Local news | Every **6 hours** (filtered for inflight safety) | Google Gemini AI (safety rules in prompt) |
| Music playlists | **Weekly** — curated by mood and destination, mixing decades and local artists | AI Music Curation Engine |
| Digital magazine articles | **Weekly** — AI-assisted editorial | Gemini + Editorial team |
| Food menu | **Weekly** or per season | Catering team |
| Translations (6 languages) | Triggered after any content update | Google Gemini AI |

### Delivery to Passengers — Silent Push & Edge Caching

**For passengers with the Vueling app:**
- **T-24h before flight**: A silent push notification triggers a background download of the entire content package (destination guide, magazine, music, weather, flight details, menu). Size: ~15-25 MB.
- **At boarding**: The experience loads instantly from the device — zero bandwidth needed. Everything works offline.

**For passengers without the app (WiFi portal):**
- **Before departure**: At the gate, ground WiFi pushes the full content package to an **onboard edge cache server** on the aircraft.
- **Onboard**: Passengers connect to inflight WiFi, enter their PNR, and the content is served from the local onboard server at LAN speed — no satellite bandwidth required for content.

### What Actually Uses Satellite Bandwidth

Only three things go over the satellite link during the flight:

| Data | Size | Frequency |
|---|---|---|
| Flight tracker updates (position, altitude, speed) | ~1 KB | Every 30 seconds |
| Food orders (JSON payload) | ~2 KB per order | Per order (~20/flight) |
| Payment transactions | ~1 KB per transaction | Per order |

**Total satellite bandwidth per flight: ~370 KB.** Less than a single webpage. Satellite costs are negligible.

### Food Orders & Payments

- **Pre-orders** (T-24h to T-1h): Processed over normal internet. Forwarded to the catering system at cutoff (T-6h). Cabin crew receives a per-seat manifest on their tablet.
- **Onboard orders**: Processed in real-time over the satellite link. Payment is tokenized (PCI-DSS compliant). Order goes to crew tablet, crew prepares and delivers to seat.

This architecture ensures the experience is **always fast, always available, and costs almost nothing to operate per passenger (~0.005 EUR).**

---

## POC Scope (What's Built Today)

- 3 destinations: Rome (FCO), London (LHR), Paris (CDG)
- 6 languages fully supported
- Single AI engine (Google Gemini 2.5 Flash) generates ALL content, weather, and news
- Complete API: one call returns the full experience
- All endpoints tested and working
- Ready for MWC demo

---

## Roadmap: POC to Platform

| Phase | What | When |
|---|---|---|
| **POC** (done) | Destination content + flight details, 3 cities, 6 languages | Feb 2026 |
| **Phase 1** | Mobile app integration + flight tracker + digital magazine | Q2 2026 |
| **Phase 2** | Food pre-order system + onboard ordering + payments | Q3 2026 |
| **Phase 3** | Music & audio playlists + full route network | Q4 2026 |
| **Phase 4** | Personalization engine (past trips, preferences, loyalty tier) | 2027 |

---

**Contact:** Product & Engineering Team
**Status:** POC Complete — Ready for Demo
**Date:** February 2026
