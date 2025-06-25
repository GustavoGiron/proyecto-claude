-- 1) Departamentos
INSERT INTO Departamentos (Codigo, Nombre) VALUES
('AL','Alta Verapaz'),
('BA','Baja Verapaz'),
('CH','Chimaltenango'),
('CQ','Chiquimula'),
('PR','El Progreso'),
('ES','Escuintla'),
('GU','Guatemala'),
('HU','Huehuetenango'),
('IZ','Izabal'),
('JA','Jalapa'),
('JU','Jutiapa'),
('PE','Petén'),
('QC','Quiché'),
('RE','Retalhuleu'),
('SA','Sacatepéquez'),
('SM','San Marcos'),
('SR','Santa Rosa'),
('SO','Sololá'),
('SU','Suchitepéquez'),
('TO','Totonicapán'),
('ZA','Zacapa'),
('QZ','Quetzaltenango');


-- 2) Municipios

-- Alta Verapaz (Id=1)
INSERT INTO Municipios (DepartamentoId, Nombre) VALUES
(1,'Chahal'),(1,'Chisec'),(1,'Cobán'),(1,'Fray Bartolomé de las Casas'),
(1,'Lanquín'),(1,'Panzós'),(1,'Raxruhá'),(1,'San Cristóbal Verapaz'),
(1,'San Juan Chamelco'),(1,'San Pedro Carchá'),(1,'Santa Catarina La Tinta'),
(1,'Santa María Cahabón'),(1,'Santa Cruz Verapaz'),(1,'Senahú'),
(1,'Tactic'),(1,'Tamahu'),(1,'Tucurú');

-- Baja Verapaz (Id=2)
INSERT INTO Municipios (DepartamentoId, Nombre) VALUES
(2,'Cubulco'),(2,'Granados'),(2,'Purulhá'),(2,'Rabinal'),
(2,'Salamá'),(2,'San Jerónimo'),(2,'San Miguel Chicaj');

-- Chimaltenango (Id=3)
INSERT INTO Municipios (DepartamentoId, Nombre) VALUES
(3,'Chimaltenango'),(3,'El Tejar'),(3,'Parramos'),(3,'Patzicía'),
(3,'Patzún'),(3,'Pochuta'),(3,'San Andrés Itzapa'),(3,'San José Poaquil'),
(3,'San Martín Jilotepeque'),(3,'Santa Apolonia'),(3,'Tecpán Guatemala'),
(3,'Yepocapa');

-- Chiquimula (Id=4)
INSERT INTO Municipios (DepartamentoId, Nombre) VALUES
(4,'Camotán'),(4,'Chiquimula'),(4,'Concepción Las Minas'),
(4,'Esquipulas'),(4,'Jocotán'),(4,'Olopa'),(4,'Quezaltepeque'),
(4,'San Jacinto'),(4,'San José La Arada'),(4,'San Juan Ermita'),
(4,'Santa María Puma') ;

-- El Progreso (Id=5)
INSERT INTO Municipios (DepartamentoId, Nombre) VALUES
(5,'El Jícaro'),(5,'Guastatoya'),(5,'Morazán'),
(5,'San Agustín Acasaguastlán'),(5,'San Cristóbal Acasaguastlán'),
(5,'Sansare') ;

-- Escuintla (Id=6)
INSERT INTO Municipios (DepartamentoId, Nombre) VALUES
(6,'Escuintla'),(6,'Guanagazapa'),(6,'Iztapa'),
(6,'La Democracia'),(6,'La Gomera'),(6,'Masagua'),
(6,'Nueva Concepción'),(6,'Palín'),(6,'San José'),
(6,'San Vicente Pacaya'),(6,'Santa Lucía Cotzumalguapa'),
(6,'Sipacate'),(6,'Siquinalá'),(6,'Tiquisate');

-- Guatemala (Id=7)
INSERT INTO Municipios (DepartamentoId, Nombre) VALUES
(7,'Amatitlán'),(7,'Chinautla'),(7,'Chuarrancho'),
(7,'Guatemala'),(7,'Mixco'),(7,'Palencia'),
(7,'Petapa'),(7,'San José del Golfo'),(7,'San José Pinula'),
(7,'San Juan Sacatepéquez'),(7,'San Miguel Petapa'),
(7,'San Pedro Ayampuc'),(7,'San Pedro Sacatepéquez'),
(7,'San Raymundo'),(7,'Santa Catarina Pinula'),
(7,'Villa Canales'),(7,'Villa Nueva');

