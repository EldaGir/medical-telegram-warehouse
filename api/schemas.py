from pydantic import BaseModel


class Product(BaseModel):
    product: str
    mentions: int


class ChannelActivity(BaseModel):
    channel_name: str
    total_posts: int
    average_views: float


class Message(BaseModel):
    message_id: int
    channel_name: str
    message_text: str


class VisualContent(BaseModel):
    channel_name: str
    image_category: str
    total_images: int