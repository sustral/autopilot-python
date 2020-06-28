## Topics and Messages

topics: `baro_raw`

message:

    {
        "time" : curr_time,
        "data" : {
            "temp" : temp,
            "pres" : pres
        }
    }

___

topics: `mpu_raw`, `lsm_raw`

message:

    {
        "time" : curr_time,
        "data" : {
            "acc" : acc,
            "gyr" : gyr,
            "mag" : mag
        }
    
    }

___

topics: `motor_inst`

message:

    {
        "fl": 0,
        "fr": 0,
        "bl": 0,
        "br": 0
    }
