*** Settings ***
Documentation    Test template for building transform images
Force Tags    Transform build
Library    Process

*** Variables ***


*** Test Cases ***
Test transform image build
    Build transform image

*** Keywords ***
Build transform image
    [Documentation]    Build transform image and confirm process completes successfully
    Build image
    Check build process status

Build image
    Run Process    hmd    --repo-name    transform-test    --repo-version    test    docker    build    stdout=build.log    stderr=STDOUT    alias=buildimg

Check build process status
    ${result}=    Get Process Result    buildimg
    Log    ${result.stdout}
    Should be equal    ${result.rc}    ${0}