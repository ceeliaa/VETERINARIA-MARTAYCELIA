USE clinica_veterinaria;
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS citas;
DROP TABLE IF EXISTS mascotas;
DROP TABLE IF EXISTS empleados;
DROP TABLE IF EXISTS clientes;


SHOW TABLES;
CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    dni VARCHAR(20) UNIQUE NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    correo VARCHAR(100)
);

CREATE TABLE mascotas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    especie VARCHAR(50) NOT NULL,
    raza VARCHAR(50),
    sexo VARCHAR(10),
    edad INT,
    estado_salud VARCHAR(50),
    cliente_id INT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        ON DELETE CASCADE
);

CREATE TABLE empleados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    apellidos VARCHAR(100),
    puesto VARCHAR(50),
    telefono VARCHAR(20)
);

CREATE TABLE citas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATETIME NOT NULL,
    motivo VARCHAR(255),
    estado VARCHAR(50), /* Pendiente, Realizada, etc */
    mascota_id INT,
    empleado_id INT,
    FOREIGN KEY (mascota_id) REFERENCES mascotas(id) ON DELETE CASCADE,
    FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE SET NULL
);

DROP TABLE IF EXISTS saldo;


CREATE TABLE saldo (
    id INT PRIMARY KEY,
    cantidad DECIMAL(10,2) NOT NULL
);

INSERT INTO saldo (id, cantidad) VALUES (1, 0.00);


SELECT * FROM clientes;

INSERT INTO clientes (nombre, apellidos, dni, telefono, correo) VALUES
("María", "Blanco González", "12345678A", "612345678", "maria.blanco@mail.com"),
("Juan", "Pérez Martínez", "12345679B", "612345679", "juan.perez@mail.com"),
("Laura", "Santos Ruiz", "12345680C", "612345680", "laura.santos@mail.com"),
("Daniel", "García López", "12345681D", "612345681", "daniel.garcia@mail.com"),
("Celia", "Moreno Pérez", "12345682E", "612345682", "celia.moreno@mail.com"),
("Lucía", "Fernández Torres", "12345683F", "612345683", "lucia.fernandez@mail.com"),
("Miguel", "López Sánchez", "12345684G", "612345684", "miguel.lopez@mail.com"),
("Ana", "Martín Ortega", "12345685H", "612345685", "ana.martin@mail.com"),
("Carlos", "Navarro Díaz", "12345686J", "612345686", "carlos.navarro@mail.com"),
("Sara", "Castro Soto", "12345687K", "612345687", "sara.castro@mail.com"),
("David", "Rey Morales", "22345670A", "622345670", "david.rey@mail.com"),
("Sofía", "Núñez Ramos", "22345671B", "622345671", "sofia.nunez@mail.com"),
("Pablo", "Vega Herrera", "22345672C", "622345672", "pablo.vega@mail.com"),
("Irene", "Cabrera León", "22345673D", "622345673", "irene.cabrera@mail.com"),
("Adrián", "Suárez Molina", "22345674E", "622345674", "adrian.suarez@mail.com"),
("Nuria", "Benítez Rojas", "22345675F", "622345675", "nuria.benitez@mail.com"),
("Rubén", "Cano Iglesias", "22345676G", "622345676", "ruben.cano@mail.com"),
("Marta", "Gómez Prieto", "22345677H", "622345677", "marta.gomez@mail.com"),
("Raúl", "Lara Domínguez", "22345678J", "622345678", "raul.lara@mail.com"),
("Patricia", "Gil Salas", "22345679K", "622345679", "patricia.gil@mail.com"),
("Álvaro", "Crespo Bravo", "32345670A", "632345670", "alvaro.crespo@mail.com"),
("Elena", "Rubio Vázquez", "32345671B", "632345671", "elena.rubio@mail.com"),
("Óscar", "Padilla Fuentes", "32345672C", "632345672", "oscar.padilla@mail.com"),
("Cristina", "Hidalgo Campos", "32345673D", "632345673", "cristina.hidalgo@mail.com"),
("Mario", "Aguilar Peña", "32345674E", "632345674", "mario.aguilar@mail.com"),
("Clara", "Serrano Ríos", "32345675F", "632345675", "clara.serrano@mail.com"),
("Jorge", "Soto Esteban", "32345676G", "632345676", "jorge.soto@mail.com"),
("Paula", "Ramos Barrios", "32345677H", "632345677", "paula.ramos@mail.com"),
("Enrique", "Luna Cordero", "32345678J", "632345678", "enrique.luna@mail.com");
SELECT COUNT(*) FROM clientes;

