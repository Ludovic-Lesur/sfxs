from __future__ import print_function
import requests
import time

# HTTP server port.
SFXS_HTTP_ADDRESS = "http://localhost:65000"
HTTP_REQUEST_DELAY_SECONDS = 1

# Backend JSON headers.
COMMON_OOB_DATA = "OOB"
SFXS_BACKEND_JSON_HEADER_TIME = "time"
SFXS_BACKEND_JSON_HEADER_EP_ID = "device"
SFXS_BACKEND_JSON_HEADER_DATA = "data"

METEOFOX_TEST_REQUEST = [
    # MeteoFox old startup data.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374000", SFXS_BACKEND_JSON_HEADER_EP_ID : "53b5", SFXS_BACKEND_JSON_HEADER_DATA : COMMON_OOB_DATA},
    # MeteoFox startup data.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374001", SFXS_BACKEND_JSON_HEADER_EP_ID : "53b5", SFXS_BACKEND_JSON_HEADER_DATA : "1401041175753760"},
    # MeteoFox monitoring data without error.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374002", SFXS_BACKEND_JSON_HEADER_EP_ID : "53b5", SFXS_BACKEND_JSON_HEADER_DATA : "10173d3d4ca45d387e"},
    # MeteoFox monitoring data with error.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374003", SFXS_BACKEND_JSON_HEADER_EP_ID : "53b5", SFXS_BACKEND_JSON_HEADER_DATA : "117f401830a43d593f"},
    # MeteoFox geoloc data.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374006", SFXS_BACKEND_JSON_HEADER_EP_ID : "53b5", SFXS_BACKEND_JSON_HEADER_DATA : "2b81e249017a1cbf00a653"},
    # MeteoFox IM weather data.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374004", SFXS_BACKEND_JSON_HEADER_EP_ID : "53b5", SFXS_BACKEND_JSON_HEADER_DATA : "183a03002726"},
    # MeteoFox CM weather data.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374005", SFXS_BACKEND_JSON_HEADER_EP_ID : "53b5", SFXS_BACKEND_JSON_HEADER_DATA : "1456030026c804185700"},
    # MeteoFox geoloc timeout data.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374007", SFXS_BACKEND_JSON_HEADER_EP_ID : "53b5", SFXS_BACKEND_JSON_HEADER_DATA : "78"},
    # MeteoFox error stack data.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374008", SFXS_BACKEND_JSON_HEADER_EP_ID : "53b5", SFXS_BACKEND_JSON_HEADER_DATA : "270d00000000000000000000"},
    # MeteoFox invalid Sigfox EP-ID.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374009", SFXS_BACKEND_JSON_HEADER_EP_ID : "0123", SFXS_BACKEND_JSON_HEADER_DATA : "050c3900f29d1d2f7f"},
    # MeteoFox invalid data.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374010", SFXS_BACKEND_JSON_HEADER_EP_ID : "53b5", SFXS_BACKEND_JSON_HEADER_DATA : "010203"},
]

SENSIT_TEST_REQUEST = [
    # Sensit monitoring data.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374100", SFXS_BACKEND_JSON_HEADER_EP_ID : "b437b2", SFXS_BACKEND_JSON_HEADER_DATA : "ae096e97"},
    # Sensit configuration data.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374101", SFXS_BACKEND_JSON_HEADER_EP_ID : "b437b2", SFXS_BACKEND_JSON_HEADER_DATA : "b609759846003f0f8004223c"},
    # MeteoFox invalid Sigfox EP-ID.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374102", SFXS_BACKEND_JSON_HEADER_EP_ID : "0123", SFXS_BACKEND_JSON_HEADER_DATA : "050c3900f29d"},
    # MeteoFox invalid data.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374103", SFXS_BACKEND_JSON_HEADER_EP_ID : "b437b2", SFXS_BACKEND_JSON_HEADER_DATA : "010203"},
]

