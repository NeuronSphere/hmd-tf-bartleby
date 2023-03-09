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
    "DEFAULT_LOGO": "",
    "CONFIDENTIALITY_STATEMENT": """HMD Labs Confidential – This document contains information that is confidential and proprietary. Neither this
document nor the information herein may be reproduced, used, or disclosed to or for the benefit of any third
party without the prior written consent of HMD Labs.""",
    "output_files": ["html/index.html", "html/readme.html"],
}

set_two = {
    "TRANSFORM_INSTANCE_CONTEXT": '{"shell": "pdf"}',
    "TRANSFORM_NID": "transform-test-reg1-hmd-123456789101",
    "TRANSFORM_INPUT": "input_files1",
    "TRANSFORM_OUTPUT": "output_files2",
    "CONFIDENTIALITY_STATEMENT": "",
    "DEFAULT_LOGO": "",
    "output_files": [f"latex/bartleby-test-{version}.pdf"],
}

confidential_pdf_one = {
    "TRANSFORM_INSTANCE_CONTEXT": '{"shell": "pdf"}',
    "TRANSFORM_NID": "transform-test-reg1-hmd-123456789101",
    "TRANSFORM_INPUT": "input_files1",
    "TRANSFORM_OUTPUT": "output_files_pdf_1",
    "CONFIDENTIALITY_STATEMENT": """HMD Labs Test""",
    "DEFAULT_LOGO": "",
    "output_files": [f"latex/bartleby-test-{version}.pdf"],
}


confidential_pdf_two = {
    "TRANSFORM_INSTANCE_CONTEXT": '{"shell": "pdf"}',
    "TRANSFORM_NID": "transform-test-reg1-hmd-123456789101",
    "TRANSFORM_INPUT": "input_files1",
    "TRANSFORM_OUTPUT": "output_files_pdf_2",
    "DEFAULT_LOGO": "",
    "CONFIDENTIALITY_STATEMENT": """Test statement""",
    "output_files": [f"latex/bartleby-test-{version}.pdf"],
}

default_cover_image = {
    "TRANSFORM_INSTANCE_CONTEXT": '{"shell": "pdf"}',
    "TRANSFORM_NID": "transform-test-reg1-hmd-123456789101",
    "TRANSFORM_INPUT": "input_files1",
    "TRANSFORM_OUTPUT": "output_files3",
    "DEFAULT_LOGO": "",
    "CONFIDENTIALITY_STATEMENT": """HMD Labs Confidential – This document contains information that is confidential and proprietary. Neither this
document nor the information herein may be reproduced, used, or disclosed to or for the benefit of any third
party without the prior written consent of HMD Labs.""",
    "output_files": [
        f"latex/bartleby-test-{version}.pdf",
        f"latex/bartleby-test-{version}.tex",
    ],
    "logo_file": "NeuronSphereSwoosh.jpg",
}


default_pdf_cover_image = {
    "TRANSFORM_INSTANCE_CONTEXT": '{"shell": "pdf"}',
    "TRANSFORM_NID": "transform-test-reg1-hmd-123456789101",
    "TRANSFORM_INPUT": "input_files1",
    "TRANSFORM_OUTPUT": "output_files4",
    "CONFIDENTIALITY_STATEMENT": """HMD Labs Confidential – This document contains information that is confidential and proprietary. Neither this
document nor the information herein may be reproduced, used, or disclosed to or for the benefit of any third
party without the prior written consent of HMD Labs.""",
    "DEFAULT_LOGO": "https://www.neuronsphere.io/hs-fs/hubfs/NeuronSphere_Trios.png?width=500&height=379&name=NeuronSphere_Trios.png",
    "output_files": [
        f"latex/bartleby-test-{version}.pdf",
        f"latex/bartleby-test-{version}.tex",
    ],
    "logo_file": "NeuronSphere_Trios.png",
}


html_logo_default = {
    "TRANSFORM_INSTANCE_CONTEXT": '{"shell": "html"}',
    "TRANSFORM_NID": "transform-test-reg1-hmd-123456789101",
    "TRANSFORM_INPUT": "input_files1",
    "TRANSFORM_OUTPUT": "output_files_html_1",
    "DEFAULT_LOGO": "",
    "CONFIDENTIALITY_STATEMENT": """HMD Labs Confidential – This document contains information that is confidential and proprietary. Neither this
document nor the information herein may be reproduced, used, or disclosed to or for the benefit of any third
party without the prior written consent of HMD Labs.""",
    "output_files": ["html/index.html", "html/readme.html"],
    "logo_file": "NeuronSphereSwoosh.jpg",
}


html_logo_dynamic = {
    "TRANSFORM_INSTANCE_CONTEXT": '{"shell": "html"}',
    "TRANSFORM_NID": "transform-test-reg1-hmd-123456789101",
    "TRANSFORM_INPUT": "input_files1",
    "TRANSFORM_OUTPUT": "output_files_html_2",
    "DEFAULT_LOGO": "https://www.neuronsphere.io/hs-fs/hubfs/NeuronSphere_Trios.png?width=500&height=379&name=NeuronSphere_Trios.png",
    "CONFIDENTIALITY_STATEMENT": """HMD Labs Confidential – This document contains information that is confidential and proprietary. Neither this
document nor the information herein may be reproduced, used, or disclosed to or for the benefit of any third
party without the prior written consent of HMD Labs.""",
    "output_files": ["html/index.html", "html/readme.html"],
    "logo_file": "NeuronSphere_Trios.png",
}