INSERT INTO mascotas (nombre, especie, raza, sexo, edad, estado_salud, cliente_id) VALUES
("Milo", "Perro", "Labrador", "Macho", 3, "Sano", 1),
("Luna", "Gato", "Europeo", "Hembra", 2, "Sano", 2),
("Rocky", "Perro", "Bulldog", "Macho", 5, "Sano", 3),
("Nala", "Gato", "Siamés", "Hembra", 1, "Sano", 4),
("Toby", "Perro", "Beagle", "Macho", 4, "Sano", 5),
("Kira", "Gato", "Persa", "Hembra", 3, "Sano", 6),
("Max", "Perro", "Pastor Alemán", "Macho", 6, "Sano", 7),
("Sasha", "Gato", "Siberiano", "Hembra", 2, "Sano", 8),
("Leo", "Perro", "Chihuahua", "Macho", 1, "Sano", 9),
("Mia", "Gato", "Bengalí", "Hembra", 4, "Sano", 10),
("Thor", "Perro", "Rottweiler", "Macho", 4, "Sano", 11),
("Coco", "Gato", "Azul Ruso", "Hembra", 3, "Sano", 12),
("Balto", "Perro", "Husky", "Macho", 2, "Sano", 13),
("Pucky", "Gato", "Común", "Hembra", 5, "Sano", 14),
("Rex", "Perro", "Dóberman", "Macho", 4, "Sano", 15),
("Niko", "Gato", "Sphynx", "Macho", 2, "Sano", 16),
("Kiwi", "Perro", "Golden Retriever", "Hembra", 3, "Sano", 17),
("Simba", "Gato", "Siamés", "Macho", 2, "Sano", 18),
("Gala", "Perro", "Yorkshire", "Hembra", 5, "Sano", 19),
("Oreo", "Gato", "Común", "Macho", 1, "Sano", 20),
("Bolt", "Perro", "Border Collie", "Macho", 3, "Sano", 21),
("Nina", "Gato", "Europeo", "Hembra", 2, "Sano", 22),
("Bobby", "Perro", "Mestizo", "Macho", 7, "Sano", 23),
("Mimi", "Gato", "Persa", "Hembra", 4, "Sano", 24),
("Koby", "Perro", "Pomerania", "Macho", 2, "Sano", 25),
("Runa", "Gato", "Común", "Hembra", 3, "Sano", 26),
("Tango", "Perro", "Caniche", "Macho", 4, "Sano", 27),
("Zoe", "Gato", "Bengalí", "Hembra", 1, "Sano", 28),
("Romeo", "Perro", "Carlino", "Macho", 6, "Sano", 29),
("Kali", "Gato", "Siberiano", "Hembra", 2, "Sano", 30);

SELECT COUNT(*) FROM mascotas;

