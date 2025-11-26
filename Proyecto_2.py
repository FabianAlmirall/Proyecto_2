# Librerías
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

# Datos
patients = pd.read_csv("patients.csv", parse_dates=["arrival_date", "departure_date"])
services_weekly = pd.read_csv("services_weekly.csv")
staff = pd.read_csv("staff.csv")
staff_schedule = pd.read_csv("staff_schedule.csv")

# Variables nuevas
patients["stay_days"] = (patients["departure_date"] - patients["arrival_date"]).dt.days
services_weekly["beds_used"] = services_weekly["patients_admitted"]

# Modelo para ANOVA
anova_model = smf.ols("beds_used ~ C(service)", data=services_weekly).fit()
anova_table = anova_lm(anova_model, typ=2)
tukey = pairwise_tukeyhsd(
    endog=services_weekly["beds_used"],
    groups=services_weekly["service"],
    alpha=0.05,
)
tukey_df = pd.DataFrame(tukey.summary().data[1:], columns=tukey.summary().data[0])

# UI
app_ui = ui.page_fluid(
    ui.h2("Proyecto Camas de hospital - Análisis estadístico por Justin y Fabián"),
    ui.navset_tab(
        # Tab 1: ANOVA
        ui.nav_panel(
            "Camas por servicio (ANOVA)",
            ui.layout_columns(
                ui.card(ui.h4("Medias e IC por servicio"), ui.output_plot("beds_plot")),
                ui.card(
                    ui.h4("ANOVA"),
                    ui.output_table("anova_tbl"),
                    ui.h4("Tukey 95%"),
                    ui.output_table("tukey_tbl"),
                ),
            ),
        ),
        # Tab 2: satisfacción vs estadía
        ui.nav_panel(
            "Satisfacción vs estadía",
            ui.layout_columns(
                ui.card(
                    ui.input_selectize(
                        "services_sel",
                        "Seleccione servicios:",
                        choices=sorted(patients["service"].unique()),
                        selected=sorted(patients["service"].unique()),
                        multiple=True,
                    ),
                    ui.output_plot("satis_plot"),
                ),
                ui.card(
                    ui.h4("Regresión lineal"),
                    ui.output_table("satis_model_tbl"),
                ),
            ),
        ),
        # Tab 3: gráfico de líneas de solicitudes de pacientes
        ui.nav_panel(
            "Solicitudes de pacientes",
            ui.card(
                ui.h4("Solicitudes de pacientes por semana y servicio"),
                ui.output_plot("requests_line_plot"),
            ),
        ),
    ),
)

# Server
def server(input, output, session):
    # Tab 1: ANOVA
    @render.plot
    def beds_plot():
        fig, ax = plt.subplots()
        order = ["ICU", "emergency", "general_medicine", "surgery"]

        sns.boxplot(
            data=services_weekly,
            x="service",
            y="beds_used",
            order=order,
            ax=ax,
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

    # Tab 2: satisfacción vs estadía
    @render.plot
    def satis_plot():
        selected = input.services_sel()
        df = patients[patients["service"].isin(selected)]

        model = smf.ols("satisfaction ~ stay_days * C(service)", data=df).fit()

        fig, ax = plt.subplots()

        sns.scatterplot(
            data=df,
            x="stay_days",
            y="satisfaction",
            hue="service",
            alpha=0.5,
            ax=ax,
        )

        for serv in selected:
            temp = df[df["service"] == serv]
            x_vals = np.linspace(temp["stay_days"].min(), temp["stay_days"].max(), 50)
            new_data = pd.DataFrame(
                {"stay_days": x_vals, "service": [serv] * len(x_vals)}
            )
            y_hat = model.predict(new_data)
            ax.plot(x_vals, y_hat, linewidth=2)

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

    # Tab 3: línea de solicitudes de pacientes
    @render.plot
    def requests_line_plot():
        fig, ax = plt.subplots()

        df = services_weekly.sort_values(["week", "service"])

        sns.lineplot(
            data=df,
            x="week",
            y="patients_request",
            hue="service",
            marker="o",
            ax=ax,
        )

        ax.set_xlabel("Semana del año")
        ax.set_ylabel("Solicitudes de pacientes")
        ax.set_title("Solicitudes de pacientes por servicio a lo largo del año")
        ax.legend(title="Servicio")
        plt.tight_layout()
        return fig

app = App(app_ui, server)
