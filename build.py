#!/usr/bin/env python3
"""
Signature Legal — static site builder.

Edit content here (firm details, advocates, practice areas, articles), then run:

    python3 build.py

It regenerates every .html page so the header, footer and disclaimer
stay identical everywhere. Needs only Python 3.8+ (no installs).
"""
import json
import os
from html import escape as esc

ROOT = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------
# Site settings — change BASE_URL once the domain is live
# --------------------------------------------------------------------------
BASE_URL = "https://signaturelegal.in"   # [YOUR DOMAIN] used for canonical / Open Graph URLs
FORM_ENDPOINT = "[FORM ENDPOINT URL]"     # e.g. https://formspree.io/f/xxxxxx — see README

FIRM = {
    "name": "Signature Legal",
    "tagline": "Counsel you can trust. Advocacy that delivers.",
    "street": "281, 17th F Main, 3rd Cross, KHB Colony, Koramangala 5th Block",
    "city": "Bengaluru",
    "pin": "560038",
    "state": "Karnataka",
    "country": "India",
    "phone": "+91 88923 43289",
    "tel": "tel:+918892343289",
    "email": "contact@signaturelegal.in",
    "hours": "8:00 AM to 9:00 PM",
    "linkedin": "#",   # [LINKEDIN URL]
    "x": "#",          # [X / TWITTER URL]
}
ADDRESS_LINE = f"{FIRM['street']}, {FIRM['city']} – {FIRM['pin']}, {FIRM['state']}, {FIRM['country']}"
MAP_QUERY = "281, 17th F Main, 3rd Cross, KHB Colony, Koramangala 5th Block, Bengaluru 560038"

# --------------------------------------------------------------------------
# People
# --------------------------------------------------------------------------
LEADS = [
    {
        "slug": "freud-richardson",
        "name": "Freud Richardson",
        "role": "Advocate",
        "experience": "More than 10 years",
        "areas": ["Criminal Litigation", "Civil Litigation", "Commercial Litigation"],
        "email": "richardson@signaturelegal.in",
        "photo": "team/freud-richardson.jpg", "photo_size": (373, 466),
        "bio": "Freud Richardson is an advocate with more than ten years of experience in criminal, civil and commercial litigation. "
               "He represents individuals and businesses at every stage of a dispute, from early advice and bail matters to trial and appeal. "
               "His practice rests on thorough preparation and candid, practical advice.",
    },
    {
        "slug": "tahura-anzar",
        "name": "Tahura Anzar",
        "role": "Advocate",
        "experience": "More than 10 years",
        "areas": ["Company Matters (NCLT, NCLAT)", "Debt Recovery", "Arbitration", "Family Law"],
        "email": "tahura@signaturelegal.in",
        "photo": "team/tahura-anzar.jpg", "photo_size": (800, 1000),
        "bio": "Tahura Anzar is an advocate with more than ten years of experience in company law, debt recovery, arbitration and family law. "
               "She advises and represents clients in proceedings before the company law tribunals, in recovery and arbitration matters, and in matrimonial disputes. "
               "She pairs procedural precision with a steady focus on workable outcomes.",
    },
    {
        "slug": "chandana-gururaj",
        "name": "Chandana Gururaj",
        "role": "Advocate",
        "experience": "Nearly 7 years",
        "areas": ["Property Matters", "Civil Litigation"],
        "email": "chandana@signaturelegal.in",
        "bio": "Chandana Gururaj is an advocate with nearly seven years of experience in property matters and civil litigation. "
               "Her work covers title verification, property documentation and civil suits relating to possession, partition and injunctions. "
               "She helps clients understand the risks in a transaction before they commit to it.",
    },
]
ASSOCIATES = [
    {"slug": "lekhan", "name": "Lekhan", "role": "Associate",
     "bio": "Lekhan is an associate at Signature Legal. He assists the firm’s advocates with legal research, drafting and the preparation of matters across the firm’s practice areas."},
    {"slug": "boopathy", "name": "Boopathy", "role": "Associate",
     "bio": "Boopathy is an associate at Signature Legal. He supports the firm’s litigation work, including research, drafting of pleadings and coordination of court filings."},
    {"slug": "samhitha", "name": "Samhitha", "role": "Associate",
     "bio": "Samhitha is an associate at Signature Legal. She assists with research, documentation and client matters, working closely with the firm’s advocates on ongoing cases."},
]
LEAD_BY_SLUG = {p["slug"]: p for p in LEADS}

# --------------------------------------------------------------------------
# Icons (24×24, stroke = currentColor)
# --------------------------------------------------------------------------
def icon(paths, label=None):
    a11y = f'role="img" aria-label="{esc(label)}"' if label else 'aria-hidden="true"'
    return (f'<svg {a11y} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round"><path d="{paths}"/></svg>')

ICONS = {
    "scales": "M12 3v18M7 21h10M4 7h16M4 14l3-7 3 7M4 14a3 3 0 0 0 6 0M14 14l3-7 3 7M14 14a3 3 0 0 0 6 0",
    "gavel": "M13 3l7 7-3 3-7-7zM11.5 8.5 3 17l2 2 8.5-8.5M3 21h10",
    "contract": "M6 3h9l4 4v14H6zM15 3v4h4M9 11h7M9 14h4M9 18c1.5-1.6 2.4.4 3.8-.9 1.2-1.1 1.8.6 3.2.4",
    "building": "M4 21V5h10v16M14 9h6v12M3 21h18M7.5 8.5h3M7.5 12h3M7.5 15.5h3M16.5 12.5h1M16.5 16h1",
    "coins": "M12 3c3.9 0 7 1.3 7 3s-3.1 3-7 3-7-1.3-7-3 3.1-3 7-3zM5 6v6c0 1.7 3.1 3 7 3s7-1.3 7-3V6M5 12v6c0 1.7 3.1 3 7 3s7-1.3 7-3v-6",
    "house": "M3 11l9-7 9 7M5 9.5V20h14V9.5M10 20v-6h4v6",
    "family": "M8 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM16 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM2 20c0-3 2.7-5 6-5s6 2 6 5M14.5 15.2A7 7 0 0 1 16 15c3.3 0 6 2 6 5",
    "briefcase": "M3 8h18v12H3zM9 8V5h6v3M3 13h18",
    "bag": "M5 8h14l-1 13H6zM9 8V6a3 3 0 0 1 6 0v2",
    "receipt": "M6 3h12v18l-2-1.5-2 1.5-2-1.5-2 1.5-2-1.5L6 21zM9 8h6M9 12h6M9 16h3",
    "badge": "M4 7h16v13H4zM9 7V4h6v3M12 13a2 2 0 1 0 0-4 2 2 0 0 0 0 4zM8.5 17.5a3.5 3.5 0 0 1 7 0",
    "pin": "M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21zM12 12a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z",
    "phone": "M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z",
    "mail": "M3 5h18v14H3zM3 6l9 7 9-7",
    "clock": "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM12 7v5l3 2",
    "linkedin": "M4 9h3.5v11H4zM5.75 3.5a2 2 0 1 1 0 4 2 2 0 0 1 0-4zM10 9h3.4v1.6c.5-.9 1.7-1.8 3.4-1.8 3.4 0 4.2 2.2 4.2 5.1V20h-3.5v-5.4c0-1.3 0-2.9-1.8-2.9s-2.1 1.4-2.1 2.8V20H10z",
    "x": "M4 4l16 16M20 4 4 20",
}

# The X logo is a filled glyph; drawn here as a simple outline mark.
def x_icon():
    return ('<svg aria-hidden="true" viewBox="0 0 24 24" fill="currentColor"><path d="M17.8 3h3.1l-6.8 7.8L22 21h-6.2l-4.9-6.4L5.3 21H2.2l7.3-8.3L2 3h6.4l4.4 5.8zm-1.1 16.2h1.7L7.4 4.7H5.6z"/></svg>')

