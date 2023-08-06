*** Settings ***
Resource                 resources/common.robot
Resource                 resources/mobile.robot
Resource                 resources/android.robot
Library                  AppiumLibrary
Library                  EyesLibrary                                                ${API KEY}    EyesLibraryApp    TestNameToOverride    AppiumLibrary

*** Variables ***
&{SEARCH BAR}            xpath=//input[@class="topcoat-search-input search-key"]
&{SEARCH RESULT ITEM}    xpath=//li[@class="topcoat-list__item"][1]

*** Test Cases ***
Check Window
    [Setup]                          Setup                                  Android Hybrid - Check Window
    Check Eyes Window                Main Screen
    [Teardown]                       Teardown

Check Region
    [Setup]                          Setup                                  Android Hybrid - Check Region
    ${location}=                     Get Element Location                   xpath=${SEARCH RESULT ITEM.xpath}
    Check Eyes Region                ${location['x']}                       ${location['y']}                             200                     200    Image Region
    [Teardown]                       Teardown

Check Region By Element
    [Setup]                          Setup                                  Android Hybrid - Check Region By Element
    ${element}=                      Get Webelement                         xpath=${SEARCH RESULT ITEM.xpath}
    Check Eyes Region By Element     ${element}                             Image
    [Teardown]                       Teardown

Check Region By Selector
    [Setup]                          Setup                                  Android Hybrid - Check Region By Selector
    Check Eyes Region By Selector    ${SEARCH RESULT ITEM.xpath}            Image                                        xpath
    [Teardown]                       Teardown

Is Session Open
    [Setup]                          Setup                                  Android Hybrid - Opened Session
    ${is open}=                      Eyes Session Is Open
    Should Be True                   ${is open}
    [Teardown]                       Teardown

*** Keywords ***
Setup
    [Arguments]                      ${test name}
    Set Test Variable                ${APP PACKAGE}                         io.appium.gappium.sampleapp
    Set Test Variable                ${APP ACTIVITY}                        io.appium.gappium.sampleapp.HelloGappium
    Open Application                 remote_url=${REMOTE URL}
    ...                              appPackage=${APP PACKAGE}
    ...                              appActivity=${APP ACTIVITY}
    ...                              nativeWebScreenshot=true
    ...                              deviceName=${DEVICE NAME}
    ...                              platformName=${PLATFORM NAME}
    ...                              automationName=UiAutomator2
    Switch To Context                WEBVIEW_io.appium.gappium.sampleapp
    Set Location                     10                                     10
    Open Eyes Session                testname=${test name}                  library=AppiumLibrary                        enable_eyes_log=true
    # EyesLibrary
    #...                              ${test name}
    #...                              ${API KEY}
    #...                              AppiumLibrary
    #...                              enable_eyes_log=true
    Input Text                       xpath=${SEARCH BAR.xpath}              a

Teardown
    Close Application
    Close Eyes Session

Wait And Click Element
    [Arguments]                      ${locator}
    Wait Until Element Is Visible    ${locator}
    Click Element                    ${locator}