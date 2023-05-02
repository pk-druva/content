import pytest
import json


def test_test_module(requests_mock):
    from Druva import Client, test_module
    requests_mock.get("https://apis.druva.com/realize/ransomwarerecovery/v1/quarantineranges", json=[], status_code=200)
    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )
    assert test_module(client) == 'ok'


def test_test_module_Command_Invalid_input(requests_mock):
    from Druva import Client, test_module
    requests_mock.get("https://apis.druva.com/realize/ransomwarerecovery/v1/quarantineranges", status_code=100)
    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )
    with pytest.raises(RuntimeError) as ve:
        test_module(client)
    assert str(ve.value) == 'Internal Error'


def test_Execute_command(mocker, requests_mock):
    from Druva import Client, Execute_command
    import demistomock as demisto
    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )

    with open("test_data/test-data.json") as file:
        data = json.load(file)
        commands = ["test-module", "druva-list-quarantine-ranges", "druva-find-device",
                    "druva-find-user", "druva-find-userDevice", "druva-find-sharePointSites",
                    "druva-find-sharedDrives", "druva-quarantine-resource",
                    "druva-delete-quarantine-range", "druva-view-quarantine-range",
                    "druva-update-quarantine-range", "druva-list-quarantine-snapshots",
                    "druva-delete-quarantined-snapshot",
                    "druva-endpoint-check-restore-status",
                    "druva-endpoint-search-file-hash"]
        mocker.patch.object(demisto, 'results')
        for cur_command in commands:
            req_type = data[cur_command]["request-type"]
            if cur_command == "druva-quarantine-resource":
                mock_response_post = data[cur_command]["mock-responce"]
                mock_response_get = data["druva-list-quarantine-ranges"]["mock-responce"]
                requests_mock.post(data[cur_command]["url-suffix"], status_code=200, json=mock_response_post)
                requests_mock.get(data["druva-list-quarantine-ranges"]["url-suffix"], status_code=200, json=mock_response_get)
                Execute_command(cur_command, client)
                outputs = demisto.results.call_args[0][0]['Contents']
                assert outputs == mock_response_get
            elif cur_command == "druva-update-quarantine-range":
                mock_response_post = data[cur_command]["mock-responce"]
                mock_response_get = data["druva-list-quarantine-ranges"]["mock-responce"]
                requests_mock.put(data[cur_command]["url-suffix"], status_code=200, json=mock_response_post)
                requests_mock.get(data["druva-list-quarantine-ranges"]["url-suffix"], status_code=200, json=mock_response_get)
                Execute_command(cur_command, client)
                outputs = demisto.results.call_args[0][0]['Contents']
                assert outputs == mock_response_get
            elif req_type == "get":
                mock_response = data[cur_command]["mock-responce"]
                requests_mock.get(data[cur_command]["url-suffix"], status_code=200, json=mock_response)
                Execute_command(cur_command, client)
                if cur_command != "test-module":
                    outputs = demisto.results.call_args[0][0]['Contents']
                    assert outputs == mock_response
            elif req_type == "delete":
                mock_response = data[cur_command]["mock-responce"]
                requests_mock.delete(data[cur_command]["url-suffix"], status_code=200, json=mock_response)
                Execute_command(cur_command, client)
                outputs = demisto.results.call_args[0][0]['Contents']
                assert outputs == mock_response
            elif req_type == "post":
                mock_response = data[cur_command]["mock-responce"]
                requests_mock.delete(data[cur_command]["url-suffix"], status_code=200, json=mock_response)
                Execute_command(cur_command, client)
                outputs = demisto.results.call_args[0][0]['Contents']
                assert outputs == mock_response_get