def linkedin_icon():
    return ('<svg aria-hidden="true" viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.5h4V21H3zM9.5 9.5h3.8v1.6h.1c.5-1 1.8-2 3.8-2 4 0 4.8 2.6 4.8 6V21h-4v-5.2c0-1.3 0-2.9-1.8-2.9s-2.1 1.4-2.1 2.8V21h-4z"/></svg>')

def logo_mark(r, variant="navy"):
    """The firm's pen-nib mark (from the supplied logo files)."""
    return (f'<img class="brand-mark" src="{r}assets/img/brand/mark-{variant}-128.png" '
            f'srcset="{r}assets/img/brand/mark-{variant}-128.png 1x, {r}assets/img/brand/mark-{variant}-512.png 4x" '
            f'width="40" height="44" alt="">')

def person_img(r, p, eager=False):
    if p.get("photo"):
        w, h = p["photo_size"]
        loading = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
        return (f'<figure class="ph ph--real"><img src="{r}assets/img/{p["photo"]}" '
                f'alt="Portrait of {esc(p["name"])}, {p.get("role", "Advocate")}" width="{w}" height="{h}" {loading}></figure>')
    return ph_img(r, "portrait-placeholder.svg", f'Photo placeholder for {p["name"]}', "[PHOTO]")

# --------------------------------------------------------------------------
# Practice areas
# --------------------------------------------------------------------------
PRACTICES = [
    {
        "slug": "civil-litigation", "title": "Civil Litigation", "icon": "scales",
        "short": "Suits, injunctions, recovery and appeals before civil courts.",
        "overview": "Civil disputes can affect your property, your money and your relationships for years. We represent individuals, families and businesses in civil proceedings, from the first legal notice through trial, execution and appeal.",
        "approach": "We start by understanding the outcome that actually matters to you, then choose the route — negotiation, mediation or litigation — most likely to achieve it.",
        "matters": ["Suits for recovery of money", "Injunctions and urgent interim relief", "Declaration and specific performance suits",
                    "Partition and possession suits", "Execution of decrees", "Appeals and revision petitions"],
        "team": ["freud-richardson", "chandana-gururaj"],
    },
    {
        "slug": "criminal-law", "title": "Criminal Law", "icon": "gavel",
        "short": "Bail, trial defence, complaints and criminal appeals.",
        "overview": "Criminal proceedings move quickly, and the earliest steps often matter most. We advise and represent accused persons and complainants from the stage of a complaint or FIR, through investigation and trial, to appeal.",
        "approach": "We explain each stage of the procedure plainly, so you know what to expect, what is required of you and what your options are.",
        "matters": ["Anticipatory and regular bail", "Defence at trial", "Quashing petitions before the High Court",
                    "Cheque dishonour cases under the Negotiable Instruments Act", "Economic and white-collar offences", "Criminal appeals and revisions"],
        "team": ["freud-richardson"],
    },
    {
        "slug": "commercial-litigation-arbitration", "title": "Commercial Litigation & Arbitration", "icon": "contract",
        "short": "Contract and business disputes in commercial courts and arbitration.",
        "overview": "Commercial disputes put contracts, cash flow and business relationships at stake. We act for companies, firms and individuals in commercial suits and in arbitration under the Arbitration and Conciliation Act, 1996.",
        "approach": "Where a dispute can be settled on sensible commercial terms we pursue that; where it cannot, we prepare to see it through to an award or decree.",
        "matters": ["Breach of contract and commercial suits", "Pre-institution mediation under the Commercial Courts Act, 2015",
                    "Domestic arbitration proceedings", "Applications for interim measures", "Challenges to and enforcement of arbitral awards",
                    "Partnership and shareholder disputes"],
        "team": ["freud-richardson", "tahura-anzar"],
    },
    {
        "slug": "company-law-nclt-nclat", "title": "Company Law Matters (NCLT & NCLAT)", "icon": "building",
        "short": "Representation before the National Company Law Tribunal and its appellate tribunal.",
        "overview": "The National Company Law Tribunal (NCLT) and the National Company Law Appellate Tribunal (NCLAT) hear corporate disputes under the Companies Act, 2013 and insolvency matters under the Insolvency and Bankruptcy Code, 2016. We represent companies, directors, shareholders, creditors and resolution professionals before them.",
        "approach": "Tribunal proceedings are document-heavy and time-bound. We focus on getting the record right early and on meeting every procedural deadline.",
        "matters": ["Oppression and mismanagement petitions", "Corporate insolvency resolution applications",
                    "Schemes of compromise, arrangement and amalgamation", "Restoration of struck-off companies",
                    "Compounding and other statutory applications", "Appeals before the NCLAT"],
        "team": ["tahura-anzar"],
    },
    {
        "slug": "debt-recovery-insolvency", "title": "Debt Recovery, Insolvency & Bankruptcy", "icon": "coins",
        "short": "Recovery and insolvency proceedings for creditors and debtors.",
        "overview": "Unpaid dues and financial distress call for timely, well-chosen action. We act for creditors and for borrowers and guarantors in recovery and insolvency proceedings.",
        "approach": "For creditors, we help select the remedy that best fits the debt and the debtor. For borrowers and guarantors, we focus on understanding exposure early and on options for settlement or restructuring.",
        "matters": ["Recovery applications before Debts Recovery Tribunals", "Proceedings under the SARFAESI Act, 2002",
                    "Insolvency applications by financial and operational creditors", "Personal guarantor insolvency",
                    "Demand notices and pre-litigation recovery", "Settlement negotiations"],
        "team": ["tahura-anzar"],
    },
    {
        "slug": "property-real-estate", "title": "Property & Real Estate Law", "icon": "house",
        "short": "Title checks, property documentation and property disputes.",
        "overview": "Property is often the largest investment a family or business makes. We help clients buy, sell, hold and protect immovable property, and represent them when disputes arise.",
        "approach": "Before a transaction, we verify title and documents so you understand the risks. Once a dispute begins, we act to protect your title and possession.",
        "matters": ["Title verification and due diligence", "Sale deeds, agreements to sell and leases",
                    "Partition and family property disputes", "Possession, injunction and eviction suits",
                    "Khata, mutation and registration matters", "Disputes with builders and developers"],
        "team": ["chandana-gururaj"],
    },
    {
        "slug": "family-matrimonial", "title": "Family & Matrimonial Law", "icon": "family",
        "short": "Divorce, maintenance and custody matters, handled with discretion.",
        "overview": "Family disputes are personal and often painful. We advise and represent clients in matrimonial and family matters with sensitivity and strict confidentiality.",
        "approach": "Wherever possible we explore mediation and settlement, especially where children are involved, while protecting your rights in court where settlement is not possible.",
        "matters": ["Divorce by mutual consent and contested divorce", "Maintenance and alimony", "Child custody and guardianship",
                    "Domestic violence proceedings", "Judicial separation and restitution of conjugal rights", "Settlement agreements and mediation"],
        "team": ["tahura-anzar"],
    },
    {
        "slug": "corporate-advisory-compliance", "title": "Corporate Advisory & Compliance", "icon": "briefcase",
        "short": "Contracts, governance and regulatory compliance for businesses.",
        "overview": "Sound advice early prevents disputes later. We support businesses with commercial contracts, corporate governance and routine regulatory compliance.",
        "approach": "We aim for advice that fits how your business actually operates, written so that the people who must act on it can understand it.",
        "matters": ["Drafting and review of commercial agreements", "Incorporation and structuring of entities",
                    "Shareholder and founder agreements", "Board and shareholder meeting compliance",
                    "Responses to regulatory notices", "Contract risk reviews"],
        "team": [],
    },
    {
        "slug": "consumer-disputes", "title": "Consumer Disputes", "icon": "bag",
        "short": "Complaints and defence before consumer commissions.",
        "overview": "When goods or services fall short, the Consumer Protection Act, 2019 offers a dedicated forum for relief. We represent consumers filing complaints and businesses responding to them.",
        "approach": "We help you assess whether a consumer complaint is the right route, which commission has jurisdiction, and what evidence you will need before you file.",
        "matters": ["Complaints before District, State and National Commissions", "Deficiency in service and defective goods",
                    "Consumer complaints against builders", "Insurance claim disputes",
                    "Defence of complaints for businesses", "Appeals and execution of orders"],
        "team": [],
    },
    {
        "slug": "tax-advisory", "title": "Tax Advisory", "icon": "receipt",
        "short": "Guidance on income tax and GST notices, assessments and appeals.",
        "overview": "Tax notices and assessments call for careful, timely responses. We advise individuals and businesses on direct and indirect tax matters and represent them in proceedings.",
        "approach": "Where specialist accounting input is needed, we work alongside your chartered accountant so the legal and financial positions stay consistent.",
        "matters": ["Responses to income tax and GST notices", "Assessment and reassessment proceedings",
                    "Appeals before appellate authorities", "Tax implications of transactions",
                    "GST compliance advisory", "Tax-related litigation"],
        "team": [],
    },
    {
        "slug": "employment-labour", "title": "Employment & Labour Law", "icon": "badge",
        "short": "Employment contracts, workplace disputes and labour compliance.",
        "overview": "Employment relationships are governed by contracts, statutes and workplace policies. We advise employers and employees on their rights and obligations, and represent them in disputes.",
        "approach": "For employers we focus on clear policies and documented processes that prevent disputes; for employees, on a clear-eyed view of their rights and remedies.",
        "matters": ["Employment contracts and workplace policies", "Termination and separation matters",
                    "Prevention of sexual harassment (POSH) compliance and inquiries", "Wage, gratuity and benefit claims",
                    "Disputes before labour authorities and courts", "Labour law compliance reviews"],
        "team": [],
    },
]

