"""
Regenerate Semiconductor product category based on official semiconductor brochure
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

# Complete semiconductor product line from official brochure
SEMICONDUCTOR_PRODUCTS = [
    # WAFER HANDLING EQUIPMENT
    {
        "name": "Wafer Taping / Laminator / Mounter",
        "category": "Semiconductor",
        "description": "Advanced wafer handling equipment for taping, laminating, and mounting operations in semiconductor manufacturing",
        "features": [
            "Precise wafer taping capability",
            "Lamination process control",
            "Automated mounting system",
            "High throughput processing",
            "Clean room compatible"
        ],
        "is_featured": False
    },
    {
        "name": "Wafer Back Grinder",
        "category": "Semiconductor",
        "description": "Precision wafer back grinding system for wafer thinning and surface preparation",
        "features": [
            "Ultra-thin wafer capability",
            "Precise thickness control",
            "Automated grinding process",
            "High uniformity",
            "Damage-free processing"
        ],
        "is_featured": False
    },
    {
        "name": "Wafer Bump 3D AOI Inspection",
        "category": "Semiconductor",
        "description": "Advanced 3D Automated Optical Inspection system for comprehensive wafer bump quality verification",
        "features": [
            "3D inspection technology",
            "High-resolution imaging",
            "Automated defect detection",
            "Bump height measurement",
            "Coplanarity analysis",
            "Real-time quality control"
        ],
        "is_featured": True
    },
    {
        "name": "Plasma Dicing System",
        "category": "Semiconductor",
        "description": "Advanced plasma-based wafer dicing technology for damage-free die separation",
        "features": [
            "Plasma dicing technology",
            "Damage-free singulation",
            "Ultra-thin wafer capability",
            "High die strength",
            "Clean process",
            "Improved yield"
        ],
        "manufacturer": "PVA TePla",
        "is_featured": True
    },
    {
        "name": "Wafer Dicing Surfactant & Injection System",
        "category": "Semiconductor",
        "description": "Integrated surfactant injection system for improved wafer dicing quality and blade life",
        "features": [
            "Automated surfactant injection",
            "Precise flow control",
            "Extended blade life",
            "Improved cut quality",
            "Reduced particle contamination"
        ],
        "is_featured": False
    },
    {
        "name": "Particle Cleaning Surfactant",
        "category": "Semiconductor",
        "description": "Specialized surfactant solution for effective particle removal from wafer surfaces",
        "features": [
            "High particle removal efficiency",
            "Compatible with various wafer types",
            "Low residue formula",
            "Clean room certified",
            "Safe for sensitive surfaces"
        ],
        "is_featured": False
    },
    
    # INSPECTION EQUIPMENT
    {
        "name": "X-Ray Inspection System",
        "category": "Semiconductor",
        "description": "Advanced X-ray inspection for non-destructive analysis of semiconductor packages and assemblies",
        "features": [
            "Sub-micron resolution",
            "2D/3D imaging capability",
            "Void detection",
            "Wire bond inspection",
            "Package analysis",
            "Automated defect detection"
        ],
        "manufacturer": "Nordson",
        "is_featured": True
    },
    {
        "name": "Scanning Acoustic Microscopy (CSAM)",
        "category": "Semiconductor",
        "description": "Non-destructive acoustic imaging for delamination and void detection in semiconductor packages",
        "features": [
            "High-resolution acoustic imaging",
            "Subsurface defect detection",
            "Delamination analysis",
            "Multiple frequency scanning",
            "3D imaging capability",
            "Non-destructive testing"
        ],
        "manufacturer": "PVA TePla",
        "is_featured": True
    },
    {
        "name": "Bond Tester",
        "category": "Semiconductor",
        "description": "Precision wire bond testing equipment for pull and shear force measurement",
        "features": [
            "Pull test capability",
            "Shear test capability",
            "High accuracy force measurement",
            "Automated testing",
            "Statistical analysis",
            "Multiple bond type support"
        ],
        "manufacturer": "Nordson",
        "is_featured": False
    },
    {
        "name": "Optical Inspection Systems",
        "category": "Semiconductor",
        "description": "Advanced optical inspection systems for semiconductor device quality control",
        "features": [
            "High-resolution optical imaging",
            "Automated defect detection",
            "Pattern recognition",
            "Dimensional measurement",
            "Real-time inspection",
            "Data analysis software"
        ],
        "is_featured": False
    },
    {
        "name": "Warpage & Topography Measurement System",
        "category": "Semiconductor",
        "description": "Precision measurement system for wafer warpage and surface topography analysis",
        "features": [
            "3D warpage mapping",
            "Real-time measurement",
            "High accuracy topography",
            "Temperature profiling",
            "Stress analysis",
            "Comprehensive reporting"
        ],
        "manufacturer": "INSIDIX",
        "is_featured": True
    },
    
    # PROCESS EQUIPMENT
    {
        "name": "Plasma Treatment Systems",
        "category": "Semiconductor",
        "description": "Advanced plasma systems for surface preparation, cleaning, and etching in semiconductor manufacturing",
        "features": [
            "Atmospheric plasma technology",
            "Surface activation",
            "Precise process control",
            "Multiple gas support",
            "Clean process",
            "Automated operation"
        ],
        "manufacturer": "Nordson",
        "is_featured": True
    },
    {
        "name": "Die Bonder",
        "category": "Semiconductor",
        "description": "High-precision die bonding equipment for semiconductor packaging and assembly",
        "features": [
            "High placement accuracy",
            "Vision alignment system",
            "Multiple die size support",
            "Heated work holder",
            "Flexible operation",
            "Process monitoring"
        ],
        "manufacturer": "TRESKY",
        "is_featured": True
    },
    {
        "name": "BGA Ball Attach System",
        "category": "Semiconductor",
        "description": "Automated system for precise solder ball attachment to BGA and CSP packages",
        "features": [
            "High accuracy ball placement",
            "Vision alignment",
            "Flux application system",
            "Multiple ball sizes",
            "Automated process",
            "Quality verification"
        ],
        "manufacturer": "HAMAMATSU",
        "is_featured": False
    },
    {
        "name": "Camera Module Lens Assembly System",
        "category": "Semiconductor",
        "description": "Precision assembly equipment for camera module and lens manufacturing",
        "features": [
            "Multi-element lens assembly",
            "Active alignment capability",
            "High precision positioning",
            "Automated testing",
            "Quality inspection",
            "High throughput"
        ],
        "is_featured": False
    },
    
    # TEST EQUIPMENT
    {
        "name": "Test Handler",
        "category": "Semiconductor",
        "description": "Automated test handler for high-speed semiconductor device testing and handling",
        "features": [
            "High-speed device handling",
            "Precise temperature control",
            "Multiple socket support",
            "Automated sorting",
            "ATE integration",
            "High throughput"
        ],
        "manufacturer": "JHT",
        "is_featured": True
    },
    {
        "name": "Modular Test Platform",
        "category": "Semiconductor",
        "description": "Flexible modular test system for analog IC, PMIC, power discrete, and power module testing",
        "features": [
            "Modular configuration",
            "Analog IC testing",
            "PMIC test capability",
            "Power discrete testing",
            "Power module support",
            "Scalable architecture"
        ],
        "manufacturer": "ACCUTEST",
        "is_featured": True
    },
    
    # CONSUMABLES
    {
        "name": "Wafer Frames",
        "category": "Semiconductor",
        "description": "Precision wafer frames for secure wafer handling and processing",
        "features": [
            "Various size options",
            "High precision",
            "Durable construction",
            "Compatible with standard equipment",
            "Easy handling"
        ],
        "is_featured": False
    },
    {
        "name": "Frame Cassette",
        "category": "Semiconductor",
        "description": "Specialized cassettes for safe storage and transport of wafer frames",
        "features": [
            "Multiple frame capacity",
            "Secure frame holding",
            "Clean room compatible",
            "Stackable design",
            "ESD safe material"
        ],
        "is_featured": False
    },
    {
        "name": "Wafer Storage Box",
        "category": "Semiconductor",
        "description": "Protective storage boxes for wafer transport and storage",
        "features": [
            "Secure wafer protection",
            "Multiple wafer capacity",
            "Clean room certified",
            "Stackable design",
            "Impact resistant"
        ],
        "is_featured": False
    }
]

async def regenerate_semiconductor():
    """Replace all semiconductor products with brochure-based products"""
    try:
        print("Starting semiconductor product regeneration...")
        
        # Delete ALL existing semiconductor products
        result = await db.products.delete_many({"category": "Semiconductor"})
        print(f"✅ Deleted {result.deleted_count} existing semiconductor products")
        
        # Insert new semiconductor products
        inserted_count = 0
        for product_data in SEMICONDUCTOR_PRODUCTS:
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
        
        print(f"✅ Successfully inserted {inserted_count} semiconductor products")
        
        # Print summary by sub-category
        print("\n📊 New Semiconductor Products by Type:")
        print("  Wafer Handling Equipment:")
        wafer_handling = [p for p in SEMICONDUCTOR_PRODUCTS if "Wafer" in p["name"] or "Dicing" in p["name"] or "Plasma Dicing" in p["name"]]
        for p in wafer_handling:
            print(f"    - {p['name']}")
        
        print("\n  Inspection Equipment:")
        inspection = [p for p in SEMICONDUCTOR_PRODUCTS if "Inspection" in p["name"] or "Bond Tester" in p["name"] or "Warpage" in p["name"] or "Acoustic" in p["name"]]
        for p in inspection:
            print(f"    - {p['name']}")
        
        print("\n  Process Equipment:")
        process = [p for p in SEMICONDUCTOR_PRODUCTS if "Plasma Treatment" in p["name"] or "Die Bonder" in p["name"] or "BGA" in p["name"] or "Camera" in p["name"]]
        for p in process:
            print(f"    - {p['name']}")
        
        print("\n  Test Equipment:")
        test = [p for p in SEMICONDUCTOR_PRODUCTS if "Test Handler" in p["name"] or "Test Platform" in p["name"]]
        for p in test:
            print(f"    - {p['name']}")
        
        print("\n  Consumables:")
        consumables = [p for p in SEMICONDUCTOR_PRODUCTS if "Frame" in p["name"] or "Box" in p["name"] or "Surfactant" in p["name"] and "System" not in p["name"]]
        for p in consumables:
            print(f"    - {p['name']}")
        
        # Print total counts
        print("\n📊 Final Product Count:")
        total = await db.products.count_documents({})
        semiconductor_count = await db.products.count_documents({"category": "Semiconductor"})
        print(f"  - Semiconductor: {semiconductor_count} products")
        print(f"  - Total Products: {total}")
        
        return inserted_count
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(regenerate_semiconductor())