INSERT INTO empleados (nombre, apellidos, puesto, telefono) VALUES
("Laura", "Serrano Martín", "Veterinaria", "600100001"),
("Hugo", "García Torres", "Veterinario", "600100002"),
("Marta", "Blanco Vega", "Recepción", "600100003"),
("Sergio", "Ruiz Ramos", "Asistente", "600100004"),
("Ana", "Navarro León", "Veterinaria", "600100005"),
("Pablo", "Díaz Montes", "Peluquero Canino", "600100006"),
("Lucía", "Morales Rey", "Recepción", "600100007"),
("David", "Soto Domínguez", "Veterinario", "600100008"),
("Elena", "Romero Pardo", "Asistente", "600100009"),
("Javier", "Campos Pino", "Veterinario", "600100010"),
("Clara", "Moya Zurita", "Auxiliar", "600100011"),
("Miguel", "Rivas Alba", "Veterinario", "600100012"),
("Sara", "Castillo Durán", "Auxiliar", "600100013"),
("Tomás", "Varela Solís", "Peluquero Canino", "600100014"),
("Nuria", "Roldán Cruz", "Recepción", "600100015"),
("Álvaro", "Martín Recio", "Veterinario", "600100016"),
("Patricia", "Sáez Bravo", "Auxiliar", "600100017"),
("Jorge", "Gallego Núñez", "Veterinario", "600100018"),
("Irene", "Cano Estévez", "Auxiliar", "600100019"),
("Raúl", "Pastor Santos", "Recepción", "600100020");


INSERT INTO citas (fecha, motivo, mascota_id, empleado_id, estado) VALUES
("2024-01-15 10:00:00", "Vacunación anual", 1, 3, "Realizada"),
("2024-02-10 16:30:00", "Consulta general", 2, 1, "Realizada"),
("2024-03-05 12:00:00", "Revisión dental", 3, 5, "Realizada"),
("2024-03-20 09:30:00", "Dolor abdominal", 4, 2, "Pendiente"),
("2024-03-25 11:45:00", "Análisis de sangre", 5, 4, "Realizada"),
("2024-04.01 17:00:00", "Problemas de piel", 6, 7, "Cancelada"),
("2024-04-18 10:15:00", "Vacuna de la rabia", 7, 6, "Realizada"),
("2024-05-02 15:30:00", "Otitis", 8, 8, "Pendiente"),
("2024-05-19 13:00:00", "Alergia estacional", 9, 2, "Realizada"),
("2024-05-25 18:00:00", "Desparasitación", 10, 3, "Realizada"),

("2024-06-04 10:45:00", "Revisión general", 11, 9, "Pendiente"),
("2024-06-10 12:30:00", "Dermatitis", 12, 1, "Realizada"),
("2024-06-21 16:00:00", "Control posquirúrgico", 13, 11, "Realizada"),
("2024-07-03 09:15:00", "Vacuna polivalente", 14, 12, "Realizada"),
("2024-07-17 14:20:00", "Tos persistente", 15, 4, "Pendiente"),

("2024-07-29 11:00:00", "Golpe en la pata", 16, 10, "Realizada"),
("2024-08-05 17:10:00", "Revisión anual", 17, 8, "Realizada"),
("2024-08-20 10:50:00", "Problemas digestivos", 18, 6, "Pendiente"),
("2024-09-02 12:40:00", "Vacunación", 19, 14, "Realizada"),
("2024-09-18 16:30:00", "Conjuntivitis", 20, 15, "Realizada"),

("2024-10-05 09:00:00", "Desparasitación", 21, 20, "Realizada"),
("2024-10-16 17:30:00", "Corte de uñas", 22, 13, "Realizada"),
("2024-11-01 13:45:00", "Infección respiratoria", 23, 11, "Pendiente"),
("2024-11-12 15:00:00", "Revisión", 24, 5, "Realizada"),
("2024-11-28 11:30:00", "Caída reciente", 25, 4, "Realizada"),

("2024-12-04 18:00:00", "Control de peso", 26, 3, "Realizada"),
("2024-12-14 10:00:00", "Consulta preventiva", 27, 7, "Pendiente"),
("2024-12-22 12:10:00", "Rascado excesivo", 28, 16, "Realizada"),
("2025-01-09 16:20:00", "Fiebre", 29, 2, "Realizada"),
("2025-01-15 09:50:00", "Vacunación anual", 30, 1, "Pendiente"),

