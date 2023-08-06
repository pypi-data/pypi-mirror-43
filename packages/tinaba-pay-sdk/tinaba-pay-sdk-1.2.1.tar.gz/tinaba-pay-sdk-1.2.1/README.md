<p align="center"><img src ="https://www.tinaba.com/wp-content/themes/tinaba/img/logos/logo-horizontal.svg" width=300 height=200 /></p>

# Tinaba Pay SDK (Python)

This package provides integration with the Tinaba Pay API for Python3.

## API reference

<a href="https://www.tinaba.com/it/developers/">Here</a> you can find the official API documentation.

## System Requirements

- Python >= 3.4

## Python Requirements
To install all needed python requirements, the following command can be run.

```bash
pip3 install -r requirements.txt
```

If you are using `pip`, these requirements will be automatically installed.

## Quick Start

In order to successfully communicate with Tinaba Pay APIs you need to
request your **Merchant ID** and **Secret** to Tinaba.

### Installing using `pip`

`pip install tinaba-pay-sdk`  <!-- TODO: name TBD -->

#### Configuring the client

To setup the API SDK you have to set the configurations of the client factory:

```python
from tinabasdk.apicontext import ApiContext
from tinabasdk.actions import TinabaFactory

config = {'mode': 'sandbox',
          'version': 'v1',
          'url_template': '{hostname}{base_url}{route}',
          'sandbox': {'timeout': 10,
                      'merchant_id': 'merch',
                      'secret': 'secret',
                      'hostname': 'https://valid.tinaba.tv',
                      'base_url': '/WebApi/tinaba/checkout',
                      'port': 443},
          'live': {'timeout': 10,
                   'merchant_id': 'merch',
                   'secret': 'secret',
                   'hostname': 'https://tfull.bancaprofilo.it',
                   'base_url': '/WebApi/tinaba/checkout',
                   'port': 443}}

context = ApiContext(config)

factory = TinabaFactory(context)
```

#### Sandbox Mode

To operate in sandbox mode set the config field `mode` to `"sandbox"` when
instantiating the `ApiContext` object. Once you do that all configurations will
be taken from the sub-dictionary `config["sandbox"]`.

## Examples

Once you have successfully managed to setup the SDK you can start making
API calls to the Tinaba Pay platform, by using the factory to instantiate
the actions you want to perform.

### Initialize a Checkout

```python
from tinabasdk.objects import InitCheckoutRequest
from datetime import datetime

action = factory.make('init.checkout')
action.body_params = InitCheckoutRequest(externalId='TR_01',
                                         amount='100',  # expressed in cents
                                         currency='EUR',
                                         description='Customized Mug purchase',
                                         validTo='10',  # expressed in minutes
                                         creationDateTime=datetime.now(),
                                         paymentMode=InitCheckoutRequest.MODE_ECOMMERCE,
                                         notificationCallback='https://example.com/TR_01/status',
                                         notificationHttpMethod='POST',
                                         backCallback='https://example.com/paymentcanceled',
                                         successCallback='https://example.com/paymentsuccess',
                                         failureCallback='https://example.com/paymentfailed',
                                         sendReceiverAddress=True)
response = action.run()
print('Payment code: {}'.format(response.paymentCode))
```

if not specified, the `sendReceiverAddress` field is assumed to be `False`. In case it is set to `True`,
the `VerifyCheckoutRequest` action will return the `userAddress` field.

Available payment modes are

```python
from tinabasdk.objects import InitCheckoutRequest
InitCheckoutRequest.MODE_PREAUTH
InitCheckoutRequest.MODE_ECOMMERCE
InitCheckoutRequest.MODE_MEDIA
```

### Confirm a Preauthorized checkout

```python
from tinabasdk.objects import ConfirmP2PtransferByCaptureRequest
action = factory.make('confirm.preauthorized.checkout')
action.body_params = ConfirmP2PtransferByCaptureRequest(externalId='TR_01',
                                                        amount='100')  # expressed in cents
response = action.run()

```

### Verify the checkout state


```python
from tinabasdk.objects import VerifyCheckoutRequest
action = factory.make('verify.checkout')
action.body_params = VerifyCheckoutRequest(externalId='TR_01')
response = action.run()
print('The checkout state is {}'.format(response.checkoutState))
```

in case the `InitCheckoutRequest` specified `sendReceiverAddress` set to `True`, the returned object will
include the field `userAddress`.

### Perform a full/partial refund of a checkout
```python
from tinabasdk.objects import RefundCheckoutRequest
action = factory.make('refund.checkout')
action.body_params = RefundCheckoutRequest(externalId='TR_01',
                                           amount='100')  # expressed in cents
response = action.run()
```

### Get the list of generated checkouts
```python
from tinabasdk.objects import GetCheckoutListRequest
from datetime import datetime
action = factory.make('get.checkout.list')
action.body_arams = GetCheckoutListRequest(dateFrom=datetime(year=2018,
                                                             month=1,
                                                             second=28).strftime('%Y-%m-%d'),
                                           dateTo=datetime(year=2018,
                                                           month=2,
                                                           second=28).strftime('%Y-%m-%d'))
response = action.run()
checkout_list = response.checkoutList

for checkout in checkout_list:
    print('Found checkout with ID {}'.format(checkout.externalId))
```

### Verify a callback
```python
from tinabasdk.callbacks import CheckoutStateCallback
from tinabasdk.exceptions import ValidationError

try:
    callback = CheckoutStateCallback.create(request.json(), secret)
    # handle callback
    # return a response with body {"status": "000"}
except ValidationError:
    # handle exception
```

### Check if a call was successful
```python
from tinabasdk.objects import RESPONSE_OK

response = action.run()

if response.status == RESPONSE_OK:
    print('Confirmation successful')
else:
    print('Confirmation failed with error code {}'.format(response.errorCode))
```