APPROACH_STEPS = [
    ("Understand the matter", "We listen, review your documents and identify the facts and deadlines that matter."),
    ("Set out your options", "We explain the available routes, their likely costs and timelines, and their risks, in plain language."),
    ("Act, and keep you informed", "Once you decide, we act promptly and tell you what has happened at each stage."),
]

# --------------------------------------------------------------------------
# Insights (placeholder articles — review before publishing)
# --------------------------------------------------------------------------
ARTICLES = [
    {
        "slug": "nclt-process-basics",
        "title": "The NCLT process: a plain-language introduction",
        "date": "[Publication date]",
        "excerpt": "What the National Company Law Tribunal does, the kinds of matters it hears, and how a corporate insolvency case moves from application to outcome.",
        "body": """
<p>The National Company Law Tribunal (NCLT) is a quasi-judicial body set up under the Companies Act, 2013. It hears a wide range of company law disputes and is also the adjudicating authority for corporate insolvency under the Insolvency and Bankruptcy Code, 2016 (IBC). The NCLT sits in benches across India, including a bench in Bengaluru.</p>
<h2>What the NCLT hears</h2>
<ul>
<li>Petitions alleging oppression of shareholders or mismanagement of a company.</li>
<li>Schemes of compromise, arrangement, merger and amalgamation.</li>
<li>Applications to restore companies struck off the register.</li>
<li>Corporate insolvency resolution and liquidation of companies and limited liability partnerships.</li>
</ul>
<h2>How a corporate insolvency case begins</h2>
<p>A corporate insolvency resolution process (CIRP) can be started by a financial creditor, an operational creditor or the company itself, when there is a default of at least the minimum amount prescribed (currently ₹1 crore). An operational creditor, such as a supplier, must first serve a demand notice and give the company an opportunity to dispute the debt or pay.</p>
<h2>What happens after admission</h2>
<p>If the NCLT admits the application, a moratorium generally comes into force, which pauses most legal proceedings against the company. An insolvency professional takes over management, and a committee of creditors is formed. The committee considers resolution plans; if no plan is approved within the time allowed, the company may go into liquidation.</p>
<h2>Appeals</h2>
<p>Orders of the NCLT can be appealed to the National Company Law Appellate Tribunal (NCLAT), and from there, on questions of law, to the Supreme Court of India. Strict time limits apply to appeals, so advice should be taken promptly.</p>
""",
    },
    {
        "slug": "property-title-checks",
        "title": "Understanding property title checks before you buy",
        "date": "[Publication date]",
        "excerpt": "The documents that usually make up a title check for property in Bengaluru, and why each one matters before you sign an agreement.",
        "body": """
<p>A title check is an examination of the documents that show who owns a property and whether it can be sold free of claims. It is best done before you sign an agreement to sell or pay a significant advance.</p>
<h2>Documents commonly reviewed</h2>
<ul>
<li><strong>Chain of title deeds.</strong> Sale deeds, gift deeds, partition deeds or wills showing how ownership passed to the present seller, typically for the past 30 years.</li>
<li><strong>Encumbrance certificate.</strong> Issued by the sub-registrar’s office, it records registered transactions such as mortgages or sales affecting the property over a period.</li>
<li><strong>Khata and property tax records.</strong> Municipal records showing the property is assessed in the seller’s name and that taxes are paid.</li>
<li><strong>Approvals.</strong> Sanctioned building plan, and for completed buildings, the occupancy or completion certificate.</li>
<li><strong>Land records.</strong> For land that was agricultural, the RTC (record of rights) and the order converting it to non-agricultural use.</li>
<li><strong>RERA registration.</strong> For under-construction projects, registration with the Karnataka Real Estate Regulatory Authority.</li>
</ul>
<h2>Common warning signs</h2>
<p>Gaps in the chain of title, sales through powers of attorney, pending litigation, unexplained differences in measurements, and properties where only photocopies are available all need careful scrutiny before you proceed.</p>
<h2>Why it is worth doing</h2>
<p>Defects found after registration are far harder and costlier to fix than defects found before. A careful review lets you negotiate, ask the seller to cure problems, or walk away.</p>
""",
    },
    {
        "slug": "before-filing-consumer-complaint",
        "title": "What to know before filing a consumer complaint",
        "date": "[Publication date]",
        "excerpt": "Who can file, which commission to approach, the time limit, and the documents to gather before you file under the Consumer Protection Act, 2019.",
        "body": """
<p>The Consumer Protection Act, 2019 lets consumers seek relief for defective goods, deficient services and unfair trade practices before consumer commissions at the district, state and national levels.</p>
<h2>Who can file</h2>
<p>Generally, a person who buys goods or avails services for consideration, and not for resale or a commercial purpose, is a consumer under the Act. Complaints can also be filed by certain associations and by the government in some cases.</p>
<h2>Which commission</h2>
<p>The forum depends on the value of the goods or services paid for. At the time of writing, District Commissions hear complaints up to ₹50 lakh, State Commissions from ₹50 lakh to ₹2 crore, and the National Commission above ₹2 crore. These limits can be revised, so check the current position before filing. You may usually file where you live or work, or where the opposite party carries on business.</p>
<h2>Time limit</h2>
<p>A complaint should ordinarily be filed within two years of the date on which the cause of action arose. Delay may be condoned only for sufficient cause.</p>
<h2>Before you file</h2>
<ul>
<li>Keep invoices, receipts, warranty cards, brochures and all correspondence.</li>
<li>Write to the seller or service provider setting out the problem and what you want done; a formal notice often resolves the matter.</li>
<li>Record dates carefully, as they matter for the time limit.</li>
<li>Complaints can be filed online through the e-Daakhil portal.</li>
</ul>
""",
    },
]

