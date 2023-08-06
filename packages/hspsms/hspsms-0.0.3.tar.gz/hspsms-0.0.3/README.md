# HSP SMS API

**API Integration of [HSPSMS](http://sms.hspsms.com)**<br>

Contributors: **WE'RE LOOKING FOR SOMEONE WHO CAN CONTRIBUTE IN DOCS**
- **[Civil Machines Technologies Private Limited](https://github.com/civilmahines)**: For providing me platform and
funds for research work. This project is hosted currently with `CMT` only. 
- **[Himanshu Shankar](https://github.com/iamhssingh)**: Himanshu Shankar has initiated this project and worked on this
project to collect useful functions and classes that are being used in various projects.

#### Installation

- Download and Install via `pip`
```
pip install hspsms
```
or<br>
Download and Install via `easy_install`
```
easy_install hspsms
```

#### Send SMS
Following is a simple example
```
from hspsms import HSPConnector

hspconn = HSPConnector(username="", apikey="", sender="", smstype="")
hspconn.send_sms(recipient=[], message="", sendername="", smstype="", scheduled="")
```

##### Using with Django
###### Using [`django-sendsms`](https://github.com/stefanfoulis/django-sendsms)
- Install `django-sendsms`: `pip install django-sendsms`

- Specify configuration for `HSP API` in `settings.py`
```
HSPSMS = {
    "USER": "",
    "APIKEY": "",
    "SENDER": "",
    "DEFAULT_SMSTYPE": ""
}
```

- Specify default `django-sendsms` backend in `settings.py`
```
SENDSMS_BACKEND = 'hspsms.backends.DjangoSendSMSBackend'
```

###### Using with [`DRF Addons`]((https://github.com/101loop/drf-addons))
- Install `drfaddons`: `pip install drfaddons`
- `DRF Addons` use `django-sendsms` to send sms. Follow steps for `django-sendsms`.
- Use `send_message` function of `drfaddons`
```
from drfaddons.utils import send_message

send_message(message="message", subject="Fallback Email Subject", "recip": [...mobile_numbers...],
             "recip_email": [...respective_fallback_email_addresses...],
             "html_message": "fallback_html_message")
```
