import csv
import json
import sqlite3
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "data"
OUT.mkdir(parents=True, exist_ok=True)

brand_sources = [
    # HVAC
    ("HVAC", "Goodman", "Heat pumps, air conditioners, furnaces, air handlers", "Literature library", "Manuals, specs, brochures", "https://www.goodmanmfg.com/support/literature-library", "Official", "Use model number; also check Daikin/Amana family docs."),
    ("HVAC", "Daikin Comfort", "Heat pumps, AC, furnaces, ductless", "Owner support center", "Manuals, brochures, warranties", "https://daikincomfort.com/my-daikin-systems/owner-support-center", "Official", "Goodman/Amana/Daikin overlap on some systems."),
    ("HVAC", "Amana HVAC", "Heat pumps, AC, furnaces", "Product literature", "Manuals, specs, warranties", "https://www.amana-hac.com/resources/product-literature", "Official", "Use model number for exact docs."),
    ("HVAC", "Trane", "AC, furnace, heat pump, air handler, thermostat", "Owner guides", "Owner manuals, troubleshooting, maintenance", "https://www.trane.com/residential/en/resources/owners-guides/", "Official", "Strong homeowner support source."),
    ("HVAC", "American Standard HVAC", "AC, furnace, heat pump, air handler", "Owner support", "Owner guides, safety, DIY tips", "https://www.americanstandardair.com/resources/owners-support/", "Official", "Trane family brand."),
    ("HVAC", "Carrier", "AC, heat pumps, furnaces, air handlers", "Product and support hub", "Product docs, owners support", "https://www.carrier.com/residential/en/us/products/", "Official", "Carrier/Bryant/Payne family."),
    ("HVAC", "Bryant", "AC, heat pumps, furnaces", "Product hub", "Product docs and support", "https://www.bryant.com/en/us/", "Official", "Carrier family brand."),
    ("HVAC", "Payne", "AC, heat pumps, furnaces", "Product hub", "Product docs and support", "https://www.payne.com/en/us/", "Official", "Carrier family value brand."),
    ("HVAC", "Lennox", "AC, heat pumps, furnaces, controls", "Owner support", "Manuals, warranty, support", "https://www.lennox.com/owners/support", "Official", "Use model number for exact docs."),
    ("HVAC", "Rheem HVAC", "AC, heat pumps, furnaces", "Resources", "Manuals, guides, support", "https://www.rheem.com/resources/", "Official", "Rheem/Ruud family."),
    ("HVAC", "Ruud", "AC, heat pumps, furnaces", "Resources", "Manuals, guides, support", "https://www.ruud.com/resources/", "Official", "Rheem/Ruud family."),
    ("HVAC", "York", "AC, heat pumps, furnaces", "Resources", "Manuals, product docs", "https://www.york.com/residential-equipment/resources", "Official", "Johnson Controls family."),
    ("HVAC", "Bosch Home Comfort", "Heat pumps, IDS systems, boilers", "Technical documentation", "Manuals and technical docs", "https://www.bosch-homecomfort.com/us/en/residential/technical-documentation/manuals/heating-and-cooling-heat-pump-systems/", "Official", "Strong heat pump docs."),
    ("HVAC", "Mitsubishi Electric", "Ductless and ducted heat pumps", "Resources", "Manuals, submittals, guides", "https://www.mitsubishicomfort.com/resources", "Official", "Mini split and hyper heat systems."),
    ("HVAC", "Fujitsu General", "Mini splits and heat pumps", "Support", "Manuals and support docs", "https://www.fujitsugeneral.com/us/support/", "Official", "Mini split resource."),
    ("HVAC", "LG HVAC", "Mini splits and heat pumps", "Support", "Manuals and product docs", "https://www.lghvac.com/support", "Official", "Ductless and VRF resource."),
    ("HVAC", "AprilAire", "Humidifiers, dehumidifiers, IAQ, thermostats", "Manuals", "Owner/install manuals", "https://www.aprilaire.com/owner-center/product-manuals", "Official", "Important IAQ add-on brand."),

    # Water heating
    ("Water Heating", "A.O. Smith", "Tank, tankless, heat pump water heaters", "Support", "Manuals, videos, product literature", "https://www.hotwater.com/support.html", "Official", "Includes rebates and pro resources."),
    ("Water Heating", "State Water Heaters", "Tank and tankless water heaters", "Support", "Manuals, documents, videos", "https://www.statewaterheaters.com/support.html", "Official", "A.O. Smith family."),
    ("Water Heating", "American Water Heaters", "Water heaters", "Documents and videos", "Manuals and troubleshooting", "https://www.americanwaterheater.com/find-documents-and-videos", "Official", "A.O. Smith family."),
    ("Water Heating", "Bradford White", "Residential/commercial water heaters", "Technical documents", "Manuals, spec sheets, parts lists", "https://forthepro.bradfordwhite.com/documentation/", "Official", "Best Bradford White pro source."),
    ("Water Heating", "Rheem Water Heating", "Tank, tankless, hybrid heat pump", "Resources", "Manuals, guides, support", "https://www.rheem.com/resources/", "Official", "Good heat pump water heater content."),
    ("Water Heating", "Navien", "Tankless, combi, boilers", "Downloads", "Manuals, drawings, specs, certificates", "https://www.navieninc.com/commercial/water-heaters/downloads", "Official", "Important tankless/combi source."),
    ("Water Heating", "Rinnai", "Tankless water heaters", "Support", "Manuals, warranty, troubleshooting", "https://www.rinnai.us/support", "Official", "Model lookup needed."),
    ("Water Heating", "Noritz", "Tankless water heaters", "Support", "Manuals and product docs", "https://www.noritz.com/support/", "Official", "Tankless troubleshooting."),
    ("Water Heating", "Stiebel Eltron", "Electric tankless, heat pump water heaters", "Downloads", "Manuals and specs", "https://www.stiebel-eltron-usa.com/service/downloads", "Official", "Electric tankless and HPWH."),
    ("Water Heating", "ENERGY STAR", "Heat pump water heaters", "Technical guide", "HPWH technical guide", "https://www.energystar.gov/sites/default/files/2024-07/ENERGY%20STAR%20Heat%20Pump%20Water%20Heater%20Technical%20Guide%20508C.pdf", "Government", "Neutral technical guidance."),

    # Thermostats
    ("Thermostats", "Honeywell Home / Resideo", "Thermostats", "Manual finder", "User/install manuals", "https://www.honeywellhome.com/pages/support-product-selector-thermostat-manuals", "Official", "Most common thermostat manual source."),
    ("Thermostats", "ecobee", "Smart thermostats and sensors", "Documents", "Install guides and user manuals", "https://support.ecobee.com/s/articles/download-documents-included-with-your-ecobee-device", "Official", "Good smart thermostat source."),
    ("Thermostats", "Google Nest", "Nest thermostats", "Help guide", "Setup and user support", "https://support.google.com/googlehome/answer/9248184?hl=en", "Official", "Homeowner setup and use."),
    ("Thermostats", "Copeland / Emerson / White-Rodgers / Sensi", "Thermostats", "Manual lookup", "Install/operation manuals", "https://www.copeland.com/en-us/products/thermostats/thermostat-manuals", "Official", "Covers older White-Rodgers and newer Sensi."),
    ("Thermostats", "Lux Products", "Thermostats", "Support", "Manuals and programming help", "https://www.luxproducts.com/pages/support", "Official", "Older affordable thermostats."),

    # Solar / battery
    ("Solar/Battery", "NREL", "PVWatts", "Solar calculator", "Production estimate", "https://pvwatts.nrel.gov/", "Government", "Neutral solar production estimator."),
    ("Solar/Battery", "EnergySage", "Solar savings", "Calculator", "Savings estimate", "https://www.energysage.com/solar/calculator/", "Industry", "Benchmark for RoofingHut solar tool."),
    ("Solar/Battery", "Enphase", "Microinverters, batteries, monitoring", "Documentation", "Install guides, datasheets, support docs", "https://enphase.com/installers/resources/documentation", "Official", "Core microinverter source."),
    ("Solar/Battery", "SolarEdge", "Inverters, optimizers, batteries", "Downloads", "Manuals, datasheets, warranties", "https://www.solaredge.com/us/support/downloads", "Official", "Core optimizer/string inverter source."),
    ("Solar/Battery", "Generac Clean Energy", "PWRcell, PWRmicro", "Manuals and spec sheets", "Manuals, quick starts, warranties", "https://www.generac.com/dealers-installers/solar-battery-installer-support/manuals-spec-sheets/", "Official", "Good solar/battery technical tables."),
    ("Solar/Battery", "Tesla", "Solar and Powerwall", "System manual", "System operation and compatibility", "https://www.tesla.com/sites/default/files/Solar-Panels-with-Powerwall-System-Manual.pdf", "Official PDF", "Homeowner solar/battery source."),
    ("Solar/Battery", "SMA America", "Solar inverters", "Downloads", "Manuals, datasheets, certificates", "https://www.sma-america.com/service/downloads", "Official", "String inverter docs."),
    ("Solar/Battery", "Fronius", "Solar inverters", "Technical data", "Manuals and datasheets", "https://www.fronius.com/en/solar-energy/installers-partners/technical-data/all-products", "Official", "Inverter docs."),
    ("Solar/Battery", "Qcells", "Solar panels and storage", "Downloads", "Datasheets, warranties, manuals", "https://www.qcells.com/us/main/service/downloads.html", "Official", "Panel docs."),
    ("Solar/Battery", "REC Group", "Solar panels", "Downloads", "Datasheets, install manuals, warranties", "https://www.recgroup.com/en/downloads", "Official", "Premium panel docs."),
    ("Solar/Battery", "IronRidge", "Solar racking", "Resources", "Install manuals, engineering docs", "https://www.ironridge.com/resources/", "Official", "Roof solar mounting."),
    ("Solar/Battery", "Unirac", "Solar racking", "Documents", "Install manuals and engineering docs", "https://unirac.com/documents/", "Official", "Roof solar mounting."),

    # Roofing
    ("Roofing", "GAF", "Shingles, underlayment, accessories", "Product documents", "Install instructions, specs, warranties", "https://www.gaf.com/en-us/resources/product-documents", "Official", "Core shingle source."),
    ("Roofing", "Owens Corning", "Roofing system", "Install instructions", "Install guides", "https://www.owenscorning.com/en-us/roofing/install-instructions", "Official", "Clear official install page."),
    ("Roofing", "CertainTeed", "Shingles and roofing products", "Roofing resources", "Manuals, specs, warranties", "https://www.certainteed.com/resources/roofing-resources/", "Official", "Important manufacturer docs."),
    ("Roofing", "IKO", "Asphalt shingles", "Roofing resources", "Install, warranty, technical docs", "https://www.iko.com/na/residential-roofing/roofing-resources/", "Official", "Shingle docs."),
    ("Roofing", "Atlas Roofing", "Shingles and underlayment", "Resources", "Specs, install, warranty", "https://www.atlasroofing.com/roof-shingles/resources", "Official", "Pinnacle/StormMaster docs."),
    ("Roofing", "TAMKO", "Shingles and roofing products", "Resources", "Brochures, install, warranty", "https://www.tamko.com/resources", "Official", "Heritage/Titan docs."),
    ("Roofing", "Malarkey", "Shingles and accessories", "Resources", "Specs, install, warranty", "https://www.malarkeyroofing.com/resources/", "Official", "Vista/Legacy/Highlander docs."),
    ("Roofing", "Mule-Hide", "Flat roofing", "Documents", "Manuals, detail drawings, specs", "https://www.mulehide.com/en-us/Resources", "Official", "Low-slope roofing."),
    ("Roofing", "Carlisle SynTec", "Flat roofing", "Resources", "Specs, details, manuals", "https://www.carlislesyntec.com/resources", "Official", "Commercial/low-slope."),
    ("Roofing", "Duro-Last", "Single-ply roofing", "Resources", "Specs, details, install", "https://duro-last.com/resources", "Official", "Commercial/low-slope."),
    ("Roofing", "Velux", "Skylights", "Support", "Install, flashing, parts", "https://www.veluxusa.com/help", "Official", "Skylight install/leak resource."),
    ("Roofing", "ARMA", "Asphalt roofing", "Residential asphalt roofing manual", "Technical manual", "https://www.asphaltroofing.org/media/_pda/2019/03/TAC-Technical-Review-Task-Force-Residential-Asphalt-Roofing-Manual-2014.pdf", "Industry PDF", "Neutral technical source."),

    # Plumbing
    ("Plumbing", "Moen", "Faucets, fixtures, smart water", "Solutions", "Install/troubleshooting/model ID", "https://solutions.moen.com/", "Official", "Faucet cartridge/model lookup."),
    ("Plumbing", "Delta Faucet", "Faucets, showers, toilets, filtration", "Support/how-to", "Videos, FAQs, troubleshooting", "https://www.deltafaucet.com/", "Official", "Homeowner-friendly."),
    ("Plumbing", "Kohler", "Kitchen/bath fixtures", "Technical specs", "Specs, diagrams, install", "https://www.kohler.com/en/for-professionals/technical-specifications", "Official", "Excellent fixture docs."),
    ("Plumbing", "American Standard", "Kitchen/bath fixtures", "Support", "FAQs, parts, install support", "https://www.americanstandard-us.com/pages/support", "Official", "Fixture support."),
    ("Plumbing", "Toto", "Toilets and bath fixtures", "Support", "Manuals, parts, support", "https://www.totousa.com/support", "Official", "Toilet parts/troubleshooting."),
    ("Plumbing", "Liberty Pumps", "Sump/sewage/drain pumps", "Support", "Manuals, specs, troubleshooting", "https://www.libertypumps.com/Support", "Official", "Pump docs."),
    ("Plumbing", "Zoeller", "Sump/sewage pumps", "Support", "Manuals, parts, troubleshooting", "https://www.zoellerpumps.com/support/", "Official", "Pump docs."),
    ("Plumbing", "Watts", "Valves, backflow, water quality", "Resources", "Specs, install, product docs", "https://www.watts.com/resources", "Official", "Valves/backflow/water quality."),
    ("Plumbing", "InSinkErator", "Garbage disposals, instant hot water", "Support", "Manuals and troubleshooting", "https://insinkerator.emerson.com/en-us/support", "Official", "Disposal docs."),

    # Electrical
    ("Electrical", "Schneider Electric / Square D", "Panels, breakers, surge protection", "Home surge protection", "Product docs and safety", "https://www.se.com/us/en/work/products/explore/home-surge-protection/", "Official", "Common residential panels."),
    ("Electrical", "Eaton", "Breakers, panels, surge", "Wiring manual", "Wiring diagrams and examples", "https://www.eaton.com/content/dam/eaton/markets/machinebuilding/eaton-wiring-manual-pu08703001z-en-en-us.pdf", "Official PDF", "Broad electrical wiring reference."),
    ("Electrical", "Siemens", "Low voltage power distribution", "Product hub", "Panels, breakers, surge docs", "https://www.siemens.com/en-us/products/low-voltage/", "Official", "Siemens residential/commercial docs."),
    ("Electrical", "Leviton", "Load centers, breakers, devices", "Support", "Manuals and specs", "https://www.leviton.com/en/support", "Official", "Smart load centers and devices."),
    ("Electrical", "Lutron", "Dimmers, lighting controls", "Support", "Install and compatibility docs", "https://support.lutron.com/us/en", "Official", "Dimmer compatibility."),
    ("Electrical", "Generac", "Generators and transfer switches", "Support/manuals", "Owner/install manuals", "https://www.generac.com/service-support/product-support-lookup", "Official", "Generator docs by serial/model."),
    ("Electrical", "Reliance Controls", "Transfer switches", "Support", "Manuals and wiring", "https://www.reliancecontrols.com/support", "Official", "Manual transfer switches."),
    ("Electrical", "ChargePoint", "EV chargers", "Support", "Install/user docs", "https://www.chargepoint.com/drivers/support", "Official", "EV charging."),
    ("Electrical", "Emporia", "EV chargers and energy monitors", "Support", "Install/user docs", "https://help.emporiaenergy.com/", "Official", "Energy monitoring and EV charging."),

    # Appliances
    ("Appliances", "Whirlpool", "Dishwashers, washers, dryers, refrigerators, ranges, microwaves", "Owner Center", "Manuals, parts, warranty, troubleshooting", "https://www.whirlpool.com/services/manuals.html", "Official", "Major appliance manual lookup by model number."),
    ("Appliances", "Maytag", "Dishwashers, washers, dryers, refrigerators, ranges", "Manuals and literature", "Manuals, parts, support", "https://www.maytag.com/services/manuals.html", "Official", "Whirlpool family brand."),
    ("Appliances", "KitchenAid", "Dishwashers, refrigerators, ranges, microwaves", "Manuals and literature", "Manuals, parts, support", "https://www.kitchenaid.com/service-and-support/manuals.html", "Official", "Whirlpool family premium kitchen brand."),
    ("Appliances", "Amana Appliances", "Dishwashers, washers, dryers, refrigerators, ranges", "Manuals and literature", "Manuals and support", "https://www.amana.com/content/amana/en_us/services/manuals.html", "Official", "Whirlpool family value appliance brand."),
    ("Appliances", "GE Appliances", "Dishwashers, washers, dryers, refrigerators, ranges, microwaves", "Owner support", "Manuals, troubleshooting, parts", "https://www.geappliances.com/ge/service-and-support/literature.htm", "Official", "Major appliance manual lookup."),
    ("Appliances", "Frigidaire", "Dishwashers, washers, dryers, refrigerators, ranges", "Owner center", "Manuals, guides, support", "https://www.frigidaire.com/en/owner-center", "Official", "Manual lookup and appliance support."),
    ("Appliances", "Samsung", "Dishwashers, washers, dryers, refrigerators, ranges", "Support", "Manuals, downloads, troubleshooting", "https://www.samsung.com/us/support/downloads/", "Official", "Model-specific manual lookup."),
    ("Appliances", "LG Appliances", "Dishwashers, washers, dryers, refrigerators, ranges", "Manuals and documents", "Manuals, software, support", "https://www.lg.com/us/support/manuals-documents", "Official", "Model-specific manual lookup."),
    ("Appliances", "Bosch Appliances", "Dishwashers, refrigerators, ranges", "Owner manuals", "Manuals, support, parts", "https://www.bosch-home.com/us/owner-support/owner-manuals", "Official", "Very common dishwasher brand."),
    ("Appliances", "Miele", "Dishwashers, washers, dryers, vacuums", "Manuals", "Operating and installation manuals", "https://www.mieleusa.com/c/manuals-and-specifications-2519.htm", "Official", "Premium appliance manuals."),
    ("Appliances", "Sub-Zero / Wolf / Cove", "Refrigeration, cooking, dishwashers", "Product support", "Manuals, specs, troubleshooting", "https://www.subzero-wolf.com/assistance", "Official", "Premium kitchen appliance support."),
    ("Appliances", "Speed Queen", "Washers and dryers", "Support", "Manuals, parts, warranty", "https://speedqueen.com/support/", "Official", "Laundry equipment support."),

    # Generators, garage doors, pumps, windows/exterior
    ("Generators", "Kohler", "Standby generators and transfer switches", "Support", "Manuals, specs, service", "https://kohlerpower.com/en/residential/support", "Official", "Standby generator docs."),
    ("Generators", "Cummins", "Standby generators", "Support", "Manuals, service, support", "https://www.cummins.com/generators/support", "Official", "Generator docs."),
    ("Generators", "Champion", "Portable and standby generators", "Support", "Manuals, parts, troubleshooting", "https://www.championpowerequipment.com/support/", "Official", "Portable/inverter generator manuals."),
    ("Generators", "Westinghouse Outdoor Power", "Portable generators", "Support", "Manuals and parts", "https://westinghouseoutdoorpower.com/pages/support", "Official", "Portable generator manuals."),
    ("Garage Doors", "LiftMaster", "Garage door openers", "Support", "Manuals, parts, programming", "https://support.chamberlaingroup.com/s/liftmaster", "Official", "Common opener brand."),
    ("Garage Doors", "Chamberlain", "Garage door openers", "Support", "Manuals, programming, troubleshooting", "https://support.chamberlaingroup.com/s/chamberlain", "Official", "Common homeowner opener brand."),
    ("Garage Doors", "Genie", "Garage door openers", "Support", "Manuals and programming", "https://www.geniecompany.com/support", "Official", "Common opener brand."),
    ("Garage Doors", "Clopay", "Garage doors", "Support", "Install manuals and care", "https://www.clopaydoor.com/residential/support", "Official", "Garage door install/care."),
    ("Windows/Doors", "Andersen", "Windows and doors", "Support", "Install guides, parts, warranty", "https://helpcenter.andersenwindows.com/", "Official", "Window/door support."),
    ("Windows/Doors", "Pella", "Windows and doors", "Support", "Install, care, parts, warranty", "https://www.pella.com/support/", "Official", "Window/door support."),
    ("Windows/Doors", "Marvin", "Windows and doors", "Support", "Manuals, parts, warranty", "https://www.marvin.com/support", "Official", "Window/door support."),
    ("Windows/Doors", "JELD-WEN", "Windows and doors", "Support", "Install and product docs", "https://www.jeld-wen.com/en-us/support", "Official", "Window/door support."),
    ("Pumps", "Grundfos", "Circulator, well and utility pumps", "Support", "Manuals, curves, specs", "https://www.grundfos.com/us/support", "Official", "Pump docs."),
    ("Pumps", "Pentair", "Pumps, water treatment, pool equipment", "Support", "Manuals, parts, troubleshooting", "https://www.pentair.com/en-us/support.html", "Official", "Pump/pool/water treatment docs."),
    ("Pumps", "Franklin Electric", "Well pumps and controls", "Support", "Manuals, AIM manual, specs", "https://franklinwater.com/resources/", "Official", "Well pump and motor documentation."),
]

