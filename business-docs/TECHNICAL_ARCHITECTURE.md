# Technical Architecture — Vueling Inflight Experience
### VP of Engineering & Product Perspective

---

## Architecture Philosophy

Three principles drive every decision:

1. **Offline-first** — The passenger experience must work without satellite connectivity
2. **Pre-computed, not on-demand** — Content is generated ahead of time, not per-request
3. **Minimal bandwidth** — Only transactional data (orders, payments, tracker) uses satellite

---

## System Overview

```
+===========================================================================+
|                        CONTENT GENERATION LAYER                           |
|                        (Scheduled / Batch Jobs)                           |
|                                                                           |
|  +-------------+  +-------------+  +-------------+  +----------------+   |
|  | DESTINATION  |  | FLIGHT      |  | NEWS        |  | MUSIC          |   |
|  | CONTENT      |  | DETAILS     |  | AGGREGATOR  |  | CURATOR        |   |
|  | GENERATOR    |  | UPDATER     |  |             |  |                |   |
|  +------+------+  +------+------+  +------+------+  +-------+-------+   |
|         |                |                |                  |            |
|    Every 2 weeks    Daily (crew/     Every 6 hours      Weekly           |
|    per destination   aircraft          per destination   per mood/dest   |
|                     allocation)                                          |
+=========+===============+===============+==================+=============+
          |               |               |                  |
          v               v               v                  v
+===========================================================================+
|                        CONTENT STORE (Cache Layer)                        |
|                                                                           |
|  +-------------------------------------------------------------------+   |
|  |                    CDN / Content Database                          |   |
|  |                                                                   |   |
|  |  Per Destination:                     Per Flight (daily):         |   |
|  |  - highlights (5)                     - aircraft details          |   |
|  |  - restaurants (3)                    - cockpit crew              |   |
|  |  - transport options                  - cabin crew                |   |
|  |  - emergency contacts                 - gates, times             |   |
|  |  - weather (refreshed 12h)            - baggage carousel         |   |
|  |  - news (refreshed 6h)                                           |   |
|  |  - magazine articles                  Per Mood/Destination:      |   |
|  |  - translations (6 languages)         - music playlists          |   |
|  |                                       - audio files              |   |
|  +-------------------------------------------------------------------+   |
+===============+==================+========================================+
                |                  |
        +-------+------+   +------+-------+
        |              |   |              |
        v              v   v              v
+===============+  +==========================+
| SILENT PUSH   |  | ONBOARD EDGE CACHE       |
| TO DEVICES    |  | (Aircraft Server)         |
| (T-24h)       |  |                          |
|               |  | Pre-loaded at gate via    |
| Content pre-  |  | ground WiFi before        |
| cached on     |  | departure                 |
| passenger     |  |                          |
| devices via   |  | Serves passengers who     |
| app           |  | use WiFi portal (no app)  |
+-------+-------+  +------------+-------------+
        |                        |
        v                        v
+===========================================================================+
|                        PASSENGER DEVICE LAYER                             |
|                                                                           |
|  +--------------------+          +--------------------+                   |
|  | VUELING APP        |          | WIFI PORTAL        |                   |
|  | (Pre-cached)       |          | (Edge-cached)      |                   |
|  |                    |          |                    |                   |
|  | - All content      |          | - All content      |                   |
|  |   loads offline    |          |   from onboard     |                   |
|  | - Music plays      |          |   server           |                   |
|  |   offline          |          | - No music          |                   |
|  | - Food ordering    |          |   streaming         |                   |
|  |   via WiFi         |          | - Food ordering     |                   |
|  | - Flight tracker   |          |   via WiFi          |                   |
|  |   via WiFi         |          | - Flight tracker    |                   |
|  +--------------------+          +--------------------+                   |
+===========================================================================+
                    |                          |
                    v                          v
+===========================================================================+
|                        REAL-TIME LAYER (Satellite)                        |
|                        (Minimal bandwidth usage)                          |
|                                                                           |
|  +----------------+  +----------------+  +--------------------+          |
|  | FLIGHT TRACKER |  | FOOD ORDERS    |  | PAYMENT GATEWAY    |          |
|  | ~1KB / 30 sec  |  | ~2KB per order |  | ~1KB per txn       |          |
|  | (position,     |  | (JSON payload) |  | (tokenized card    |          |
|  |  altitude,     |  |                |  |  processing)       |          |
|  |  speed, ETA)   |  |                |  |                    |          |
|  +----------------+  +----------------+  +--------------------+          |
+===========================================================================+
```

---

## Content Generation Cadence

The key insight: **we don't generate content per-passenger or per-request.** We generate it on a scheduled cadence and cache it. This means:

