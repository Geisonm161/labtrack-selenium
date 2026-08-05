# Historias de usuario y criterios

Cada sección debe registrarse como una historia independiente en Jira o Azure DevOps. Se recomienda crear las etiquetas `selenium`, `camino-feliz`, `negativa` y `limite`, y adjuntar a cada historia sus tres escenarios.

## HU-01 — Iniciar sesión

**Como** responsable del laboratorio, **quiero** iniciar sesión con mis credenciales **para** acceder de forma segura al inventario.

### Criterios de aceptación

1. Dado un usuario registrado mediante la configuración segura, cuando introduce sus credenciales válidas, entonces el sistema abre el inventario y confirma el inicio de sesión.
2. Los campos usuario y contraseña son obligatorios.
3. La contraseña admite entre 8 y 64 caracteres y el usuario entre 3 y 30.

### Criterios de rechazo

1. Se rechaza una combinación de usuario y contraseña que no coincide con un usuario registrado.
2. No se envía el formulario si uno de los campos obligatorios está vacío.
3. Una persona no autenticada que intenta acceder al inventario es redirigida al login.

### Escenarios automatizados

- Feliz: credenciales válidas abren `/equipos`.
- Negativo: contraseña incorrecta muestra `Credenciales inválidas`.
- Límite: usuario vacío activa la validación obligatoria del navegador.

## HU-02 — Registrar un equipo

**Como** responsable del laboratorio, **quiero** registrar un equipo **para** mantener actualizado el inventario.

### Criterios de aceptación

1. El equipo se registra con código único, nombre, categoría, estado y cantidad válidos.
2. El código contiene entre 3 y 12 caracteres; el nombre, entre 3 y 80; y la categoría, entre 3 y 40.
3. La cantidad se encuentra entre 0 y 9999, ambos inclusive.
4. Al guardar, el sistema muestra el detalle y una confirmación.

### Criterios de rechazo

1. No se permite registrar un código que ya pertenece a otro equipo.
2. Se rechazan campos obligatorios vacíos o fuera de su rango.
3. Se rechaza un estado distinto de `Disponible`, `Prestado` o `En mantenimiento`.

### Escenarios automatizados

- Feliz: registro de una centrífuga con datos válidos.
- Negativo: intento de registro con el código existente `EQ-001`.
- Límite: registro con un nombre de exactamente 80 caracteres y cantidad 0.

## HU-03 — Consultar equipos

**Como** responsable del laboratorio, **quiero** consultar y buscar equipos **para** conocer su información y disponibilidad.

### Criterios de aceptación

1. El inventario lista código, nombre, categoría, estado y cantidad.
2. Al seleccionar el nombre se muestra el detalle completo del equipo.
3. La búsqueda encuentra coincidencias parciales por código, nombre o categoría.
4. El término de búsqueda admite hasta 50 caracteres.

### Criterios de rechazo

1. Cuando no hay coincidencias, no se muestran registros ajenos a la búsqueda.
2. La interfaz informa claramente que no se encontraron equipos.
3. No se procesan más de 50 caracteres como criterio de búsqueda.

### Escenarios automatizados

- Feliz: consulta del detalle del microscopio `EQ-001`.
- Negativo: búsqueda inexistente muestra el estado vacío.
- Límite: búsqueda con exactamente 50 caracteres.

## HU-04 — Actualizar un equipo

**Como** responsable del laboratorio, **quiero** modificar un equipo **para** reflejar cambios de estado, datos o existencia.

### Criterios de aceptación

1. El formulario de edición presenta los valores actuales.
2. Se pueden guardar datos que cumplen las mismas reglas del registro.
3. El sistema muestra el detalle actualizado y una confirmación.
4. El código actual puede conservarse sin considerarse duplicado.

### Criterios de rechazo

1. No se permite cambiar el código por el de otro equipo.
2. No se guardan valores fuera de los límites definidos.
3. Si hay un error, el formulario conserva los valores introducidos y muestra el motivo.

### Escenarios automatizados

- Feliz: actualización de nombre, estado, cantidad y notas de `EQ-001`.
- Negativo: intento de asignar a `EQ-001` el código de `EQ-002`.
- Límite: actualización de cantidad a su máximo permitido, 9999.

## HU-05 — Eliminar un equipo

**Como** responsable del laboratorio, **quiero** eliminar un equipo obsoleto **para** evitar registros que ya no pertenecen al inventario.

### Criterios de aceptación

1. Antes de eliminar, se presenta una confirmación que identifica al equipo.
2. Al confirmar, el registro desaparece y se muestra un mensaje de éxito.
3. Al eliminar el último registro, se presenta un estado vacío con una acción clara.

### Criterios de rechazo

1. Al cancelar la confirmación, el equipo permanece sin cambios.
2. Una persona sin sesión no puede ejecutar la eliminación.
3. Una solicitud de eliminación inválida o sin token de seguridad es rechazada.

### Escenarios automatizados

- Feliz: eliminación confirmada de `EQ-002`.
- Negativo: cancelación de la eliminación de `EQ-001`.
- Límite: eliminación de todos los registros hasta dejar el inventario vacío.