exact_manuals = [
    ("HVAC", "Goodman", "Heat Pump", "GSZ14", "GSZ140301", "2.5 ton split heat pump", "Service manual", "Goodman GSZ14 Service Manual", "https://documents.alpinehomeair.com/product/Goodman%20GSZ14%20Service%20Manual.pdf", "PDF", "R-410A, 208/230V, single phase", "Tech only", "Service/troubleshooting manual for R-410A split heat pumps."),
    ("HVAC", "Goodman", "Heat Pump", "GSZ14", "GSZ140301", "2.5 ton split heat pump", "Installation/service reference", "Goodman GSZ Installation Manual", "https://www.budgetheating.com/content/files/downloadables/gsz%20-%20installation%20manual.pdf", "PDF", "R-410A, 208/230V, single phase", "Tech only", "Installation/service reference; verify exact revision."),
    ("HVAC", "Goodman", "Heat Pump", "GSZ14", "GSZ140301", "2.5 ton split heat pump", "Spec sheet", "Goodman GSZ14 Spec Sheet", "https://documents.alpinehomeair.com/product/Goodman%20GSZ14%20Spec%20Sheet.pdf", "PDF", "30,000 BTU, 2.5 ton", "Homeowner/Tech", "Performance data, AHRI ratings and wiring diagram section."),
    ("Solar/Battery", "Tesla", "Solar + Battery", "Powerwall with solar panels", "N/A", "Solar panels with Powerwall", "System manual", "Tesla Solar Panels with Powerwall System Manual", "https://www.tesla.com/sites/default/files/Solar-Panels-with-Powerwall-System-Manual.pdf", "PDF", "Solar + battery", "Homeowner/Tech", "Homeowner system operation and compatibility reference."),
    ("Water Heating", "ENERGY STAR", "Heat Pump Water Heater", "HPWH", "N/A", "Heat pump water heater", "Technical guide", "ENERGY STAR HPWH Technical Guide", "https://www.energystar.gov/sites/default/files/2024-07/ENERGY%20STAR%20Heat%20Pump%20Water%20Heater%20Technical%20Guide%20508C.pdf", "PDF", "208/240V typical", "Homeowner/Tech", "Neutral planning guide for HPWH content."),
    ("Electrical", "Eaton", "Surge / Electrical", "Wiring Manual", "N/A", "Electrical wiring reference", "Wiring manual", "Eaton Wiring Manual", "https://www.eaton.com/content/dam/eaton/markets/machinebuilding/eaton-wiring-manual-pu08703001z-en-en-us.pdf", "PDF", "Electrical", "Tech only", "Broad wiring/circuit example reference."),
    ("Electrical", "Siemens", "Surge Protection", "TPS4", "N/A", "Surge protective device", "Installation/user manual", "Siemens TPS4 Surge Protection Manual", "https://support.industry.siemens.com/cs/attachments/109800427/SIE_IM_SurgeProtection_TPS4.pdf", "PDF", "Electrical", "Tech only", "SPD installation and operation."),
    ("Electrical", "Generac", "Transfer Switch", "GenReady", "N/A", "Load center / transfer switch", "Owner manual", "Generac GenReady Multi-breaker Load Center Owner's Manual", "https://www.generac.com/globalassets/products/residential/standby-generator-transfer-switches/automatic-transfer-switches/owners-manual/g0054532-g0054542-g0054482-g0054492-owners-manual.pdf", "PDF", "Generator transfer switch", "Tech only", "Contains wiring diagrams and electrical schematics."),
    ("Roofing", "ARMA", "Asphalt Roofing", "Residential Asphalt Roofing Manual", "N/A", "Residential asphalt roof systems", "Technical manual", "Residential Asphalt Roofing Manual", "https://www.asphaltroofing.org/media/_pda/2019/03/TAC-Technical-Review-Task-Force-Residential-Asphalt-Roofing-Manual-2014.pdf", "PDF", "Roofing", "Homeowner/Tech", "Neutral asphalt roofing practices."),
]

