#!/usr/bin/env python3
"""Build the 25 supplied RCC-BGM pages from the Santa Clara location template."""

from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "santa-clara-ca.html"

# Context is intentionally qualitative. It is based on official municipal economic-
# development, planning/building and permit resources and avoids fragile statistics.
MARKETS = [
 ("san-jose-ca","San Jose","CA","Silicon Valley / Santa Clara County","Reliable + Brilliant",
  "Downtown, North San Jose and the city's industrial corridors include office, technology, advanced-manufacturing, retail and service properties.",
  "Technology & Advanced Manufacturing|Downtown Offices & Mixed Use|Industrial & Logistics|Healthcare & Research",
  "San José's Development Services Permit Center routes commercial and industrial work through the applicable planning, building, fire and public-works reviews."),
 ("santa-clara-ca","Santa Clara","CA","Silicon Valley / Santa Clara County","Reliable + Brilliant",
  "Santa Clara combines technology campuses, semiconductor and R&D space, data-center properties, offices and visitor-serving commercial facilities.",
  "Semiconductor & Hardware|Technology Campuses|Data Centers|R&D Facilities",
  "The City of Santa Clara Permit Center coordinates Building, Planning, Fire and Public Works review; the required path depends on the proposed use and alterations."),
 ("sunnyvale-ca","Sunnyvale","CA","Silicon Valley / Santa Clara County","Reliable + Brilliant",
  "Sunnyvale's business environment spans technology offices, research space, industrial districts, neighborhood retail and an evolving downtown.",
  "Technology & Software|Aerospace & R&D|Industrial & Flex Space|Downtown Commerce",
  "Sunnyvale's One-Stop Permit Center coordinates Building, Fire, Planning and Public Works Engineering, and commercial work may require online plan review and inspections."),
 ("cupertino-ca","Cupertino","CA","Silicon Valley / Santa Clara County","Reliable + Brilliant",
  "Cupertino is shaped by large technology workplaces, professional offices, retail centers and commercial properties serving employees and residents.",
  "Technology Workplaces|Professional Offices|Retail Centers|R&D & Engineering",
  "Cupertino's Building Division reviews commercial tenant improvements and other construction; zoning, fire review and inspections may also apply to a particular scope."),
 ("los-gatos-ca","Los Gatos","CA","West Valley / Santa Clara County","Reliable + Brilliant",
  "Los Gatos has a distinctive downtown, medical and professional offices, neighborhood retail and commercial properties along major travel corridors.",
  "Professional Offices|Healthcare Practices|Downtown Retail|Hospitality & Dining",
  "Los Gatos Community Development administers planning and building review, so changes of use, signs and tenant alterations should be checked before work is scheduled."),
 ("fremont-ca","Fremont","CA","East Bay / Alameda County","Reliable + Brilliant",
  "Fremont's employment areas support advanced manufacturing, clean technology, life science, logistics, offices and a growing mixed-use core.",
  "Advanced Manufacturing|Clean Technology|Life Science|Logistics & Flex",
  "Fremont's Development Services Center brings planning, building, engineering and fire requirements into the project review process for commercial properties."),
 ("palo-alto-ca","Palo Alto","CA","Peninsula / Santa Clara County","Reliable + Brilliant",
  "Palo Alto includes research-oriented workplaces, professional offices, medical facilities, downtown storefronts and Stanford Research Park properties.",
  "Research & Innovation|Medical & Life Science|Professional Offices|Downtown Retail",
  "Palo Alto's Development Center handles planning and building applications; commercial alterations may also involve fire, accessibility and utility review."),
 ("menlo-park-ca","Menlo Park","CA","Peninsula / San Mateo County","Reliable + Brilliant",
  "Menlo Park's commercial landscape includes venture and professional offices, life-science space, technology campuses and neighborhood-serving business districts.",
  "Venture & Professional Services|Life Science|Technology Offices|Neighborhood Commerce",
  "Menlo Park's Building Division and Planning Division review commercial projects, with permit needs determined by use, construction scope and site conditions."),
 ("redwood-city-ca","Redwood City","CA","Peninsula / San Mateo County","Reliable + Brilliant",
  "Redwood City combines a busy downtown with technology offices, life-science properties, healthcare facilities and industrial or waterfront employment areas.",
  "Downtown Offices|Life Science & Research|Healthcare|Industrial & Waterfront",
  "Redwood City's online permit services support building and planning submittals; tenant work can also require fire and public-works coordination."),
 ("san-mateo-ca","San Mateo","CA","Peninsula / San Mateo County","Reliable + Brilliant",
  "San Mateo supports downtown and Class A offices, retail centers, healthcare properties and mixed-use commercial buildings near regional transportation.",
  "Corporate Offices|Downtown & Mixed Use|Healthcare Properties|Retail & Services",
  "San Mateo's Building Division reviews permits and inspections, while planning approval or fire review may be required based on use and project details."),
 ("san-francisco-ca","San Francisco","CA","San Francisco / Northern California","Reliable + Brilliant",
  "San Francisco's dense commercial fabric includes high-rise offices, neighborhood business districts, healthcare campuses, hospitality properties and Mission Bay research space.",
  "High-Rise Offices|Life Science & Mission Bay|Healthcare|Hospitality & Retail",
  "San Francisco's Department of Building Inspection and Planning Department administer separate parts of development review; occupied-building logistics and permit sequencing should be assessed early."),
 ("pleasanton-ca","Pleasanton","CA","Tri-Valley / Alameda County","Reliable + Brilliant",
  "Pleasanton includes Hacienda-area offices, business parks, professional services, retail destinations and industrial or flex properties.",
  "Business Parks|Professional Services|Retail Destinations|Industrial & Flex",
  "Pleasanton's Permit Center coordinates planning, building and engineering review, with fire requirements and inspections tied to the particular business use and alterations."),
 ("walnut-creek-ca","Walnut Creek","CA","Contra Costa County / East Bay","Reliable + Brilliant",
  "Walnut Creek is a regional center for offices, healthcare, retail, restaurants and mixed-use properties around downtown and major transportation corridors.",
  "Regional Offices|Healthcare|Downtown Retail|Mixed-Use Properties",
  "Walnut Creek's Permit Center processes building and planning work; commercial scopes may require zoning confirmation, plan review, inspections and fire approval."),
 ("sacramento-ca","Sacramento","CA","Sacramento Region / Northern California","Reliable + Brilliant",
  "California's capital supports government-adjacent offices, healthcare systems, downtown properties, industrial districts and distribution facilities.",
  "Government-Adjacent Offices|Healthcare|Downtown Commerce|Industrial & Distribution",
  "Sacramento's Community Development Department manages building and planning review, and commercial work may require coordinated fire, utilities or public-works approvals."),
 ("los-angeles-ca","Los Angeles","CA","Los Angeles County / Southern California","Reliable + Brilliant",
  "Los Angeles contains highly varied commercial environments, from downtown offices and production space to healthcare, hospitality, retail and logistics properties.",
  "Media & Production|Downtown Offices|Healthcare|Logistics & Retail",
  "Los Angeles projects may involve the Department of Building and Safety, City Planning and the Fire Department; requirements vary substantially by address, occupancy and scope."),
 ("long-beach-ca","Long Beach","CA","Los Angeles County / Southern California","Reliable + Brilliant",
  "Long Beach combines port-related logistics, downtown offices, hospitality, healthcare, aerospace activity and neighborhood commercial corridors.",
  "Port & Logistics|Aerospace|Downtown Offices|Healthcare & Hospitality",
  "Long Beach Development Services reviews planning and building matters, while fire and port-related requirements may affect certain sites and operations."),
 ("pasadena-ca","Pasadena","CA","San Gabriel Valley / Los Angeles County","Reliable + Brilliant",
  "Pasadena's economy includes research institutions, healthcare, professional offices, hospitality and commercial properties in historic and mixed-use districts.",
  "Research & Education|Healthcare|Professional Offices|Hospitality & Retail",
  "Pasadena's Permit Center supports building and planning applications; historic resources, changes of use and fire review can influence a commercial project's path."),
 ("santa-monica-ca","Santa Monica","CA","Westside / Los Angeles County","Reliable + Brilliant",
  "Santa Monica has creative and technology offices, hospitality, healthcare, retail and dense mixed-use properties in a coastal urban setting.",
  "Creative & Technology|Hospitality|Healthcare|Retail & Mixed Use",
  "Santa Monica's permit services coordinate building and planning review, and coastal, transportation, fire or business-license requirements may apply to a specific property."),
 ("irvine-ca","Irvine","CA","Orange County / Southern California","Reliable + Brilliant",
  "Irvine's planned business districts include corporate campuses, life-science and medical space, technology offices, retail centers and industrial properties.",
  "Corporate Campuses|Life Science & Medical|Technology|Industrial & Retail",
  "Irvine's Community Development team reviews building and planning applications; commercial tenant work may also require fire review and inspection sequencing."),
 ("san-diego-ca","San Diego","CA","San Diego County / Southern California","Reliable + Brilliant",
  "San Diego's large commercial market spans life science, defense and technology, healthcare, tourism, offices and cross-border logistics.",
  "Life Science|Defense & Technology|Healthcare|Hospitality & Logistics",
  "San Diego's Development Services Department administers permits and inspections, with zoning, fire and other agency review depending on site, occupancy and work type."),
 ("phoenix-az","Phoenix","AZ","Maricopa County / Arizona","Brilliant",
  "Phoenix supports corporate offices, advanced manufacturing, healthcare, distribution, hospitality and rapidly developing commercial corridors.",
  "Advanced Manufacturing|Healthcare|Distribution & Logistics|Offices & Hospitality",
  "The City of Phoenix Planning and Development Department handles plan review, permits and inspections; use, fire, civil and building requirements depend on the site and scope."),
 ("las-vegas-nv","Las Vegas","NV","Clark County / Nevada","Brilliant",
  "Las Vegas has intensive hospitality and entertainment properties alongside offices, healthcare, retail, convention and service facilities.",
  "Hospitality & Gaming|Convention Facilities|Retail & Dining|Offices & Healthcare",
  "Within city limits, Las Vegas Building & Safety and Planning administer development review; properties elsewhere in the valley may fall under a different jurisdiction."),
 ("reno-nv","Reno","NV","Washoe County / Northern Nevada","Reliable + Brilliant",
  "Reno's commercial base includes logistics and data-oriented facilities, advanced manufacturing, offices, healthcare, hospitality and downtown properties.",
  "Logistics & Data Facilities|Advanced Manufacturing|Healthcare|Hospitality & Offices",
  "Reno's Development Services group coordinates building, planning and engineering review, while fire requirements and the responsible jurisdiction must be confirmed by address."),
 ("grand-rapids-mi","Grand Rapids","MI","Kent County / West Michigan","Brilliant",
  "Grand Rapids anchors a diverse West Michigan economy with healthcare, office, manufacturing, distribution, hospitality and downtown commercial properties.",
  "Healthcare|Manufacturing|Distribution|Downtown Offices & Hospitality",
  "The City of Grand Rapids Development Center coordinates permits and plan review; building, trade, fire and zoning requirements depend on the proposed work and occupancy."),
 ("kalamazoo-mi","Kalamazoo","MI","Kalamazoo County / West Michigan","Brilliant",
  "Kalamazoo supports healthcare and life-science activity, higher education, manufacturing, offices, retail and downtown mixed-use properties.",
  "Healthcare & Life Science|Higher Education|Manufacturing|Downtown Commerce",
  "Kalamazoo's Community Planning and Economic Development services address zoning and building permits; trade permits and inspections may be required for a commercial scope."),
]

