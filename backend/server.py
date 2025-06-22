from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime
import os
import uuid
from typing import List, Optional

# Environment variables
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017/')

# MongoDB connection
client = MongoClient(MONGO_URL)
db = client.rbc_community
giveaways_collection = db.giveaways

# FastAPI app
app = FastAPI(title="RBC Community API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class Giveaway(BaseModel):
    title: str
    description: str
    prize: str
    endDate: str
    entryRequirement: str

class GiveawayResponse(BaseModel):
    id: str
    title: str
    description: str
    prize: str
    endDate: str
    entryRequirement: str
    createdAt: str

class AdminLogin(BaseModel):
    password: str

# Admin password (in production, this should be properly secured)
ADMIN_PASSWORD = "Rbcadminpass2025"

# Helper functions
def giveaway_to_dict(giveaway_doc):
    """Convert MongoDB document to dictionary for API response"""
    return {
        "id": giveaway_doc["id"],
        "title": giveaway_doc["title"],
        "description": giveaway_doc["description"],
        "prize": giveaway_doc["prize"],
        "endDate": giveaway_doc["endDate"],
        "entryRequirement": giveaway_doc["entryRequirement"],
        "createdAt": giveaway_doc["createdAt"]
    }

# API Routes

@app.get("/")
async def root():
    return {"message": "RBC Community API is running! 🐅"}

@app.get("/api/health")
async def health_check():
    try:
        # Test database connection
        db.command('ping')
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "database": "disconnected",
            "error": str(e)
        }

@app.get("/api/giveaways", response_model=List[GiveawayResponse])
async def get_giveaways():
    """Get all giveaways"""
    try:
        giveaways = list(giveaways_collection.find().sort("createdAt", -1))
        return [giveaway_to_dict(giveaway) for giveaway in giveaways]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch giveaways: {str(e)}"
        )

@app.get("/api/giveaways/active", response_model=List[GiveawayResponse])
async def get_active_giveaways():
    """Get only active giveaways (not ended)"""
    try:
        current_time = datetime.now().isoformat()
        giveaways = list(giveaways_collection.find({
            "endDate": {"$gt": current_time}
        }).sort("endDate", 1))
        return [giveaway_to_dict(giveaway) for giveaway in giveaways]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch active giveaways: {str(e)}"
        )

@app.post("/api/admin/login")
async def admin_login(credentials: AdminLogin):
    """Admin authentication"""
    if credentials.password != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin password"
        )
    return {"message": "Admin authenticated successfully", "status": "success"}

@app.post("/api/admin/giveaways", response_model=GiveawayResponse)
async def create_giveaway(giveaway: Giveaway):
    """Create a new giveaway (admin only)"""
    try:
        # Validate end date
        try:
            end_date = datetime.fromisoformat(giveaway.endDate.replace('Z', '+00:00'))
            if end_date <= datetime.now():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="End date must be in the future"
                )
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format"
            )

        # Create giveaway document
        giveaway_doc = {
            "id": str(uuid.uuid4()),
            "title": giveaway.title,
            "description": giveaway.description,
            "prize": giveaway.prize,
            "endDate": giveaway.endDate,
            "entryRequirement": giveaway.entryRequirement,
            "createdAt": datetime.now().isoformat()
        }

        # Insert into database
        result = giveaways_collection.insert_one(giveaway_doc)
        
        if result.inserted_id:
            return giveaway_to_dict(giveaway_doc)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create giveaway"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create giveaway: {str(e)}"
        )

@app.delete("/api/admin/giveaways/{giveaway_id}")
async def delete_giveaway(giveaway_id: str):
    """Delete a giveaway (admin only)"""
    try:
        result = giveaways_collection.delete_one({"id": giveaway_id})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Giveaway not found"
            )
        
        return {"message": "Giveaway deleted successfully", "status": "success"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete giveaway: {str(e)}"
        )

@app.put("/api/admin/giveaways/{giveaway_id}", response_model=GiveawayResponse)
async def update_giveaway(giveaway_id: str, giveaway: Giveaway):
    """Update a giveaway (admin only)"""
    try:
        # Validate end date
        try:
            end_date = datetime.fromisoformat(giveaway.endDate.replace('Z', '+00:00'))
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format"
            )

        # Update document
        update_data = {
            "title": giveaway.title,
            "description": giveaway.description,
            "prize": giveaway.prize,
            "endDate": giveaway.endDate,
            "entryRequirement": giveaway.entryRequirement,
            "updatedAt": datetime.now().isoformat()
        }

        result = giveaways_collection.update_one(
            {"id": giveaway_id},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Giveaway not found"
            )

        # Fetch and return updated giveaway
        updated_giveaway = giveaways_collection.find_one({"id": giveaway_id})
        return giveaway_to_dict(updated_giveaway)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update giveaway: {str(e)}"
        )

@app.get("/api/stats")
async def get_community_stats():
    """Get community statistics"""
    try:
        total_giveaways = giveaways_collection.count_documents({})
        active_giveaways = giveaways_collection.count_documents({
            "endDate": {"$gt": datetime.now().isoformat()}
        })
        
        return {
            "totalGiveaways": total_giveaways,
            "activeGiveaways": active_giveaways,
            "memberCount": 500,  # Static for now
            "communityStatus": "active"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch stats: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)