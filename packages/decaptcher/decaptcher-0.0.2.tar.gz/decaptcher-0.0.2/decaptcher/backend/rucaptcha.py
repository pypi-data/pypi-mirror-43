from .common import CommonBackend


class RucaptchaBackend(CommonBackend):
    software_id = 2373
    base_url = 'http://rucaptcha.com'
