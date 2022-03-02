*** Settings ***
Documentation    Test template for running transform container with multiple inputs
Force Tags    Transform run
Library    Process
Library    OperatingSystem

Variables    tx_vars.py


*** Test Cases ***
Test transform engine
    [Documentation]     Run transform template suite
    [Template]    Test transform
    ${set_one}
    ${set_two}

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
    Empty Directory     ${env}[TRANSFORM_OUTPUT]
    Load Environment Variables    ${env}

Load Environment Variables
    [Documentation]    Loads needed environment variables
    [Arguments]    ${env}
    Set Environment Variable    TRANSFORM_INSTANCE_CONTEXT    ${env}[TRANSFORM_INSTANCE_CONTEXT]
    Set Environment Variable    TRANSFORM_NID    ${env}[TRANSFORM_NID]
    Set Environment Variable    TRANSFORM_INPUT    ${env}[TRANSFORM_INPUT]
    Set Environment Variable    TRANSFORM_OUTPUT    ${env}[TRANSFORM_OUTPUT]

Do transform
    [Documentation]    Run transform container with expected volume mounts and env variables
    Run Process    docker-compose    --file    ./test_suite/docker-compose.yaml    up    stdout=run-transform.log    stderr=STDOUT    alias=runtransform
    ${result}=    Get Process Result    runtransform
    Log    ${result.stdout}
    Should be equal    ${result.rc}    ${0}

Check output files
    [Documentation]    Verify output file count matches input file count
    [Arguments]    ${env}
    ${in}=    Count Items In Directory    ${env}[TRANSFORM_INPUT]
    ${out}=    Count Items In Directory    ${env}[TRANSFORM_OUTPUT]
    Should be equal    ${in}    ${out}

Reset Environment Variables
    Remove Environment Variable    TRANSFORM_INSTANCE_CONTEXT    TRANSFORM_NID    TRANSFORM_INPUT    TRANSFORM_OUTPUT
