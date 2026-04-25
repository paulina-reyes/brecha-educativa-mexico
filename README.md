# Brecha educativa en México por entidad federativa 

**Autora:** Paulina Reyes García  
**Licenciatura en Ingeniería en IA**

---

## Descripción

Este proyecto presenta una narrativa visual interactiva sobre la relación entre el rezago social y distintos indicadores educativos en México a nivel estatal.

A través de visualizaciones desarrolladas con Dash y Plotly, se analiza cómo las condiciones sociales se asocian con:

- el analfabetismo  
- el abandono escolar  
- la escolaridad promedio  

---

## Fuentes de datos

- CONEVAL (2020). Índice de Rezago Social  
  👉 [Ver fuente](https://www.coneval.org.mx/Medicion/IRS/Paginas/Indice_de_Rezago_Social_2020_anexos.aspx)
  Consultado el: 22 de abril de 2026

- SEP (2022–2023). Indicadores educativos por entidad federativa  
  👉 [Ver fuente](https://siged.sep.gob.mx/SIGED/indicadores_entidad.html)
  Consultado el: 22 de abril de 2026

---

## Reproducibilidad

### 1. Descargar los datos

Descargar los archivos desde las fuentes oficiales: 32 reportes de la SEP(todos los estados) y el del coneval 

---

### 2. Colocar los archivos en las carpetas correspondientes

Los archivos deben organizarse en la carpeta de data de la siguiente manera:

```text
data/
├── coneval/
│   └── rezago_social.xlsx
├── sep/
│   ├── estadistica_e_indicadores_educativos_01AGS.xlsx
│   ├── estadistica_e_indicadores_educativos_02BC.xlsx
│   ├── ...

```
⚠️ Es importante respetar la estructura de carpetas para que el script funcione correctamente.

---

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```
---

### 4. Generar el dataset limpio

```bash
python limpieza_datos.py
```

Esto generará una solo archivo con las datos necesarios: data/clean/brecha_educativa_estados.csv

---

### 5. Ejecutar la aplicación
```bash
python app.py
```
Abrir en navegador: http://127.0.0.1:8050/

---

### 6. Despliegue

Aplicación desplegada en Render:

👉 [Pegar aquí tu link de Render]

