from dotenv import load_dotenv
from imagekitio import ImageKit
import os

import imagekitio
# print(imagekitio.__version__)
# print(imagekitio.ImageKit.__init__.__code__.co_varnames)

load_dotenv()  # Load environment variables from .env file

imagekit = ImageKit(
    private_key=os.getenv("IMAGEKIT_PRIVATE_KEY"),
    # public_key=os.getenv("IMAGEKIT_PUBLIC_KEY"),
    
)


# url_endpoint=os.getenv.get("IMAGEKIT_URL")