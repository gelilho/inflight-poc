# System Architecture — Vueling Inflight Experience

---

## Two Repos, One Experience

The POC is built as two independent projects that work together:

```
┌──────────────────────┐         ┌──────────────────────────┐
│   inflight-ui-poc    │  HTTP   │     inflight-poc          │
│   React + Vite       │ ──────→ │     FastAPI + Gemini      │
│   :3000              │         │     :8000                  │
└──────────────────────┘         └──────────────────────────┘
        │                                   │
        │ fallback-data.ts                  └── Gemini 2.5 Flash
        │ (pre-cached data)                     (single AI engine: highlights,
        └── demo never breaks                    restaurants, weather, news,
                                                 transport, translations)
```

| Repo | Tech | Role |
|---|---|---|
| **inflight-poc** | Python, FastAPI, Pydantic | Backend API — data, AI content generation, translation |
| **inflight-ui-poc** | React, Vite, TypeScript | Frontend UI — passenger-facing screens |

**Fallback-first design**: The UI loads with pre-cached data instantly, then upgrades to live API data. If any API call fails, the cached data stays. The demo never breaks.

---

## What Connects to the API

| Screen | Endpoint | Speed |
|---|---|---|
| Crew + Aircraft + Connections | `/api/v1/flight/{number}/{date}` | Fast (CSV lookup) |
| Flight Advisories | `/api/v1/flight/advisories` | Fast (static) |
| Highlights + Restaurants | `/api/v1/destination/{code}/content/{lang}` | Slow first call (Gemini AI) |
| Emergency | `/api/v1/destination/{code}/content/{lang}` | Slow first call (Gemini AI) |
| Weather | `/api/v1/destination/{code}/weather/{lang}` | Fast (Gemini, cached) |
| News | `/api/v1/destination/{code}/news/{lang}` | Fast (Gemini, cached) |

API-driven static data: FlightInfo, BaggageInfo, ConnectingFlights, FlightAdvisories.

Static screens (no API): WelcomeHeader, FlightMap, Transport, Products, Entertainment, Feedback, Magazine, Checkout.

---

## Full Platform Architecture (Production Vision)

```
+===========================================================================+
|                    CONTENT GENERATION LAYER (Scheduled)                    |
|                                                                           |
|  +-------------+  +-------------+  +----------+  +--------+  +---------+ |
|  | DESTINATION  |  | FLIGHT      |  | NEWS +   |  | MUSIC  |  | FAQ     | |
|  | CONTENT      |  | DETAILS     |  | WEATHER  |  | ENGINE |  | INDEXER | |
|  | (Gemini AI)  |  | (Ops data)  |  |(Gemini)  |  | (AI)   |  |(Vueling)| |
|  +------+------+  +------+------+  +----+-----+  +---+----+  +----+----+ |
|         |                |               |            |            |      |
|    Every 2 weeks    Daily           Every 6h      Weekly     On change   |
+=========+===============+===============+============+============+=======+
          |               |               |            |            |
          v               v               v            v            v
+===========================================================================+
|                    CONTENT STORE (CDN / Cache Database)                    |
|                                                                           |
|  Per Destination:            Per Flight (daily):     Shared:             |
|  - highlights (5)            - aircraft details      - music playlists   |
|  - restaurants (3)           - cockpit crew          - FAQ index         |
|  - transport options         - cabin crew            - magazine articles |
|  - emergency contacts        - gates, times          - food menu         |
|  - weather (12h refresh)     - baggage carousel                         |
|  - news (6h refresh)                                                    |
|  - translations (6 langs)                                               |
+====================+======================+===============================+
                     |                      |
              +------+------+        +------+-------+
              v             v        v              v
     +===============+  +==========================+
     | SILENT PUSH   |  | ONBOARD EDGE CACHE       |
     | TO DEVICES    |  | (Aircraft Server)         |
     | (T-24h)       |  |                          |
     |               |  | Pre-loaded at gate via    |
     | All content   |  | ground WiFi               |
     | pre-cached    |  |                          |
     | on passenger  |  | Serves WiFi portal       |
     | device        |  | users (no app needed)    |
     +-------+-------+  +------------+-------------+
             |                        |
             v                        v
+===========================================================================+
|                    PASSENGER DEVICE LAYER                                  |
|                                                                           |
|  +--------------------+          +--------------------+                   |
|  | VUELING APP        |          | WIFI PORTAL        |                   |
|  | (Pre-cached)       |          | (Edge-cached)      |                   |
|  |                    |          |                    |                   |
|  | All content offline|          | All content from   |                   |
|  | Music offline      |          | onboard server     |                   |
|  | Food ordering WiFi |          | Food ordering WiFi |                   |
|  | Flight tracker WiFi|          | Flight tracker WiFi|                   |
|  +--------------------+          +--------------------+                   |
+===========================================================================+
             |                        |
             v                        v
+===========================================================================+
|                    REAL-TIME LAYER (Satellite — Minimal)                   |
|                                                                           |
|  +----------------+  +----------------+  +--------------------+          |
|  | FLIGHT TRACKER |  | FOOD ORDERS    |  | PAYMENT GATEWAY    |          |
|  | ~1KB / 30 sec  |  | ~2KB per order |  | ~1KB per txn       |          |
|  +----------------+  +----------------+  +--------------------+          |
|                                                                           |
|  TOTAL PER FLIGHT: ~370 KB  (less than one webpage)                      |
+===========================================================================+
```