def test_Druva_FindDevice_Command(requests_mock):
    from Druva import Client, Druva_FindDevice_Command
    mock_response = {'resources': [{
        'orgID': '-1',
        'resourceID': '12345',
        'resourceName': 'test',
        'resourceParent': 'testUser',
        'resourceStatus': 'enabled',
        'resourceType': 'VMware'
    }]}
    requests_mock.get('https://apis.druva.com/realize/ransomwarerecovery/v1/search/backupset?hostname=test',
                      json=mock_response)
    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )
    search_string = 'test'
    response = Druva_FindDevice_Command(client, search_string)
    assert response.outputs["Druva.Resource(val.resourceID == obj.resourceID)"] == [{
        'orgID': '-1',
        'resourceID': '12345',
        'resourceName': 'test',
        'resourceParent': 'testUser',
        'resourceStatus': 'enabled',
        'resourceType': 'VMware'
    }, {
        'orgID': '-1',
        'resourceID': '12345',
        'resourceName': 'test',
        'resourceParent': 'testUser',
        'resourceStatus': 'enabled',
        'resourceType': 'VMware'
    }]


def test_Druva_FindDevice_Command_Invalid_input(requests_mock):
    from Druva import Client, Druva_FindDevice_Command
    requests_mock.get('https://apis.druva.com/realize/ransomwarerecovery/v1/search/backupset?hostname=test', status_code=100)
    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )
    with pytest.raises(RuntimeError) as ve:
        Druva_FindDevice_Command(client, "test")
    assert str(ve.value) == 'Internal Error'


def test_Druva_FindUser_Command(requests_mock):
    from Druva import Client, Druva_FindUser_Command
    mock_response = {"users": [{
        "userID": "100",
        "userName": "test",
        "emailID": "test@test.com"
    }]}
    requests_mock.get('https://apis.druva.com/realize/ransomwarerecovery/v1/users?users=test',
                      json=mock_response)
    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )
    search_string = 'test'
    response = Druva_FindUser_Command(client, search_string)
    assert response.outputs["Druva.User(val.userID == obj.userID)"] == [{
        "userID": "100",
        "userName": "test",
        "emailID": "test@test.com"
    }]


def test_Druva_FindUser_Command_invalid_input(requests_mock):
    from Druva import Client, Druva_FindUser_Command

    requests_mock.get('https://apis.druva.com/realize/ransomwarerecovery/v1/users?users=test', status_code=100)
    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )
    search_string = 'test'
    with pytest.raises(RuntimeError) as ve:
        Druva_FindUser_Command(client, search_string)
    assert str(ve.value) == 'Internal Error'


def test_Druva_FindUserDevice_Command(requests_mock):
    from Druva import Client, Druva_FindUserDevice_Command
    mock_response = {"resources": [{
        "resourceID": "100",
        "resourceName": "test",
        "resourceType": "OneDrive",
        "resourceStatus": "Enabled",
        "userID": "100",
        "userName": "test",
        "profileID": "100"
    }]}
    requests_mock.get('https://apis.druva.com/realize/ransomwarerecovery/v1/search/device',
                      json=mock_response)
    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )
    search_string = '100'
    response = Druva_FindUserDevice_Command(client, search_string)
    assert response.outputs["Druva.Resource(val.resourceID == obj.resourceID)"] == [{
        "resourceID": "100",
        "resourceName": "test",
        "resourceType": "OneDrive",
        "resourceStatus": "Enabled",
        "userID": "100",
        "userName": "test",
        "profileID": "100"
    }]


def test_Druva_FindUserDevice_Command_invalid_Status_code(requests_mock):
    from Druva import Client, Druva_FindUserDevice_Command

    requests_mock.get('https://apis.druva.com/realize/ransomwarerecovery/v1/search/device',
                      status_code=100)
    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )
    search_string = 'test'
    with pytest.raises(RuntimeError) as ve:
        Druva_FindUserDevice_Command(client, search_string)
    assert str(ve.value) == 'Internal Error'


def test_Druva_FindSharePointSites_Command(requests_mock):
    from Druva import Client, Druva_FindSharePointSites_Command
    mock_response = {"siteCollections": [{
        "resourceID": "1",
        "resourceName": "test",
        "resourceType": "SharePoint",
        "resourceStatus": "Disabled",
        "resourceParentName": "https://druvainternal.sharepoint.com/sites/msteams_88b98c_693649-private123__0_",
        "siteType": "M365 Groups Site"
    }]}
    requests_mock.get(
        'https://apis.druva.com/realize/ransomwarerecovery/v1/search/sharepoint-sites?siteTitlePrefix=test',
        json=mock_response)
    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )
    search_string = 'test'
    response = Druva_FindSharePointSites_Command(client, search_string)
    assert response.outputs["Druva.Resource(val.resourceID == obj.resourceID)"] == [{
        "resourceID": "1",
        "resourceName": "test",
        "resourceType": "SharePoint",
        "resourceStatus": "Disabled",
        "resourceParentName": "https://druvainternal.sharepoint.com/sites/msteams_88b98c_693649-private123__0_",
        "siteType": "M365 Groups Site"
    }]


