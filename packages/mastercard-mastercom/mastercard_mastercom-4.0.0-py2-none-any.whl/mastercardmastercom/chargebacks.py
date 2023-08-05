#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (c) 2016 MasterCard International Incorporated
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of
# conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of
# conditions and the following disclaimer in the documentation and/or other materials
# provided with the distribution.
# Neither the name of the MasterCard International Incorporated nor the names of its
# contributors may be used to endorse or promote products derived from this software
# without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#


from __future__ import absolute_import
from mastercardapicore import BaseObject
from mastercardapicore import RequestMap
from mastercardapicore import OperationConfig
from mastercardapicore import OperationMetadata
from mastercardmastercom import ResourceConfig

class Chargebacks(BaseObject):
    """
    
    """

    __config = {
        
        "8caca31a-f7d7-4719-ba1c-affc9df2f33c" : OperationConfig("/mastercom/v4/chargebacks/acknowledge", "update", [], []),
        
        "75ff4cd6-97ca-491f-863f-0b027deee4e4" : OperationConfig("/mastercom/v4/claims/{claim-id}/chargebacks", "create", [], []),
        
        "fca18550-8d4b-4b37-b253-b461bdcb8e96" : OperationConfig("/mastercom/v4/claims/{claim-id}/chargebacks/{chargeback-id}/reversal", "create", [], []),
        
        "c8f0cdce-01ba-4ff7-a9f6-029fac9649a6" : OperationConfig("/mastercom/v4/claims/{claim-id}/chargebacks/{chargeback-id}/documents", "query", [], ["format"]),
        
        "cca60c0d-4a89-4a2e-a28b-b1170658cc78" : OperationConfig("/mastercom/v4/claims/{claim-id}/chargebacks/loaddataforchargebacks", "create", [], []),
        
        "3dbab9a1-f20a-4900-b123-c9f11e903ce8" : OperationConfig("/mastercom/v4/chargebacks/imagestatus", "update", [], []),
        
        "9c6624a6-0bb9-417f-a5ff-b3e942ec8d6a" : OperationConfig("/mastercom/v4/chargebacks/status", "update", [], []),
        
        "9e3779d9-5fd5-4060-87fc-2c2a82f0b6ce" : OperationConfig("/mastercom/v4/claims/{claim-id}/chargebacks/{chargeback-id}", "update", [], []),
        
    }

    def getOperationConfig(self,operationUUID):
        if operationUUID not in self.__config:
            raise Exception("Invalid operationUUID: "+operationUUID)

        return self.__config[operationUUID]

    def getOperationMetadata(self):
        return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext(), ResourceConfig.getInstance().getJsonNative(), ResourceConfig.getInstance().getContentTypeOverride())



    def acknowledgeReceivedChargebacks(self):
        """
        Updates an object of type Chargebacks

        @return Chargebacks object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("8caca31a-f7d7-4719-ba1c-affc9df2f33c", self)





    @classmethod
    def create(cls,mapObj):
        """
        Creates object of type Chargebacks

        @param Dict mapObj, containing the required parameters to create a new object
        @return Chargebacks of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("75ff4cd6-97ca-491f-863f-0b027deee4e4", Chargebacks(mapObj))






    @classmethod
    def createReversal(cls,mapObj):
        """
        Creates object of type Chargebacks

        @param Dict mapObj, containing the required parameters to create a new object
        @return Chargebacks of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("fca18550-8d4b-4b37-b253-b461bdcb8e96", Chargebacks(mapObj))











    @classmethod
    def retrieveDocumentation(cls,criteria):
        """
        Query objects of type Chargebacks by id and optional criteria
        @param type criteria
        @return Chargebacks object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("c8f0cdce-01ba-4ff7-a9f6-029fac9649a6", Chargebacks(criteria))

    @classmethod
    def getPossibleValueListsForCreate(cls,mapObj):
        """
        Creates object of type Chargebacks

        @param Dict mapObj, containing the required parameters to create a new object
        @return Chargebacks of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("cca60c0d-4a89-4a2e-a28b-b1170658cc78", Chargebacks(mapObj))







    def chargebacksImageStatus(self):
        """
        Updates an object of type Chargebacks

        @return Chargebacks object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("3dbab9a1-f20a-4900-b123-c9f11e903ce8", self)






    def chargebacksStatus(self):
        """
        Updates an object of type Chargebacks

        @return Chargebacks object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("9c6624a6-0bb9-417f-a5ff-b3e942ec8d6a", self)






    def update(self):
        """
        Updates an object of type Chargebacks

        @return Chargebacks object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("9e3779d9-5fd5-4060-87fc-2c2a82f0b6ce", self)






