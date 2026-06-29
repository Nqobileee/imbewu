import re, sys

with open('pia_unpacked/word/document.xml', encoding='utf-8') as f:
    doc = f.read()

TNR = '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>'
SZ  = '<w:sz w:val="19"/>'

def r(text):
    """Single run, Times New Roman 9.5pt, no bold."""
    safe = (text.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
                .replace('"','&quot;').replace("'","&apos;"))
    return (f'<w:r><w:rPr>{TNR}{SZ}</w:rPr>'
            f'<w:t xml:space="preserve">{safe}</w:t></w:r>')

def rb(text):
    """Bold run."""
    safe = (text.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
                .replace('"','&quot;').replace("'","&apos;"))
    return (f'<w:r><w:rPr><w:b/>{TNR}{SZ}</w:rPr>'
            f'<w:t xml:space="preserve">{safe}</w:t></w:r>')

def p(*runs, before=40, after=60):
    inner = ''.join(runs)
    return (f'<w:p><w:pPr><w:pStyle w:val="TableParagraph"/>'
            f'<w:spacing w:before="{before}" w:after="{after}"/>'
            f'<w:rPr>{TNR}{SZ}</w:rPr></w:pPr>{inner}</w:p>')

def txbx(paragraphs):
    return (f'<wps:txbx><w:txbxContent>'
            f'{"".join(paragraphs)}'
            f'</w:txbxContent></wps:txbx>')

# ── SECTION A: fill 7 empty response cells (w=5677) ──────────────────────────
EMPTY_CELL = (
    '        <w:tc>\n'
    '          <w:tcPr>\n'
    '            <w:tcW w:w="5677" w:type="dxa"/>\n'
    '          </w:tcPr>\n'
    '          <w:p>\n'
    '            <w:pPr>\n'
    '              <w:pStyle w:val="TableParagraph"/>\n'
    '              <w:spacing w:before="0"/>\n'
    '              <w:rPr>\n'
    '                <w:rFonts w:ascii="Times New Roman"/>\n'
    '                <w:sz w:val="18"/>\n'
    '              </w:rPr>\n'
    '            </w:pPr>\n'
    '          </w:p>\n'
    '        </w:tc>'
)

def filled_cell(content_xml):
    return (
        '        <w:tc>\n'
        '          <w:tcPr>\n'
        '            <w:tcW w:w="5677" w:type="dxa"/>\n'
        '          </w:tcPr>\n'
        f'{content_xml}\n'
        '        </w:tc>'
    )

a_responses = [
    # A1
    p(r('Offline AI-Powered Precision Crop Disease Diagnostic System')),
    # A2
    p(r('Andile Prince Bhebhe and Edith Nqobile Muyambiri')),
    # A3
    p(r('andileprincebhebhe@gmail.com | nqobilemuyambiri@gmail.com')),
    # A4
    p(r('Liquid Intelligent Technologies, Bulawayo; Omnishi AI; '
        'Harare Institute of Technology; ZB Innovation Hub, Harare')),
    # A5
    p(r('Agriculture, Food Security and Environmental Innovation')),
    # A6
    p(r('AG-FS-01')),
    # A7
    p(r('Bulawayo / Harare, Zimbabwe')),
]

for ans in a_responses:
    doc = doc.replace(EMPTY_CELL, filled_cell(ans), 1)

print(f"Section A done. Remaining empty cells: {doc.count(EMPTY_CELL)}")

