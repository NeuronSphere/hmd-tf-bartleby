*** Settings ***
Documentation     Test template for running transform container with multiple inputs
Force Tags        Transform run
Library           Process
Library           OperatingSystem
Library           resources.PdfChecks.PdfChecks
Variables         tx_vars.py

*** Test Cases ***
Test Bartleby Transform
    [Documentation]    Run transform template suite
    [Template]    Test transform
    ${set_one}
    ${set_two}

Confidentiality Statement Exists In PDF
    [Tags]    confidentiality    dynamic_env
    Test transform    ${confidential_pdf_one}
    Should Contain Confidentiality Statement    ${confidential_pdf_one}[TRANSFORM_OUTPUT]/${confidential_pdf_one}[output_files][0]    ${confidential_pdf_one}[CONFIDENTIALITY_STATEMENT]

Confidentiality Statement Is Dynamic
    [Tags]    confidentiality    dynamic_env
    Test transform    ${confidential_pdf_two}
    Should Contain Confidentiality Statement    ${confidential_pdf_two}[TRANSFORM_OUTPUT]/${confidential_pdf_two}[output_files][0]    ${confidential_pdf_two}[CONFIDENTIALITY_STATEMENT]

Default NeuronSphere Cover Image Is Used
    [Tags]    logos    dynamic_env
    Test Transform    ${default_cover_image}
    Should Contain Correct Cover Image    ${default_cover_image}[TRANSFORM_OUTPUT]/${default_cover_image}[output_files][1]    ${default_cover_image}[logo_file]

Default NeuronSphere Cover Image Is Dynamic
    [Tags]    logos    dynamic_env
    Test Transform    ${default_pdf_cover_image}
    Should Contain Correct Cover Image    ${default_pdf_cover_image}[TRANSFORM_OUTPUT]/${default_pdf_cover_image}[output_files][1]    ${default_pdf_cover_image}[logo_file]

Default NeuronSphere HTML Logo Is Used
    [Tags]    logos    dynamic_env
    Test Transform    ${html_logo_default}
    Should Contain Correct Cover Image    ${html_logo_default}[TRANSFORM_OUTPUT]/${html_logo_default}[output_files][0]    ${html_logo_default}[logo_file]

Default NeuronSphere HTML Logo Is Dynamic
    [Tags]    logos    dynamic_env
    Test Transform    ${html_logo_dynamic}
    Should Contain Correct Cover Image    ${html_logo_dynamic}[TRANSFORM_OUTPUT]/${html_logo_dynamic}[output_files][0]    ${html_logo_dynamic}[logo_file]

Root Document Is Dynamic
    [Tags]    dynamic_env    root_doc
    Test transform    ${root_doc_change}
    Should Contain Correct Title    ${root_doc_change}[TRANSFORM_OUTPUT]/${root_doc_change}[output_files][0]    Test Docs

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
    Remove Environment Variable    TRANSFORM_INSTANCE_CONTEXT    TRANSFORM_NID    TRANSFORM_INPUT    TRANSFORM_OUTPUT    VERSION    CONFIDENTIALITY_STATEMENT    DEFAULT_LOGO
