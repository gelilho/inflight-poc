# Pitch Script — Vueling Inflight Experience
### 7-minute pitch for MWC Barcelona 2026
### Delivered as VP of Engineering & Product

---

## OPENING — THE HOOK (30 seconds)

"Last year, 34 million people flew with Vueling. Each one spent between one and three hours in our aircraft. That's over 60 million hours of undivided attention — a captive audience sitting in seats we own, looking at screens we could fill.

And what did we give them? A paper magazine and a cart pushed down the aisle.

Today I'm going to show you how we change that. Completely."

---

## THE PROBLEM (1 minute)

"Angel books a flight to Rome. He checks in, boards, sits in 14D. For the next two hours, he scrolls Instagram, watches something he downloaded from Netflix, maybe naps. He doesn't interact with Vueling at all.

When he lands in Rome, he opens Google. He searches for restaurants. He googles how to get from Fiumicino to the city center. He checks the weather. All of this on someone else's platform.

We had her for two hours. We gave her nothing. And then we lost her to Google.

And here's the business angle: food sales are low because most passengers skip buying simply because the ordering experience isn't convenient enough. We're leaving millions on the table.

No engagement. No content. No commerce. No connection."

---

## THE VISION (1 minute 30 seconds)

"We built a complete digital ecosystem. Eleven pillars:

**Food & Snacks** — the revenue engine. Pre-order the day before. Order onboard from your phone. Delivered to your seat. No cart. No cash. No friction.

**Your Aircraft and Your Crew** — know you're flying on the 'Spirit of Barcelona,' know your captain's name. Make flying personal.

**Live Flight Tracker** — see where you are on a real-time map. Passengers love this.

**Discover Your Destination** — five must-see places, three restaurant picks, all AI-generated, in their language.

**Getting to the City** — how to get from the airport to the center, with the option to book your transfer.

**Peace of Mind** — every emergency contact and the Vueling helpline, always accessible.

**Weather and News** — forecast and curated local headlines. Only positive, safe content.

**Music** — AI-curated playlists personalized by destination. Discover the soundtrack of Rome before you land. Local artists mixed with global hits across decades.

**Digital Magazine** — bringing back the spirit of the beloved Ling magazine, reborn in digital form. Travel stories, tips, Vueling news.

And **FAQ & Help** — a searchable Vueling knowledge base. Baggage rules, rebooking, loyalty questions — answers instantly without calling anyone."

---

## THE FOOD REVENUE ENGINE (1 minute)

"Let me zoom into the one that pays for everything.

Day before the flight. Angel gets a push notification: 'Flying to Rome tomorrow? Pre-order your onboard menu.' He opens the app, sees a beautiful menu with photos, orders a Mediterranean salad and a coffee. Paid. Done. That's guaranteed revenue before the plane departs.

At the airport, after security: 'Two hours to go! Want a snack bag?' He adds a picnic selection.

Onboard, after takeoff: she browses the digital menu, taps a chocolate croissant, pays in-app. The order goes to the crew tablet. They deliver to 14D.

Pre-orders are a game-changer. Not just for revenue — they're a demand signal. We know what to load on the plane. We optimize catering. We reduce food waste. We save money while making more.

Digital menus with photos increase average order value by 20 to 40 percent. That's proven in every industry that went from paper to digital."

---

## THE ARCHITECTURE (45 seconds)

"The technology is clean.

Google Gemini generates destination content, translates it, curates it. Content is pre-computed on a schedule — destinations every two weeks, flights daily, news every six hours, music weekly. Nothing is generated per-request.

The key insight is offline-first. Day before the flight, a silent push notification downloads the entire content package to the passenger's device. When they board, everything loads instantly. Zero bandwidth.

For passengers without the app, an onboard edge cache server at the aircraft has everything pre-loaded from ground WiFi at the gate.

Total satellite bandwidth per flight: 370 kilobytes. That's less than a single webpage. Only food orders, payments, and tiny flight tracker packets go over satellite.

The cost per passenger? Half a cent. The food revenue per passenger? Orders of magnitude higher."

---

## THE METRICS (30 seconds)

"25 percent activation in six months. 12 minutes average session. 8 percent pre-order food conversion. Plus 30 percent average order value uplift. Plus 5 NPS points. Minus 15 percent crew aisle time. Minus 20 percent food waste.

Every metric is measurable. Every metric is tied to a business outcome."

---

## THE FUTURE — HYPERPERSONALIZATION (45 seconds)

"But here's where it gets truly exciting.

Every interaction with this platform is a data point. Over time, we learn. Maria always orders Mediterranean — we suggest it first. She reads about historical sites — we highlight museums. She's flown twelve times this year and orders food every flight — she gets a personalized welcome and priority offers.

The vision is to treat every passenger like a VIP. Whether they're flying for holidays, leisure, or business. Personal greetings. Remembered preferences. Offers that feel curated, not generic.

The frequent flyer who uses the food service regularly? We recognize them. We reward them. We make them feel that Vueling knows who they are and what they love.

This isn't just a product. It's a data flywheel that gets better with every flight."

---

## THE DEMO (45 seconds)

"Let me show you.

_[Live API call + UI]_

Angel Garcia. VY71299. Barcelona to Rome. Spanish.

In seconds: her crew, the aircraft, five highlights in Rome, three restaurants, transport from Fiumicino, weather, news. All in Spanish. All generated by AI. All running right now.

This is the POC. Two repos — backend API and frontend UI. Both working.

Now imagine: add the pre-order button. Add the music tab. Add the FAQ search. That's Phase 1. And the architecture is ready."

---

## THE CLOSE (30 seconds)

"Today, passengers only get this kind of experience on long-haul flights — premium entertainment, personal food ordering, destination content, all in one screen. No short-haul carrier in the world delivers this.

Vueling can be the first to bring the long-haul experience to every flight in Europe.

Content. Entertainment. Commerce. Personalization. All from one booking number. The POC is proven. The UI is live. The business case is clear.

Every flight is a canvas. Every passenger is an audience of one.

Let's build the future of flying. And let's win."

---

## Q&A PREP

**Q: Total investment?**
A: POC built in weeks. Phase 1 needs 3-4 engineers for one quarter. Phase 2 adds catering + payment integration. Full rollout under 12 months.

**Q: Food revenue potential?**
A: 8% of 34M passengers x 10 EUR avg. = ~27M EUR incremental pre-order revenue/year. Plus onboard digital ordering. Plus reduced waste savings.

**Q: Passengers without the app?**
A: WiFi portal serves the same experience via browser from the onboard edge cache. All content pillars work. Music would be app-only.

**Q: How do payments work at altitude?**
A: Small JSON payloads over satellite (~1KB). Same infrastructure airlines already use for inflight card transactions.

**Q: What about GDPR?**
A: Only the booking number (PNR) is used. No personal data goes to external APIs. AI receives "Rome, Italy" — never passenger names. Fully GDPR compliant by design.

**Q: Can competitors copy this?**
A: They can try. First-mover advantage is significant. Brand association compounds. And the data moat — passenger preferences, order history — grows with every flight.

**Q: Timeline to revenue?**
A: Content Phase 1: Q2 2026. Food ordering Phase 2: Q3 2026. Revenue impact measurable Q4 2026.