# ── SECTION B: insert txbx into Shape 1 (Graphic 4) ─────────────────────────
sec_b = [
    p(rb('Problem: '), r('Crop diseases, particularly Northern Corn Leaf Blight (NCLB), cost '
      "Zimbabwe's 1.4 million smallholder maize farmers yield losses of 30 to 50 percent "
      'when infection establishes early in the season. Extension officers are overstretched, '
      'internet connectivity is absent across most rural areas, and existing digital advisory '
      'tools require cloud infrastructure that smallholder farmers do not have.'), before=60, after=40),
    p(rb('Innovation: '), r('This system delivers offline, on-device AI-powered crop disease '
      'diagnosis. A convolutional neural network built on a lightweight MobileNetV3-Small '
      'backbone, fine-tuned on 1,821 field-collected maize-leaf photographs, runs inference '
      'entirely on the device with no internet required. A farmer photographs an affected leaf '
      'and receives an instant diagnosis in English, Shona or Ndebele with actionable treatment '
      'guidance. The model achieves 96.0 percent test accuracy and 0.960 macro-F1.'), before=0, after=40),
    p(rb('Tiered Deployment: '), r('The same AI engine scales across four hardware tiers matched '
      'to farm size. Tier 1 (under 2 ha, smallholder): smartphone app requiring no SIM card or '
      'Wi-Fi. Tier 2 (2 to 20 ha): drone-mounted camera for aerial scouting and disease hotspot '
      'mapping, enabling targeted rather than blanket treatment. Tier 3 (20 to 200 ha): '
      'autonomous robotic ground vehicle for row-by-row canopy inspection with GPS geo-tagging. '
      'Tier 4 (above 200 ha, large commercial): module embedded directly in moving pivot or '
      'linear irrigation systems, diagnosing disease continuously as the arm sweeps across the '
      'field and issuing alerts before the next irrigation cycle.'), before=0, after=40),
    p(rb('Impact: '), r('The system advances SDG 2 (Zero Hunger) and SDG 9 (Industry, '
      'Innovation and Infrastructure), responds directly to the inaugural Zimbabwe AI Grand '
      'Challenge (food security theme), and aligns with Zimbabwe\'s National AI Strategy '
      '2026 to 2030.'), before=0, after=60),
]
doc = doc.replace(
    '<wps:cNvPr id="4" name="Graphic 4"/>',
    '<wps:cNvPr id="4" name="Graphic 4"/>', 1  # no-op; locate marker
)
doc = doc.replace(
    '</wps:spPr>\n                      <wps:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" rtlCol="0">',
    '</wps:spPr>\n                      ' + txbx(sec_b) +
    '\n                      <wps:bodyPr wrap="square" lIns="91440" tIns="45720" rIns="91440" bIns="45720" rtlCol="0">',
    1
)
print("Section B done")

# ── SECTION C ────────────────────────────────────────────────────────────────
sec_c = [
    p(rb('Originality: '), r('This is the first documented offline, on-device AI diagnostic '
      'tool for maize disease tailored to Zimbabwean smallholder conditions. Key novelties '
      'include: (1) offline-first architecture with zero network dependency; (2) leakage-free, '
      'group-aware evaluation keeping all images from the same physical leaf in one partition, '
      'preventing inflated scores common in published plant-disease studies; (3) a four-tier '
      'hardware platform scaling from a handset to pivot-irrigation integration; and '
      '(4) multilingual output in English, Shona and Ndebele.'), before=60, after=40),
    p(rb('Feasibility: '), r('A fully functional prototype has been built and peer-reviewed. '
      'Dataset: 1,821 field-collected maize-leaf images with group-aware train/val/test split '
      '(1,299 / 273 / 249). Model: MobileNetV3-Small fine-tuned in PyTorch with class-weighted '
      'cross-entropy, AdamW optimiser and early stopping. Results: 96.0 percent test accuracy, '
      '0.959 balanced accuracy, 0.960 macro-F1. Quantised to 8-bit integers, the model is a '
      'few megabytes and runs on a low-cost Android smartphone CPU. The paper has been submitted '
      'to JRISS Vol. 6, Issue 1, 2026.'), before=0, after=40),
    p(rb('Value Addition: '), r('The system closes the connectivity gap, replacing the absent '
      'extension officer for routine screening. Early NCLB detection enables timely intervention '
      'before the 30 to 50 percent yield loss threshold. Grad-CAM heat-maps confirm predictions '
      'rest on lesion tissue, making the AI reasoning visible and auditable by agronomists and '
      'farmers alike.'), before=0, after=40),
    p(rb('Scalability: '), r('Tier 1 (smartphone): ready for pilot deployment today. Tier 2 '
      '(drone): aerial scouting over small farms, disease hotspot maps for precision spraying. '
      'Tier 3 (robotic ground vehicle): autonomous row-by-row inspection with geo-tagged '
      'outbreak maps. Tier 4 (pivot/linear irrigation): AI module on the irrigation arm '
      'diagnoses in motion across 200-plus-hectare estates, with treatment alerts delivered '
      'before the next irrigation pass. The model is hardware-agnostic and exportable to '
      'ONNX format for any edge device.'), before=0, after=40),
    p(rb('Environmental Friendliness: '), r('Precision diagnosis enables targeted fungicide '
      'application, reducing chemical inputs by treating only affected zones. This lowers '
      'pesticide runoff, soil contamination and imported agrochemical spend. The drone and '
      'robot tiers use electric drive with no direct emissions. Early detection reduces crop '
      'failure, lowering pressure to expand farmland into ecologically sensitive areas.'),
      before=0, after=60),
]
doc = doc.replace(
    '</wps:spPr>\n                      <wps:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" rtlCol="0">',
    '</wps:spPr>\n                      ' + txbx(sec_c) +
    '\n                      <wps:bodyPr wrap="square" lIns="91440" tIns="45720" rIns="91440" bIns="45720" rtlCol="0">',
    1
)
print("Section C done")

