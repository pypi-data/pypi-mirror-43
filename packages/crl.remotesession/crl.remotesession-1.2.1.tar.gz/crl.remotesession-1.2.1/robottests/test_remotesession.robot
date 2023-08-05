# Copyright (C) 2019, Nokia

*** Settings ***

Library    crl.remotesession.remotesession.RemoteSession
...        WITH NAME    RemoteSession

Library    filehelper.py

Suite Setup    Create Random File
Suite Teardown    RemoteSession.Close
Test Setup    Set Targets
Force Tags     remotecompare

*** Variables ***

&{HOST1}=    host=10.102.227.10
...          user=root
...          password=root

&{HOST2}=    host=10.20.105.90
...          user=root

...          password=root


@{SHELLDICTS1}=    ${HOST1}
@{SHELLDICTS2}=    ${HOST2}

${TESTFILESIZE}=    1000000

*** Keywords ***
Create Random File
    filehelper.Create Random File    targetlocal    ${TESTFILESIZE}

Set Targets
    Set RemoteScript Targets
    Set RemoteRunner Targets

Set RemoteRunner Targets
    RemoteSession.Set Runner Target    shelldicts=${SHELLDICTS1}
    ...                                name=runner1

    RemoteSession.Set Runner Target    shelldicts=${SHELLDICTS2}
    ...                                name=runner2

Set RemoteScript Targets
    RemoteSession.Set Target    host=${HOST1.host}
    ...                         username=${HOST1.user}
    ...                         password=${HOST1.password}
    ...                         name=script1

    RemoteSession.Set Target     host=${HOST2.host}
    ...                         username=${HOST2.user}
    ...                         password=${HOST2.password}
    ...                         name=script2



*** Keywords ***

Compare Results
	[Arguments]    ${result1}    ${result2}
	Should Be True
        ...    '${result1.status}' == '${result2.status}' or '${result2.status}' == 'unknown'
        Should Be Equal    ${result1.stdout}    ${result2.stdout}
        Should Be Equal    ${result1.stderr}    ${result2.stderr}


*** Test Cases ***

Compare File Copying
    ${runner1}=    RemoteSession.Copy File To Target
    ...    targetlocal
    ...    .
    ...    0755
    ...    runner1
    ${runner2}=    RemoteSession.Copy File Between Targets
    ...     runner1
    ...     targetlocal
    ...     runner2
    ...     .
    ...     0755

    ${runner3}=    RemoteSession.Copy File From Target
    ...    targetlocal
    ...    remoterunnerfile
    ...    target=runner2
    filehelper.diff files    targetlocal    remoterunnerfile

    ${script1}=    RemoteSession.Copy File To Target
    ...    targetlocal
    ...    .
    ...    0755
    ...    script1

    ${script2}=    RemoteSession.Copy File Between Targets
    ...     script1
    ...     targetlocal
    ...     script2
    ...     .
    ...     0755

    ${script3}=    RemoteSession.Copy File From Target
    ...    targetlocal
    ...    remotescriptfile
    ...    target=script2

    ${mixed11}=    RemoteSession.Copy File To Target
    ...    targetlocal
    ...    .
    ...    0755
    ...    script1

    ${mixed12}=    RemoteSession.Copy File Between Targets
    ...     script1
    ...     targetlocal
    ...     runner2
    ...     .
    ...     0755

    ${mixed13}=    RemoteSession.Copy File From Target
    ...    targetlocal
    ...    mixedfile1
    ...    target=script2


    filehelper.diff files    targetlocal    mixedfile1

    ${mixed21}=    RemoteSession.Copy File To Target
    ...    targetlocal
    ...    .
    ...    0755
    ...    runner1

    ${mixed22}=    RemoteSession.Copy File Between Targets
    ...     runner1
    ...     targetlocal
    ...     script2
    ...     .
    ...     0755

    ${mixed33}=    RemoteSession.Copy File From Target
    ...    targetlocal
    ...    mixedfile2
    ...    target=script2

    filehelper.diff files    targetlocal    mixedfile2

    Compare Results    ${runner1}    ${script1}
    Compare Results    ${runner2}    ${script2}
    Compare Results    ${runner3}    ${script3}
    Compare Results    ${runner1}    ${mixed11}
    Compare Results    ${runner2}    ${mixed12}
    Compare Results    ${runner3}    ${mixed13}


Compare Execute Command In Target
    ${runner}=    RemoteSession.Execute Command In Target    echo out;>&2 echo err
    ...    runner1    1
    ${script}=    RemoteSession.Execute Command In Target    echo out;>&2 echo err
    ...    script1    1
    Compare Results    ${runner}    ${script}


Compare Copy Directory To Target
    ${runner}=     RemoteSession.Copy Directory To Target
    ...    tests/
    ...    /tmp/runner/
    ...    0744
    ...    runner1
    ${script}=     RemoteSession.Copy Directory To Target
    ...    tests/
    ...    /tmp/script/
    ...    0744
    ...    script1
    ${diff}=    RemoteSession.Execute Command In Target
    ...    diff -r /tmp/runner/ /tmp/script/    runner1
    Should Be Equal    ${diff.status}    0
    Compare Results    ${runner}    ${script}


Compare Create Directory In Target
    ${runner}=    RemoteSession.Create Directory In Target
    ...    /tmp/runnercreate/
    ...    0444
    ...   runner1

    ${script}=    RemoteSession.Create Directory In Target
    ...    /tmp/scriptcreate
    ...    0444
    ...   script1
    ${diff}=    RemoteSession.Execute Command In Target
    ...    diff -r /tmp/runnercreate/ /tmp/scriptcreate/    runner1
    Should Be Equal    ${diff.status}    0
    Compare Results    ${runner}    ${script}


Compare Execute Background Command In Target
    :FOR    ${i}    IN RANGE    2
    \    RemoteSession.Execute Background Command In Target
    	 ...    echo out;>&2 echo err;sleep 10
    	 ...    runner1
    	 ...    test
    \    Sleep    1
    \	 RemoteSession.Kill Background Execution    test
    \	 ${runner}=    RemoteSession.Wait Background Execution    test

    # No comparison with the RemoteScript can be done because there is a bugs
    # in the RemotScript background execution functionality Using instead
    # comparison with results which RemoteScript should ideally return

    Should Be Equal    ${runner.status}    -15
    Should Be Equal    ${runner.stdout}    out
    Should Be Equal    ${runner.stderr}    err
