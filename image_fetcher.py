"""
Image fetching from various sources (Unsplash, Bing, etc.)
"""
import os
import requests
from pathlib import Path
from typing import Optional


class UnsplashFetcher:
    """Fetch random wallpapers from Unsplash API"""
    
    BASE_URL = "https://api.unsplash.com/photos/random"
    
    def __init__(self, api_key: str):
        """
        Initialize Unsplash fetcher
        
        Args:
            api_key: Unsplash API key
        """
        self.api_key = api_key
    
    def fetch_wallpaper(self, query: str = "nature", width: int = 1920, height: int = 1080) -> Optional[str]:
        """
        Fetch a random wallpaper from Unsplash
        
        Args:
            query: Search query (e.g., 'nature', 'space', 'city')
            width: Image width
            height: Image height
            
        Returns:
            Image URL or None if failed
        """
        try:
            params = {
                "client_id": self.api_key,
                "query": query,
                "orientation": "landscape",
                "w": width,
                "h": height
            }
            
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            image_url = data.get("urls", {}).get("raw")
            
            if image_url:
                print(f"✓ Fetched image from Unsplash: {data.get('alt_description', 'Unknown')}")
                return image_url
            else:
                print("✗ No image URL found in response")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Error fetching from Unsplash: {str(e)}")
            return None
    
    def download_image(self, url: str, save_path: str) -> bool:
        """
        Download image from URL
        
        Args:
            url: Image URL
            save_path: Where to save the image
            
        Returns:
            True if successful, False otherwise
        """
        try:
            response = requests.get(url, timeout=10, stream=True)
            response.raise_for_status()
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            print(f"✓ Image downloaded to {save_path}")
            return True
            
        except Exception as e:
            print(f"✗ Error downloading image: {str(e)}")
            return False


class BingFetcher:
    """Fetch wallpapers from Bing"""
    
    BASE_URL = "https://www.bing.com/HPImageArchive.aspx"
    
    def fetch_wallpaper(self) -> Optional[str]:
        """
        Fetch today's Bing wallpaper
        
        Returns:
            Image URL or None if failed
        """
        try:
            params = {
                "format": "js",
                "idx": "0",
                "n": "1"
            }
            
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get("images"):
                image_path = data["images"][0].get("url")
                image_url = f"https://www.bing.com{image_path}"
                print(f"✓ Fetched image from Bing")
                return image_url
            else:
                print("✗ No image found from Bing")
                return None
                
        except Exception as e:
            print(f"✗ Error fetching from Bing: {str(e)}")
            return None
    
    def download_image(self, url: str, save_path: str) -> bool:
        """
        Download image from URL
        
        Args:
            url: Image URL
            save_path: Where to save the image
            
        Returns:
            True if successful, False otherwise
        """
        try:
            response = requests.get(url, timeout=10, stream=True)
            response.raise_for_status()
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            print(f"✓ Image downloaded to {save_path}")
            return True
            
        except Exception as e:
            print(f"✗ Error downloading image: {str(e)}")
            return False