def test_Druva_FindSharePointSites_Command_invalid_Status_code(requests_mock):
    from Druva import Client, Druva_FindSharePointSites_Command

    requests_mock.get(
        'https://apis.druva.com/realize/ransomwarerecovery/v1/search/sharepoint-sites?siteTitlePrefix=test',
        status_code=100)
    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )
    search_string = 'test'
    with pytest.raises(RuntimeError) as ve:
        Druva_FindSharePointSites_Command(client, search_string)
    assert str(ve.value) == 'Internal Error'


def test_Druva_FindSharedDrives_Command(requests_mock):
    from Druva import Client, Druva_FindSharedDrives_Command
    mock_response = {'accountList': [{
        'resourceID': '1',
        'resourceName': 'test',
        'resourceType': 'Shared Drive',
        'resourceStatus': 'Enabled',
        'resourceParentName': 'https://drive.google.com/drive/folders/0ADBm3g-NG_F4Uk9PVA'
    }]}
    requests_mock.get(
        'https://apis.druva.com/realize/ransomwarerecovery/v1/search/shareddrive-accounts?accountTitlePrefix=test',
        json=mock_response)
    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )
    search_string = 'test'
    response = Druva_FindSharedDrives_Command(client, search_string)
    assert response.outputs["Druva.Resource(val.resourceID == obj.resourceID)"] == [{
        'resourceID': '1',
        'resourceName': 'test',
        'resourceType': 'Shared Drive',
        'resourceStatus': 'Enabled',
        'resourceParentName': 'https://drive.google.com/drive/folders/0ADBm3g-NG_F4Uk9PVA'
    }]


def test_Druva_FindSharedDrives_Command_invalid_Status_code(requests_mock):
    from Druva import Client, Druva_FindSharedDrives_Command

    requests_mock.get(
        'https://apis.druva.com/realize/ransomwarerecovery/v1/search/shareddrive-accounts?accountTitlePrefix=test',
        status_code=100)
    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )
    search_string = 'test'
    with pytest.raises(RuntimeError) as ve:
        Druva_FindSharedDrives_Command(client, search_string)
    assert str(ve.value) == 'Internal Error'


def test_Druva_ListQuarantineRanges_Command(requests_mock):
    from Druva import Client, Druva_ListQuarantineRanges_Command
    mock_response = {'quarantineRanges': [{
        'rangeID': '100',
        'resourceID': '12345',
        'resourceType': 'Endpoint',
        'startDate': '2020-12-01',
        'endDate': '2020-12-10'
    }]}

    requests_mock.get('https://apis.druva.com/realize/ransomwarerecovery/v1/quarantineranges', json=mock_response)
    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )

    response = Druva_ListQuarantineRanges_Command(client)
    assert response.outputs["Druva.activeQuarantineRanges(val.rangeID == obj.rangeID)"] == [{
        'rangeID': '100',
        'resourceID': '12345',
        'resourceType': 'Endpoint',
        'startDate': '2020-12-01',
        'endDate': '2020-12-10'
    }]


def test_Druva_ListQuarantineRanges_Command_invalid_Status_code(requests_mock):
    from Druva import Client, Druva_ListQuarantineRanges_Command

    requests_mock.get('https://apis.druva.com/realize/ransomwarerecovery/v1/quarantineranges',
                      status_code=100)
    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )

    with pytest.raises(RuntimeError) as ve:
        Druva_ListQuarantineRanges_Command(client)
    assert str(ve.value) == 'Internal Error'


