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

class Retrievals(BaseObject):
    """
    
    """

    __config = {
        
        "f28014ff-183e-4a2c-8ecb-e921ccc237f3" : OperationConfig("/mastercom/v4/claims/{claim-id}/retrievalrequests/{request-id}/fulfillments", "create", [], []),
        
        "6e5a72c9-c6b3-4358-93a1-01c1b7c5feba" : OperationConfig("/mastercom/v4/claims/{claim-id}/retrievalrequests", "create", [], []),
        
        "06318652-07fb-49ff-a3fc-fb4d67588873" : OperationConfig("/mastercom/v4/claims/{claim-id}/retrievalrequests/loaddataforretrievalrequests", "query", [], []),
        
        "bca0f291-99c1-4e72-a27d-f888decb8c6e" : OperationConfig("/mastercom/v4/claims/{claim-id}/retrievalrequests/{request-id}/documents", "query", [], ["format"]),
        
        "35213b18-64a7-4444-8eac-5ef7ce401739" : OperationConfig("/mastercom/v4/claims/{claim-id}/retrievalrequests/{request-id}/fulfillments/response", "create", [], []),
        
        "6d3afc8e-203a-4d2b-99d5-c40671e582a2" : OperationConfig("/mastercom/v4/retrievalrequests/imagestatus", "update", [], []),
        
        "0ed60ee4-182f-4aa1-b539-4fe2417ce153" : OperationConfig("/mastercom/v4/retrievalrequests/status", "update", [], []),
        
    }

    def getOperationConfig(self,operationUUID):
        if operationUUID not in self.__config:
            raise Exception("Invalid operationUUID: "+operationUUID)

        return self.__config[operationUUID]

    def getOperationMetadata(self):
        return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext(), ResourceConfig.getInstance().getJsonNative(), ResourceConfig.getInstance().getContentTypeOverride())


    @classmethod
    def acquirerFulfillARequest(cls,mapObj):
        """
        Creates object of type Retrievals

        @param Dict mapObj, containing the required parameters to create a new object
        @return Retrievals of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("f28014ff-183e-4a2c-8ecb-e921ccc237f3", Retrievals(mapObj))






    @classmethod
    def create(cls,mapObj):
        """
        Creates object of type Retrievals

        @param Dict mapObj, containing the required parameters to create a new object
        @return Retrievals of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("6e5a72c9-c6b3-4358-93a1-01c1b7c5feba", Retrievals(mapObj))











    @classmethod
    def getPossibleValueListsForCreate(cls,criteria):
        """
        Query objects of type Retrievals by id and optional criteria
        @param type criteria
        @return Retrievals object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("06318652-07fb-49ff-a3fc-fb4d67588873", Retrievals(criteria))






    @classmethod
    def getDocumentation(cls,criteria):
        """
        Query objects of type Retrievals by id and optional criteria
        @param type criteria
        @return Retrievals object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("bca0f291-99c1-4e72-a27d-f888decb8c6e", Retrievals(criteria))

    @classmethod
    def issuerRespondToFulfillment(cls,mapObj):
        """
        Creates object of type Retrievals

        @param Dict mapObj, containing the required parameters to create a new object
        @return Retrievals of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("35213b18-64a7-4444-8eac-5ef7ce401739", Retrievals(mapObj))







    def retrievalFullfilmentImageStatus(self):
        """
        Updates an object of type Retrievals

        @return Retrievals object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("6d3afc8e-203a-4d2b-99d5-c40671e582a2", self)






    def retrievalFullfilmentStatus(self):
        """
        Updates an object of type Retrievals

        @return Retrievals object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("0ed60ee4-182f-4aa1-b539-4fe2417ce153", self)






