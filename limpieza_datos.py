import pandas as pd
import os
import unicodedata

coneval_path = "data/coneval/rezago_social.xlsx"
ruta_sep = "data/sep/"
salida = "data/clean/brecha_educativa_estados.csv"

os.makedirs("data/clean", exist_ok=True)

def normalizar(texto):
    texto = str(texto).strip()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return texto.lower()


def leer_hoja_indicadores(path):
    xls = pd.ExcelFile(path)

    for hoja in xls.sheet_names:
        df = pd.read_excel(path, sheet_name=hoja, header=None)
        contenido = df.astype(str).to_string()

        if "Indicadores educativos" in contenido and "Nivel Educativo / Indicador" in contenido:
            return df

    return None


def extraer_abandono(df, nombre_nivel):
    columna = df.iloc[:, 0].astype(str)

    idx_nivel = df[
        columna.str.contains(nombre_nivel, case=False, na=False)
    ].index

    if len(idx_nivel) == 0:
        return None

    inicio = idx_nivel[0]
    bloque = df.iloc[inicio:inicio + 15]

    fila_abandono = bloque[
        bloque.iloc[:, 0].astype(str).str.contains(
            "Abandono escolar",
            case=False,
            na=False
        )
    ]

    if fila_abandono.empty:
        return None

    # Columna 4 - dato estatal 2022-2023
    return fila_abandono.iloc[0, 4]


# 1. CONEVAL
df_coneval_raw = pd.read_excel(coneval_path, header=None)
df_coneval = df_coneval_raw.iloc[7:, [1, 3, 14, 15]].copy()

df_coneval.columns = [
    "estado",
    "analfabetismo",
    "rezago_social",
    "grado_rezago_social"
]

df_coneval = df_coneval[df_coneval["estado"].notna()]
df_coneval = df_coneval[df_coneval["estado"] != "Nacional"]

df_coneval["estado_key"] = df_coneval["estado"].apply(normalizar)

df_coneval["analfabetismo"] = pd.to_numeric(
    df_coneval["analfabetismo"],
    errors="coerce"
)

df_coneval["rezago_social"] = pd.to_numeric(
    df_coneval["rezago_social"],
    errors="coerce"
)

# 2. SEP
datos_sep = []

for archivo in os.listdir(ruta_sep):

    if archivo.endswith(".xlsx"):
        path = os.path.join(ruta_sep, archivo)

        df = leer_hoja_indicadores(path)

        texto_archivo = df.astype(str).to_string()
        estado = None

        estados_ordenados = sorted(
            df_coneval["estado"].tolist(),
            key=len,
            reverse=True
        )

        for edo in estados_ordenados:
            if edo in texto_archivo:
                estado = edo
                break

        abandono_primaria = extraer_abandono(df, "Educación primaria")
        abandono_secundaria = extraer_abandono(df, "Educación secundaria")
        abandono_media_superior = extraer_abandono(df, "Educación media superior")
        abandono_superior = extraer_abandono(df, "Educación superior")

        columna = df.iloc[:, 0].astype(str)

        fila_escolaridad = df[
            columna.str.contains(
                "Grado promedio de escolaridad",
                case=False,
                na=False
            )
        ]

        escolaridad_promedio = None

        if not fila_escolaridad.empty:
            escolaridad_promedio = fila_escolaridad.iloc[0, 4]

        datos_sep.append({
            "estado": estado,
            "estado_key": normalizar(estado),
            "abandono_primaria": abandono_primaria,
            "abandono_secundaria": abandono_secundaria,
            "abandono_media_superior": abandono_media_superior,
            "abandono_superior": abandono_superior,
            "escolaridad_promedio": escolaridad_promedio
        })


df_sep = pd.DataFrame(datos_sep)

for col in [
    "abandono_primaria",
    "abandono_secundaria",
    "abandono_media_superior",
    "abandono_superior",
    "escolaridad_promedio"
]:
    df_sep[col] = pd.to_numeric(df_sep[col], errors="coerce")


# 3. UNIR
df_final = pd.merge(
    df_coneval,
    df_sep[
        [
            "estado_key",
            "abandono_primaria",
            "abandono_secundaria",
            "abandono_media_superior",
            "abandono_superior",
            "escolaridad_promedio"
        ]
    ],
    on="estado_key",
    how="inner"
)

df_final = df_final.drop(columns=["estado_key"])

# Redondear
df_final = df_final.round({
    "analfabetismo": 1,
    "rezago_social": 3,
    "abandono_primaria": 1,
    "abandono_secundaria": 1,
    "abandono_media_superior": 1,
    "abandono_superior": 1,
    "escolaridad_promedio": 1
})

df_final = df_final.dropna()

df_final = df_final.sort_values(
    by="rezago_social",
    ascending=False
)

# Guardar
df_final.to_csv(salida, index=False, encoding="utf-8-sig")