lookup_rules = [
    ("HVAC tonnage", "018=1.5 ton, 024=2 ton, 030=2.5 ton, 036=3 ton, 042=3.5 ton, 048=4 ton, 060=5 ton", "Applies broadly to split AC/heat pump model numbers, but always verify."),
    ("Goodman GSZ14", "GSZ14 is Goodman 14 SEER-class split heat pump family using R-410A; GSZ140301 is 30,000 BTU / 2.5 ton single-phase pattern.", "Exact suffix/revision matters for parts and wiring."),
    ("HVAC safety", "Service manuals are generally for trained HVAC technicians only; homeowners should use owner manuals and call a licensed pro for electrical, refrigerant, gas, or combustion work.", "Use safety note in RoofingHut answers."),
    ("Water heater age", "Most water heater brands encode manufacture date in serial number, but each brand differs.", "Use brand-specific age lookup before advising replacement age."),
    ("Thermostat wiring", "Common terminals: R/Rc/Rh 24V, C common, Y compressor, G fan, W/Aux heat, O/B reversing valve.", "Heat pumps require careful O/B and aux heat setup."),
    ("Electrical safety", "Panel, breaker, transfer switch, surge protector, EV charger and generator wiring should be handled by qualified/licensed electricians.", "Never present dangerous electrical work as DIY."),
]