# --------------------------------------------------------------------------
# Shared components
# --------------------------------------------------------------------------
NAV = [
    ("index.html", "Home", "home"),
    ("about.html", "About", "about"),
    ("practice-areas.html", "Practice Areas", "practice"),
    ("team.html", "Our Team", "team"),
    ("insights.html", "Insights", "insights"),
    ("careers.html", "Careers", "careers"),
]

def header(r, active):
    links = "".join(
        f'<li><a href="{r}{href}"{" aria-current=\"page\"" if key == active else ""}>{label}</a></li>'
        for href, label, key in NAV
    )
    return f"""<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="{r}index.html" aria-label="Signature Legal, home">{logo_mark(r)}<span class="brand-name">SIGNATURE LEGAL</span></a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu"><span></span><span></span><span></span></button>
    <nav id="site-nav" class="site-nav" aria-label="Main">
      <ul>{links}</ul>
      <a class="btn btn-navy" href="{r}contact.html"{" aria-current=\"page\"" if active == "contact" else ""}>Contact Us</a>
    </nav>
  </div>
</header>"""

def footer(r):
    quick = [("index.html", "Home"), ("about.html", "About"), ("practice-areas.html", "Practice Areas"),
             ("team.html", "Our Team"), ("insights.html", "Insights"), ("careers.html", "Careers"), ("contact.html", "Contact")]
    quick_html = "".join(f'<li><a href="{r}{h}">{l}</a></li>' for h, l in quick)
    prac_html = "".join(f'<li><a href="{r}practice-areas/{p["slug"]}.html">{esc(p["title"])}</a></li>' for p in PRACTICES)
    return f"""<footer class="site-footer">
  <div class="container footer-top">
    <div>
      <a class="brand" href="{r}index.html" aria-label="Signature Legal, home">{logo_mark(r, "white")}<span class="brand-name">SIGNATURE LEGAL</span></a>
      <p>{esc(FIRM['tagline'])}</p>
      <div class="social">
        <a href="{FIRM['linkedin']}" aria-label="Signature Legal on LinkedIn (link to be added)">{linkedin_icon()}</a>
        <a href="{FIRM['x']}" aria-label="Signature Legal on X (link to be added)">{x_icon()}</a>
      </div>
    </div>
    <nav aria-label="Footer">
      <h2>Quick links</h2>
      <ul>{quick_html}</ul>
    </nav>
    <nav aria-label="Practice areas">
      <h2>Practice areas</h2>
      <ul>{prac_html}</ul>
    </nav>
    <div>
      <h2>Office</h2>
      <address>{esc(FIRM['street'])},<br>{FIRM['city']} – {FIRM['pin']}, {FIRM['state']}, {FIRM['country']}</address>
      <ul style="margin-top:14px">
        <li><a href="{FIRM['tel']}">{FIRM['phone']}</a></li>
        <li><a href="mailto:{FIRM['email']}">{FIRM['email']}</a></li>
        <li>Working hours: {FIRM['hours']}</li>
      </ul>
    </div>
  </div>
  <div class="container footer-bottom">
    <p>As per the rules of the Bar Council of India, this website is for information only and is not an advertisement or solicitation. Nothing on it is legal advice, and using it does not create an advocate-client relationship.</p>
    <div class="footer-legal">
      <p>© 2026 Signature Legal. All rights reserved.</p>
      <a href="{r}disclaimer.html">Disclaimer</a>
      <a href="{r}privacy.html">Privacy Policy</a>
      <a href="{r}terms.html">Terms of Use</a>
    </div>
  </div>
</footer>"""

def consent_modal(r):
    return f"""<div class="consent" id="consent" role="dialog" aria-modal="true" aria-labelledby="consent-title" aria-describedby="consent-desc" hidden>
  <div class="consent-box">
    <img class="consent-logo" src="{r}assets/img/brand/logo-full-navy.png" width="130" height="145" alt="Signature Legal">
    <h2 id="consent-title">Disclaimer</h2>
    <div id="consent-desc">
      <p>Under the rules of the Bar Council of India, law firms are not permitted to solicit work or advertise. By clicking ‘I AGREE’, the user acknowledges that:</p>
      <ol>
        <li>the user wishes to know more about Signature Legal, its practice areas and its advocates, for their own information;</li>
        <li>the information is provided only on the user’s request and use of this site does not create an advocate-client relationship;</li>
        <li>nothing on this website is legal advice or a legal opinion;</li>
        <li>Signature Legal is not liable for any action taken in reliance on this website, and users must seek independent legal advice.</li>
      </ol>
    </div>
    <div class="consent-actions">
      <button type="button" class="btn btn-navy" data-consent="agree">I AGREE</button>
      <button type="button" class="btn btn-line" data-consent="disagree">DISAGREE</button>
    </div>
  </div>
</div>"""

def json_ld():
    data = {
        "@context": "https://schema.org",
        "@type": "LegalService",
        "name": "Signature Legal",
        "url": BASE_URL + "/",
        "logo": BASE_URL + "/assets/img/icon-512.png",
        "image": BASE_URL + "/assets/img/og-image.jpg",
        "telephone": "+91-8892343289",
        "email": FIRM["email"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": FIRM["street"],
            "addressLocality": "Bengaluru",
            "addressRegion": "Karnataka",
            "postalCode": "560038",
            "addressCountry": "IN",
        },
        "openingHours": "Mo-Su 08:00-21:00",  # [CONFIRM working days]
        "areaServed": "Bengaluru, Karnataka, India",
        "employee": [{"@type": "Person", "name": p["name"], "jobTitle": "Advocate", "email": p["email"]} for p in LEADS],
    }
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, indent=2) + "</script>"

def page(path, title, desc, active, body, ld=False):
    depth = path.count("/")
    r = "../" * depth
    full_title = title if title.startswith("Signature Legal") else f"{title} | Signature Legal, Bengaluru"
    url = f"{BASE_URL}/{'' if path == 'index.html' else path}"
    return f"""<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Signature Legal">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE_URL}/assets/img/og-image.jpg">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0B1F3A">
<link rel="icon" href="{r}assets/img/favicon-64.png" type="image/png" sizes="64x64">
<link rel="apple-touch-icon" href="{r}assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="{r}assets/css/style.css">
{json_ld() if ld else ""}
</head>
<body>
{header(r, active)}
<main id="main">
{body}
</main>
{footer(r)}
{consent_modal(r)}
<script src="{r}assets/js/script.js" defer></script>
</body>
</html>
"""

def page_head(title, intro, crumbs, r):
    items = "".join(f'<li><a href="{r}{h}">{esc(l)}</a></li>' for h, l in crumbs)
    return f"""<section class="page-head">
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb"><ol><li><a href="{r}index.html">Home</a></li>{items}<li><span aria-current="page">{esc(title)}</span></li></ol></nav>
    <h1>{esc(title)}</h1>
    {f'<p>{intro}</p>' if intro else ''}
  </div>
</section>"""

def ph_img(r, file, alt, label, w=800, h=1000, eager=False):
    loading = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<figure class="ph" data-ph="{esc(label)}"><img src="{r}assets/img/{file}" alt="{esc(alt)}" '
            f'width="{w}" height="{h}" {loading}></figure>')

def cta_band(r):
    return f"""<section class="section section--navy cta-band">
  <div class="container reveal">
    <div>
      <h2>Have a legal matter? Let’s talk.</h2>
      <p>Call {FIRM['phone']} or write to {FIRM['email']}. We’re available {FIRM['hours']}.</p>
    </div>
    <a class="btn btn-brass" href="{r}contact.html">Contact Us</a>
  </div>
</section>"""

