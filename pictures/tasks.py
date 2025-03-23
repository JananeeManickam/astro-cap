from celery import shared_task
from django.utils import timezone
import requests
from .models import TelescopeObservation, TelescopeStatus
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@shared_task
def fetch_hubble_telescope_data():
    """
    Celery task to periodically fetch and update Hubble telescope data.
    """
    BASE_URL = "https://spacetelescopelive.org/hubble"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://spacetelescopelive.org/hubble/",
    }
    
    try:
        # Fetch current observation
        current_obs_response = requests.get(
            f"{BASE_URL}/api/current_observation",
            headers=HEADERS
        )
        current_obs_response.raise_for_status()
        current_obs_data = current_obs_response.json()
        
        # Fetch instrument status
        instrument_status_response = requests.get(
            f"{BASE_URL}/api/instrument_status",
            headers=HEADERS
        )
        instrument_status_response.raise_for_status()
        instrument_status_data = instrument_status_response.json()
        
        # Update database with current observation
        if current_obs_data:
            observation_date = datetime.fromisoformat(current_obs_data.get("observation_date", datetime.now().isoformat()))
            
            # Update or create the current observation
            observation, created = TelescopeObservation.objects.update_or_create(
                telescope="Hubble",
                title=current_obs_data.get("title", "Current Hubble Observation"),
                is_current=True,
                defaults={
                    "description": current_obs_data.get("description", ""),
                    "image_url": current_obs_data.get("image_url", ""),
                    "observation_date": observation_date,
                    "target_name": current_obs_data.get("target_name", ""),
                    "observation_type": current_obs_data.get("type", ""),
                    "metadata": current_obs_data
                }
            )
            
            # Set all other observations for this telescope to not current
            TelescopeObservation.objects.filter(
                telescope="Hubble", 
                is_current=True
            ).exclude(id=observation.id).update(is_current=False)
        
        # Update telescope status
        if instrument_status_data:
            last_update = datetime.fromisoformat(instrument_status_data.get("updated_at", datetime.now().isoformat()))
            
            TelescopeStatus.objects.update_or_create(
                telescope="Hubble",
                defaults={
                    "status": instrument_status_data.get("status", "Unknown"),
                    "current_instrument": instrument_status_data.get("current_instrument", "Unknown"),
                    "last_update": last_update,
                    "additional_info": instrument_status_data
                }
            )
        
        # Additionally, fetch recent observations
        recent_obs_response = requests.get(
            f"{BASE_URL}/api/recent_observations",
            headers=HEADERS
        )
        recent_obs_response.raise_for_status()
        recent_obs_data = recent_obs_response.json()
        
        # Process recent observations
        for obs in recent_obs_data:
            observation_date = datetime.fromisoformat(obs.get("observation_date", datetime.now().isoformat()))
            
            TelescopeObservation.objects.update_or_create(
                telescope="Hubble",
                title=obs.get("title", "Hubble Observation"),
                observation_date=observation_date,
                defaults={
                    "description": obs.get("description", ""),
                    "image_url": obs.get("image_url", ""),
                    "target_name": obs.get("target_name", ""),
                    "observation_type": obs.get("type", ""),
                    "is_current": False,
                    "metadata": obs
                }
            )
        
        logger.info("Successfully fetched and updated Hubble telescope data")
        return {"status": "success"}
        
    except Exception as e:
        logger.error(f"Error in fetch_hubble_telescope_data task: {e}")
        return {"status": "error", "error": str(e)}