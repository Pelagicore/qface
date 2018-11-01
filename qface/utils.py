from .generator import FileSystem
from .helper import doc


def module_info(text):
    system = FileSystem.parse_text(text)
    module = list(system.modules)[0]
    return {
        'title': module.name,
        'brief': " ".join(doc.parse_doc(module.comment).brief)
    }