ATXFOX_TEST_REQUEST = [
    # ATXFox startup data.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374200", SFXS_BACKEND_JSON_HEADER_EP_ID : "868e", SFXS_BACKEND_JSON_HEADER_DATA : "1c020201749a0be1"},
    # ATXFox startup data.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374201", SFXS_BACKEND_JSON_HEADER_EP_ID : "868e", SFXS_BACKEND_JSON_HEADER_DATA : "01"},
    # ATXFox shutdown data.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374202", SFXS_BACKEND_JSON_HEADER_EP_ID : "868e", SFXS_BACKEND_JSON_HEADER_DATA : "00"},
    # ATXFox invalid data.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374203", SFXS_BACKEND_JSON_HEADER_EP_ID : "868e", SFXS_BACKEND_JSON_HEADER_DATA : "31"},
    # ATXFox monitoring data without error.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374204", SFXS_BACKEND_JSON_HEADER_EP_ID : "868e", SFXS_BACKEND_JSON_HEADER_DATA : "2fa302063bad0d5f1d"}, 
    # ATXFox monitoring data with error.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374205", SFXS_BACKEND_JSON_HEADER_EP_ID : "868e", SFXS_BACKEND_JSON_HEADER_DATA : "0d9903ffffff0d611e"},
    # ATXFox error stack data.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374206", SFXS_BACKEND_JSON_HEADER_EP_ID : "868e", SFXS_BACKEND_JSON_HEADER_DATA : "1d031d031d03000000000000"},
    # ATXFox invalid Sigfox EP-ID.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374207", SFXS_BACKEND_JSON_HEADER_EP_ID : "abcd", SFXS_BACKEND_JSON_HEADER_DATA : "050c3900f29d1d2f7f"},
    # ATXFox invalid data.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374208", SFXS_BACKEND_JSON_HEADER_EP_ID : "868e", SFXS_BACKEND_JSON_HEADER_DATA : "010203"},
]

TRACKFOX_TEST_REQUEST = [
    # TrackFox startup data.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374300", SFXS_BACKEND_JSON_HEADER_EP_ID : "4257", SFXS_BACKEND_JSON_HEADER_DATA : "0c010601fd3256e0"},
    # TrackFox monitoring data without error.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374301", SFXS_BACKEND_JSON_HEADER_EP_ID : "4257", SFXS_BACKEND_JSON_HEADER_DATA : "1741180000a55bca7c"},
    # TrackFox monitoring data with error.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374302", SFXS_BACKEND_JSON_HEADER_EP_ID : "4257", SFXS_BACKEND_JSON_HEADER_DATA : "17ff180000a55bca7c"},
    # TrackFox geoloc data.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374303", SFXS_BACKEND_JSON_HEADER_EP_ID : "4257", SFXS_BACKEND_JSON_HEADER_DATA : "2b883feb017084a7009606"},
    # TrackFox geoloc timeout data.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374304", SFXS_BACKEND_JSON_HEADER_EP_ID : "4257", SFXS_BACKEND_JSON_HEADER_DATA : "46"},
    # TrackFox error stack data.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374305", SFXS_BACKEND_JSON_HEADER_EP_ID : "4257", SFXS_BACKEND_JSON_HEADER_DATA : "1f0200000000000000000000"},
    # TrackFox invalid Sigfox EP-ID.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374306", SFXS_BACKEND_JSON_HEADER_EP_ID : "aabb", SFXS_BACKEND_JSON_HEADER_DATA : "121203138e7bc6f0"},
    # TrackFox invalid data.
    {SFXS_BACKEND_JSON_HEADER_TIME : "1666374307", SFXS_BACKEND_JSON_HEADER_EP_ID : "4257", SFXS_BACKEND_JSON_HEADER_DATA : "010203"},
]

# Function to send a test requests list.
def TEST_make(log_message, request_table):
    print(log_message)
    for idx in range(len(request_table)) :
        r = requests.post(SFXS_HTTP_ADDRESS, json=request_table[idx])
        print("Sending request " + str(idx) + r.text)
        time.sleep(HTTP_REQUEST_DELAY_SECONDS)
        
### MAIN PROGRAM ###

TEST_make("METEOFOX requests test", METEOFOX_TEST_REQUEST)
TEST_make("SENSIT requests test", SENSIT_TEST_REQUEST)
TEST_make("ATXFOX requests test", ATXFOX_TEST_REQUEST)
TEST_make("TRACKFOX requests test", TRACKFOX_TEST_REQUEST)