-- Huehuetenango (Id=8)
INSERT INTO Municipios (DepartamentoId, Nombre) VALUES
(8,'Aguacatán'),(8,'Chiantla'),(8,'Colotenango'),
(8,'Concepción Huista'),(8,'Cuilco'),(8,'La Democracia'),
(8,'La Libertad'),(8,'Malacatancito'),(8,'Nentón'),
(8,'San Antonio Huista'),(8,'San Gaspar Ixchil'),(8,'San Ildefonso Ixtahuacán'),
(8,'San Juan Atitán'),(8,'San Juan Ixcoy'),(8,'San Mateo Ixtatán'),
(8,'San Miguel Acatán'),(8,'San Pedro Necta'),(8,'San Rafael La Independencia'),
(8,'San Sebastián Huehuetenango'),(8,'Santa Ana Huista'),(8,'Santa Bárbara'),
(8,'Santa Cruz Barillas'),(8,'Santa Eulalia'),(8,'Santiago Chimaltenango'),
(8,'Tectitán');

-- Izabal (Id=9)
INSERT INTO Municipios (DepartamentoId, Nombre) VALUES
(9,'El Estor'),(9,'Livingston'),(9,'Los Amates'),
(9,'Mataquescuintla'),(9,'Puerto Barrios');

-- Jalapa (Id=10)
INSERT INTO Municipios (DepartamentoId, Nombre) VALUES
(10,'Jalapa'),(10,'Mataquescuintla'),(10,'Monjas'),
(10,'San Carlos Alzatate'),(10,'San Luis Jilotepeque'),
(10,'San Manuel Chaparrón') ;

-- Jutiapa (Id=11)
INSERT INTO Municipios (DepartamentoId, Nombre) VALUES
(11,'Agua Blanca'),(11,'Asunción Mita'),(11,'Atescatempa'),
(11,'Comapa'),(11,'Conguaco'),(11,'El Adelanto'),
(11,'Jalpatagua'),(11,'Jerez'),(11,'Jutiapa'),
(11,'Moyuta'),(11,'Pasaco'),(11,'Quesada'),
(11,'San José Acatempa'),(11,'Santa Catarina Mita'),
(11,'Yupiltepeque');

-- Petén (Id=12)
INSERT INTO Municipios (DepartamentoId, Nombre) VALUES
(12,'Dolores'),(12,'El Chal'),(12,'Flores'),
(12,'Las Cruces'),(12,'Melchor de Mencos'),
(12,'Poptún'),(12,'San Andrés'),
(12,'San Benito'),(12,'San Francisco'),
(12,'San José'),(12,'San Luis'),(12,'Sayaxché');

-- Quiché (Id=13)
INSERT INTO Municipios (DepartamentoId, Nombre) VALUES
(13,'Canillá'),(13,'Chajul'),(13,'Chicamán'),
(13,'Chiché'),(13,'Chichicastenango'),
(13,'Chinique'),(13,'Cunén'),
(13,'Ixcán'),(13,'Joyabaj'),(13,'Patzité'),
(13,'Sacapulas'),(13,'San Andrés Sajcabajá'),
(13,'San Bartolomé Jocotenango'),(13,'San Gaspar Vivar'),
(13,'Santa Cruz del Quiché'),
(13,'Uspantán'),(13,'Zacualpa');

-- Retalhuleu (Id=14)
INSERT INTO Municipios (DepartamentoId, Nombre) VALUES
(14,'Champerico'),(14,'El Asintal'),(14,'Nuevo San Carlos'),
(14,'Retalhuleu'),(14,'San Andrés Villa Seca'),
(14,'San Martín Zapotitlán'),(14,'San Sebastián'),
(14,'Santa Cruz Muluá');

-- Sacatepéquez (Id=15)
INSERT INTO Municipios (DepartamentoId, Nombre) VALUES
(15,'Alotenango'),(15,'Antigua Guatemala'),(15,'Ciudad Vieja'),
(15,'Jocotenango'),(15,'Pastores'),(15,'San Antonio Aguas Calientes'),
(15,'San Bartolomé Milpas Altas'),(15,'San Lucas Sacatepéquez'),
(15,'San Miguel Dueñas'),(15,'San Pedro Pastores'),
(15,'Sumpango');

