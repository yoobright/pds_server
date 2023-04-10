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
        "physical_q1": {
            "type": "string",
            "description": "身体状况Q1"
        },
        "physical_q2": {
            "type": "string",
            "description": "身体状况Q2"
        },
        "physical_q3": {
            "type": "string",
            "description": "身体状况Q3"
        },
        "physical_q4": {
            "type": "string",
            "description": "身体状况Q4"
        },
        "physical_q5": {
            "type": "string",
            "description": "身体状况Q5"
        },
        "physical_score": {
            "type": "string",
            "description": "身体状况分数"
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
        "201": {
            "description": " patient created and return primary key",
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
        "204": {
            "description": "patient deleted and return primary key",
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

diagnostic_brief_schema = {
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
        "uuid": {
            "type": "string",
            "format": "uuid"
        },
        "patient_basic_info_id": {
            "type": "integer"
        },
        "pain_assessment_info_id": {
            "type": "integer"
        },
        "prev_medication_info_id": {
            "type": "integer"
        },
        "decision_info_id": {
            "type": "integer"
        },
        "doctor_id": {
            "type": "integer"
        },
        "previous_medication_issue": {
            "type": "string"
        },
        "recmd": {
            "type": "string"
        },
        "feedback_score": {
            "type": "integer"
        },
        "patient_basic_info": {
            "type": "object",
            "properties": {
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
                "physical_score": {
                    "type": "string"
                }
            }
        }
    }
}

diagnostic_get_dict = {
    "parameters": [
        {
            "name": "user_name",
            "in": "query",
            "description": "user name",
            "schema": {
                "type": "string"
            }
        },
        {
            "name": "page",
            "in": "query",
            "description": "page",
            "schema": {
                "type": "integer"
            }
        },
        {
            "name": "limit",
            "in": "query",
            "description": "limit",
            "schema": {
                "type": "integer"
            }
        }
    ],
    "responses": {
        "200": {
            "description": "diagnostic list",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "total": {
                                "type": "integer"
                            },
                            "data": {
                                "type": "array",
                                "items": {
                                    **diagnostic_brief_schema
                                }
                            }
                        }
                    }
                }
            }
        },
    }
}

diagnostic_post_dict = {
    "requestBody": {
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "uuid": {
                            "type": "string",
                            "format": "uuid"
                        },
                        "patient_basic_info_id": {
                            "type": "integer"
                        },
                        "pain_assessment_info_id": {
                            "type": "integer"
                        },
                        "prev_medication_info_id": {
                            "type": "integer"
                        },
                        "decision_info_id": {
                            "type": "integer"
                        },
                        "doctor_id": {
                            "type": "integer"
                        },
                        "previous_medication_issue": {
                            "type": "string"
                        },
                        "recmd": {
                            "type": "string"
                        }
                    }
                }
            }
        }
    },

    "responses": {
        "201": {
            "description": "diagnostic created",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "integer"
                            },
                            "uuid": {
                                "type": "string",
                                "format": "uuid"
                            }
                        }
                    }
                }
            }
        },
        "422": {
            "description": "diagnostic not created",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "integer",
                                "enum": [-1]
                            }
                        }
                    }
                }
            }
        },
    }
}

pain_assessment_schema = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer",
        },
        "diagnostic_uuid": {
            "type": "string",
            "format": "uuid"
        },
        "causes": {
            "type": "string",
        },
        "body_parts": {
            "type": "string",
        },
        "pain_extra": {
            "type": "string",
        },
        "pain_score": {
            "type": "number",
        },
        "character": {
            "type": "string",
        },
        "level": {
            "type": "integer",
        },
        "aggravating_factors": {
            "type": "string",
        },
        "relief_factors": {
            "type": "string",
        },
        "breakout_type": {
            "type": "string",
        },
        "breakout_freq": {
            "type": "string",
        },
    }
}

prev_medication_schema = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer",
        },
        "uuid": {
            "type": "string",
            "format": "uuid"
        },
        "diagnostic_uuid": {
            "type": "string",
            "format": "uuid"
        },
        "compliance_q1": {
            "type": "string",
        },
        "compliance_q2": {
            "type": "string",
        },
        "compliance_q3": {
            "type": "string",
        },
        "compliance_q4": {
            "type": "string",
        },
        "adverse_reaction": {
            "type": "string",
        },
        "adverse_reaction_drugs": {
            "type": "string",
        },
        "drug_table_id": {
            "type": "string",
        },
        "drug_table": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "drug_name": {
                        "type": "string",
                    },
                    "spec": {
                        "type": "string",
                    },
                    "dose": {
                        "type": "number",
                    },
                    "dose_unit": {
                        "type": "string",
                    },
                    "freq": {
                        "type": "string",
                    },
                    "freq_unit": {
                        "type": "string",
                    },
                    "duration": {
                        "type": "string",
                    },
                }
            }
        }
    }
}

