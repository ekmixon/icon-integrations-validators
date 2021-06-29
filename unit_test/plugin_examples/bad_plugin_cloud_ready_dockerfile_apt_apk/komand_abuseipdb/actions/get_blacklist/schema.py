# GENERATED BY KOMAND SDK - DO NOT EDIT
import insightconnect_plugin_runtime
import json


class Component:
    DESCRIPTION = "List of blacklisted IP addresses"


class Input:
    CONFIDENCEMINIMUM = "confidenceMinimum"
    LIMIT = "limit"
    

class Output:
    BLACKLIST = "blacklist"
    SUCCESS = "success"
    

class GetBlacklistInput(insightconnect_plugin_runtime.Input):
    schema = json.loads("""
   {
  "type": "object",
  "title": "Variables",
  "properties": {
    "confidenceMinimum": {
      "type": "string",
      "title": "Confidence Minimum",
      "description": "Minimum confidence to filter by, scaled 0-100, least to most confident",
      "order": 1
    },
    "limit": {
      "type": "string",
      "title": "Limit",
      "description": "Max length of blacklist",
      "order": 2
    }
  },
  "required": [
    "confidenceMinimum"
  ]
}
    """)

    def __init__(self):
        super(self.__class__, self).__init__(self.schema)


class GetBlacklistOutput(insightconnect_plugin_runtime.Output):
    schema = json.loads("""
   {
  "type": "object",
  "title": "Variables",
  "properties": {
    "blacklist": {
      "type": "array",
      "title": "Blacklist",
      "description": "List of abusive IPs",
      "items": {
        "$ref": "#/definitions/blacklisted"
      },
      "order": 1
    },
    "success": {
      "type": "boolean",
      "title": "Success",
      "description": "Was the blacklist successfully retrieved",
      "order": 2
    }
  },
  "required": [
    "success"
  ],
  "definitions": {
    "blacklisted": {
      "type": "object",
      "title": "blacklisted",
      "properties": {
        "abuseConfidenceScore": {
          "type": "string",
          "title": "Abuse Confidence Score",
          "description": "Confidence that IP is abusive",
          "order": 2
        },
        "ipAddress": {
          "type": "string",
          "title": "IP Address",
          "description": "IP Address of abusive IP",
          "order": 1
        }
      },
      "required": [
        "abuseConfidenceScore",
        "ipAddress"
      ]
    }
  }
}
    """)

    def __init__(self):
        super(self.__class__, self).__init__(self.schema)