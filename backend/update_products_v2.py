"""
Update products database according to new requirements
- Remove Tongtai and Graco
- Update manufacturers and descriptions
- Remove/add products as specified
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime, timezone
import uuid

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Updated products data
UPDATED_PRODUCTS = [
    # ELECTRONIC ASSEMBLY PRODUCTS
    {
        "name": "Pick and Place Machine",
        "category": "Electronic Assembly Products",
        "description": "High-speed, high-flexibility component placement system for SMT assembly with advanced vision alignment and multi-head configuration",
        "features": [
            "High-speed component placement",
            "Multiple feeder capacity",
            "Vision-guided placement",
            "Component range from 0201 to large ICs",
            "Intuitive programming interface",
            "High-mix flexibility"
        ],
        "manufacturer": "Mycronic",
        "is_featured": True
    },
    {
        "name": "Jet Printer",
        "category": "Electronic Assembly Products",
        "description": "Advanced contactless jetting technology for precise solder paste and adhesive dispensing with programmable patterns",
        "features": [
            "Contactless jet dispensing",
            "High-precision material application",
            "Flexible pattern programming",
            "No stencil required",
            "Reduced material waste"
        ],
        "manufacturer": "Mycronic",
        "is_featured": True
    },
    {
        "name": "SMD Component Tower",
        "category": "Electronic Assembly Products",
        "description": "Automated vertical storage and retrieval system for SMT component management",
        "features": [
            "Automated component storage",
            "Quick component retrieval",
            "Integration with pick and place",
            "Space-saving vertical design",
            "Inventory management"
        ],
        "is_featured": False
    },
    {
        "name": "Stencil Printing Machine",
        "category": "Electronic Assembly Products",
        "description": "High-precision automated stencil printer for consistent solder paste application",
        "features": [
            "Automated vision alignment",
            "Programmable print parameters",
            "Consistent paste deposit control",
            "Quick stencil changeover",
            "3D inspection capability"
        ],
        "manufacturer": "HCX",
        "is_featured": False
    },
    {
        "name": "Solder Paste Screen Printer",
        "category": "Electronic Assembly Products",
        "description": "Precision screen printing system for high-volume solder paste application with automated features",
        "features": [
            "Dual-rail transport system",
            "Automatic paste replenishment",
            "Vision alignment system",
            "Industry 4.0 ready",
            "Real-time process monitoring"
        ],
        "manufacturer": "HCX Mycronic",
        "is_featured": False
    },
    {
        "name": "3D Solder Paste Inspection (SPI)",
        "category": "Electronic Assembly Products",
        "description": "Advanced 3D inspection system for solder paste quality control and process optimization",
        "features": [
            "3D height measurement",
            "Volume and area calculation",
            "Real-time process feedback",
            "Statistical process control",
            "Automatic defect detection"
        ],
        "manufacturer": "Mirtec",
        "is_featured": True
    },
    {
        "name": "3D Auto Optical Inspection (AOI)",
        "category": "Electronic Assembly Products",
        "description": "Automated 3D optical inspection for comprehensive SMT assembly defect detection",
        "features": [
            "3D imaging technology",
            "Component presence/absence detection",
            "Polarity and orientation verification",
            "Solder joint quality analysis",
            "High-resolution inspection"
        ],
        "manufacturer": "Mirtec",
        "is_featured": True
    },
    {
        "name": "PCB Magazine Loader",
        "category": "Electronic Assembly Products",
        "description": "Automated PCB loading system for seamless SMT line integration",
        "features": [
            "Automatic board loading",
            "SMEMA compatible",
            "Adjustable magazine capacity",
            "Gentle board handling",
            "Production line integration"
        ],
        "manufacturer": "YJ Link",
        "is_featured": False
    },
    {
        "name": "PCB Magazine Unloader",
        "category": "Electronic Assembly Products",
        "description": "Automated PCB unloading system for efficient SMT line completion",
        "features": [
            "Automatic board unloading",
            "SMEMA compatible",
            "Sorting capability",
            "Buffer management",
            "Production line integration"
        ],
        "manufacturer": "YJ Link",
        "is_featured": False
    },
    {
        "name": "Reflow Oven",
        "category": "Electronic Assembly Products",
        "description": "Multi-zone reflow oven for precise temperature profile control during solder reflow process",
        "features": [
            "Multiple independent heating zones",
            "Nitrogen capability",
            "Temperature profiling system",
            "Energy efficient design",
            "Forced convection heating"
        ],
        "manufacturer": "JT, SMT",
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
            "Nitrogen atmosphere option",
            "Programmable conveyor speed"
        ],
        "manufacturer": "JT",
        "is_featured": False
    },
    {
        "name": "AGV (Automated Guided Vehicle)",
        "category": "Electronic Assembly Products",
        "description": "Autonomous material transport system for factory automation and logistics",
        "features": [
            "Autonomous navigation",
            "SMEMA integration",
            "Wireless communication",
            "Safety sensors",
            "Flexible routing"
        ],
        "manufacturer": "YJ Link",
        "is_featured": False
    },
    {
        "name": "High Performance Dispensing Machine",
        "category": "Electronic Assembly Products",
        "description": "Precision dispensing system for adhesives, sealants, and coatings",
        "features": [
            "Multi-axis motion control",
            "Vision-guided dispensing",
            "Various material compatibility",
            "Programmable patterns",
            "High accuracy"
        ],
        "manufacturer": "Axxon",
        "is_featured": False
    },

    # ASSEMBLY TOOLS
    {
        "name": "Robotic Soldering System",
        "category": "Assembly Tools",
        "description": "Automated robotic soldering system for precision soldering operations",
        "features": [
            "Programmable soldering paths",
            "Consistent solder joint quality",
            "Multiple tip configurations",
            "Temperature control system",
            "High repeatability"
        ],
        "manufacturer": "Apollo Seiko",
        "is_featured": True
    },
    {
        "name": "BGA Rework System",
        "category": "Assembly Tools",
        "description": "Professional BGA component removal and replacement system",
        "features": [
            "Precision placement accuracy",
            "Split vision system",
            "Profile-controlled heating",
            "Component library database",
            "X-ray integration option"
        ],
        "manufacturer": "PACE",
        "is_featured": True
    },
    {
        "name": "Soldering/Desoldering Station",
        "category": "Assembly Tools",
        "description": "Professional soldering and desoldering workstation for precision work",
        "features": [
            "Temperature controlled tips",
            "Vacuum desoldering capability",
            "ESD safe design",
            "Multiple tip options",
            "Digital temperature display"
        ],
        "manufacturer": "PACE",
        "is_featured": False
    },
    {
        "name": "SMT Form & Trim System",
        "category": "Assembly Tools",
        "description": "Automated system for component lead forming and trimming",
        "features": [
            "Automatic component forming",
            "Precision lead cutting",
            "Multiple component compatibility",
            "Adjustable parameters",
            "High throughput"
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
            "Inline integration",
            "Nitrogen atmosphere"
        ],
        "is_featured": False
    },
    {
        "name": "Selective Soldering System",
        "category": "Assembly Tools",
        "description": "Precision selective soldering equipment for targeted solder application",
        "features": [
            "Precise joint targeting",
            "Programmable soldering paths",
            "Flux management",
            "Minimal thermal stress",
            "Flexible positioning"
        ],
        "is_featured": False
    },
    {
        "name": "Tabletop Wave Soldering",
        "category": "Assembly Tools",
        "description": "Compact wave soldering machine for small-scale production",
        "features": [
            "Benchtop design",
            "Mini wave solder pot",
            "Programmable parameters",
            "Cost-effective solution",
            "Quick setup"
        ],
        "manufacturer": "EPS",
        "is_featured": False
    },
    {
        "name": "Auto Screwing Machine",
        "category": "Assembly Tools",
        "description": "Automated screw driving system for assembly automation",
        "features": [
            "Programmable patterns",
            "Torque control",
            "Multiple screw sizes",
            "Fast cycle time",
            "Precision positioning"
        ],
        "manufacturer": "KTC",
        "is_featured": False
    },
    {
        "name": "Industrial Workbenches",
        "category": "Assembly Tools",
        "description": "Ergonomic industrial workbenches for electronics assembly",
        "features": [
            "ESD safe surfaces",
            "Adjustable height",
            "Modular accessories",
            "Durable construction",
            "Cable management"
        ],
        "manufacturer": "TRESTON",
        "is_featured": False
    },
    {
        "name": "Fume Extractor",
        "category": "Assembly Tools",
        "description": "Professional fume extraction system for soldering operations",
        "features": [
            "HEPA filtration",
            "Multiple extraction arms",
            "Quiet operation",
            "Energy efficient",
            "Adjustable airflow"
        ],
        "manufacturer": "BOFA",
        "is_featured": False
    },
    {
        "name": "Vapour Degreaser",
        "category": "Assembly Tools",
        "description": "Industrial vapor degreasing system for precision cleaning",
        "features": [
            "Solvent vapor cleaning",
            "Automated process",
            "Environmentally controlled",
            "Multiple chamber sizes",
            "Efficient cleaning"
        ],
        "manufacturer": "CCH",
        "is_featured": False
    },
    {
        "name": "Conformal Coating System",
        "category": "Assembly Tools",
        "description": "Automated conformal coating system for PCB protection",
        "features": [
            "Selective coating",
            "UV or thermal cure",
            "Programmable patterns",
            "Easy material changeover",
            "Precise application"
        ],
        "manufacturer": "Axxon",
        "is_featured": False
    },

    # INSPECTION AND TESTING
    {
        "name": "X-Ray Inspection System",
        "category": "Inspection and Testing",
        "description": "Advanced X-ray inspection for BGA, QFN, and hidden solder joint analysis",
        "features": [
            "Sub-micron resolution",
            "Automated BGA void analysis",
            "2D/3D imaging capability",
            "Real-time inspection",
            "70° oblique viewing",
            "Component counting"
        ],
        "manufacturer": "Nordson DAGE",
        "is_featured": True
    },
    {
        "name": "Inline X-Ray Inspection",
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
        "name": "Compact X-Ray System",
        "category": "Inspection and Testing",
        "description": "Benchtop X-ray inspection for lab and small-scale production",
        "features": [
            "Compact design",
            "High resolution imaging",
            "User-friendly interface",
            "Cost-effective solution",
            "Versatile applications"
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
            "Pass/fail criteria",
            "Cleanliness verification"
        ],
        "is_featured": False
    },
    {
        "name": "Component Counter",
        "category": "Inspection and Testing",
        "description": "X-ray based component counting system for inventory management",
        "features": [
            "Non-destructive counting",
            "High accuracy",
            "Multiple reel sizes",
            "Database integration",
            "Quick verification"
        ],
        "manufacturer": "V-count",
        "is_featured": False
    },
    {
        "name": "Inline Component Counter",
        "category": "Inspection and Testing",
        "description": "Inline X-ray component counting for real-time inventory tracking",
        "features": [
            "Real-time counting",
            "Production line integration",
            "Automated data capture",
            "Traceability support",
            "Inventory management"
        ],
        "manufacturer": "V-count",
        "is_featured": False
    },
    {
        "name": "Thermal Profiler",
        "category": "Inspection and Testing",
        "description": "Advanced thermal profiling system for reflow oven optimization",
        "features": [
            "Multiple thermocouple inputs",
            "Real-time monitoring",
            "Profile optimization software",
            "SPC charting",
            "Data logging"
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
            "Flexible programming",
            "Cost-effective"
        ],
        "manufacturer": "Digital Test",
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
            "High throughput",
            "Comprehensive test coverage"
        ],
        "manufacturer": "Digital Test",
        "is_featured": True
    },
    {
        "name": "PCB and Stencil Cleaning System (Batch)",
        "category": "Inspection and Testing",
        "description": "Batch cleaning system for PCBs and stencils using aqueous solutions",
        "features": [
            "Batch processing capability",
            "Environmentally friendly",
            "Effective flux removal",
            "Automated cleaning cycle",
            "Drying system included"
        ],
        "manufacturer": "Aqueous",
        "is_featured": False
    },
    {
        "name": "PCB and Stencil Cleaning System (Inline)",
        "category": "Inspection and Testing",
        "description": "Inline cleaning system for continuous PCB and stencil cleaning",
        "features": [
            "Inline processing",
            "High throughput",
            "Automated operation",
            "Water-based cleaning",
            "Quick dry cycle"
        ],
        "manufacturer": "AAT",
        "is_featured": False
    },
    {
        "name": "Bond Tester",
        "category": "Inspection and Testing",
        "description": "Wire bond pull and shear testing equipment for quality control",
        "features": [
            "Pull test capability",
            "Shear test capability",
            "Force measurement",
            "Statistical analysis",
            "Data logging"
        ],
        "manufacturer": "Nordson",
        "is_featured": False
    },

    # SEMICONDUCTOR
    {
        "name": "AccoTEST Functional Tester",
        "category": "Semiconductor",
        "description": "Advanced functional test equipment for comprehensive semiconductor device testing",
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
        "description": "High-performance test handler for automated semiconductor device handling",
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
        "name": "Plasma Cleaner",
        "category": "Semiconductor",
        "description": "Plasma cleaning system for surface preparation in semiconductor manufacturing",
        "features": [
            "Atmospheric plasma",
            "Surface activation",
            "Improved bonding",
            "Contamination removal",
            "Gentle process"
        ],
        "manufacturer": "Nordson",
        "is_featured": True
    },
    {
        "name": "FlexTrack Plasma System",
        "category": "Semiconductor",
        "description": "Flexible plasma treatment system for various substrate types",
        "features": [
            "Flexible substrate handling",
            "Inline processing",
            "Uniform treatment",
            "Process monitoring",
            "Automated control"
        ],
        "manufacturer": "Nordson",
        "is_featured": False
    },
    {
        "name": "Plasma Dicing System",
        "category": "Semiconductor",
        "description": "Advanced plasma dicing technology for wafer singulation",
        "features": [
            "Damage-free dicing",
            "High die strength",
            "Ultra-thin wafer capability",
            "Clean process",
            "Improved yield"
        ],
        "manufacturer": "PVA TePla",
        "is_featured": True
    },
    {
        "name": "Manual Die Bonder",
        "category": "Semiconductor",
        "description": "Precision manual die bonding system for semiconductor packaging",
        "features": [
            "High placement accuracy",
            "Vision alignment",
            "Multiple die sizes",
            "Heated work holder",
            "Flexible operation"
        ],
        "manufacturer": "TRESKY",
        "is_featured": False
    },
    {
        "name": "Dual Semi-Auto Wire Bonder",
        "category": "Semiconductor",
        "description": "Dual-head semi-automatic wire bonding system",
        "features": [
            "Dual bonding heads",
            "Semi-automatic operation",
            "Gold/aluminum wire",
            "Ball/wedge bonding",
            "High productivity"
        ],
        "manufacturer": "Micropoint",
        "is_featured": False
    },
    {
        "name": "Semi-Auto Solder Ball Attach Machine",
        "category": "Semiconductor",
        "description": "Semi-automatic system for precise BGA solder ball attachment",
        "features": [
            "Precise ball placement",
            "Flux application system",
            "Vision alignment",
            "Various ball sizes",
            "High accuracy"
        ],
        "manufacturer": "KOSES",
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
            "Color calibration",
            "Comprehensive analysis"
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
            "Quality verification",
            "Automated process"
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
            "High throughput",
            "Quality control"
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
            "Functional verification",
            "Advanced diagnostics"
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
            "Clean application",
            "Uniform coverage"
        ],
        "is_featured": False
    },

    # NON-DESTRUCTIVE TESTING
    {
        "name": "PVA TePla Scanning Acoustic Microscope (SAM)",
        "category": "Non Destructive Testing",
        "description": "Advanced SAM system for subsurface defect detection and material analysis",
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
            "Reflow simulation",
            "Data analysis"
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
            "Advanced software",
            "Comprehensive reporting"
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
            "Expert consultation",
            "Detailed reporting"
        ],
        "is_featured": False
    },

    # MECHANICAL
    {
        "name": "CNC Machining Center",
        "category": "Mechanical",
        "description": "High-precision CNC machining center for metal and plastic processing",
        "features": [
            "Vertical/horizontal machining",
            "5-axis capability",
            "High-speed spindle",
            "Precision control",
            "Automatic tool change"
        ],
        "is_featured": False
    },
    {
        "name": "PCB Drilling Machine",
        "category": "Mechanical",
        "description": "Precision drilling machine for PCB manufacturing",
        "features": [
            "Multiple spindles",
            "High-speed drilling",
            "Vision alignment",
            "Automatic tool change",
            "Depth control"
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
            "Multiple tool support",
            "Quick setup"
        ],
        "is_featured": False
    }
]

async def update_database():
    """Update products database with new requirements"""
    try:
        print("Starting database update...")
        
        # Delete existing products
        result = await db.products.delete_many({})
        print(f"✅ Deleted {result.deleted_count} existing products")
        
        # Delete Tongtai and Graco partnerships
        result_partnerships = await db.partnerships.delete_many({
            "company_name": {"$in": ["Tongtai", "Graco"]}
        })
        print(f"✅ Deleted {result_partnerships.deleted_count} partnerships (Tongtai, Graco)")
        
        # Insert new products
        inserted_count = 0
        for product_data in UPDATED_PRODUCTS:
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
        
        print(f"✅ Successfully inserted {inserted_count} updated products")
        
        # Print summary by category
        print("\n📊 Updated Products by Category:")
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
        
        # Print partnership count
        partnership_count = await db.partnerships.count_documents({})
        print(f"\n📊 Remaining Partnerships: {partnership_count}")
        
        return inserted_count
        
    except Exception as e:
        print(f"❌ Error updating database: {str(e)}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(update_database())
