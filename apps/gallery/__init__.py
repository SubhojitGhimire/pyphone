from .gallery import GalleryApp

def get_app_info():
    return {
        "name": "Gallery",
        "icon": "apps/gallery/icon.png",
        "widget": GalleryApp
    }