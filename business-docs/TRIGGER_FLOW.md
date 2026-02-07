# Inflight Experience — Complete Trigger Flow

## The Full Passenger Journey

This document maps **every touchpoint** from 24 hours before the flight to landing — showing how the experience is triggered, what content is served, and how food ordering fits into the timeline.

---

## Journey Overview

```
T-24h          T-3h           T-0            T+15min        T+90min        LANDING
  |              |              |               |              |              |
  v              v              v               v              v              v
PRE-ORDER     AIRPORT        BOARDING        CRUISING       DESCENT        POST-FLIGHT
PUSH          PUSH           EXPERIENCE      FOOD ORDER     DESTINATION    NPS SURVEY
              + SNACK BAG    LOADS           LIVE           DEEP DIVE
```

---

## PHASE 1 — PRE-FLIGHT (T-24h to T-3h)

### Trigger: Push Notification — Day Before

```
SYSTEM                                    PASSENGER
  |                                          |
  |-- Flight VY71299 departs tomorrow ------>|
  |-- Check: passenger has app installed --->|
  |-- Send silent push: pre-cache content -->|  (content downloaded in background)
  |                                          |
  |-- T-24h: Push notification ------------->|  "Flying to Rome tomorrow!
  |                                          |   Pre-order your onboard menu"
  |                                          |
  |                                     [Passenger taps notification]
  |                                          |
  |                                     [Opens menu in app]
  |                                     [Browses snacks, meals, drinks]
  |                                     [Places pre-order, pays in-app]
  |                                          |
  |<-- Pre-order received + payment ---------|
  |-- Confirm order: "Your lunch is booked!"-|
  |-- Forward order to catering system ----->|
```

**Content pre-cached via silent push:**
- Destination guide (highlights, restaurants, transport)
- Digital magazine articles
- Music playlists (audio files)
- Weather forecast
- Flight details (aircraft, crew — if allocated)
- Emergency contacts

### Trigger: Airport Touchpoints (T-3h to T-0)

```
PASSENGER ACTION                          SYSTEM RESPONSE
  |                                          |
  |-- Checks in (app or counter) ---------->|
  |                                          |-- Push: "Checked in! Explore Rome
  |                                          |   while you wait" (destination preview)
  |                                          |
  |-- Drops luggage at belt --------------->|
  |                                          |-- (optional) Push: "Luggage done!
  |                                          |   Pre-order a snack bag for your flight?"
  |                                          |
  |-- Passes security checkpoint ---------->|
  |                                          |-- Push: "You're through! 2 hours to go.
  |                                          |   Add a picnic bag to your flight?"
  |                                          |
  |-- At the gate, waiting ---------------->|
  |                                          |-- Content available: full destination
  |                                          |   guide, magazine, music already loaded
```

**Pre-order options at this stage:**
- Snack bag: curated selection (sandwich, drink, snack) — picked up at gate or delivered onboard
- Full meal: hot/cold options — delivered to seat after takeoff
- Drinks package: selection of beverages for the flight

---

## PHASE 2 — BOARDING (T-0)

### Trigger: Inflight WiFi Connect or App Detection

```
PASSENGER                           SYSTEM                         CONTENT
  |                                    |                              |
  |-- Boards aircraft ----------------->|                              |
  |-- Sits in seat 14D ---------------->|                              |
  |                                    |                              |
  |  OPTION A: Opens Vueling app       |                              |
  |  App detects inflight WiFi SSID -->|-- Activate experience ------>|
  |                                    |                              |
  |  OPTION B: Connects to WiFi       |                              |
  |  WiFi portal asks for PNR -------->|-- Lookup booking ----------->|
  |                                    |                              |
  |  OPTION C: Seatback IFE screen    |                              |
  |  Scans boarding pass QR ---------->|-- Identify passenger ------->|
  |                                    |                              |
  |                                    |-- Load pre-cached content -->|
  |                                    |                              |
  |<-- Full experience displayed ------|<-- Content package -----------|
  |                                    |                              |
  |  WHAT THEY SEE:                    |                              |
  |  - Welcome, Maria!                |                              |
  |  - Your flight VY71299 to Rome    |                              |
  |  - Captain Carlos Martinez        |                              |
  |  - Aircraft: Spirit of Barcelona  |                              |
  |  - [Explore Rome] [Magazine]      |                              |
  |  - [Music] [Flight Map]           |                              |
  |  - [Order Food] [Your Pre-order]  |                              |
```

