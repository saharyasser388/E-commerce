import strawberry
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile

@strawberry.scalar(
    name="Upload",
    description="Represents an uploaded file"
)
def Upload(value) -> InMemoryUploadedFile:
    if isinstance(value, (InMemoryUploadedFile, TemporaryUploadedFile)):
        return value
    raise ValueError("Invalid file upload")