def test_Druva_QuarantineResource_Command(requests_mock):
    from Druva import Client, Druva_QuarantineResource_Command
    mock_response = {
        'rangeID': '100'
    }
    requests_mock.post('https://apis.druva.com/realize/ransomwarerecovery/v1/quarantineranges/resource/12345',
                       json=mock_response)

    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )
    org_id = '-1'
    resource_id = '12345'
    resource_type = 'endpoint'
    from_date = '2020-12-01'
    to_date = '2020-12-10'

    response = Druva_QuarantineResource_Command(client, org_id, resource_id, resource_type, from_date, to_date)
    assert response.outputs["Druva.QuarantinedRangeID"] == '100'


def test_Druva_QuarantineResource_Command_invalid_Status_code(requests_mock):
    from Druva import Client, Druva_QuarantineResource_Command

    requests_mock.post('https://apis.druva.com/realize/ransomwarerecovery/v1/quarantineranges/resource/12345',
                       status_code=100)
    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )
    org_id = '-1'
    resource_id = '12345'
    resource_type = 'endpoint'
    from_date = '2020-12-01'
    to_date = '2020-12-10'

    with pytest.raises(RuntimeError) as ve:
        Druva_QuarantineResource_Command(client, org_id, resource_id, resource_type, from_date, to_date)
    assert str(ve.value) == 'Internal Error'


def test_Druva_DeleteQuarantineRange_Command(requests_mock):
    from Druva import Client, Druva_DeleteQuarantineRange_Command
    mock_response = {
        'rangeID': '100'
    }
    requests_mock.delete(
        'https://apis.druva.com/realize/ransomwarerecovery/v1/quarantineranges/resource/12345/range/100',
        json=mock_response)
    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )
    resource_id = '12345'
    range_id = '100'

    response = Druva_DeleteQuarantineRange_Command(client, resource_id, range_id)
    assert response.raw_response["rangeID"] == '100'


def test_Druva_DeleteQuarantineRange_Command_invalid_Status_code(requests_mock):
    from Druva import Client, Druva_DeleteQuarantineRange_Command

    requests_mock.delete(
        'https://apis.druva.com/realize/ransomwarerecovery/v1/quarantineranges/resource/12345/range/100',
        status_code=100)

    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )
    resource_id = '12345'
    range_id = '100'

    with pytest.raises(RuntimeError) as ve:
        Druva_DeleteQuarantineRange_Command(client, resource_id, range_id)
    assert str(ve.value) == 'Internal Error'


def test_Druva_ViewQurantineRange_Command(requests_mock):
    from Druva import Client, Druva_ViewQurantineRange_Command
    mock_response = {
        'rangeID': '100'
    }
    requests_mock.get('https://apis.druva.com/realize/ransomwarerecovery/v1/quarantineranges/resource/12345/range/100',
                      json=mock_response)
    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )
    resource_id = '12345'
    range_id = '100'

    response = Druva_ViewQurantineRange_Command(client, resource_id, range_id)
    assert response.outputs["Druva.viewedQuarantineRange(val.rangeID == obj.rangeID)"] == {
        'rangeID': '100'
    }


def test_Druva_ViewQurantineRange_Command_invalid_Status_code(requests_mock):
    from Druva import Client, Druva_ViewQurantineRange_Command

    requests_mock.get('https://apis.druva.com/realize/ransomwarerecovery/v1/quarantineranges/resource/12345/range/100',
                      status_code=100)

    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )
    resource_id = '12345'
    range_id = '100'

    with pytest.raises(RuntimeError) as ve:
        Druva_ViewQurantineRange_Command(client, resource_id, range_id)
    assert str(ve.value) == 'Internal Error'


def test_Druva_UpdateQuarantineRange_Command(requests_mock):
    from Druva import Client, Druva_UpdateQuarantineRange_Command
    mock_response = {
        'rangeID': '100'
    }
    requests_mock.put(
        'https://apis.druva.com/realize/ransomwarerecovery/v1/quarantineranges/resource/12345/range/100',
        json=mock_response)
    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )
    resource_id = '12345'
    resource_type = 'endpoint'
    range_id = '100'
    from_date = '2020-12-05'
    to_date = '2020-12-10'

    response = Druva_UpdateQuarantineRange_Command(client, resource_id, resource_type, range_id, from_date, to_date)
    assert response.outputs["Druva.updatedQuarantineRange"] == '100'