**Key architectural decision:**
- If app installed: content is **already pre-cached** on device. Loads instantly. Zero bandwidth.
- If no app (WiFi portal): content served from **onboard edge cache server**. Minimal satellite data transfer.
- Flight tracker data: small real-time packets via satellite — position, altitude, speed (~1KB every 30 seconds).

---

## PHASE 3 — IN-FLIGHT EXPERIENCE (T+15min onwards)

### Trigger: Seatbelt Sign Off / Cruising Altitude

```
PASSENGER                           SYSTEM
  |                                    |
  |  CONTENT BROWSING (offline-capable)|
  |  ================================ |
  |  - Discover Rome: 5 highlights    |
  |  - Restaurants: 3 local picks     |
  |  - Transport: train/bus/taxi      |
  |  - Weather: 3-day forecast        |
  |  - News: 5 curated headlines      |
  |  - Magazine: travel articles      |
  |  - Music: curated playlist        |
  |  - Flight Map: live position      |
  |  - Aircraft info: A320neo details |
  |                                    |
  |  FOOD ORDERING (requires WiFi)    |
  |  ================================ |
  |  - Browse digital menu with photos|
  |  - Tap item -> Add to cart        |
  |  - Cart review -> Pay in-app      |
  |  - Order sent to cabin crew tablet|
  |                                    |
  |                                    |-- Order notification to crew -->
  |                                    |-- Crew confirms + prepares -->
  |                                    |-- Crew delivers to seat 14D -->
  |                                    |
  |<-- "Your order is on its way!" ----|
  |                                    |
  |  PRE-ORDER DELIVERY               |
  |  ================================ |
  |  - Crew has pre-order manifest    |
  |  - Pre-orders delivered first     |
  |  - Then live orders by seat number|
```

### Food Order Technical Flow

```
PASSENGER APP          BACKEND (WiFi)         CREW TABLET          PAYMENT
     |                      |                      |                  |
     |-- Add to cart ------>|                      |                  |
     |-- Checkout --------->|                      |                  |
     |                      |-- Validate order --->|                  |
     |                      |-- Process payment ---|----------------->|
     |                      |<-- Payment confirmed-|<-----------------|
     |                      |-- Send to crew ----->|                  |
     |<-- Order confirmed --|                      |                  |
     |                      |                      |-- Prepare order  |
     |                      |                      |-- Deliver seat   |
     |<-- "Delivered!" -----|<-- Mark delivered ----|                  |
```

---

## PHASE 4 — DESCENT (T+90min / 30 min before landing)

### Trigger: Approaching Destination

```
SYSTEM                                    PASSENGER
  |                                          |
  |-- Flight entering descent phase -------->|
  |                                          |
  |-- Push/notification in app: ------------>|  "30 minutes to Rome!
  |                                          |   Here's your weather & transport info"
  |                                          |
  |-- Surface key content: ----------------->|  - Weather on arrival: 15C, partly cloudy
  |                                          |  - Transport: Leonardo Express train,
  |                                          |    32 min to Termini, every 15 min
  |                                          |  - Baggage: Carousel 5
  |                                          |  - Emergency: 112 (police), 118 (ambulance)
  |                                          |  - Vueling: +34 931 518 158
```

---

## PHASE 5 — POST-FLIGHT (Landing)

### Trigger: Aircraft Landed