- Near-zero latency for the passenger (content is already ready)
- Near-zero cost per passenger (content is amortized across all passengers on that route)
- Quality control: content can be reviewed between refresh cycles

### Cadence Table

| Content Type | Generation Trigger | Refresh Cadence | AI Model | Storage |
|---|---|---|---|---|
| **Destination Highlights** | New destination added or refresh cycle | Every **2 weeks** | Gemini 2.5 Flash | CDN + Device Cache |
| **Restaurant Recommendations** | Same as highlights | Every **2 weeks** | Gemini 2.5 Flash | CDN + Device Cache |
| **Transport Options** | Same as highlights | Every **2 weeks** | Gemini 2.5 Flash | CDN + Device Cache |
| **Emergency Contacts** | Manually maintained | On change only | N/A (static data) | CDN + Device Cache |
| **Flight Details** (crew, aircraft) | Daily crew/aircraft allocation | **Daily** (batch at 06:00) | N/A (from ops system) | CDN + Device Cache |
| **Weather Forecast** | Scheduled job | Every **12 hours** | OpenWeatherMap API | CDN + Device Cache |
| **News Headlines** | Scheduled job | Every **6 hours** | NewsAPI + Gemini filter | CDN + Device Cache |
| **Digital Magazine** | Editorial + AI assisted | **Weekly** new articles | Gemini + Editorial | CDN + Device Cache |
| **Music Playlists** | AI curation engine | **Weekly** per mood/dest | AI Music Curation | CDN + Audio Cache |
| **Translations** | After any content refresh | Triggered by content update | Gemini 2.5 Flash | CDN + Device Cache |
| **Food Menu** | Catering team updates | **Weekly** or per season | N/A (manual + photos) | CDN + Device Cache |

---

## Offline-First Delivery Strategy

### For Passengers WITH the Vueling App

```
TIMELINE                ACTION                              RESULT
T-24h     Silent push notification sent              Content package downloaded
          (destination, magazine, music,             in background over home WiFi
          weather, news, flight details,             or mobile data
          menu photos)
          Size: ~15-25 MB (mostly music/images)

T-0       Passenger opens app onboard               Everything loads instantly
          App detects inflight WiFi SSID             from local device storage
          No network request needed for content      Zero bandwidth used

Onboard   Food order / Flight tracker               Small packets over WiFi
          Only these features need connectivity      to satellite link
```

### For Passengers WITHOUT the App (WiFi Portal)

```
TIMELINE                ACTION                              RESULT
Pre-flight  Ground WiFi at gate pushes content       Edge cache server on aircraft
            to onboard server                        has all content pre-loaded
            (~500 MB total for all destinations      Ready to serve
            on that flight's route)

T-0         Passenger connects to inflight WiFi      WiFi portal login with PNR
            Browser loads experience                 Content served from onboard
                                                     server (LAN speed, no satellite)

Onboard     Food order / Flight tracker              Same satellite path as app users
```

### Bandwidth Budget (Per Flight)

| Data Type | Direction | Size | Frequency | Total per 2h flight |
|---|---|---|---|---|
| Flight tracker | Aircraft -> Ground | 1 KB | Every 30s | ~240 KB |
| Food orders | Aircraft -> Ground | 2 KB per order | ~20 orders/flight | ~40 KB |
| Payment transactions | Bidirectional | 1 KB per txn | ~20 txns/flight | ~40 KB |
| NPS responses | Aircraft -> Ground | 0.5 KB | End of flight | ~50 KB |
| **Content (destination, magazine, music)** | **None** | **0** | **Pre-cached** | **0 KB** |
| **TOTAL satellite bandwidth per flight** | | | | **~370 KB** |

**370 KB per flight.** That's less than a single webpage. Satellite costs are negligible.

---

## Food Ordering System — Technical Design

```
+------------------+     +-------------------+     +------------------+
|  PASSENGER APP   |     |  ONBOARD SERVER   |     |  CREW TABLET     |
|                  |     |  (Edge)           |     |                  |
|  - Browse menu   |---->|  - Validate order |---->|  - Order queue   |
|  - Add to cart   |     |  - Queue order    |     |  - Seat number   |
|  - Checkout      |     |  - Process payment|     |  - Items ordered |
|  - Pay           |     |    (via satellite)|     |  - Mark prepared |
|                  |<----|  - Confirm order  |     |  - Mark delivered|
+------------------+     +-------------------+     +------------------+
                                |
                                | Satellite (only for payment)
                                v
                         +-------------------+
                         | PAYMENT GATEWAY   |
                         | (Ground)          |
                         |                   |
                         | - Tokenized card  |
                         | - Authorize       |
                         | - Confirm         |
                         +-------------------+
```

### Order States

```
PLACED --> PAYMENT_PENDING --> PAID --> PREPARING --> READY --> DELIVERED
```

