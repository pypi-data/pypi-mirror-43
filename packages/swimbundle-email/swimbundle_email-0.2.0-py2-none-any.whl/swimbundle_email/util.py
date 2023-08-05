import magic
import base64


# Check if the email base64 object conforms to rfc822
def check_if_rfc_822(b64):
    file_decoded = base64.b64decode(b64)
    mime_type = magic.from_buffer(file_decoded, mime=True)
    if mime_type == "message/rfc822":
        return True
    else:
        return False