NEARBY = {
 "san-jose-ca":["santa-clara-ca","sunnyvale-ca","fremont-ca"], "santa-clara-ca":["san-jose-ca","sunnyvale-ca","cupertino-ca"],
 "sunnyvale-ca":["santa-clara-ca","cupertino-ca","palo-alto-ca"], "cupertino-ca":["sunnyvale-ca","los-gatos-ca","san-jose-ca"],
 "los-gatos-ca":["san-jose-ca","cupertino-ca","santa-clara-ca"], "fremont-ca":["san-jose-ca","pleasanton-ca","palo-alto-ca"],
 "palo-alto-ca":["menlo-park-ca","redwood-city-ca","sunnyvale-ca"], "menlo-park-ca":["palo-alto-ca","redwood-city-ca","san-mateo-ca"],
 "redwood-city-ca":["menlo-park-ca","san-mateo-ca","palo-alto-ca"], "san-mateo-ca":["redwood-city-ca","san-francisco-ca","menlo-park-ca"],
 "san-francisco-ca":["san-mateo-ca","redwood-city-ca","walnut-creek-ca"], "pleasanton-ca":["fremont-ca","walnut-creek-ca","san-jose-ca"],
 "walnut-creek-ca":["pleasanton-ca","san-francisco-ca","sacramento-ca"], "sacramento-ca":["walnut-creek-ca","san-francisco-ca","pleasanton-ca"],
 "los-angeles-ca":["long-beach-ca","pasadena-ca","santa-monica-ca"], "long-beach-ca":["los-angeles-ca","irvine-ca","santa-monica-ca"],
 "pasadena-ca":["los-angeles-ca","santa-monica-ca","long-beach-ca"], "santa-monica-ca":["los-angeles-ca","pasadena-ca","long-beach-ca"],
 "irvine-ca":["long-beach-ca","los-angeles-ca","san-diego-ca"], "san-diego-ca":["irvine-ca","long-beach-ca","los-angeles-ca"],
 "phoenix-az":["las-vegas-nv","san-diego-ca","irvine-ca"], "las-vegas-nv":["reno-nv","phoenix-az","los-angeles-ca"],
 "reno-nv":["las-vegas-nv","sacramento-ca","san-francisco-ca"], "grand-rapids-mi":["kalamazoo-mi","reno-nv","phoenix-az"],
 "kalamazoo-mi":["grand-rapids-mi","reno-nv","phoenix-az"],
}