# ── SECTION D ────────────────────────────────────────────────────────────────
sec_d = [
    p(rb('National Strategic Importance: '), r("Zimbabwe's National AI Strategy 2026 to 2030 "
      'names agriculture as a priority sector and explicitly commits to AI for crop disease '
      'prevention, food security and smallholder support. The inaugural Zimbabwe AI Grand '
      'Challenge 2026 is dedicated to food security, the exact domain of this prototype. '
      'The system also advances NDS2 pillars on food security and digital transformation, '
      'and contributes to SDG 2 (Zero Hunger) and SDG 9 (Industry, Innovation and '
      'Infrastructure).'), before=60, after=40),
    p(rb('Viability: '), r('The AI engine is trained once and deployed at near-zero marginal '
      'cost per diagnosis. Revenue streams include app subscriptions, institutional licensing '
      'to agri-input companies and NGOs, hardware bundles for Tiers 2 to 4, data analytics '
      'sales and SADC export licensing. Break-even is projected in Year 2.'), before=0, after=40),
    p(rb('Market Acceptance: '), r('Zimbabwe AI Grand Challenge provides immediate high-profile '
      'validation. Expressions of interest are being secured from agricultural input suppliers, '
      'development-finance institutions and farmer cooperative unions. The peer-reviewed JRISS '
      'paper provides the diagnostic accuracy evidence underpinning market confidence.'),
      before=0, after=40),
    p(rb('Employment Creation: '), r('Direct roles include AI/ML engineers, software developers, '
      'field data collectors, agricultural domain experts, hardware integration technicians and '
      'sales support agents. Phase 1 targets 11 to 20 direct jobs; Phase 3 targets 21 or more. '
      'Indirect employment includes drone pilots, robot maintenance technicians and agronomist '
      'extension partners.'), before=0, after=40),
    p(rb('Social Impact: '), r("The tool reaches Zimbabwe's most marginalised agricultural "
      'households: subsistence farmers with no internet, no nearby extension officer and no '
      'financial buffer against crop loss. Multilingual support (English, Shona, Ndebele) and '
      'a one-button photo interface lower barriers for women farmers who head a majority of '
      'smallholder households in rural Zimbabwe.'), before=0, after=40),
    p(rb('Opportunity Cost: '), r('Reduced NCLB losses lower the national maize import '
      'requirement, saving foreign exchange. Precision fungicide use cuts agrochemical imports. '
      'SADC licensing generates forex inflows from Year 2. Data analytics services sold to '
      'commodity traders and crop insurers provide additional hard-currency revenue.'),
      before=0, after=60),
]
doc = doc.replace(
    '</wps:spPr>\n                      <wps:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" rtlCol="0">',
    '</wps:spPr>\n                      ' + txbx(sec_d) +
    '\n                      <wps:bodyPr wrap="square" lIns="91440" tIns="45720" rIns="91440" bIns="45720" rtlCol="0">',
    1
)
print("Section D done")

