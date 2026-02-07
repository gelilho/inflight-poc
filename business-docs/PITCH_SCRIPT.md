# Pitch Script — Vueling Inflight Experience
### 7-minute pitch for leadership and investors
### Delivered as VP of Engineering & Product

---

## OPENING — THE HOOK (30 seconds)

"Last year, 34 million people flew with Vueling. Each one spent between one and three hours in our aircraft. That's over 60 million hours of undivided attention — a captive audience sitting in seats we own, connected to WiFi we provide, looking at screens we could fill.

And what did we give them? A paper magazine and a cart pushed down the aisle.

Today I'm going to show you how we change that. Completely."

---

## THE PROBLEM — MAKE THEM FEEL IT (1 minute)

"Let me paint the picture.

Maria books a flight to Rome. She checks in, she boards, she sits in 14D. For the next two hours, she scrolls Instagram, watches something she downloaded from Netflix, maybe naps. She doesn't interact with Vueling at all.

When she lands in Rome, she opens Google Maps. She searches 'best restaurants in Rome.' She googles 'how to get from Fiumicino to the city center.' She checks the weather on her phone's app. She does all of this on someone else's platform.

We had her for two hours. We gave her nothing. And then we lost her to Google.

Now imagine something worse. Maria has an emergency. She doesn't know the Italian emergency number. She doesn't know how to reach Vueling in Rome. The experience ended at the aircraft door.

And here's the business problem: food sales are low because the aisle cart is friction-heavy. Most passengers don't buy because the process is inconvenient. We're leaving millions of euros on the table.

This is the problem. No engagement. No content. No commerce. No connection."

---

## THE VISION — THE BIG PICTURE (1 minute 30 seconds)

"What if we reimagined the entire flight experience?

Not just a destination guide. A complete digital ecosystem that starts 24 hours before the flight and doesn't end until the passenger comes home.

Here's what we've designed — eight pillars of the Vueling Inflight Experience:

**One — Discover Your Destination.** AI-generated content: the top five places to visit, three restaurant recommendations, transport options from the airport, emergency contacts. All in the passenger's language. All fresh, all safe for inflight.

**Two — Live Flight Tracker.** Real-time map showing where you are — altitude, speed, time to arrival. Passengers love this. It's the single most-viewed feature on every airline that offers it.

**Three — Your Aircraft.** The model, the registration, the name — 'Spirit of Barcelona.' Make flying personal. Make it transparent.

**Four — Your Crew.** Captain's name, first officer, cabin crew. Humanize the experience. Passengers feel safer when they know who's flying them.

**Five — Weather and News.** Three-day forecast and curated local headlines — sports, culture, events. Only positive. No anxiety at altitude.

**Six — Digital Magazine.** Replaces the paper magazine. Saves printing costs, saves weight, saves trees. Better content, zero logistics.

**Seven — Music and Audio.** AI-curated playlists by mood and destination. Chill, upbeat, focus. A mix of decades and local artists. Refreshed weekly.

And **Eight — the one that pays for everything — Food and Snacks.**"

---

## THE REVENUE ENGINE — FOOD ORDERING (1 minute 30 seconds)

"This is where the business case gets exciting.

Today, food sales onboard depend on a cabin crew member pushing a cart down the aisle. The passenger has to decide on the spot, sometimes doesn't have cash, feels awkward ordering in a tight space. Conversion is low.

We flip this completely.

**Day before the flight.** Maria gets a push notification: 'Flying to Rome tomorrow? Pre-order your onboard menu now.' She opens the app, sees a beautiful digital menu with photos and descriptions, and orders a Mediterranean salad and a coffee. She pays right there. Done. That's guaranteed revenue before the plane even departs.

**At the airport.** After she drops her luggage or passes security, another notification: 'Two hours to go! Want a snack bag for the flight?' She adds a picnic bag — a curated selection of a sandwich, a drink, and a snack. Maybe she picks it up at the gate, maybe it's waiting at her seat.

**Onboard.** After takeoff, the food ordering goes live. She browses the digital menu on her phone, taps a chocolate croissant, pays in-app. The order goes directly to the crew tablet. They prepare it. They deliver it to seat 14D. No cart. No cash. No friction.

Here's why this is transformational:

Pre-orders mean guaranteed revenue — booked and paid before departure. Digital menus with photos increase average order value by 20 to 40 percent — that's proven in every industry that went from paper menus to digital. Cabin crew efficiency goes up — pre-orders are prepared in advance, reducing aisle passes and enabling faster turnarounds. And the data — we know exactly what passengers want. We optimize catering. We reduce food waste. We save money while making more.

This food vertical alone could pay for the entire platform."

---

## THE ARCHITECTURE — HOW WE BUILT IT (45 seconds)

"The technology behind this is clean and scalable.

The content engine uses Google Gemini — AI generates destination content, translates it, curates it. Destination content is refreshed every two weeks. Flight details are updated daily when crew and aircraft are assigned. News refreshes every six hours. Music playlists every week.

The key architectural insight is **offline-first**. The day before the flight, we send a silent push notification to the passenger's device. All content — destination guide, magazine, music — is pre-cached. When they board, everything loads instantly. Zero bandwidth.