troubleshooting_topics = [
    ("HVAC", "Heat pump not heating", "Check thermostat mode/settings, breaker/disconnect, outdoor unit running, ice buildup, air filter, error codes. Escalate refrigerant/electrical issues to pro.", "GSZ14 docs, brand manual, thermostat manual"),
    ("HVAC", "Heat pump iced over", "Some frost is normal; heavy ice may mean defrost issue, airflow restriction, low refrigerant, sensor/board issue.", "Service manual, wiring diagram, defrost board docs"),
    ("HVAC", "Thermostat blank", "Check batteries if applicable, furnace/air-handler power, float switch, breaker, low-voltage fuse.", "Thermostat manual, air handler wiring diagram"),
    ("Water Heating", "No hot water electric tank", "Check breaker, reset, thermostat, elements; electrical testing is pro-level.", "Brand install/service manual"),
    ("Water Heating", "Tankless error code", "Use exact brand/model error table; check venting, gas supply, water flow, ignition, condensate.", "Navien/Rinnai/Noritz manual"),
    ("Roofing", "Roof leak after rain", "Track entry vs visible stain; inspect flashing, pipe boots, valleys, skylights, vents, nail pops.", "Roofing manufacturer install docs"),
    ("Electrical", "Breaker trips repeatedly", "Do not keep resetting; possible overload, short, ground fault, failed appliance or breaker.", "Panel/breaker docs; licensed electrician"),
    ("Solar/Battery", "Solar production low", "Check monitoring app, inverter status, shading, dirty panels, breaker/disconnect, grid outage.", "Inverter manual and monitoring docs"),
    ("Plumbing", "Faucet dripping", "Identify brand/model, cartridge/stem, shutoff, exact parts diagram.", "Moen/Delta/Kohler support"),
    ("Appliances", "Dishwasher not draining", "Check filter, drain hose high loop/air gap, garbage disposal knockout, pump obstruction. Use exact model manual before disassembly.", "Appliance owner/service manual"),
    ("Appliances", "Washer not spinning", "Check load balance, lid/door lock, drain issue, error code, belt/direct drive notes by model.", "Washer manual and error code chart"),
    ("Appliances", "Dryer not heating", "Check lint restriction, breaker/gas supply, vent blockage; electrical/gas testing is pro-level.", "Dryer manual and wiring diagram"),
    ("Appliances", "Refrigerator not cooling", "Check condenser coils, door seal, evaporator fan, condenser fan, start relay, error codes.", "Refrigerator service/owner manual"),
    ("Garage Doors", "Opener will not close", "Check photo eyes/safety sensors, door balance, travel limits, force settings, obstruction.", "Opener manual and wiring diagram"),
    ("Generators", "Standby generator will not start", "Check battery, fuel supply, exercise schedule, error code, oil level, transfer switch status.", "Generator owner/install manual"),
    ("Pumps", "Sump pump not running", "Check power/GFCI, float switch, pit debris, check valve, discharge freezing/clogging.", "Pump manual"),
]

