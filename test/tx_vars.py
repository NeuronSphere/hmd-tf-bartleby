import os

import yaml


version = "0.1"
os.environ["PWD"] = os.getcwd()
print(os.environ["PWD"])
if os.path.exists("./instance_configuration.yaml"):
    with open("./instance_configuration.yaml", "r") as ic:
        cfg = yaml.safe_load(ic)
        version = cfg.get("version")

set_one = {
    "TRANSFORM_INSTANCE_CONTEXT": '{"shell": "html"}',
    "TRANSFORM_NID": "transform-test-reg1-hmd-123456789101",
    "TRANSFORM_INPUT": "input_files1",
    "TRANSFORM_OUTPUT": "output_files1",
    "CONFIDENTIALITY_STATEMENT": """HMD Labs Confidential – This document contains information that is confidential and proprietary. Neither this
document nor the information herein may be reproduced, used, or disclosed to or for the benefit of any third
party without the prior written consent of HMD Labs.""",
    "output_files": ["html/index.html", "html/readme.html"],
}

set_two = {
    "TRANSFORM_INSTANCE_CONTEXT": '{"shell": "pdf"}',
    "TRANSFORM_NID": "transform-test-reg1-hmd-123456789101",
    "TRANSFORM_INPUT": "input_files1",
    "TRANSFORM_OUTPUT": "output_files1",
    "CONFIDENTIALITY_STATEMENT": "",
    "output_files": ["latex/bartleby-test-0.1-linux-amd64.pdf"],
}
