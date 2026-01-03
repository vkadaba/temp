"""
Update products database with new requirements
- Semiconductor: Remove/add products
- Non Destructive Testing: Updates
- Mechanical: Updates
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

async def update_products():
    """Update products based on new requirements"""
    try:
        print("Starting product updates...")
        
        # SEMICONDUCTOR - REMOVALS
        semiconductor_removals = [
            "2-Sided Flux Application System",
            "Lens Cell Assembly System",
            "Lens Module Assembly System",
            "Camera Module Tester",
            "Plasma Dicing System",
            "FlexTrack Plasma System"
        ]
        
        for product_name in semiconductor_removals:
            result = await db.products.delete_one({"name": product_name, "category": "Semiconductor"})
            if result.deleted_count > 0:
                print(f"✅ Removed: {product_name}")
        
        # SEMICONDUCTOR - ADD SIP AOI Test System
        sip_aoi = {
            "id": str(uuid.uuid4()),
            "name": "SIP AOI Test System",
            "category": "Semiconductor",
            "description": "Advanced Automated Optical Inspection system for System-in-Package testing",
            "features": [
                "High-resolution 3D inspection",
                "Multi-chip package support",
                "Automated defect detection",
                "SIP-specific algorithms",
                "High throughput capability",
                "Comprehensive reporting"
            ],
            "manufacturer": "Mirtec",
            "is_featured": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.products.insert_one(sip_aoi)
        print("✅ Added: SIP AOI Test System (Mirtec)")
        
        # NON DESTRUCTIVE TESTING - REMOVALS
        ndt_removals = [
            "INSIDIX TDM Compact 3",
            "Acoustic Microscopy Services"
        ]
        
        for product_name in ndt_removals:
            result = await db.products.delete_one({"name": product_name, "category": "Non Destructive Testing"})
            if result.deleted_count > 0:
                print(f"✅ Removed: {product_name}")
        
        # NON DESTRUCTIVE TESTING - Update SAM
        # Remove existing SAM
        await db.products.delete_one({"name": {"$regex": "Scanning Acoustic Microscope"}, "category": "Non Destructive Testing"})
        
        # Add SAM from PVA TePla AS
        sam_as = {
            "id": str(uuid.uuid4()),
            "name": "Scanning Acoustic Microscope (SAM)",
            "category": "Non Destructive Testing",
            "description": "Advanced SAM system for subsurface defect detection and material characterization",
            "features": [
                "High-resolution acoustic imaging",
                "Subsurface defect detection",
                "Delamination analysis",
                "Void detection",
                "Non-destructive testing",
                "Material characterization"
            ],
            "manufacturer": "PVA TePla AS",
            "is_featured": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.products.insert_one(sam_as)
        print("✅ Added: SAM (PVA TePla AS)")
        
        # Add SAM from PVA TePla OKOS
        sam_okos = {
            "id": str(uuid.uuid4()),
            "name": "Scanning Acoustic Microscope (SAM)",
            "category": "Non Destructive Testing",
            "description": "High-performance scanning acoustic microscope for advanced failure analysis",
            "features": [
                "Ultra-high resolution imaging",
                "Advanced defect analysis",
                "Real-time scanning",
                "Multiple frequency options",
                "Automated inspection",
                "Data analysis software"
            ],
            "manufacturer": "PVA TePla OKOS",
            "is_featured": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.products.insert_one(sam_okos)
        print("✅ Added: SAM (PVA TePla OKOS)")
        
        # MECHANICAL - REMOVALS
        mechanical_removals = [
            "PCB Drilling Machine",
            "CNC Machining Center"  # Tongtai was already removed, this is the generic one
        ]
        
        for product_name in mechanical_removals:
            result = await db.products.delete_one({"name": product_name, "category": "Mechanical"})
            if result.deleted_count > 0:
                print(f"✅ Removed: {product_name}")
        
        # MECHANICAL - Update PCB Routing Machine
        await db.products.update_one(
            {"name": "PCB Routing Machine", "category": "Mechanical"},
            {"$set": {"manufacturer": "Genetic"}}
        )
        print("✅ Updated: PCB Routing Machine (Genetic)")
        
        # MECHANICAL - ADD new products
        pcb_depanelling = {
            "id": str(uuid.uuid4()),
            "name": "PCB Depanelling Machine",
            "category": "Mechanical",
            "description": "Precision PCB depanelling and separation system for clean board separation",
            "features": [
                "Clean board separation",
                "Multiple separation methods",
                "Dust collection system",
                "Programmable cutting paths",
                "Minimal stress on boards",
                "High precision"
            ],
            "manufacturer": "Genetic",
            "is_featured": False,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.products.insert_one(pcb_depanelling)
        print("✅ Added: PCB Depanelling Machine (Genetic)")
        
        solder_paste_mixer = {
            "id": str(uuid.uuid4()),
            "name": "Solder Paste Mixer",
            "category": "Mechanical",
            "description": "Automated solder paste mixing system for consistent paste quality",
            "features": [
                "Automated mixing cycle",
                "Consistent paste quality",
                "Temperature control",
                "Programmable settings",
                "Easy jar loading",
                "Reduced air entrapment"
            ],
            "manufacturer": "Genetic",
            "is_featured": False,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.products.insert_one(solder_paste_mixer)
        print("✅ Added: Solder Paste Mixer (Genetic)")
        
        # Print final summary
        print("\n📊 Final Product Count by Category:")
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
        
        total = await db.products.count_documents({})
        print(f"\n✅ Total Products: {total}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(update_products())