def practice_list(r):
    items = "".join(
        f'<li><a class="practice-link" href="{r}practice-areas/{p["slug"]}.html">{icon(ICONS[p["icon"]])}'
        f'<h3>{esc(p["title"])}</h3><p>{esc(p["short"])}</p></a></li>'
        for p in PRACTICES
    )
    return f'<ul class="practice-grid">{items}</ul>'

def practices_for(slug):
    return [p for p in PRACTICES if slug in p["team"]]

# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------
def build_home():
    r = ""
    people = "".join(
        f"""<li class="person reveal">
  {person_img(r, p)}
  <h3><a href="team.html#{p['slug']}">{esc(p['name'])}</a></h3>
  <p class="role">{p['role']}, {p['experience'].lower()} of experience</p>
  <p class="areas">{esc(', '.join(p['areas']))}</p>
</li>""" for p in LEADS)
    body = f"""
<section class="hero">
  <div class="container hero-grid">
    <div class="hero-anim">
      <h1>Counsel you can trust. Advocacy that delivers.</h1>
      <hr class="hero-rule">
      <p>Signature Legal is a Bengaluru law firm offering clear, client-focused legal solutions in litigation, arbitration and advisory matters.</p>
      <div class="hero-actions">
        <a class="btn btn-brass" href="contact.html">Contact Us</a>
        <a class="btn btn-line" href="practice-areas.html">View practice areas</a>
      </div>
    </div>
    <figure class="hero-logo"><img src="assets/img/brand/logo-full-white.png" width="520" height="578" alt="Signature Legal logo: a fountain-pen nib within a crescent" fetchpriority="high"></figure>
  </div>
</section>

<section class="section">
  <div class="container split split--media">
    <div class="reveal">
      <h2>About the firm</h2>
      <p class="lede">We advise and represent individuals, families and businesses across civil, criminal, commercial, company and property matters.</p>
      <p>Our advocates handle each matter personally, explain the law in plain terms and keep clients informed at every stage, so that decisions are made with a clear understanding of the options and risks.</p>
      <a class="text-link" href="about.html">Learn more about Signature Legal</a>
    </div>
    <div class="reveal">{ph_img(r, 'books-placeholder.svg', 'Placeholder image of law books on a shelf', '[PLACEHOLDER IMAGE]', 900, 700)}</div>
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <div class="section-head reveal">
      <h2>Practice areas</h2>
      <p>Select an area to see the matters we handle and how we approach them.</p>
    </div>
    {practice_list(r)}
  </div>
</section>

<section class="section section--navy">
  <div class="container">
    <div class="section-head reveal"><h2>Why Signature Legal</h2></div>
    <div class="values reveal">
      <div><h3>Strategic clarity</h3><p>We identify what matters most in your case and build a plan around it.</p></div>
      <div><h3>Client-centric approach</h3><p>Your goals shape our advice, and we explain each step in plain language.</p></div>
      <div><h3>Integrity</h3><p>Honest assessments, including when the news is not what you hoped to hear.</p></div>
      <div><h3>Responsiveness</h3><p>Prompt replies and regular updates, from {FIRM['hours']}.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <h2>Our advocates</h2>
      <a class="text-link" href="team.html">Meet the full team</a>
    </div>
    <ul class="people">{people}</ul>
  </div>
</section>
{cta_band(r)}
"""
    return page("index.html", "Signature Legal | Advocates in Koramangala, Bengaluru",
                "Signature Legal is a law firm in Koramangala, Bengaluru, handling civil, criminal, commercial, company, property and family law matters.",
                "home", body, ld=True)

def build_about():
    r = ""
    body = f"""
{page_head('About Signature Legal', 'A Bengaluru law firm built on clear advice and careful advocacy.', [], r)}
<section class="section">
  <div class="container split">
    <div class="prose reveal">
      <h2>Our story</h2>
      <p>Signature Legal was founded in Bengaluru by advocates who believed that clients deserve to understand their own case. <span class="editable">[editable]</span></p>
      <p>From our office in Koramangala, the firm advises and represents individuals, families and businesses in litigation, arbitration and advisory work. We have deliberately stayed a focused team, so that every matter receives the personal attention of an advocate.</p>
      <p class="muted small">[Add founding year and any further history here.]</p>
    </div>
    <div class="reveal">{ph_img(r, 'architecture-placeholder.svg', 'Placeholder image of abstract architecture', '[PLACEHOLDER IMAGE]', 900, 700)}</div>
  </div>
</section>
<section class="section section--alt">
  <div class="container split">
    <div class="prose reveal">
      <h2>Our philosophy</h2>
      <p>Good legal work is not only about winning arguments. It is about understanding what the client needs, giving an honest view of the options, and pursuing the chosen course with care and persistence.</p>
      <p>We prefer to resolve disputes early where that serves the client, and we are prepared to litigate fully where it does not.</p>
    </div>
    <div class="prose reveal">
      <h2>How we work</h2>
      <ol class="steps">
        {''.join(f'<li><div><h3>{t}</h3><p>{d}</p></div></li>' for t, d in APPROACH_STEPS)}
      </ol>
    </div>
  </div>
</section>
<section class="section section--navy">
  <div class="container">
    <div class="section-head reveal"><h2>Our values</h2></div>
    <div class="values reveal">
      <div><h3>Strategic clarity</h3><p>A clear plan built around what matters most in your matter.</p></div>
      <div><h3>Client-centric approach</h3><p>Your goals and circumstances shape every piece of advice.</p></div>
      <div><h3>Integrity</h3><p>Honest assessments, confidentiality and adherence to the profession’s rules.</p></div>
      <div><h3>Responsiveness</h3><p>Prompt replies and regular updates on every matter.</p></div>
    </div>
  </div>
</section>
{cta_band(r)}
"""
    return page("about.html", "About Us", "Learn about Signature Legal, a law firm in Koramangala, Bengaluru: our story, philosophy, approach and values.", "about", body)

def build_practice_index():
    r = ""
    body = f"""
{page_head('Practice Areas', 'We advise and represent clients across eleven areas of law. Select an area to learn more.', [], r)}
<section class="section">
  <div class="container">{practice_list(r)}</div>
</section>
{cta_band(r)}
"""
    return page("practice-areas.html", "Practice Areas", "Practice areas of Signature Legal, Bengaluru: civil, criminal, commercial and arbitration, company law (NCLT/NCLAT), property, family, consumer, tax and employment law.", "practice", body)

