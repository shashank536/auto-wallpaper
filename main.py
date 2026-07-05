"""
Automatic Wallpaper Changer for Windows
Changes desktop wallpaper every 5 minutes with images from Unsplash
"""
import os
import sys
import json
import time
import schedule
from datetime import datetime
from pathlib import Path

from wallpaper_manager import WallpaperManager
from image_fetcher import UnsplashFetcher, BingFetcher


class AutoWallpaperChanger:
    """Main application class for automatic wallpaper changes"""
    
    def __init__(self, config_file: str = "config.json"):
        """
        Initialize the wallpaper changer
        
        Args:
            config_file: Path to configuration JSON file
        """
        self.config = self.load_config(config_file)
        self.wallpaper_dir = self.config.get("wallpaper_directory", "./wallpapers")
        self.interval = self.config.get("interval_minutes", 5)
        self.image_source = self.config.get("image_source", "unsplash")
        
        # Create wallpaper directory if it doesn't exist
        os.makedirs(self.wallpaper_dir, exist_ok=True)
        
        # Initialize fetcher based on config
        if self.image_source == "unsplash":
            api_key = self.config.get("unsplash_api_key")
            if not api_key or api_key == "your_unsplash_api_key_here":
                print("✗ ERROR: Unsplash API key not configured!")
                print("  Please get your API key from https://unsplash.com/api/")
                print("  and update it in config.json")
                sys.exit(1)
            self.fetcher = UnsplashFetcher(api_key)
        elif self.image_source == "bing":
            self.fetcher = BingFetcher()
        else:
            print(f"✗ Unknown image source: {self.image_source}")
            sys.exit(1)
        
        self.wallpaper_manager = WallpaperManager()
    
    @staticmethod
    def load_config(config_file: str) -> dict:
        """
        Load configuration from JSON file
        
        Args:
            config_file: Path to config JSON file
            
        Returns:
            Configuration dictionary
        """
        try:
            if not os.path.exists(config_file):
                print(f"✗ Config file not found: {config_file}")
                sys.exit(1)
            
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            print(f"✓ Configuration loaded from {config_file}")
            return config
            
        except json.JSONDecodeError as e:
            print(f"✗ Error parsing config JSON: {str(e)}")
            sys.exit(1)
    
    def change_wallpaper_task(self):
        """
        Task to change wallpaper - called by scheduler
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = os.path.join(self.wallpaper_dir, f"wallpaper_{timestamp}.jpg")
            
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Changing wallpaper...")
            
            # Fetch image
            if self.image_source == "unsplash":
                query = self.config.get("image_query", "nature")
                image_url = self.fetcher.fetch_wallpaper(query=query)
            else:
                image_url = self.fetcher.fetch_wallpaper()
            
            if not image_url:
                print("✗ Failed to fetch image")
                return
            
            # Download image
            if not self.fetcher.download_image(image_url, image_path):
                print("✗ Failed to download image")
                return
            
            # Change wallpaper
            if self.wallpaper_manager.change_wallpaper(image_path):
                self.cleanup_old_wallpapers()
                print("✓ Wallpaper changed successfully!")
            else:
                print("✗ Failed to change wallpaper")
        
        except Exception as e:
            print(f"✗ Error in wallpaper change task: {str(e)}")
    
    def cleanup_old_wallpapers(self):
        """
        Remove old wallpapers to save disk space
        """
        try:
            keep_wallpapers = self.config.get("keep_wallpapers", True)
            max_wallpapers = self.config.get("max_wallpapers_to_keep", 50)
            
            if not keep_wallpapers:
                return
            
            # Get all wallpaper files
            wallpaper_files = sorted(
                Path(self.wallpaper_dir).glob("wallpaper_*.jpg"),
                key=lambda x: x.stat().st_mtime
            )
            
            # Remove old files if exceeds max
            if len(wallpaper_files) > max_wallpapers:
                files_to_remove = len(wallpaper_files) - max_wallpapers
                for file in wallpaper_files[:files_to_remove]:
                    try:
                        file.unlink()
                        print(f"  Removed old wallpaper: {file.name}")
                    except Exception as e:
                        print(f"  Failed to remove {file.name}: {str(e)}")
        
        except Exception as e:
            print(f"Warning: Error cleaning up wallpapers: {str(e)}")
    
    def start(self):
        """
        Start the automatic wallpaper changer service
        """
        print("=" * 60)
        print("🖼️  AUTO-WALLPAPER CHANGER FOR WINDOWS")
        print("=" * 60)
        print(f"✓ Image Source: {self.image_source.upper()}")
        print(f"✓ Change Interval: {self.interval} minutes")
        print(f"✓ Wallpaper Directory: {os.path.abspath(self.wallpaper_dir)}")
        print("=" * 60)
        print("Press Ctrl+C to stop\n")
        
        # Schedule the task
        schedule.every(self.interval).minutes.do(self.change_wallpaper_task)
        
        # Run initial wallpaper change
        print("Running initial wallpaper change...")
        self.change_wallpaper_task()
        
        # Keep the scheduler running
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("\n\n✓ Wallpaper changer stopped. Goodbye!")
            sys.exit(0)


def main():
    """Main entry point"""
    changer = AutoWallpaperChanger("config.json")
    changer.start()


if __name__ == "__main__":
    main()
