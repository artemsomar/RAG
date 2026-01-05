class DocumentNotFound(Exception):
    """Called when a document is not found in the database."""

    pass


class DocumentUploadError(Exception):
    """Called when an error occurred while creating a document (DB or S3)."""

    pass


class UserNotFound(Exception):
    """Called when a User not found in the database."""

    pass
