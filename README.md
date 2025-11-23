# Proyecto de Programación 2

**Desarrolladores:**

- Fabián Almirall Marchena
- Justin Zhu Fan

## 1. Introducción 
La adecuada gestión de camas hospitalarias es un elemento clave para garantizar una atención médica eficiente y oportuna. En hospitales de tamaño mediano, la distribución de camas, la asignación de personal y el flujo de pacientes representan desafíos constantes que pueden afectar la calidad del servicio y la disponibilidad de recursos. Por ello, el análisis de datos se convierte en una herramienta fundamental para comprender y optimizar estos procesos.

Este proyecto se basa en un conjunto de datos sintético que simula las operaciones reales de un hospital, incorporando información sobre personal, pacientes, servicios y horarios. A partir de estos datos, se busca analizar el comportamiento de la demanda hospitalaria y la utilización de camas entre distintos servicios, con el fin de identificar patrones, posibles cuellos de botella y oportunidades de mejora en la administración de los recursos hospitalarios.

## 2. Justificación 

En la actualidad, la gestión de camas de hospitales es un aspecto clave para garantizar una atención oportuna y eficiente a los pacientes, especialmente ante el aumento de la demanda de servicios de salud y las limitaciones de recursos. En Costa Rica, la salud ha tenido problemas administrativos, como por ejemplo la falta de infraestructura en los centros de salud. Por ello, la aplicación de la estadística en este campo puede ayudar a garantizar un mejor funcionamiento de estos centros.

Por ende, el proyecto Camas de hospitales toma como base la teoría estadística y las herramientas de programación para aplicar un análisis sólido a partir de una base de datos sobre camas de hospitales, y así obtener resultados que permitan una toma de decisiones más adecuada en el manejo de dichas camas.

## 3. Selección de la base de datos

Para este proyecto se seleccionó el conjunto de datos “Hospital Beds Management” de Kaggle porque ofrece información estructurada y detallada sobre procesos clave de un hospital: ingreso de pacientes, servicios, uso de camas, dotación de personal y horarios.

Desde el punto de vista estadístico, esta base de datos es adecuada porque:

Contiene variables cuantitativas y categóricas, lo que permite aplicar técnicas descriptivas (tablas, gráficos, medidas de resumen) y comparativas (ANOVA, pruebas de hipótesis entre grupos, etc.).

Incluye información a nivel individual (pacientes y personal) y a nivel agregado (servicio semanal), lo que facilita análisis por niveles, como comparación entre servicios, semanas o tipos de pacientes.

La estructura de los datos permite plantear modelos de regresión para estudiar factores asociados al uso de camas, duración de la estancia o demanda de servicios.

Al ser un conjunto de datos sintético, se puede trabajar libremente sin restricciones de confidencialidad, manteniendo un escenario realista para la práctica de análisis en gestión hospitalaria.

Estas características hacen que la base sea pertinente para los objetivos del proyecto, centrados en analizar y modelar el comportamiento de variables relacionadas con la administración de camas hospitalarias.

## 4. Descripción de la base de datos

El conjunto de datos está compuesto por cuatro archivos en formato CSV, los cuales representan diferentes dimensiones operativas del hospital:

hospital_staff: Contiene información del personal hospitalario, incluyendo su identificación, rol, departamento y otros datos relevantes para el análisis de la dotación de recursos humanos.

hospital_patients: Registra datos relacionados con los pacientes, tales como información básica, fechas de ingreso, servicios asignados y estado de hospitalización.

hospital_service_weekly: Presenta datos semanales a nivel de servicio, permitiendo analizar el uso de camas, la demanda de pacientes y el rendimiento de cada área médica.

hospital_staff_schedule: Incluye los horarios semanales del personal, lo que facilita estudiar la relación entre la disponibilidad de trabajadores y la atención brindada.

En conjunto, estas bases permiten explorar la interacción entre el flujo de pacientes, la asignación de camas y la gestión del personal, proporcionando una estructura sólida para realizar análisis estadísticos orientados a la optimización de recursos y a la mejora en la toma de decisiones en el contexto hospitalario.

## 5. Objetivos

El proyecto tiene los siguientes objetivos:Observar la menor satisfacción de los pacientes durante el tiempo de estadía en el centro médico.

Predecir el tiempo de estadía de los pacientes según la edad de los mismos.

### 5.1 Objetivo General 

Analizar el comportamiento de diferentes variables referentes al manejo de camas de hospitales a través de una aplicación de Shiny.

### 5.2 Objetivos Específicos

1- Realizar un análisis de varianza sobre los servicios médicos que requieren camas de hospitales.

2- Observar la satisfacción de los pacientes durante el tiempo de estadía en el centro médico.

3- Predecir el tiempo de estadía de los pacientes según la edad de los mismos.

## 6. Preguntas 

En relación con los objetivos propuestos, la app de shiny debe dar respuesta a las siguientes preguntas.

¿Hay diferencias entre la cantidad de camas usadas según el servicio médico? Agregar intervalos de confianza.

¿Cómo se comporta la satisfacción de los pacientes según su tiempo de estadía?

¿Cuánto es el tiempo de estadía de un paciente de 30,45,65 y 80 años? Agregar intervalos de confianza.

## 7. Metodología 


## 8. Resultados 

## 9. Conclusiones


