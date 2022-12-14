

patient_schema = {
    "type": "object",
    "properties": {
        "created_at": {
            "type": "string",
            "format": "date-time"
        },
        "updated_at": {
            "type": "string",
            "format": "date-time"
        },
        "id": {
            "type": "integer"
        },
        "user_name": {
            "type": "string"
        },
        "uid": {
            "type": "string"
        },
        "gender": {
            "type": "string"
        },
        "age": {
            "type": "integer"
        },
        "height": {
            "type": "number",
            "format": "float"
        },
        "weight": {
            "type": "number",
            "format": "float"
        },
        "job": {
            "type": "string"
        },
        "edu": {
            "type": "string"
        },
        "special": {
            "type": "string"
        },
        "tel": {
            "type": "string"
        },
        "tumor": {
            "type": "string"
        },
        "tumor_metastasis": {
            "type": "string"
        },
        "tumor_treatment": {
            "type": "string"
        },
        "illness": {
            "type": "string"
        },
        "liver_function": {
            "type": "string"
        },
        "kidney_function": {
            "type": "string"
        },
        "cardiac_function": {
            "type": "string"
        },
        "allergy": {
            "type": "string"
        },
        "physical_q1": {
            "type": "string",
        },
        "physical_q2": {
            "type": "string",
        },
        "physical_q3": {
            "type": "string",
        },
        "physical_q4": {
            "type": "string",
        },
        "physical_q5": {
            "type": "string",
        },
        "physical_score": {
            "type": "float",
        }
    }
}


input_patient_schema = {
    "type": "object",
    "required": ["user_name", "gender", "age"],
    "properties": {
        "user_name": {
            "type": "string",
            "description": "????????????"
        },
        "uid": {
            "type": "string",
            "description": "??????id"
        },
        "gender": {
            "type": "string",
            "enum": ["0", "1"],
            "description": "??????"
        },
        "age": {
            "type": "integer",
            "description": "??????"
        },
        "height": {
            "type": "number",
            "format": "float",
            "description": "??????"
        },
        "weight": {
            "type": "number",
            "format": "float",
            "description": "??????"
        },
        "job": {
            "type": "string",
            "description": "??????"
        },
        "edu": {
            "type": "string",
            "description": "??????"
        },
        "special": {
            "type": "string",
            "description": "????????????"
        },
        "tel": {
            "type": "string",
            "description": "??????"
        },
        "tumor": {
            "type": "string",
            "description": "??????"
        },
        "tumor_metastasis": {
            "type": "string",
            "description": "????????????"
        },
        "tumor_treatment": {
            "type": "string",
            "description": "????????????"
        },
        "illness": {
            "type": "string",
            "description": "??????"
        },
        "liver_function": {
            "type": "string",
            "description": "?????????"
        },
        "kidney_function": {
            "type": "string",
            "description": "?????????"
        },
        "cardiac_function": {
            "type": "string",
            "description": "?????????"
        },
        "allergy": {
            "type": "string",
            "description": "?????????"
        },
        "physical_q1": {
            "type": "string",
            "description": "????????????Q1"
        },
        "physical_q2": {
            "type": "string",
            "description": "????????????Q2"
        },
        "physical_q3": {
            "type": "string",
            "description": "????????????Q3"
        },
        "physical_q4": {
            "type": "string",
            "description": "????????????Q4"
        },
        "physical_q5": {
            "type": "string",
            "description": "????????????Q5"
        },
        "physical_score": {
            "type": "float",
            "description": "??????????????????"
        }        
    }
}

patient_get_dict = {
    "responses": {
        "200": {
            "description": "patient list",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "array",
                        "items": {
                            **patient_schema
                        }
                    }
                }
            }
        },
    }
}


patient_post_dict = {
    "requestBody": {
        "description": "patient info",
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    **input_patient_schema
                }
            }
        }
    },
    "responses": {
        "200": {
            "description": "patient primary key",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "integer"
                            }
                        }
                    }
                }
            }
        }
    }
}

patient_delete_by_id_dict = {

    "parameters": [
        {
            "name": "pid",
            "in": "path",
            "description": "patient pid",
            "required": True,
            "schema": {
                "type": "integer"
            }
        }
    ],
    "responses": {
        "200": {
            "description": "patient primary key",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "integer"
                            }
                        }
                    }
                }
            }
        }
    }
}

patient_get_by_id_dict = {
    "parameters": [
        {
            "name": "pid",
            "in": "path",
            "description": "patient pid",
            "required": True,
            "schema": {
                "type": "integer"
            }
        }
    ],
    "responses": {
        "200": {
            "description": "patient info",
            "content": {
                "application/json": {
                    "schema": {
                        **patient_schema
                    }
                }
            }
        }
    }
}


drug_schema = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer"
        },
        "drug_id": {
            "type": "string"
        },
        "drug_name": {
            "type": "string"
        },
        "spc": {
            "type": "string"
        },
        "unit": {
            "type": "string"
        },
        "category": {
            "type": "string"
        },
        "high_dose": {
            "type": "string"
        },
        "exce_freq": {
            "type": "string"
        }
    }
}


drug_get_dict = {
    "responses": {
        "200": {
            "description": "drug list",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "array",
                        "items": {
                            **drug_schema
                        }
                    }
                }
            }
        },
    }
}