def build_practice(p):
    r = "../"
    if p["team"]:
        team_html = "<ul>" + "".join(
            f'<li><a href="{r}team.html#{s}">{esc(LEAD_BY_SLUG[s]["name"])}</a><br><span class="muted small">Advocate</span></li>'
            for s in p["team"]) + "</ul>"
    else:
        team_html = ("<!-- [ASSIGN ADVOCATE(S) for this practice area in build.py → PRACTICES → team] -->"
                     f'<p>Matters in this area are handled by the firm’s team. <a href="{r}contact.html">Contact us</a> and we will direct you to the right advocate.</p>')
    others = [o for o in PRACTICES if o["slug"] != p["slug"]][:5]
    body = f"""
{page_head(p['title'], esc(p['short']), [('practice-areas.html', 'Practice Areas')], r)}
<section class="section">
  <div class="container detail">
    <div>
      <section class="reveal">
        <h2>Overview</h2>
        <p class="lede">{esc(p['overview'])}</p>
      </section>
      <section class="reveal">
        <h2>Matters we handle</h2>
        <ul class="matters">{''.join(f'<li>{esc(m)}</li>' for m in p['matters'])}</ul>
      </section>
      <section class="reveal">
        <h2>How we approach them</h2>
        <p>{esc(p['approach'])}</p>
        <ol class="steps">{''.join(f'<li><div><h3>{t}</h3><p>{d}</p></div></li>' for t, d in APPROACH_STEPS)}</ol>
      </section>
      <p class="note">This page describes our work in general terms and is not legal advice. Every matter depends on its own facts.</p>
    </div>
    <aside>
      <div class="aside-box">
        <h2>{'Advocates' if len(p['team']) > 1 else 'Advocate' if p['team'] else 'Who handles this'}</h2>
        {team_html}
        <a class="btn btn-navy" style="margin-top:18px;width:100%" href="{r}contact.html">Contact Us</a>
      </div>
      <div class="aside-box">
        <h2>Other practice areas</h2>
        <ul>{''.join(f'<li><a href="{o["slug"]}.html">{esc(o["title"])}</a></li>' for o in others)}</ul>
        <a class="text-link" href="{r}practice-areas.html">All practice areas</a>
      </div>
    </aside>
  </div>
</section>
{cta_band(r)}
"""
    return page(f"practice-areas/{p['slug']}.html", p["title"], f"{p['title']} at Signature Legal, Bengaluru. {p['short']}", "practice", body)

def build_team():
    r = ""
    leads = ""
    for p in LEADS:
        prac_links = ", ".join(f'<a href="practice-areas/{x["slug"]}.html">{esc(x["title"])}</a>' for x in practices_for(p["slug"]))
        leads += f"""
<article class="profile reveal" id="{p['slug']}">
  {person_img(r, p)}
  <div>
    <h2>{esc(p['name'])}</h2>
    <p class="role">{p['role']}</p>
    <dl class="facts">
      <dt>Experience</dt><dd>{p['experience']}</dd>
      <dt>Areas of practice</dt><dd>{esc(', '.join(p['areas']))}</dd>
    </dl>
    <p>{esc(p['bio'])} <span class="editable">[editable]</span></p>
    <p class="small muted">Related practice areas: {prac_links}</p>
    <div class="icon-links">
      <a class="icon-link" href="mailto:{p['email']}">{icon(ICONS['mail'])}{p['email']}</a>
      <a class="icon-link" href="#" aria-label="{esc(p['name'])} on LinkedIn (link to be added)">{linkedin_icon()}LinkedIn [LINKEDIN URL]</a>
    </div>
  </div>
</article>"""
    assoc = "".join(f"""
<li class="person reveal" id="{a['slug']}">
  {ph_img(r, 'portrait-placeholder.svg', f'Photo placeholder for {a["name"]}', '[PHOTO]')}
  <h3>{esc(a['name'])}</h3>
  <p class="role">{a['role']}</p>
  <p class="areas">{esc(a['bio'])} <span class="editable">[editable]</span></p>
  <div class="icon-links" style="margin-top:12px">
    <a class="icon-link" href="#" aria-label="{esc(a['name'])} on LinkedIn (link to be added)">{linkedin_icon()}LinkedIn</a>
  </div>
</li>""" for a in ASSOCIATES)
    body = f"""
{page_head('Our Team', 'Our advocates handle each matter personally, supported by a team of associates.', [], r)}
<section class="section">
  <div class="container">
    <h2 class="visually-hidden">Lead advocates</h2>
    {leads}
  </div>
</section>
<section class="section section--alt">
  <div class="container">
    <div class="section-head reveal"><h2>Associates</h2><p>For enquiries, please write to <a href="mailto:{FIRM['email']}">{FIRM['email']}</a>.</p></div>
    <ul class="people">{assoc}</ul>
  </div>
</section>
{cta_band(r)}
"""
    return page("team.html", "Our Team", "Meet the advocates and associates of Signature Legal, Bengaluru: Freud Richardson, Tahura Anzar, Chandana Gururaj and team.", "team", body)

def build_insights():
    r = ""
    cards = "".join(f"""
<li class="reveal"><article class="post">
  <time>{a['date']}</time>
  <h2><a href="insights/{a['slug']}.html">{esc(a['title'])}</a></h2>
  <p>{esc(a['excerpt'])}</p>
  <a class="text-link" href="insights/{a['slug']}.html" aria-label="Read more: {esc(a['title'])}">Read more</a>
</article></li>""" for a in ARTICLES)
    body = f"""
{page_head('Insights', 'Short, plain-language notes on legal topics that commonly affect individuals and businesses.', [], r)}
<section class="section">
  <div class="container">
    <ul class="posts">{cards}</ul>
    <div class="note"><p>These articles are for general information only. They are not legal advice and may not reflect the latest changes in law. Please seek advice on your specific situation.</p></div>
  </div>
</section>
"""
    return page("insights.html", "Insights", "Legal awareness articles from Signature Legal, Bengaluru, on NCLT proceedings, property title checks and consumer complaints.", "insights", body)

def build_article(a):
    r = "../"
    body = f"""
{page_head(a['title'], f"<time>{a['date']}</time>", [('insights.html', 'Insights')], r)}
<section class="section">
  <div class="container">
    <article class="prose">
      <p class="note" style="margin:0 0 32px"><strong>Placeholder article:</strong> review, edit and date this content before publishing. <span class="editable">[editable]</span></p>
      {a['body']}
      <div class="note"><p>This article is for general information only and is not legal advice. The law may have changed since it was written. For advice on your situation, please <a href="{r}contact.html">contact us</a>.</p></div>
      <p style="margin-top:32px"><a class="text-link" href="{r}insights.html">Back to Insights</a></p>
    </article>
  </div>
</section>
"""
    return page(f"insights/{a['slug']}.html", a["title"], a["excerpt"], "insights", body)

def field(id_, label, type_="text", required=True, extra="", hint=None, autocomplete=None):
    req = ' <span class="req" aria-hidden="true">*</span>' if required else ""
    ac = f' autocomplete="{autocomplete}"' if autocomplete else ""
    desc = f"{id_}-error" + (f" {id_}-hint" if hint else "")
    hint_html = f'<span class="hint" id="{id_}-hint">{hint}</span>' if hint else ""
    if type_ == "textarea":
        control = f'<textarea id="{id_}" name="{id_}" data-label="{label}" {"required" if required else ""} aria-describedby="{desc}" {extra}></textarea>'
    else:
        control = f'<input id="{id_}" name="{id_}" type="{type_}" data-label="{label}"{ac} {"required" if required else ""} aria-describedby="{desc}" {extra}>'
    return f'<div class="field"><label for="{id_}">{label}{req}</label>{control}{hint_html}<span class="error" id="{id_}-error" aria-live="polite"></span></div>'

