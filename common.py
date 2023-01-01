from __future__ import print_function

from influx_db import *
from log import *

### PUBLIC MACROS ###

COMMON_OOB_DATA = "OOB"
COMMON_STARTUP_DATA_LENGTH_BYTES = 8
COMMON_GEOLOC_DATA_LENGTH_BYTES = 11
COMMON_GEOLOC_TIMEOUT_DATA_LENGTH_BYTES = 1
# Error values.
COMMON_ERROR_DATA = "error"
COMMON_ERROR_VALUE_ANALOG_12BITS = 0xFFF
COMMON_ERROR_VALUE_ANALOG_16BITS = 0xFFFF
COMMON_ERROR_VALUE_ANALOG_24BITS = 0xFFFFFF
COMMON_ERROR_VALUE_LIGHT = 0xFF
COMMON_ERROR_VALUE_TEMPERATURE = 0x7F
COMMON_ERROR_VALUE_HUMIDITY = 0xFF
COMMON_ERROR_VALUE_UV_INDEX = 0xFF
COMMON_ERROR_VALUE_PRESSURE = 0xFFFF
COMMON_ERROR_VALUE_WIND = 0xFF
COMMON_ERROR_VALUE_RAIN = 0xFF

### PUBLIC FUNCTIONS ###

# Function which computes the real value of a one complement number.
def COMMON_one_complement_to_value(one_complement_data, sign_bit_position) :
    value = (one_complement_data & 0x7F);
    if ((one_complement_data & (1 << sign_bit_position)) != 0) :
        value = (-1) * value
    return value

# Function for parsing startup frame.
def COMMON_create_json_startup_data(timestamp, data) :
    # Parse fields.
    reset_flags = int(data[0:2], 16)
    version_major = int(data[2:4], 16)
    version_minor = int(data[4:6], 16)
    version_commit_index = int(data[6:8], 16)
    version_commit_id = int(data[8:15], 16)
    version_dirty_flag = int(data[15:16], 16)
    version = "SW" + str(version_major) + "." + str(version_minor) + "." + str(version_commit_index)
    if (version_dirty_flag != 0) :
        version = version + ".d"
    # Create JSON object.
    json_body = [
    {
        "time" : timestamp,
        "measurement" : INFLUX_DB_MEASUREMENT_GLOBAL,
        "fields" : {
            INFLUX_DB_FIELD_TIME_LAST_STARTUP : timestamp,
            INFLUX_DB_FIELD_RESET_FLAGS : reset_flags,
            INFLUX_DB_FIELD_VERSION : version,
            INFLUX_DB_FIELD_VERSION_MAJOR : version_major,
            INFLUX_DB_FIELD_VERSION_MINOR : version_minor,
            INFLUX_DB_FIELD_VERSION_COMMIT_INDEX : version_commit_index,
            INFLUX_DB_FIELD_VERSION_COMMIT_ID : version_commit_id,
            INFLUX_DB_FIELD_VERSION_DIRTY_FLAG : version_dirty_flag,
            INFLUX_DB_FIELD_TIME_LAST_COMMUNICATION : timestamp
        }
    }]
    log_data = "reset_flags=" + hex(reset_flags) + " version=" + version + " version_commit_id=" + hex(version_commit_id)
    return json_body, log_data

# Function for parsing geoloc frame.
def COMMON_create_json_geoloc_data(timestamp, data) :
    # Parse fields.
    latitude_degrees = int(data[0:2], 16)
    latitude_minutes = (int(data[2:4], 16) >> 2) & 0x3F
    latitude_seconds = ((((int(data[2:8], 16) & 0x03FFFE) >> 1) & 0x01FFFF) / (100000.0)) * 60.0
    latitude_north = int(data[6:8], 16) & 0x01
    latitude = latitude_degrees + (latitude_minutes / 60.0) + (latitude_seconds / 3600.0)
    if (latitude_north == 0):
        latitude = -latitude
    longitude_degrees = int(data[8:10], 16)
    longitude_minutes = (int(data[10:12], 16) >> 2) & 0x3F
    longitude_seconds = ((((int(data[10:16], 16) & 0x03FFFE) >> 1) & 0x01FFFF) / (100000.0)) * 60.0
    longitude_east = int(data[14:16], 16) & 0x01
    longitude = longitude_degrees + (longitude_minutes / 60.0) + (longitude_seconds / 3600.0)
    if (longitude_east == 0):
        longitude = -longitude
    altitude = int(data[16:20], 16)
    gps_fix_duration = int(data[20:22], 16)
    # Create JSON object.
    json_body = [
    {
        "time" : timestamp,
        "measurement" : INFLUX_DB_MEASUREMENT_GEOLOC,
        "fields" : {
            INFLUX_DB_FIELD_TIME_LAST_GEOLOC_DATA : timestamp,
            INFLUX_DB_FIELD_LATITUDE : latitude,
            INFLUX_DB_FIELD_LONGITUDE : longitude,
            INFLUX_DB_FIELD_ALTITUDE : altitude,
            INFLUX_DB_FIELD_GPS_FIX_DURATION : gps_fix_duration
        },
    },
    {
        "time" : timestamp,
        "measurement": INFLUX_DB_MEASUREMENT_GLOBAL,
        "fields": {
            INFLUX_DB_FIELD_TIME_LAST_COMMUNICATION : timestamp
        },
    }]
    log_data = "latitude=" + str(latitude) + ", longitude=" + str(longitude) + ", altitude=" + str(altitude) + "m, gps_fix_duration=" + str(gps_fix_duration) + "s"
    return json_body, log_data
    
# Function for parsing geoloc timeout frame.
def COMMON_create_json_geoloc_timeout_data(timestamp, data) :
    # Parse field.
    gps_timeout_duration = int(data[0:2], 16)
    # Create JSON object.
    json_body = [
    {
        "time" : timestamp,
        "measurement": INFLUX_DB_MEASUREMENT_GEOLOC,
        "fields": {
            INFLUX_DB_FIELD_GPS_TIMEOUT_DURATION : gps_timeout_duration
        },
    },
    {
        "time" : timestamp,
        "measurement": INFLUX_DB_MEASUREMENT_GLOBAL,
        "fields": {
            INFLUX_DB_FIELD_TIME_LAST_COMMUNICATION : timestamp
        },
    }]
    log_data = "gps_timeout_duration=" + str(gps_timeout_duration) + "s."
    return json_body, log_data
    
# Function for parsing error stack frame.
def COMMON_create_json_error_stack_data(timestamp, data, number_of_errors) :
    # Parse field.
    log_data = ""
    for idx in range(0, number_of_errors):
        error = int(data[(idx * 4) : ((idx * 4) + 4)], 16)
        # Store error code if not null.
        if (error != 0):
            # Create JSON object.
            json_body = [
            {
                "time": (timestamp + idx),
                "measurement": INFLUX_DB_MEASUREMENT_GLOBAL,
                "fields": {
                    INFLUX_DB_FIELD_TIME_LAST_COMMUNICATION : timestamp,
                    INFLUX_DB_FIELD_ERROR : error
                },
            }]
            log_data = log_data + "code_" + str(idx) + "=" + hex(error) + " "
    return json_body, log_data                