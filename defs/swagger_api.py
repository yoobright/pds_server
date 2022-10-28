

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
        "physical": {
            "type": "string"
        }
    }
}


input_patient_schema = {
    "type": "object",
    "required": ["user_name", "gender", "age"],
    "properties": {
        "user_name": {
            "type": "string",
            "description": "病人名称"
        },
        "uid": {
            "type": "string",
            "description": "用户id"
        },
        "gender": {
            "type": "string",
            "enum": ["0", "1"],
            "description": "性别"
        },
        "age": {
            "type": "integer",
            "description": "年龄"
        },
        "height": {
            "type": "number",
            "format": "float",
            "description": "身高"
        },
        "weight": {
            "type": "number",
            "format": "float",
            "description": "体重"
        },
        "job": {
            "type": "string",
            "description": "职业"
        },
        "edu": {
            "type": "string",
            "description": "学历"
        },
        "special": {
            "type": "string",
            "description": "特殊情况"
        },
        "tel": {
            "type": "string",
            "description": "电话"
        },
        "tumor": {
            "type": "string",
            "description": "肿瘤"
        },
        "tumor_metastasis": {
            "type": "string",
            "description": "肿瘤转移"
        },
        "tumor_treatment": {
            "type": "string",
            "description": "肿瘤治疗"
        },
        "illness": {
            "type": "string",
            "description": "疾病"
        },
        "liver_function": {
            "type": "string",
            "description": "肝功能"
        },
        "kidney_function": {
            "type": "string",
            "description": "肾功能"
        },
        "cardiac_function": {
            "type": "string",
            "description": "心功能"
        },
        "allergy": {
            "type": "string",
            "description": "过敏史"
        },
        "physical": {
            "type": "string",
            "description": "身体状况"
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