("2025-01-29 14:00:00", "Pérdida de apetito", 5, 9, "Realizada"),
("2025-02-06 11:25:00", "Cojera", 12, 10, "Realizada"),
("2025-02-14 17:45:00", "Diabetes control", 3, 6, "Pendiente"),
("2025-02-25 10:10:00", "Vacuna leptospirosis", 7, 14, "Realizada"),
("2025-03-03 12:30:00", "Chequeo prequirúrgico", 18, 17, "Pendiente"),

("2025-03-11 16:00:00", "Urgencia: vómitos", 22, 19, "Realizada"),
("2025-03-20 09:00:00", "Consulta general", 9, 3, "Realizada"),
("2025-04-01 15:30:00", "Piel seca", 13, 11, "Realizada"),
("2025-04-09 10:15:00", "Dolor lumbar", 16, 8, "Pendiente"),
("2025-04-18 17:55:00", "Vacuna antirrábica", 2, 4, "Realizada");

SELECT COUNT(*) FROM citas;


SELECT * FROM citas LIMIT 10;

DELETE FROM saldo WHERE id = 1;
INSERT INTO saldo (id, cantidad) VALUES (1, 2500.00);


SHOW TABLES;

ALTER TABLE clientes 
ADD COLUMN direccion VARCHAR(200) AFTER telefono;

DESCRIBE clientes;
ALTER TABLE clientes
ADD COLUMN fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP;


SELECT * FROM mascotas WHERE cliente_id = (SELECT id FROM clientes WHERE nombre = 'Daniel');

SELECT * FROM mascotas WHERE cliente_id = 2;
SELECT * FROM saldo;
INSERT INTO saldo (id, cantidad) VALUES
(2, 1780.50),
(3, 3200.75),
(4, 950.00),
(5, 4120.90),
(6, 2675.40),
(7, 389.99),
(8, 1540.25),
(9, 6050.00),
(10, 780.60),
(11, 2245.70),
(12, 1190.30),
(13, 330.00),
(14, 8700.00),
(15, 46.20);

DROP TABLE IF EXISTS saldo;
CREATE TABLE saldo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATETIME,
    tipo_operacion VARCHAR(50),
    concepto VARCHAR(200),
    monto DECIMAL(10,2),
    saldo_anterior DECIMAL(10,2),
    saldo_nuevo DECIMAL(10,2)
);

ALTER TABLE saldo 
ADD COLUMN saldo DECIMAL(10,2) AFTER saldo_nuevo;

SELECT * FROM saldo;

INSERT INTO saldo (fecha, tipo_operacion, concepto, monto, saldo_anterior, saldo_nuevo) VALUES
("2024-01-01 09:00:00", "INICIO", "Saldo inicial del sistema", 0.00, 0.00, 2500.00),

("2024-01-03 11:15:00", "INGRESO", "Consulta general - Cliente: Daniel Romero", 45.00, 2500.00, 2545.00),
("2024-01-04 10:00:00", "INGRESO", "Vacunación - Cliente: Ana López", 30.00, 2545.00, 2575.00),
("2024-01-05 16:40:00", "GASTO", "Nómina Empleado: Laura Serrano Martín", 1200.00, 2575.00, 1375.00),

("2024-01-07 12:20:00", "INGRESO", "Consulta digestiva - Cliente: Sergio Ruiz", 50.00, 1375.00, 1425.00),
("2024-01-08 17:10:00", "INGRESO", "Desparasitación - Cliente: Marta Blanco", 35.00, 1425.00, 1460.00),
("2024-01-10 09:30:00", "GASTO", "Pago a proveedor: Material médico", 280.00, 1460.00, 1180.00),

("2024-01-12 15:50:00", "INGRESO", "Consulta dermatológica - Cliente: Hugo García", 55.00, 1180.00, 1235.00),
("2024-01-13 11:00:00", "GASTO", "Nómina Empleado: Hugo García Torres", 1250.00, 1235.00, -15.00),

("2024-01-14 13:30:00", "INGRESO", "Revisión general - Cliente: Elena Romero", 40.00, -15.00, 25.00),
("2024-01-15 18:10:00", "INGRESO", "Vacunación - Cliente: Pablo Díaz", 30.00, 25.00, 55.00),