```
SYSTEM                                    PASSENGER
  |                                          |
  |-- Flight landed at FCO ----------------->|
  |                                          |
  |-- Push: "Welcome to Rome!" ------------>|  "Hope you enjoyed your flight.
  |                                          |   Rate your experience?"
  |                                          |
  |                                     [Passenger rates 1-5 stars]
  |                                     [Optional: NPS question]
  |                                     [Optional: feedback text]
  |                                          |
  |<-- Rating + feedback received -----------|
  |-- Store in analytics ------------------->|
  |                                          |
  |-- Post-flight content still available -->|  Destination guide remains
  |                                          |  accessible for the trip duration
```

---

## All Trigger Points Summary

| Trigger | When | Channel | Content | Requires WiFi |
|---|---|---|---|---|
| Silent push (pre-cache) | T-24h | App background | All content downloaded silently | Yes (home WiFi) |
| Pre-order notification | T-24h | Push notification | Food menu | Yes |
| Check-in push | T-3h | Push notification | Destination preview | Yes |
| Luggage drop push | T-2.5h | Push notification | Snack bag offer | Yes |
| Security push | T-2h | Push notification | Snack bag reminder | Yes |
| App WiFi detection | T-0 (boarding) | Vueling app | Full experience | No (pre-cached) |
| WiFi portal login | T-0 (boarding) | Browser | Full experience | Yes (edge cache) |
| QR scan (IFE) | T-0 (boarding) | Seatback screen | Full experience | Yes (edge cache) |
| Seatbelt off | T+15min | In-app | Food ordering enabled | Yes (for orders) |
| Descent notification | T-30min landing | In-app | Weather + transport summary | No (pre-cached) |
| Landing push | After landing | Push notification | NPS survey | Yes |

---

## Offline vs. Online Content Matrix

| Content | Pre-cached (offline) | Requires real-time WiFi |
|---|---|---|
| Destination highlights | Pre-cached | No |
| Restaurants | Pre-cached | No |
| Transport options | Pre-cached | No |
| Emergency contacts | Pre-cached | No |
| Weather forecast | Pre-cached (refreshed if WiFi) | No |
| News | Pre-cached | No |
| Digital magazine | Pre-cached | No |
| Music playlists | Pre-cached (audio files) | No |
| Aircraft info | Pre-cached | No |
| Crew names | Pre-cached (updated daily) | No |
| **Flight tracker (live map)** | **No** | **Yes — small packets** |
| **Food ordering** | **Menu pre-cached, order requires** | **Yes — transactional** |
| **Payment processing** | **No** | **Yes — real-time** |
| **NPS survey submission** | **Stored locally, synced later** | **Queued if offline** |

---

## Edge Cache Architecture (Onboard)

```
GROUND                          AIRCRAFT                      PASSENGER
  |                                |                              |
  |-- Pre-flight: push content -->|                              |
  |   to onboard cache server     |                              |
  |   (via ground WiFi at gate)   |                              |
  |                                |                              |
  |                          [Onboard Edge Cache]                |
  |                          - All destination content           |
  |                          - Magazine articles                 |
  |                          - Music files                       |
  |                          - Menu with images                  |
  |                                |                              |
  |                                |<-- Passenger connects -------|
  |                                |-- Serve from local cache --->|
  |                                |   (no satellite needed)      |
  |                                |                              |
  |                          [Satellite link - minimal use]      |
  |<-- Food orders (small JSON) ---|                              |
  |-- Payment confirmations ------>|                              |
  |<-- Flight tracker updates -----|                              |
  |   (~1KB every 30 seconds)      |                              |
```

**This design minimizes satellite bandwidth costs by 90%+.**
Only transactional data (food orders, payments) and tiny flight tracker packets go over satellite.

---

**This complete flow is the blueprint for the Vueling Inflight Experience.**
**The POC proves the content generation and delivery engine. The rest is execution.**
