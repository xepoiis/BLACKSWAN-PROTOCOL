# Black-Swan Protocol: Malla de Alerta Cautiva Off-Grid

Sistema integral de alerta temprana y evacuación diseñado para comunidades rurales colindantes a zonas forestales. Este proyecto simula un ecosistema de telecomunicaciones "Zero-Install" que funciona de manera 100% independiente de la red de internet, garantizando la comunicación durante emergencias donde la infraestructura tradicional colapsa.

## Descripción del Proyecto

El sistema resuelve dos problemáticas críticas en zonas rurales durante incendios:
1. **La Desinformación y Falsas Alarmas:** Requiere validación humana (PIN de seguridad por parte de un dirigente) antes de emitir cualquier alerta, evitando el pánico por errores de sensores automatizados.
2. **La Brecha Tecnológica bajo Estrés:** Utiliza un Portal Cautivo (DNS Sinkhole). Al activarse la alarma, los vecinos se conectan a una red Wi-Fi de emergencia abierta y el sistema "secuestra" sus navegadores para mostrar automáticamente la ruta de evacuación, sin requerir descarga de apps ni plan de datos.

## Arquitectura de Software

El proyecto sigue una estructura modular limpia (MVC) desarrollada en Python, diseñada para ser altamente compatible (testeada en entornos Windows 7/10/11):

* **`app.py` (Frontend / Nodo Maestro):** Interfaz gráfica (GUI) construida con Tkinter que actúa como terminal de validación física para el dirigente vecinal.
* **`servidor.py` (Backend / Controlador):** Servidor HTTP TCP local que intercepta peticiones simulando un DNS Sinkhole para distribuir el portal de emergencia.
* **`index.html` (Vista / Portal Cautivo):** Interfaz web responsiva "Zero-Dependency" (sin llamadas a librerías externas en la nube) que despliega el mapa SVG vectorizado con la ruta de evacuación.

## Instrucciones de Despliegue (Simulacro Local)

Para ejecutar este simulador en un entorno de pruebas o presentación académica:

### 1. Requisitos Previos
* Python 3.x instalado en el equipo host.
* Los archivos `app.py`, `servidor.py` e `index.html` en el mismo directorio.
* Tarjeta de red inalámbrica (o anclaje de red USB mediante un smartphone).

### 2. Levantar la Red Local
1. En el equipo host, active la opción **Zona con cobertura inalámbrica móvil** (Mobile Hotspot).
2. Configure el nombre de red (SSID) como `ALERTA`.

### 3. Ejecución
1. Abra una terminal en el directorio del proyecto y ejecute:
   ```bash
   python app.py

    En la interfaz gráfica del Nodo Maestro, ingrese el PIN de seguridad del dirigente (1234).

    El sistema levantará el servidor web en segundo plano y arrojará la dirección IP local asignada.

### 4. Prueba de Cliente
* Conecte un dispositivo móvil a la red Wi-Fi ALERTA.
* Abra el navegador web e ingrese la IP arrojada por el sistema.
* El dispositivo mostrará la interfaz de evacuación oficial.

Autor y Contexto

Proyecto desarrollado como propuesta de innovación tecnológica e infraestructura de redes.