def test_Druva_UpdateQuarantineRange_Command_invalid_Status_code(requests_mock):
    from Druva import Client, Druva_UpdateQuarantineRange_Command

    requests_mock.put(
        'https://apis.druva.com/realize/ransomwarerecovery/v1/quarantineranges/resource/12345/range/100',
        status_code=100)

    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )
    resource_id = '12345'
    resource_type = 'endpoint'
    range_id = '100'
    from_date = '2020-12-05'
    to_date = '2020-12-10'

    with pytest.raises(RuntimeError) as ve:
        Druva_UpdateQuarantineRange_Command(client, resource_id, resource_type, range_id, from_date, to_date)
    assert str(ve.value) == 'Internal Error'


def test_Druva_ListQuarantine_Snapshots_Command(requests_mock):
    from Druva import Client, Druva_ListQuarantine_Snapshots_Command
    mock_response = {'snapshots': [{
        'name': 'May 4 2020, 15:02',
        'snapshotID': 'TW9uIE1heSAgNCAxNTowMjo0MSAyMDIw',
        'snapshotSize': 'Endpoint',
        'status': 'Quarantined'
    }]}

    requests_mock.get('https://apis.druva.com/realize/ransomwarerecovery/v1/snapshots/resource/28604/range/233',
                      json=mock_response)
    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )
    resource_id = '28604'
    range_id = '233'
    response = Druva_ListQuarantine_Snapshots_Command(client, resource_id, range_id)
    assert response.outputs["Druva.quarantinedSnapshots(val.snapshotID == obj.snapshotID)"] == [{
        'name': 'May 4 2020, 15:02',
        'snapshotID': 'TW9uIE1heSAgNCAxNTowMjo0MSAyMDIw',
        'snapshotSize': 'Endpoint',
        'status': 'Quarantined'
    }]


def test_Druva_ListQuarantine_Snapshots_Command_invalid_Status_code(requests_mock):
    from Druva import Client, Druva_ListQuarantine_Snapshots_Command

    requests_mock.get('https://apis.druva.com/realize/ransomwarerecovery/v1/snapshots/resource/28604/range/233',
                      status_code=100)

    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )
    resource_id = '28604'
    range_id = '233'

    with pytest.raises(RuntimeError) as ve:
        Druva_ListQuarantine_Snapshots_Command(client, resource_id, range_id)
    assert str(ve.value) == 'Internal Error'


def test_Druva_DeleteQuarantined_Snapshots_Command(requests_mock):
    from Druva import Client, Druva_DeleteQuarantined_Snapshots_Command
    mock_response = {
        'snapshotID': 'TW9uIE1heSAgNCAxNTowMjo0MSAyMDIw'
    }
    requests_mock.delete(
        'https://apis.druva.com/realize/ransomwarerecovery/v1/'
        'snapshots/resource/28604/range/233/snapshot/TW9uIE1heSAgNCAxNTowMjo0MSAyMDIw',
        json=mock_response)
    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )
    resource_id = '28604'
    range_id = '233'
    snapshot_id = 'TW9uIE1heSAgNCAxNTowMjo0MSAyMDIw'
    response = Druva_DeleteQuarantined_Snapshots_Command(client, resource_id, range_id, snapshot_id)
    assert response.raw_response['snapshotID'] == 'TW9uIE1heSAgNCAxNTowMjo0MSAyMDIw'


def test_Druva_DeleteQuarantined_Snapshots_Command_invalid_Status_code(requests_mock):
    from Druva import Client, Druva_DeleteQuarantined_Snapshots_Command

    requests_mock.delete(
        'https://apis.druva.com/realize/ransomwarerecovery/v1/'
        'snapshots/resource/28604/range/233/snapshot/TW9uIE1heSAgNCAxNTowMjo0MSAyMDIw',
        status_code=100)

    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )
    resource_id = '28604'
    range_id = '233'
    snapshot_id = 'TW9uIE1heSAgNCAxNTowMjo0MSAyMDIw'
    with pytest.raises(RuntimeError) as ve:
        Druva_DeleteQuarantined_Snapshots_Command(client, resource_id, range_id, snapshot_id)
    assert str(ve.value) == 'Internal Error'