ICON = ["fa-microchip","fa-building","fa-industry","fa-briefcase"]
BY_SLUG = {m[0]: m for m in MARKETS}

def services(m):
    slug, city, state, region, coverage, context, industries, permit = m
    brilliant = (
      f"Commercial janitorial, floor care and specialty-cleaning needs for a {city} property may be assessed by Brilliant. "
      "Program type, frequency, access procedures and local availability must be confirmed for the specific property and scope."
    )
    if coverage == "Brilliant":
        reliable = (
          f"This official market is identified for Brilliant services. Construction, HVAC, MEP or tenant-improvement work in {city} "
          "must not be assumed available; ask RCC-BGM to confirm whether the requested scope can be supported."
        )
    else:
        reliable = (
          f"Commercial maintenance, tenant-improvement, HVAC or MEP needs in {city} may be assessed by Reliable. "
          "Applicable licensing, permits, trade availability and property-specific scope must be confirmed before work is proposed."
        )
    return brilliant, reliable

def main_html(m):
    slug, city, state, region, coverage, context, industry_text, permit = m
    industry_names = industry_text.split("|")
    brilliant, reliable = services(m)
    industry_cards = "".join(
      f'<div class="s-item scroll-reveal" style="cursor:default"><i class="fa-solid {ICON[i]}"></i>'
      f'<h3>{escape(name)}</h3><p>{escape(name)} properties may have different occupancy, access, finish, hygiene and operating-hour requirements; the facility and requested scope should be assessed before service is confirmed.</p></div>'
      for i, name in enumerate(industry_names)
    )
    nearby_cards = "".join(
      f'<a class="s-item scroll-reveal" href="{n}.html"><i class="fa-solid fa-location-dot"></i>'
      f'<h3>{escape(BY_SLUG[n][1])}, {BY_SLUG[n][2]}</h3><p>Review the separate market context and confirm service availability for a property in {escape(BY_SLUG[n][1])}.</p>'
      '<span class="s-link">View market <i class="fa-solid fa-arrow-right"></i></span></a>'
      for n in NEARBY[slug]
    )
    return f"""
    <main>
      <section class="container section-padding">
        <div style="max-width:850px">
          <span class="hero-tag">{escape(region)} Market</span>
          <h2>Commercial Property Context in {escape(city)}</h2>
          <p style="margin-top:16px">{escape(context)} RCC-BGM's official locations page includes {escape(city)} in its service network, but that listing does not establish that every service is available at every address. Any request must be matched to the property, division, requested work and current local availability.</p>
        </div>
        <div class="services-grid" style="margin-top:48px">
          <a class="s-item scroll-reveal active" href="commercial-cleaning-services.html"><i class="fa-solid fa-broom"></i><h3>Janitorial &amp; Specialty Cleaning Assessment</h3><p>{escape(brilliant)}</p><span class="s-link">Review cleaning services <i class="fa-solid fa-arrow-right"></i></span></a>
          <a class="s-item scroll-reveal" href="commercial-construction.html"><i class="fa-solid fa-helmet-safety"></i><h3>Construction &amp; Tenant-Improvement Review</h3><p>{escape(reliable)}</p><span class="s-link">Review construction services <i class="fa-solid fa-arrow-right"></i></span></a>
          <a class="s-item scroll-reveal" href="facility-maintenance-services.html"><i class="fa-solid fa-screwdriver-wrench"></i><h3>Property-Specific Maintenance</h3><p>Repair and upkeep needs may be assessed after the building type, affected systems, access limits and responsibility boundaries are known. Service is subject to local availability.</p><span class="s-link">Review maintenance services <i class="fa-solid fa-arrow-right"></i></span></a>
          <a class="s-item scroll-reveal" href="commercial-hvac-services.html"><i class="fa-solid fa-temperature-arrow-down"></i><h3>HVAC &amp; MEP Scope Confirmation</h3><p>HVAC or MEP work must be confirmed for the specific {escape(city)} property and scope, including jurisdiction, permits, licensing, system condition and trade availability.</p><span class="s-link">Review HVAC services <i class="fa-solid fa-arrow-right"></i></span></a>
        </div>
      </section>
      <section class="container section-padding" style="background:var(--bg-warm);border-top:1px solid var(--border-warm);border-bottom:1px solid var(--border-warm)">
        <h2>{escape(city)} Industries and Commercial Property Types</h2>
        <p class="section-intro">{escape(context)} These market characteristics help frame a site conversation; they are not claims that RCC-BGM serves every facility in these categories.</p>
        <div class="services-grid">{industry_cards}</div>
      </section>
      <section class="container section-padding">
        <h2>Permitting and Project Planning in {escape(city)}</h2>
        <p class="section-intro">{escape(permit)} Property owners and managers should confirm the authority having jurisdiction and required approvals directly with official agencies. RCC-BGM service availability does not replace permit, design, licensing or inspection requirements.</p>
        <div class="process-grid">
          <div class="step-card scroll-reveal"><h2>01</h2><h4>Identify the Property</h4><p>Share the exact {escape(city)} address, occupancy, facility type and operating constraints.</p></div>
          <div class="step-card scroll-reveal"><h2>02</h2><h4>Define the Need</h4><p>Separate recurring cleaning, repair, building-system and improvement needs into a reviewable scope.</p></div>
          <div class="step-card scroll-reveal"><h2>03</h2><h4>Confirm Coverage</h4><p>RCC-BGM confirms the applicable division and whether service is locally available for that property and scope.</p></div>
          <div class="step-card scroll-reveal"><h2>04</h2><h4>Check Requirements</h4><p>Confirm permits, licensing, access, schedule, exclusions and responsibilities before a proposal or work plan.</p></div>
        </div>
      </section>
      <section class="container section-padding" style="background:var(--bg-warm);border-top:1px solid var(--border-warm);border-bottom:1px solid var(--border-warm)">
        <h2>Service Questions for a {escape(city)} Property</h2>
        <div class="services-grid" style="margin-top:30px">
          <div class="s-item scroll-reveal"><h3>Facility conditions</h3><p>Building size, occupancy, surfaces, equipment, security and operating hours shape what may be appropriate.</p></div>
          <div class="s-item scroll-reveal"><h3>Division availability</h3><p>The official network identifies this as a {escape(coverage)} market. The specific service still must be confirmed.</p></div>
          <div class="s-item scroll-reveal"><h3>Jurisdiction and permits</h3><p>City, county, fire or other agency requirements may apply depending on the address and work.</p></div>
          <div class="s-item scroll-reveal"><h3>Proposal boundaries</h3><p>A useful proposal should identify included work, frequency or schedule, assumptions, responsibilities and exclusions.</p></div>
        </div>
      </section>
      <section class="container section-padding">
        <h2>Frequently Asked Questions About {escape(city)}</h2>
        <p class="section-intro">Answers are intentionally conditional because availability is confirmed property by property.</p>
        <details class="faq-item scroll-reveal" open><summary>Is {escape(city)} supported by RCC-BGM?</summary><p>Yes. RCC-BGM's original official locations page lists {escape(city)} in its multi-state service network and identifies the market as {escape(coverage)}. Service must still be confirmed for the specific property and scope.</p></details>
        <details class="faq-item scroll-reveal"><summary>Can I request commercial cleaning in {escape(city)}?</summary><p>A commercial cleaning or janitorial need may be assessed. Frequency, facility requirements, access and current local availability must be reviewed before service is confirmed.</p></details>
        <details class="faq-item scroll-reveal"><summary>Are construction and HVAC services automatically available here?</summary><p>No. Do not assume that every RCC-BGM service is offered in this market. Construction, HVAC, MEP and improvement work is subject to division coverage, licensing, trade availability and the particular property scope.</p></details>
        <details class="faq-item scroll-reveal"><summary>Who confirms permits for work in {escape(city)}?</summary><p>The property owner and project participants should verify requirements with the authority having jurisdiction. {escape(permit)}</p></details>
        <details class="faq-item scroll-reveal"><summary>What should I provide for an assessment?</summary><p>Provide the exact address, facility and occupancy type, requested work, preferred schedule, known site restrictions and any existing plans or permit information. RCC-BGM can then confirm the appropriate next step.</p></details>
      </section>
      <section id="contact" class="container section-padding" style="padding-bottom:100px">
        <div class="cta-box scroll-reveal"><h2>Confirm Service for Your {escape(city)} Property</h2>
          <p style="margin-top:16px;color:var(--text-body);max-width:680px;margin-left:auto;margin-right:auto">Tell RCC-BGM what the property is, where it is located and what outcome you need. The request may be assessed and routed only after the relevant division and local availability are confirmed for the specific scope.</p>
          <div style="margin-top:32px"><a href="contact.html" class="btn-header btn-glow">Request a Property Review <i class="fa-solid fa-arrow-right"></i></a></div>
        </div>
      </section>
      <section class="container section-padding" style="text-align:center;border-top:1px solid var(--border-warm)">
        <h2>Compare Nearby RCC-BGM Markets</h2><p style="margin:14px auto 0;max-width:680px;color:var(--text-body)">Each market has its own business, property and service-availability context. Use the location page for the property's actual address.</p>
        <div class="services-grid" style="margin-top:40px">{nearby_cards}</div>
      </section>
    </main>"""

