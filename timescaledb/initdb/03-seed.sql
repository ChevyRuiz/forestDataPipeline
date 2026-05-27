-- Stations
INSERT INTO station (stationCode)
VALUES
    ('BOP-EXP'),
    ('BOP-CTRL'),
    ('EPN-EXP'),
    ('EPN-CTRL'),
    ('TOUR')
ON CONFLICT DO NOTHING;


-- Logger boxes / boîtiers
INSERT INTO loggerBox (boxNumber, loggerSerialNumber, loggerModel)
VALUES
    ('5', '24833', 'CR1000X')
ON CONFLICT DO NOTHING;


-- Station - Boîtier relation
INSERT INTO stationBox (stationCode, boxNumber)
VALUES
    ('BOP-CTRL', '5'),
    ('BOP-EXP', '5')
ON CONFLICT DO NOTHING;


-- Sensors
INSERT INTO sensor (
    stationCode,
    boxNumber,
    sensorNumber,
    sensorType,
    loggerVarName,
    port
)
VALUES
    -- BOP-EXP
    ('BOP-EXP', '5', 5, 'dendrometer', 'dendro(1)', '1HL'),
    ('BOP-EXP', '5', 4, 'sapflow', 'sapflow(1)', '5HL'),
    ('BOP-EXP', '5', 5, 'sapflow', 'sapflow(2)', '6HL'),
    ('BOP-EXP', '5', 3, 'CS616', 'VW(1)', '8H'),

    -- BOP-CTRL
    ('BOP-CTRL', '5', 5, 'dendrometer', 'dendro(2)', '2HL'),
    ('BOP-CTRL', '5', 6, 'dendrometer', 'dendro(3)', '3HL'),
    ('BOP-CTRL', '5', 7, 'dendrometer', 'dendro(4)', '4HL'),
    ('BOP-CTRL', '5', 6, 'sapflow', 'sapflow(3)', '7HL'),
    ('BOP-CTRL', '5', 3, 'CS616', 'VW(2)', '8L')
ON CONFLICT DO NOTHING;
