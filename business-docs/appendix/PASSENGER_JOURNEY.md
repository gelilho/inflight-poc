# Passenger Journey — Complete Trigger Flow

---

## Overview

```
T-24h          T-3h           T-0            T+15min        T+90min        LANDING
  |              |              |               |              |              |
  v              v              v               v              v              v
PRE-ORDER     AIRPORT        BOARDING        CRUISING       DESCENT        POST-FLIGHT
PUSH          PUSH           EXPERIENCE      FOOD ORDER     DESTINATION    NPS SURVEY
+ PRE-CACHE   + SNACK BAG   LOADS INSTANT   LIVE           DEEP DIVE
```

---

## Phase 1 — Pre-Flight (T-24h)

**Silent push**: Content package downloaded in background (~15-25 MB)
**Visible push**: "Flying to Rome tomorrow? Pre-order your onboard menu"

```
Passenger taps → Opens menu → Browses → Orders → Pays → "Your lunch is booked!"
```

Pre-order forwarded to catering system.

---

## Phase 2 — At the Airport (T-3h to T-0)

| Passenger Action | System Response |
|---|---|
| Checks in | Push: "Checked in! Explore Rome while you wait" |
| Drops luggage | Push: "Luggage done! Pre-order a snack bag?" |
| Passes security | Push: "You're through! Add a picnic bag to your flight?" |
| At the gate | Full experience already loaded — browse destination, music, magazine |

---

## Phase 3 — Boarding (T-0)

Three entry points:

| Method | How It Works |
|---|---|
| **Vueling App** | Detects inflight WiFi → loads pre-cached experience instantly |
| **WiFi Portal** | Connect to WiFi → enter PNR → experience served from edge cache |
| **Seatback IFE** | Scan boarding pass QR → experience on screen |

What they see: Welcome + crew names + aircraft info + [Explore Rome] [Magazine] [Music] [Flight Map] [Order Food] [FAQ]

---

## Phase 4 — In-Flight (T+15min onwards)

**Content (offline):** Destination highlights, restaurants, transport, weather, news, magazine, music, aircraft, crew, FAQ

**Transactional (WiFi):** Food ordering → digital menu → cart → pay → crew delivers to seat

Pre-orders delivered first. Then live orders by seat number.

---

## Phase 5 — Descent (T-30min)

Notification: "30 minutes to Rome!"
- Weather on arrival
- Transport: Leonardo Express train, 32 min to Termini
- Baggage: Carousel 5
- Emergency: 112 (police), 118 (ambulance)
- Vueling: +34 931 518 158

---

## Phase 6 — Post-Flight

Push: "Welcome to Rome! Rate your experience?"
- 1-5 star rating
- NPS question
- Optional feedback
- Destination guide remains accessible for the trip

---

## All Trigger Points

| Trigger | When | WiFi Needed |
|---|---|---|
| Silent push (pre-cache) | T-24h | Yes (home WiFi) |
| Pre-order notification | T-24h | Yes |
| Check-in push | T-3h | Yes |
| Security push | T-2h | Yes |
| App WiFi detection | Boarding | No (pre-cached) |
| WiFi portal login | Boarding | Yes (edge cache) |
| Food ordering enabled | T+15min | Yes (transactional) |
| Descent notification | T-30min | No (pre-cached) |
| Landing NPS survey | After landing | Yes |

---

## Offline vs. Online

| Content | Offline | Needs WiFi |
|---|---|---|
| Destination, restaurants, transport | Pre-cached | No |
| Emergency contacts, Vueling helpline | Pre-cached | No |
| Weather, news | Pre-cached | No |
| Connecting flights (gate, terminal) | Pre-cached | No |
| Flight advisories (airplane mode, etc.) | Pre-cached | No |
| Magazine, music | Pre-cached | No |
| Aircraft info, crew names | Pre-cached | No |
| FAQ content | Pre-cached | No |
| **Flight tracker (live map)** | — | **Yes (small packets)** |
| **Food ordering + payments** | — | **Yes (transactional)** |
