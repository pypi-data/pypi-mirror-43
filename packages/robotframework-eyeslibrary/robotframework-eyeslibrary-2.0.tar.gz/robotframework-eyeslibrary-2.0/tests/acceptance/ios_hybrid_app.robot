*** Settings ***
Library        AppiumLibrary
Library        EyesLibrary
Resource       resources/common.robot
Resource       resources/mobile.robot
Resource       resources/ios.robot

*** Variables ***
&{TEST DIV}    xpath=//div[@class="app"]

*** Test Cases ***
Check Window
    [Setup]                          Setup                                                                             iOS Hybrid - Check Window
    Check Eyes Window                Main Screen
    [Teardown]                       Teardown

Check Region
    [Setup]                          Setup                                                                             iOS Hybrid - Check Region
    ${location}=                     Get Element Location                                                              xpath=${TEST DIV.xpath}
    Check Eyes Region                ${location['x']}                                                                  ${location['y']}                         200      200    Image Region
    [Teardown]                       Teardown

Check Region By Element
    [Setup]                          Setup                                                                             iOS Hybrid - Check Region By Element
    ${element}=                      Get Webelement                                                                    xpath=${TEST DIV.xpath}
    Check Eyes Region By Element     ${element}                                                                        Image
    [Teardown]                       Teardown

Check Region By Selector
    [Setup]                          Setup                                                                             iOS Hybrid - Check Region By Selector
    Check Eyes Region By Selector    ${TEST DIV.xpath}                                                                 Image                                    xpath
    [Teardown]                       Teardown

Is Session Open
    [Setup]                          Setup                                                                             iOS Hybrid - Opened Session
    ${is open}=                      Eyes Session Is Open
    Should Be True                   ${is open}
    [Teardown]                       Teardown

*** Keywords ***
Setup
    [Arguments]                      ${test name}
    Open Application                 remote_url=${REMOTE URL}
    ...                              platformName=${PLATFORM NAME}
    ...                              platformVersion=${PLATFORM VERSION}
    ...                              deviceName=${DEVICE NAME}
    ...                              app=/Users/sfnunes/Documents/GitHub/EyesLibrary/tests/resources/HelloWorld.zip
    ...                              automationName=XCUITest
    @{CONTEXTS}=                     Get Contexts
    Switch To Context                @{CONTEXTS}[1]
    Open Eyes Session                ${API KEY}
    ...                              EyesLibrary
    ...                              ${test name}
    ...                              AppiumLibrary
    ...                              enable_eyes_log=true

Teardown
    Close Application
    Close Eyes Session

Wait And Click Element
    [Arguments]                      ${locator}
    Wait Until Element Is Visible    ${locator}
    Click Element                    ${locator}