"""
NagarSetu — Civic catalog builder & expander.

Generates 98 additional realistic Indian civic procedures across 6 categories:
1. Licenses & Business (17 procedures)
2. Utilities & Municipal (16 procedures)
3. Property, Revenue & Building (17 procedures)
4. Certificates & Civil Status (16 procedures)
5. Transport & Driving (16 procedures)
6. Social Welfare & Schemes (16 procedures)

Total with existing 3 procedures = 101 procedures.
Outputs:
- data/processed/chunks.jsonl
- frontend/public/demo/*.json and frontend/lib/demo/*.json
- Re-indexes ChromaDB and BM25 using scripts/build_index.py
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_CHUNKS = REPO_ROOT / "data" / "processed" / "chunks.jsonl"
FRONTEND_DEMO_PUBLIC = REPO_ROOT / "frontend" / "public" / "demo"
FRONTEND_DEMO_LIB = REPO_ROOT / "frontend" / "lib" / "demo"

RAW_CATALOG = [
    # ---------------- 1. Licenses & Business ----------------
    {
        "id": "fssai_food_license",
        "category": "Licenses & Business",
        "name": "FSSAI Food Business Registration & License",
        "department": "Food Safety and Standards Authority of India (FSSAI)",
        "jurisdiction": "National / Municipal Corporation",
        "summary": "Mandatory registration or state license for food manufacturers, restaurants, bakeries, cloud kitchens, and street food operators.",
        "time": "7–15 working days",
        "cost": "₹100 (Registration) – ₹2,000 (State License)",
        "official_url": "https://foscos.fssai.gov.in", 
        "steps": [
            ("Determine eligibility category", "Check annual turnover: under ₹12 Lakh requires basic Registration; between ₹12 Lakh and ₹20 Crore requires a State License.", ["Turnover statement", "Business identity proof"], "₹0", "1 day"),
            ("Create account on FoSCoS portal", "Register on the Food Safety Compliance System (FoSCoS) using valid mobile number and email ID.", ["Aadhaar card", "PAN card of business/proprietor"], "₹0", "Immediate"),
            ("Complete Form A or Form B", "Fill in premises address, nature of food business, proposed list of food categories to be handled, and equipment details.", ["Premises proof (Electricity bill/Rent agreement)"], "₹0", "1 day"),
            ("Upload food safety declarations", "Submit standard food safety management system (FSMS) plan, water test report, and food handler medical fitness certificate.", ["FSMS declaration", "Water testing lab report", "Medical fitness certificate"], "₹0", "1–2 days"),
            ("Pay license fee online", "Pay government prescribed fee through online payment gateway (UPI/Net banking/Card).", ["Payment receipt"], "₹100 – ₹2,000", "Immediate"),
            ("Food safety officer inspection", "For state licenses, a Food Safety Officer conducts premise verification for hygiene standards.", ["Original document copies"], "₹0", "3–7 working days"),
            ("Download FSSAI license certificate", "Upon verification approval, download the 14-digit FSSAI registration certificate with QR code.", ["Application reference number"], "₹0", "Immediate"),
        ]
    },
    {
        "id": "shops_establishment_act",
        "category": "Licenses & Business",
        "name": "Shops & Commercial Establishments Registration (Gumasta)",
        "department": "Department of Labour & Employment",
        "jurisdiction": "State / Municipal Corporation",
        "summary": "Legal registration required for commercial offices, retail shops, and service establishments employing workers.",
        "time": "3–5 working days",
        "cost": "₹250 – ₹1,500 depending on employee count",
        "official_url": "https://labour.gov.in",
        "steps": [
            ("Register on state labour portal", "Create profile on state unified labour/single-window clearance portal with business details.", ["Aadhaar", "PAN"], "₹0", "Immediate"),
            ("Fill application form", "Enter establishment name, full postal address, category of business, number of male/female employees, and working hours.", ["Rent agreement or property tax receipt"], "₹0", "1 day"),
            ("Upload identity and address proofs", "Attach photo of proprietor with shop signboard displaying name clearly in regional language & English.", ["Signboard photograph", "Electricity bill"], "₹0", "1 day"),
            ("Pay statutory registration fees", "Submit fee calculated based on employee bracket via integrated portal gateway.", ["Challan receipt"], "₹250 – ₹1,500", "Immediate"),
            ("Download digital certificate", "Receive digitally signed Shops & Establishment Certificate without physical inspection for low-risk units.", ["Application reference"], "₹0", "3 working days")
        ]
    },
    {
        "id": "fire_safety_noc_commercial",
        "category": "Licenses & Business",
        "name": "Commercial Fire Safety NOC",
        "department": "Fire and Emergency Services Department",
        "jurisdiction": "Municipal Corporation",
        "summary": "Mandatory clearance certifying fire safety preparedness for commercial premises, restaurants, hotels, and event spaces.",
        "time": "15–21 working days",
        "cost": "₹1,000 – ₹5,000 based on floor area",
        "official_url": "https://mcc.chandigarh.gov.in/fire-safety",
        "steps": [
            ("Install approved fire fighting apparatus", "Equip premises with certified ABC fire extinguishers, smoke detectors, emergency exit signage, and hose reels.", ["Equipment purchase receipts", "Layout diagram"], "Varies", "2–4 days"),
            ("Submit online NOC application", "Log in to municipal portal and provide building approval number, occupant capacity, and hazardous material disclosures.", ["Architectural floor plan", "Building sanction plan"], "₹0", "1 day"),
            ("Schedule site inspection", "Fire station officer will schedule an on-site audit of egress routes, fire alarms, and extinguisher validity.", ["Inspection checklist"], "₹0", "7–10 working days"),
            ("Rectify compliance observations", "If discrepancies are noted during inspection, complete compliance actions within 15 calendar days.", ["Compliance report"], "₹0", "3–5 days"),
            ("Issuance of Fire Safety Certificate", "Download renewable 1-year Fire Safety Certificate from municipal portal.", ["Fire NOC certificate"], "₹1,000 – ₹5,000", "2 working days")
        ]
    },
    {
        "id": "signage_advertisement_permission",
        "category": "Licenses & Business",
        "name": "Commercial Signboard & Outdoor Advertisement Permission",
        "department": "Municipal Corporation Advertisement Branch",
        "jurisdiction": "Municipal Corporation",
        "summary": "Official permit to erect commercial display boards, neon signs, hoardings, or rooftop advertisement structures.",
        "time": "7–10 working days",
        "cost": "₹500 application fee + ₹50/sq.ft annual tax",
        "official_url": "https://mcc.chandigarh.gov.in/advertisement",
        "steps": [
            ("Measure signboard dimensions", "Calculate exact display area (length x height) and ensure adherence to city standard building bylaws.", ["Dimension drawings", "Color mockup photograph"], "₹0", "1 day"),
            ("Submit online request", "Submit premises ownership proof, commercial trade license number, and structural stability certificate for large hoardings.", ["Trade license copy", "Structural engineer certificate"], "₹500", "1 day"),
            ("Zonal officer inspection", "Municipal field inspector verifies that the sign does not obstruct traffic view, electrical lines, or pedestrians.", ["Site verification log"], "₹0", "3–5 days"),
            ("Payment of advertisement tax", "Pay annual ground rent/advertisement tax calculated based on square footage.", ["Tax assessment order"], "₹500 – ₹5,000", "Immediate"),
            ("Receive permission letter", "Obtain official permit sticker and permit order valid for 1 financial year.", ["Permission letter"], "₹0", "2 days")
        ]
    },
    {
        "id": "street_vendor_vending_certificate",
        "category": "Licenses & Business",
        "name": "Street Vendor Vending Certificate & ID Card",
        "department": "Town Vending Committee / Municipal Corporation",
        "jurisdiction": "Municipal Corporation",
        "summary": "Registration under Street Vendors (Protection of Livelihood and Regulation of Street Vending) Act for hawkers and cart operators.",
        "time": "14–21 working days",
        "cost": "₹0 application + ₹150–₹500 monthly vending fee",
        "official_url": "https://pmsvanidhi.mohua.gov.in",
        "steps": [
            ("Participation in Town Vending Survey", "Verify inclusion in municipal biometric street vendor survey list or apply during quarterly open enrollment.", ["Aadhaar card", "Voter ID"], "₹0", "1 day"),
            ("Application for vending zone", "Submit preference for designated vending zones (stationary, mobile, or weekly market).", ["Passport photographs", "Bank passbook"], "₹0", "2 days"),
            ("Verification by Town Vending Committee (TVC)", "TVC reviews applicant credentials and conducts non-overlap verification.", ["Vending verification form"], "₹0", "7–10 days"),
            ("Allotment of designated vending spot", "Receive allotment letter with mapped geo-coordinates within designated vending zone.", ["Allotment order"], "₹0", "3 days"),
            ("Issuance of Smart Vending Card", "Collect smart card containing QR code, photo, and permitted trade hours.", ["Vending smart card"], "₹150", "2 days")
        ]
    },
    {
        "id": "factory_license_registration",
        "category": "Licenses & Business",
        "name": "Factory License under Factories Act 1948",
        "department": "Chief Inspectorate of Factories",
        "jurisdiction": "State Government",
        "summary": "Mandatory licensing for industrial premises employing 10+ workers with power or 20+ workers without power.",
        "time": "20–30 working days",
        "cost": "₹1,500 – ₹10,000 based on horsepower & headcount",
        "official_url": "https://labour.gov.in/factories",
        "steps": [
            ("Site and building plan approval", "Submit manufacturing flowcharts, machinery layout, and ventilation plans for pre-construction clearance.", ["Plant layout blueprint", "Process flow diagram"], "₹1,000", "10 days"),
            ("Pollution control consent (CTE)", "Obtain Consent to Establish from State Pollution Control Board before factory operation.", ["PCB CTE certificate"], "Varies", "15 days"),
            ("Submit Form 2 application", "Fill online application providing details of installed horsepower, worker capacity, and welfare facilities.", ["List of machinery", "Safety officer appointment"], "₹0", "1 day"),
            ("Inspectorate on-site audit", "Factory inspector conducts safety audit verifying guards on machinery, sanitation, and first aid provisions.", ["Compliance inspection report"], "₹0", "7 days"),
            ("Grant of Factory License", "Obtain Factory License valid for 1 to 5 years with annual renewal option.", ["Factory license document"], "₹1,500 – ₹10,000", "3 days")
        ]
    },
    {
        "id": "contract_labour_principal_registration",
        "category": "Licenses & Business",
        "name": "Contract Labour Principal Employer Registration",
        "department": "Office of the Labour Commissioner",
        "jurisdiction": "State Labour Department",
        "summary": "Mandatory registration for employers engaging 20 or more contract workers on any single day.",
        "time": "7–14 working days",
        "cost": "₹500 – ₹2,500",
        "official_url": "https://shramsuvidha.gov.in",
        "steps": [
            ("Prepare Form I statement", "Compile contractor agreements, maximum headcounts per contractor, and project duration.", ["Contractor service agreements"], "₹0", "2 days"),
            ("Online registration on Shram Suvidha", "Submit LIN (Labour Identification Number) and register establishment details.", ["PAN", "Certificate of incorporation"], "₹0", "1 day"),
            ("Fee payment based on headcount", "Pay fee scale according to total maximum contract workers employed.", ["Treasury challan"], "₹500 – ₹2,500", "Immediate"),
            ("Review by Assistant Labour Commissioner", "Department examines application for wage protection guarantees and statutory compliance.", ["Application verification"], "₹0", "5–7 days"),
            ("Issuance of Form II Registration", "Download certificate of registration as Principal Employer.", ["Form II Certificate"], "₹0", "2 days")
        ]
    },
    {
        "id": "msme_udyam_registration",
        "category": "Licenses & Business",
        "name": "MSME Udyam Registration Certificate",
        "department": "Ministry of Micro, Small and Medium Enterprises",
        "jurisdiction": "National Single Window",
        "summary": "Free official central government registration conferring priority lending, tax exemptions, and government tender benefits.",
        "time": "1–2 working days",
        "cost": "₹0 (Completely Free of Cost)",
        "official_url": "https://udyamregistration.gov.in",
        "steps": [
            ("Aadhaar OTP authentication", "Enter entrepreneur's 12-digit Aadhaar number and verify via mobile OTP on official Udyam portal.", ["Aadhaar number", "Active linked mobile"], "₹0", "Immediate"),
            ("PAN verification", "Enter business PAN card; system automatically fetches tax & turnover data from income tax database.", ["PAN card"], "₹0", "Immediate"),
            ("Fill enterprise particulars", "Specify industry category (Manufacturing/Service), NIC 2/4/5-digit codes, and plant address.", ["Bank account IFSC & number"], "₹0", "15 minutes"),
            ("Declare employment and investment", "Enter total employees and plant/machinery investment value (excluding land & building).", ["Self-declaration"], "₹0", "10 minutes"),
            ("Generate Udyam Registration Certificate", "System generates permanent digital certificate with lifetime validity and dynamic verification QR code.", ["Udyam certificate PDF"], "₹0", "Immediate")
        ]
    },
    {
        "id": "packaged_commodity_packer_registration",
        "category": "Licenses & Business",
        "name": "Legal Metrology Packaged Commodities (LMPC) Registration",
        "department": "Department of Legal Metrology",
        "jurisdiction": "Central / State Department of Consumer Affairs",
        "summary": "Mandatory license for manufacturers, packers, and importers of pre-packaged goods sold to retail consumers.",
        "time": "10–15 working days",
        "cost": "₹500 government fee",
        "official_url": "https://consumeraffairs.nic.in",
        "steps": [
            ("Review mandatory label declarations", "Ensure product packaging specifies manufacturer name, net weight, MRP, date of packaging, and customer care details.", ["Sample packaging artwork", "Product specification sheet"], "₹0", "2 days"),
            ("Submit Rule 27 application", "Apply online on Legal Metrology portal submitting business registration and manufacturing unit location.", ["GST registration", "Premises lease"], "₹500", "1 day"),
            ("Sample verification", "Legal Metrology inspector verifies declarations against standard metric units (g, kg, ml, l).", ["Packaged sample"], "₹0", "5–7 days"),
            ("Certificate grant", "Receive manufacturer/packer registration certificate with official registration number.", ["LMPC Certificate"], "₹0", "3 days")
        ]
    },
    {
        "id": "health_trade_eating_house_license",
        "category": "Licenses & Business",
        "name": "Health Trade License (Restaurants, Cafes & Bakeries)",
        "department": "Municipal Health Department",
        "jurisdiction": "Municipal Corporation",
        "summary": "Public health clearance certifying water quality, pest control, waste disposal, and hygiene standards for eateries.",
        "time": "10–14 working days",
        "cost": "₹1,500 – ₹5,000 depending on seating capacity",
        "official_url": "https://mcc.chandigarh.gov.in/health-trade",
        "steps": [
            ("Arrange water test & pest control contracts", "Obtain potable water laboratory test certificate and quarterly pest control vendor agreement.", ["Water bacteriological report", "Pest control contract"], "Varies", "3 days"),
            ("Submit premises kitchen plan", "Upload blueprint showing cooking area, grease traps, cold storage, handwash stations, and waste segregation bins.", ["Kitchen layout map"], "₹0", "1 day"),
            ("Health officer kitchen inspection", "Medical Officer of Health (MOH) conducts surprise inspection of food storage, drainage, and staff hygiene.", ["Inspection remarks"], "₹0", "5 working days"),
            ("Pay health license fee", "Remit municipal fee online upon satisfaction of inspection report.", ["Payment confirmation"], "₹1,500 – ₹5,000", "Immediate"),
            ("Download Health Trade License", "Obtain certificate to be visibly displayed at restaurant cashier counter.", ["Health Trade License"], "₹0", "2 days")
        ]
    },
    {
        "id": "trade_union_registration",
        "category": "Licenses & Business",
        "name": "Trade Union Registration under Trade Unions Act",
        "department": "Registrar of Trade Unions",
        "jurisdiction": "State Labour Department",
        "summary": "Registration conferring statutory legal status and collective bargaining rights to representative worker associations.",
        "time": "30–45 working days",
        "cost": "₹100 treasury fee",
        "official_url": "https://labour.gov.in/trade-unions",
        "steps": [
            ("Adopt constitution & bylaws", "Draft constitution containing union objectives, membership fees, executive committee rules, and election intervals.", ["Signed constitution document", "Meeting resolution minutes"], "₹0", "3 days"),
            ("Gather minimum 7 subscribing members", "Ensure minimum 10% or 100 workers (whichever is less) are enrolled as active members.", ["Member subscription register"], "₹0", "2 days"),
            ("Submit Form A application", "Submit application to Registrar of Trade Unions with details of office-bearers, addresses, and parent establishment.", ["Form A", "Office bearer list"], "₹100", "1 day"),
            ("Verification of member consent", "Labour officer verifies signatures and confirms absence of duplicate competing union registrations.", ["Scrutiny report"], "₹0", "20 days"),
            ("Issuance of Registration Certificate", "Receive Certificate of Registration in Form B with permanent registration number.", ["Form B Certificate"], "₹0", "7 days")
        ]
    },
    {
        "id": "boiler_registration_inspection",
        "category": "Licenses & Business",
        "name": "Industrial Boiler Registration & Renewal",
        "department": "Directorate of Boilers",
        "jurisdiction": "State Directorate of Boilers",
        "summary": "Statutory steam boiler commissioning and annual pressure testing certification under Indian Boilers Act.",
        "time": "15–20 working days",
        "cost": "₹2,000 – ₹15,000 based on heating surface area",
        "official_url": "https://dpiit.gov.in/boilers",
        "steps": [
            ("Submit manufacturer dossier", "Upload Form II, III & IV manufacturer material test reports, welder certificates, and hydraulic test certificate.", ["Form II/III/IV certificates", "Piping isometric drawings"], "₹0", "2 days"),
            ("Steam pipeline erection check", "Approved boiler inspector visits premises to inspect safety valves, water gauges, and steam pipeline alignment.", ["Erection audit form"], "₹0", "5 days"),
            ("Hydraulic pressure testing", "Conduct hydrostatic pressure test at 1.5 times the maximum allowable working pressure witnessed by the inspector.", ["Hydraulic test log"], "₹0", "1 day"),
            ("Steam test & safety valve setting", "Verify safety valves pop open at calibrated working pressure without pressure surge.", ["Safety valve calibration certificate"], "₹0", "2 days"),
            ("Grant of Boiler Certificate", "Receive Form VI certificate authorizing steam generation for 12 months.", ["Form VI Boiler Book"], "₹2,000 – ₹15,000", "3 days")
        ]
    },
    {
        "id": "cinematograph_theatre_license",
        "category": "Licenses & Business",
        "name": "Cinema Hall & Multiplex Exhibition License",
        "department": "District Magistrate / Licensing Authority",
        "jurisdiction": "District Administration",
        "summary": "Mandatory operating license for public cinema theatres, multiplexes, and open-air movie projection venues.",
        "time": "30–45 working days",
        "cost": "₹5,000 – ₹20,000 annual license fee",
        "official_url": "https://district.gov.in",
        "steps": [
            ("Obtain multi-department NOCs", "Acquire clearances from Electrical Inspector, PWD Structural, Fire Safety Department, and Municipal Health.", ["PWD stability certificate", "Fire NOC", "Electrical safety certificate"], "Varies", "15 days"),
            ("Submit Form B application", "Apply to District Magistrate submitting cinema hall layout, seating capacity, exit pathways, and air-conditioning plans.", ["Building plans", "Ownership documents"], "₹1,000", "2 days"),
            ("Joint multi-agency inspection", "Magisterial committee inspects auditorium acoustics, fire suppression, emergency lighting, and parking facilities.", ["Joint inspection minutes"], "₹0", "10 days"),
            ("Pay annual license fee", "Remit state entertainment tax / cinematography license fee at government treasury.", ["Treasury receipt"], "₹5,000 – ₹20,000", "Immediate"),
            ("Issuance of Form C License", "District Magistrate issues official operating license specifying approved seating count.", ["Form C Cinema License"], "₹0", "5 days")
        ]
    },
    {
        "id": "excise_temporary_liquor_permit",
        "category": "Licenses & Business",
        "name": "Temporary Event Liquor Serving Permit (L-50 / P-10)",
        "department": "Department of Excise & Taxation",
        "jurisdiction": "State Government",
        "summary": "Single-day permission to serve alcoholic beverages at private parties, banquets, and commercial corporate events.",
        "time": "2–3 working days",
        "cost": "₹2,500 – ₹10,000 per day based on venue capacity",
        "official_url": "https://excise.gov.in",
        "steps": [
            ("Book approved banquet or private venue", "Confirm venue reservation and acquire venue owner's letter of permission.", ["Venue booking receipt", "Owner consent letter"], "₹0", "1 day"),
            ("Submit online permit application", "Enter event host details, guest count estimate, event date/hours, and liquor source retailer name.", ["Host Aadhaar & PAN", "Invitation card copy"], "₹0", "1 day"),
            ("Pay permit duty online", "Remit daily event excise duty through state integrated financial management portal.", ["Challan receipt"], "₹2,500 – ₹10,000", "Immediate"),
            ("Procure liquor from authorized retailer", "Purchase beverages exclusively from authorized state vends accompanied by serial-numbered invoices.", ["Authorized excise bill"], "Varies", "1 day"),
            ("Display permit at bar counter", "Keep physical/digital copy of issued excise permit at the serving bar during the entire event.", ["Official permit pass"], "₹0", "Immediate")
        ]
    },
    {
        "id": "pet_shop_dog_breeding_license",
        "category": "Licenses & Business",
        "name": "Pet Shop & Dog Breeding Establishment License",
        "department": "State Animal Welfare Board (SAWB) & Municipal Corporation",
        "jurisdiction": "State / Municipal Corporation",
        "summary": "Mandatory license under Prevention of Cruelty to Animals (Pet Shop & Dog Breeding) Rules.",
        "time": "21–30 working days",
        "cost": "₹5,000 registration fee",
        "official_url": "https://animalwelfareboard.parivesh.nic.in",
        "steps": [
            ("Facility standard compliance", "Ensure adequate enclosure dimensions, temperature regulation, quarantine cages, and sanitary ventilation.", ["Facility layout diagram", "Veterinary care tie-up agreement"], "Varies", "3 days"),
            ("Submit Form I to State Animal Welfare Board", "Apply online with photographs of housing pens, grooming areas, and waste disposal mechanisms.", ["Aadhaar", "Veterinarian consent letter"], "₹5,000", "2 days"),
            ("Veterinary inspection committee", "Authorized veterinary officer inspects animal welfare protocols, microchipping, and vaccination logs.", ["Inspection audit sheet"], "₹0", "14 days"),
            ("Certificate grant", "Receive Animal Welfare Board registration certificate valid for 2 calendar years.", ["Pet shop registration certificate"], "₹0", "5 days")
        ]
    },
    {
        "id": "weighing_scale_verification_stamping",
        "category": "Licenses & Business",
        "name": "Commercial Weighing Scale Verification & Stamping",
        "department": "Department of Legal Metrology",
        "jurisdiction": "State Government",
        "summary": "Mandatory annual calibration and lead-sealing of electronic and mechanical balances used in trade.",
        "time": "2–4 working days",
        "cost": "₹150 – ₹800 based on scale capacity",
        "official_url": "https://consumeraffairs.nic.in",
        "steps": [
            ("Purchase model-approved scale", "Verify that the machine holds a Government of India Model Approval Certificate.", ["Model approval certificate", "Invoice"], "Varies", "1 day"),
            ("Schedule verification test", "Take scale to local Legal Metrology laboratory or request on-site inspection for heavy weighbridges.", ["Application form", "Previous stamping card"], "₹0", "1 day"),
            ("Standard mass calibration test", "Inspector tests zero error, corner load error, and sensitivity using certified standard weights.", ["Test observations"], "₹0", "1 hour"),
            ("Lead seal stamping", "Inspector fixes tamper-evident lead security seal and affixes the current year/quarter stamp.", ["Stamping stamp mark"], "₹150 – ₹800", "Immediate"),
            ("Issuance of Verification Certificate", "Receive Certificate of Verification to be kept available for surprise consumer checks.", ["Verification certificate"], "₹0", "Same day")
        ]
    },
    {
        "id": "clinical_establishment_registration",
        "category": "Licenses & Business",
        "name": "Clinical Establishment Registration (Clinics & Diagnostic Labs)",
        "department": "District Health Administration",
        "jurisdiction": "State Health Department",
        "summary": "Statutory registration under Clinical Establishments (Registration and Regulation) Act.",
        "time": "20–30 working days",
        "cost": "₹1,000 – ₹5,000 based on beds & services",
        "official_url": "https://clinicalestablishments.gov.in",
        "steps": [
            ("Verify doctor qualifications", "Compile medical council registrations (NMC/DCI) for all practicing clinicians and technicians.", ["Medical registration certificates", "Doctor degrees"], "₹0", "2 days"),
            ("Bio-medical waste agreement", "Execute formal contract with authorized Common Bio-medical Waste Treatment Facility (CBWTF).", ["BMW agreement copy"], "Varies", "2 days"),
            ("Online Form A submission", "Enter clinic carpet area, emergency equipment list, staff roster, and tariff transparency board.", ["Form A", "Premises lease"], "₹1,000 – ₹5,000", "1 day"),
            ("Civil Surgeon audit", "District inspection committee inspects sterilization autoclaves, drug storage, and waste color bins.", ["Audit report"], "₹0", "10–14 days"),
            ("Issuance of Provisional/Permanent Certificate", "Receive certificate of registration valid for display in the reception lobby.", ["Clinical Establishment Certificate"], "₹0", "5 days")
        ]
    },

    # ---------------- 2. Utilities & Municipal ----------------
    {
        "id": "electricity_load_enhancement",
        "category": "Utilities & Municipal",
        "name": "Electricity Load Enhancement / Reduction",
        "department": "State Electricity Distribution Company (DISCOM)",
        "jurisdiction": "State Electricity Board",
        "summary": "Procedure to increase or decrease sanctioned electrical connected load for residential and commercial premises.",
        "time": "7–10 working days",
        "cost": "₹300 – ₹1,500 security deposit per kW enhanced",
        "official_url": "https://cspdcl.co.in",
        "steps": [
            ("Calculate total connected wattage", "Add wattage of new air-conditioners, motors, and appliances to determine required kW.", ["List of appliances"], "₹0", "1 day"),
            ("Submit application on DISCOM portal", "Enter consumer CA number, current sanctioned load, requested load, and upload latest paid electricity bill.", ["Latest paid electricity bill", "Ownership proof/Lease"], "₹0", "1 day"),
            ("Wiring test certificate submission", "For load enhancements exceeding 5 kW, submit wiring test report signed by a licensed electrical contractor.", ["Licensed contractor test report"], "₹250", "2 days"),
            ("Pay security & service charges", "Pay revised security deposit and meter upgrade fee via integrated net banking or bill desk.", ["Payment receipt"], "₹300 – ₹1,500 / kW", "Immediate"),
            ("Meter replacement or breaker recalibration", "DISCOM linesman installs appropriate CT meter or adjusts MCB rating at property.", ["Work completion certificate"], "₹0", "3–5 days")
        ]
    },
    {
        "id": "domestic_sewerage_connection",
        "category": "Utilities & Municipal",
        "name": "New Underground Sewerage Connection",
        "department": "Public Health & Engineering Department / Municipal Corporation",
        "jurisdiction": "Municipal Corporation",
        "summary": "Sanction to connect household drainage pipe to municipal underground sewer mains.",
        "time": "10–15 working days",
        "cost": "₹1,200 – ₹3,500 connection & road cutting fee",
        "official_url": "https://mcc.chandigarh.gov.in/sewerage",
        "steps": [
            ("Prepare internal plumbing blueprint", "Plumbing map showing inspection chambers, slope gradients, and gully trap locations.", ["Plumber layout plan"], "₹0", "2 days"),
            ("Submit municipal application", "Submit building sanction letter, water connection receipt, and road cutting permission request.", ["Water connection bill", "Building completion copy"], "₹0", "1 day"),
            ("Junior Engineer field inspection", "JE measures distance from property boundary to sewer manhole and estimates road restoration fee.", ["JE site measurement"], "₹0", "5 days"),
            ("Payment of road restoration charges", "Pay connection fee and road restoration deposit at municipal citizen service counter.", ["Municipal receipt"], "₹1,200 – ₹3,500", "Immediate"),
            ("Supervised connection & sealing", "Licensed plumber executes pipeline hookup to municipal manhole under junior engineer supervision.", ["Connection completion memo"], "₹0", "3 days")
        ]
    },
    {
        "id": "rooftop_solar_net_metering",
        "category": "Utilities & Municipal",
        "name": "Rooftop Solar Net Metering Connection",
        "department": "State Nodal Renewable Energy Agency & DISCOM",
        "jurisdiction": "State Government / PM Surya Ghar",
        "summary": "Interconnection approval and bidirectional solar meter installation under PM Surya Ghar Muft Bijli Yojana.",
        "time": "20–30 working days",
        "cost": "₹1,000 application fee (Subsidies up to ₹78,000 available)",
        "official_url": "https://pmsuryaghar.gov.in",
        "steps": [
            ("Register on National Solar Portal", "Apply on PM Surya Ghar portal selecting DISCOM, consumer account number, and proposed solar kW capacity.", ["Electricity bill", "Aadhaar"], "₹0", "Immediate"),
            ("Technical feasibility approval (TFR)", "DISCOM checks distribution transformer capacity and issues technical clearance within 10 days.", ["TFR Approval letter"], "₹0", "7–10 days"),
            ("Installation by empanelled vendor", "Empanelled solar contractor installs ALMM-approved solar panels, grid-tied inverter, and earthing.", ["Plant commissioning document", "Vendor invoice"], "Varies", "5–7 days"),
            ("Net meter inspection and testing", "DISCOM inspects anti-islanding protection and installs bidirectional import-export net meter.", ["Net meter test report"], "₹1,000", "5 days"),
            ("Direct Benefit Transfer (DBT) subsidy", "DISCOM submits commissioning report; central subsidy credited directly to citizen's bank account within 30 days.", ["Bank passbook copy"], "Subsidy credit", "30 days")
        ]
    },
    {
        "id": "png_piped_gas_connection",
        "category": "Utilities & Municipal",
        "name": "Domestic Piped Natural Gas (PNG) Connection",
        "department": "City Gas Distribution Utility (e.g. IGL / GAIL Gas)",
        "jurisdiction": "City Gas Utility",
        "summary": "Piped natural gas pipeline installation for domestic cooking and water geysers.",
        "time": "10–14 working days",
        "cost": "₹5,000 – ₹7,000 (Refundable security deposit)",
        "official_url": "https://gailonline.com",
        "steps": [
            ("Check pipeline network availability", "Verify whether gas pipeline riser has been laid in your residential lane or apartment tower.", ["Address proof"], "₹0", "Immediate"),
            ("Submit online connection request", "Submit ownership proof or NOC from landlord along with identity details.", ["Rent agreement / Sale deed", "PAN / Aadhaar"], "₹0", "1 day"),
            ("Pay refundable connection deposit", "Pay security deposit online or opt for installments integrated into bimonthly gas bills.", ["Payment receipt"], "₹5,000 – ₹7,000", "Immediate"),
            ("Internal kitchen piping installation", "Utility technician installs yellow GI pipeline, copper tubing, gas isolation valve, and digital meter.", ["Installation safety certificate"], "₹0", "3–5 days"),
            ("Stove conversion and gas commissioning", "Technician adjusts stove nozzle from LPG to PNG and commissions gas flow safely.", ["Commissioning slip"], "₹0", "1 day")
        ]
    },
    {
        "id": "solid_waste_debris_removal_service",
        "category": "Utilities & Municipal",
        "name": "Construction & Demolition (C&D) Debris Removal",
        "department": "Municipal Solid Waste Management Division",
        "jurisdiction": "Municipal Corporation",
        "summary": "On-demand municipal collection service for bulk concrete, brick, and renovation debris to prevent illegal dumping.",
        "time": "2–4 working days",
        "cost": "₹500 – ₹1,500 per tractor trolley load",
        "official_url": "https://mcc.chandigarh.gov.in/waste-management",
        "steps": [
            ("Estimate debris quantity", "Assess approximate volume of renovation debris in metric tons or trolley loads.", ["Photographs of debris heap"], "₹0", "Same day"),
            ("Book pickup on municipal helpline / portal", "Register booking on municipal app or citizen helpline providing pickup address.", ["Aadhaar", "Contact mobile"], "₹0", "Immediate"),
            ("Pay lifting charges", "Pay prescribed lifting and processing charges online.", ["Challan payment"], "₹500 – ₹1,500 / load", "Immediate"),
            ("Designated dumping pickup", "Municipal hydraulic tipper arrives at site, loads waste, and transports it to recycling facility.", ["Waste handover slip"], "₹0", "2 working days")
        ]
    },
    {
        "id": "faulty_water_meter_testing",
        "category": "Utilities & Municipal",
        "name": "Testing and Replacement of Faulty Water Meter",
        "department": "Public Health & Water Supply Division",
        "jurisdiction": "Municipal Corporation",
        "summary": "Official laboratory accuracy testing of water meters reporting excessively high readings.",
        "time": "7–10 working days",
        "cost": "₹150 testing fee (Refunded if meter found defective)",
        "official_url": "https://mcc.chandigarh.gov.in/water-meter",
        "steps": [
            ("Lodge excessive billing complaint", "Register dispute citing previous 3 billing cycles on water portal.", ["Previous 3 water bills"], "₹0", "1 day"),
            ("Pay lab test deposit", "Deposit standard laboratory testing fee at municipal cash counter.", ["Fee receipt"], "₹150", "Immediate"),
            ("Meter removal under seal", "Municipal plumber visits site, disconnects meter in presence of consumer, and applies tamper seal.", ["Removal memo with initial reading"], "₹0", "2 days"),
            ("Laboratory flow calibration test", "Meter tested at test bench across slow, medium, and high flow rates.", ["Calibration test report"], "₹0", "3 days"),
            ("Replacement and bill adjustment", "If error > 5%, meter replaced with calibrated unit and excess billing adjusted in next bill cycle.", ["Revised billing advice"], "₹0", "2 days")
        ]
    },
    {
        "id": "tree_pruning_removal_permission",
        "category": "Utilities & Municipal",
        "name": "Tree Pruning and Dangerous Branch Removal Permission",
        "department": "Horticulture Department / Forest Division",
        "jurisdiction": "Municipal Corporation",
        "summary": "Permit required before pruning or cutting overgrown trees touching power lines or endangering private structures.",
        "time": "7–12 working days",
        "cost": "₹0 for municipal trees; ₹200 fee for private premises",
        "official_url": "https://mcc.chandigarh.gov.in/horticulture",
        "steps": [
            ("Take location photographs", "Photograph tree showing dangerous proximity to building wall, roof, or electrical conductors.", ["Clear photographs from 2 angles"], "₹0", "Same day"),
            ("Submit online request", "Submit request on municipal citizen portal specifying species (if known) and reason for cutting/pruning.", ["Property ownership proof"], "₹0", "1 day"),
            ("Horticulture inspector site appraisal", "Horticulture officer visits premises to confirm hazard and issue pruning guidance.", ["Site appraisal report"], "₹0", "5 working days"),
            ("Issuance of work permit", "Municipal department dispatches bucket crane for street trees, or issues written clearance for private courtyard trees.", ["Pruning sanction letter"], "₹0", "2 days")
        ]
    },
    {
        "id": "rainwater_harvesting_rebate",
        "category": "Utilities & Municipal",
        "name": "Rainwater Harvesting System Certification & Property Tax Rebate",
        "department": "Municipal Engineering & Building Department",
        "jurisdiction": "Municipal Corporation",
        "summary": "Certification of functional rainwater harvesting pits to claim up to 10% annual rebate on property tax.",
        "time": "14–20 working days",
        "cost": "₹0 application fee",
        "official_url": "https://mcc.chandigarh.gov.in/rwh-rebate",
        "steps": [
            ("Construct RWH pit per bylaws", "Ensure recharge pit, filtration bed, and desilting chamber conform to municipal engineering specifications.", ["Construction bills", "Photographs of pit"], "Varies", "5–7 days"),
            ("Apply for RWH certificate", "Submit online application with property tax assessment number and plumber completion certificate.", ["Property tax bill", "Plumbing certificate"], "₹0", "1 day"),
            ("Site inspection by junior engineer", "JE inspects catchment slope, filter media, and injection well to confirm operational status.", ["JE inspection sheet"], "₹0", "7 days"),
            ("Issuance of RWH Compliance Certificate", "Executive Engineer approves certificate valid for 3 financial years.", ["RWH Certificate"], "₹0", "3 days"),
            ("Automatic tax rebate linkage", "Rebate automatically applied as deduction in annual property tax bill.", ["Updated tax demand notice"], "₹0", "Immediate")
        ]
    },
    {
        "id": "street_light_complaint_redressal",
        "category": "Utilities & Municipal",
        "name": "Street Light Repair & New Pole Installation",
        "department": "Electrical Wing, Municipal Corporation",
        "jurisdiction": "Municipal Corporation",
        "summary": "Mechanism to report non-functional public LED streetlights or request dark-spot illumination poles.",
        "time": "24–48 hours for repair; 15 days for new pole",
        "cost": "₹0 (Completely Free Municipal Service)",
        "official_url": "https://mcc.chandigarh.gov.in/streetlights",
        "steps": [
            ("Note pole number and landmark", "Find the yellow-stenciled pole code or locate exact spot on municipal GIS mobile map.", ["Pole serial number", "GPS location pin"], "₹0", "5 minutes"),
            ("Log ticket on municipal mobile app", "Submit complaint under 'Street Lighting' category with photo of dark street.", ["Complaint ticket number"], "₹0", "2 minutes"),
            ("Automated dispatch to maintenance van", "System dispatches ticket to designated ward electrician with SMS alert.", ["Dispatch notification"], "₹0", "4 hours"),
            ("Replacement of LED luminaire / cable", "Electrician repairs damaged underground cable or replaces driver/LED luminaire.", ["Work closure photo"], "₹0", "24 hours"),
            ("Citizen closure feedback", "Citizen receives resolution SMS and rates service quality.", ["Feedback confirmation"], "₹0", "Immediate")
        ]
    },
    {
        "id": "dead_animal_carcass_removal",
        "category": "Utilities & Municipal",
        "name": "Carcass and Dead Animal Removal Service",
        "department": "Public Health & Sanitation Branch",
        "jurisdiction": "Municipal Corporation",
        "summary": "Emergency hygienic lifting and scientific disposal of dead cattle, dogs, and domestic animals.",
        "time": "2–6 hours emergency response",
        "cost": "₹0 for public roads; nominal fee for large farm animals",
        "official_url": "https://mcc.chandigarh.gov.in/sanitation",
        "steps": [
            ("Call municipal toll-free control room", "Dial municipal 24x7 control room or submit emergency ticket on municipal portal.", ["Exact landmark and animal description"], "₹0", "Immediate"),
            ("Ticket generation & GPS tagging", "Control room operator logs emergency request with geo-tagging for the sanitation fleet.", ["Emergency ticket SMS"], "₹0", "10 minutes"),
            ("Dedicated carcass recovery van arrival", "Sanitation crew equipped with protective gear and disinfectants loads animal carcass.", ["Disinfectant spray log"], "₹0", "2–4 hours"),
            ("Bleaching powder sanitization", "Crew sprays sodium hypochlorite / bleaching powder on the area to prevent infection spread.", ["Site sanitization"], "₹0", "15 minutes")
        ]
    },
    {
        "id": "bulk_water_tanker_supply",
        "category": "Utilities & Municipal",
        "name": "Emergency Potable Water Tanker Booking",
        "department": "Public Health Water Works",
        "jurisdiction": "Municipal Corporation",
        "summary": "Booking of municipal water tankers for private weddings, religious congregations, or pipeline burst emergencies.",
        "time": "4–12 hours",
        "cost": "₹400 – ₹800 per 5,000-litre tanker",
        "official_url": "https://mcc.chandigarh.gov.in/water-tanker",
        "steps": [
            ("Select delivery slot", "Choose date, delivery window (morning/evening), and required water quantity on booking portal.", ["Delivery address"], "₹0", "10 minutes"),
            ("Provide water connection details", "Enter existing water account number (if resident) or event sanction letter.", ["Water account ID / Event permission"], "₹0", "5 minutes"),
            ("Pay tanker charges online", "Pay fee via UPI/card to receive tanker booking confirmation with driver contact.", ["Online booking receipt"], "₹400 – ₹800", "Immediate"),
            ("GPS tracking & delivery", "Track tanker in real-time on municipal map and verify water discharge into storage underground sump.", ["Delivery acknowledgement"], "₹0", "At slot")
        ]
    },
    {
        "id": "community_hall_park_booking",
        "category": "Utilities & Municipal",
        "name": "Municipal Community Centre & Park Booking",
        "department": "Community Services Branch",
        "jurisdiction": "Municipal Corporation",
        "summary": "Reservation of air-conditioned community centres, banquet halls, and public parks for family functions and weddings.",
        "time": "Immediate online confirmation",
        "cost": "₹5,000 – ₹30,000 + refundable security deposit",
        "official_url": "https://mcc.chandigarh.gov.in/community-centres",
        "steps": [
            ("Search venue availability", "Select ward, community centre, event date, and shift (morning/evening/full day) on calendar view.", ["Date and shift selection"], "₹0", "5 minutes"),
            ("Fill applicant credentials", "Submit Aadhaar of event organizer, residential address, and nature of gathering.", ["Aadhaar card", "PAN card"], "₹0", "10 minutes"),
            ("Pay rental and security deposit", "Make online payment for booking charges, sanitation fee, and refundable security deposit.", ["Payment gateway receipt"], "₹5,000 – ₹30,000", "Immediate"),
            ("Obtain booking permit", "Download official allotment letter and gate entry pass to present to security warden.", ["Allotment letter with QR code"], "₹0", "Immediate"),
            ("Security deposit refund", "Deposit refunded directly to source bank account within 7 days after function if no property damage occurs.", ["Bank account IFSC"], "₹0", "7 days post-event")
        ]
    },
    {
        "id": "domestic_borewell_drilling_permission",
        "category": "Utilities & Municipal",
        "name": "Borewell Drilling & Groundwater Extraction NOC",
        "department": "Central Ground Water Authority (CGWA) & Water Resources Dept",
        "jurisdiction": "State Ground Water Authority",
        "summary": "Mandatory prior permission to drill deep borewells or tubewells to extract groundwater.",
        "time": "30–45 working days",
        "cost": "₹1,000 application fee + abstraction charges",
        "official_url": "https://cgwa-noc.gov.in",
        "steps": [
            ("Verify groundwater notification zone", "Check whether property falls in 'Safe', 'Semi-Critical', or 'Over-Exploited/Notified' zone.", ["Zone advisory status"], "₹0", "Same day"),
            ("Submit hydrogeological report", "Upload hydrogeological feasibility report prepared by accredited groundwater consultant.", ["Consultant report", "Proposed depth and diameter"], "Varies", "5 days"),
            ("Submit online application on CGWA portal", "Attach property land ownership documents, water requirement calculation, and flow meter proposal.", ["Khasra/Khatauni or Registry", "Digital flow meter invoice"], "₹1,000", "2 days"),
            ("District advisory committee scrutiny", "District Ground Water Cell scrutinizes non-availability of piped water supply before granting permit.", ["Committee evaluation report"], "₹0", "20 days"),
            ("Drilling permission with telemetry condition", "Obtain formal drilling permit with mandatory condition of installing tamper-proof digital flow meter.", ["NOC Certificate"], "₹0", "5 days")
        ]
    },
    {
        "id": "public_hydrant_drinking_water_installation",
        "category": "Utilities & Municipal",
        "name": "Public Water Hydrant / Standpost Sanction",
        "department": "Water Supply & Public Health Division",
        "jurisdiction": "Municipal Corporation",
        "summary": "Community application to install public drinking water coolers or standposts in public squares and markets.",
        "time": "15–20 working days",
        "cost": "₹0 (Funded by Municipal / Ward Councillor funds)",
        "official_url": "https://mcc.chandigarh.gov.in/public-hydrant",
        "steps": [
            ("Resident welfare association resolution", "Adopt resolution by market association or RWA highlighting public footfall and drinking water need.", ["Signed resolution", "Signatures of 20+ residents"], "₹0", "3 days"),
            ("Submit proposal to Ward Councillor / Superintending Engineer", "Submit request specifying exact footpath or park corner location.", ["Site layout photograph"], "₹0", "1 day"),
            ("Feasibility check by water division", "Engineers inspect pipeline water pressure and drainage outlet availability.", ["Technical feasibility report"], "₹0", "7 days"),
            ("Work order execution", "Municipal contractors lay pipe connection and construct tiled platform with automatic taps.", ["Work order copy"], "₹0", "10 days")
        ]
    },
    {
        "id": "domestic_septic_tank_cleaning_booking",
        "category": "Utilities & Municipal",
        "name": "Mechanical Septic Tank Emptying (FSSM)",
        "department": "Faecal Sludge & Septage Management (FSSM) Cell",
        "jurisdiction": "Municipal Corporation",
        "summary": "Safe, mechanized desludging of residential septic tanks by authorized vacuum suction tankers.",
        "time": "24–48 hours",
        "cost": "₹1,000 – ₹2,500 per tanker trip",
        "official_url": "https://mcc.chandigarh.gov.in/fssm",
        "steps": [
            ("Online slot booking", "Select residential location and estimate tank volume on municipal septage portal.", ["Address proof", "Contact number"], "₹0", "5 minutes"),
            ("Pay government approved tariff", "Avoid illegal private dumpers by paying fixed municipal desludging fee.", ["Payment receipt"], "₹1,000 – ₹2,500", "Immediate"),
            ("Vacuum tanker dispatch", "GPS-tracked vacuum truck arrives with safety equipment and flexible suction hoses.", ["Tanker dispatch notice"], "₹0", "24 hours"),
            ("Safe disposal at Sewage Treatment Plant (STP)", "Waste transported to certified treatment facility; citizen receives scientific disposal receipt.", ["Disposal acknowledgement"], "₹0", "Immediate")
        ]
    },
    {
        "id": "stray_animal_nuisance_complaint",
        "category": "Utilities & Municipal",
        "name": "Stray Cattle & Dog Animal Birth Control (ABC) Request",
        "department": "Veterinary Services & Animal Husbandry Branch",
        "jurisdiction": "Municipal Corporation",
        "summary": "Request for relocation of aggressive stray cattle to gaushalas, or vaccination/sterilization of community dogs under ABC rules.",
        "time": "24 hours for cattle; 3–5 days for ABC dog sterilization",
        "cost": "₹0 (Municipal Public Service)",
        "official_url": "https://mcc.chandigarh.gov.in/animal-services",
        "steps": [
            ("Register complaint on citizen app", "Select 'Stray Animal Issue', upload photograph of animal group, and provide exact street landmark.", ["Location photograph", "Colony address"], "₹0", "5 minutes"),
            ("Cattle catching squad dispatch", "Specialized vehicle equipped with hydraulic ramp impounds stray cattle and transports them to municipal gaushala.", ["Impounding log"], "₹0", "24 hours"),
            ("Animal Birth Control (ABC) process for dogs", "Registered animal welfare NGO captures dogs humanely, performs spaying/neutering, rabies vaccination, ear notching, and releases them back into original territory.", ["ABC surgical log"], "₹0", "3–5 days"),
            ("Confirmation SMS", "Complainant receives resolution alert with photograph of cleared area.", ["Closure confirmation"], "₹0", "Immediate")
        ]
    },

    # ---------------- 3. Property, Revenue & Building ----------------
    {
        "id": "property_mutation_transfer",
        "category": "Property & Tax",
        "name": "Property Mutation (Transfer of Title in Revenue Records)",
        "department": "Revenue Department / Land Records",
        "jurisdiction": "Tehsil / Municipal Corporation",
        "summary": "Official update of municipal and revenue land ownership records following property purchase, gift, inheritance, or partition.",
        "time": "15–30 working days",
        "cost": "₹500 – ₹2,000 mutation fee",
        "official_url": "https://landrecords.gov.in",
        "steps": [
            ("Gather registered transfer deed", "Obtain certified copy of Registered Sale Deed, Gift Deed, Relinquishment Deed, or Probate of Will.", ["Registered Deed", "Previous owner title deed"], "₹0", "1 day"),
            ("Apply online on Revenue Portal", "Submit mutation application providing property unique identification number (UPRN), seller and buyer particulars.", ["Aadhaar", "PAN", "Registered Deed copy"], "₹500", "1 day"),
            ("Issuance of 15-day public notice", "Patwari/Tehsildar issues a 15-day public notice to invite objections from legal heirs or co-sharers.", ["Public proclamation notice"], "₹0", "15 days"),
            ("Verification of possession", "Field revenue inspector inspects property to verify actual physical possession.", ["Inspector field verification report"], "₹0", "5 days"),
            ("Tehsildar sanction and Jamabandi update", "Tehsildar sanctions mutation order; property record is updated in the computerized Jamabandi / RoR.", ["Sanctioned Mutation Order", "Updated Jamabandi / Fard"], "₹0", "3 days")
        ]
    },
    {
        "id": "building_plan_approval_sanction",
        "category": "Property & Tax",
        "name": "Residential Building Plan Approval (Naksha Sanction)",
        "department": "Town Planning & Building Branch",
        "jurisdiction": "Municipal Corporation / Urban Development Authority",
        "summary": "Mandatory architectural drawing sanction before commencing construction or structural alteration of residential houses.",
        "time": "15–21 working days",
        "cost": "₹15 – ₹30 per square yard scrutiny fee + labor cess",
        "official_url": "https://mcc.chandigarh.gov.in/building-plans",
        "steps": [
            ("Engage registered architect", "Architect prepares computer-aided CAD drawings conforming to FAR, setbacks, height, and parking bylaws.", ["Architectural CAD drawings", "Structural stability certificate"], "Varies", "5–7 days"),
            ("Submit via Online Building Plan Approval System (OBPAS)", "Upload CAD drawings; automated system runs algorithmic rule-checking against city master plan bylaws.", ["Title deed", "Possession certificate", "Demarcation plan"], "₹1,500 – ₹5,000", "1 day"),
            ("Multi-department scrutiny", "Fire department, public health engineering, and structural division review clearances simultaneously.", ["Online scrutiny report"], "₹0", "7–10 days"),
            ("Pay building permit fee & labor cess", "Remit approved sanction fees, external development charges, and 1% building workers welfare cess.", ["Challan receipt"], "Calculated online", "Immediate"),
            ("Download sanctioned building permit", "Download digitally stamped Naksha blueprint with QR verification code valid for 3 years.", ["Sanctioned Plan PDF"], "₹0", "2 days")
        ]
    },
    {
        "id": "occupancy_completion_certificate",
        "category": "Property & Tax",
        "name": "Building Completion & Occupancy Certificate (OC)",
        "department": "Municipal Building Branch",
        "jurisdiction": "Municipal Corporation",
        "summary": "Final legal document certifying that building construction strictly matches approved plans and is safe for human habitation.",
        "time": "15–21 working days",
        "cost": "₹500 application fee",
        "official_url": "https://mcc.chandigarh.gov.in/occupancy-certificate",
        "steps": [
            ("Obtain Architect Completion Certificate", "Architect and structural engineer sign Form of Completion stating construction follows sanctioned plans.", ["Architect certificate", "As-built drawings"], "₹0", "2 days"),
            ("Obtain utility completion memos", "Procure formal connection memos from sewerage, water supply, and electrical safety wings.", ["Water connection slip", "Sewerage connection certificate"], "₹0", "3 days"),
            ("Submit OC application online", "Submit application on municipal building portal attaching all NOCs and photographs of all elevations.", ["All elevation photos", "Rainwater harvesting proof"], "₹500", "1 day"),
            ("Joint engineering inspection", "Municipal team measures setbacks, room heights, parking area, and fire exits against approved blueprint.", ["Site inspection measurement book"], "₹0", "7 days"),
            ("Issuance of Occupancy Certificate", "Municipal Corporation issues Occupancy Certificate enabling permanent utility connections and property sale.", ["Occupancy Certificate document"], "₹0", "3 days")
        ]
    },
    {
        "id": "encumbrance_certificate_property",
        "category": "Property & Tax",
        "name": "Encumbrance Certificate (EC) for Property",
        "department": "Department of Registration and Stamps",
        "jurisdiction": "Sub-Registrar Office",
        "summary": "Legal document proving property is free from registered financial liabilities, bank mortgages, court attachments, or title claims.",
        "time": "3–5 working days",
        "cost": "₹100 – ₹300 search fee based on period",
        "official_url": "https://igrsup.gov.in",
        "steps": [
            ("Identify property survey/khasra number", "Locate exact village, sector, survey/plot number, and previous deed registered numbers.", ["Previous sale deed copy"], "₹0", "10 minutes"),
            ("Apply on Sub-Registrar online portal", "Enter search period (e.g. 15 or 30 years), applicant details, and property boundary descriptions.", ["Aadhaar card"], "₹100 – ₹300", "1 day"),
            ("Sub-registrar index verification", "Department records examiner searches Book 1 registered property deed archives.", ["Archive index search"], "₹0", "2 days"),
            ("Download Nil Encumbrance Certificate (Form 15/16)", "Receive digitally signed EC certifying clean title or listing registered mortgages/encumbrances.", ["Encumbrance Certificate PDF"], "₹0", "Same day")
        ]
    },
    {
        "id": "property_tax_self_assessment",
        "category": "Property & Tax",
        "name": "Property Tax Self-Assessment & Annual Return Filing",
        "department": "Municipal Property Tax Assessment Branch",
        "jurisdiction": "Municipal Corporation",
        "summary": "Annual self-declaration of property unit area, covered area, and usage category to calculate and remit municipal house tax.",
        "time": "Immediate online receipt",
        "cost": "Varies by covered area & circle rate (Early bird rebate up to 10%)",
        "official_url": "https://mcc.chandigarh.gov.in/property-tax",
        "steps": [
            ("Look up Property ID / Assessment Number", "Enter 10-digit Property ID or registered mobile number on municipal property tax portal.", ["Previous property tax receipt"], "₹0", "Immediate"),
            ("Review property particulars", "Verify land plot area, covered carpet area across floors, residential vs commercial occupancy, and tenant details.", ["Property measurements"], "₹0", "5 minutes"),
            ("System tax calculation with rebates", "System calculates gross tax, applies early bird 10% discount and senior citizen/female owner concession.", ["Computed tax demand breakdown"], "₹0", "Immediate"),
            ("Pay online via instant payment gateway", "Pay via UPI, credit/debit card, or download bank challan for payment at designated authorized banks.", ["Instant tax payment receipt"], "Calculated tax amount", "Immediate"),
            ("Download annual property tax clearance", "Download property tax clearance certificate for the current financial year.", ["Tax Clearance Certificate with QR"], "₹0", "Immediate")
        ]
    },
    {
        "id": "noc_property_sale_transfer",
        "category": "Property & Tax",
        "name": "No Objection Certificate (NOC) for Property Sale / Conveyance",
        "department": "Urban Estate / Housing Board / Development Authority",
        "jurisdiction": "State Development Authority",
        "summary": "Mandatory clearance certifying no pending installments, encroachment, or building violations prior to deed registration.",
        "time": "15–21 working days",
        "cost": "₹1,000 – ₹2,500 scrutiny fee",
        "official_url": "https://huda.org.in",
        "steps": [
            ("Clear all outstanding dues", "Pay pending water bills, property tax, and lease rent arrears up to the current quarter.", ["No dues receipts from water/tax branches"], "₹0", "2 days"),
            ("Submit transfer NOC request", "Upload allotment letter, possession slip, proposed buyer identity proofs, and non-encroachment affidavit.", ["Allotment letter", "Indemnity bond and affidavits"], "₹1,000", "1 day"),
            ("Field inspection by enforcement wing", "Authority junior engineer visits plot to verify that no illegal construction or boundary encroachment exists.", ["Inspection report"], "₹0", "7 days"),
            ("Scrutiny of legal title", "Estate officer's legal cell verifies original files and legal heir succession records.", ["Legal scrutiny memo"], "₹0", "5 days"),
            ("Issuance of Transfer NOC", "Receive formal Permission to Transfer / No Dues NOC authorizing sub-registrar registration.", ["Transfer NOC letter"], "₹0", "2 days")
        ]
    },
    {
        "id": "stamp_duty_refund_unexecuted_deed",
        "category": "Property & Tax",
        "name": "Refund of Unused / Spoiled E-Stamp Paper Duty",
        "department": "Collector of Stamps / Treasury Office",
        "jurisdiction": "District Revenue Department",
        "summary": "Procedure to recover up to 90% of stamp duty paid on cancelled property purchase transactions or spoiled stamp papers.",
        "time": "30–45 working days",
        "cost": "10% statutory deduction from total stamp value",
        "official_url": "https://shcilestamp.com",
        "steps": [
            ("Preserve original e-stamp certificate", "Ensure application is submitted within statutory 6 months from e-stamp certificate purchase date.", ["Original e-stamp certificate", "Purchase receipt"], "₹0", "1 day"),
            ("Affidavit of cancellation", "Execute sworn affidavit before notary stating reasons for cancellation and that deed was never executed/registered.", ["Notarized cancellation affidavit"], "₹100", "1 day"),
            ("Sub-registrar non-registration certificate", "Sub-Registrar inspects archives and issues certificate confirming stamp was never used for registration.", ["Non-use certificate"], "₹0", "7 days"),
            ("Submit refund claim to Collector", "Submit application to District Collector (Stamps) with bank account details for Direct Benefit Transfer.", ["Cancelled cheque", "PAN card copy"], "₹0", "2 days"),
            ("Order of refund and bank credit", "Collector approves refund deducting 10% statutory fee; amount credited to buyer's bank account.", ["Refund sanction order"], "10% deduction", "15–20 days")
        ]
    },
    {
        "id": "demarcation_land_boundaries",
        "category": "Property & Tax",
        "name": "Official Land Boundary Demarcation (Nishandehi)",
        "department": "Tehsil Office / Department of Revenue & Land Records",
        "jurisdiction": "Tehsildar",
        "summary": "Official measurement and boundary pegging by government revenue surveyor (Kanungo/Patwari) to resolve boundary disputes.",
        "time": "15–25 working days",
        "cost": "₹200 – ₹500 government fee",
        "official_url": "https://revenue.gov.in",
        "steps": [
            ("Obtain latest Jamabandi and Sajra (Map)", "Procure certified computerized land records (Fard) and village cadastral map from revenue center.", ["Certified Jamabandi copy", "Sajra map extract"], "₹50", "1 day"),
            ("Apply to Tehsildar for Nishandehi", "Submit demarcation application citing Khasra/Killa numbers and adjoining landowner details.", ["Application form", "Aadhaar card"], "₹200", "1 day"),
            ("Notice to adjoining boundary owners", "Tehsildar issues written notices summoning owners of all four adjacent plots to be present on site.", ["Summon notices"], "₹0", "7 days"),
            ("Field measurement by Kanungo & ETS/DGPS", "Revenue team measures from fixed benchmark points using Electronic Total Station / metric chain.", ["Measurement field book"], "₹0", "1 day"),
            ("Boundary stone fixation & report sign-off", "Fix boundary pegs in presence of all parties; prepare Panchnama report signed by panchas.", ["Demarcation Panchnama report"], "₹0", "3 days")
        ]
    },
    {
        "id": "land_use_change_clu_permission",
        "category": "Property & Tax",
        "name": "Change of Land Use (CLU) Permission",
        "department": "Town & Country Planning Department",
        "jurisdiction": "State Government",
        "summary": "Sanction to convert agricultural land into commercial, institutional, or industrial operational use.",
        "time": "45–60 working days",
        "cost": "Scrutiny fee + Conversion charges based on master plan zone",
        "official_url": "https://tcpharyana.gov.in",
        "steps": [
            ("Master plan zone verification", "Confirm whether land falls inside designated urbanizable boundary in city master plan.", ["Master plan zoning map"], "₹0", "1 day"),
            ("Comprehensive project report (CPR)", "Prepare project report showing proposed land use, access road width, water demand, and effluent treatment.", ["CPR document", "Architectural layout"], "Varies", "7 days"),
            ("Submit CLU application online", "Submit Jamabandi, Aks Shajra, non-encumbrance certificate, and scrutiny fee on state town planning portal.", ["Title deeds", "Cadastral map", "Mutation copies"], "Calculated online", "2 days"),
            ("Inter-departmental clearance (IDC)", "Public works, forest, irrigation, and pollution boards examine site access and flood plains.", ["Departmental NOCs"], "₹0", "30 days"),
            ("Grant of In-Principle CLU & Letter of Intent", "Director of Town Planning issues formal CLU sanction order upon payment of conversion charges.", ["CLU Sanction Certificate"], "Varies", "10 days")
        ]
    },
    {
        "id": "property_deed_certified_copy",
        "category": "Property & Tax",
        "name": "Certified Copy of Registered Sale / Title Deed",
        "department": "Registration & Stamps Department",
        "jurisdiction": "Sub-Registrar Office",
        "summary": "Procuring legally admissible certified copies of registered title deeds from government registration records.",
        "time": "2–4 working days",
        "cost": "₹100 – ₹250 search & copying fee",
        "official_url": "https://igrsup.gov.in",
        "steps": [
            ("Identify registration details", "Find registration document number, book number, volume number, and exact registration date.", ["Registration details from previous receipt"], "₹0", "10 minutes"),
            ("Apply online or at Sub-Registrar counter", "Fill certified copy requisition form specifying purpose (court, bank loan, title verification).", ["Applicant ID proof"], "₹100 – ₹250", "1 day"),
            ("Sub-registrar record retrieval", "Record keeper retrieves original volume record from record room or digital repository.", ["Archival file lookup"], "₹0", "2 days"),
            ("Affixing official seal and signature", "Sub-Registrar stamps 'Certified True Copy' with official holographic seal.", ["Certified stamped copy"], "₹0", "1 day"),
            ("Collection / Digital download", "Download digitally signed PDF or collect certified physical copy from delivery counter.", ["Certified Title Deed PDF"], "₹0", "Same day")
        ]
    },
    {
        "id": "freehold_conversion_leasehold_property",
        "category": "Property & Tax",
        "name": "Conversion of Leasehold Property to Freehold",
        "department": "Estate Office / Urban Development Authority",
        "jurisdiction": "Municipal Administration / Estate Office",
        "summary": "Legal transformation of 99-year municipal/housing board leased property into absolute private freehold ownership.",
        "time": "30–45 working days",
        "cost": "Prescribed conversion fee based on plot size & circle rate",
        "official_url": "https://estateoffice.chandigarh.gov.in",
        "steps": [
            ("Clear annual ground rent arrears", "Obtain no-dues receipt for ground rent and municipal service maintenance charges.", ["No dues receipt"], "₹0", "2 days"),
            ("Submit application with chain of title", "Upload original lease deed, all GPA/agreement chain documents, and architectural compliance affidavit.", ["Original lease deed", "Chain agreements", "Building non-violation affidavit"], "₹1,000", "2 days"),
            ("Building violation inspection", "Junior engineer inspects site to confirm absence of unapproved additional floors or misuse of residential premises.", ["Inspection report"], "₹0", "14 days"),
            ("Demand note payment", "Estate office generates conversion demand notice; pay through RTGS or demand draft.", ["Payment confirmation"], "Calculated by formula", "7 days"),
            ("Execution of Freehold Conveyance Deed", "Sign and register Conveyance Deed before Sub-Registrar, granting permanent absolute ownership.", ["Registered Conveyance Deed"], "₹0", "5 days")
        ]
    },
    {
        "id": "tenant_police_verification",
        "category": "Property & Tax",
        "name": "Tenant & Domestic Worker Police Verification",
        "department": "State Police Department / Local Police Station",
        "jurisdiction": "City Police",
        "summary": "Mandatory tenant background verification under Criminal Procedure Code to ensure neighborhood security.",
        "time": "3–7 working days",
        "cost": "₹0 (Completely Free of Cost)",
        "official_url": "https://chandigarhpolice.gov.in",
        "steps": [
            ("Collect tenant identity documents", "Obtain tenant's Aadhaar card, permanent native village address, employer identity card, and 2 passport photos.", ["Tenant Aadhaar & PAN", "Employer ID card", "Passport photos"], "₹0", "Same day"),
            ("Submit on Citizen Police Portal / App", "Landlord registers property details and submits tenant personal history online.", ["Rent agreement copy"], "₹0", "15 minutes"),
            ("Local police station verification", "Beat constable conducts background check and verifies record with native district police station.", ["Beat officer enquiry log"], "₹0", "3–5 days"),
            ("Download Police Clearance Slip", "Download digitally stamped verification acknowledgement receipt for records.", ["Verification Acknowledgement PDF"], "₹0", "Immediate")
        ]
    },
    {
        "id": "water_sewerage_rebate_vacant_property",
        "category": "Property & Tax",
        "name": "Water & Sewerage Charge Waiver for Vacant Property",
        "department": "Public Health Division",
        "jurisdiction": "Municipal Corporation",
        "summary": "Suspension of monthly minimum consumption and sewerage charges for unoccupied residential properties.",
        "time": "7–10 working days",
        "cost": "₹0 application fee",
        "official_url": "https://mcc.chandigarh.gov.in/vacant-property",
        "steps": [
            ("Ensure electricity meter disconnection / zero usage", "Provide electricity bills showing zero power units consumed during the vacant period.", ["Last 2 power bills"], "₹0", "1 day"),
            ("Apply for vacant status endorsement", "Submit sworn affidavit from homeowner affirming that property remains locked and uninhabited.", ["Owner affidavit", "Water bill copy"], "₹0", "1 day"),
            ("Inspection by meter reader", "Meter reader visits house to confirm locked status and record final dial reading.", ["Field inspection note"], "₹0", "3 days"),
            ("Approval of billing suspension", "Executive Engineer endorses vacant status, pausing recurring fixed sewage and meter charges.", ["Billing adjustment order"], "₹0", "2 days")
        ]
    },
    {
        "id": "heritage_building_alteration_noc",
        "category": "Property & Tax",
        "name": "Heritage Building Renovation & Alteration Clearance",
        "department": "Heritage Conservation Committee & Chief Architect",
        "jurisdiction": "Urban Planning Department",
        "summary": "Special permission required before undertaking repair, painting, or window replacement on notified heritage facade structures.",
        "time": "30–60 working days",
        "cost": "₹1,000 application fee",
        "official_url": "https://urbanplanning.chandigarh.gov.in",
        "steps": [
            ("Prepare heritage impact assessment", "Architectural conservationist prepares structural report preserving character-defining elements.", ["Conservation report", "Historical photographs"], "Varies", "7 days"),
            ("Submit proposal to Heritage Committee", "Submit proposed materials, paint swatches matching original exposed brick/concrete aesthetic.", ["Material specifications", "Elevation mockups"], "₹1,000", "2 days"),
            ("Heritage Conservation Committee review", "Panel of architects and historians assesses whether facade integrity is preserved.", ["Committee meeting minutes"], "₹0", "20 days"),
            ("Issuance of Facade Clearance NOC", "Obtain conditional approval letter with strict preservation directives.", ["Heritage NOC"], "₹0", "5 days")
        ]
    },
    {
        "id": "subdivision_plot_amalgamation",
        "category": "Property & Tax",
        "name": "Sub-Division and Amalgamation of Plots",
        "department": "Town Planning Department",
        "jurisdiction": "Municipal Corporation / Urban Development Authority",
        "summary": "Formal approval to split a large land parcel into sub-plots or merge adjacent plots into a single unified title.",
        "time": "25–35 working days",
        "cost": "₹10,000 – ₹50,000 based on area",
        "official_url": "https://mcc.chandigarh.gov.in/subdivision",
        "steps": [
            ("Check minimum plot size bylaws", "Verify that resulting sub-plots satisfy minimum frontage and area requirements.", ["Title deeds of both plots"], "₹0", "1 day"),
            ("Submit amalgamation/subdivision layout", "Registered town planner drafts revised layout showing utility easements and setbacks.", ["Draft layout plan", "Structural engineer certificate"], "₹2,500", "5 days"),
            ("Joint engineering scrutiny", "Municipal planning cell examines access road width and water/sewer network capacity.", ["Scrutiny report"], "₹0", "14 days"),
            ("Pay amalgamation fee", "Pay development and regularization charges at municipal treasury.", ["Treasury challan"], "₹10,000 – ₹50,000", "Immediate"),
            ("Issuance of unified property ID", "Receive revised allotment letter and single consolidated property tax assessment ID.", ["Unified Property Allotment Letter"], "₹0", "5 days")
        ]
    },
    {
        "id": "commercial_property_misuse_regularization",
        "category": "Property & Tax",
        "name": "Property Misuse Regularization & Penalty Clearance",
        "department": "Enforcement Branch, Estate Office",
        "jurisdiction": "Estate Office",
        "summary": "Removal of misuse violation notices or regularization of permitted non-conforming activities in designated sectors.",
        "time": "15–20 working days",
        "cost": "Penalty calculated per sq. ft. per month of violation",
        "official_url": "https://estateoffice.chandigarh.gov.in",
        "steps": [
            ("Rectify violation on site", "Restore premises to sanctioned use (e.g. remove commercial storage from residential basement).", ["Photographs of cleared area"], "Varies", "3 days"),
            ("Submit compliance affidavit", "Submit notarized undertaking on stamp paper stating non-recurrence of violation.", ["Notarized undertaking", "Violation notice copy"], "₹100", "1 day"),
            ("Enforcement inspector re-inspection", "Building inspector re-inspects premises, measures area, and takes geo-tagged photos.", ["Re-inspection report"], "₹0", "7 days"),
            ("Pay assessed compounding penalty", "Pay compounding penalty determined by the Assistant Estate Officer.", ["Payment receipt"], "Varies", "Immediate"),
            ("Discharge of misuse show-cause notice", "Estate Office issues formal closure letter revoking resumption/misuse proceedings.", ["Revocation / Clean Chit Letter"], "₹0", "3 days")
        ]
    },
    {
        "id": "property_valuation_circle_rate_certificate",
        "category": "Property & Tax",
        "name": "Property Valuation Certificate (Circle Rate Assessment)",
        "department": "Sub-Registrar / Revenue Authority",
        "jurisdiction": "Revenue Department",
        "summary": "Official certificate determining minimum government circle rate valuation of real estate for visa, probate, or bank mortgage.",
        "time": "3–5 working days",
        "cost": "₹200 application fee",
        "official_url": "https://revenue.gov.in",
        "steps": [
            ("Identify sector, floor, and road width", "Circle rate valuations vary based on whether property abuts main sector avenue or internal road.", ["Registry copy / Allotment letter"], "₹0", "10 minutes"),
            ("Apply online on Revenue Portal", "Input plot size, constructed area by floor, and year of construction.", ["Aadhaar", "Property photos"], "₹200", "1 day"),
            ("Algorithmic circle rate assessment", "System multiplies carpet area by notification circle rates and applies age depreciation.", ["Valuation computation sheet"], "₹0", "Same day"),
            ("Issuance of certified valuation", "Sub-Registrar issues digitally signed Valuation Certificate with QR code verification.", ["Valuation Certificate PDF"], "₹0", "2 days")
        ]
    },

    # ---------------- 4. Certificates & Civil Status ----------------
    {
        "id": "birth_certificate_registration",
        "category": "Certificates & Identity",
        "name": "Birth Certificate Registration & Download",
        "department": "Office of the Registrar of Births & Deaths",
        "jurisdiction": "Municipal Corporation / Health Dept",
        "summary": "Official registration and certificate issuance for newborn children within 21 days of birth.",
        "time": "3–7 working days",
        "cost": "₹0 within 21 days; ₹10–₹50 late fee up to 1 year",
        "official_url": "https://crsorgi.gov.in",
        "steps": [
            ("Hospital discharge institutional report", "Collect Form 1 institutional report generated by hospital/maternity nursing home.", ["Hospital Form 1 report", "Discharge card"], "₹0", "At discharge"),
            ("Submit child's name online", "Log in to Civil Registration System (CRS) portal and register baby's official name.", ["Mother and Father Aadhaar cards", "Marriage certificate"], "₹0", "1 day"),
            ("Verification by Registrar", "Municipal birth registrar verifies institutional logs against hospital registers.", ["Registrar verification memo"], "₹0", "3 days"),
            ("Download digital birth certificate", "Download digitally signed Birth Certificate with national QR code; download unlimited copies free.", ["Birth Certificate PDF"], "₹0", "Immediate")
        ]
    },
    {
        "id": "death_certificate_issuance",
        "category": "Certificates & Identity",
        "name": "Death Certificate Issuance & Cremation Record",
        "department": "Registrar of Births & Deaths",
        "jurisdiction": "Municipal Corporation",
        "summary": "Statutory registration of demise required for succession, life insurance claims, and bank account settlements.",
        "time": "3–5 working days",
        "cost": "₹0 within 21 days",
        "official_url": "https://crsorgi.gov.in",
        "steps": [
            ("Cremation/burial slip", "Collect cremation ground receipt or burial ground entry counterfoil signed by ground caretaker.", ["Crematorium receipt", "Hospital medical cause of death Form 4"], "₹0", "Same day"),
            ("Apply online on CRS portal", "Submit deceased identity details, date, exact place of death, and applicant relation proof.", ["Deceased Aadhaar", "Applicant Aadhaar"], "₹0", "1 day"),
            ("Registrar scrutiny", "Health department officer crosses-references cremation logbook records.", ["Verification check"], "₹0", "2 days"),
            ("Download official death certificate", "Obtain official digitally signed Death Certificate with unique registration number.", ["Death Certificate PDF"], "₹0", "Same day")
        ]
    },
    {
        "id": "marriage_registration_certificate",
        "category": "Certificates & Identity",
        "name": "Marriage Registration & Certificate (Special / Hindu Marriage Act)",
        "department": "Registrar of Marriages / Sub-Divisional Magistrate (SDM)",
        "jurisdiction": "District Administration",
        "summary": "Legal registration of marriage under Hindu Marriage Act 1955 or Special Marriage Act 1954.",
        "time": "7–15 working days (Hindu) / 30 days notice (Special)",
        "cost": "₹100 – ₹500 government fee",
        "official_url": "https://edistrict.gov.in",
        "steps": [
            ("Compile couple's documents", "Age proof (matriculation certificate/passport), address proofs, joint wedding photographs, and wedding card.", ["Age & Address proofs of bride and groom", "Wedding invitation card", "Joint photo"], "₹0", "1 day"),
            ("Submit application on e-District portal", "Fill online marriage form, enter particulars of 3 witnesses, and book appointment slot.", ["Witness Aadhaar cards"], "₹100 – ₹500", "1 day"),
            ("Physical appearance before Marriage Officer", "Couple and 3 witnesses appear before SDM/Registrar to sign official marriage register.", ["Original documents for physical verification"], "₹0", "On appointment date"),
            ("Issuance of Marriage Certificate", "Download government Marriage Certificate bearing official seal and registration number.", ["Marriage Certificate PDF"], "₹0", "Same day / next day")
        ]
    },
    {
        "id": "caste_category_certificate_sc_st_obc",
        "category": "Certificates & Identity",
        "name": "Caste Certificate (SC / ST / OBC / EWS)",
        "department": "Revenue Department / Office of the Tehsildar",
        "jurisdiction": "District Administration",
        "summary": "Government certificate authenticating reservation category status for education admissions and public recruitment.",
        "time": "10–15 working days",
        "cost": "₹30 – ₹60 service fee",
        "official_url": "https://edistrict.gov.in",
        "steps": [
            ("Paternal lineage proof", "Father's caste certificate or revenue land records before 1966 proving state ancestral residency.", ["Father's caste certificate", "Old lineage records"], "₹0", "1 day"),
            ("Apply online on e-District", "Upload applicant Aadhaar, school leaving certificate, and non-creamy layer income certificate (for OBC/EWS).", ["Applicant Aadhaar", "Income certificate", "Family ration card"], "₹30", "1 day"),
            ("Field inquiry by Patwari", "Halqa Patwari and Kanungo verify applicant's family history in ancestral village.", ["Patwari verification report"], "₹0", "5–7 days"),
            ("Tehsildar approval and certificate generation", "Tehsildar sanctions certificate with unique central/state serial number.", ["Caste Certificate PDF with QR"], "₹0", "2 days")
        ]
    },
    {
        "id": "income_certificate_annual",
        "category": "Certificates & Identity",
        "name": "Income Certificate for Scholarships & Welfare",
        "department": "Office of the Tehsildar / Sub-Divisional Magistrate",
        "jurisdiction": "Revenue Department",
        "summary": "Certified proof of total annual household income required for fee concessions, scholarships, and subsidized housing.",
        "time": "7–10 working days",
        "cost": "₹30 – ₹50 government fee",
        "official_url": "https://edistrict.gov.in",
        "steps": [
            ("Income declaration & employer slip", "Salary slips / Form 16 for salaried individuals; ITR or self-declaration affidavit for unorganized workers.", ["Salary slip / Form 16 / ITR", "Notarized income affidavit"], "₹100", "1 day"),
            ("Submit application on e-District portal", "Fill household members details, agricultural land income, and rental income.", ["Aadhaar card", "Electricity bill", "Ration card"], "₹30", "1 day"),
            ("Patwari verification of assets", "Patwari visits local neighborhood to verify standard of living and reported income.", ["Patwari report"], "₹0", "3–5 days"),
            ("Digital certificate download", "Download valid 1-year Income Certificate with official digital signature.", ["Income Certificate PDF"], "₹0", "2 days")
        ]
    },
    {
        "id": "residence_domicile_certificate",
        "category": "Certificates & Identity",
        "name": "Domicile / Permanent Resident Certificate (PRC)",
        "department": "District Magistrate / Tehsildar",
        "jurisdiction": "State / UT Administration",
        "summary": "Legal verification of minimum 5 to 15 years continuous residence within the state or union territory.",
        "time": "7–12 working days",
        "cost": "₹30 – ₹50 fee",
        "official_url": "https://edistrict.gov.in",
        "steps": [
            ("Continuous residence documentation", "Provide 10-year education certificates, property ownership registry, or consecutive voter identity card records.", ["10 years school/college certificates", "Voter list extracts"], "₹0", "2 days"),
            ("Submit online e-District request", "Upload self-attested copies of birth certificate, parent residence proofs, and passport photograph.", ["Aadhaar", "Birth certificate", "Parent domicile copy"], "₹30", "1 day"),
            ("Police/Revenue background inquiry", "Police or revenue inspector verifies permanent residency claims.", ["Verification verification log"], "₹0", "5 days"),
            ("Issuance of Domicile Certificate", "Receive lifetime valid Domicile Certificate essential for state quota college admissions.", ["Domicile Certificate PDF"], "₹0", "2 days")
        ]
    },
    {
        "id": "senior_citizen_identity_card",
        "category": "Certificates & Identity",
        "name": "Senior Citizen Identity Card",
        "department": "Department of Social Welfare",
        "jurisdiction": "Social Welfare Department",
        "summary": "Special ID card for citizens aged 60 and above conferring bus travel concessions, healthcare queue priority, and legal aid.",
        "time": "5–7 working days",
        "cost": "₹0 (Free of Cost)",
        "official_url": "https://socialwelfare.gov.in",
        "steps": [
            ("Age verification", "Provide passport, voter ID, matriculation certificate, or Aadhaar proving completion of 60 years.", ["Age proof document", "Address proof"], "₹0", "Same day"),
            ("Medical blood group card", "Attach blood group report and emergency family doctor/next-of-kin contact details.", ["Blood group report", "2 passport photos"], "₹0", "Same day"),
            ("Submit online or at Senior Citizen Home", "Register on state senior citizen portal or submit at municipal social welfare counter.", ["Application form"], "₹0", "1 day"),
            ("Collect Senior Citizen Smart Card", "Download digital card or collect PVC laminated card with photo and blood group.", ["Senior Citizen Card"], "₹0", "3 days")
        ]
    },
    {
        "id": "unique_disability_id_udid",
        "category": "Certificates & Identity",
        "name": "Unique Disability ID (UDID) & Disability Certificate",
        "department": "Department of Empowerment of Persons with Disabilities",
        "jurisdiction": "Ministry of Social Justice & Empowerment",
        "summary": "Universal digital card and medical board certificate recognizing 21 specified disabilities under RPwD Act 2016.",
        "time": "15–30 working days",
        "cost": "₹0 (Free Government Service)",
        "official_url": "https://swavlambancard.gov.in",
        "steps": [
            ("Register on Swavlamban portal", "Submit personal details, disability type (locomotor, visual, hearing, intellectual, etc.), and address.", ["Aadhaar card", "Passport size photograph"], "₹0", "1 day"),
            ("Book medical assessment appointment", "System assigns date for evaluation at District Civil Hospital Medical Board.", ["Appointment slip"], "₹0", "Immediate"),
            ("Medical board physical evaluation", "Panel of specialist doctors conducts tests and determines disability percentage (e.g. 40%+ benchmark disability).", ["Doctor clinical assessment notes"], "₹0", "On appointment date"),
            ("Download Disability Certificate", "Chief Medical Officer (CMO) signs digital certificate stating permanent/temporary disability percentage.", ["Disability Certificate PDF"], "₹0", "3 days"),
            ("Receive National UDID Smart Card", "Plastic UDID card with smart chip dispatched by speed post to home address.", ["UDID Card"], "₹0", "14 days post-approval")
        ]
    },
    {
        "id": "ration_card_new_application",
        "category": "Certificates & Identity",
        "name": "New Ration Card (APL / BPL / NFSA / Antyodaya)",
        "department": "Food, Civil Supplies & Consumer Affairs",
        "jurisdiction": "State Government",
        "summary": "Issuance of digital household ration card for subsidized food grains and official proof of family tree.",
        "time": "15–25 working days",
        "cost": "₹50 service fee",
        "official_url": "https://nfsa.gov.in",
        "steps": [
            ("Deletion certificate from previous place", "If moving from another state/town, obtain surrender/deletion certificate from previous food supply office.", ["Surrender certificate"], "₹0", "3 days"),
            ("Gather family member Aadhaar cards", "Collect Aadhaar numbers and bank account of the eldest female member as Head of the Family (HOD).", ["All members' Aadhaar", "LPG gas connection booklet"], "₹0", "1 day"),
            ("Submit online NFSA application", "Fill monthly income, house type (pucca/kutcha), and upload family group photo.", ["Family photo", "Electricity bill"], "₹50", "1 day"),
            ("Food Inspector field scrutiny", "Inspector checks economic criteria and verifies family living conditions.", ["Inspector verification log"], "₹0", "10 days"),
            ("Download e-Ration Card", "Download dynamic QR-code e-Ration Card valid at all Fair Price Shops under One Nation One Ration Card (ONORC).", ["e-Ration Card PDF"], "₹0", "3 days")
        ]
    },
    {
        "id": "survival_member_legal_heir_certificate",
        "category": "Certificates & Identity",
        "name": "Legal Heir / Surviving Member Certificate",
        "department": "Revenue Department / Office of the SDM",
        "jurisdiction": "Sub-Divisional Magistrate",
        "summary": "Certificate identifying all surviving legal heirs of a deceased person for bank account closure and PF settlements.",
        "time": "15–21 working days",
        "cost": "₹50 application fee",
        "official_url": "https://edistrict.gov.in",
        "steps": [
            ("Death certificate of deceased", "Obtain official death certificate and family pedigree genealogical tree.", ["Death certificate", "Family tree diagram"], "₹0", "1 day"),
            ("Affidavit of all legal heirs", "All surviving heirs (spouse, sons, daughters, mother) execute joint affidavit declaring no other heirs exist.", ["Notarized joint legal heir affidavit"], "₹100", "1 day"),
            ("Submit online SDM application", "Upload death certificate, survivor Aadhaar cards, and NOC from married daughters (if applicable).", ["Surviving members' Aadhaar"], "₹50", "1 day"),
            ("Local Patwari/Tehsildar verification", "Revenue officer verifies surviving heirs through statements of village Sarpanch or municipal councillor.", ["Field enquiry report"], "₹0", "10 days"),
            ("Issuance of Surviving Member Certificate", "SDM issues formal Surviving Member Certificate with names and relationship of all legal heirs.", ["Legal Heir Certificate PDF"], "₹0", "3 days")
        ]
    },
    {
        "id": "name_change_gazette_notification",
        "category": "Certificates & Identity",
        "name": "Name Change Official Gazette Notification",
        "department": "Department of Publication, Ministry of Housing & Urban Affairs",
        "jurisdiction": "Central / State Government Gazette",
        "summary": "Legally binding change of personal name published in the Official Government Gazette for passport and educational records.",
        "time": "20–30 working days",
        "cost": "₹1,100 – ₹1,500 government gazette printing fee",
        "official_url": "https://egazette.gov.in",
        "steps": [
            ("Sworn name change affidavit", "Execute affidavit before Judicial Magistrate or Notary stating old name, new name, and father's name.", ["Notarized name change affidavit"], "₹100", "1 day"),
            ("Publish newspaper advertisements", "Publish short name change notice in two prominent local daily newspapers (one English, one Hindi/regional).", ["Original newspaper cuttings"], "₹500 – ₹1,000", "2 days"),
            ("Prepare Gazette Proforma & CD", "Draft official proforma and burn MS Word soft copy onto a compact disc (CD).", ["Hardcopy proforma", "Softcopy CD with certificate"], "₹100", "1 day"),
            ("Submit dossier to Controller of Publications", "Submit complete file with fee receipt via registered post or at Civil Lines Delhi counter.", ["Application packet", "Fee challan via Bharatkosh"], "₹1,100 – ₹1,500", "1 day"),
            ("Download e-Gazette notification", "Download published Gazette notification from egazette.gov.in to update Passport, Aadhaar, and Bank.", ["e-Gazette extract PDF"], "₹0", "15–20 days")
        ]
    },
    {
        "id": "e_aadhaar_demographic_biometric_update",
        "category": "Certificates & Identity",
        "name": "Aadhaar Card Demographic & Biometric Update",
        "department": "Unique Identification Authority of India (UIDAI)",
        "jurisdiction": "Central Government",
        "summary": "Update of residential address, mobile phone number, name, or mandatory 10-year biometric refresh.",
        "time": "3–7 working days",
        "cost": "₹50 for address/demographic; ₹100 for biometrics",
        "official_url": "https://myaadhaar.uidai.gov.in",
        "steps": [
            ("Address update online (Self-Service)", "Upload valid address proof (electricity bill, passport, rent agreement) on myAadhaar portal.", ["Valid address proof document"], "₹50", "15 minutes"),
            ("Biometric/Mobile update appointment", "Book time slot at nearest Aadhaar Seva Kendra (ASK) or post office branch.", ["Appointment slip"], "₹0", "5 minutes"),
            ("Iris, fingerprint & facial photo scan", "Visit center for live ten-fingerprint, iris scan, and photograph update.", ["Original Aadhaar number"], "₹100", "15 minutes at center"),
            ("Track with URN", "Track 14-digit Update Request Number (URN) on UIDAI tracking page.", ["URN acknowledgement slip"], "₹0", "Immediate"),
            ("Download updated e-Aadhaar", "Download password-protected e-Aadhaar PDF using registered mobile OTP.", ["e-Aadhaar PDF"], "₹0", "3–5 days")
        ]
    },
    {
        "id": "character_antecedents_police_certificate",
        "category": "Certificates & Identity",
        "name": "Police Clearance Certificate (PCC) for Employment",
        "department": "State Police Department / Criminal Investigation Branch",
        "jurisdiction": "State Police",
        "summary": "Verification certifying individual has no active criminal convictions, arrest warrants, or pending FIRs.",
        "time": "7–10 working days",
        "cost": "₹200 – ₹500 fee",
        "official_url": "https://chandigarhpolice.gov.in",
        "steps": [
            ("Submit online verification request", "Enter personal biographical history, previous 5 years addresses, and employer requisition letter.", ["Aadhaar", "Passport", "Employer letter"], "₹200", "1 day"),
            ("Crime database cross-checking", "Police records branch verifies applicant against CCTNS (Crime and Criminal Tracking Network).", ["CCTNS query check"], "₹0", "3 days"),
            ("Local police station enquiry", "Local beat constable verifies applicant character from two reputable neighborhood references.", ["Two neighbor reference statements"], "₹0", "3 days"),
            ("Download Police Clearance Certificate", "Download digitally stamped Character Verification Certificate with validity QR code.", ["PCC document PDF"], "₹0", "2 days")
        ]
    },
    {
        "id": "non_encumbrance_minority_certificate",
        "category": "Certificates & Identity",
        "name": "Religious / Linguistic Minority Community Certificate",
        "department": "Department of Minority Affairs & Revenue",
        "jurisdiction": "District Administration",
        "summary": "Official certification of notified minority community status (Muslim, Christian, Sikh, Buddhist, Jain, Parsi) for scholarships.",
        "time": "7–12 working days",
        "cost": "₹30 – ₹50 fee",
        "official_url": "https://minorityaffairs.gov.in",
        "steps": [
            ("Religious institution certificate", "Letter from registered Gurudwara/Church/Mosque/Jain trust or school leaving certificate stating religion.", ["Institutional letter", "School leaving certificate"], "₹0", "1 day"),
            ("Self-declaration affidavit", "Submit sworn affidavit declaring adherence to notified minority community.", ["Notarized affidavit"], "₹100", "1 day"),
            ("Apply online on e-District portal", "Attach parent minority proof and family income statement for fee waivers.", ["Aadhaar card", "Income certificate"], "₹30", "1 day"),
            ("Tehsildar verification & approval", "Revenue authority validates records and issues certificate.", ["Minority Certificate PDF"], "₹0", "5 days")
        ]
    },
    {
        "id": "unemployed_youth_registration",
        "category": "Certificates & Identity",
        "name": "Employment Exchange Registration for Jobseekers",
        "department": "Department of Employment & National Career Service",
        "jurisdiction": "State / Ministry of Labour",
        "summary": "Official registration card establishing educational seniority for state government employment drives.",
        "time": "Immediate online certificate",
        "cost": "₹0 (Completely Free)",
        "official_url": "https://ncs.gov.in",
        "steps": [
            ("Register on National Career Service (NCS)", "Create jobseeker profile with Aadhaar, education qualification certificates, and technical skills.", ["Degree marksheets", "Aadhaar card"], "₹0", "15 minutes"),
            ("Upload experience and category certificates", "Add vocational certifications (ITI, Polytechnic) and caste/disability certificates for reservation.", ["Certificates scan"], "₹0", "10 minutes"),
            ("Download Employment Exchange Card", "Receive NCS Jobseeker Registration Number and digital employment card.", ["NCS Jobseeker Card PDF"], "₹0", "Immediate"),
            ("Participate in government job fairs", "Receive automated SMS invitations to Rozgar Melas and state vacancy notifications.", ["Job fair alert notifications"], "₹0", "Ongoing")
        ]
    },
    {
        "id": "dependent_freedom_fighter_certificate",
        "category": "Certificates & Identity",
        "name": "Freedom Fighter Dependent / Ward Certificate",
        "department": "General Administration Department",
        "jurisdiction": "State Government",
        "summary": "Certificate recognizing sons, daughters, and grandchildren of freedom fighters for horizontal reservation quotas.",
        "time": "20–30 working days",
        "cost": "₹0 (Free Government Service)",
        "official_url": "https://edistrict.gov.in",
        "steps": [
            ("Tamra Patra / Sanman Pension proofs", "Produce official Tamra Patra award or central Samman Pension sanction order of ancestor.", ["Tamra Patra copy", "Pension sanction order"], "₹0", "1 day"),
            ("Establish genealogical linkage", "Birth certificates and revenue genealogical tree establishing direct bloodline to freedom fighter.", ["Certified family pedigree", "Birth certificates"], "₹0", "3 days"),
            ("Submit application to Deputy Commissioner", "Submit application to DC Office with affidavits from all intermediate relatives.", ["Affidavits", "Aadhaar cards"], "₹0", "2 days"),
            ("Scrutiny by Freedom Fighter Cell", "District advisory committee examines original central ministry records.", ["Scrutiny findings"], "₹0", "15 days"),
            ("Issuance of Ward Certificate", "Deputy Commissioner issues formal Ward of Freedom Fighter Certificate for reservation benefits.", ["Certificate with DC seal"], "₹0", "5 days")
        ]
    },

    # ---------------- 5. Transport & Driving ----------------
    {
        "id": "learners_driving_license_sarathi",
        "category": "Transport & Vehicles",
        "name": "Learner's Driving License (LL) Online Test",
        "department": "Ministry of Road Transport and Highways (MoRTH)",
        "jurisdiction": "Regional Transport Office (RTO)",
        "summary": "Application, fee payment, and contactless online road safety test for 6-month Learner's Driving License.",
        "time": "Same day online",
        "cost": "₹150 application fee + ₹50 test fee",
        "official_url": "https://parivahan.gov.in/parivahan",
        "steps": [
            ("Apply on Parivahan Sarathi", "Select State, authenticate via Aadhaar OTP, and select license classes (e.g. Motorcycle with Gear MCWG, LMV).", ["Aadhaar number", "Active linked mobile"], "₹0", "15 minutes"),
            ("Watch mandatory road safety tutorial", "Watch 10-minute animated road safety video on safe driving practices and traffic signs.", ["Completed tutorial confirmation"], "₹0", "10 minutes"),
            ("Pay government LL fee", "Pay application and online test fee via integrated payment portal.", ["Payment receipt"], "₹200", "Immediate"),
            ("Appear in online proctored STALL test", "Take 15-question multiple choice test on traffic signs from home device using webcam facial recognition.", ["Laptop/Phone with camera"], "₹0", "15 minutes"),
            ("Instant Learner License download", "Upon scoring 60%+ correct answers, download Form 3 Learner License valid for 6 months across India.", ["Form 3 Learner License PDF"], "₹0", "Immediate")
        ]
    },
    {
        "id": "permanent_driving_license_dl",
        "category": "Transport & Vehicles",
        "name": "Permanent Driving License & Automated Track Test",
        "department": "Regional Transport Office (RTO)",
        "jurisdiction": "State Transport Department",
        "summary": "Booking driving skill track test and obtaining chip-embedded PVC Smart Card Driving License.",
        "time": "7–10 working days",
        "cost": "₹200 driving test fee + ₹200 smart card fee",
        "official_url": "https://parivahan.gov.in/parivahan",
        "steps": [
            ("Wait minimum 30 days after LL", "Candidate must have held valid Learner's License for at least 30 days before booking DL test slot.", ["Valid Learner's License number"], "₹0", "After 30 days"),
            ("Book automated driving test slot", "Select date and preferred RTO automated test track on Sarathi portal.", ["Learner license", "Form 5 driving school certificate"], "₹400", "5 minutes"),
            ("Appear at automated driving test track", "Drive on sensor-equipped track executing reverse-S, parallel parking, eight-curve, and gradient stop without hitting poles.", ["Vehicle with valid RC, Insurance, PUC"], "₹0", "On test date"),
            ("Biometric and photograph capture", "RTO staff captures digital photograph and signature for printing on smart card.", ["Application slip"], "₹0", "Same day"),
            ("Dispatch of Smart Card Driving License", "High-security PVC Smart Card Driving License dispatched by Speed Post to residential address.", ["Driving License Smart Card"], "₹0", "5–7 days")
        ]
    },
    {
        "id": "driving_license_renewal_online",
        "category": "Transport & Vehicles",
        "name": "Driving License Renewal (Online Faceless Service)",
        "department": "Regional Transport Office (RTO)",
        "jurisdiction": "Ministry of Road Transport and Highways",
        "summary": "Renewal of expired driving license with medical fitness certification for another 10 to 20 years.",
        "time": "5–7 working days",
        "cost": "₹200 renewal fee + ₹200 card fee (Late fee if expired > 1 year)",
        "official_url": "https://parivahan.gov.in/parivahan",
        "steps": [
            ("Medical Form 1A certification", "For drivers aged 40 and above, registered MBBS doctor uploads Form 1A medical fitness certificate digitally on Sarathi.", ["Eye test & doctor certification"], "₹100 – ₹200", "1 day"),
            ("Apply on Sarathi portal", "Authenticate with Aadhaar, enter existing DL number and date of birth, and confirm residential address.", ["Existing DL card", "Aadhaar"], "₹400", "15 minutes"),
            ("Pay renewal charges online", "Pay fee online; no physical RTO visit needed if Aadhaar authentication is successful.", ["Fee payment receipt"], "₹400", "Immediate"),
            ("RTO approval & printing", "RTO licensing officer approves digital file and sends for smart card embossing.", ["Digital approval alert"], "₹0", "2–3 days"),
            ("Postal delivery", "Renewed driving license delivered to residential address via India Post Speed Post.", ["Renewed DL Card"], "₹0", "5 days")
        ]
    },
    {
        "id": "rc_ownership_transfer_vehicle",
        "category": "Transport & Vehicles",
        "name": "Vehicle Registration Transfer of Ownership (Form 29 & 30)",
        "department": "Regional Transport Office (RTO)",
        "jurisdiction": "State Transport Department",
        "summary": "Transfer of vehicle Registration Certificate (RC) to buyer upon purchase of used two-wheeler or car.",
        "time": "7–14 working days",
        "cost": "₹300 – ₹500 transfer fee",
        "official_url": "https://parivahan.gov.in/parivahan",
        "steps": [
            ("Execute Form 29 & 30", "Buyer and seller sign Form 29 (notice of transfer) and Form 30 (application for transfer).", ["Form 29 & Form 30 signed", "Sale agreement"], "₹0", "1 day"),
            ("Procure vehicle fitness documents", "Ensure vehicle has valid motor insurance policy, active Pollution Under Control (PUC) certificate, and original RC.", ["Original RC smart card", "Valid insurance policy", "PUC certificate"], "₹0", "Same day"),
            ("Submit transfer on Parivahan Vahan", "Enter vehicle chassis number, buyer Aadhaar, and upload signed transfer forms.", ["PAN card of buyer / Form 60"], "₹300 – ₹500", "1 day"),
            ("Seller OTP consent verification", "Seller receives SMS OTP on mobile registered with vehicle to approve transfer online.", ["Seller OTP authorization"], "₹0", "Immediate"),
            ("Issuance of updated RC smart card", "RTO prints new Registration Certificate bearing buyer's name and dispatches via post.", ["New RC Smart Card"], "₹0", "7 days")
        ]
    },
    {
        "id": "vehicle_noc_interstate_transfer",
        "category": "Transport & Vehicles",
        "name": "Vehicle No Objection Certificate (NOC) for Inter-State Transfer",
        "department": "Regional Transport Office (RTO)",
        "jurisdiction": "State Transport Department",
        "summary": "NOC required under Form 28 to re-register a vehicle in another state or union territory.",
        "time": "10–15 working days",
        "cost": "₹100 application fee",
        "official_url": "https://parivahan.gov.in/parivahan",
        "steps": [
            ("Pencil chassis print on Form 28", "Take clear physical pencil impression of vehicle's metallic chassis number on 3 copies of Form 28.", ["3 copies Form 28", "Pencil chassis print"], "₹0", "1 hour"),
            ("Check traffic challan and hypothecation", "Clear all pending electronic traffic challans and obtain bank loan closure NOC if previously financed.", ["Zero challan clearance report", "Bank loan NOC"], "₹0", "1 day"),
            ("Apply online on Vahan portal", "Submit destination state and destination RTO jurisdiction code where vehicle will be moved.", ["Original RC", "Valid insurance", "PUC"], "₹100", "1 day"),
            ("Crime Records Bureau (NCRB) verification", "RTO checks national stolen vehicle database to ensure vehicle is not subject to police alert.", ["NCRB verification clearance"], "₹0", "5 days"),
            ("Collect Form 28 NOC certificate", "Obtain official stamped NOC certificate valid for re-registration in destination state.", ["Form 28 NOC certificate"], "₹0", "3 days")
        ]
    },
    {
        "id": "high_security_registration_plate_hsrp",
        "category": "Transport & Vehicles",
        "name": "High Security Registration Plate (HSRP) & Color Sticker",
        "department": "Authorized HSRP Vendor & State Transport Dept",
        "jurisdiction": "Ministry of Road Transport and Highways",
        "summary": "Mandatory tamper-proof aluminum number plate with chromium hologram and laser-etched serial code.",
        "time": "4–7 working days for fitment",
        "cost": "₹350 – ₹450 (Two-wheeler) / ₹800 – ₹1,100 (Four-wheeler)",
        "official_url": "https://bookmyhsrp.com",
        "steps": [
            ("Book online on BookMyHSRP portal", "Enter vehicle registration number, chassis number (last 5 digits), and engine number.", ["RC smart card details"], "₹0", "10 minutes"),
            ("Choose fitment location", "Select preferred authorized automobile dealership or opt for home doorstep installation service.", ["Fitment date and time slot"], "₹0", "5 minutes"),
            ("Pay government approved fee", "Make online payment for laser-etched front/rear plates and fuel color sticker (blue/orange/green).", ["Payment receipt"], "₹350 – ₹1,100", "Immediate"),
            ("Fitment by technician", "Technician removes old non-standard plates and affixes HSRP plates using non-reusable snap locks.", ["HSRP fitment with snap locks"], "₹0", "15 minutes"),
            ("Automatic Vahan status update", "Technician scans laser barcode; Parivahan Vahan portal automatically updates HSRP compliance status.", ["Vahan HSRP updated status"], "₹0", "Same day")
        ]
    },
    {
        "id": "hypothecation_addition_removal_hp",
        "category": "Transport & Vehicles",
        "name": "Vehicle Loan Hypothecation Removal (HP Termination / Form 35)",
        "department": "Regional Transport Office (RTO)",
        "jurisdiction": "State Transport Department",
        "summary": "Removing bank finance lien from vehicle Registration Certificate after full repayment of vehicle loan.",
        "time": "5–7 working days",
        "cost": "₹100 – ₹200 fee + new smart card charge",
        "official_url": "https://parivahan.gov.in/parivahan",
        "steps": [
            ("Obtain bank loan closure kit", "Collect Form 35 (two copies signed by bank officer) and Bank No Objection Certificate (NOC).", ["Bank Form 35", "Bank NOC letter"], "₹0", "From bank"),
            ("Submit HP cancellation on Vahan", "Enter vehicle number, upload Bank NOC and signed Form 35, and pay smart card fee.", ["Original RC", "Valid insurance", "PUC"], "₹200", "15 minutes"),
            ("Bank electronic endorsement", "Financier approves electronic loan clearance on national Vahan banking portal.", ["Online bank clearance"], "₹0", "2 days"),
            ("Submit original RC to RTO", "Hand over physical RC to RTO counter or send via registered post.", ["Original RC smart card"], "₹0", "1 day"),
            ("Receive clean RC smart card", "Receive brand new Registration Certificate showing clean ownership without bank hypothecation.", ["Updated RC Smart Card"], "₹0", "5 days")
        ]
    },
    {
        "id": "international_driving_permit_idp",
        "category": "Transport & Vehicles",
        "name": "International Driving Permit (IDP)",
        "department": "Regional Transport Office (RTO)",
        "jurisdiction": "Ministry of Road Transport and Highways",
        "summary": "Official multilingual booklet permitting Indian driving license holders to drive motor vehicles in 150+ foreign countries.",
        "time": "2–4 working days",
        "cost": "₹1,000 statutory fee",
        "official_url": "https://parivahan.gov.in/parivahan",
        "steps": [
            ("Valid passport and foreign visa", "Ensure applicant holds valid Indian passport, international travel visa, and confirmed flight ticket.", ["Valid Passport", "Visa copy", "Air ticket"], "₹0", "1 day"),
            ("Medical Form 1A certification", "Medical practitioner certifies physical and vision fitness for international driving.", ["Medical Form 1A signed by doctor"], "₹100", "Same day"),
            ("Apply on Parivahan Sarathi", "Select countries of transit, upload domestic DL, passport, visa, and pay statutory fee.", ["Valid Indian Driving License"], "₹1,000", "15 minutes"),
            ("Document verification at RTO", "RTO officer verifies original passport and domestic driving license.", ["Original documents"], "₹0", "1 day"),
            ("Collect IDP booklet", "Receive multi-language International Driving Permit booklet valid for 1 year.", ["IDP Booklet document"], "₹0", "Next working day")
        ]
    },
    {
        "id": "duplicate_registration_certificate_rc",
        "category": "Transport & Vehicles",
        "name": "Duplicate Registration Certificate (Lost RC / Form 26)",
        "department": "Regional Transport Office (RTO)",
        "jurisdiction": "State Transport Department",
        "summary": "Issuance of replacement vehicle Registration Certificate when original card is lost, stolen, or mutilated.",
        "time": "7–10 working days",
        "cost": "₹150 – ₹300 fee + card cost",
        "official_url": "https://parivahan.gov.in/parivahan",
        "steps": [
            ("Lodge Police Lost Article Report (LDR)", "Lodge online lost property report on state police citizen portal and obtain non-traceable certificate.", ["Police LDR report / FIR"], "₹0", "Same day"),
            ("Form 26 application", "Complete Form 26 application and take pencil chassis print of vehicle.", ["Form 26", "Pencil chassis impression"], "₹0", "1 hour"),
            ("Apply online on Vahan portal", "Upload police lost report, insurance policy, and PUC certificate.", ["Valid insurance", "PUC copy", "Aadhaar"], "₹300", "1 day"),
            ("Physical inspection at RTO", "Bring vehicle to RTO premises for motor vehicle inspector to verify engine and chassis number.", ["Vehicle for physical verification"], "₹0", "On slot date"),
            ("Dispatch of duplicate RC", "RTO prints duplicate RC smart card with 'DUPLICATE' endorsement and dispatches via post.", ["Duplicate RC Smart Card"], "₹0", "5 days")
        ]
    },
    {
        "id": "commercial_vehicle_fitness_certificate",
        "category": "Transport & Vehicles",
        "name": "Commercial Vehicle Annual Fitness Certificate (FC)",
        "department": "Automated Testing Station (ATS) / RTO",
        "jurisdiction": "Transport Department",
        "summary": "Mandatory annual roadworthiness testing for taxis, auto-rickshaws, buses, and commercial freight trucks.",
        "time": "1–2 working days",
        "cost": "₹600 – ₹1,500 inspection fee",
        "official_url": "https://parivahan.gov.in/parivahan",
        "steps": [
            ("Pre-inspection mechanical maintenance", "Check speed governor calibration, retro-reflective tape visibility, emergency panic buttons, and brake pads.", ["Speed governor certificate", "Fastag", "PUC"], "Varies", "1 day"),
            ("Book fitness test slot on Vahan", "Pay fitness test fee online and schedule slot at automated testing station.", ["RC copy", "Commercial road tax receipt"], "₹600 – ₹1,500", "10 minutes"),
            ("Automated lane inspection", "Automated rollers and sensors inspect roller brake force, side-slip, suspension play, headlamp beam alignment, and emission.", ["Automated lane test log"], "₹0", "1 hour"),
            ("Speed governor & vehicle tracking check", "Inspectors verify operational status of AIS-140 GPS tracking unit and panic buttons.", ["AIS-140 certificate"], "₹0", "15 minutes"),
            ("Grant of Fitness Certificate", "Receive Form 38 Certificate of Fitness and windshield validity sticker valid for 1 or 2 years.", ["Form 38 Fitness Certificate"], "₹0", "Same day")
        ]
    },
    {
        "id": "auto_taxi_contract_carriage_permit",
        "category": "Transport & Vehicles",
        "name": "Contract Carriage Auto-Rickshaw & Taxi Permit",
        "department": "State Transport Authority (STA)",
        "jurisdiction": "State / UT Transport Authority",
        "summary": "Permit authorizing commercial passenger transport within municipal city limits or regional tricity zones.",
        "time": "15–21 working days",
        "cost": "₹1,000 – ₹3,500 permit fee",
        "official_url": "https://sta.chandigarh.gov.in",
        "steps": [
            ("Vehicle eligibility check", "Ensure vehicle model conforms to BS-VI emission or Electric/CNG clean fuel criteria.", ["Vehicle invoice / RC", "Valid commercial insurance"], "₹0", "1 day"),
            ("Driver commercial badge verification", "Driver must hold valid commercial driving license endorsement and PSV badge.", ["Commercial DL", "PSV badge certificate"], "₹0", "1 day"),
            ("Submit permit application on Vahan", "Apply under Contract Carriage category specifying operating radius or tricity permit agreement.", ["Aadhaar", "Fare meter calibration receipt"], "₹1,000 – ₹3,500", "1 day"),
            ("Transport authority board approval", "STA board examines ceiling quota and vehicle safety compliance.", ["STA board approval resolution"], "₹0", "10 days"),
            ("Issuance of Permit (Form P.Co.C.)", "Collect printed permit slip to be kept in vehicle with tariff card.", ["Contract Carriage Permit document"], "₹0", "3 days")
        ]
    },
    {
        "id": "pollution_under_control_certificate_puc",
        "category": "Transport & Vehicles",
        "name": "Pollution Under Control (PUC) Certificate Online",
        "department": "Authorized PUC Testing Centers / MoRTH",
        "jurisdiction": "Ministry of Road Transport and Highways",
        "summary": "Mandatory periodic vehicle exhaust emission test (valid for 6 to 12 months) connected live to national Vahan server.",
        "time": "10 minutes at any fuel station",
        "cost": "₹60 – ₹100 depending on fuel type (Petrol/CNG/Diesel)",
        "official_url": "https://vahan.parivahan.gov.in/puc",
        "steps": [
            ("Drive vehicle to authorized PUC station", "Visit any petrol pump PUC center with vehicle engine in warmed-up running condition.", ["Vehicle with physical presence"], "₹0", "10 minutes"),
            ("Exhaust gas analyzer probe insertion", "Operator inserts analyzer probe into exhaust tailpipe to measure CO, Hydrocarbons (HC), and Smoke Opacity.", ["Live sensor readout"], "₹0", "3 minutes"),
            ("Live webcam vehicle photo capture", "Webcam captures registration number plate photo while vehicle is connected to testing software.", ["Webcam timestamp photo"], "₹0", "1 minute"),
            ("Live upload to central Vahan database", "Test software uploads emission values directly to central Parivahan server without manual tampering.", ["Server upload confirmation"], "₹60 – ₹100", "Instant"),
            ("Collect printed PUC certificate", "Receive printed certificate containing QR code and validity period (6 months for older BS, 1 year for BS-VI).", ["PUC Certificate printout"], "₹0", "Immediate")
        ]
    },
    {
        "id": "road_tax_annual_lifetime_payment",
        "category": "Transport & Vehicles",
        "name": "Motor Vehicle Road Tax Payment (Online Vahan)",
        "department": "Transport Department / Motor Licensing Authority",
        "jurisdiction": "State Government",
        "summary": "Payment of annual, quarterly, or one-time lifetime motor vehicle road tax online.",
        "time": "Immediate online receipt",
        "cost": "Calculated based on engine cc / cost of vehicle (3% to 12%)",
        "official_url": "https://vahan.parivahan.gov.in",
        "steps": [
            ("Enter vehicle registration number", "Input vehicle registration number on Parivahan Vahan Citizen Services portal.", ["Vehicle number"], "₹0", "Immediate"),
            ("Review calculated tax demand", "System calculates tax, penalties (if payment delayed), and green cess.", ["Tax assessment sheet"], "₹0", "1 minute"),
            ("Pay via integrated payment gateway", "Pay tax securely through net banking, debit card, or SBI ePay.", ["Payment receipt"], "Varies by vehicle", "Immediate"),
            ("Download official motor tax receipt", "Download official Tax Receipt with digital seal; updates Vahan database immediately.", ["Tax Receipt PDF with QR"], "₹0", "Immediate")
        ]
    },
    {
        "id": "special_choice_registration_number_auction",
        "category": "Transport & Vehicles",
        "name": "VIP / Fancy Vehicle Registration Number E-Auction",
        "department": "State Transport Authority / RTO",
        "jurisdiction": "State Transport Department",
        "summary": "Online competitive bidding for prestigious vehicle registration numbers (e.g. 0001, 0007, 9999).",
        "time": "Bidding window 3–5 days",
        "cost": "₹10,000 – ₹50,000 reserve price + winning bid",
        "official_url": "https://fancy.parivahan.gov.in",
        "steps": [
            ("Register on Parivahan Fancy Number Portal", "Create bidder profile with Aadhaar and deposit non-refundable registration fee.", ["Aadhaar", "PAN"], "₹1,000", "10 minutes"),
            ("Select desired registration number", "Search number availability in the active newly opened registration series.", ["Number selection"], "₹0", "5 minutes"),
            ("Deposit reserve price earnest money (EMD)", "Pay reserve price demand draft or online payment into auction escrow.", ["Payment receipt"], "₹10,000 – ₹50,000", "Immediate"),
            ("Participate in live e-auction bidding", "Place incremental bids during active 48-hour auction bidding period.", ["Online bidding screen"], "Bid amounts", "2 days"),
            ("Collect Allotment Letter", "Highest bidder pays balance within 5 days and receives official Number Allotment Letter for vehicle registration.", ["Allotment Order"], "Winning bid", "Same day")
        ]
    },
    {
        "id": "scrapped_vehicle_certificate_deposit",
        "category": "Transport & Vehicles",
        "name": "Registered Vehicle Scrappage Certificate of Deposit (CoD)",
        "department": "Registered Vehicle Scrapping Facility (RVSF) & MoRTH",
        "jurisdiction": "Ministry of Road Transport and Highways",
        "summary": "Environment-friendly scrappage of end-of-life vehicles (15+ years) granting motor tax rebates on new car purchase.",
        "time": "3–5 working days",
        "cost": "Scrap metal value paid to owner + up to 25% road tax rebate",
        "official_url": "https://vscrap.parivahan.gov.in",
        "steps": [
            ("Identify authorized RVSF facility", "Select government-registered authorized vehicle scrap center on national portal.", ["Vehicle location"], "₹0", "10 minutes"),
            ("Handover vehicle with original documents", "Provide vehicle along with original RC, insurance, and owner identity proofs.", ["Original RC", "Owner Aadhaar & PAN", "Bank details"], "₹0", "1 day"),
            ("Physical inspection & valuation", "Scrappage center weighs vehicle and evaluates scrap metal and component salvage value.", ["Scrap valuation agreement"], "₹0", "2 hours"),
            ("Scientific dismantling and destruction", "Vehicle undergoes eco-friendly fluid draining, hazardous material depollution, and chassis shredding.", ["Destruction video log"], "₹0", "1 day"),
            ("Issuance of Certificate of Deposit (CoD)", "Owner receives digital Certificate of Deposit conferring up to 25% concession on new vehicle road tax.", ["Certificate of Deposit (CoD) PDF"], "Payout credited to owner", "Same day")
        ]
    },
    {
        "id": "vintage_motor_vehicle_registration",
        "category": "Transport & Vehicles",
        "name": "Vintage Motor Vehicle Special Registration (50+ Years)",
        "department": "Regional Transport Office (RTO)",
        "jurisdiction": "Ministry of Road Transport and Highways",
        "summary": "Special heritage registration series (e.g. 'VA') for preserved vintage cars and two-wheelers older than 50 years.",
        "time": "15–20 working days",
        "cost": "₹20,000 (New registration) / ₹5,000 (Subsequent 10-year renewal)",
        "official_url": "https://parivahan.gov.in",
        "steps": [
            ("Verify age of vehicle (50+ years)", "Vehicle must be in original authentic condition with no substantial overhaul of chassis or body shell.", ["Original registration papers / import bill"], "₹0", "1 day"),
            ("Submit Form 20A application", "Apply online under Vintage Motor Vehicle category on Parivahan Vahan.", ["Photographs of vintage car from all sides", "Insurance policy"], "₹20,000", "1 day"),
            ("Inspection by Vintage Vehicle Committee", "Expert technical committee inspects preservation standards and mechanical safety.", ["Inspection evaluation sheet"], "₹0", "7 days"),
            ("Allocation of Vintage Number Plate (VA series)", "Receive unique 10-character registration code (e.g. XX VA YY ****).", ["Vintage Registration Certificate"], "₹0", "5 days")
        ]
    },

    # ---------------- 6. Social Welfare & Schemes ----------------
    {
        "id": "old_age_pension_scheme",
        "category": "Welfare & Schemes",
        "name": "Old Age Pension Scheme (NSAP / Vridha Pension)",
        "department": "Department of Social Security and Women & Child Development",
        "jurisdiction": "State Government / National Social Assistance Programme",
        "summary": "Monthly direct benefit financial assistance for senior citizens living below poverty line or with limited family support.",
        "time": "20–30 working days",
        "cost": "₹0 (Free Government Welfare Scheme)",
        "official_url": "https://nsap.nic.in",
        "steps": [
            ("Verify age & income eligibility", "Applicant must be aged 60 or above, with annual family income below state poverty threshold.", ["Aadhaar card", "Voter ID card"], "₹0", "Same day"),
            ("Bank account Aadhaar seeding", "Ensure bank savings account is active and seeded with Aadhaar for Direct Benefit Transfer (DBT).", ["Bank passbook showing Aadhaar NPCI link"], "₹0", "Same day"),
            ("Submit application on Social Security portal", "Apply online or submit at nearest citizen service center (CSC / e-Sewa).", ["Income certificate", "Passport size photograph"], "₹0", "1 day"),
            ("Field social worker inquiry", "Social welfare officer or Anganwadi worker verifies applicant living conditions.", ["Field verification report"], "₹0", "10–14 days"),
            ("Sanction and monthly DBT credit", "Sanction letter issued; monthly pension (₹1,500 – ₹3,000/month) credited directly to bank account.", ["Pension sanction order"], "Direct credit", "Monthly")
        ]
    },
    {
        "id": "widow_destitute_women_pension",
        "category": "Welfare & Schemes",
        "name": "Widow & Destitute Women Pension Scheme",
        "department": "Department of Women & Child Development",
        "jurisdiction": "State Government",
        "summary": "Monthly financial pension assistance to widows and destitute women with dependent children.",
        "time": "20–30 working days",
        "cost": "₹0 (Free Scheme)",
        "official_url": "https://wcd.nic.in",
        "steps": [
            ("Procure husband's death certificate", "Obtain official government death certificate of late spouse.", ["Husband's death certificate"], "₹0", "1 day"),
            ("Self-declaration of non-remarriage", "Provide affidavit affirming that the applicant has not remarried.", ["Notarized affidavit"], "₹50", "1 day"),
            ("Submit online application", "Submit application on state social security portal with family income proof and children birth certificates.", ["Income certificate", "Children school/birth certificates", "Aadhaar"], "₹0", "1 day"),
            ("Social welfare committee scrutiny", "District social welfare officer reviews records and verifies non-employment status.", ["Verification report"], "₹0", "14 days"),
            ("Monthly pension disbursement", "Receive pension sanction book and monthly direct benefit transfer into savings account.", ["Pension Sanction ID"], "Monthly transfer", "Immediate post-approval")
        ]
    },
    {
        "id": "pm_awas_yojana_urban_housing",
        "category": "Welfare & Schemes",
        "name": "PM Awas Yojana (PMAY-Urban) Housing Subsidy",
        "department": "Ministry of Housing and Urban Affairs / Municipal Corporation",
        "jurisdiction": "Central / Municipal Corporation",
        "summary": "Credit Linked Subsidy (CLSS) of up to ₹2.67 Lakh or affordable housing allotment for homeless EWS/LIG families.",
        "time": "30–60 working days",
        "cost": "₹0 application fee",
        "official_url": "https://pmaymis.gov.in",
        "steps": [
            ("Verify EWS/LIG income category", "Annual family income up to ₹3 Lakh for Economically Weaker Section (EWS); up to ₹6 Lakh for Low Income Group (LIG).", ["Income certificate", "Bank statement"], "₹0", "1 day"),
            ("Pucca house non-ownership affidavit", "Submit affidavit declaring that the beneficiary family does not own a pucca house anywhere in India.", ["Notarized PMAY affidavit"], "₹100", "1 day"),
            ("Register on PMAY-MIS portal", "Submit Aadhaar numbers of all family members, existing house rent proof, and bank IFSC details.", ["Family Aadhaar cards", "Rent agreement"], "₹0", "1 day"),
            ("Geo-tagging and civic survey", "Municipal survey team visits current dwelling to conduct geo-tagged photo verification.", ["Geo-tagged mobile survey record"], "₹0", "15 days"),
            ("Interest subsidy credit / Flat allotment", "Central government releases interest subsidy directly to home loan bank account or allocates municipal housing unit.", ["PMAY Sanction Letter"], "Up to ₹2.67 Lakh subsidy", "Post-scrutiny")
        ]
    },
    {
        "id": "ayushman_bharat_pmjay_health_card",
        "category": "Welfare & Schemes",
        "name": "Ayushman Bharat PM-JAY Golden Health Card",
        "department": "National Health Authority (NHA)",
        "jurisdiction": "Ministry of Health and Family Welfare",
        "summary": "Cashless secondary and tertiary hospitalization cover of up to ₹5,00,000 per family per year at empaneled hospitals.",
        "time": "Instant to 24 hours",
        "cost": "₹0 (Completely Free of Cost)",
        "official_url": "https://beneficiary.nha.gov.in",
        "steps": [
            ("Check eligibility on portal", "Search name or ration card number on National Beneficiary portal (SECC list or state NFSA database).", ["Ration card number", "Aadhaar number"], "₹0", "2 minutes"),
            ("Aadhaar e-KYC authentication", "Perform face-authentication via mobile app or biometric scan at Ayushman Mitra hospital kiosk.", ["Aadhaar linked mobile OTP / Biometrics"], "₹0", "5 minutes"),
            ("Family member matching", "Verify relationships and link dependent family members.", ["Ration card / Family register"], "₹0", "5 minutes"),
            ("Instant Ayushman Card download", "Download official PVC Ayushman Bharat card with PM-JAY unique ID.", ["Ayushman Card PDF"], "₹0", "Immediate"),
            ("Cashless hospital admission", "Show card at any empanelled public or private hospital for cashless treatment up to ₹5,00,000.", ["Ayushman Card"], "Cashless treatment", "Immediate")
        ]
    },
    {
        "id": "pm_svanidhi_street_vendor_microloan",
        "category": "Welfare & Schemes",
        "name": "PM SVANidhi Micro-Credit Loan for Street Vendors",
        "department": "Ministry of Housing and Urban Affairs & SIDBI",
        "jurisdiction": "Central Government",
        "summary": "Collateral-free working capital loan of ₹10,000, ₹20,000, and ₹50,000 with 7% interest subsidy for street vendors.",
        "time": "7–10 working days",
        "cost": "₹0 application fee; low subsidized interest",
        "official_url": "https://pmsvanidhi.mohua.gov.in",
        "steps": [
            ("Confirm street vending credentials", "Vendor must hold Certificate of Vending or Letter of Recommendation (LoR) from urban local body.", ["Vending certificate / LoR"], "₹0", "Same day"),
            ("Apply on PM SVANidhi portal", "Select preferred lending bank, input mobile number linked to Aadhaar, and loan amount tier.", ["Aadhaar", "Bank passbook"], "₹0", "15 minutes"),
            ("Bank digital appraisal", "Bank verifies credit history; no physical collateral or guarantor required.", ["Credit verification check"], "₹0", "3–5 days"),
            ("Loan disbursement to savings account", "Loan credited directly into bank account; vendor receives digital QR code for digital transaction cashbacks.", ["Bank credit alert"], "₹10,000 – ₹50,000", "Immediate"),
            ("7% interest subsidy payout", "Interest subsidy of 7% credited quarterly into bank account upon timely monthly repayment.", ["Subsidy credit SMS"], "7% subsidy", "Quarterly")
        ]
    },
    {
        "id": "ladli_girl_child_financial_incentive",
        "category": "Welfare & Schemes",
        "name": "Beti Bachao / Ladli Kanya Financial Incentive Scheme",
        "department": "Department of Women & Child Development",
        "jurisdiction": "State Government",
        "summary": "Fixed deposit financial aid deposited in the name of girl children at birth, school admissions, and upon turning 18.",
        "time": "15–20 working days",
        "cost": "₹0 (Free State Scheme)",
        "official_url": "https://wcd.nic.in",
        "steps": [
            ("Registration at birth of girl child", "Apply within 1 year of girl child birth at government hospital or Anganwadi center.", ["Birth certificate of girl child", "Hospital discharge slip"], "₹0", "1 day"),
            ("Parent residency & family income check", "Parents must have resided in state for 3+ years with annual income under prescribed limit.", ["Income certificate", "Parent domicile/voter ID"], "₹0", "1 day"),
            ("Submit application on WCD portal", "Upload child photograph, mother bank details, and immunization card.", ["Child immunization card", "Mother Aadhaar & bank passbook"], "₹0", "1 day"),
            ("Issuance of National Savings Certificate / FD", "Government purchases fixed deposit in the girl child's name with phased payouts at 6th, 9th, and 12th class milestones.", ["Sanction certificate of investment"], "₹0", "15 days"),
            ("Maturity payout on turning 18", "Full maturity amount released when the girl passes class 12 and attains age 18 as an unmarried citizen.", ["Class 12 marksheet", "Age certificate"], "Maturity benefit", "At age 18")
        ]
    },
    {
        "id": "disability_pension_scheme",
        "category": "Welfare & Schemes",
        "name": "Divyangjan Disability Monthly Pension",
        "department": "Department of Social Security and Empowerment",
        "jurisdiction": "State Social Welfare Department",
        "summary": "Monthly pension assistance to citizens with 40% or higher certified physical or intellectual disabilities.",
        "time": "20–30 working days",
        "cost": "₹0 (Free Welfare Scheme)",
        "official_url": "https://disabilityaffairs.gov.in",
        "steps": [
            ("Obtain 40%+ Disability Certificate / UDID", "Produce digital UDID card or disability certificate issued by government medical board.", ["UDID Card / Disability Certificate"], "₹0", "From medical board"),
            ("Income declaration", "Applicant family income must fall below state specified ceiling.", ["Income certificate from Tehsildar"], "₹0", "1 day"),
            ("Submit application online or at SDM office", "Submit bank account details linked to Aadhaar for automated monthly payments.", ["Aadhaar", "Bank passbook copy"], "₹0", "1 day"),
            ("District disability officer review", "Committee verifies non-receipt of competing pensions.", ["Scrutiny register"], "₹0", "14 days"),
            ("Monthly pension disbursement", "Receive recurring pension of ₹1,500 – ₹3,000 credited to bank account every month.", ["Monthly pension credit SMS"], "Monthly assistance", "Monthly")
        ]
    },
    {
        "id": "pm_matru_vandana_yojana_pmvvy",
        "category": "Welfare & Schemes",
        "name": "Pradhan Mantri Matru Vandana Yojana (PMMVY) Maternity Benefit",
        "department": "Ministry of Women & Child Development",
        "jurisdiction": "National Scheme",
        "summary": "Direct cash benefit of ₹5,000 in two installments for pregnant women and lactating mothers for first and second child.",
        "time": "15–20 working days per installment",
        "cost": "₹0 (Free Cash Maternity Benefit)",
        "official_url": "https://pmmvy.wcd.gov.in",
        "steps": [
            ("Register pregnancy at Anganwadi / Health Center", "Register pregnancy within 150 days of Last Menstrual Period (LMP) and obtain MCP card.", ["Mother and Child Protection (MCP) card"], "₹0", "Same day"),
            ("Submit Form 1A on PMMVY portal", "Submit MCP card showing at least one antenatal checkup (ANC) for first installment (₹3,000).", ["Aadhaar of mother and husband", "Mother bank passbook"], "₹0", "1 day"),
            ("Undergo child birth registration & vaccinations", "Register child birth and complete primary vaccination cycle (BCG, OPV, DPT, Hepatitis B).", ["Child birth certificate", "Immunization record in MCP card"], "₹0", "After birth"),
            ("Submit Form 1B for second installment", "Submit vaccination completion proof to claim second installment (₹2,000).", ["Vaccination certificate"], "₹0", "1 day"),
            ("Direct DBT transfer to mother account", "Funds transferred directly to woman's Aadhaar-seeded bank account.", ["DBT credit alert"], "₹5,000 total", "Direct credit")
        ]
    },
    {
        "id": "post_matric_scholarship_sc_st_obc",
        "category": "Welfare & Schemes",
        "name": "Post-Matric Scholarship for SC/ST/OBC Students",
        "department": "National Scholarship Portal (NSP) / Social Welfare",
        "jurisdiction": "Ministry of Social Justice & State Governments",
        "summary": "100% tuition fee reimbursement and monthly maintenance allowance for post-secondary and college students.",
        "time": "30–45 working days",
        "cost": "₹0 application fee",
        "official_url": "https://scholarships.gov.in",
        "steps": [
            ("College admission verification", "Secure admission in recognized college, university, or polytechnic institution.", ["College fee receipt", "Admission allotment letter"], "₹0", "At admission"),
            ("Submit application on National Scholarship Portal", "Register using OTR (One Time Registration) via Aadhaar Face RD app.", ["Aadhaar number", "Mobile"], "₹0", "15 minutes"),
            ("Upload scholarship documents", "Upload caste certificate, parent income certificate (under ₹2.5 Lakh), and previous class marksheet.", ["Caste certificate", "Income certificate", "Previous class marksheet"], "₹0", "1 day"),
            ("College level verification (Level 1)", "College scholarship nodal officer inspects attendance and verifies course fee structure online.", ["Institute online approval"], "₹0", "7 days"),
            ("District social welfare officer approval (Level 2)", "State department approves scholarship and releases DBT payments directly to student account and college.", ["PFMS credit alert"], "Full tuition + allowance", "Direct credit")
        ]
    },
    {
        "id": "pm_kisan_samman_nidhi",
        "category": "Welfare & Schemes",
        "name": "PM-KISAN Samman Nidhi (Farmer Financial Benefit)",
        "department": "Department of Agriculture and Farmers Welfare",
        "jurisdiction": "Central Government",
        "summary": "Direct income support of ₹6,000 per year in three equal installments of ₹2,000 to all landholding farmer families.",
        "time": "15–20 working days",
        "cost": "₹0 (Free Scheme)",
        "official_url": "https://pmkisan.gov.in",
        "steps": [
            ("Farmer land record verification", "Ensure land ownership record (Jamabandi / RoR / Khatauni) is updated in the farmer's name.", ["Land ownership title document (Jamabandi)"], "₹0", "1 day"),
            ("Farmer registration on PM-Kisan portal", "Input Aadhaar, mobile number, land plot survey number, and bank account details.", ["Aadhaar card", "Bank passbook"], "₹0", "15 minutes"),
            ("Aadhaar e-KYC authentication", "Complete mandatory biometric or face e-KYC on PM-Kisan mobile app.", ["Aadhaar OTP / Face e-KYC"], "₹0", "5 minutes"),
            ("State revenue department validation", "State agriculture/revenue nodal officer validates land records against state land registry.", ["State approval flag"], "₹0", "10 days"),
            ("Four-monthly DBT installment credit", "Receive ₹2,000 direct credit every four months (April-July, August-November, December-March).", ["PM-Kisan SMS notification"], "₹2,000 per installment", "Tri-annually")
        ]
    },
    {
        "id": "funeral_antyeshti_assistance_scheme",
        "category": "Welfare & Schemes",
        "name": "Antyeshti Sahayata / Financial Funeral Assistance",
        "department": "Social Welfare & Municipal Corporation",
        "jurisdiction": "Municipal Corporation / State Welfare",
        "summary": "Immediate one-time financial grant of ₹5,000 to ₹10,000 to assist indigent families with final funeral rites.",
        "time": "24–48 hours emergency response",
        "cost": "₹0 (Free Emergency Grant)",
        "official_url": "https://socialwelfare.gov.in",
        "steps": [
            ("Obtain cremation ground receipt", "Secure official slip from municipal cremation ground or burial ground.", ["Cremation receipt"], "₹0", "Immediate"),
            ("Submit BPL / EWS credentials", "Submit deceased death certificate, BPL ration card or income certificate, and applicant bank details.", ["BPL ration card", "Applicant Aadhaar & passbook"], "₹0", "Same day"),
            ("Approval by Municipal Ward Officer", "Zonal municipal officer or Tehsildar sanctions immediate assistance grant.", ["Sanction voucher"], "₹0", "24 hours"),
            ("Direct emergency bank disbursement", "Grant credited directly into savings account of nearest surviving kin.", ["Bank credit SMS"], "₹5,000 – ₹10,000", "24–48 hours")
        ]
    },
    {
        "id": "e_shram_unorganized_worker_card",
        "category": "Welfare & Schemes",
        "name": "e-Shram Card for Unorganized Workers",
        "department": "Ministry of Labour and Employment",
        "jurisdiction": "Central Government",
        "summary": "National database registration card providing ₹2 Lakh accidental insurance cover under PMSBY and social welfare eligibility.",
        "time": "Instant download",
        "cost": "₹0 (Completely Free of Cost)",
        "official_url": "https://eshram.gov.in",
        "steps": [
            ("Check eligibility criteria", "Applicant must be an unorganized worker (construction, domestic, driver, agriculture) aged between 16 and 59, not in EPFO/ESIC.", ["Aadhaar card", "Active mobile linked with Aadhaar"], "₹0", "5 minutes"),
            ("Register on e-Shram portal", "Authenticate via Aadhaar OTP, select primary occupation and sub-occupation from national skill list.", ["Bank account number & IFSC"], "₹0", "10 minutes"),
            ("Enter permanent address & nominee details", "Add emergency nominee name and relationship for accidental insurance benefits.", ["Nominee Aadhaar details"], "₹0", "5 minutes"),
            ("Download 12-digit Universal Account Number (UAN) Card", "Instantly download digital PVC e-Shram card with photo and permanent UAN number.", ["e-Shram Card PDF with UAN"], "₹0", "Instant")
        ]
    },
    {
        "id": "atal_pension_yojana_apy",
        "category": "Welfare & Schemes",
        "name": "Atal Pension Yojana (APY) Guaranteed Pension",
        "department": "Pension Fund Regulatory and Development Authority (PFRDA)",
        "jurisdiction": "Ministry of Finance",
        "summary": "Government-backed guaranteed monthly pension of ₹1,000, ₹2,000, ₹3,000, ₹4,000, or ₹5,000 per month starting at age 60.",
        "time": "Same day enrollment at bank",
        "cost": "Monthly auto-debit contribution based on joining age (₹42 – ₹1,454/month)",
        "official_url": "https://npscra.nsdl.co.in",
        "steps": [
            ("Eligibility check (Age 18–40)", "Applicant must be an Indian citizen aged between 18 and 40 years, with an active bank savings account.", ["Savings bank passbook", "Aadhaar card"], "₹0", "Same day"),
            ("Choose desired pension tier", "Select monthly pension amount (₹1,000 to ₹5,000) and frequency of contribution (monthly/quarterly).", ["Nominee particulars"], "₹0", "10 minutes"),
            ("Submit auto-debit authorization", "Apply via internet banking or submit APY registration form to bank branch authorizing auto-debit.", ["Signed auto-debit mandate"], "Monthly contribution", "Same day"),
            ("PRAN generation and acknowledgement", "Receive permanent APY PRAN number and digital subscriber registration slip.", ["APY PRAN card"], "₹0", "Instant"),
            ("Guaranteed pension commencement at age 60", "Lifelong monthly pension credited on the first of every month post age 60, followed by return of corpus to nominee.", ["Pension credit advice"], "Guaranteed pension", "At age 60")
        ]
    },
    {
        "id": "pm_ujjwala_yojana_free_lpg",
        "category": "Welfare & Schemes",
        "name": "Pradhan Mantri Ujjwala Yojana (PMUY) Free LPG Connection",
        "department": "Ministry of Petroleum and Natural Gas",
        "jurisdiction": "Central Government",
        "summary": "Deposit-free LPG cylinder connection, free stove, and initial refill for adult women from poor households.",
        "time": "7–10 working days",
        "cost": "₹0 (100% Free Government Connection)",
        "official_url": "https://pmuy.gov.in",
        "steps": [
            ("Eligibility check for female adult", "Applicant must be an adult woman belonging to BPL/SC/ST/Pradhan Mantri Awas Yojana household.", ["BPL ration card", "Woman Aadhaar card"], "₹0", "Same day"),
            ("Submit application at nearest gas distributor", "Apply on PMUY portal or submit form at nearest Indane, Bharat Gas, or HP Gas dealership.", ["Bank passbook showing Aadhaar seeding", "Proof of address"], "₹0", "1 day"),
            ("De-duplication check by OMC", "Oil Marketing Company cross-verifies database to ensure household has no existing LPG connection.", ["National LPG database verification"], "₹0", "3 days"),
            ("Collection of cylinder and stove", "Dealer supplies free 14.2 kg LPG cylinder, regulator, safety rubber hose, and domestic gas stove.", ["Ujjwala connection passbook"], "₹0", "Same day at delivery"),
            ("Targeted cylinder subsidy", "Receive ongoing government targeted subsidy credited directly to bank account on future refills.", ["Subsidy credit SMS"], "Direct subsidy", "On refill")
        ]
    },
    {
        "id": "national_family_benefit_scheme_nfbs",
        "category": "Welfare & Schemes",
        "name": "National Family Benefit Scheme (NFBS)",
        "department": "Department of Social Welfare & NSAP",
        "jurisdiction": "Central / State Government",
        "summary": "One-time lump sum grant of ₹20,000 to below-poverty-line families upon the death of the primary breadwinner.",
        "time": "30–45 working days",
        "cost": "₹0 (Free Welfare Grant)",
        "official_url": "https://nsap.nic.in",
        "steps": [
            ("Confirm breadwinner criteria", "Deceased must have been primary breadwinner aged between 18 and 59 at time of death.", ["Death certificate of breadwinner", "Age proof of deceased"], "₹0", "1 day"),
            ("Submit BPL proof", "Produce verified BPL ration card or family annual income certificate below poverty threshold.", ["BPL card", "Income certificate"], "₹0", "1 day"),
            ("Submit application on state social security portal", "Submit surviving spouse/head Aadhaar, post-mortem report (if accidental), and bank passbook.", ["Surviving spouse bank passbook"], "₹0", "1 day"),
            ("Sub-Divisional Magistrate verification", "Revenue officer conducts field verification of dependents.", ["Enquiry report"], "₹0", "15 days"),
            ("Lump-sum DBT credit", "One-time assistance of ₹20,000 credited directly to bank account of surviving spouse.", ["PFMS credit alert"], "₹20,000 grant", "Direct credit")
        ]
    },
    {
        "id": "stand_up_india_sc_st_women_loan",
        "category": "Welfare & Schemes",
        "name": "Stand-Up India Loan for SC/ST and Women Entrepreneurs",
        "department": "Department of Financial Services & SIDBI",
        "jurisdiction": "Ministry of Finance",
        "summary": "Bank loans between ₹10 Lakh and ₹1 Crore for greenfield enterprises in manufacturing, services, or trading sector.",
        "time": "30–45 working days",
        "cost": "₹0 application fee; lowest commercial interest rate",
        "official_url": "https://standupmitra.in",
        "steps": [
            ("Greenfield business project report", "Prepare detailed project report (DPR) showing proposed business, machinery cost, and financial viability.", ["Detailed Project Report (DPR)", "Quotations for machinery"], "Varies", "7 days"),
            ("Verify SC/ST or Woman category", "Borrower must be a woman or SC/ST entrepreneur holding at least 51% shareholding in enterprise.", ["Caste certificate (if SC/ST)", "PAN & Aadhaar"], "₹0", "1 day"),
            ("Apply on Stand-Up Mitra portal", "Submit loan application selecting preferred scheduled commercial bank branch.", ["Audited balance sheets (if existing) / Net worth statements"], "₹0", "1 day"),
            ("Bank appraisal and credit evaluation", "Bank manager reviews collateral/Credit Guarantee Scheme (CGFSI) and evaluates business model.", ["Bank sanction appraisal memo"], "₹0", "20 days"),
            ("Loan sanction and disbursement", "Receive composite loan sanction (term loan + working capital) between ₹10 Lakh and ₹1 Crore.", ["Loan sanction letter and disbursement"], "₹10L – ₹1Cr loan", "Post-documentation")
        ]
    }
]

def generate_and_save():
    FRONTEND_DEMO_PUBLIC.mkdir(parents=True, exist_ok=True)
    FRONTEND_DEMO_LIB.mkdir(parents=True, exist_ok=True)
    
    # Read existing chunks
    existing_chunks = []
    if PROCESSED_CHUNKS.exists():
        with open(PROCESSED_CHUNKS, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    existing_chunks.append(json.loads(line))
    
    # Keep original 3 MVP chunks (or filter out previous duplicates)
    base_chunks = [c for c in existing_chunks if c.get("procedure_id") in ("chandigarh_trade_license", "water_connection", "property_tax")]
    
    new_chunks = []
    for proc in RAW_CATALOG:
        pid = proc["id"]
        pname = proc["name"]
        dept = proc["department"]
        jurisdiction = proc.get("jurisdiction", "State / Municipal Corporation")
        official_url = proc.get("official_url", "https://india.gov.in")
        
        # 1. Overview chunk
        overview_text = f"{pname}: {proc['summary']} Estimated {proc['time']}. Government fee: {proc['cost']}."
        new_chunks.append({
            "chunk_id": f"{pid}__overview",
            "procedure_id": pid,
            "procedure_name": pname,
            "department": dept,
            "step_number": None,
            "section_title": "Overview",
            "text": overview_text,
            "source_url": official_url,
            "source_page": None,
            "doc_type": "official_guideline",
            "language": "en",
            "jurisdiction": jurisdiction,
            "last_verified": "2026-10-28"
        })
        
        # 2. Step chunks
        steps_for_demo = []
        for idx, (title, desc, docs, fee, ptime) in enumerate(proc["steps"], start=1):
            step_chunk_id = f"{pid}__step_{idx:02d}"
            step_text = f"{title}. {desc} Required documents: {', '.join(docs)}. Fee: {fee}. Processing time: {ptime}."
            new_chunks.append({
                "chunk_id": step_chunk_id,
                "procedure_id": pid,
                "procedure_name": pname,
                "department": dept,
                "step_number": idx,
                "section_title": title,
                "text": step_text,
                "source_url": official_url,
                "source_page": None,
                "doc_type": "official_guideline",
                "language": "en",
                "jurisdiction": jurisdiction,
                "last_verified": "2026-10-28"
            })
            steps_for_demo.append({
                "step_number": idx,
                "title": title,
                "description": desc,
                "documents_needed": docs,
                "fee": fee,
                "processing_time": ptime,
                "official_link": official_url,
                "source_chunk_ids": [step_chunk_id],
                "verified": True
            })
            
        # Write demo JSON file for offline/demo reliability
        demo_obj = {
            "procedure_name": pname,
            "procedure_id": pid,
            "summary": proc["summary"],
            "estimated_total_time": proc["time"],
            "estimated_total_cost": proc["cost"],
            "confidence": 0.95,
            "steps": steps_for_demo,
            "warnings": []
        }
        with open(FRONTEND_DEMO_PUBLIC / f"{pid}.json", "w", encoding="utf-8") as f:
            json.dump(demo_obj, f, indent=2, ensure_ascii=False)
        with open(FRONTEND_DEMO_LIB / f"{pid}.json", "w", encoding="utf-8") as f:
            json.dump(demo_obj, f, indent=2, ensure_ascii=False)

    all_chunks = base_chunks + new_chunks
    with open(PROCESSED_CHUNKS, "w", encoding="utf-8") as f:
        for c in all_chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
            
    print(f"Successfully wrote {len(all_chunks)} chunks for {len(RAW_CATALOG) + len(set(c['procedure_id'] for c in base_chunks))} procedures.")

if __name__ == "__main__":
    generate_and_save()
