# Librerías que se utilizan en el proyecto
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from shiny import App, ui, render, reactive
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd

sns.set(style="whitegrid")

# Se cargan los datos 
patients = pd.read_csv("patients.csv", parse_dates=["arrival_date", "departure_date"])
services_weekly = pd.read_csv("services_weekly.csv")
staff = pd.read_csv("staff.csv")
staff_schedule = pd.read_csv("staff_schedule.csv")

# Calculo de algunas variables
patients["stay_days"] = (patients["departure_date"] - patients["arrival_date"]).dt.days
services_weekly["beds_used"] = services_weekly["patients_admitted"]

# Modelos pre-calculados
anova_model = smf.ols("beds_used ~ C(service)", data=services_weekly).fit()
anova_table = anova_lm(anova_model, typ=2)
tukey = pairwise_tukeyhsd(endog=services_weekly["beds_used"],
                          groups=services_weekly["service"], alpha=0.05)
tukey_df = pd.DataFrame(tukey.summary().data[1:], columns=tukey.summary().data[0])

satis_model = smf.ols("satisfaction ~ stay_days", data=patients).fit()
stay_age_model = smf.ols("stay_days ~ age", data=patients).fit()

pred_ages = pd.DataFrame({"age": [30, 45, 65, 80]})
pred_age_ci = stay_age_model.get_prediction(pred_ages).summary_frame(alpha=0.05)
pred_age_table = pd.concat(
    [pred_ages, pred_age_ci[["mean", "mean_ci_lower", "mean_ci_upper"]]], axis=1
)

# Parte visual UI
app_ui = ui.page_fluid(
    ui.h2("Proyecto Servicios Médicos - Análisis (Python Shiny)"),
    ui.navset_tab(
        ui.nav_panel(
            "Camas por servicio (ANOVA)",
            ui.layout_columns(
                ui.card(ui.h4("Medias e IC por servicio"), ui.output_plot("beds_plot")),
                ui.card(
                    ui.h4("ANOVA"), ui.output_table("anova_tbl"),
                    ui.h4("Tukey 95%"), ui.output_table("tukey_tbl")
                ),
            ),
        ),
        ui.nav_panel(
            "Satisfacción vs estadía",
            ui.layout_columns(
                ui.card(ui.output_plot("satis_plot")),
                ui.card(ui.h4("Regresión lineal"), ui.output_table("satis_model_tbl"))
            )
        ),
        ui.nav_panel(
            "Predicción estadía por edad",
            ui.layout_columns(
                ui.card(ui.h4("Modelo stay_days ~ age"), ui.output_text_verbatim("stay_age_summary")),
                ui.card(ui.h4("Predicciones fijas (IC 95%)"), ui.output_table("age_pred_tbl"))
            ),
            ui.card(
                ui.input_slider("edad", "Edad", min=0, max=100, value=50, step=1),
                ui.output_table("age_pred_dynamic"),
                ui.output_ui("age_plotly")  # Plotly interactivo
            )
        )
    )
)

# Parte mecánica (Server)
def server(input, output, session):
    @render.plot
    def beds_plot():
        fig, ax = plt.subplots()

       
        order = ["ICU", "emergency", "general_medicine", "surgery"]

        sns.boxplot(
            data=services_weekly,
            x="service",
            y="beds_used",
            order=order,
            ax=ax
        )

        ax.set_xlabel("Servicio")
        ax.set_ylabel("Camas usadas por semana")
        ax.set_title("Distribución de camas usadas por servicio")

        plt.tight_layout()
        return fig
     
    @render.table
    def anova_tbl():
        df = anova_table.reset_index().rename(columns={"index": "term"})
        numeric_cols = df.select_dtypes(include=[float, int]).columns
        df[numeric_cols] = df[numeric_cols].round(4)
        return df

    @render.table
    def tukey_tbl():
        df = tukey_df.copy()
        num_cols = df.select_dtypes(include=[float, int]).columns
        df[num_cols] = df[num_cols].round(3)
        return df

    @render.plot
    def satis_plot():
        fig, ax = plt.subplots()
        sns.scatterplot(data=patients, x="stay_days", y="satisfaction",
                        hue="service", alpha=0.5, ax=ax)
        sns.regplot(data=patients, x="stay_days", y="satisfaction",
                    scatter=False, ax=ax, color="black", lowess=True)
        ax.set_xlabel("Días de estadía")
        ax.set_ylabel("Satisfacción del paciente")
        plt.tight_layout()
        return fig

    @render.table
    def satis_model_tbl():
        selected = input.services_sel()
        df = patients[patients["service"].isin(selected)]

        model = smf.ols("satisfaction ~ stay_days * C(service)", data=df).fit()

        coef = (
            model.summary2()
            .tables[1]
            .reset_index()
            .rename(columns={"index": "term"})
        )

        num_cols = coef.select_dtypes(include=["float", "int"]).columns
        coef[num_cols] = coef[num_cols].round(3)

        return coef[["term", "Coef.", "Std.Err.", "t", "P>|t|"]]

    @render.text
    def stay_age_summary():
        return stay_age_model.summary().as_text()

    @render.table
    def age_pred_tbl():
        df = pred_age_table.copy()
        df.columns = ["edad", "pred_dias", "ci_inf", "ci_sup"]
        df[["pred_dias", "ci_inf", "ci_sup"]] = df[["pred_dias", "ci_inf", "ci_sup"]].round(2)
        return df

    @reactive.Calc
    def dynamic_age_pred():
        age_df = pd.DataFrame({"age": [input.edad()]})
        pred = stay_age_model.get_prediction(age_df).summary_frame(alpha=0.05)
        out = pd.concat([age_df, pred[["mean", "mean_ci_lower", "mean_ci_upper"]]], axis=1)
        out.columns = ["edad", "pred_dias", "ci_inf", "ci_sup"]
        out[["pred_dias", "ci_inf", "ci_sup"]] = out[["pred_dias", "ci_inf", "ci_sup"]].round(2)
        return out

    @render.table
    def age_pred_dynamic():
        return dynamic_age_pred()

    @render.ui
    def age_plotly():
        df = dynamic_age_pred()
        fig = px.scatter(
            df, x="edad", y="pred_dias",
            error_y=df["ci_sup"] - df["pred_dias"],
            error_y_minus=df["pred_dias"] - df["ci_inf"],
            labels={"edad": "Edad", "pred_dias": "Pred. días de estadía"},
            title="Predicción con IC 95% (Plotly)"
        )
        return ui.output_plot("plotly_dummy")  # placeholder; Shiny muestra fig abajo

    @render.plot
    def plotly_dummy():
        # Se usa sólo como placeholder; el gráfico real es el objeto Plotly devuelto arriba
        fig, ax = plt.subplots()
        ax.axis("off")
        return fig

app = App(app_ui, server)