### Pre-Order Flow (T-24h to T-6h)

```
PASSENGER APP          VUELING BACKEND         CATERING SYSTEM
     |                      |                       |
     |-- Pre-order -------->|                       |
     |-- Payment ---------->|                       |
     |<-- Confirmed --------|                       |
     |                      |                       |
     |              (T-6h cutoff)                   |
     |                      |-- Manifest ---------->|
     |                      |   (per-seat orders)   |
     |                      |                       |-- Prepare orders
     |                      |                       |-- Load on aircraft
     |                      |                       |
     |              (Boarding)                      |
     |                      |-- Manifest to crew -->|
     |                      |   tablet              |
```

---

## Music Curation Engine

### How Playlists Are Generated

```
INPUTS                          AI CURATION                     OUTPUT
                                ENGINE
- Destination city      ------>
- Mood (chill, upbeat,  ------> Generate playlist    ---------> Playlist JSON
  focus, local vibes)           - Mix decades (60s-2020s)        + Audio file URLs
- Duration target       ------> - Include local artists
  (1h, 2h, 3h)                 - Genre diversity
- Content safety rules  ------> - No explicit content
                                - Uplifting tone
```

### Cadence

- Playlists regenerated **weekly** per mood-destination combination
- New music added as catalog expands
- Audio files stored on CDN and pre-cached on devices / onboard server
- Typical playlist: 15-20 songs (~60-80 MB compressed audio)

---

## Integration Points

| System | Integration Type | Direction | Frequency |
|---|---|---|---|
| **Amadeus / Navitaire** (Booking) | API | Read | Per PNR lookup |
| **Crew Management System** | Batch file / API | Read | Daily at 06:00 |
| **Aircraft Assignment System** | Batch file / API | Read | Daily at 06:00 |
| **Catering System** | API | Write (manifests) | T-6h before flight |
| **Payment Gateway** (Stripe/Adyen) | API | Bidirectional | Real-time per order |
| **Google Gemini** | API | Read | Per content refresh cycle |
| **OpenWeatherMap** | API | Read | Every 12 hours |
| **NewsAPI.org** | API | Read | Every 6 hours |
| **Apple APNS / Google FCM** | Push | Write | T-24h silent push |
| **Onboard Edge Cache** | File sync | Write | Pre-departure at gate |
| **Analytics Platform** | Events | Write | Continuous (batched) |

---

## Scalability

| Dimension | POC (Today) | Phase 1-2 | Full Scale |
|---|---|---|---|
| Destinations | 3 | 50+ | All Vueling routes (~180) |
| Languages | 6 | 6 | 10+ (add Portuguese, German, Dutch, etc.) |
| Content refresh | On-demand | Scheduled cadence | Fully automated pipeline |
| Passengers/day | Demo | 10K | 93K (34M/year) |
| Food orders/day | N/A | Pilot routes | Network-wide |
| Music playlists | N/A | 5 moods x 50 destinations | Full catalog |
| Edge cache servers | N/A | 10 aircraft pilot | Full fleet (~120 aircraft) |

---

## Security & Privacy

| Concern | How We Handle It |
|---|---|
| **GDPR** | Only PNR used for personalization. No PII sent to external APIs. AI receives "Rome, Italy" not passenger names. |
| **Payment data** | Tokenized via PCI-DSS compliant gateway (Stripe/Adyen). No card numbers stored. |
| **Content safety** | AI prompts enforce strict inflight rules. Programmatic news filtering. Review pipeline at scale. |
| **Data at rest** | Pre-cached content on devices is non-sensitive (destination info, music). No personal data cached. |
| **Onboard server** | Edge cache contains only public content. No passenger data. Wiped and refreshed per flight cycle. |

---

## Cost Model (Per Passenger)

| Component | Cost | Notes |
|---|---|---|
| AI content generation | ~0.001 EUR | Amortized across all passengers on route |
| Weather API | ~0.0001 EUR | Amortized (cached per destination) |
| News API | ~0.0001 EUR | Amortized (cached per destination) |
| Silent push notification | ~0.0001 EUR | Standard push costs |
| Satellite bandwidth | ~0.002 EUR | Only tracker + orders (~370 KB/flight) |
| CDN storage + delivery | ~0.001 EUR | Pre-cached content delivery |
| **TOTAL per passenger** | **~0.005 EUR** | **Less than half a cent** |

Against food pre-order revenue of 0.80-1.20 EUR per passenger (8% conversion x 10 EUR avg), the ROI is **160x to 240x**.

---

**This architecture is designed to scale from POC to full fleet with minimal rearchitecting.**
**The hardest problems (AI content, offline delivery, edge caching) are solved in the design.**
**What remains is integration and execution.**