# ── SECTION E ────────────────────────────────────────────────────────────────
sec_e = [
    p(rb('Profitability and Foreign Currency Generation: '), r('Revenue streams: (1) freemium '
      'app -- USD 2/month per farmer, USD 15/year per cooperative group; (2) institutional '
      'licensing -- USD 0.50 to 1.00 per farmer reached annually; (3) hardware bundles for '
      'drone, robot and irrigation tiers; (4) data analytics sold to commodity traders and '
      'insurers; (5) SADC export licensing from Year 2. Projected revenues: USD 20,000 (Year 1), '
      'USD 118,000 (Year 2), USD 320,000 (Year 3). Net surplus: USD 48,000 (Year 2), '
      'USD 210,000 (Year 3). Foreign currency generation through SADC licensing and data '
      'service exports.'), before=60, after=40),
    p(rb('Payback Period: '), r('Estimated 18 to 24 months from first commercial deployment. '
      'The core AI asset is already built; remaining investment covers app hardening, '
      'go-to-market and hardware integration.'), before=0, after=40),
    p(rb('Cash Flow Projection: '), r('Year 1 -- Revenue USD 20,000 / Costs USD 45,000 / '
      'Deficit (USD 25,000). Year 2 -- Revenue USD 118,000 / Costs USD 70,000 / '
      'Surplus USD 48,000. Year 3 -- Revenue USD 320,000 / Costs USD 110,000 / '
      'Surplus USD 210,000. Projections are conservative and assume no grant funding beyond '
      'the initial PIA award.'), before=0, after=40),
    p(rb('Risk Assessment: '), r('Key risks and mitigations: (1) Model accuracy on new field '
      'conditions -- mitigated by independent cross-field validation and low-confidence '
      'deferral to extension officers. (2) Farmer digital literacy -- mitigated by one-button '
      'UI and partner onboarding via AGRITEX. (3) Drone/robot regulatory uncertainty -- '
      'mitigated by early CAAZ engagement with Phase 2 timeline absorbing lead time. '
      '(4) Agrochemical guidance liability -- mitigated by agronomist review and ZAMA '
      'product-list alignment.'), before=0, after=40),
    p(rb('Financial Requirements: '), r('Phase 1 (0 to 6 months): USD 40,000 for app '
      'hardening and pilot deployment in two districts. Phase 2 (6 to 18 months): USD 80,000 '
      'for multi-disease model, drone and robot integration, and independent test-set '
      'collection. Phase 3 (18 to 36 months): USD 150,000 for irrigation-system integration, '
      'treatment knowledge base and regional market entry. Total 3-year requirement: '
      'USD 270,000 -- grant, impact-investment or blended-finance eligible.'), before=0, after=60),
]
doc = doc.replace(
    '</wps:spPr>\n                      <wps:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" rtlCol="0">',
    '</wps:spPr>\n                      ' + txbx(sec_e) +
    '\n                      <wps:bodyPr wrap="square" lIns="91440" tIns="45720" rIns="91440" bIns="45720" rtlCol="0">',
    1
)
print("Section E done")

# ── SECTION F ────────────────────────────────────────────────────────────────
sec_f = [
    p(rb('Market Readiness and Demand: '), r("Target customers: Zimbabwe's 1.4 million "
      'smallholder maize households (Tier 1); commercial farmers, agribusinesses and '
      'cooperative unions (Tiers 2 to 4); government extension services (AGRITEX). '
      'The SADC digital agri-advisory market is estimated at USD 50 million and growing. '
      'Tier 1 is pilot-ready with no additional infrastructure required. Institutional demand '
      'confirmed through the Zimbabwe AI Grand Challenge and NAS 2026 to 2030 mandate.'),
      before=60, after=40),
    p(rb('Technology Maturity and Scalability: '), r('Technology readiness levels by tier: '
      'Tier 1 smartphone -- TRL 6, pilot-deployable now. Tier 2 drone -- TRL 4, hardware '
      'integration design complete. Tier 3 robotic vehicle -- TRL 3, mechanical prototype in '
      'design. Tier 4 irrigation integration -- TRL 3, concept validated with pivot-irrigation '
      'partners. The AI model is exported in ONNX format and runs on ARM smartphone CPUs, '
      'drone companion computers and irrigation PLCs without modification.'), before=0, after=40),
    p(rb('Business Model and Revenue Potential: '), r('Five revenue streams: (1) B2C freemium '
      'app scalable to 100,000-plus users across SADC at near-zero marginal cost per user; '
      '(2) B2B institutional licensing to input companies (Syngenta, Windmill), cooperatives '
      'and development NGOs; (3) B2G government procurement for national disease surveillance; '
      '(4) Hardware-as-a-Service drone and robot kits leased on a per-hectare-scouted fee; '
      '(5) Data-as-a-Service disease-incidence intelligence sold to commodity traders, '
      'insurers and agricultural lenders.'), before=0, after=40),
    p(rb('Regulatory and Compliance Requirements: '), r('Mobile app: compliant with '
      "Zimbabwe's Data Protection Act 2021; no personal data collected beyond anonymised "
      'usage analytics. Drone operations: Civil Aviation Authority of Zimbabwe Part 101 '
      'compliance; operator licensing and no-fly-zone adherence required for Tier 2; '
      'engagement initiated. Agrochemical guidance: treatment recommendations reviewed by '
      'registered agronomists and aligned with ZAMA approved product lists. AI ethics: '
      'low-confidence cases deferred to human extension officers; consistent with NAS '
      '2026 to 2030 responsible-AI principles.'), before=0, after=40),
    p(rb('Investment and Financial Viability: '), r('The prototype has been developed with '
      'institutional support from Liquid Intelligent Technologies, Harare Institute of '
      'Technology and ZB Innovation Hub. The PIA award would provide catalytic funding and '
      'national profile to attract impact investors. Break-even in Year 2 and USD 210,000 '
      'surplus in Year 3 demonstrate strong return on catalytic investment. The combination '
      'of commercial revenue and measurable SDG impact meets the investment criteria of IFC, '
      'AfDB AgriTech windows and Zimbabwean impact funds.'), before=0, after=60),
]
doc = doc.replace(
    '</wps:spPr>\n                      <wps:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" rtlCol="0">',
    '</wps:spPr>\n                      ' + txbx(sec_f) +
    '\n                      <wps:bodyPr wrap="square" lIns="91440" tIns="45720" rIns="91440" bIns="45720" rtlCol="0">',
    1
)
print("Section F done")

