CREATE TYPE stationType AS ENUM ('BOP-EXP', 'BOP-CTRL', 'EPN-EXP', 'EPN-CTRL', 'TOUR');
CREATE TYPE boxType AS ENUM('1', '2', '3', '4', '5', '6', '7', '8', 'FLUX', 'AP200');
CREATE TYPE loggerType AS ENUM('CR1000X', 'CR1000');
CREATE TYPE forestSensorType AS ENUM('dendrometer', 'sapflow', 'CS616', 'SM100', 'SMEC300'); -- Add those from the tower later
CREATE TYPE portType AS ENUM('1H', '1L', '1HL', '2H', '2L', '2HL', '3H', '3L', '3HL', '4H', '4L', '4HL', '5H', '5L', '5HL', '6H', '6L', '6HL', '7H', '7L', '7HL', '8H', '8L', '8HL');

CREATE TABLE station (
    stationCode stationType PRIMARY KEY
);

CREATE TABLE loggerBox (
    boxNumber boxType PRIMARY KEY,
    loggerSerialNumber TEXT NOT NULL UNIQUE,
    loggerModel loggerType NOT NULL
);

CREATE TABLE stationBox (
    stationCode stationType NOT NULL,
    boxNumber boxType NOT NULL,

    PRIMARY KEY (stationCode, boxNumber),

    FOREIGN KEY (stationCode) REFERENCES station(stationCode),
    FOREIGN KEY (boxNumber) REFERENCES loggerBox(boxNumber)
);

CREATE TABLE sensor (
    stationCode stationType NOT NULL,
    boxNumber boxType NOT NULL,
    sensorNumber INT NOT NULL,
    sensorType forestSensorType NOT NULL,
    loggerVarName TEXT NOT NULL,
    port portType NOT NULL,

    PRIMARY KEY (stationCode, boxNumber, sensorNumber, sensorType),

    FOREIGN KEY (stationCode, boxNumber)
        REFERENCES stationBox(stationCode, boxNumber)
);

-- hypertable
CREATE TABLE measurement (
    measured_at TIMESTAMPTZ NOT NULL,

    stationCode stationType NOT NULL,
    boxNumber boxType NOT NULL,
    sensorNumber INT NOT NULL,
    sensorType forestSensorType NOT NULL,

    fieldName TEXT NOT NULL,

    value DOUBLE PRECISION NOT NULL,
    unit TEXT NOT NULL,

    receivedAt TIMESTAMPTZ NOT NULL DEFAULT now(),

    PRIMARY KEY (
        measured_at,
        stationCode,
        boxNumber,
        sensorNumber,
        sensorType,
        fieldName
    ),

    FOREIGN KEY (stationCode, boxNumber, sensorNumber, sensorType)
        REFERENCES sensor(stationCode, boxNumber, sensorNumber, sensorType)
);

SELECT create_hypertable('measurement', 'measured_at');
