import unittest
import os
import tests
import json
import logging

import checkout_sdk as sdk

from checkout_sdk import HttpClient, Config, Utils
from checkout_sdk.payments import PaymentsClient, PaymentResponse
from checkout_sdk.tokens import TokensClient
from tests.base import CheckoutSdkTestCase
from enum import Enum


class PaymentsClientTests(CheckoutSdkTestCase):
    def setUp(self):
        super().setUp()
        self.http_client = HttpClient(Config())
        self.token_client = TokensClient(self.http_client)
        self.client = PaymentsClient(self.http_client)

    def tearDown(self):
        super().tearDown()
        self.http_client.close_session()

    def test_bad_payment_response_init(self):
        with self.assertRaises(TypeError):
            PaymentResponse(False)

    def test_payments_client_full_card_auth_request(self):
        payment = self.auth_card()

        self.assertEqual(payment.http_response.status, 200)
        self.assertIsNotNone(payment.created)

        # test payment
        self.assertIsNotNone(payment.id)
        self.assertTrue(payment.approved)
        self.assertIsNotNone(payment.auth_code)
        self.assertEqual(payment.value, 100)
        self.assertEqual(payment.currency, 'USD')
        self.assertEqual(payment.track_id, 'ORDER-001-002')
        self.assertFalse(payment.requires_redirect)

        # test card
        self.assertIsNotNone(payment.card.id)
        self.assertEqual(int(payment.card.expiryMonth), 6)
        self.assertEqual(int(payment.card.expiryYear), 2025)
        self.assertEqual(payment.card.last4, '4242')
        self.assertEqual(payment.card.name, 'Joe Smith')

        # test customer
        self.assertIsNotNone(payment.customer.id)
        self.assertEqual(payment.customer.email, 'joesmith@gmail.com')

        # test other content from the http body
        body = payment.http_response.body

        self.assertEqual(body['card']['billingDetails']['city'], 'London')
        self.assertEqual(body['transactionIndicator'],
                         sdk.PaymentType.Recurring.value)  # pylint: disable = no-member
        self.assertEqual(body['udf1'], 'udf1')
        # below is also a test of snake >> camel casing.
        self.assertEqual(body['customerIp'], '8.8.8.8')
        self.assertEqual(body['products'][0]['price'], 2000)

    def test_payments_client_3d_full_card_auth_request(self):
        payment = self.auth_card(threeds=True)

        self.assertTrue(payment.requires_redirect)
        self.assertTrue(payment.charge_mode == sdk.ChargeMode.ThreeDS.value)  # pylint: disable = no-member

    def test_payments_client_3d_full_card_auth_request_with_downgrade(self):
        # value 5000 will trigger 20153 (https://docs.checkout.com/docs/testing#section-response-codes)
        payment = self.auth_card(value=5000, threeds=True, attempt_n3d=True)

        self.assertTrue(payment.requires_redirect)
        self.assertTrue(payment.downgraded)

    def test_payments_client_get_request(self):
        payment = self.auth_card()
        # get the previous auth request
        response = self.client.get(payment.id)

        self.assertEqual(response.http_response.status, 200)
        self.assertEqual(payment.id, response.id)
        # TODO: improve test to compare all GET value with previous Auth response values

    def test_payments_history_response(self):
        payment = self.auth_card()
        # history on the previous auth request
        history = self.client.history(payment.id)
        self.assertEqual(history.http_response.status, 200)
        self.assertTrue(len(history.charges) == 1)

        self.assertIsNotNone(history.charges[0].id)
        self.assertEqual(history.charges[0].value, 100)
        self.assertEqual(history.charges[0].currency, 'USD')
        self.assertIsNotNone(history.charges[0].created)
        self.assertIsNotNone(history.charges[0].track_id)
        self.assertIsNotNone(history.charges[0].email)
        self.assertIsNotNone(history.charges[0].status)
        self.assertIsNotNone(history.charges[0].response_code)

        # history after capture
        capture = self.client.capture(payment.id)
        self.assertEqual(capture.http_response.status, 200)

        history = self.client.history(payment.id)
        self.assertEqual(history.http_response.status, 200)
        self.assertTrue(len(history.charges) == 2)

    def test_payments_client_capture_full_amount_request(self):
        payment = self.auth_card(value=150)
        # capture the previous auth request
        response = self.client.capture(payment.id,
                                       track_id='ORDER-001-002-CAPTURE')

        self.assertEqual(response.http_response.status, 200)
        # test payment
        self.assertIsNotNone(response.id)
        self.assertIsNotNone(response.original_id)
        self.assertEqual(payment.id, response.original_id)
        self.assertEqual(response.track_id, 'ORDER-001-002-CAPTURE')
        self.assertEqual(response.value, 150)
        self.assertTrue(response.approved)

    def test_payments_client_capture_partial_amount_request(self):
        payment = self.auth_card(value=150)
        # capture the previous auth request
        response = self.client.capture(payment.id, value=100,
                                       track_id='ORDER-001-002-CAPTURE')

        self.assertEqual(response.http_response.status, 200)
        # test payment
        self.assertIsNotNone(response.id)
        self.assertIsNotNone(response.original_id)
        self.assertEqual(response.track_id, 'ORDER-001-002-CAPTURE')
        self.assertEqual(response.value, 100)
        self.assertTrue(response.approved)

    def test_payments_client_void_request(self):
        payment = self.auth_card()
        # void the previous auth request
        response = self.client.void(payment.id,
                                    track_id='ORDER-001-002-VOID')

        self.assertEqual(response.http_response.status, 200)
        # test payment
        self.assertIsNotNone(response.id)
        self.assertIsNotNone(response.original_id)
        self.assertEqual(response.track_id, 'ORDER-001-002-VOID')
        self.assertTrue(response.approved)

    def test_payments_client_refund_full_amount_request(self):
        payment = self.auth_card(value=150)
        # capture the previous auth request
        capture = self.client.capture(payment.id,
                                      track_id='ORDER-001-002-CAPTURE')
        self.assertEqual(payment.id, capture.original_id)
        # refund the capture
        response = self.client.refund(capture.id,
                                      track_id='ORDER-001-002-REFUND')
        self.assertEqual(response.http_response.status, 200)
        # test payment
        self.assertIsNotNone(response.id)
        self.assertIsNotNone(response.original_id)
        self.assertEqual(capture.id, response.original_id)
        self.assertEqual(response.track_id, 'ORDER-001-002-REFUND')
        self.assertEqual(response.value, 150)
        self.assertTrue(response.approved)

    def test_payments_client_multiple_partial_refunds_request(self):
        payment = self.auth_card(value=150)
        # capture the previous auth request
        capture = self.client.capture(payment.id,
                                      track_id='ORDER-001-002-CAPTURE')
        self.assertEqual(payment.id, capture.original_id)
        # partial refund the capture
        response1 = self.client.refund(capture.id, value=50,
                                       track_id='ORDER-001-002-REFUND-1')
        self.assertTrue(response1.approved)
        self.assertEqual(response1.value, 50)

        response2 = self.client.refund(capture.id, value=80,
                                       track_id='ORDER-001-002-REFUND-2')
        self.assertTrue(response2.approved)
        self.assertEqual(response2.value, 80)

    def test_alternative_payment_information(self):
        info = self.client.alternative_payment_info(sdk.AlternativePaymentMethodId.IDEAL)
        self.assertIsNotNone(info.http_response.body)

    def test_alternative_payment_information_with_unsupported_apm(self):
        with self.assertRaises(ValueError):
            self.client.alternative_payment_info('unsupported')

    def test_alternative_payment_request(self):
        token = self.token_client.request_payment_token(
            value=100, currency=sdk.Currency.EUR
        )
        payment = self.client.alternative_payment_request(
            apm_id=sdk.AlternativePaymentMethodId.IDEAL,
            payment_token=token.id,
            user_data={
                'issuerId': 'INGBNL2A'
            },
            customer='joesmith@gmail.com'
        )
        self.assertTrue(payment.id.startswith('pay_tok'))
        self.assertTrue(payment.requires_redirect)
        self.assertIsNotNone(payment.redirect_url)

    def auth_card(self, value=None, threeds=False, attempt_n3d=False):
        return self.client.request(
            card={
                'number': '4242424242424242',
                'expiryMonth': 6,
                'expiry_year': 2025,  # testing that snake_case is automatically converted
                'cvv': '100',
                'name': 'Joe Smith',
                'billingDetails': {
                    'addressLine1': '1 London Street',
                    'postcode': 'W1',
                    'country': 'GB',
                    'city': 'London',
                    'state': 'Central London',
                    'phone': {
                        'countryCode': '44',
                        'number': '203 123 1234'
                    }
                }
            },
            value=value or 100,  # cents
            currency=sdk.Currency.USD,  # or 'usd'
            auto_capture=False,
            payment_type=sdk.PaymentType.Recurring,
            charge_mode=2 if threeds else 1,
            attempt_n3d=attempt_n3d,
            track_id='ORDER-001-002',
            customer='joesmith@gmail.com',
            udf1='udf1',
            customer_ip='8.8.8.8',
            products=[{
                "description": "Blue Medium",
                "name": "T-Shirt",
                "price": 2000,
                "quantity": 1,
                "shippingCost": 50,
                "sku": "tee123"
            }]
        )