-- San Marcos (Id=16)
INSERT INTO Municipios (DepartamentoId, Nombre) VALUES
(16,'Ayutla'),(16,'Catarina'),(16,'El Quetzal'),
(16,'El Tumbador'),(16,'Esquipulas Palo Gordo'),
(16,'Ixchiguán'),(16,'La Blanca'),(16,'La Reforma'),
(16,'Malacatán'),(16,'Nuevo Progreso'),(16,'Ocós'),
(16,'Pajapita'),(16,'Río Blanco'),(16,'San Antonio Sacatepéquez'),
(16,'San Cristóbal Cucho'),(16,'San José Ojetenam'),
(16,'San Lorenzo'),(16,'San Marcos'),(16,'San Miguel Ixtahuacán'),
(16,'San Pablo'),(16,'San Pedro Sacatepéquez'),(16,'San Rafael Pie de la Cuesta'),
(16,'Sibinal'),(16,'Sipacapa'),(16,'Tajumulco'),(16,'Tecuán'),
(16,'Malacatán');

-- Santa Rosa (Id=17)
INSERT INTO Municipios (DepartamentoId, Nombre) VALUES
(17,'Barberena'),(17,'Casillas'),(17,'Chiquimulilla'),
(17,'Cuilapa'),(17,'Guazacapán'),(17,'Nueva Santa Rosa'),
(17,'Oratorio'),(17,'Pueblo Nuevo Viñas'),
(17,'San Juan Tecuaco'),(17,'San Rafael Las Flores'),
(17,'Santa Cruz Naranjo'),(17,'Santa María Ixhuatán'),
(17,'Santa Rosa de Lima');

-- Sololá (Id=18)
INSERT INTO Municipios (DepartamentoId, Nombre) VALUES
(18,'Concepción'),(18,'Nahualá'),(18,'Panajachel'),
(18,'Santa Catarina Ixtahuacán'),(18,'Santa Catarina Palopó'),
(18,'Santa Clara La Laguna'),(18,'Santa Cruz La Laguna'),
(18,'Santa Lucía Utatlán'),(18,'Santa María Visitación'),
(18,'Santiago Atitlán'),(18,'Sololá'),
(18,'San Andrés Semetabaj'),(18,'San Antonio Palopó'),
(18,'San José Chacayá'),(18,'San Juan La Laguna'),
(18,'San Lucas Tolimán');

-- Suchitepéquez (Id=19)
INSERT INTO Municipios (DepartamentoId, Nombre) VALUES
(19,'Chicacao'),(19,'Cuyotenango'),(19,'Patulul'),
(19,'Pueblo Nueva'),(19,'Río Bravo'),(19,'Samayac'),
(19,'San Antonio Suchitepéquez'),(19,'San Bernardino'),
(19,'San Francisco Zapotitlán'),(19,'San Gabriel'),
(19,'San José El Idolo'),(19,'San Juan Bautista'),
(19,'San Lorenzo'),(19,'San Miguel Panán'),
(19,'San Pablo Jocopilas'),(19,'Santa Bárbara'),
(19,'Santo Domingo Suchitepéquez'),
(19,'Santo Tomás La Unión'),(19,'Zunilito');

-- Totonicapán (Id=20)
INSERT INTO Municipios (DepartamentoId, Nombre) VALUES
(20,'Momostenango'),(20,'San Andrés Xecul'),
(20,'San Bartolo'),(20,'San Cristóbal Totonicapán'),
(20,'San Francisco El Alto'),(20,'San Juan Ixcoy'),
(20,'San Miguel Chicaj ?'),(20,'San Pablo La Laguna'),
(20,'Santa Lucía La Reforma'),
(20,'Santa María Chiquimula'),(20,'Totonicapán');

-- Zacapa (Id=21)
INSERT INTO Municipios (DepartamentoId, Nombre) VALUES
(21,'Cabañas'),(21,'Estanzuela'),(21,'Gualán'),
(21,'Huité'),(21,'La Unión'),(21,'Río Hondo'),
(21,'San Diego'),(21,'Teculután'),(21,'Usumatlán'),
(21,'Zacapa');

-- Quetzaltenango (Id=22)
INSERT INTO Municipios (DepartamentoId, Nombre) VALUES
(22,'Almolonga'),(22,'Cantel'),(22,'Coatepeque'),
(22,'Colomba Costa Cuca'),(22,'Concepción Chiquirichapa'),
(22,'El Palmar'),(22,'Flores Costa Cuca'),(22,'Génova'),
(22,'La Esperanza'),(22,'Olintepeque'),(22,'Palestina de Los Altos'),
(22,'Salcajá'),(22,'San Carlos Sija'),
(22,'San Francisco La Unión'),(22,'San Juan Ostuncalco'),
(22,'San Martín Sacatepéquez'),
(22,'San Mateo'),(22,'San Miguel Sigüilá'),
(22,'San Sebastián'),(22,'Zunilal');