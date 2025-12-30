from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone
from enum import Enum


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Enums
class ProductCategory(str, Enum):
    ELECTRONIC_ASSEMBLY = "Electronic Assembly Products"
    ASSEMBLY_TOOLS = "Assembly Tools"
    INSPECTION_TESTING = "Inspection and Testing"
    SEMICONDUCTOR = "Semiconductor"
    NON_DESTRUCTIVE_TESTING = "Non Destructive Testing"
    MECHANICAL = "Mechanical"


# Models
class Partnership(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    company_name: str
    website_url: str
    description: str
    partnership_date: str
    logo_url: Optional<str> = None
    products_offered: Optional[str] = None
    is_featured: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PartnershipCreate(BaseModel):
    company_name: str
    website_url: str
    description: str
    partnership_date: str
    logo_url: Optional[str] = None
    products_offered: Optional[str] = None
    is_featured: bool = False


class Product(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    category: ProductCategory
    description: str
    features: Optional[List[str]] = []
    image_url: Optional[str] = None
    brochure_url: Optional[str] = None
    manufacturer: Optional[str] = None
    is_featured: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ProductCreate(BaseModel):
    name: str
    category: ProductCategory
    description: str
    features: Optional[List[str]] = []
    image_url: Optional[str] = None
    brochure_url: Optional[str] = None
    manufacturer: Optional[str] = None
    is_featured: bool = False


class Testimonial(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    company_name: Optional[str] = None
    designation: Optional[str] = None
    testimonial_text: Optional[str] = None
    video_url: Optional[str] = None
    image_url: Optional[str] = None
    is_featured: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TestimonialCreate(BaseModel):
    client_name: str
    company_name: Optional[str] = None
    designation: Optional[str] = None
    testimonial_text: Optional[str] = None
    video_url: Optional[str] = None
    image_url: Optional[str] = None
    is_featured: bool = True


class NewsEvent(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    content: str
    event_type: str  # "PARTNERSHIP", "EVENT", "NEWS", "INDUSTRY"
    image_url: Optional[str] = None
    link_url: Optional[str] = None
    published_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_featured: bool = True


class NewsEventCreate(BaseModel):
    title: str
    content: str
    event_type: str
    image_url: Optional[str] = None
    link_url: Optional[str] = None
    is_featured: bool = True


class ContactInquiry(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    phone: Optional[str] = None
    company: Optional[str] = None
    message: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ContactInquiryCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    company: Optional[str] = None
    message: str


# API Routes

@api_router.get("/")
async def root():
    return {"message": "Accurex Solutions API", "version": "2.0", "years_of_excellence": 39}


# Partnership Routes
@api_router.post("/partnerships", response_model=Partnership)
async def create_partnership(input: PartnershipCreate):
    partnership_dict = input.model_dump()
    partnership_obj = Partnership(**partnership_dict)
    
    doc = partnership_obj.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.partnerships.insert_one(doc)
    return partnership_obj


@api_router.get("/partnerships", response_model=List[Partnership])
async def get_partnerships():
    partnerships = await db.partnerships.find({}, {"_id": 0}).sort("created_at", -1).to_list(1000)
    
    for partnership in partnerships:
        if isinstance(partnership['created_at'], str):
            partnership['created_at'] = datetime.fromisoformat(partnership['created_at'])
    
    return partnerships


@api_router.get("/partnerships/{partnership_id}", response_model=Partnership)
async def get_partnership(partnership_id: str):
    partnership = await db.partnerships.find_one({"id": partnership_id}, {"_id": 0})
    if not partnership:
        raise HTTPException(status_code=404, detail="Partnership not found")
    
    if isinstance(partnership['created_at'], str):
        partnership['created_at'] = datetime.fromisoformat(partnership['created_at'])
    
    return partnership


# Product Routes
@api_router.post("/products", response_model=Product)
async def create_product(input: ProductCreate):
    product_dict = input.model_dump()
    product_obj = Product(**product_dict)
    
    doc = product_obj.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.products.insert_one(doc)
    return product_obj


@api_router.get("/products", response_model=List[Product])
async def get_products(category: Optional[str] = None):
    query = {}
    if category:
        query['category'] = category
    
    products = await db.products.find(query, {"_id": 0}).sort("created_at", -1).to_list(1000)
    
    for product in products:
        if isinstance(product['created_at'], str):
            product['created_at'] = datetime.fromisoformat(product['created_at'])
    
    return products


@api_router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    product = await db.products.find_one({"id": product_id}, {"_id": 0})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if isinstance(product['created_at'], str):
        product['created_at'] = datetime.fromisoformat(product['created_at'])
    
    return product


# Testimonial Routes
@api_router.post("/testimonials", response_model=Testimonial)
async def create_testimonial(input: TestimonialCreate):
    testimonial_dict = input.model_dump()
    testimonial_obj = Testimonial(**testimonial_dict)
    
    doc = testimonial_obj.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.testimonials.insert_one(doc)
    return testimonial_obj


@api_router.get("/testimonials", response_model=List[Testimonial])
async def get_testimonials():
    testimonials = await db.testimonials.find({}, {"_id": 0}).sort("created_at", -1).to_list(1000)
    
    for testimonial in testimonials:
        if isinstance(testimonial['created_at'], str):
            testimonial['created_at'] = datetime.fromisoformat(testimonial['created_at'])
    
    return testimonials


# News & Events Routes
@api_router.post("/news", response_model=NewsEvent)
async def create_news(input: NewsEventCreate):
    news_dict = input.model_dump()
    news_obj = NewsEvent(**news_dict)
    
    doc = news_obj.model_dump()
    doc['published_date'] = doc['published_date'].isoformat()
    
    await db.news_events.insert_one(doc)
    return news_obj


@api_router.get("/news", response_model=List[NewsEvent])
async def get_news():
    news = await db.news_events.find({}, {"_id": 0}).sort("published_date", -1).to_list(1000)
    
    for item in news:
        if isinstance(item['published_date'], str):
            item['published_date'] = datetime.fromisoformat(item['published_date'])
    
    return news


# Contact Routes
@api_router.post("/contact", response_model=ContactInquiry)
async def create_contact_inquiry(input: ContactInquiryCreate):
    contact_dict = input.model_dump()
    contact_obj = ContactInquiry(**contact_dict)
    
    doc = contact_obj.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.contact_inquiries.insert_one(doc)
    return contact_obj


@api_router.get("/contact", response_model=List[ContactInquiry])
async def get_contact_inquiries():
    contacts = await db.contact_inquiries.find({}, {"_id": 0}).sort("created_at", -1).to_list(1000)
    
    for contact in contacts:
        if isinstance(contact['created_at'], str):
            contact['created_at'] = datetime.fromisoformat(contact['created_at'])
    
    return contacts


# Seed Data Route (for initial setup)
@api_router.post("/seed-data")
async def seed_database():
    """Seed the database with initial Accurex data"""
    
    # Clear existing data
    await db.partnerships.delete_many({})
    await db.products.delete_many({})
    await db.testimonials.delete_many({})
    await db.news_events.delete_many({})
    
    # Seed Partnerships (Existing + New 3)
    partnerships_data = [
        {
            "company_name": "Mycronic",
            "website_url": "https://www.mycronic.com",
            "description": "Complete, agile manufacturing solution for Industry 4.0. Mycronic offers innovative feeder technology, automated traceability systems, and comprehensive software solutions covering the entire chain of electronics assembly.",
            "partnership_date": "2020",
            "products_offered": "Pick and Place Machines, SMT Solutions, Industry 4.0 Solutions",
            "is_featured": True
        },
        {
            "company_name": "Tongtai",
            "website_url": "https://www.tongtai.com.tw/en/",
            "description": "Taiwan Based Tongtai is part of TT group that includes six international machinery brands. Products include vertical/horizontal machining centres, 5-axis machining centres, CNC lathes, multi-tasking machining centres, PCB processing machines.",
            "partnership_date": "2022",
            "products_offered": "CNC Machines, Machining Centers, PCB Processing Machines",
            "is_featured": True
        },
        {
            "company_name": "Insidix",
            "website_url": "http://www.insidix.com/",
            "description": "Accurex expands NDT offerings with TDM by Insidix from Grenoble. TDM equipment uses Projection Moiré for temperature-dependent warpage measurement, making it a unique solution for thermo-mechanical stress-induced warpage under realistic reflow conditions.",
            "partnership_date": "2021",
            "products_offered": "TDM Equipment, NDT Solutions, Warpage Measurement",
            "is_featured": True
        },
        {
            "company_name": "Graco",
            "website_url": "http://www.graco.com/",
            "description": "US Based Graco, founded in 1926, is a global leader in fluid handling technology. Partnership for Potting Applications needs in Indian Market. Focus on innovation with advanced features, pioneering design and high performance.",
            "partnership_date": "2022",
            "products_offered": "Potting Applications, Fluid Handling Equipment",
            "is_featured": True
        },
        # NEW PARTNERSHIPS 2025
        {
            "company_name": "AccoTEST Global",
            "website_url": "https://accotest.com/",
            "description": "Accurex Solutions partners with AccoTEST Global to provide local service support and sales in the Indian Market for functional testers manufactured by AccoTEST.",
            "partnership_date": "2025",
            "products_offered": "Functional Testers, Automatic Test Equipment",
            "is_featured": True
        },
        {
            "company_name": "JHT Semiconductors",
            "website_url": "https://jhtsemiconductor.com/",
            "description": "Accurex Solutions partners with JHT Semiconductors to provide local service support and sales in the Indian Market for Pick and Place test handlers manufactured by JHT.",
            "partnership_date": "2025",
            "products_offered": "Pick and Place Test Handlers, Semiconductor Test Equipment",
            "is_featured": True
        },
        {
            "company_name": "PVA TePla AS",
            "website_url": "https://www.pvatepla-sam.com/en/",
            "description": "Accurex Solutions partners with PVA TePla AS to provide local service support and sales in the Indian Market for the SAM (Scanning Acoustic Microscope) product line.",
            "partnership_date": "2025",
            "products_offered": "SAM Product Line, Scanning Acoustic Microscopy, NDT Equipment",
            "is_featured": True
        }
    ]
    
    for partnership_data in partnerships_data:
        partnership = Partnership(**partnership_data)
        doc = partnership.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        await db.partnerships.insert_one(doc)
    
    # Seed Sample Products
    products_data = [
        {
            "name": "Screen Printer",
            "category": "Electronic Assembly Products",
            "description": "High-precision screen printing for solder paste application",
            "features": ["Automatic alignment", "Vision system", "High accuracy placement"]
        },
        {
            "name": "Pick and Place Machine",
            "category": "Electronic Assembly Products",
            "description": "Advanced component placement system for PCB assembly",
            "features": ["High-speed placement", "Multi-head configuration", "Vision inspection"]
        },
        {
            "name": "Reflow Oven",
            "category": "Electronic Assembly Products",
            "description": "Precision temperature control for PCB soldering",
            "features": ["Multiple heating zones", "Nitrogen atmosphere", "Temperature profiling"]
        },
        {
            "name": "AOI System",
            "category": "Inspection and Testing",
            "description": "Automatic Optical Inspection for quality control",
            "features": ["3D inspection", "High-resolution imaging", "Defect classification"]
        },
        {
            "name": "X-Ray Inspection",
            "category": "Inspection and Testing",
            "description": "Non-destructive X-Ray inspection for hidden defects",
            "features": ["2D & 3D imaging", "BGA inspection", "Void analysis"]
        },
        {
            "name": "Functional Tester (AccoTEST)",
            "category": "Semiconductor",
            "description": "Advanced functional testing equipment from AccoTEST Global",
            "features": ["Comprehensive test coverage", "High throughput", "Flexible configuration"],
            "manufacturer": "AccoTEST Global"
        },
        {
            "name": "Pick and Place Test Handler (JHT)",
            "category": "Semiconductor",
            "description": "High-performance test handlers from JHT Semiconductors",
            "features": ["Automated handling", "High accuracy", "Quick changeover"],
            "manufacturer": "JHT Semiconductors"
        },
        {
            "name": "Scanning Acoustic Microscope (SAM)",
            "category": "Non Destructive Testing",
            "description": "Advanced SAM equipment from PVA TePla AS for defect detection",
            "features": ["High-resolution imaging", "Subsurface defect detection", "Material characterization"],
            "manufacturer": "PVA TePla AS"
        }
    ]
    
    for product_data in products_data:
        product = Product(**product_data)
        doc = product.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        await db.products.insert_one(doc)
    
    # Seed Testimonials
    testimonials_data = [
        {
            "client_name": "Manufacturing Director",
            "company_name": "Leading EMS Company",
            "testimonial_text": "Accurex has been our reliable and honest partner for over a decade now and they have stood by us every time.",
            "is_featured": True
        },
        {
            "client_name": "Operations Manager",
            "company_name": "Electronics Manufacturer",
            "testimonial_text": "Accurex is synonymous with service. Team work is their hallmark of relationship building.",
            "is_featured": True
        },
        {
            "client_name": "Production Head",
            "company_name": "R&D Manufacturing Facility",
            "testimonial_text": "As we do many R&D and Low/Medium Production Manufacturing, we should never have Down Time on Pick and Place Machines. The Service and Expertise M/s. Accurex extends are Excellent.",
            "is_featured": True
        },
        {
            "client_name": "Mr. Chan Wha Pak",
            "designation": "Distinguished Guest",
            "testimonial_text": "Video testimonial from demo center inauguration",
            "video_url": "PLACEHOLDER_FOR_VIDEO_URL",
            "is_featured": True
        }
    ]
    
    for testimonial_data in testimonials_data:
        testimonial = Testimonial(**testimonial_data)
        doc = testimonial.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        await db.testimonials.insert_one(doc)
    
    return {
        "message": "Database seeded successfully",
        "partnerships": len(partnerships_data),
        "products": len(products_data),
        "testimonials": len(testimonials_data)
    }


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
