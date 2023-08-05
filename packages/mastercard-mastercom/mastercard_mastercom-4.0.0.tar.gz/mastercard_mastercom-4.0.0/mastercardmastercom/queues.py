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

class Queues(BaseObject):
    """
    
    """

    __config = {
        
        "19cc9a5e-655f-4c77-8c90-6661bf529b0f" : OperationConfig("/mastercom/v4/queues", "list", [], ["queue-name"]),
        
        "1223cfeb-2843-4054-8611-ac72e3dd731e" : OperationConfig("/mastercom/v4/queues/names", "list", [], []),
        
    }

    def getOperationConfig(self,operationUUID):
        if operationUUID not in self.__config:
            raise Exception("Invalid operationUUID: "+operationUUID)

        return self.__config[operationUUID]

    def getOperationMetadata(self):
        return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext(), ResourceConfig.getInstance().getJsonNative(), ResourceConfig.getInstance().getContentTypeOverride())




    @classmethod
    def retrieveClaimsFromQueue(cls,criteria=None):
        """
        List objects of type Queues

        @param Dict criteria
        @return Array of Queues object matching the criteria.
        @raise ApiException: raised an exception from the response status
        """

        if not criteria :
            return BaseObject.execute("19cc9a5e-655f-4c77-8c90-6661bf529b0f", Queues())
        else:
            return BaseObject.execute("19cc9a5e-655f-4c77-8c90-6661bf529b0f", Queues(criteria))






    @classmethod
    def retrieveQueueNames(cls,criteria=None):
        """
        List objects of type Queues

        @param Dict criteria
        @return Array of Queues object matching the criteria.
        @raise ApiException: raised an exception from the response status
        """

        if not criteria :
            return BaseObject.execute("1223cfeb-2843-4054-8611-ac72e3dd731e", Queues())
        else:
            return BaseObject.execute("1223cfeb-2843-4054-8611-ac72e3dd731e", Queues(criteria))