decision_schema = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer",
        },
        "uuid": {
            "type": "string",
            "format": "uuid"
        },
        "diagnostic_uuid": {
            "type": "string",
            "format": "uuid"
        },
        "drug_table_id": {
            "type": "string",
        },
        "previous_medication_issue": {
            "type": "string",
        },
        "recmd": {
            "type": "string",
        },
        "recmd_constraint": {
            "type": "string",
        },
        "pcne_constraint": {
            "type": "string",
        },
        "drug_table": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "drug_name": {
                        "type": "string",
                    },
                    "spec": {
                        "type": "string",
                    },
                    "dose": {
                        "type": "number",
                    },
                    "dose_unit": {
                        "type": "string",
                    },
                    "freq": {
                        "type": "string",
                    },
                    "freq_unit": {
                        "type": "string",
                    },
                    "duration": {
                        "type": "string",
                    }
                }
            }
        }
    }
}

diagnostic_get_responses = {
    "200": {
        "description": "successful operation",
        "content": {
            "application/json": {
                "schema": {
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
                        "uuid": {
                            "type": "string"
                        },
                        "patient_basic_info_id": {
                            "type": "integer"
                        },
                        "pain_assessment_info_id": {
                            "type": "integer"
                        },
                        "prev_medication_info_id": {
                            "type": "integer"
                        },
                        "decision_info_id": {
                            "type": "integer"
                        },
                        "doctor_id": {
                            "type": "integer"
                        },
                        "previous_medication_issue": {
                            "type": "string"
                        },
                        "recmd": {
                            "type": "string"
                        },
                        "feedback_score": {
                            "type": "integer"
                        },
                        "patient_basic_info": {
                            **patient_schema
                        },
                        "pain_assessment_info": {
                            **pain_assessment_schema
                        },
                        "prev_medication_info": {
                            **prev_medication_schema
                        },
                        "decision_info": {
                            **decision_schema
                        }
                    }
                }
            }
        }
    }
}

diagnostic_uuid_get_dict = {
    "responses": {
        **diagnostic_get_responses
    }
}

diagnostic_uuid_post_dict = {
    "requestBody": {
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "previous_medication_issue": {
                            "type": "string"
                        },
                        "recmd": {
                            "type": "string"
                        },
                        "feedback_score": {
                            "type": "integer"
                        }
                    }
                }
            }
        }
    },
    "responses": {
        "200": {
            "description": "successful operation",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "uuid": {
                                "type": "string",
                                "format": "uuid"
                            }
                        }
                    }
                }
            }
        },
        "400": {
            "description": "invalid input",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                            }
                        }
                    }
                }
            }
        }
    }
}

diagnostic_patient_get_dict = {
    "parameters": [
        {
            "name": "user_name",
            "in": "query",
            "required": True,
            "schema": {
                "type": "string"
            }
        },
        {

            "name": "uid",
            "in": "query",
            "required": True,
            "schema": {
                "type": "string"
            }
        },
        {
            "name": "latest",
            "in": "query",
            "required": False,
            "schema": {
                "type": "boolean"
            }
        }
    ],

    "responses": {
        **diagnostic_get_responses
    }
}

pain_assessment_post_dict = {
    "requestBody": {
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "causes": {
                            "type": "string"
                        },
                        "body_parts": {
                            "type": "string"
                        },
                        "pain_extra": {
                            "type": "string"
                        },
                        "character": {
                            "type": "string"
                        },
                        "level": {
                            "type": "integer"
                        },
                        "aggravating_factors": {
                            "type": "string"
                        },
                        "relief_factors": {
                            "type": "string"
                        },
                        "breakout_type": {
                            "type": "string"
                        },
                        "breakout_freq": {
                            "type": "string"
                        }
                    }
                }
            }
        }
    },
    "responses": {
        "201": {
            "description": "successful operation",
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
        },
        "422": {
            "description": "diagnostic not created",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "integer",
                                "enum": [-1]
                            }
                        }
                    }
                }
            }
        },
    }
}

drug_table_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "drug_name": {"type": "string"},
            "spec": {"type": "string"},
            "dose": {"type": "number"},
            "dose_unit": {"type": "string"},
            "freq": {"type": "string"},
            "freq_unit": {"type": "string"},
            "duration": {"type": "string"}
        },
        "required": ["drug_name", "spec", "dose", "dose_unit",
                     "freq", "freq_unit", "duration"]
    }
}

decision_post_dict = {
    "requestBody": {
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "drug_table": {
                            **drug_table_schema
                        },
                        "previous_medication_issue": {
                            "type": "string"
                        },
                        "recmd": {
                            "type": "string"
                        },
                        "recmd_constraint": {
                            "type": "boolean"
                        },
                        "pcne_constraint": {
                            "type": "boolean"
                        }
                    }
                }
            }
        }
    },
}

previous_medication_post_dict = {
    "requestBody": {
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "diagnostic_uuid": {
                            "type": "string"
                        },
                        "drug_table": {
                            **drug_table_schema
                        },
                        "compliance_q1": {
                            "type": "string"
                        },
                        "compliance_q2": {
                            "type": "string"
                        },
                        "compliance_q3": {
                            "type": "string"
                        },
                        "compliance_q4": {
                            "type": "string"
                        },
                        "adverse_reaction": {
                            "type": "string"
                        },
                        "adverse_reaction_drugs": {
                            "type": "string"
                        }
                    }
                }
            }
        }
    },
}
