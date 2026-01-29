
import re

class TaxonomyClassifier:
    def __init__(self):
        # Mapping definition: Theme -> {Sector Filter (set of GICS Sector/Sub-Industries), Keywords (list)}
        self.rules = {
            "AI": {
                "sectors": {"Information Technology", "Communication Services", "Semiconductors", "Application Software", "Systems Software", "Technology Hardware, Storage & Peripherals"},
                "keywords": [r"artificial intelligence", r"\bai\b", r"machine learning", r"neural network", r"generative ai", r"deep learning", r"gpu", r"large language model", r"openai", r"copilot"]
            },
            "Semiconductor": {
                "sectors": {"Semiconductors", "Semiconductor Materials & Equipment", "Technology Hardware, Storage & Peripherals", "Electronic Components"},
                "keywords": [r"semiconductor", r"microchip", r"integrated circuit", r"wafer", r"chipset", r"nand", r"dram", r"flash memory", r"solid-state drive", r"hard disk", r"processor", r"graphics card", r"cpu", r"gpu", r"foundry"]
            },
            "Memory & Storage": {
                "sectors": {"Technology Hardware, Storage & Peripherals", "Semiconductors"},
                "keywords": [r"nand", r"dram", r"dynamic random access memory", r"solid-state drive", r"hard disk", r"flash memory"]
            },
            "Cloud Computing": {
                "sectors": {"Information Technology", "Communication Services", "Internet Services & Infrastructure", "Systems Software", "IT Consulting & Other Services", "Application Software"},
                "keywords": [r"cloud", r"data center", r"saas", r"paas", r"iaas", r"server virtualization", r"web services", r"hosting"]
            },
            "Cybersecurity": {
                "sectors": {"Systems Software", "Application Software", "IT Consulting & Other Services"},
                "keywords": [r"cybersecurity", r"network security", r"firewall", r"threat detection", r"identity management", r"endpoint protection", r"security software", r"data security"]
            },
            "EV & Auto": {
                "sectors": {"Automobile Manufacturers", "Auto Parts & Equipment", "Automotive Retail", "Industrial Machinery & Supplies & Components"},
                "keywords": [r"electric vehicle", r"\bev\b", r"lithium-ion", r"battery pack", r"charging station", r"autonomous driving", r"electric motor", r"hybrid vehicle", r"powertrain"]
            },
            "Healthcare": {
                "sectors": {"Health Care", "Biotechnology", "Pharmaceuticals", "Health Care Equipment & Supplies", "Life Sciences Tools & Services"},
                "keywords": [r"pharmaceutical", r"biotechnology", r"medical device", r"drug discovery", r"life sciences", r"vaccine", r"health", r"biopharm"]
            },
            "Fintech": {
                "sectors": {"Financials", "Information Technology", "Consumer Finance", "Transaction & Payment Processing Services", "Financial Exch. & Data", "Application Software"},
                "keywords": [r"digital payment", r"fintech", r"mobile banking", r"electronic trading", r"payment processing", r"credit card", r"debit card", r"transaction processing", r"financial data", r"exchange"]
            },
            "Gaming": {
                "sectors": {"Interactive Home Entertainment", "Leisure Products", "Semiconductors", "Interactive Media & Services", "Systems Software", "Application Software"},
                "keywords": [r"video game", r"gaming", r"interactive entertainment", r"graphics processor", r"e-sports", r"electronic arts", r"playstation", r"xbox", r"nintendo", r"publish"]
            },
            "E-commerce": {
                "sectors": {"Broadline Retail", "Consumer Discretionary", "Consumer Staples", "Footwear", "Apparel, Accessories & Luxury Goods"},
                "keywords": [r"e-commerce", r"online retail", r"digital marketplace", r"internet shopping", r"online store", r"online marketplace", r"retail", r"fulfillment"]
            },
            "Energy": {
                "sectors": {"Energy", "Utilities", "Oil, Gas & Consumable Fuels", "Electric Utilities", "Multi-Utilities"},
                "keywords": [r"oil", r"gas", r"petroleum", r"renewable energy", r"solar", r"wind power", r"fossil fuel", r"electricity", r"power generation"]
            },
            "Defense": {
                "sectors": {"Aerospace & Defense"},
                "keywords": [r"defense", r"military", r"weapon", r"national security", r"aerospace", r"aircraft", r"missile", r"satellite"]
            },
            "Real Estate": {
                "sectors": {"Real Estate", "Office REITs", "Residential REITs", "Retail REITs", "Specialized REITs", "Health Care REITs"},
                "keywords": [r"reit", r"property management", r"real estate", r"commercial real estate", r"residential real estate", r"apartment"]
            },
            "Social Media": {
                "sectors": {"Interactive Media & Services", "Communication Services", "Advertising"},
                "keywords": [r"social network", r"social media", r"messaging platform", r"online community", r"user-generated content", r"advertising", r"video sharing", r"engagement", r"facebook", r"instagram", r"whatsapp", r"snapchat", r"pinterest", r"search engine"]
            },
            "Travel & Leisure": {
                "sectors": {"Hotels, Resorts & Cruise Lines", "Passenger Airlines", "Broadline Retail", "Casinos & Gaming", "Hotels, Restaurants & Leisure"},
                "keywords": [r"airline", r"hotel", r"cruise", r"booking", r"tourism", r"hospitality", r"vacation", r"casino", r"restaurant"]
            },
            "Robotics": {
                "sectors": {"Industrial Machinery & Supplies & Components", "Electrical Components & Equipment", "Healthcare Equipment", "Semiconductor Materials & Equipment", "Industrial Machinery", "Industrials"},
                "keywords": [r"robotics", r"industrial automation", r"autonomous machine", r"drone", r"mechatronics", r"manufacturing solution", r"surgical robot", r"test equipment", r"control system"]
            },
            "Blockchain": {
                "sectors": {"Financials", "Information Technology"},
                "keywords": [r"blockchain", r"cryptocurrency", r"bitcoin", r"digital asset", r"distributed ledger"]
            },
            "Streaming & Digital Media": {
                "sectors": {"Movies & Entertainment", "Interactive Media & Services", "Communication Services", "Entertainment"},
                "keywords": [r"streaming", r"content library", r"digital entertainment", r"subscription", r"broadcasting", r"video on demand", r"entertainment", r"music"]
            },
            "Infrastructure": {
                "sectors": {"Construction & Engineering", "Electrical Components & Equipment", "Industrial Conglomerates", "Industrial Machinery & Supplies & Components", "Rail Transportation", "Heavy Electrical Equipment", "Industrials"},
                "keywords": [r"infrastructure", r"construction", r"engineering", r"power grid", r"railway", r"bridge", r"tunnel", r"building and maintenance"]
            },
            "Building & Construction": {
                "sectors": {"Building Products", "Homebuilding", "Construction Materials", "Industrials"},
                "keywords": [r"building products", r"construction materials", r"homebuilding", r"interior products", r"cladding", r"roofing", r"piping"]
            },
            "Waste & Environmental": {
                "sectors": {"Environmental & Facilities Services", "Industrials"},
                "keywords": [r"waste management", r"recycling", r"environmental service", r"trash", r"sustainability solution"]
            },
            "Industrial Distribution": {
                "sectors": {"Trading Companies & Distributors", "Industrials"},
                "keywords": [r"distribution", r"supply chain", r"logistics solution", r"wholesale", r"industrial supply"]
            }
        }

    def classify(self, summary, sector="", sub_industry=""):
        """
        Classifies stock into themes based on Sector Guardrails + Keyword Verification.
        """
        if not summary:
            return []
            
        summary_lower = summary.lower()
        matched_tags = []
        
        # Sector/Sub-industry can sometimes be broad (e.g. 'Industrials')
        # We check both to be safe
        
        for theme, rule in self.rules.items():
            # Sector Guardrail
            sector_match = (not rule["sectors"]) or \
                          (sector in rule["sectors"]) or \
                          (sub_industry in rule["sectors"])
            
            if sector_match:
                # Keyword Verification
                for pattern in rule["keywords"]:
                    if re.search(pattern, summary_lower):
                        matched_tags.append(theme)
                        break
                        
        if not matched_tags and sub_industry and str(sub_industry).lower() != 'nan':
            return [str(sub_industry)]
            
        return matched_tags

# Singleton instance
_classifier = None

def get_classifier():
    global _classifier
    if _classifier is None:
        _classifier = TaxonomyClassifier()
    return _classifier