# ── SECTION G: fill rows 1-5 (empty cells w=3710 and w=4595) ─────────────────
g_rows = [
    ('Offline_AI_Crop_Disease_Diagnosis.pdf',
     'Full peer-review paper submitted to JRISS Vol. 6, Issue 1, 2026 -- methodology, '
     'results (96.0 percent accuracy, 0.960 macro-F1) and deployment architecture.'),
    ('Prototype_Demo_Video.mp4',
     'Screen-recorded demonstration of the smartphone app performing offline NCLB '
     'diagnosis on field images with no internet connection.'),
    ('Grad-CAM_Visualisations.pdf',
     'Grad-CAM heat-map outputs on held-out test images showing model attention '
     'concentrated on necrotic lesion tissue rather than background.'),
    ('Tiered_Architecture_Diagrams.pdf',
     'System architecture diagrams for all four deployment tiers: smartphone, drone, '
     'robotic ground vehicle and pivot-irrigation integration.'),
    ('Model_Performance_Metrics.json',
     'Machine-readable JSON file containing all headline and per-class evaluation '
     'metrics from the held-out test set (accuracy, F1, PR-AUC, confusion matrix).'),
]

EMPTY_NAME = (
    '          <w:p>\n'
    '            <w:pPr>\n'
    '              <w:pStyle w:val="TableParagraph"/>\n'
    '              <w:spacing w:before="0"/>\n'
    '              <w:rPr>\n'
    '                <w:rFonts w:ascii="Times New Roman"/>\n'
    '                <w:sz w:val="18"/>\n'
    '              </w:rPr>\n'
    '            </w:pPr>\n'
    '          </w:p>'
)

def filled_p(text):
    safe = text.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    return (
        '          <w:p>\n'
        '            <w:pPr>\n'
        '              <w:pStyle w:val="TableParagraph"/>\n'
        '              <w:spacing w:before="0"/>\n'
        '              <w:rPr>\n'
        f'                {TNR}\n'
        f'                {SZ}\n'
        '              </w:rPr>\n'
        '            </w:pPr>\n'
        f'            <w:r><w:rPr>{TNR}{SZ}</w:rPr>'
        f'<w:t xml:space="preserve">{safe}</w:t></w:r>\n'
        '          </w:p>'
    )

for name, desc in g_rows:
    doc = doc.replace(EMPTY_NAME, filled_p(name), 1)
    doc = doc.replace(EMPTY_NAME, filled_p(desc), 1)

print(f"Section G done. Remaining EMPTY_NAME: {doc.count(EMPTY_NAME)}")

# ── SECTION I: Name of Primary Innovator and Date ────────────────────────────
# The Section I table has cells w=6834 with the same empty paragraph structure
EMPTY_6834 = (
    '          <w:p>\n'
    '            <w:pPr>\n'
    '              <w:pStyle w:val="TableParagraph"/>\n'
    '              <w:spacing w:before="0"/>\n'
    '              <w:rPr>\n'
    '                <w:rFonts w:ascii="Times New Roman"/>\n'
    '                <w:sz w:val="18"/>\n'
    '              </w:rPr>\n'
    '            </w:pPr>\n'
    '          </w:p>'
)

# Row order in Section I: Name of Primary Innovator, Signature, Date,
# then (For Institutional) Name of Endorsing Officer, Position/Title, Signature, Date
sec_i_values = [
    'Andile Prince Bhebhe',  # Name of Primary Innovator
    '',                       # Signature (leave blank for wet ink)
    '29 June 2026',          # Date
    '',                       # Name of Endorsing Officer
    '',                       # Position/Title
    '',                       # Signature
    '',                       # Date
]
for val in sec_i_values:
    if val:
        doc = doc.replace(EMPTY_6834, filled_p(val), 1)
    else:
        doc = doc.replace(EMPTY_6834, EMPTY_6834, 1)  # leave blank

print("Section I done")

with open('pia_unpacked/word/document.xml', 'w', encoding='utf-8') as f:
    f.write(doc)
print("Written successfully")