def build(template, m):
    slug, city, state, region, coverage, context, industries, permit = m
    title = f"{city} Commercial Facility Service Assessment | RCC-BGM"
    meta = (f"Explore commercial property context in {city}, {state}, and request an RCC-BGM service assessment. "
            "Availability must be confirmed for the specific property and scope.")
    text = re.sub(r"<title>.*?</title>", f"<title>{escape(title)}</title>", template, count=1)
    text = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{escape(meta)}">', text, count=1)
    text = re.sub(r'<span class="hero-tag animate__animated animate__fadeInDown">.*?</span>',
                  f'<span class="hero-tag animate__animated animate__fadeInDown"><i class="fa-solid fa-location-dot"></i> {escape(region)}</span>', text, count=1)
    text = re.sub(r'<h1 class="animate__animated animate__fadeInUp">.*?</h1>',
                  f'<h1 class="animate__animated animate__fadeInUp">Commercial Facility Service Assessment in <span>{escape(city)}, {state}</span></h1>', text, count=1, flags=re.S)
    text = re.sub(r'(<h1 class="animate__animated animate__fadeInUp">.*?</h1>\s*<p class="animate__animated animate__fadeInUp"[^>]*>).*?(</p>)',
                  rf'\1RCC-BGM lists {escape(city)} as a {escape(coverage)} market. Cleaning, maintenance, construction and building-system needs are assessed separately and remain subject to local availability.\2', text, count=1, flags=re.S)
    text = re.sub(r'<div class="hv-chip loc">.*?</div>', f'<div class="hv-chip loc"><i class="fa-solid fa-location-dot"></i> {escape(city)}, {state}</div>', text, count=1)
    text = re.sub(r'<div class="hv-chip trust">.*?</div>', '<div class="hv-chip trust"><i class="fa-solid fa-circle-check"></i> Scope confirmation required</div>', text, count=1)
    text = re.sub(r"\s*<main>.*?</main>", "\n" + main_html(m), text, count=1, flags=re.S)
    text = text.replace("Commercial facility services for offices, technology campuses and controlled environments. Cleaning, construction, HVAC and maintenance â€” coordinated through one platform.",
                        "Commercial facility needs are reviewed by property, market, division and scope. Availability must be confirmed before service is represented or scheduled.")
    text = text.replace("Mon â€“ Fri: 7AM â€“ 6PM", "Hours: confirm when requesting service")
    return "\n".join(line.rstrip() for line in text.splitlines()) + "\n"

def main():
    template = TEMPLATE.read_text(encoding="utf-8")
    for market in MARKETS:
        (ROOT / f"{market[0]}.html").write_text(build(template, market), encoding="utf-8")
    print(f"Updated {len(MARKETS)} supplied location pages from {TEMPLATE.name}")

if __name__ == "__main__":
    main()