---

## Content Generation Cadence

| Content | Cadence | Why This Cadence |
|---|---|---|
| **Destination content** | Every 2 weeks | Cities don't change fast; AI quality is better with review cycles |
| **Flight details** | Daily at 06:00 | Crew and aircraft are assigned to flights daily |
| **Weather** | Every 12 hours | Forecasts update twice daily; sufficient for 3-day outlook |
| **News** | Every 6 hours | Keep headlines fresh; filter for inflight safety each cycle |
| **Music playlists** | Weekly | Fresh enough to feel curated; stable enough to pre-cache |
| **Digital magazine** | Weekly | Editorial cadence; AI-assisted article generation |
| **FAQ content** | On change | Synced from Vueling's FAQ database when policies update |
| **Food menu** | Weekly / seasonal | Catering team manages; synced to onboard stock |
| **Translations** | After any update | Auto-triggered when source content refreshes |

---

## Offline Delivery Strategy

| Channel | How | When |
|---|---|---|
| **Vueling App** | Silent push → ~15-25 MB pre-cached on device | T-24h |
| **WiFi Portal** | Ground WiFi → onboard edge cache (~500 MB) | Pre-departure |

All content works offline. Only live tracker, food orders, and payments use satellite. **Total: ~370 KB per flight.**

---

## Food Ordering — Technical Flow

```
PASSENGER APP         ONBOARD SERVER          CREW TABLET         PAYMENT
     |                     |                      |                  |
     |-- Add to cart ----->|                      |                  |
     |-- Checkout -------->|                      |                  |
     |                     |-- Validate order --->|                  |
     |                     |-- Process payment ---|----------------->|
     |                     |<-- Confirmed --------|<-----------------|
     |                     |-- Send to crew ----->|                  |
     |<-- "Order confirmed"|                      |                  |
     |                     |                      |-- Prepare        |
     |                     |                      |-- Deliver seat   |
     |<-- "Delivered!" ----|<-- Mark delivered ----|                  |
```

**Pre-orders** (T-24h to T-1h): Processed over normal internet. Forwarded to catering at T-6h. Crew receives per-seat manifest on tablet.

**Onboard orders**: Real-time over satellite. Tokenized payment (PCI-DSS). ~2KB per order.

---

## Cost Per Passenger

| Component | Cost |
|---|---|
| AI content generation (amortized) | ~0.001 EUR |
| Weather + News APIs (amortized) | ~0.0002 EUR |
| Silent push notification | ~0.0001 EUR |
| Satellite bandwidth | ~0.002 EUR |
| CDN delivery | ~0.001 EUR |
| **TOTAL** | **~0.005 EUR** |

Against food revenue of 0.80-1.20 EUR per passenger (8% conversion x 10 EUR), the **ROI is 160x to 240x**.

---

**Three core principles: Offline-first. Pre-computed. Minimal satellite.**
**This architecture scales from POC to full fleet without rearchitecting.**
