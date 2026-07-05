"""
Windows wallpaper manager using ctypes
"""
import ctypes
import os
from pathlib import Path


class WallpaperManager:
    """Manages wallpaper changes on Windows"""
    
    SPI_SETDESKWALLPAPER = 20
    SPIF_UPDATEINIFILE = 0x01
    SPIF_SENDCHANGE = 0x02
    
    @staticmethod
    def change_wallpaper(image_path: str) -> bool:
        """
        Change the Windows desktop wallpaper
        
        Args:
            image_path: Full path to the image file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert to absolute path
            image_path = os.path.abspath(image_path)
            
            # Check if file exists
            if not os.path.exists(image_path):
                print(f"Error: Image file not found at {image_path}")
                return False
            
            # Call Windows API to set wallpaper
            result = ctypes.windll.user32.SystemParametersInfoW(
                WallpaperManager.SPI_SETDESKWALLPAPER,
                0,
                image_path,
                WallpaperManager.SPIF_UPDATEINIFILE | WallpaperManager.SPIF_SENDCHANGE
            )
            
            if result:
                print(f"✓ Wallpaper changed successfully: {os.path.basename(image_path)}")
                return True
            else:
                print(f"✗ Failed to change wallpaper")
                return False
                
        except Exception as e:
            print(f"✗ Error changing wallpaper: {str(e)}")
            return False
    
    @staticmethod
    def get_current_wallpaper() -> str:
        """
        Get the path of the current wallpaper
        
        Returns:
            Path to the current wallpaper
        """
        try:
            import winreg
            registry_path = r"Control Panel\Desktop"
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path)
            value, _ = winreg.QueryValueEx(registry_key, "Wallpaper")
            winreg.CloseKey(registry_key)
            return value
        except Exception as e:
            print(f"Error getting current wallpaper: {str(e)}")
            return ""
