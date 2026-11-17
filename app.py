import base64
import textwrap
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="The Black Friday Edition",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_PATH = Path(__file__).parent / "Black_Friday_Trends_in_Romania.csv"
df = pd.read_csv(DATA_PATH)
df["year"] = pd.to_numeric(df["year"], errors="coerce")
df["value"] = pd.to_numeric(df["value"], errors="coerce")

# ── Colour palette (used for the UI *and* every chart) ──────────────────────
PLUM = "#30213F"
VIOLET = "#8064A2"
LILAC = "#B49ACB"
PALE = "#E9DDF1"
IVORY = "#F5F1E9"
GOLD = "#D5B779"
INK = "#292331"
MUTED = "#776F7D"
GRID = "#EFE9F2"

CAT = [PLUM, GOLD, VIOLET, LILAC]                       # fixed categorical order
YEAR_COLORS = {2023: LILAC, 2024: VIOLET, 2025: PLUM, 2026: GOLD}  # colour = year

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,500;1,600&display=swap');
html, body, [class*="css"] {{ font-family: 'DM Sans', sans-serif; }}
.stApp {{ background: {IVORY}; color: {INK}; }}
.block-container {{ padding-top: 2.4rem; max-width: 1280px; }}
[data-testid="stSidebar"] {{ background: #eee7f1; border-right: 1px solid #ddd1e4; }}
/* Sidebar menu: always black so it is readable in light and dark browser themes */
[data-testid="stSidebar"] [data-testid="stRadio"] *,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] *,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] * {{ color: #000000 !important; }}
[data-testid="stSidebar"] [data-testid="stRadio"] label p {{ font-weight: 500; font-size: .98rem; }}
h1,h2,h3 {{ font-family: 'Playfair Display', Georgia, serif !important; color: {PLUM}; }}
.eyebrow {{ color: {VIOLET}; letter-spacing: .16em; font-size: .72rem; font-weight: 700; text-transform: uppercase; }}
.masthead {{ font-family: 'Playfair Display', Georgia, serif; font-size: clamp(2.7rem, 6vw, 5.6rem); line-height: .98; color: {PLUM}; font-weight: 600; }}
.deck {{ color: {MUTED}; font-size: 1.08rem; max-width: 850px; line-height: 1.65; }}
.rule {{ border-top: 1px solid #d8cfc0; margin: 1.2rem 0; }}

/* KPI strip */
.kpi {{ background: {PALE}; border-top: 4px solid {GOLD}; padding: 1rem 1.2rem 1.05rem; border-radius: 4px 4px 14px 14px; min-height: 142px; }}
.kpi-label {{ color: {PLUM}; font-size: .72rem; font-weight: 700; letter-spacing: .09em; text-transform: uppercase; line-height: 1.35; min-height: 2.0em; }}
.kpi-value {{ font-family: 'Playfair Display', Georgia, serif; font-size: 2.5rem; line-height: 1.1; color: {PLUM}; margin-top: .3rem; font-weight: 600; }}
.kpi-sub {{ color: #51465c; font-size: .8rem; margin-top: .35rem; }}

/* Chart cards */
[class*="st-key-fig_"] {{ background: #FFFFFF; border: 1px solid #e6dceb; border-radius: 16px; padding: .6rem .8rem; box-shadow: 0 1px 0 rgba(48,33,63,.04); }}
.fig-no {{ color: {VIOLET}; letter-spacing: .16em; font-size: .7rem; font-weight: 700; text-transform: uppercase; }}
.fig-title {{ font-family: 'Playfair Display', Georgia, serif; color: {PLUM}; font-size: 1.35rem; line-height: 1.25; font-weight: 600; margin: .35rem 0 .7rem; }}
.fig-desc {{ color: {INK}; font-size: .97rem; line-height: 1.65; border-left: 3px solid {GOLD}; padding-left: .85rem; }}

/* Hide Deploy button and the 3-dots menu */
[data-testid="stAppDeployButton"], [data-testid="stToolbarActions"], [data-testid="stMainMenu"], .stDeployButton {{ display: none !important; }}

/* Sidebar collapse / expand buttons: always visible, not only on hover */
[data-testid="stSidebarCollapseButton"], [data-testid="stSidebarCollapseButton"] button,
[data-testid="stExpandSidebarButton"], [data-testid="stSidebarCollapsedControl"] {{ opacity: 1 !important; visibility: visible !important; }}
[data-testid="stSidebarCollapseButton"] button, [data-testid="stExpandSidebarButton"] {{
    background: #FFFFFF !important; border: 1px solid #cdbfd8 !important; border-radius: 10px !important; color: {PLUM} !important; }}
[data-testid="stSidebarCollapseButton"] *, [data-testid="stExpandSidebarButton"] * {{ color: {PLUM} !important; }}

/* Sidebar footer pinned to the bottom of the menu */
.sb-foot {{ position: fixed; bottom: 1.1rem; left: 1.5rem; width: 16.5rem; color: #000000; font-size: .78rem; line-height: 1.5; }}

/* Previous / next buttons at the bottom of each page (text centred, thumbnail on hover) */
[class*="st-key-pgnav_"] {{ display: flex; width: 100%; }}
[class*="st-key-pgnav_"][class*="_prev"] {{ justify-content: flex-start; }}
[class*="st-key-pgnav_"][class*="_next"] {{ justify-content: flex-end; }}
[class*="st-key-pgnav_"] .stButton {{ width: auto; }}
[class*="st-key-pgnav_"] button {{ position: relative; overflow: visible !important; width: 300px; max-width: 100%; justify-content: center; text-align: center;
    background: #FFFFFF; border: 1px solid #cdbfd8; border-radius: 999px; padding: .55rem 1rem; }}
[class*="st-key-pgnav_"] button > div, [class*="st-key-pgnav_"] button p {{ width: 100%; justify-content: center !important; text-align: center !important; }}
[class*="st-key-pgnav_"] button p {{ color: {PLUM}; font-weight: 600; font-size: .9rem; line-height: 1.3; }}
[class*="st-key-pgnav_"] button:hover {{ background: {PALE}; border-color: {VIOLET}; }}
[class*="st-key-pgnav_"][class*="_next"] button {{ background: {PLUM}; border-color: {PLUM}; }}
[class*="st-key-pgnav_"][class*="_next"] button p {{ color: {IVORY}; }}
[class*="st-key-pgnav_"][class*="_next"] button:hover {{ background: {VIOLET}; border-color: {VIOLET}; }}
[class*="st-key-pgnav_"] button::after {{ content: ""; position: absolute; bottom: calc(100% + 14px); width: 340px; height: 215px;
    background-color: #FFFFFF; background-size: cover; background-position: top center; background-repeat: no-repeat;
    border: 4px solid #FFFFFF; border-radius: 14px; box-shadow: 0 10px 30px rgba(48,33,63,.30), 0 0 0 1px #d9cce2;
    opacity: 0; transform: translateY(8px); transition: opacity .18s ease, transform .18s ease; pointer-events: none; z-index: 10000; }}
[class*="st-key-pgnav_"][class*="_prev"] button::after {{ left: 0; }}
[class*="st-key-pgnav_"][class*="_next"] button::after {{ right: 0; }}
[class*="st-key-pgnav_"] button:hover::after {{ opacity: 1; transform: translateY(0); }}

/* Breadcrumb */
[class*="st-key-crumb_"] button {{ background: transparent; border: none; padding: 0; min-height: 0; box-shadow: none; }}
[class*="st-key-crumb_"] button p {{ color: {VIOLET}; letter-spacing: .16em; font-size: .72rem; font-weight: 700; text-transform: uppercase; text-decoration: underline; text-underline-offset: 3px; }}
[class*="st-key-crumb_"] button:hover p {{ color: {PLUM}; }}
[class*="st-key-crumb_"] button p {{ margin: 0; line-height: 1.2; }}
.crumb-rest {{ line-height: 1.2; color: {VIOLET}; letter-spacing: .16em; font-size: .72rem; font-weight: 700; text-transform: uppercase; }}

/* Footer with profile links */
.author-footer {{ background: {PLUM}; border-radius: 18px; padding: 1.6rem 1.8rem; margin-top: 2.2rem; color: {IVORY}; }}
.author-footer .af-eyebrow {{ color: {GOLD}; letter-spacing: .16em; font-size: .72rem; font-weight: 700; text-transform: uppercase; }}
.author-footer .af-title {{ font-family: 'Playfair Display', Georgia, serif; font-size: 1.6rem; line-height: 1.25; margin: .4rem 0 .4rem; color: {IVORY}; font-weight: 600; }}
.author-footer .af-text {{ color: #d9cce2; font-size: .95rem; line-height: 1.6; max-width: 720px; }}
.author-footer .af-links {{ display: flex; flex-wrap: wrap; gap: .8rem; margin-top: 1.1rem; }}
.author-footer a {{ background: {GOLD}; color: {PLUM} !important; font-weight: 700; text-decoration: none !important; border-radius: 999px; padding: .65rem 1.3rem; font-size: .95rem; transition: transform .15s ease, background .15s ease; }}
.author-footer a:hover {{ background: #E6CD94; transform: translateY(-2px); }}
.author-footer a.alt {{ background: transparent; color: {IVORY} !important; border: 1.5px solid {GOLD}; }}
.author-footer a.alt:hover {{ background: rgba(213,183,121,.18); }}

/* Back-to-top button */
a.to-top {{ position: fixed; right: 1.6rem; bottom: 1.6rem; z-index: 9999; width: 46px; height: 46px; border-radius: 50%;
    background: {PLUM}; color: {IVORY} !important; font-size: 1.35rem; line-height: 46px; text-align: center; text-decoration: none !important;
    box-shadow: 0 4px 14px rgba(48,33,63,.35); border: 2px solid {GOLD}; }}
a.to-top:hover {{ background: {VIOLET}; }}

/* Clickable "Inside this issue" cards on the cover */
[class*="st-key-tease_"], [class*="st-key-tease_"] .stButton {{ width: 100%; }}
[class*="st-key-tease_"] button, [class*="st-key-tease_"] button * {{ white-space: normal !important; overflow: visible !important; text-overflow: clip !important; }}
[class*="st-key-tease_"] button {{ width: 100%; justify-content: flex-start; text-align: left; background: #FFFFFF; border: 1px solid #e6dceb;
    border-top: 3px solid {GOLD}; border-radius: 12px; padding: .9rem 1rem; min-height: 78px; }}
[class*="st-key-tease_"] button > div, [class*="st-key-tease_"] button p {{ width: 100%; justify-content: flex-start !important; text-align: left !important; }}
[class*="st-key-tease_"] button p {{ color: {PLUM}; font-family: 'Playfair Display', Georgia, serif; font-size: 1.05rem; font-weight: 600; line-height: 1.3; }}
[class*="st-key-tease_"] button:hover {{ background: {PALE}; border-color: {VIOLET}; }}

.pullquote {{ background: {PLUM}; color: {IVORY}; border-radius: 14px; padding: 1.4rem 1.5rem; font-family: 'Playfair Display', Georgia, serif; font-size: 1.45rem; font-style: italic; line-height: 1.35; }}
</style>
""", unsafe_allow_html=True)

# ── Page content ────────────────────────────────────────────────────────────
M_INTENT = "Share of respondents by BF purchase intention (November)"
M_BOUGHT = "Declared afterwards that they bought (actual purchase)"
M_WEEKS = "Average weeks before BF reference date when the shopping list is started"
M_LIST = "Share who make a list in advance"
M_BUDGET_SET = "Share with budget set in advance"
M_BUDGET = "Average planned BF budget"
M_CONSIDER = "What buyers considered when setting the BF budget"
M_TOP10 = "Products / services intended to buy at BF 2026 (top 10 of 26)"
M_ITEMS = "Average number of products / services planned"
M_NOBUY = "Main reason for not buying at Black Friday"
M_DISC = "Average discount that would convince the undecided to buy"
M_CONVINCE = "What would convince the undecided to buy at a discount"
M_DIFF = "What customers want to be different at BF this year"
M_CHANNEL = "Planned shopping channel for BF"
M_LEARN = "Where people learn about BF offers"
M_ONLINE = "Online channels planned for BF 2026"
M_SAT = "Satisfaction with overall BF shopping experience"
M_SATMEAN = "Mean satisfaction score"
M_DISSAT = "Reasons for dissatisfaction"
M_MULT = "Card transactions on BF day vs. an ordinary banking day (ordinary day = 1)"
M_INDEX = "Card transactions index, 14 days before BF = 100 (daily average)"
M_TICKET = "Average transaction value on BF day"
M_YOY = "YoY change BF day 2024 to 2025"
M_YOY_ONLINE = "Online card transactions on BF day, YoY"
M_PEAK = "Peak hour on BF day"
M_MIDNIGHT = "Share of BF-day transactions processed 00:00-00:59"
M_WINDOW = "Share of card payments in the 29-day window around BF 2025"

PAGES = {
    "Cover": {
        "chapter": "SPECIAL DATA EDITION",
        "title": "THE BLACK FRIDAY EDITION",
        "subtitle": "Are Romanians shopping smarter, or simply shopping more?",
        "intro": "A data-led investigation into the habits, expectations and decisions behind Romania's biggest shopping event.",
    },
    "01 · The Big Story": {
        "chapter": "01 / THE BIG STORY",
        "title": "The Black Friday Effect",
        "subtitle": "Is purchase intention changing — and does intention translate into action?",
        "figures": [
            dict(metric=M_INTENT, kind="line",
                 desc="Intention to buy has climbed from 57% in 2023 to 70% in 2026, after two flat years at 57% and a first step up to 62% in 2025. "
                      "Most of the gain comes from the undecided, who shrink from 34% to 24%, while non-buyers stay inside a narrow 6–10% band."),
            dict(metric=M_BOUGHT, kind="line_single",
                 desc="Afterwards, the share who say they actually bought rises every year: 71% in 2023, 77% in 2024 and 79% in 2025. "
                      "It is measured in the following year's wave on a different base from the intention question, so read it alongside intention rather than as an exact conversion."),
        ],
        "take": "Purchase intention and reported purchase are different measures. Read them as two parts of the story, not as a direct conversion funnel.",
    },
    "02 · Shopping Habits": {
        "chapter": "02 / THE SHOPPING HABITS",
        "title": "Planning is the new impulse",
        "subtitle": "The shopping spree starts before the event itself.",
        "figures": [
            dict(metric=M_WEEKS, kind="line_single", unit_title="weeks",
                 desc="Buyers start their shopping list about four weeks ahead. The lead time is longest in 2026 at 4.1 weeks, up from 3.7 in 2023 and 2025: the hunt begins a little earlier each season."),
            dict(metric=M_BUDGET, kind="line_single", unit_title="RON",
                 desc="Planned spending stays close to 2,100 RON. It dipped from 2,179 RON in 2024 to 2,046 RON in 2025 and recovered to 2,100 RON in 2026, so shoppers are planning more without planning to spend much more."),
            dict(metric=M_CONSIDER, kind="line",
                 desc="Available financial resources is still the top consideration when setting a budget, but it falls from 71% in 2023 to 50% in 2025 and 2026. "
                      "The economic context (19% to 25%) and the option to pay in instalments (19% to 25%) weigh more, while price stays in the 34–46% range."),
        ],
        "take": "Planning horizon, list-making and budgeting describe different behaviours. Keep weeks, percentages and RON in separate visualisations.",
    },
    "03 · The Wishlist": {
        "chapter": "03 / THE WISHLIST",
        "title": "What's in the cart?",
        "subtitle": "A closer look at the products and services shoppers plan to buy.",
        "figures": [
            dict(metric=M_TOP10, kind="hbar", height=470,
                 desc="Home appliances and electronics lead the 2026 wishlist at 51%, followed by IT&C products (37%) and fashion (30%). "
                      "Beyond the top three, interest spreads across everyday categories from cosmetics (27%) to books, stationery, music and films (12%). Respondents could pick several categories."),
        ],
        "take": "The category question allows multiple responses. Percentages are not expected to total 100%. The category ranking is for 2026 only.",
    },
    "04 · The Discount Dilemma": {
        "chapter": "04 / THE OPINION PIECE",
        "title": "The discount dilemma",
        "subtitle": "A good deal is only good if shoppers believe it — and find it worthwhile.",
        "figures": [
            dict(metric=M_NOBUY, kind="gbar", height=520,
                 desc="Among non-buyers, distrust of discounts has halved from 44% in 2023 to 21% in 2026. Money worries have taken its place: a tight budget rises from 13% to 24%, "
                      "and caution about the economic situation jumps from 12% to 28%, now the top reason. Three further reasons appear only in the 2026 data."),
            dict(metric=M_DISC, kind="line_single", unit_title="% of price",
                 desc="The undecided would need roughly half off to buy: 51% in 2024, 54% in 2025 and 49% in 2026, the lowest of the three years."),
            dict(metric=M_CONVINCE, kind="hbar", height=420,
                 desc="A large discount is the strongest persuader (61%), but it is not the only one. Offers on products of special interest (50%) and an easy way to verify the real discount (36%) "
                      "matter almost as much, while free delivery (23%) and flexible payment (13%) play a smaller role."),
            dict(metric=M_DIFF, kind="hbar", height=420,
                 desc="Shoppers' wish list for this year is led by substantial and/or authentic discounts, named by 77%, more than twice the next ask, sufficient stock (33%). Everything else, from range to platform functionality, trails far behind."),
        ],
        "take": "The barriers question is answered by non-buyers, while discount expectations concern undecided shoppers or the wider buyer base. Always show the question base and source note.",
    },
    "05 · The Digital Life": {
        "chapter": "05 / THE DIGITAL LIFE",
        "title": "Click, shop, repeat",
        "subtitle": "Where people plan to shop — and where they discover the offers.",
        "figures": [
            dict(metric=M_CHANNEL, kind="line", height=400,
                 desc="Online is back to 60% in 2026 after a dip to 47% in 2025, the year hybrid shopping peaked at 39%. Physical-only shopping keeps shrinking and sits at 8%, the lowest point in the series."),
            dict(metric=M_LEARN, kind="heatmap", height=420,
                 desc="Discovery is led by the retailers' own channels (74% in 2026), followed by social media (57%) and traditional advertising (45%). "
                      "The pattern is remarkably stable across the four years, and AI assistants make their first appearance in 2026 at 6%."),
            dict(metric=M_ONLINE, kind="hbar", height=300,
                 desc="Within online shopping, marketplaces such as eMAG, Amazon, SHEIN and Temu are the top planned channel at 70%, ahead of retailers' own websites (61%) and mobile apps (41%). Buying directly in social networks remains marginal at 12%."),
        ],
        "take": "The 2026 online-channel breakdown is a separate question from the overall shopping-channel split. Multiple-response answers may exceed 100%.",
    },
    "06 · Customer Experience": {
        "chapter": "06 / THE CUSTOMER EXPERIENCE",
        "title": "After the click",
        "subtitle": "The shopping experience does not end at checkout.",
        "figures": [
            dict(metric=M_SAT, kind="stack", height=420,
                 desc="Satisfaction edges up: 59% of buyers rate their experience 6–7 out of 7 in 2025, against 56% in 2023 and 2024. The dissatisfied group is unchanged at 10% in all three editions."),
            dict(metric=M_DISSAT, kind="gbar", height=470,
                 desc="Out-of-stock products are the leading complaint in 2023–2025 (43–50%), followed by technical problems and long delivery times. "
                      "The 2026 survey adds new options, and 'discount smaller than expected' tops the list at 60%. Bases are small, so treat these as indicative."),
        ],
        "take": "Satisfaction series currently ends in 2025. Some dissatisfaction options or questions may have changed over time; use the notes and bases before making trend claims.",
    },
    "07 · The Payment Pulse": {
        "chapter": "07 / THE PAYMENT PULSE",
        "title": "When Black Friday goes live",
        "subtitle": "A separate look at activity recorded by NETOPIA's payment infrastructure.",
        "figures": [
            dict(metric=M_MULT, kind="col", hl="2025", unit_title="×",
                 desc="On Black Friday itself, card transactions were 1.9 times an ordinary banking day in 2023, 1.5 times in 2024 and 1.4 times in 2025. The single-day spike is flattening year after year."),
            dict(metric=M_INDEX, kind="col", hl="BF day (7 Nov 2025)",
                 desc="Against a baseline of 100 for the daily average two weeks before, activity reaches 151.6 on BF day and is still at 133.5 across the following fortnight: the event leaves a lasting lift."),
            dict(metric=M_WINDOW, kind="col", hl="BF day",
                 desc="Across the 29-day window around BF 2025, only 4% of card payments fall on the day itself. 41% come in the 14 days before and 55% in the 14 days after, so the season is far wider than one date."),
            dict(metric=M_YOY, kind="hbar", height=300,
                 desc="Compared with 2024, BF day processed 19% more volume in euros and 14% more transactions, with 8% more active merchants. Value grew faster than transaction count, and transaction count faster than the merchant base."),
        ],
        "take": "NETOPIA metrics describe transactions processed through NETOPIA, not the entire Romanian market. Multipliers, index values, RON and percentage changes must remain separate.",
    },
    "08 · The Final Edit": {
        "chapter": "08 / THE FINAL EDIT",
        "title": "So, are Romanians shopping smarter?",
        "subtitle": "Three lenses on the changing Black Friday shopper.",
        "figures": [],
        "take": "The dataset suggests a shopper who plans ahead, weighs the value of discounts and increasingly uses digital channels. These are interpretations of separate survey measures, not proof of individual-level behaviour.",
    },
}

# ── Helpers ─────────────────────────────────────────────────────────────────
def val(metric, year=None, segment=None):
    d = df[df["metric"].eq(metric)]
    if year is not None:
        d = d[d["year"].eq(year)]
    if segment is not None:
        d = d[d["segment"].eq(segment)]
    return None if d.empty else float(d.iloc[0]["value"])

def delta(new, old, unit, since):
    d = round(new - old, 2)
    if d == 0:
        return f"Unchanged since {since}"
    arrow, sign = ("▲", "+") if d > 0 else ("▼", "−")
    return f"{arrow} {sign}{abs(d):g}{unit} vs {since}"

def pct(v):
    return f"{v:g}%"

def ron(v):
    return f'{v:,.0f}'.replace(",", " ") + '<span style="font-size:.5em"> RON</span>'

def kpi_row(items):
    cols = st.columns(len(items))
    for col, (label, value, sub) in zip(cols, items):
        with col:
            sub_html = f'<div class="kpi-sub">{sub}</div>' if sub else ""
            st.markdown(
                f'<div class="kpi"><div class="kpi-label">{label}</div>'
                f'<div class="kpi-value">{value}</div>{sub_html}</div>',
                unsafe_allow_html=True,
            )

def kpis_for(selected):
    if selected.startswith("01"):
        seg = lambda s, y: val(M_INTENT, y, s)
        return [
            ("Intend to buy · 2026", pct(seg("Buyers (intend to buy)", 2026)), delta(seg("Buyers (intend to buy)", 2026), seg("Buyers (intend to buy)", 2023), " pp", 2023)),
            ("Undecided · 2026", pct(seg("Undecided", 2026)), delta(seg("Undecided", 2026), seg("Undecided", 2023), " pp", 2023)),
            ("Non-buyers · 2026", pct(seg("Non-buyers", 2026)), delta(seg("Non-buyers", 2026), seg("Non-buyers", 2023), " pp", 2023)),
            ("Reported purchase · 2025", pct(val(M_BOUGHT, 2025)), delta(val(M_BOUGHT, 2025), val(M_BOUGHT, 2023), " pp", 2023)),
        ]
    if selected.startswith("02"):
        return [
            ("Make a list in advance · 2026", pct(val(M_LIST, 2026)), "Buyers (hot leads)"),
            ("Budget set in advance · 2026", pct(val(M_BUDGET_SET, 2026)), "Buyers (hot leads)"),
            ("Average planned budget · 2026", ron(val(M_BUDGET, 2026)), delta(val(M_BUDGET, 2026), val(M_BUDGET, 2025), " RON", 2025)),
            ("List started · weeks ahead", f'{val(M_WEEKS, 2026):g} weeks', delta(val(M_WEEKS, 2026), val(M_WEEKS, 2023), " wk", 2023)),
        ]
    if selected.startswith("03"):
        top = val(M_TOP10, 2026, "Home appliances & electronics")
        return [
            ("Products planned per buyer", f'{val(M_ITEMS, 2026):g} items', "All buyers · 2026"),
            ("Home appliances & electronics", pct(top), "Top category · 2026"),
            ("IT&C products", pct(val(M_TOP10, 2026, "IT&C products")), "Second category · 2026"),
            ("Fashion", pct(val(M_TOP10, 2026, "Fashion")), "Third category · 2026"),
        ]
    if selected.startswith("04"):
        return [
            ("Average discount to convince the undecided", pct(val(M_DISC, 2026)), delta(val(M_DISC, 2026), val(M_DISC, 2025), " pp", 2025)),
            ("Undecided naming a 25–50% discount", pct(val("Share of undecided naming a discount between 25% and 50%", 2026)), "2026"),
            ("Undecided naming exactly 50%", pct(val("Share of undecided naming exactly 50%", 2026)), "2026"),
            ("Non-buyers who distrust discounts", pct(val(M_NOBUY, 2026, "Distrust: do not believe discounts are real")),
             delta(val(M_NOBUY, 2026, "Distrust: do not believe discounts are real"), val(M_NOBUY, 2023, "Distrust: do not believe discounts are real"), " pp", 2023)),
        ]
    if selected.startswith("05"):
        on = lambda y: val(M_CHANNEL, y, "Online")
        hy = lambda y: val(M_CHANNEL, y, "Hybrid (online and physical)")
        rt = lambda y: val(M_LEARN, y, "Retailer (app, website, newsletters, push)")
        return [
            ("Plan to shop online · 2026", pct(on(2026)), delta(on(2026), on(2025), " pp", 2025)),
            ("Plan to shop hybrid · 2026", pct(hy(2026)), delta(hy(2026), hy(2025), " pp", 2025)),
            ("Marketplaces among online channels", pct(val(M_ONLINE, 2026, "Marketplaces (eMAG, Amazon, SHEIN, Temu etc.)")), "2026"),
            ("Learn about offers from retailers", pct(rt(2026)), delta(rt(2026), rt(2025), " pp", 2025)),
        ]
    if selected.startswith("06"):
        sat = lambda y: val(M_SAT, y, "Satisfied (6-7 on 7-point scale)")
        dis = lambda y: val(M_SAT, y, "Dissatisfied (1-3)")
        return [
            ("Satisfied · 2025", pct(sat(2025)), delta(sat(2025), sat(2023), " pp", 2023)),
            ("Mean satisfaction score", f'{val(M_SATMEAN, 2025):g} / 7', delta(val(M_SATMEAN, 2025), val(M_SATMEAN, 2023), "", 2023)),
            ("Dissatisfied · 2025", pct(dis(2025)), delta(dis(2025), dis(2023), " pp", 2023)),
            ("Say the discount was smaller than expected", pct(val(M_DISSAT, 2026, "Discount smaller than expected (new option in 2026 survey)")), "Top reason in the 2026 survey"),
        ]
    if selected.startswith("07"):
        return [
            ("BF day vs an ordinary day · 2025", f'{val(M_MULT, 2025):g}×', delta(val(M_MULT, 2025), val(M_MULT, 2024), "×", 2024)),
            ("Average transaction value", ron(val(M_TICKET, 2025)), "BF day 2025"),
            ("Online card transactions", f'+{val(M_YOY_ONLINE, 2025):g}%', "BF day, year on year"),
            ("Peak hour on BF day", f'{int(val(M_PEAK, 2025)):02d}:00', "2025"),
            ("Processed 00:00–00:59", pct(val(M_MIDNIGHT, 2025)), "of BF-day transactions"),
        ]
    if selected.startswith("08"):
        distrust = lambda y: val(M_NOBUY, y, "Distrust: do not believe discounts are real")
        return [
            ("Lens 1 · Plan ahead", pct(val(M_LIST, 2026)), "of buyers make a list in advance"),
            ("Lens 2 · Weigh the deal", pct(distrust(2026)), f"of non-buyers still distrust discounts ({distrust(2023):g}% in 2023)"),
            ("Lens 3 · Go digital", pct(val(M_CHANNEL, 2026, "Online")), "plan to shop online in 2026"),
        ]
    return []

# ── Charts ──────────────────────────────────────────────────────────────────
def wrap(s, n=30):
    return "<br>".join(textwrap.wrap(str(s), n)) or str(s)

def lerp_hex(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(a, b))

def fmt(v, unit):
    if pd.isna(v):
        return ""
    if unit in ("%", "% of price"):
        return f"{v:g}%"
    if unit == "% change":
        return f"+{v:g}%"
    if unit == "x":
        return f"{v:g}×"
    if unit == "RON":
        return f"{v:,.0f}".replace(",", " ")
    return f"{v:g}"

def axis_suffix(unit):
    return {"%": "%", "% of price": "%", "% change": "%", "x": "×"}.get(unit, "")

def style(fig, height, legend=False, unit=""):
    fig.update_layout(
        template="plotly_white", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans, sans-serif", color=INK, size=13),
        margin=dict(l=8, r=24, t=56 if legend else 12, b=12), height=height,
        showlegend=legend, bargap=0.32,
        legend=dict(orientation="h", yanchor="bottom", y=1.0, x=0, title_text="", font=dict(color=INK, size=12)),
        hoverlabel=dict(bgcolor="#FFFFFF", bordercolor=LILAC, font=dict(family="DM Sans", color=INK)),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor="#d8cfc0", tickfont=dict(color=MUTED))
    fig.update_yaxes(gridcolor=GRID, zeroline=False, tickfont=dict(color=MUTED))
    return fig

def years_axis(fig, years):
    fig.update_xaxes(tickmode="array", tickvals=years, ticktext=[str(int(y)) for y in years], type="linear",
                     range=[min(years) - 0.35, max(years) + 0.35])

def fig_hbar(data, unit, height):
    d = data.sort_values("value", ascending=True)
    lo, hi = d["value"].min(), d["value"].max()
    colors = [lerp_hex(LILAC, PLUM, (v - lo) / (hi - lo) if hi > lo else 1) for v in d["value"]]
    fig = go.Figure(go.Bar(
        x=d["value"], y=[wrap(s, 34) for s in d["segment"]], orientation="h",
        marker=dict(color=colors, cornerradius=5), text=[fmt(v, unit) for v in d["value"]],
        textposition="outside", textfont=dict(color=INK, size=13), cliponaxis=False,
        hovertemplate="%{y}<br><b>%{text}</b><extra></extra>",
    ))
    style(fig, height)
    fig.update_xaxes(visible=False, range=[0, hi * 1.18])
    fig.update_yaxes(showgrid=False, tickfont=dict(color=INK, size=12.5))
    return fig

def fig_gbar(data, unit, height):
    p = data.pivot_table(index="segment", columns="year", values="value")
    order = p.max(axis=1).sort_values(ascending=False).index.tolist()
    fig = go.Figure()
    for y in sorted(p.columns):
        vals = [None if pd.isna(p.loc[s, y]) else p.loc[s, y] for s in order]
        fig.add_trace(go.Bar(
            name=str(int(y)), x=vals, y=[wrap(s, 34) for s in order], orientation="h",
            marker=dict(color=YEAR_COLORS.get(int(y), VIOLET), cornerradius=4),
            text=[fmt(v, unit) if v is not None else "" for v in vals], textposition="outside",
            textfont=dict(color=INK, size=11.5), cliponaxis=False,
            hovertemplate="%{y}<br>" + str(int(y)) + ": <b>%{text}</b><extra></extra>",
        ))
    style(fig, height, legend=True)
    fig.update_layout(barmode="group", bargap=0.28, bargroupgap=0.08, legend=dict(traceorder="normal"))
    fig.update_xaxes(visible=False, range=[0, float(p.max().max()) * 1.2])
    fig.update_yaxes(showgrid=False, autorange="reversed", tickfont=dict(color=INK, size=12.5))
    return fig

def fig_line(data, unit, height):
    p = data.pivot_table(index="year", columns="segment", values="value")
    order = p.iloc[-1].sort_values(ascending=False).index.tolist()
    years = p.index.tolist()
    fig = go.Figure()
    for i, s in enumerate(order):
        ys = p[s].tolist()
        text = [fmt(v, unit) if j in (0, len(ys) - 1) else "" for j, v in enumerate(ys)]
        fig.add_trace(go.Scatter(
            name=s, x=years, y=ys, mode="lines+markers+text", text=text, textposition="top center",
            textfont=dict(color=INK, size=12),
            line=dict(color=CAT[i % len(CAT)], width=3.2),
            marker=dict(size=10, color=CAT[i % len(CAT)], line=dict(color="#FFFFFF", width=2)),
            hovertemplate=f"{s}<br>%{{x}}: <b>%{{y:g}}{axis_suffix(unit)}</b><extra></extra>",
        ))
    style(fig, height, legend=True)
    years_axis(fig, years)
    fig.update_yaxes(ticksuffix=axis_suffix(unit), rangemode="tozero")
    fig.update_yaxes(range=[0, float(p.max().max()) * 1.18])
    return fig

def fig_line_single(data, unit, height, unit_title=""):
    d = data.sort_values("year")
    years, ys = d["year"].tolist(), d["value"].tolist()
    pad = (max(ys) - min(ys)) * 0.6 or 1
    fig = go.Figure(go.Scatter(
        x=years, y=ys, mode="lines+markers+text", text=[fmt(v, unit) for v in ys],
        textposition=["bottom center" if 0 < i < len(ys) - 1 and ys[i] < min(ys[i - 1], ys[i + 1]) else "top center" for i in range(len(ys))],
        textfont=dict(color=INK, size=13), line=dict(color=PLUM, width=3.4),
        marker=dict(size=12, color=[GOLD if y == years[-1] else PLUM for y in years], line=dict(color="#FFFFFF", width=2.5)),
        hovertemplate="%{x}: <b>%{text}</b><extra></extra>",
    ))
    style(fig, height)
    years_axis(fig, years)
    fig.update_yaxes(range=[min(ys) - pad, max(ys) + pad], ticksuffix=axis_suffix(unit),
                     title=dict(text=unit_title if unit_title and not axis_suffix(unit) else "", font=dict(color=MUTED, size=12)))
    return fig

def fig_col(data, unit, height, hl=None, unit_title=""):
    d = data.sort_values("row_id")
    xs = [str(int(s)) if pd.api.types.is_number(s) and not pd.isna(s) else str(s) for s in
          (d["year"] if d["segment"].nunique() == 1 else d["segment"])]
    ys = d["value"].tolist()
    colors = [PLUM if x == hl else LILAC for x in xs]
    fig = go.Figure(go.Bar(
        x=[wrap(x, 16) for x in xs], y=ys, marker=dict(color=colors, cornerradius=6),
        text=[fmt(v, unit) for v in ys], textposition="outside", textfont=dict(color=INK, size=14), cliponaxis=False,
        hovertemplate="%{x}<br><b>%{text}</b><extra></extra>",
    ))
    style(fig, height)
    fig.update_layout(bargap=0.45)
    fig.update_yaxes(visible=False, range=[0, max(ys) * 1.2])
    fig.update_xaxes(tickfont=dict(color=INK, size=12.5))
    return fig

def fig_stack(data, unit, height):
    p = data.pivot_table(index="year", columns="segment", values="value")
    order = [c for c in ["Satisfied (6-7 on 7-point scale)", "Neutral (4-5)", "Dissatisfied (1-3)"] if c in p.columns]
    colors = {order[0]: PLUM, order[1]: LILAC, order[2]: GOLD} if len(order) == 3 else {}
    txt = {order[0]: "#FFFFFF", order[1]: INK, order[2]: INK} if len(order) == 3 else {}
    fig = go.Figure()
    years = [str(int(y)) for y in p.index]
    for s in order:
        fig.add_trace(go.Bar(
            name=s, x=years, y=p[s], marker=dict(color=colors.get(s, VIOLET), line=dict(color="#FFFFFF", width=2)),
            text=[fmt(v, unit) for v in p[s]], textposition="inside", insidetextanchor="middle",
            textfont=dict(color=txt.get(s, INK), size=14),
            hovertemplate=f"{s}<br>%{{x}}: <b>%{{text}}</b><extra></extra>",
        ))
    style(fig, height, legend=True)
    fig.update_layout(barmode="stack", bargap=0.35, legend=dict(traceorder="normal"))
    fig.update_yaxes(range=[0, 100], ticksuffix="%")
    return fig

def fig_heatmap(data, unit, height):
    p = data.pivot_table(index="segment", columns="year", values="value")
    p = p.loc[p.max(axis=1).sort_values(ascending=False).index]
    years = [int(y) for y in p.columns]
    segs = [wrap(s, 34) for s in p.index]
    z = p.values
    fig = go.Figure(go.Heatmap(
        z=z, x=years, y=segs, xgap=4, ygap=4, showscale=False, zmin=0, zmax=80,
        colorscale=[[0, PALE], [0.5, LILAC], [1, PLUM]],
        hovertemplate="%{y}<br>%{x}: <b>%{z:g}%</b><extra></extra>", hoverongaps=False,
    ))
    vmax = 80
    for i in range(z.shape[0]):
        for j in range(z.shape[1]):
            v = z[i, j]
            label = "–" if pd.isna(v) else f"{v:g}%"
            dark = (not pd.isna(v)) and v / vmax > 0.5
            fig.add_annotation(x=years[j], y=segs[i], text=label, showarrow=False,
                               font=dict(size=13, color="#FFFFFF" if dark else INK))
    style(fig, height)
    fig.update_xaxes(side="top", tickmode="array", tickvals=years, ticktext=[str(y) for y in years],
                     range=[min(years) - 0.5, max(years) + 0.5], tickfont=dict(color=INK, size=13))
    fig.update_yaxes(autorange="reversed", showgrid=False, tickfont=dict(color=INK, size=12.5))
    return fig

def go_to(page_name):
    st.session_state["nav"] = page_name
    st.session_state["scroll_top"] = True

PREVIEW_DIR = Path(__file__).parent / "previews"

@st.cache_data
def preview_uri(num):
    f = PREVIEW_DIR / f"{num}.jpg"
    if not f.exists():
        return None
    return "data:image/jpeg;base64," + base64.b64encode(f.read_bytes()).decode()

def page_nav(selected):
    """Previous / Next buttons (bottom of the page). Hovering shows a thumbnail of the target page."""
    names = list(PAGES.keys())
    i = names.index(selected)
    css = ""
    prev_col, next_col = st.columns(2, gap="medium")
    with prev_col:
        if i > 1:
            st.button(f"← {names[i - 1]}", key="pgnav_prev", on_click=go_to, args=(names[i - 1],))
            uri = preview_uri(names[i - 1][:2])
            if uri:
                css += f'.st-key-pgnav_prev button::after {{ background-image: url("{uri}"); }}'
    with next_col:
        if i < len(names) - 1:
            st.button(f"{names[i + 1]} →", key="pgnav_next", on_click=go_to, args=(names[i + 1],))
            uri = preview_uri(names[i + 1][:2])
            if uri:
                css += f'.st-key-pgnav_next button::after {{ background-image: url("{uri}"); }}'
    if css:
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def breadcrumb(page):
    """COVER › 01 / THE BIG STORY  — the cover part is a link back to the cover."""
    c1, c2, c3 = st.columns([0.8, 6.2, 3], vertical_alignment="center", gap="small")
    with c1:
        st.button("⌂ Cover", key="crumb_cover", on_click=go_to, args=(list(PAGES.keys())[0],))
    with c2:
        st.markdown(f'<div class="crumb-rest">›&nbsp; {page["chapter"]}</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="crumb-rest" style="text-align:right">THE BLACK FRIDAY EDITION</div>', unsafe_allow_html=True)

def author_footer():
    st.markdown(
        '<div class="author-footer">'
        '<div class="af-eyebrow">Behind the numbers</div>'
        '<div class="af-title">Liked the story? There is more where it came from.</div>'
        '<div class="af-text">I\'m Elena-Luchiana Dumitrescu, a data analyst and BI developer. '
        'Come see the dashboards and projects I build, and read my SQL and analytics articles.</div>'
        '<div class="af-links">'
        '<a href="https://www.linkedin.com/in/elena-luchiana-dumitrescu" target="_blank" rel="noopener noreferrer">See my projects on LinkedIn →</a>'
        '<a class="alt" href="https://medium.com/@luchianadumitrescu" target="_blank" rel="noopener noreferrer">Read my articles on Medium →</a>'
        '</div></div>',
        unsafe_allow_html=True,
    )

def build_fig(spec):
    data = df[df["metric"].eq(spec["metric"])].copy()
    units = data["unit"].dropna().unique()
    unit = units[0] if len(units) else ""
    kind, h = spec["kind"], spec.get("height", 360)
    if kind == "hbar":
        return fig_hbar(data, unit, h)
    if kind == "gbar":
        return fig_gbar(data, unit, h)
    if kind == "line":
        return fig_line(data, unit, h)
    if kind == "line_single":
        return fig_line_single(data, unit, h, spec.get("unit_title", ""))
    if kind == "col":
        return fig_col(data, unit, h, spec.get("hl"), spec.get("unit_title", ""))
    if kind == "stack":
        return fig_stack(data, unit, h)
    return fig_heatmap(data, unit, h)

def show_chart(fig):
    cfg = {"displayModeBar": False}
    try:
        st.plotly_chart(fig, width="stretch", config=cfg)
    except TypeError:  # older Streamlit versions
        st.plotly_chart(fig, use_container_width=True, config=cfg)

def render_figure(n, spec, page_no):
    with st.container(border=True, key=f"fig_{page_no}_{n}"):
        text_col, chart_col = st.columns([1, 2], gap="large", vertical_alignment="center")
        with text_col:
            st.markdown(
                f'<div class="fig-no">Figure {n}</div>'
                f'<div class="fig-title">{spec.get("title", spec["metric"])}</div>'
                f'<div class="fig-desc">{spec["desc"]}</div>',
                unsafe_allow_html=True,
            )
        with chart_col:
            show_chart(build_fig(spec))
    st.write("")

# ── Navigation ──────────────────────────────────────────────────────────────
st.sidebar.markdown('<div class="eyebrow">THE BLACK FRIDAY EDITION</div>', unsafe_allow_html=True)
selected = st.sidebar.radio("READ THE ISSUE", list(PAGES.keys()), key="nav")
st.markdown('<div id="top-anchor" style="scroll-margin-top:5rem"></div><a class="to-top" href="#top-anchor" title="Back to top">↑</a>', unsafe_allow_html=True)
page = PAGES[selected]

if selected == "Cover":
    st.markdown('<div class="eyebrow">ROMANIA · 2023–2026 · SPECIAL DATA EDITION</div>', unsafe_allow_html=True)
    st.markdown('<div class="masthead">THE BLACK<br>FRIDAY EDITION</div>', unsafe_allow_html=True)
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
    st.markdown(f'<h2 style="font-size:2.1rem; max-width:850px; line-height:1.15">{page["subtitle"]}</h2>', unsafe_allow_html=True)
    st.markdown(f'<p class="deck">{page["intro"]}</p>', unsafe_allow_html=True)
    st.markdown('<div class="pullquote">“Shopping is a story. And every number has something to say.”</div>', unsafe_allow_html=True)
    st.markdown('<div class="rule"></div><div class="eyebrow">INSIDE THIS ISSUE</div>', unsafe_allow_html=True)
    teasers = [
        ("01", "The Black Friday Effect"),
        ("02", "Planning is the new impulse"),
        ("03", "What's in the cart?"),
        ("04", "The discount dilemma"),
        ("05", "Click, shop, repeat"),
        ("06", "After the click"),
        ("07", "The payment pulse"),
        ("08", "The final edit"),
    ]
    page_names = list(PAGES.keys())
    for row, chunk in enumerate((teasers[:4], teasers[4:])):
        for col, (num, label) in zip(st.columns(4), chunk):
            with col:
                st.button(f"{num} · {label}", key=f"tease_{num}", on_click=go_to, args=(page_names[int(num)],))
    st.info("Click a chapter above, or use the left navigation, to start reading.")
else:
    page_no = selected[:2]
    breadcrumb(page)
    st.title(page["title"])
    st.markdown(f'<p class="deck">{page["subtitle"]}</p>', unsafe_allow_html=True)
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

    # KPIs first, so the headline numbers are the first thing on every page
    st.markdown('<div class="eyebrow" style="margin-bottom:.6rem">AT A GLANCE</div>', unsafe_allow_html=True)
    kpi_row(kpis_for(selected))
    st.write("")

    for n, spec in enumerate(page["figures"], 1):
        render_figure(n, spec, page_no)

    if page.get("take"):
        st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
        st.markdown('<div class="eyebrow">THE EDITORIAL TAKE</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="pullquote">{page["take"]}</div>', unsafe_allow_html=True)

    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
    page_nav(selected)

author_footer()

if st.session_state.pop("scroll_top", False):
    import streamlit.components.v1 as components
    components.html(
        "<script>const d=window.parent.document;"
        "for(const sel of ['[data-testid=\"stMain\"]','section.main','[data-testid=\"stAppViewContainer\"]']){"
        "const e=d.querySelector(sel); if(e) e.scrollTo({top:0,behavior:'instant'});}</script>",
        height=0,
    )

st.sidebar.markdown('<div class="sb-foot">An editorial data experience · Built with Python + Streamlit</div>', unsafe_allow_html=True)
