*** Settings ***
Library                AppiumLibrary
Library                EyesLibrary
Resource               resources/common.robot
Resource               resources/mobile.robot
Resource               resources/android.robot

*** Variables ***
&{NEXT PAGE BUTTON}    xpath=//android.widget.ImageView[@content-desc="next page"]

*** Test Cases ***
Check Window
    [Setup]               Setup                            Android App - Check Window
    Check Eyes Window     Google Calendar
    [Teardown]            Teardown

Check Region
    [Setup]               Setup                            Android App - Check Region
    ${location}=          Get Element Location             xpath=${NEXT PAGE BUTTON.xpath}
    Check Eyes Region     ${location['x']}                 ${location['y']}                         150             150              Next Page Button
    [Teardown]            Teardown

Is Session Open
    [Setup]               Setup                            Android App - Opened Session
    ${is open}=           Eyes Session Is Open
    Should Be True        ${is open}
    [Teardown]            Teardown

*** Keywords ***
Setup
    [Arguments]           ${test name}
    Set Test Variable     ${APP PACKAGE}                   com.google.android.calendar
    Set Test Variable     ${APP ACTIVITY}                  com.android.calendar.AllInOneActivity
    Open Application      remote_url=${REMOTE URL}
    ...                   appPackage=${APP PACKAGE}
    ...                   appActivity=${APP ACTIVITY}
    ...                   nativeWebScreenshot=true
    ...                   deviceName=${DEVICE NAME}
    ...                   platformName=${PLATFORM NAME}
    ...                   automationName=UiAutomator2
    Open Eyes Session     ${API KEY}                       EyesLibrary                              ${test name}    AppiumLibrary    enable_eyes_log=true

Teardown
    Close Application
    Close Eyes Session
