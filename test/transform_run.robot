*** Settings ***
Documentation     Test template for running transform container with multiple inputs
Force Tags        Transform run
Library           Process
Library           OperatingSystem
Library           resources.PdfChecks.PdfChecks
Library           resources.OfficeChecks.OfficeChecks
Variables         tx_vars.py

*** Test Cases ***
Test Bartleby Transform
    [Documentation]    Run transform template suite
    [Tags]    REQ_BUILD_001    REQ_BUILD_002    REQ_BUILD_003
    [Template]    Test transform
    ${set_one}
    ${set_two}

Confidentiality Statement Exists In PDF
    [Tags]    confidentiality    dynamic_env    REQ_BRAND_001
    Test transform    ${confidential_pdf_one}
    Should Contain Confidentiality Statement    ${confidential_pdf_one}[TRANSFORM_OUTPUT]/${confidential_pdf_one}[output_files][0]    ${confidential_pdf_one}[CONFIDENTIALITY_STATEMENT]

Confidentiality Statement Is Dynamic
    [Tags]    confidentiality    dynamic_env    REQ_BRAND_002
    Test transform    ${confidential_pdf_two}
    Should Contain Confidentiality Statement    ${confidential_pdf_two}[TRANSFORM_OUTPUT]/${confidential_pdf_two}[output_files][0]    ${confidential_pdf_two}[CONFIDENTIALITY_STATEMENT]

Default NeuronSphere Cover Image Is Used
    [Tags]    logos    dynamic_env    REQ_BRAND_003
    Test Transform    ${default_cover_image}
    Should Contain Correct Cover Image    ${default_cover_image}[TRANSFORM_OUTPUT]/${default_cover_image}[output_files][1]    ${default_cover_image}[logo_file]

Default NeuronSphere Cover Image Is Dynamic
    [Tags]    logos    dynamic_env    REQ_BRAND_003
    Test Transform    ${default_pdf_cover_image}
    Should Contain Correct Cover Image    ${default_pdf_cover_image}[TRANSFORM_OUTPUT]/${default_pdf_cover_image}[output_files][1]    ${default_pdf_cover_image}[logo_file]

Default NeuronSphere HTML Logo Is Used
    [Tags]    logos    dynamic_env    REQ_BRAND_004
    Test Transform    ${html_logo_default}
    Should Contain Correct Cover Image    ${html_logo_default}[TRANSFORM_OUTPUT]/${html_logo_default}[output_files][0]    ${html_logo_default}[logo_file]

Default NeuronSphere HTML Logo Is Dynamic
    [Tags]    logos    dynamic_env    REQ_BRAND_004
    Test Transform    ${html_logo_dynamic}
    Should Contain Correct Cover Image    ${html_logo_dynamic}[TRANSFORM_OUTPUT]/${html_logo_dynamic}[output_files][0]    ${html_logo_dynamic}[logo_file]

Root Document Is Dynamic
    [Tags]    dynamic_env    root_doc    REQ_SEL_001
    Test transform    ${root_doc_change}
    Should Contain Correct Title    ${root_doc_change}[TRANSFORM_OUTPUT]/${root_doc_change}[output_files][0]    Test Docs

Copyright Notice Is The Callers To Set
    [Tags]    branding    dynamic_env    REQ_BRAND_006
    Test transform    ${copyright_override}
    ${page}=    Get File    ${copyright_override}[TRANSFORM_OUTPUT]/${copyright_override}[output_files][0]
    Should Contain    ${page}    ${copyright_override}[HMD_DOC_COPYRIGHT]

Word Document Is Produced
    [Tags]    pandoc    docx    REQ_CONV_001    REQ_CONV_003
    Test transform    ${docx_output}
    Docx Should Contain    ${docx_output}[TRANSFORM_OUTPUT]/${docx_output}[output_files][0]    Bartleby Transform Test

Converted Output Leaves The Theme Behind
    [Tags]    pandoc    docx    REQ_CONV_004    REQ_CONV_004_SPEC001
    Test transform    ${docx_output}
    ${file}=    Set Variable    ${docx_output}[TRANSFORM_OUTPUT]/${docx_output}[output_files][0]
    # The permalink glyph Sphinx puts on every heading, and the sidebar's own
    # headings — pandoc converts a whole page, so both arrive unless stripped.
    Docx Should Not Contain    ${file}    ¶
    Docx Should Not Contain    ${file}    Quick search
    Docx Should Not Contain    ${file}    Navigation

Slide Deck Is Produced One Slide Per Section
    [Tags]    pandoc    pptx    REQ_CONV_002    REQ_CONV_003    REQ_CONV_004_SPEC001
    Test transform    ${pptx_output}
    ${file}=    Set Variable    ${pptx_output}[TRANSFORM_OUTPUT]/${pptx_output}[output_files][0]
    ${slides}=    Count Slides    ${file}
    # Sphinx wraps sections in <section>, which pandoc reads as a Div; a heading
    # inside a Div starts no slide, so the whole deck collapses to one page.
    Should Be True    ${slides} > 1    The deck has ${slides} slide(s); the sections did not split
    Slides Should Contain    ${file}    Indices and tables

*** Keywords ***
Test transform
    [Documentation]    Run transform and verify process completes successfully
    [Arguments]    ${env}
    Setup Transform Test    ${env}
    Do transform
    Check output files    ${env}
    Reset Environment Variables

Setup Transform Test
    [Documentation]    Transform Test Setup
    [Arguments]    ${env}
    Create Directory    ${env}[TRANSFORM_OUTPUT]
    Empty Directory    ${env}[TRANSFORM_OUTPUT]
    Load Environment Variables    ${env}

Load Environment Variables
    [Documentation]    Loads needed environment variables
    [Arguments]    ${env}
    Set Environment Variable    VERSION    ${version}
    Set Environment Variable    TRANSFORM_INSTANCE_CONTEXT    ${env}[TRANSFORM_INSTANCE_CONTEXT]
    Set Environment Variable    TRANSFORM_NID    ${env}[TRANSFORM_NID]
    Set Environment Variable    TRANSFORM_INPUT    ${env}[TRANSFORM_INPUT]
    Set Environment Variable    TRANSFORM_OUTPUT    ${env}[TRANSFORM_OUTPUT]
    Set Environment Variable    CONFIDENTIALITY_STATEMENT    ${env}[CONFIDENTIALITY_STATEMENT]
    Set Environment Variable    DEFAULT_LOGO    ${env}[DEFAULT_LOGO]
    Set Environment Variable    HMD_DOC_COPYRIGHT    ${env.get("HMD_DOC_COPYRIGHT", "")}

Do transform
    [Documentation]    Run transform container with expected volume mounts and env variables
    Run Process    docker-compose    up    stdout=run-transform.log    stderr=STDOUT    alias=runtransform
    ${result}=    Get Process Result    runtransform
    Log    ${result.stdout}
    Should be equal    ${result.rc}    ${0}
    Run Process    docker-compose    down

Check output files
    [Documentation]    Verify output file count matches input file count
    [Arguments]    ${env}
    FOR    ${file}    IN    @{env}[output_files]
        File Should Exist    ${env}[TRANSFORM_OUTPUT]/${file}
    END

Reset Environment Variables
    Remove Environment Variable    TRANSFORM_INSTANCE_CONTEXT    TRANSFORM_NID    TRANSFORM_INPUT    TRANSFORM_OUTPUT    VERSION    CONFIDENTIALITY_STATEMENT    DEFAULT_LOGO    HMD_DOC_COPYRIGHT
