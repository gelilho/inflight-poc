#!/usr/bin/env python3
"""
Generate Visual Deck PDF — Clean White Vueling Template.

Design language (from user template):
- White background, massive whitespace
- Top-left: yellow dot + "Vueling" bold black
- Top-right: decorative dot grid (yellow + gray)
- Bottom-right: larger gray dot triangle
- Thin gray line under header
- Short yellow bars above section titles
- Big bold black text, light gray descriptions
- Footer: light gray left-aligned
"""

from fpdf import FPDF
import os
import math

# --- COLORS ---
BLACK = (30, 30, 30)
DARK_TEXT = (40, 40, 40)
BODY_TEXT = (80, 80, 80)
LIGHT_TEXT = (150, 150, 150)
FAINT = (210, 210, 210)
YELLOW = (255, 240, 0)
WHITE = (255, 255, 255)
BG = (250, 250, 250)  # very slight off-white for cards if needed

W = 297  # A4 landscape
H = 210
MARGIN = 22
CONTENT_W = W - 2 * MARGIN


class VuelingDeck(FPDF):
    def __init__(self):
        super().__init__(orientation='L', unit='mm', format='A4')
        self.set_auto_page_break(auto=False)
        font_dir = '/System/Library/Fonts/Supplemental/'
        self.add_font('Arial', '', font_dir + 'Arial.ttf', uni=True)
        self.add_font('Arial', 'B', font_dir + 'Arial Bold.ttf', uni=True)
        self.add_font('Arial', 'I', font_dir + 'Arial Italic.ttf', uni=True)
        self.add_font('Arial', 'BI', font_dir + 'Arial Bold Italic.ttf', uni=True)

    # ── TEMPLATE ELEMENTS ──

    def chrome(self):
        """Draw the shared slide chrome: white bg, header, dots, footer."""
        # White background
        self.set_fill_color(*WHITE)
        self.rect(0, 0, W, H, 'F')

        # Top-left: yellow dot + "Vueling"
        self.set_fill_color(*YELLOW)
        self.ellipse(MARGIN, 10, 4, 4, 'F')
        self.set_text_color(*BLACK)
        self.set_font('Arial', 'B', 11)
        self.set_xy(MARGIN + 6, 10)
        self.cell(30, 4.5, 'Vueling')

        # Thin gray line under header
        self.set_draw_color(*FAINT)
        self.set_line_width(0.3)
        self.line(MARGIN, 18, W - MARGIN, 18)

        # Top-right dot grid (small decorative dots)
        self._dot_grid_top()

        # Bottom-right dot triangle
        self._dot_triangle()

        # Footer
        self.set_text_color(*LIGHT_TEXT)
        self.set_font('Arial', '', 7)
        self.set_xy(MARGIN, H - 10)
        self.cell(CONTENT_W, 4, 'Vueling Inflight Experience  |  MWC Barcelona 2026')

    def _dot_grid_top(self):
        """Small dot grid top-right corner."""
        start_x = W - MARGIN - 28
        start_y = 8
        dot_r = 0.8
        gap = 4.5
        for row in range(2):
            cols = 7 if row == 0 else 4
            for col in range(cols):
                x = start_x + col * gap
                y = start_y + row * gap
                # First dot yellow, rest gray
                if row == 0 and col == 0:
                    self.set_fill_color(*YELLOW)
                else:
                    self.set_fill_color(*FAINT)
                self.ellipse(x, y, dot_r * 2, dot_r * 2, 'F')

    def _dot_triangle(self):
        """Decorative dot triangle bottom-right."""
        base_x = W - MARGIN - 40
        base_y = H - 48
        dot_r = 1.8
        gap = 7
        rows = 7
        for row in range(rows):
            dots_in_row = row + 1
            for col in range(dots_in_row):
                x = base_x + col * gap + (rows - row - 1) * gap * 0.5
                y = base_y + row * gap
                alpha = max(0.15, 1.0 - row * 0.12)
                gray = int(210 + (1 - alpha) * 40)
                gray = min(gray, 245)
                self.set_fill_color(gray, gray, gray)
                self.ellipse(x, y, dot_r * 2, dot_r * 2, 'F')

    def yellow_bar(self, x, y, w=28):
        """Short yellow accent bar (above titles)."""
        self.set_fill_color(*YELLOW)
        self.rect(x, y, w, 2.5, 'F')

    def big_text(self, text, y, size=32, color=BLACK, align='C'):
        """Big statement text, centered."""
        self.set_text_color(*color)
        self.set_font('Arial', 'B', size)
        self.set_xy(MARGIN, y)
        self.multi_cell(CONTENT_W, size * 0.42, text, align=align)

    def body_text(self, text, y, size=11, color=BODY_TEXT, align='C', x=None, w=None):
        """Body description text."""
        self.set_text_color(*color)
        self.set_font('Arial', '', size)
        self.set_xy(x or MARGIN, y)
        self.multi_cell(w or CONTENT_W, size * 0.48, text, align=align)

    def section_title(self, text, x, y, size=16):
        """Section title with yellow bar above."""
        self.yellow_bar(x, y - 5)
        self.set_text_color(*BLACK)
        self.set_font('Arial', 'B', size)
        self.set_xy(x, y)
        self.cell(0, size * 0.4, text)

    def section_desc(self, text, x, y, w=70, size=9.5):
        """Section description text."""
        self.set_text_color(*BODY_TEXT)
        self.set_font('Arial', '', size)
        self.set_xy(x, y)
        self.multi_cell(w, size * 0.48, text)

    def stat_block(self, x, y, number, label, num_size=36):
        """Big number + label below."""
        self.set_text_color(*BLACK)
        self.set_font('Arial', 'B', num_size)
        self.set_xy(x, y)
        self.cell(0, num_size * 0.4, number)
        self.set_text_color(*BODY_TEXT)
        self.set_font('Arial', '', 9)
        self.set_xy(x, y + num_size * 0.42)
        self.cell(0, 5, label)

    # ── SLIDES ──

    def slide_01_cover(self):
        """35 million passengers choose Vueling."""
        self.add_page()
        self.chrome()
        self.big_text('Today, over 35 million\npassengers choose\nVueling every year.', 55, size=34)
        self.yellow_bar((W - 28) / 2, 115)

    def slide_02_opportunity(self):
        """60 million hours, zero engagement."""
        self.add_page()
        self.chrome()
        self.big_text('60 million flight hours.\nZero digital engagement.', 50, size=30)
        self.yellow_bar((W - 28) / 2, 100)
        self.body_text('Passengers bring their own entertainment. They skip food because ordering\n'
                       'is inconvenient. They land and google everything on someone else\'s platform.\n\n'
                       'We have the attention. We just aren\'t using it.', 112, size=11)

    def slide_03_solution(self):
        """Three pillars: AI-Powered, Real-Time, Seamless."""
        self.add_page()
        self.chrome()

        col_w = CONTENT_W / 3
        y_bar = 68
        y_title = 75
        y_desc = 86

        pillars = [
            ('AI-Powered', 'Personalized travel\nrecommendations'),
            ('Real-Time', 'Instant notifications\nand updates'),
            ('Seamless', 'From booking\nto landing'),
        ]

        for i, (title, desc) in enumerate(pillars):
            cx = MARGIN + i * col_w + col_w / 2
            self.yellow_bar(cx - 14, y_bar)
            self.set_text_color(*BLACK)
            self.set_font('Arial', 'B', 18)
            self.set_xy(MARGIN + i * col_w, y_title)
            self.cell(col_w, 8, title, align='C')
            self.set_text_color(*BODY_TEXT)
            self.set_font('Arial', '', 10)
            self.set_xy(MARGIN + i * col_w, y_desc)
            self.multi_cell(col_w, 5, desc, align='C')

    def slide_04_eleven_pillars(self):
        """The 11 experience pillars."""
        self.add_page()
        self.chrome()

        self.big_text('11 Experience Pillars', 28, size=26, align='L')
        self.body_text('One app. One booking number. A complete journey.', 42, size=11, align='L')

        # Three columns
        col_w = (CONTENT_W - 16) / 3
        y_start = 55

        cols = [
            ('Commerce & Entertainment', [
                ('Food & Snacks', 'Pre-order, order onboard, delivered to seat'),
                ('Music & Audio', 'AI-curated playlists per destination'),
            ]),
            ('Content', [
                ('Discover Destination', 'Top highlights + restaurants, AI-generated'),
                ('Weather & News', '3-day forecast + curated local news'),
                ('Digital Magazine', 'The new Ling, reborn digital'),
            ]),
            ('Utility & Personalization', [
                ('Live Flight Tracker', 'Real-time map, altitude, ETA'),
                ('Getting to the City', 'Transport options + bookable transfers'),
                ('Peace of Mind', 'Emergency contacts + helpline'),
                ('FAQ & Help', 'Searchable answers without calling'),
                ('Your Aircraft & Crew', '"Air Force Juan" + captain names'),
            ]),
        ]

        for c, (cat_title, items) in enumerate(cols):
            x = MARGIN + c * (col_w + 8)
            self.yellow_bar(x, y_start - 4, w=20)
            self.set_text_color(*BLACK)
            self.set_font('Arial', 'B', 9)
            self.set_xy(x, y_start)
            self.cell(col_w, 4, cat_title.upper())

            y = y_start + 8
            for name, desc in items:
                self.set_text_color(*BLACK)
                self.set_font('Arial', 'B', 9)
                self.set_xy(x, y)
                self.cell(col_w, 4, name)
                self.set_text_color(*LIGHT_TEXT)
                self.set_font('Arial', '', 7.5)
                self.set_xy(x, y + 5)
                self.cell(col_w, 3.5, desc)
                # Light separator
                y += 13
                if y < 150:
                    self.set_draw_color(235, 235, 235)
                    self.set_line_width(0.2)
                    self.line(x, y - 2, x + col_w - 5, y - 2)

    def slide_05_food_engine(self):
        """Three moments to capture a sale."""
        self.add_page()
        self.chrome()

        self.big_text('Three Moments\nto Capture a Sale', 28, size=26, align='L')
        self.body_text('The pillar that pays for the entire platform.', 50, size=11, align='L')

        col_w = (CONTENT_W - 16) / 3
        y_top = 65

        moments = [
            ('Day Before', 'T-24h', '"Pre-order your\nonboard menu"', 'Guaranteed revenue\nbefore departure'),
            ('At the Airport', 'T-3h', '"Add a snack bag\nfor the flight?"', 'Upsell revenue\nat the gate'),
            ('Onboard', 'T+15min', 'Browse, tap,\norder, pay', 'Live order,\ncrew delivers to seat'),
        ]

        for i, (title, time, action, outcome) in enumerate(moments):
            x = MARGIN + i * (col_w + 8)
            self.yellow_bar(x, y_top - 4, w=20)
            self.set_text_color(*BLACK)
            self.set_font('Arial', 'B', 14)
            self.set_xy(x, y_top)
            self.cell(col_w, 6, title)
            self.set_text_color(*LIGHT_TEXT)
            self.set_font('Arial', '', 8)
            self.set_xy(x, y_top + 8)
            self.cell(col_w, 4, time)
            self.set_text_color(*BODY_TEXT)
            self.set_font('Arial', '', 9.5)
            self.set_xy(x, y_top + 16)
            self.multi_cell(col_w, 4.5, action)
            self.set_text_color(*LIGHT_TEXT)
            self.set_font('Arial', '', 8.5)
            self.set_xy(x, y_top + 35)
            self.multi_cell(col_w, 4, outcome)

        # Bottom stats
        y_stats = 120
        self.set_draw_color(235, 235, 235)
        self.set_line_width(0.3)
        self.line(MARGIN, y_stats - 4, W - MARGIN, y_stats - 4)

        stats = [
            ('+30%', 'avg. order value'),
            ('-20%', 'food waste'),
            ('-15%', 'crew aisle time'),
            ('~27M EUR', 'year 1 revenue'),
        ]
        stat_w = CONTENT_W / 4
        for i, (num, label) in enumerate(stats):
            x = MARGIN + i * stat_w
            self.yellow_bar(x, y_stats - 1, w=16)
            self.set_text_color(*BLACK)
            self.set_font('Arial', 'B', 18)
            self.set_xy(x, y_stats + 4)
            self.cell(stat_w, 7, num)
            self.set_text_color(*LIGHT_TEXT)
            self.set_font('Arial', '', 8)
            self.set_xy(x, y_stats + 13)
            self.cell(stat_w, 4, label)

    def slide_06_journey(self):
        """Passenger journey timeline."""
        self.add_page()
        self.chrome()

        self.big_text('The Experience Starts\n24 Hours Before Boarding', 28, size=24, align='L')

        steps = [
            ('T-24h', 'Before the flight', 'Silent push: content pre-cached on device. Push: "Pre-order your menu"'),
            ('T-3h', 'At the airport', 'After check-in and security: "Explore Rome while you wait"'),
            ('T-0', 'Boarding', 'App or WiFi portal loads full experience instantly from cache'),
            ('T+15min', 'Cruising', 'Browse content offline. Food ordering live: menu, cart, pay, delivered'),
            ('T-30min', 'Approaching', '"30 min to Rome!" Weather, transport info, emergency contacts'),
            ('Landing', 'Post-flight', '"Rate your experience?" NPS survey. Guide stays accessible'),
        ]

        y = 58
        for i, (time, title, desc) in enumerate(steps):
            # Yellow dot
            self.set_fill_color(*YELLOW)
            self.ellipse(MARGIN + 2, y + 1, 3, 3, 'F')

            # Connector line
            if i < len(steps) - 1:
                self.set_draw_color(*FAINT)
                self.set_line_width(0.4)
                self.line(MARGIN + 3.5, y + 5, MARGIN + 3.5, y + 19)

            # Time
            self.set_text_color(*BLACK)
            self.set_font('Arial', 'B', 9)
            self.set_xy(MARGIN + 10, y)
            self.cell(20, 4, time)

            # Title
            self.set_font('Arial', 'B', 9)
            self.set_xy(MARGIN + 35, y)
            self.cell(40, 4, title)

            # Description
            self.set_text_color(*BODY_TEXT)
            self.set_font('Arial', '', 8.5)
            self.set_xy(MARGIN + 80, y)
            self.cell(CONTENT_W - 80, 4, desc)

            y += 19

    def slide_07_architecture(self):
        """Technical architecture - clean layered."""
        self.add_page()
        self.chrome()

        self.big_text('Architecture', 28, size=26, align='L')
        self.body_text('Offline-first. Pre-computed. Minimal satellite.', 42, size=11, align='L')

        box_w = CONTENT_W - 40
        x = MARGIN + 20
        y = 58

        layers = [
            ('Content Generation', 'Scheduled cadences: Destinations (2wk) | Flights (daily) | News (6h) | Weather (12h) | Music (wk)'),
            ('Google Gemini 2.5 Flash', 'Single AI engine: highlights, restaurants, weather, news, transport, translations (6 languages)'),
        ]

        for title, desc in layers:
            self.set_draw_color(*FAINT)
            self.set_line_width(0.4)
            self.rect(x, y, box_w, 14, 'D')
            self.set_text_color(*BLACK)
            self.set_font('Arial', 'B', 9)
            self.set_xy(x + 4, y + 1.5)
            self.cell(box_w - 8, 5, title, align='C')
            self.set_text_color(*LIGHT_TEXT)
            self.set_font('Arial', '', 7)
            self.set_xy(x + 4, y + 7.5)
            self.cell(box_w - 8, 4, desc, align='C')

            # Arrow down
            self.set_text_color(*FAINT)
            self.set_font('Arial', '', 12)
            self.set_xy(x, y + 14)
            self.cell(box_w, 5, '|', align='C')
            y += 21

        # Two delivery channels side by side
        half_w = box_w / 2 - 4
        channels = [
            ('Silent Push (App)', 'T-24h | ~15-25 MB on device'),
            ('Onboard Edge Cache (WiFi)', 'Loaded at gate via ground WiFi'),
        ]
        for i, (title, desc) in enumerate(channels):
            cx = x + i * (half_w + 8)
            self.set_draw_color(*FAINT)
            self.rect(cx, y, half_w, 12, 'D')
            self.set_text_color(*BLACK)
            self.set_font('Arial', 'B', 8.5)
            self.set_xy(cx, y + 1)
            self.cell(half_w, 4.5, title, align='C')
            self.set_text_color(*LIGHT_TEXT)
            self.set_font('Arial', '', 7)
            self.set_xy(cx, y + 6)
            self.cell(half_w, 4, desc, align='C')

        # Arrow
        self.set_text_color(*FAINT)
        self.set_font('Arial', '', 12)
        self.set_xy(x, y + 12)
        self.cell(box_w, 5, '|', align='C')
        y += 19

        # Passenger device
        self.set_draw_color(*FAINT)
        self.rect(x, y, box_w, 12, 'D')
        self.set_text_color(*BLACK)
        self.set_font('Arial', 'B', 9)
        self.set_xy(x + 4, y + 1.5)
        self.cell(box_w - 8, 5, 'Passenger Device', align='C')
        self.set_text_color(*LIGHT_TEXT)
        self.set_font('Arial', '', 7)
        self.set_xy(x + 4, y + 7)
        self.cell(box_w - 8, 4, 'Content loads instantly. Zero satellite bandwidth.', align='C')

        # Arrow
        self.set_text_color(*FAINT)
        self.set_font('Arial', '', 12)
        self.set_xy(x, y + 12)
        self.cell(box_w, 5, '|', align='C')
        y += 19

        # Satellite - minimal
        self.set_fill_color(248, 248, 248)
        self.set_draw_color(*FAINT)
        self.rect(x, y, box_w, 12, 'FD')
        self.set_text_color(*BLACK)
        self.set_font('Arial', 'B', 9)
        self.set_xy(x + 4, y + 1.5)
        self.cell((box_w - 8) / 2, 5, 'Satellite (real-time only)')
        self.set_text_color(*YELLOW)
        self.set_font('Arial', 'B', 10)
        r_half = (box_w - 8) / 2
        self.set_xy(x + 4 + r_half, y + 1.5)
        self.cell(r_half, 5, '~370 KB per flight', align='R')
        self.set_text_color(*LIGHT_TEXT)
        self.set_font('Arial', '', 7)
        self.set_xy(x + 4, y + 7)
        self.cell(box_w - 8, 4, 'Flight tracker | Food orders | Payments. Less than a single webpage.', align='C')

    def slide_08_kpis(self):
        """Key metrics."""
        self.add_page()
        self.chrome()

        self.big_text('The Numbers\nThat Matter', 28, size=26, align='L')

        # Two columns of metrics
        y = 56
        left_x = MARGIN
        right_x = MARGIN + CONTENT_W / 2 + 5

        categories = [
            (left_x, 'Engagement', [
                ('>25%', 'activation rate'),
                ('>12 min', 'session duration'),
            ]),
            (left_x, 'Revenue', [
                ('>8%', 'food pre-order conversion'),
                ('+30%', 'AOV uplift vs. aisle'),
            ]),
            (right_x, 'Satisfaction', [
                ('+5 pts', 'NPS lift'),
            ]),
            (right_x, 'Operations & Sustainability', [
                ('-15%', 'crew aisle time'),
                ('-20%', 'food waste'),
                ('>85%', 'catering forecast accuracy'),
            ]),
        ]

        cy = [y, y]  # track y for left/right columns
        for (x, cat_name, metrics) in categories:
            col = 0 if x == left_x else 1
            self.yellow_bar(x, cy[col] - 3, w=18)
            self.set_text_color(*LIGHT_TEXT)
            self.set_font('Arial', 'B', 7.5)
            self.set_xy(x, cy[col])
            self.cell(0, 4, cat_name.upper())
            cy[col] += 7

            for num, label in metrics:
                self.set_text_color(*BLACK)
                self.set_font('Arial', 'B', 20)
                self.set_xy(x, cy[col])
                self.cell(0, 8, num)
                self.set_text_color(*BODY_TEXT)
                self.set_font('Arial', '', 8.5)
                self.set_xy(x, cy[col] + 9)
                self.cell(0, 4, label)
                cy[col] += 18
            cy[col] += 4

        # Bottom stat
        y_bottom = 140
        self.set_draw_color(235, 235, 235)
        self.set_line_width(0.3)
        self.line(MARGIN, y_bottom, W - MARGIN, y_bottom)

        self.set_text_color(*BLACK)
        self.set_font('Arial', 'B', 11)
        self.set_xy(MARGIN, y_bottom + 5)
        self.cell(CONTENT_W, 5, 'Cost per passenger: ~0.005 EUR        ROI: 160x \u2014 240x', align='C')

    def slide_09_personalization(self):
        """Hyperpersonalization."""
        self.add_page()
        self.chrome()

        self.big_text('Treat every passenger\nlike a VIP.', 35, size=28, align='C')
        self.yellow_bar((W - 28) / 2, 62)
        self.body_text('Through software, not hardware.', 70, size=12)

        # Examples as clean list
        examples = [
            ('Maria always orders Mediterranean', '"Your usual?" \u2014 one-tap reorder'),
            ('Carlos reads culture articles', 'Magazine opens culture-first'),
            ('Family flying to Mallorca', 'Kids\' menu + family content highlighted'),
            ('10th food order from a frequent flyer', '"This one\'s on us!"'),
            ('Monday BCN \u2192 MAD business traveler', 'Coffee + news-first layout'),
        ]

        y = 86
        for who, result in examples:
            self.set_text_color(*BLACK)
            self.set_font('Arial', 'B', 9)
            self.set_xy(MARGIN + 20, y)
            self.cell(100, 4.5, who)
            self.set_text_color(*BODY_TEXT)
            self.set_font('Arial', '', 9)
            self.set_xy(MARGIN + 125, y)
            self.cell(0, 4.5, result)
            y += 11
            if y < 150:
                self.set_draw_color(240, 240, 240)
                self.set_line_width(0.2)
                self.line(MARGIN + 20, y - 3, W - MARGIN - 20, y - 3)

    def slide_10_impact(self):
        """Business impact - big numbers."""
        self.add_page()
        self.chrome()

        self.big_text('Business Impact', 28, size=26, align='L')

        # Three big stat blocks
        col_w = CONTENT_W / 3
        y = 52

        stats = [
            ('~27M', 'EUR/year', 'Food pre-orders alone.\nEvery content card is a\nfuture commerce touchpoint.'),
            ('0.005', 'EUR/passenger', 'AI content cost.\nEliminates paper magazine.\nReduces food waste.'),
            ('160x', 'ROI', 'Against food revenue.\nLong-haul level experience\non short-haul flights.'),
        ]

        for i, (number, unit, desc) in enumerate(stats):
            x = MARGIN + i * col_w
            self.yellow_bar(x, y - 4, w=20)
            self.set_text_color(*BLACK)
            self.set_font('Arial', 'B', 32)
            self.set_xy(x, y)
            self.cell(col_w, 12, number)
            self.set_text_color(*LIGHT_TEXT)
            self.set_font('Arial', 'B', 9)
            self.set_xy(x, y + 14)
            self.cell(col_w, 4, unit)
            self.set_text_color(*BODY_TEXT)
            self.set_font('Arial', '', 8.5)
            self.set_xy(x, y + 22)
            self.multi_cell(col_w - 10, 4, desc)

        # Bottom line
        y_b = 115
        self.set_draw_color(235, 235, 235)
        self.set_line_width(0.3)
        self.line(MARGIN, y_b, W - MARGIN, y_b)

        impacts = [
            ('Brand', 'First LCC with AI-powered inflight experience at scale'),
            ('Data', 'Every interaction builds the richest passenger profile in LCC aviation'),
            ('Operations', '-15% crew time, -20% food waste, predictive catering'),
        ]

        ix = MARGIN
        iw = CONTENT_W / 3
        for title, desc in impacts:
            self.yellow_bar(ix, y_b + 4, w=14)
            self.set_text_color(*BLACK)
            self.set_font('Arial', 'B', 10)
            self.set_xy(ix, y_b + 9)
            self.cell(iw, 4, title)
            self.set_text_color(*BODY_TEXT)
            self.set_font('Arial', '', 8)
            self.set_xy(ix, y_b + 15)
            self.multi_cell(iw - 5, 3.5, desc)
            ix += iw

    def slide_11_roadmap(self):
        """Roadmap."""
        self.add_page()
        self.chrome()

        self.big_text('From POC to Platform', 28, size=26, align='L')

        phases = [
            ('POC', True, 'Feb 2026', 'Destination content\nFlight details\n3 cities, 6 languages\nWorking UI + API'),
            ('Phase 1', False, 'TBD 2026', 'Food pre-order\nFlight tracker\nDigital magazine\nFAQ, Offline caching'),
            ('Phase 2', False, 'TBD 2026', 'Music & Audio\nOnboard ordering\n+ Payments\nFull route network'),
            ('Phase 3', False, 'End 2026', 'Hyperpersonalization\nPreferences, Loyalty\nVIP for all'),
            ('Phase 4', False, '2027', 'Commerce\nBookable restaurants\nTransfers & tickets\nPredictive intelligence'),
        ]

        col_w = (CONTENT_W - 4 * 6) / 5
        y = 50

        for i, (name, done, date, items) in enumerate(phases):
            x = MARGIN + i * (col_w + 6)

            # Yellow bar for done, gray for others
            if done:
                self.yellow_bar(x, y - 3, w=col_w)
            else:
                self.set_fill_color(240, 240, 240)
                self.rect(x, y - 3, col_w, 2, 'F')

            # Phase name
            self.set_text_color(*BLACK)
            self.set_font('Arial', 'B', 10)
            self.set_xy(x, y + 2)
            label = name + (' [DONE]' if done else '')
            self.cell(col_w, 4, label)

            # Date
            self.set_text_color(*LIGHT_TEXT)
            self.set_font('Arial', '', 7.5)
            self.set_xy(x, y + 8)
            self.cell(col_w, 3.5, date)

            # Items
            self.set_text_color(*BODY_TEXT)
            self.set_font('Arial', '', 8)
            self.set_xy(x, y + 16)
            self.multi_cell(col_w, 3.8, items)

    def slide_12_stakeholders(self):
        """What every team gets."""
        self.add_page()
        self.chrome()

        self.big_text('What Every Team Gets', 28, size=26, align='L')

        stakeholders = [
            ('Product', '11 pillars of passenger value from a single booking number'),
            ('Engineering', 'Offline-first architecture that works at 35,000 feet with 370 KB of satellite'),
            ('Design', 'One unified experience that feels personal, from boarding to landing'),
            ('Data', 'Every interaction is a signal. The richest passenger profile in LCC aviation'),
            ('Operations', '-15% crew time, -20% food waste, predictive catering from real demand'),
            ('Leadership', 'First-mover advantage. ~27M EUR revenue. A data flywheel.'),
        ]

        col_w = (CONTENT_W - 8) / 2
        y_start = 50

        for i, (name, desc) in enumerate(stakeholders):
            col = i % 2
            row = i // 2
            x = MARGIN + col * (col_w + 8)
            y = y_start + row * 24

            self.yellow_bar(x, y - 3, w=14)
            self.set_text_color(*BLACK)
            self.set_font('Arial', 'B', 11)
            self.set_xy(x, y)
            self.cell(col_w, 5, name)
            self.set_text_color(*BODY_TEXT)
            self.set_font('Arial', '', 9)
            self.set_xy(x, y + 7)
            self.multi_cell(col_w, 4, desc)

    def slide_13_demo(self):
        """Live demo slide."""
        self.add_page()
        self.chrome()

        self.big_text('Live Demo', 50, size=34)
        self.yellow_bar((W - 28) / 2, 68)

        # Demo details
        details = [
            ('Passenger', 'Angel Garcia'),
            ('Seat', '14D'),
            ('Flight', 'VY71299'),
            ('Route', 'Barcelona \u2192 Rome'),
            ('Language', 'Spanish'),
        ]

        y = 80
        for label, value in details:
            self.set_text_color(*LIGHT_TEXT)
            self.set_font('Arial', '', 10)
            self.set_xy(W / 2 - 40, y)
            self.cell(35, 5, label, align='R')
            self.set_text_color(*BLACK)
            self.set_font('Arial', 'B', 10)
            self.set_xy(W / 2 + 2, y)
            self.cell(50, 5, value)
            y += 9

        self.body_text('"This is the POC. Live. Working. Now imagine:\nadd a pre-order button, a music tab, a FAQ search. That\'s Phase 1."',
                       135, size=10, color=LIGHT_TEXT)

    def slide_14_closing(self):
        """Closing slide."""
        self.add_page()
        self.chrome()

        self.big_text('Every flight is a canvas.\nEvery passenger is\nan audience of one.', 42, size=28)

        self.yellow_bar((W - 28) / 2, 88)

        self.body_text('The POC is proven. The architecture is designed.\nThe business case is clear.', 98, size=12, color=BODY_TEXT)

        self.set_text_color(*BLACK)
        self.set_font('Arial', 'B', 14)
        self.set_xy(MARGIN, 118)
        self.cell(CONTENT_W, 6, 'Let\'s build the future of flying.', align='C')

        self.set_text_color(*LIGHT_TEXT)
        self.set_font('Arial', '', 9)
        self.set_xy(MARGIN, 145)
        self.cell(CONTENT_W, 4, 'Vueling Inflight Experience  |  MWC Barcelona 2026', align='C')


def main():
    pdf = VuelingDeck()

    pdf.slide_01_cover()
    pdf.slide_02_opportunity()
    pdf.slide_03_solution()
    pdf.slide_04_eleven_pillars()
    pdf.slide_05_food_engine()
    pdf.slide_06_journey()
    pdf.slide_07_architecture()
    pdf.slide_08_kpis()
    pdf.slide_09_personalization()
    pdf.slide_10_impact()
    pdf.slide_11_roadmap()
    pdf.slide_12_stakeholders()
    pdf.slide_13_demo()
    pdf.slide_14_closing()

    out_path = os.path.join(os.path.dirname(__file__), 'Visual Deck - Inflight Vueling Experience.pdf')
    pdf.output(out_path)
    print(f'PDF generated: {out_path}')
    print(f'Slides: {pdf.pages_count}')


if __name__ == '__main__':
    main()
