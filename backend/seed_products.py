"""
Seed products from ASPL Line Card 2025 into MongoDB database
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Comprehensive product data from line card
PRODUCTS_DATA = [
    # ELECTRONIC ASSEMBLY PRODUCTS
    {
        "name": "Mycronic MYPro A40/A40DX Pick & Place Machine",
        "category": "Electronic Assembly Products",
        "description": "High-speed, high-flexibility pick-and-place platform for SMT assembly with 59,000 cph IPC-rated speed",
        "features": [
            "59,000 CPH placement speed (48% faster than MY300DX)",
            "224 × 8mm feeder capacity (expandable to 448)",
            "Component range: 0.3×0.15mm to 99×73×15mm",
            "MX7 mounthead with 7 independent nozzles",
            "Intuitive graphical touchscreen interface",
            "High-mix flexibility with on-the-fly optimization"
        ],
        "manufacturer": "Mycronic",
        "is_featured": True
    },
    {
        "name": "Mycronic My700 Jet Printer",
        "category": "Electronic Assembly Products",
        "description": "Advanced jet printing system for precise solder paste and adhesive dispensing",
        "features": [
            "Jet printing technology for contactless dispensing",
            "High-precision solder paste application",
            "Flexible programming for complex patterns",
            "Compatible with MYPro platform"
        ],
        "manufacturer": "Mycronic",
        "is_featured": True
    },
    {
        "name": "SMD Tower Component Handler",
        "category": "Electronic Assembly Products",
        "description": "Versatile SMT component handling system for automated component storage and retrieval",
        "features": [
            "Automated component storage",
            "Quick component changeover",
            "Integration with pick and place machines",
            "Space-saving vertical design"
        ],
        "is_featured": False
    },
    {
        "name": "Stencil Printing Machine",
        "category": "Electronic Assembly Products",
        "description": "High-precision stencil printer for solder paste application in SMT processes",
        "features": [
            "Automated vision alignment",
            "Programmable print parameters",
            "Consistent paste deposit control",
            "Quick stencil changeover"
        ],
        "is_featured": False
    },
    {
        "name": "HCX Mycronic Solder Paste Screen Printer",
        "category": "Electronic Assembly Products",
        "description": "Advanced screen printing equipment for high-volume solder paste application",
        "features": [
            "Dual-rail transport system",
            "3D inspection capability",
            "Automatic paste replenishment",
            "Industry 4.0 ready"
        ],
        "manufacturer": "Mycronic",
        "is_featured": False
    },
    {
        "name": "3D Solder Paste Inspection (SPI)",
        "category": "Electronic Assembly Products",
        "description": "Automated 3D inspection system for solder paste deposits quality control",
        "features": [
            "3D height measurement",
            "Volume and area calculation",
            "Real-time process feedback",
            "Statistical process control"
        ],
        "is_featured": True
    },
    {
        "name": "3D Auto Optical Inspection (AOI)",
        "category": "Electronic Assembly Products",
        "description": "Automated optical inspection for SMT assembly defect detection",
        "features": [
            "3D imaging technology",
            "Component presence/absence detection",
            "Polarity and orientation verification",
            "Solder joint quality analysis"
        ],
        "is_featured": True
    },
    {
        "name": "LED Automatic SMT Pick & Place",
        "category": "Electronic Assembly Products",
        "description": "Specialized pick and place machine optimized for high-speed LED placement",
        "features": [
            "High-speed LED placement",
            "Specialized LED handling nozzles",
            "Vision inspection for LED orientation",
            "Optimized for LED manufacturing"
        ],
        "is_featured": False
    },
    {
        "name": "Semi-Automatic Pick & Place",
        "category": "Electronic Assembly Products",
        "description": "Semi-automated component placement system for prototyping and low-volume production",
        "features": [
            "Manual loading with automated placement",
            "Suitable for R&D and prototyping",
            "Cost-effective for low volumes",
            "Easy programming interface"
        ],
        "is_featured": False
    },
    {
        "name": "PCB Magazine Loader",
        "category": "Electronic Assembly Products",
        "description": "Automated PCB loading system for SMT line integration",
        "features": [
            "Automatic board loading",
            "SMEMA compatible",
            "Adjustable magazine capacity",
            "Integration with production lines"
        ],
        "is_featured": False
    },
    {
        "name": "PCB Magazine Unloader",
        "category": "Electronic Assembly Products",
        "description": "Automated PCB unloading system for SMT line completion",
        "features": [
            "Automatic board unloading",
            "SMEMA compatible",
            "Gentle board handling",
            "Sorting capability"
        ],
        "is_featured": False
    },
    {
        "name": "JT 8/10 Zone Reflow Oven",
        "category": "Electronic Assembly Products",
        "description": "Multi-zone reflow oven for precise temperature profile control during soldering",
        "features": [
            "8 or 10 independent heating zones",
            "Nitrogen capability",
            "Temperature profiling system",
            "Energy efficient design"
        ],
        "manufacturer": "JT (Jintuo)",
        "is_featured": True
    },
    {
        "name": "Wave Soldering Machine",
        "category": "Electronic Assembly Products",
        "description": "Automated wave soldering system for through-hole component assembly",
        "features": [
            "Dual wave configuration",
            "Flux management system",
            "Preheat control",
            "Nitrogen atmosphere option"
        ],
        "is_featured": False
    },

    # ASSEMBLY TOOLS
    {
        "name": "Apollo Seiko Robotic Soldering System",
        "category": "Assembly Tools",
        "description": "Automated robotic soldering system for precision soldering operations",
        "features": [
            "Programmable soldering paths",
            "Consistent solder joint quality",
            "Multiple tip configurations",
            "Temperature control system"
        ],
        "manufacturer": "Apollo Seiko",
        "is_featured": True
    },
    {
        "name": "PACE BGA Rework System",
        "category": "Assembly Tools",
        "description": "Professional BGA component removal and replacement system",
        "features": [
            "Precision placement accuracy",
            "Split vision system",
            "Profile-controlled heating",
            "Component library database"
        ],
        "manufacturer": "PACE",
        "is_featured": True
    },
    {
        "name": "PACE Soldering/Desoldering Station",
        "category": "Assembly Tools",
        "description": "Professional soldering and desoldering workstation",
        "features": [
            "Temperature controlled tips",
            "Vacuum desoldering capability",
            "ESD safe design",
            "Multiple tip options"
        ],
        "manufacturer": "PACE",
        "is_featured": False
    },
    {
        "name": "Graco Mix and Dispense System",
        "category": "Assembly Tools",
        "description": "Precision mixing and dispensing system for adhesives, sealants, and potting materials",
        "features": [
            "Accurate material mixing",
            "Programmable dispense patterns",
            "Material flow control",
            "Compatible with various materials"
        ],
        "manufacturer": "Graco",
        "is_featured": True
    },
    {
        "name": "SMT Form & Trim System",
        "category": "Assembly Tools",
        "description": "Automated system for component lead forming and trimming",
        "features": [
            "Automatic component forming",
            "Precision lead cutting",
            "Multiple component compatibility",
            "Adjustable parameters"
        ],
        "is_featured": False
    },
    {
        "name": "KOSES Semi-Auto Solder Ball Attach Machine",
        "category": "Assembly Tools",
        "description": "Semi-automatic system for BGA solder ball attachment",
        "features": [
            "Precise ball placement",
            "Flux application system",
            "Vision alignment",
            "Various ball sizes"
        ],
        "manufacturer": "KOSES",
        "is_featured": False
    },
    {
        "name": "IBL Economic Vapor Phase Soldering",
        "category": "Assembly Tools",
        "description": "Cost-effective vapor phase soldering system for void-free solder joints",
        "features": [
            "Uniform heating profile",
            "Void-free solder joints",
            "No thermal shock",
            "Energy efficient"
        ],
        "manufacturer": "IBL",
        "is_featured": False
    },
    {
        "name": "Vacuum Vapor Phase Soldering Machine",
        "category": "Assembly Tools",
        "description": "Advanced vacuum vapor phase system for high-reliability applications",
        "features": [
            "Vacuum chamber operation",
            "Void elimination",
            "High-reliability soldering",
            "Controlled atmosphere"
        ],
        "is_featured": False
    },
    {
        "name": "In-Line Selective Soldering System",
        "category": "Assembly Tools",
        "description": "Automated selective soldering for mixed technology assemblies",
        "features": [
            "Precise solder application",
            "Multiple soldering heads",
            "Programmable patterns",
            "Inline integration"
        ],
        "is_featured": False
    },
    {
        "name": "EPS Tabletop Wave Soldering",
        "category": "Assembly Tools",
        "description": "Compact wave soldering machine for small-scale production",
        "features": [
            "Benchtop design",
            "Mini wave solder pot",
            "Programmable parameters",
            "Cost-effective solution"
        ],
        "manufacturer": "EPS",
        "is_featured": False
    },
    {
        "name": "3-Zone Reflow Oven",
        "category": "Assembly Tools",
        "description": "Compact reflow oven for small to medium production",
        "features": [
            "3 independent zones",
            "Forced convection",
            "Temperature monitoring",
            "Compact footprint"
        ],
        "is_featured": False
    },
    {
        "name": "5-Zone Reflow Oven",
        "category": "Assembly Tools",
        "description": "Mid-range reflow oven for consistent soldering profiles",
        "features": [
            "5 heating zones",
            "Profile storage",
            "Nitrogen ready",
            "Energy efficient"
        ],
        "is_featured": False
    },
    {
        "name": "KTC Auto Screw Machine",
        "category": "Assembly Tools",
        "description": "Automated screw driving system for assembly automation",
        "features": [
            "Programmable patterns",
            "Torque control",
            "Multiple screw sizes",
            "Fast cycle time"
        ],
        "manufacturer": "KTC",
        "is_featured": False
    },
    {
        "name": "TRESTON Industrial Workbenches",
        "category": "Assembly Tools",
        "description": "Ergonomic industrial workbenches for electronics assembly",
        "features": [
            "ESD safe surfaces",
            "Adjustable height",
            "Modular accessories",
            "Durable construction"
        ],
        "manufacturer": "TRESTON",
        "is_featured": False
    },
    {
        "name": "BOFA Fume Extractor",
        "category": "Assembly Tools",
        "description": "Professional fume extraction system for soldering operations",
        "features": [
            "HEPA filtration",
            "Multiple extraction arms",
            "Quiet operation",
            "Energy efficient"
        ],
        "manufacturer": "BOFA",
        "is_featured": False
    },
    {
        "name": "CCH Vapour Degreaser",
        "category": "Assembly Tools",
        "description": "Industrial vapor degreasing system for precision cleaning",
        "features": [
            "Solvent vapor cleaning",
            "Automated process",
            "Environmentally controlled",
            "Multiple chamber sizes"
        ],
        "manufacturer": "CCH",
        "is_featured": False
    },

    # INSPECTION AND TESTING
    {
        "name": "Nordson DAGE X-Ray Inspection System",
        "category": "Inspection and Testing",
        "description": "Advanced X-ray inspection for BGA, QFN, and hidden solder joint analysis",
        "features": [
            "Sub-micron resolution (<0.5µm)",
            "Automated BGA void analysis",
            "2D/3D imaging capability",
            "Real-time inspection",
            "70° oblique viewing",
            "Up to 10W X-ray power"
        ],
        "manufacturer": "Nordson DAGE",
        "is_featured": True
    },
    {
        "name": "Nordson MXI Quadra 7 Pro Inline X-Ray",
        "category": "Inspection and Testing",
        "description": "High-speed inline X-ray inspection system for production lines",
        "features": [
            "Inline inspection capability",
            "High throughput",
            "Automatic defect detection",
            "Statistical process control",
            "Industry 4.0 integration"
        ],
        "manufacturer": "Nordson",
        "is_featured": True
    },
    {
        "name": "Glenbrook Compact X-Ray System",
        "category": "Inspection and Testing",
        "description": "Benchtop X-ray inspection for lab and small-scale production",
        "features": [
            "Compact design",
            "High resolution imaging",
            "User-friendly interface",
            "Cost-effective solution"
        ],
        "manufacturer": "Glenbrook Technologies",
        "is_featured": False
    },
    {
        "name": "Ionic Contamination Tester",
        "category": "Inspection and Testing",
        "description": "Equipment for measuring ionic contamination on PCB assemblies",
        "features": [
            "IPC standards compliance",
            "Automated testing",
            "Data logging",
            "Pass/fail criteria"
        ],
        "is_featured": False
    },
    {
        "name": "V-count XRH Count Component Counter",
        "category": "Inspection and Testing",
        "description": "X-ray based component counting system for inventory management",
        "features": [
            "Non-destructive counting",
            "High accuracy",
            "Multiple reel sizes",
            "Database integration"
        ],
        "manufacturer": "V-count",
        "is_featured": False
    },
    {
        "name": "V-count XRH Count Inline",
        "category": "Inspection and Testing",
        "description": "Inline X-ray component counting for real-time inventory tracking",
        "features": [
            "Real-time counting",
            "Production line integration",
            "Automated data capture",
            "Traceability support"
        ],
        "manufacturer": "V-count",
        "is_featured": False
    },
    {
        "name": "KIC Thermal Profiler",
        "category": "Inspection and Testing",
        "description": "Advanced thermal profiling system for reflow oven optimization",
        "features": [
            "Multiple thermocouple inputs",
            "Real-time monitoring",
            "Profile optimization software",
            "SPC charting"
        ],
        "manufacturer": "KIC",
        "is_featured": False
    },
    {
        "name": "Flying Probe Tester",
        "category": "Inspection and Testing",
        "description": "Fixtureless electrical testing system for PCB assemblies",
        "features": [
            "No test fixture required",
            "Rapid test development",
            "High accuracy",
            "Flexible programming"
        ],
        "is_featured": True
    },
    {
        "name": "In-Circuit Tester (ICT)",
        "category": "Inspection and Testing",
        "description": "High-speed in-circuit testing for component verification",
        "features": [
            "Component value testing",
            "Short/open detection",
            "Boundary scan",
            "High throughput"
        ],
        "is_featured": True
    },
    {
        "name": "Aqueous Cleaning System",
        "category": "Inspection and Testing",
        "description": "Water-based cleaning system for post-assembly flux removal",
        "features": [
            "Environmentally friendly",
            "Effective flux removal",
            "Automated process",
            "Drying system included"
        ],
        "is_featured": False
    },

    # SEMICONDUCTOR
    {
        "name": "AccoTEST Functional Tester",
        "category": "Semiconductor",
        "description": "Advanced functional test equipment from AccoTEST Global for comprehensive device testing",
        "features": [
            "Comprehensive test coverage",
            "High throughput capability",
            "Flexible test configuration",
            "Automated test programs",
            "Real-time diagnostics"
        ],
        "manufacturer": "AccoTEST Global",
        "is_featured": True
    },
    {
        "name": "JHT Pick & Place Test Handler",
        "category": "Semiconductor",
        "description": "High-performance test handler from JHT Semiconductors for automated device handling",
        "features": [
            "Automated device handling",
            "High accuracy placement",
            "Quick changeover capability",
            "Temperature control options",
            "Integration with ATE systems"
        ],
        "manufacturer": "JHT Semiconductors",
        "is_featured": True
    },
    {
        "name": "Nordson Plasma Cleaner",
        "category": "Semiconductor",
        "description": "Plasma cleaning system for surface preparation in semiconductor manufacturing",
        "features": [
            "Atmospheric plasma",
            "Surface activation",
            "Improved bonding",
            "Contamination removal"
        ],
        "manufacturer": "Nordson",
        "is_featured": True
    },
    {
        "name": "Nordson FlexTrack Plasma System",
        "category": "Semiconductor",
        "description": "Flexible plasma treatment system for various substrate types",
        "features": [
            "Flexible substrate handling",
            "Inline processing",
            "Uniform treatment",
            "Process monitoring"
        ],
        "manufacturer": "Nordson",
        "is_featured": False
    },
    {
        "name": "PVA TePla Plasma Dicing System",
        "category": "Semiconductor",
        "description": "Advanced plasma dicing technology for wafer singulation",
        "features": [
            "Damage-free dicing",
            "High die strength",
            "Ultra-thin wafer capability",
            "Clean process"
        ],
        "manufacturer": "PVA TePla",
        "is_featured": True
    },
    {
        "name": "TRESKY Manual Die Bonder",
        "category": "Semiconductor",
        "description": "Precision manual die bonding system for semiconductor packaging",
        "features": [
            "High placement accuracy",
            "Vision alignment",
            "Multiple die sizes",
            "Heated work holder"
        ],
        "manufacturer": "TRESKY",
        "is_featured": False
    },
    {
        "name": "Micropoint Dual Semi-Auto Wire Bonder",
        "category": "Semiconductor",
        "description": "Dual-head semi-automatic wire bonding system",
        "features": [
            "Dual bonding heads",
            "Semi-automatic operation",
            "Gold/aluminum wire",
            "Ball/wedge bonding"
        ],
        "manufacturer": "Micropoint",
        "is_featured": False
    },
    {
        "name": "Bond Tester",
        "category": "Semiconductor",
        "description": "Wire bond pull and shear testing equipment",
        "features": [
            "Pull test capability",
            "Shear test capability",
            "Force measurement",
            "Statistical analysis"
        ],
        "is_featured": False
    },
    {
        "name": "Camera Module Tester",
        "category": "Semiconductor",
        "description": "Specialized testing equipment for camera module quality verification",
        "features": [
            "Image quality testing",
            "Resolution verification",
            "Auto-focus testing",
            "Color calibration"
        ],
        "is_featured": False
    },
    {
        "name": "Lens Cell Assembly System",
        "category": "Semiconductor",
        "description": "Automated system for precision lens cell assembly",
        "features": [
            "High precision assembly",
            "Vision alignment",
            "Adhesive dispensing",
            "Quality verification"
        ],
        "is_featured": False
    },
    {
        "name": "Lens Module Assembly System",
        "category": "Semiconductor",
        "description": "Complete lens module assembly automation",
        "features": [
            "Multi-element assembly",
            "Active alignment",
            "Automated testing",
            "High throughput"
        ],
        "is_featured": False
    },
    {
        "name": "SIP (System in Package) Test System",
        "category": "Semiconductor",
        "description": "Comprehensive testing solution for system-in-package devices",
        "features": [
            "Multi-chip testing",
            "High-speed interface",
            "Thermal testing",
            "Functional verification"
        ],
        "is_featured": False
    },
    {
        "name": "2-Sided Flux Application System",
        "category": "Semiconductor",
        "description": "Dual-side flux application for semiconductor packaging",
        "features": [
            "Both-side application",
            "Precise flux control",
            "Automated process",
            "Clean application"
        ],
        "is_featured": False
    },

    # NON-DESTRUCTIVE TESTING
    {
        "name": "PVA TePla Scanning Acoustic Microscope (SAM)",
        "category": "Non Destructive Testing",
        "description": "Advanced SAM system from PVA TePla AS for subsurface defect detection",
        "features": [
            "High-resolution acoustic imaging",
            "Subsurface defect detection",
            "Delamination analysis",
            "Void detection",
            "Non-destructive analysis",
            "Material characterization"
        ],
        "manufacturer": "PVA TePla AS",
        "is_featured": True
    },
    {
        "name": "INSIDIX TDM Compact",
        "category": "Non Destructive Testing",
        "description": "Compact thermo-mechanical deformation measurement system",
        "features": [
            "Warpage measurement",
            "Temperature profiling",
            "Real-time monitoring",
            "Reflow simulation"
        ],
        "manufacturer": "INSIDIX",
        "is_featured": True
    },
    {
        "name": "INSIDIX TDM Compact 3",
        "category": "Non Destructive Testing",
        "description": "Advanced third-generation TDM system for warpage analysis",
        "features": [
            "3D warpage mapping",
            "Enhanced accuracy",
            "Larger measurement area",
            "Advanced software"
        ],
        "manufacturer": "INSIDIX",
        "is_featured": True
    },
    {
        "name": "Acoustic Microscopy Services",
        "category": "Non Destructive Testing",
        "description": "Professional microscopy and analytical services for failure analysis",
        "features": [
            "Failure analysis",
            "Cross-section analysis",
            "Material characterization",
            "Expert consultation"
        ],
        "is_featured": False
    },

    # MECHANICAL
    {
        "name": "Tongtai CNC Machining Center",
        "category": "Mechanical",
        "description": "High-precision CNC machining center from Tongtai for metal and plastic processing",
        "features": [
            "Vertical/horizontal machining",
            "5-axis capability",
            "High-speed spindle",
            "Precision control"
        ],
        "manufacturer": "Tongtai",
        "is_featured": True
    },
    {
        "name": "PCB Drilling Machine",
        "category": "Mechanical",
        "description": "Precision drilling machine for PCB manufacturing",
        "features": [
            "Multiple spindles",
            "High-speed drilling",
            "Vision alignment",
            "Automatic tool change"
        ],
        "is_featured": False
    },
    {
        "name": "PCB Routing Machine",
        "category": "Mechanical",
        "description": "CNC routing system for PCB depaneling and profiling",
        "features": [
            "Precision routing",
            "Dust collection",
            "Programmable paths",
            "Multiple tool support"
        ],
        "is_featured": False
    },

    # ADDITIONAL EQUIPMENT
    {
        "name": "High Performance Dispensing Machine",
        "category": "Electronic Assembly Products",
        "description": "Precision dispensing system for adhesives, sealants, and coatings",
        "features": [
            "Multi-axis motion control",
            "Vision-guided dispensing",
            "Various material compatibility",
            "Programmable patterns"
        ],
        "is_featured": False
    },
    {
        "name": "Benchtop Conformal Coating System",
        "category": "Assembly Tools",
        "description": "Compact conformal coating application system",
        "features": [
            "Selective coating",
            "UV or thermal cure",
            "Programmable patterns",
            "Easy material changeover"
        ],
        "is_featured": False
    },
    {
        "name": "Conformal Coating Machine",
        "category": "Assembly Tools",
        "description": "Automated conformal coating system for PCB protection",
        "features": [
            "Automated spray/dip coating",
            "Masking capability",
            "Uniform coverage",
            "Curing system"
        ],
        "is_featured": False
    },
    {
        "name": "AGV (Automated Guided Vehicle)",
        "category": "Electronic Assembly Products",
        "description": "Autonomous material transport system for factory automation",
        "features": [
            "Autonomous navigation",
            "SMEMA integration",
            "Wireless communication",
            "Safety sensors"
        ],
        "is_featured": False
    },
    {
        "name": "BPM Universal Programming Station",
        "category": "Inspection and Testing",
        "description": "Universal device programmer for microcontrollers and memory devices",
        "features": [
            "Wide device support",
            "Gang programming",
            "Stand-alone operation",
            "PC interface"
        ],
        "manufacturer": "BPM",
        "is_featured": False
    }
]

async def seed_products():
    """Seed products database with line card equipment"""
    try:
        print("Starting product database seeding...")
        
        # Clear existing products
        result = await db.products.delete_many({})
        print(f"Cleared {result.deleted_count} existing products")
        
        # Insert new products
        inserted_count = 0
        for product_data in PRODUCTS_DATA:
            from datetime import datetime, timezone
            import uuid
            
            product_doc = {
                "id": str(uuid.uuid4()),
                "name": product_data["name"],
                "category": product_data["category"],
                "description": product_data["description"],
                "features": product_data.get("features", []),
                "image_url": product_data.get("image_url"),
                "brochure_url": product_data.get("brochure_url"),
                "manufacturer": product_data.get("manufacturer"),
                "is_featured": product_data.get("is_featured", False),
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            
            await db.products.insert_one(product_doc)
            inserted_count += 1
        
        print(f"✅ Successfully inserted {inserted_count} products")
        
        # Print summary by category
        print("\n📊 Products by Category:")
        for category in [
            "Electronic Assembly Products",
            "Assembly Tools",
            "Inspection and Testing",
            "Semiconductor",
            "Non Destructive Testing",
            "Mechanical"
        ]:
            count = await db.products.count_documents({"category": category})
            print(f"  - {category}: {count} products")
        
        return inserted_count
        
    except Exception as e:
        print(f"❌ Error seeding products: {str(e)}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(seed_products())
