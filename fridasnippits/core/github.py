from django.core.cache import cache
import requests

def get_latest_frida_release():
    CACHE_KEY = 'frida-releases'
    results = cache.get(CACHE_KEY)
    if results:
        return results

    try:
        response = requests.get('https://api.github.com/repos/frida/frida/releases').json()
        cache.set(CACHE_KEY, [x['tag_name'] for x in response], 3600)
    except:
        return ""