For passengers without the app, the onboard WiFi serves from an edge cache server on the aircraft. Content is pre-loaded at the gate via ground WiFi. No satellite data needed for content.

The only things that go over satellite are tiny flight tracker packets — about one kilobyte every thirty seconds — and food orders with payments. That's it. We minimize bandwidth costs by over 90 percent.

This is not a bandwidth-heavy solution. It's an elegant, offline-first architecture."

---

## THE METRICS — HOW WE WIN (45 seconds)

"Let me tell you how we measure success.

**Engagement:** We're targeting 25 percent of passengers using the experience within six months. Average session time of 12 minutes. That's 12 minutes of Vueling-owned attention instead of Netflix or Instagram.

**Revenue:** 8 percent pre-order food conversion and 12 percent onboard ordering. At an average ticket of 8 to 12 euros, across 34 million passengers — the math speaks for itself. And average order value with digital menus goes up 30 percent versus aisle service.

**Satisfaction:** We expect a 5-point NPS lift for passengers who use the experience. Post-flight satisfaction score target: 4.2 out of 5.

**Operations:** 15 percent reduction in cabin crew aisle service time per flight. 20 percent food waste reduction from pre-order accuracy.

**Sustainability:** Full elimination of the paper magazine. That's tons of paper saved every year, plus weight savings that translate to fuel savings.

Every metric is measurable. Every metric is tied to a business outcome."

---

## THE DEMO (45 seconds)

"Let me show you what we've built.

_[Run live API call]_

Passenger Maria Garcia. Flight VY71299. Barcelona to Rome. Seat 14D. Spanish.

In thirty seconds: her crew names, the aircraft 'Spirit of Barcelona,' five highlights in Rome, three restaurants, how to get from Fiumicino to Termini, tomorrow's weather, five curated news headlines. All in Spanish.

This is the POC. It's live. It works. Three destinations, six languages, all APIs integrated.

Now imagine: add a music button. Add a magazine tab. Add an 'Order Food' button. That's Phase 2. And the architecture is ready for it."

---

## THE CLOSE — MAKE IT IRRESISTIBLE (30 seconds)

"Let me leave you with this.

No low-cost carrier in the world offers a personalized, AI-powered inflight experience. Not Ryanair. Not EasyJet. Not Wizz Air. No one.

Vueling can be first.

Content. Entertainment. Commerce. All from one booking number. The POC is proven. The architecture is designed. The revenue model is clear. The KPIs are defined.

Every flight is a canvas. Every passenger is an audience of one.

Let's build the future of flying. And let's do it first."

---

## Q&A PREP — EXPECT THESE QUESTIONS

**Q: What's the total investment needed?**
A: The POC was built in weeks with a small team. Phase 1 (app + tracker + magazine) needs 3-4 engineers for one quarter. Phase 2 (food ordering + payments) needs integration with catering and a payment gateway — that's a cross-functional team for one quarter. Total: under 12 months to full rollout, leveraging existing infrastructure.

**Q: How much revenue can the food vertical generate?**
A: Conservative estimate: if 8% of 34M passengers pre-order at avg. 10 EUR = ~27M EUR incremental per year. Plus onboard digital ordering. Plus reduced food waste savings. The food vertical alone has strong standalone ROI.

**Q: What about passengers without the app?**
A: The WiFi portal serves the same experience via browser. Content comes from the onboard edge cache — no app required. Music streaming would be app-only (for audio caching), but all other pillars work in browser.

**Q: How do food payments work at 35,000 feet?**
A: Payment processing goes over the satellite link. It's a small JSON payload — a few kilobytes. Same infrastructure airlines already use for in-flight credit card transactions. Latency is acceptable for food orders (not milliseconds-critical).

**Q: What about the catering logistics for pre-orders?**
A: Pre-orders are forwarded to the catering system at cutoff time (e.g., T-6h before flight). Catering prepares per-seat manifests. Cabin crew receives a tablet with the pre-order list. This integrates with existing catering workflows — it's an input channel, not a new logistics system.

**Q: What if the AI generates wrong content?**
A: Strict safety rules in every prompt. Content is regenerated on a cadence (not per-request), which means it can be spot-checked. For the POC we also filter news programmatically — no violence, no crime. At scale, a content review pipeline can be added as a quality gate.

**Q: How much does the AI cost?**
A: ~0.005 EUR per passenger for content generation. Since content is cached per destination (not per passenger), the actual cost is even lower — maybe 0.001 EUR amortized. Negligible at any scale.

**Q: What about data privacy / GDPR?**
A: We only use the booking number (PNR). No personal data is sent to any external API. The AI receives "Rome, Italy" — never passenger names, emails, or personal details. Food order data stays within Vueling systems. Fully GDPR compliant by design.

**Q: Can competitors copy this?**
A: They can try. But first-mover advantage in inflight digital experience is significant. The brand association — "Vueling is the airline that takes care of you" — compounds over time. And the data moat (passenger preferences, order history) grows with every flight.

**Q: What's the timeline to see revenue?**
A: Content experience (Phase 1): Q2 2026. Food ordering (Phase 2): Q3 2026. Revenue impact measurable by Q4 2026. This is fast.