def build_careers():
    r = ""
    body = f"""
{page_head('Careers & Internships', 'We welcome applications from law students and young advocates who want to learn the craft of careful, client-focused practice.', [], r)}
<section class="section">
  <div class="container split">
    <div class="prose reveal">
      <h2>Working with us</h2>
      <p>Interns and junior advocates at Signature Legal work directly with our advocates on live matters: researching, drafting, attending court and meeting clients.</p>
      <h3>Internships</h3>
      <p>Open to law students. Please apply with your CV, your year of study and your preferred dates. <span class="muted">[Add internship duration and terms]</span></p>
      <h3>Junior associates</h3>
      <p>Open to advocates enrolled with a State Bar Council. Please include your enrolment details and areas of interest.</p>
      <p>You can also email your application to <a href="mailto:{FIRM['email']}?subject=Application">{FIRM['email']}</a>.</p>
    </div>
    <div class="reveal">
      <h2>Apply</h2>
      <form class="form" novalidate data-validate data-endpoint="{FORM_ENDPOINT}" data-subject="Careers application" data-success="Thank you. Your application has been received; we will contact you if your profile matches a current opening.">
        <input type="hidden" name="_subject" value="Careers application – Signature Legal">
        <div class="visually-hidden" aria-hidden="true"><label for="c-gotcha">Leave this empty</label><input id="c-gotcha" name="_gotcha" tabindex="-1" autocomplete="off"></div>
        <div class="form-row">
          {field('name', 'Full name', autocomplete='name')}
          {field('email', 'Email', 'email', autocomplete='email')}
        </div>
        <div class="form-row">
          {field('phone', 'Phone', 'tel', autocomplete='tel')}
          {field('college', 'College or enrolment number')}
        </div>
        <div class="field">
          <label for="position">Position <span class="req" aria-hidden="true">*</span></label>
          <select id="position" name="position" data-label="Position" required aria-describedby="position-error">
            <option value="">Select a position</option>
            <option>Internship (law student)</option>
            <option>Junior associate</option>
            <option>Other</option>
          </select>
          <span class="error" id="position-error" aria-live="polite"></span>
        </div>
        {field('cv', 'CV', 'file', extra='accept=".pdf,.doc,.docx"', hint='PDF or Word, up to 5 MB.')}
        {field('message', 'Message', 'textarea', required=False)}
        <button class="btn btn-navy" type="submit" data-label="Send application">Send application</button>
        <p class="form-status" role="status" tabindex="-1"></p>
      </form>
    </div>
  </div>
</section>
"""
    return page("careers.html", "Careers & Internships", "Internships and junior associate opportunities at Signature Legal, Bengaluru. Apply online or email contact@signaturelegal.in.", "careers", body)

def build_contact():
    r = ""
    adv = "".join(f'<li><a href="mailto:{p["email"]}">{esc(p["name"])}</a> <span class="muted small">{p["email"]}</span></li>' for p in LEADS)
    map_src = "https://www.google.com/maps?q=" + MAP_QUERY.replace(" ", "+").replace(",", "%2C") + "&output=embed"
    dir_href = "https://www.google.com/maps/dir/?api=1&destination=" + MAP_QUERY.replace(" ", "+").replace(",", "%2C")
    body = f"""
{page_head('Contact Us', 'Write to us, call, or visit our office in Koramangala.', [], r)}
<section class="section">
  <div class="container split">
    <div class="reveal">
      <h2>Office</h2>
      <ul class="contact-list">
        <li>{icon(ICONS['pin'])}<div><strong>Address</strong><address style="font-style:normal">{esc(FIRM['street'])},<br>{FIRM['city']} – {FIRM['pin']}, {FIRM['state']}, {FIRM['country']}</address></div></li>
        <li>{icon(ICONS['phone'])}<div><strong>Phone</strong><a href="{FIRM['tel']}">{FIRM['phone']}</a></div></li>
        <li>{icon(ICONS['mail'])}<div><strong>Email</strong><a href="mailto:{FIRM['email']}">{FIRM['email']}</a></div></li>
        <li>{icon(ICONS['clock'])}<div><strong>Working hours</strong>{FIRM['hours']}</div></li>
      </ul>
      <h3>Advocates</h3>
      <ul class="contact-list" style="list-style:none">{adv.replace('<li>', '<li style="display:block">')}</ul>
    </div>
    <div class="reveal">
      <h2>Send an enquiry</h2>
      <form class="form" novalidate data-validate data-endpoint="{FORM_ENDPOINT}" data-subject="Website enquiry" data-success="Thank you. Your enquiry has been sent. We will respond during working hours.">
        <input type="hidden" name="_subject" value="Website enquiry – Signature Legal">
        <div class="visually-hidden" aria-hidden="true"><label for="e-gotcha">Leave this empty</label><input id="e-gotcha" name="_gotcha" tabindex="-1" autocomplete="off"></div>
        <div class="form-row">
          {field('name', 'Full name', autocomplete='name')}
          {field('email', 'Email', 'email', autocomplete='email')}
        </div>
        <div class="form-row">
          {field('phone', 'Phone', 'tel', autocomplete='tel')}
          {field('subject', 'Subject')}
        </div>
        {field('message', 'Message', 'textarea', extra='minlength="10"', hint='Briefly describe your matter. Please do not include confidential details.')}
        <div class="field">
          <label class="check"><input id="consent-check" name="consent" type="checkbox" required aria-describedby="consent-check-error">
          <span>I agree that Signature Legal may use these details to respond to my enquiry, as described in the <a href="privacy.html">Privacy Policy</a>. <span class="req" aria-hidden="true">*</span></span></label>
          <span class="error" id="consent-check-error" aria-live="polite"></span>
        </div>
        <button class="btn btn-navy" type="submit" data-label="Send enquiry">Send enquiry</button>
        <p class="form-status" role="status" tabindex="-1"></p>
        <p class="small muted">Submitting this form does not create an advocate-client relationship.</p>
      </form>
    </div>
  </div>
</section>
<section class="section section--alt">
  <div class="container">
    <h2 class="reveal">Find us</h2>
    <div class="map-wrap reveal">
      <iframe src="{map_src}" title="Map showing Signature Legal, Koramangala 5th Block, Bengaluru" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
    </div>
    <p class="map-actions"><a class="btn btn-line" href="{dir_href}" target="_blank" rel="noopener">Get directions<span class="visually-hidden"> (opens Google Maps in a new tab)</span></a></p>
  </div>
</section>
"""
    return page("contact.html", "Contact Us", f"Contact Signature Legal, Koramangala 5th Block, Bengaluru 560038. Phone {FIRM['phone']}, email {FIRM['email']}. Open {FIRM['hours']}.", "contact", body, ld=True)

def legal_page(path, title, intro, html_body, desc):
    r = ""
    body = f"""
{page_head(title, intro, [], r)}
<section class="section">
  <div class="container"><div class="prose">{html_body}
  <p class="muted small" style="margin-top:40px">Last updated: [DATE]. This is general boilerplate; have it reviewed before publishing.</p></div></div>
</section>
"""
    return page(path, title, desc, "", body)

DISCLAIMER = f"""
<p>Under the rules of the Bar Council of India, advocates and law firms are not permitted to solicit work or advertise. This website is meant only to provide information about Signature Legal, its practice areas and its advocates to persons who seek it.</p>
<h2>No solicitation</h2>
<p>By accessing this website, you confirm that you are seeking information about Signature Legal of your own accord and that there has been no advertisement, solicitation, invitation or inducement of any kind by the firm or its members.</p>
<h2>No legal advice</h2>
<p>The content of this website, including articles in the Insights section, is for general information only. It is not legal advice or a legal opinion and should not be relied on as such. You should obtain independent legal advice on your specific facts.</p>
<h2>No advocate-client relationship</h2>
<p>Using this website, sending an email, or submitting a form does not create an advocate-client relationship. Such a relationship arises only on formal engagement by the firm. Please do not send confidential information until you have been asked to.</p>
<h2>No liability</h2>
<p>Signature Legal is not liable for any consequence of any action taken by a user in reliance on material on this website. While we try to keep information accurate, the law changes and content may be out of date.</p>
<h2>External links</h2>
<p>Links to third-party websites are provided for convenience. Signature Legal does not endorse, and is not responsible for, the content of those websites.</p>
"""

