# Automatización de Plantillas para Metrología 📊⚡

Una aplicación de escritorio diseñada para automatizar la creación de plantillas de calibración de multímetros y pinzas amperimétricas, optimizando el flujo de trabajo en laboratorios de metrología.

## 🔥 Problema vs. Solución

* **Antes:** Los metrólogos ingresaban manualmente los datos de interpolación, las especificaciones del patrón (`show_spec`) y los decimales correspondientes en archivos de Excel.
* **Ahora:** Los datos están centralizados en una base de datos SQLite3. El programa consulta los rangos automáticamente, modifica una plantilla base conservando logos/estilos y oculta las filas que no se utilizan.

## ✨ Características Principales

* **Compatibilidad Total:** No altera el diseño ni la estructura de las plantillas a las que los metrólogos ya están acostumbrados.
* **Base de Datos Centralizada:** Gestión de especificaciones (`show_spec`) e Interpolacion.
* **Automatización Inteligente:** Inserción automática de interpolaciones y formatos de decimales según el rango medido.
* **Lógica de Limpieza:** Oculta dinámicamente las filas no utilizadas de Hoja de datos de medicion ().
* **Interfaz Gráfica (UI):** Desarrollada con CustomTkinter para una experiencia de usuario moderna e intuitiva.
* **Panel de Administración:** Permite crear nuevas plantillas e ingresar nuevos patrones (`show_spec`) a la base de datos de forma visual.

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.x
* **Interfaz Gráfica:** CustomTkinter
* **Base de Datos:** SQLite3
* **Manipulación de Plantillas:** OpenPyXL