coverage = [
    ("Roofing", "Shingles, metal, flat, underlayment, flashing, vents, skylights, gutters", "Install instructions, detail drawings, warranty, repair guides"),
    ("HVAC", "AC, heat pump, furnace, air handler, mini split, IAQ, humidifiers", "Install, owner, service, wiring, fault codes, parts lists"),
    ("Water Heating", "Gas/electric tank, tankless, HPWH, combi, boilers", "Install, service, wiring, venting, error codes, parts"),
    ("Thermostats", "Smart, programmable, non-programmable, communicating", "Install, wiring, setup, compatibility, user guides"),
    ("Solar/Battery", "Panels, inverters, batteries, racking, rapid shutdown", "Datasheets, install, commissioning, compatibility, warranty"),
    ("Electrical", "Panels, breakers, surge, transfer switches, EV chargers", "Wiring diagrams, install, compatibility, safety docs"),
    ("Plumbing", "Fixtures, valves, pumps, filtration, disposals", "Install, parts diagrams, troubleshooting, warranty"),
    ("Generators", "Standby, portable, inverter, transfer switches", "Owner, install, wiring, maintenance, parts"),
    ("Appliances", "Refrigerator, range, dishwasher, washer/dryer", "Owner/install, error codes, wiring where available"),
    ("Windows/Doors", "Windows, exterior doors, skylights", "Install, flashing, parts, warranty"),
    ("Siding/Exterior", "Vinyl, fiber cement, engineered wood, housewrap", "Install, clearance, fastening, warranty"),
    ("Insulation/Air Sealing", "Batts, blown, spray foam, rigid foam", "R-value, install, SDS, code guides"),
    ("Garage Doors", "Doors, openers, springs, sensors", "Owner/install, troubleshooting, wiring"),
    ("Flooring/Tile", "LVP, laminate, hardwood, tile, grout", "Install, substrate, warranty"),
    ("Drywall/Paint", "Drywall, joint compound, coatings, sealants", "Product data, SDS, application guides"),
    ("Masonry/Concrete", "Concrete, mortar, pavers, waterproofing", "Product data, SDS, structural guides"),
    ("Decks/Outdoor", "Decking, railing, fasteners", "Install, span/fastening, warranty"),
    ("Pools/Spas", "Pumps, heaters, filters, automation", "Manuals, wiring, error codes"),
    ("Smart Home/Security", "Cameras, locks, sensors, alarms", "Setup, wiring, compatibility"),
    ("Irrigation/Landscape", "Controllers, valves, pumps, lighting", "Manuals, wiring, troubleshooting"),
    ("Septic/Well", "Well pumps, pressure tanks, septic pumps", "Pump curves, wiring, troubleshooting"),
]

