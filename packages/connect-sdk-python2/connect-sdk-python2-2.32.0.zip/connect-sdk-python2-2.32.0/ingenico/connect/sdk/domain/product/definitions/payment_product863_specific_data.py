# -*- coding: utf-8 -*-
#
# This class was auto-generated from the API references found at
# https://epayments-api.developer-ingenico.com/s2sapi/v1/
#
from ingenico.connect.sdk.data_object import DataObject


class PaymentProduct863SpecificData(DataObject):

    __integration_types = None

    @property
    def integration_types(self):
        """
        | The WeChat Pay integration types that can be used in the current payment context. Possible values:
        
        * desktopQRCode - used on desktops, the consumer opens the WeChat app by scanning a QR code.
        * urlIntent - used in mobile apps or on mobile web pages, the consumer opens the WeChat app using a URL intent.
        * nativeInApp - used in mobile apps that use the WeChat Pay SDK.
        
        Type: list[str]
        """
        return self.__integration_types

    @integration_types.setter
    def integration_types(self, value):
        self.__integration_types = value

    def to_dictionary(self):
        dictionary = super(PaymentProduct863SpecificData, self).to_dictionary()
        self._add_to_dictionary(dictionary, 'integrationTypes', self.integration_types)
        return dictionary

    def from_dictionary(self, dictionary):
        super(PaymentProduct863SpecificData, self).from_dictionary(dictionary)
        if 'integrationTypes' in dictionary:
            if not isinstance(dictionary['integrationTypes'], list):
                raise TypeError('value \'{}\' is not a list'.format(dictionary['integrationTypes']))
            self.integration_types = []
            for integrationTypes_element in dictionary['integrationTypes']:
                self.integration_types.append(integrationTypes_element)
        return self
