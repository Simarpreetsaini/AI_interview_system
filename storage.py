import os
import cloudinary
import cloudinary.uploader

# Cloudinary Configuration
cloudinary.config(
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key = os.getenv("CLOUDINARY_API_KEY"),
    api_secret = os.getenv("CLOUDINARY_API_SECRET"),
    secure = True
)

def upload_file_to_storage(file_path: str, object_name: str) -> str:
    """
    Uploads a file to Cloudinary. 
    If not configured, it returns a local path.
    """
    if os.getenv("CLOUDINARY_CLOUD_NAME"):
        try:
            # We use upload_large for videos
            response = cloudinary.uploader.upload_large(
                file_path,
                resource_type="video",
                public_id=object_name.split('.')[0]
            )
            return response.get('secure_url')
        except Exception as e:
            print(f"Failed to upload to Cloudinary: {e}")
            return f"/static/videos/{object_name}"
            
    # Fallback to local storage if Cloudinary is not configured
    return f"/static/videos/{object_name}"