def write_csv(name, headers, rows):
    path = OUT / name
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    return path

write_csv("brand_document_hubs.csv", ["trade","brand","equipment_scope","resource_name","resource_types","url","source_type","notes"], brand_sources)
write_csv("exact_manual_index.csv", ["trade","brand","product_family","series","model","equipment","document_type","document_title","url","format","key_specs","audience","notes"], exact_manuals)
write_csv("lookup_rules.csv", ["topic","rule","caution"], lookup_rules)
write_csv("troubleshooting_topics.csv", ["trade","problem","first_checks","needed_documents"], troubleshooting_topics)
write_csv("trade_coverage.csv", ["trade","product_families","document_types_needed"], coverage)

payload = {
    "brand_document_hubs": [dict(zip(["trade","brand","equipment_scope","resource_name","resource_types","url","source_type","notes"], r)) for r in brand_sources],
    "exact_manual_index": [dict(zip(["trade","brand","product_family","series","model","equipment","document_type","document_title","url","format","key_specs","audience","notes"], r)) for r in exact_manuals],
    "lookup_rules": [dict(zip(["topic","rule","caution"], r)) for r in lookup_rules],
    "troubleshooting_topics": [dict(zip(["trade","problem","first_checks","needed_documents"], r)) for r in troubleshooting_topics],
    "trade_coverage": [dict(zip(["trade","product_families","document_types_needed"], r)) for r in coverage],
}
(OUT / "roofinghut_master_library.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

db = OUT / "roofinghut_master_library.sqlite"
if db.exists():
    db.unlink()
conn = sqlite3.connect(db)
cur = conn.cursor()
cur.execute("CREATE TABLE brand_document_hubs (trade TEXT, brand TEXT, equipment_scope TEXT, resource_name TEXT, resource_types TEXT, url TEXT, source_type TEXT, notes TEXT)")
cur.executemany("INSERT INTO brand_document_hubs VALUES (?,?,?,?,?,?,?,?)", brand_sources)
cur.execute("CREATE TABLE exact_manual_index (trade TEXT, brand TEXT, product_family TEXT, series TEXT, model TEXT, equipment TEXT, document_type TEXT, document_title TEXT, url TEXT, format TEXT, key_specs TEXT, audience TEXT, notes TEXT)")
cur.executemany("INSERT INTO exact_manual_index VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", exact_manuals)
cur.execute("CREATE TABLE lookup_rules (topic TEXT, rule TEXT, caution TEXT)")
cur.executemany("INSERT INTO lookup_rules VALUES (?,?,?)", lookup_rules)
cur.execute("CREATE TABLE troubleshooting_topics (trade TEXT, problem TEXT, first_checks TEXT, needed_documents TEXT)")
cur.executemany("INSERT INTO troubleshooting_topics VALUES (?,?,?,?)", troubleshooting_topics)
cur.execute("CREATE TABLE trade_coverage (trade TEXT, product_families TEXT, document_types_needed TEXT)")
cur.executemany("INSERT INTO trade_coverage VALUES (?,?,?)", coverage)
cur.execute("CREATE VIRTUAL TABLE search_index USING fts5(kind, trade, brand, title, body, url)")
for r in brand_sources:
    cur.execute("INSERT INTO search_index VALUES (?,?,?,?,?,?)", ("brand_hub", r[0], r[1], r[3], " ".join(r[:6] + (r[7],)), r[5]))
for r in exact_manuals:
    cur.execute("INSERT INTO search_index VALUES (?,?,?,?,?,?)", ("manual", r[0], r[1], r[7], " ".join(r[:8] + r[10:]), r[8]))
for r in troubleshooting_topics:
    cur.execute("INSERT INTO search_index VALUES (?,?,?,?,?,?)", ("troubleshooting", r[0], "", r[1], " ".join(r), ""))
conn.commit()
conn.close()

summary = f"""RoofingHut Master Library v2
Generated local searchable files:
- {len(brand_sources)} brand/source document hubs
- {len(exact_manuals)} exact manual records
- {len(lookup_rules)} lookup rules
- {len(troubleshooting_topics)} troubleshooting topics
- {len(coverage)} trade coverage areas

Use roofinghut_master_library.sqlite for fast local search.
Use exact_manual_index.csv for model-specific answers.
Use brand_document_hubs.csv when exact model is not indexed yet.
"""
(OUT / "README_Master_Library_v2.txt").write_text(summary, encoding="utf-8")
print(summary)