("2024-01-16 10:45:00", "GASTO", "Factura proveedor: Limpieza clínica", 90.00, 55.00, -35.00),

("2024-01-17 11:50:00", "INGRESO", "Consulta general - Cliente: Nuria Roldán", 45.00, -35.00, 10.00),
("2024-01-18 09:20:00", "INGRESO", "Control post-operatorio - Cliente: Javier Campos", 50.00, 10.00, 60.00),

("2024-01-19 14:00:00", "GASTO", "Nómina Empleado: Marta Blanco Vega", 1100.00, 60.00, -1040.00),

("2024-01-21 09:00:00", "INGRESO", "Corte pelo canino - Cliente: Raúl Pastor", 25.00, -1040.00, -1015.00),

("2024-01-22 15:10:00", "INGRESO", "Consulta general - Cliente: Irene Cano", 45.00, -1015.00, -970.00),
("2024-01-23 12:40:00", "INGRESO", "Vacuna antirrábica - Cliente: Sara Castillo", 35.00, -970.00, -935.00),

("2024-01-25 17:30:00", "GASTO", "Pago proveedor: Equipamiento quirúrgico", 350.00, -935.00, -1285.00);


ALTER TABLE citas ADD COLUMN duracion INT DEFAULT 60;

INSERT INTO mascotas (nombre, especie, raza, sexo, edad, estado_salud, cliente_id) VALUES
("Bunny", "Conejo", "Enano Holandés", "Hembra", 2, "Sano", 1),
("Storm", "Hurón", "Hurón Doméstico", "Macho", 3, "Sano", 2),
("Shelly", "Tortuga", "Tortuga Rusa", "Hembra", 5, "Sano", 3),
("Pip", "Hámster", "Hámster Sirio", "Macho", 1, "Sano", 4),
("Kiwi", "Loro", "Loro Amazonas", "Hembra", 4, "Sano", 5),
("Rango", "Iguana", "Iguana Verde", "Macho", 6, "Sano", 6),
("Nugget", "Cobaya", "Cobaya Abisinia", "Hembra", 2, "Sano", 7),
("Shadow", "Serpiente", "Pitón Real", "Macho", 3, "Sano", 8),
("Loki", "Gecko", "Leopard Gecko", "Macho", 2, "Sano", 9),
("Spike", "Erizo", "Erizo Africano", "Macho", 1, "Sano", 10),
("Quack", "Pato", "Pato Doméstico", "Hembra", 2, "Sano", 11),
("Cleo", "Gallina", "Plymouth Rock", "Hembra", 1, "Sano", 12),
("Blanca", "Cabra", "Cabra Enana", "Hembra", 3, "Sano", 13),
("Tornado", "Pony", "Pony Shetland", "Macho", 7, "Sano", 14),
("Pepper", "Cerdo", "Cerdo Vietnamita", "Macho", 4, "Sano", 15),
("Chispa", "Chinchilla", "Chinchilla Estándar", "Hembra", 2, "Sano", 16),
("Bubbles", "Pez", "Pez Betta", "Macho", 1, "Sano", 17),
("Neo", "Camaleón", "Camaleón Velado", "Macho", 3, "Sano", 18),
("Blue", "Periquito", "Periquito Australiano", "Hembra", 2, "Sano", 19),
("Groot", "Sapo", "Sapo Verde Europeo", "Macho", 1, "Sano", 20);

SELECT cliente_id, COUNT(*) 
FROM mascotas 
GROUP BY cliente_id;

SELECT * FROM mascotas WHERE cliente_id = (SELECT id FROM clientes WHERE nombre = 'Daniel');

SELECT 
    c.id,
    CONCAT(c.nombre, ' ', c.apellidos) AS cliente,
    COUNT(m.id) AS num_mascotas
FROM clientes c
LEFT JOIN mascotas m ON c.id = m.cliente_id
GROUP BY c.id, c.nombre, c.apellidos
ORDER BY num_mascotas DESC;