PRIVACY = f"""
<p>Signature Legal respects your privacy. This policy explains what personal data we collect through this website and how we handle it, in keeping with the Digital Personal Data Protection Act, 2023.</p>
<h2>What we collect</h2>
<ul>
<li>Details you enter in our enquiry or careers forms: name, email, phone number, subject, message, college or enrolment details, and any CV you upload.</li>
<li>Basic technical information that web servers record automatically, such as browser type and IP address.</li>
</ul>
<p>The website stores a single item in your browser’s session storage to remember that you accepted the disclaimer. It is deleted when you close the browser tab. We do not use advertising or tracking cookies. [Update this if you add analytics.]</p>
<h2>Why we use it</h2>
<p>We use your data only to respond to your enquiry, to consider your job or internship application, and to keep necessary records. We rely on your consent, which you give when you submit a form.</p>
<h2>Sharing</h2>
<p>We do not sell your personal data. We share it only with service providers who help us run this website and receive form submissions [name the form service, e.g. Formspree], or where required by law. Embedded Google Maps and Google Fonts are provided by Google and are subject to Google’s privacy policy.</p>
<h2>How long we keep it</h2>
<p>We keep enquiry data for as long as needed to respond and for reasonable record-keeping, and application data for up to [12 months], after which it is deleted.</p>
<h2>Your rights</h2>
<p>You may ask to access, correct or erase your personal data, withdraw your consent, or raise a grievance, by writing to our grievance contact: [NAME], at <a href="mailto:{FIRM['email']}">{FIRM['email']}</a>. If you are not satisfied with our response, you may approach the Data Protection Board of India.</p>
<h2>Children</h2>
<p>This website is not directed at children. If you are under 18, please do not submit personal data without the involvement of a parent or guardian.</p>
<h2>Changes</h2>
<p>We may update this policy. The date at the bottom of this page shows when it was last changed.</p>
"""

TERMS = f"""
<p>By using this website you agree to these terms. If you do not agree, please do not use the website.</p>
<h2>Purpose of the website</h2>
<p>This website provides information about Signature Legal in accordance with the rules of the Bar Council of India. It is not an advertisement or solicitation. Please read our <a href="disclaimer.html">Disclaimer</a>.</p>
<h2>No legal advice</h2>
<p>Nothing on this website is legal advice. Using the website does not create an advocate-client relationship.</p>
<h2>Intellectual property</h2>
<p>The text, design and logo on this website belong to Signature Legal unless stated otherwise. You may view and print pages for personal, non-commercial use, but you may not copy or republish content without our written permission.</p>
<h2>Acceptable use</h2>
<p>You agree not to misuse the website, including by attempting to gain unauthorised access, introducing malicious code, or submitting false or unlawful information through its forms.</p>
<h2>Third-party links and services</h2>
<p>We are not responsible for websites or services operated by others, including embedded maps.</p>
<h2>Limitation of liability</h2>
<p>To the extent permitted by law, Signature Legal is not liable for any loss arising from use of, or reliance on, this website or its content.</p>
<h2>Governing law</h2>
<p>These terms are governed by the laws of India. Courts at Bengaluru, Karnataka have exclusive jurisdiction over any dispute arising from them.</p>
<h2>Changes</h2>
<p>We may revise these terms at any time by updating this page.</p>
"""

def build_404():
    body = """
<section class="section notfound">
  <div class="container narrow">
    <h1>Page not found</h1>
    <p class="lede">The page you’re looking for may have moved. Try the home page, or contact us if you need help.</p>
    <p><a class="btn btn-navy" href="/index.html">Go to the home page</a></p>
  </div>
</section>
"""
    # 404 is served from the site root on GitHub Pages; links are root-relative.
    return page("404.html", "Page not found", "Page not found.", "", body).replace('href="assets/', 'href="/assets/').replace('src="assets/', 'src="/assets/').replace('href="index.html"', 'href="/index.html"')

# --------------------------------------------------------------------------
# Placeholder images (SVG) — replace with licensed photos later
# --------------------------------------------------------------------------
def svg_wrap(w, h, inner, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<rect width="{w}" height="{h}" fill="#E7E1D6"/>{inner}'
            f'<text x="{w/2}" y="{h-36}" text-anchor="middle" font-family="Arial, sans-serif" font-size="22" fill="#5B5F66">{label}</text></svg>')

def placeholders():
    s = "#0B1F3A"; b = "#B08D57"
    court = "".join(f'<rect x="{180+i*90}" y="380" width="34" height="380" fill="none" stroke="{s}" stroke-width="3"/>' for i in range(5))
    court = (f'<path d="M140 380 400 230 660 380z" fill="none" stroke="{s}" stroke-width="3"/>'
             f'<rect x="140" y="360" width="520" height="20" fill="none" stroke="{b}" stroke-width="3"/>' + court +
             f'<rect x="120" y="760" width="560" height="22" fill="none" stroke="{s}" stroke-width="3"/>'
             f'<rect x="100" y="782" width="600" height="22" fill="none" stroke="{s}" stroke-width="3"/>')
    books = "".join(f'<rect x="{150+i*58}" y="{230+(i%3)*24}" width="44" height="{300-(i%3)*24}" fill="none" stroke="{s if i%4 else b}" stroke-width="3"/>' for i in range(10))
    books += f'<line x1="110" y1="530" x2="790" y2="530" stroke="{s}" stroke-width="4"/>'
    arch = "".join(f'<line x1="{i*60}" y1="620" x2="{450+i*15}" y2="80" stroke="{s if i%3 else b}" stroke-width="2"/>' for i in range(16))
    portrait = (f'<circle cx="400" cy="400" r="120" fill="none" stroke="{s}" stroke-width="3"/>'
                f'<path d="M190 820c20-160 110-240 210-240s190 80 210 240" fill="none" stroke="{s}" stroke-width="3"/>')
    files = {
        "courthouse-placeholder.svg": svg_wrap(800, 1000, court, "[PLACEHOLDER] Courthouse – replace with licensed photo"),
        "books-placeholder.svg": svg_wrap(900, 700, books, "[PLACEHOLDER] Law books – replace with licensed photo"),
        "architecture-placeholder.svg": svg_wrap(900, 700, arch, "[PLACEHOLDER] Architecture – replace with licensed photo"),
        "portrait-placeholder.svg": svg_wrap(800, 1000, portrait, "[PHOTO] Replace with portrait"),
    }
    os.makedirs(os.path.join(ROOT, "assets", "img"), exist_ok=True)
    for name, svg in files.items():
        with open(os.path.join(ROOT, "assets", "img", name), "w", encoding="utf-8") as f:
            f.write(svg)

# --------------------------------------------------------------------------
def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)

def sitemap(paths):
    urls = "".join(f"<url><loc>{BASE_URL}/{'' if p == 'index.html' else p}</loc></url>" for p in paths if p != "404.html")
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n'

def main():
    placeholders()
    pages = {
        "index.html": build_home(),
        "about.html": build_about(),
        "practice-areas.html": build_practice_index(),
        "team.html": build_team(),
        "insights.html": build_insights(),
        "careers.html": build_careers(),
        "contact.html": build_contact(),
        "disclaimer.html": legal_page("disclaimer.html", "Disclaimer", "Please read this before using the website.", DISCLAIMER, "Disclaimer for the Signature Legal website, in line with the rules of the Bar Council of India."),
        "privacy.html": legal_page("privacy.html", "Privacy Policy", "How we handle personal data submitted through this website.", PRIVACY, "Privacy policy of Signature Legal, Bengaluru, in line with the Digital Personal Data Protection Act, 2023."),
        "terms.html": legal_page("terms.html", "Terms of Use", "The terms that apply when you use this website.", TERMS, "Terms of use for the Signature Legal website."),
        "404.html": build_404(),
    }
    for p in PRACTICES:
        pages[f"practice-areas/{p['slug']}.html"] = build_practice(p)
    for a in ARTICLES:
        pages[f"insights/{a['slug']}.html"] = build_article(a)
    for path, html in pages.items():
        write(path, html)
    write("sitemap.xml", sitemap(pages.keys()))
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n")
    print(f"Built {len(pages)} pages.")

if __name__ == "__main__":
    main()
