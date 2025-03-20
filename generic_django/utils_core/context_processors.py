from django.conf import settings

def global_context(request):
    """This function gathers all settings that start with the CONTEXT_ prefix"""

    return settings.GLOBAL_CONTEXT