def test_Druva_SearchbyFileHash_Command(requests_mock):
    from Druva import Client, Druva_SearchbyFileHash_Command
    mock_response = {'results': [{
        'resourceID': '12345',
        'resourceParent': 'testUser',
        'resourceType': 'endpoint'
    }]}

    requests_mock.get(
        'https://apis.druva.com/realize/mds/v1/user/files?sha1Checksum=12345abcdef6789ghijkl101112mnop',
        json=mock_response)
    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )
    sha1_checksum = '12345abcdef6789ghijkl101112mnop'
    response = Druva_SearchbyFileHash_Command(client, sha1_checksum)
    assert response.outputs["Druva.searchEndpointsFileHashResults(val.objectID == obj.objectID)"] == [{
        'resourceID': '12345',
        'resourceParent': 'testUser',
        'resourceType': 'endpoint'
    }]


def test_Druva_SearchbyFileHash_Command_invalid_Status_code(requests_mock):
    from Druva import Client, Druva_SearchbyFileHash_Command

    requests_mock.get(
        'https://apis.druva.com/realize/mds/v1/user/files?sha1Checksum=12345abcdef6789ghijkl101112mnop',
        status_code=100)

    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )
    sha1_checksum = '12345abcdef6789ghijkl101112mnop'
    with pytest.raises(RuntimeError) as ve:
        Druva_SearchbyFileHash_Command(client, sha1_checksum)
    assert str(ve.value) == 'Internal Error'


def test_Druva_Restore_Endpoint(requests_mock):
    from Druva import Client, Druva_Restore_Endpoint
    mock_response = {'restores': [{
        'deviceID': '12345',
        'targetDeviceID': '12345',
        'restoreLocation': 'Desktop',
        'userID': '12345',
        'restoreID': '100'
    }]}
    requests_mock.post('https://apis.druva.com/insync/endpoints/v1/restores', json=mock_response)
    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )
    source_resourceid = '12345'
    target_resourceid = '12345'
    restore_location = 'Desktop'

    response = Druva_Restore_Endpoint(client, source_resourceid, target_resourceid, restore_location)
    assert response.outputs["Druva.restoreJobs(val.restoreID == obj.restoreID)"] == [{
        'deviceID': '12345',
        'targetDeviceID': '12345',
        'restoreLocation': 'Desktop',
        'userID': '12345',
        'restoreID': '100'
    }]


def test_Druva_Restore_Endpoint_invalid_Status_code(requests_mock):
    from Druva import Client, Druva_Restore_Endpoint

    requests_mock.post('https://apis.druva.com/insync/endpoints/v1/restores',
                       status_code=100)

    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )
    source_resourceid = '12345'
    target_resourceid = '12345'
    restore_location = 'Desktop'

    with pytest.raises(RuntimeError) as ve:
        Druva_Restore_Endpoint(client, source_resourceid, target_resourceid, restore_location)
    assert str(ve.value) == 'Internal Error'


def test_Druva_Restore_Status(requests_mock):
    from Druva import Client, Druva_Restore_Status
    mock_response = {
        'deviceID': '12345',
        'targetDeviceID': '12345',
        'restoreLocation': 'Desktop',
        'userID': '12345',
        'status': 'Successful'
    }

    requests_mock.get('https://apis.druva.com/insync/endpoints/v1/restores/100', json=mock_response)
    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )
    restore_id = '100'
    response = Druva_Restore_Status(client, restore_id)
    assert response.outputs["Druva.restoreJobs(val.restoreID == obj.restoreID)"] == {
        'deviceID': '12345',
        'targetDeviceID': '12345',
        'restoreLocation': 'Desktop',
        'userID': '12345',
        'status': 'Successful'
    }


def test_Druva_Restore_Status_invalid_Status_code(requests_mock):
    from Druva import Client, Druva_Restore_Status

    requests_mock.get('https://apis.druva.com/insync/endpoints/v1/restores/100',
                      status_code=100)

    client = Client(
        base_url='https://apis.druva.com/',
        verify=False,
        headers={
            'Authentication': 'Bearer some_api_key'
        }
    )
    restore_id = '100'
    with pytest.raises(RuntimeError) as ve:
        Druva_Restore_Status(client, restore_id)
    assert str(ve.value) == 'Internal Error'
