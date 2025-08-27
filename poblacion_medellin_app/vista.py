import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont

# Importamos toda la lógica de negocio desde nuestro nuevo módulo 'modelo'
import modelo as mdl

# Soporte opcional de gráficos con Matplotlib
try:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    MPL_AVAILABLE = True
except ImportError:
    MPL_AVAILABLE = False


class PopulationApp(ttk.Frame):
    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master, padding=16)
        self.master.title("Población de Medellín — Modelo Geométrico")
        self.master.geometry("880x520")
        self.master.minsize(820, 460)
        try:
            self.master.iconbitmap(default=None)
        except Exception:
            pass

        self._build_style()
        self._build_widgets()

    def _build_style(self) -> None:
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        try:
            default_font = tkfont.nametofont("TkDefaultFont")
            text_font = tkfont.nametofont("TkTextFont")
            heading_font = tkfont.nametofont("TkHeadingFont")
            menu_font = tkfont.nametofont("TkMenuFont")
            default_font.configure(size=14)
            text_font.configure(size=14)
            heading_font.configure(size=16, weight="bold")
            menu_font.configure(size=14)
        except Exception:
            pass

        style.configure("TFrame", background="#FFFFFF")
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#0F5132", background="#FFFFFF")
        style.configure("Hint.TLabel", foreground="#444444", background="#FFFFFF", font=("Segoe UI", 14))
        style.configure("Result.TLabel", font=("Segoe UI", 15, "bold"), foreground="#1F2937", background="#FFFFFF")
        style.configure("Card.TLabelframe", background="#FFFFFF", padding=12)
        style.configure("Card.TLabelframe.Label", font=("Segoe UI", 14, "bold"), foreground="#111827", background="#FFFFFF")
        style.configure("TButton", padding=8)
        style.configure("Accent.TButton", padding=9, foreground="#FFFFFF", background="#2563EB")
        style.map(
            "Accent.TButton",
            background=[("active", "#1D4ED8"), ("pressed", "#1E40AF")],
            relief=[("pressed", "sunken"), ("!pressed", "raised")],
        )

    def _build_widgets(self) -> None:
        header = ttk.Label(
            self,
            text=(
                "Modelo geométrico:  P(n) = P0 · (1 + r)^n   con  "
                f"P0 = {mdl.INITIAL_POPULATION_MILLIONS} millones,  r = {mdl.ANNUAL_GROWTH_RATE*100:.0f}% anual,  "
                f"n = año − {mdl.BASE_YEAR}"
            ),
            style="Header.TLabel",
            wraplength=820,
            justify="center",
        )
        header.grid(row=0, column=0, columnspan=2, sticky="we", pady=(0, 12))

        hint = ttk.Label(
            self,
            text=(
                "Ingrese un año para estimar la población, o una población objetivo (en millones) "
                "para estimar el año en que se alcanzará/superará."
            ),
            style="Hint.TLabel",
            wraplength=820,
            justify="center",
        )
        hint.grid(row=1, column=0, columnspan=2, sticky="we", pady=(0, 12))

        left = ttk.Frame(self)
        right = ttk.Frame(self)
        left.grid(row=2, column=0, sticky="nsew", padx=(0, 8))
        right.grid(row=2, column=1, sticky="nsew", padx=(8, 0))

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self._build_year_to_population(left)
        self._build_population_to_year(right)

        self.pack(fill="both", expand=True)

        charts_container = ttk.Frame(self)
        charts_container.grid(row=3, column=0, columnspan=2, sticky="nsew")
        self.rowconfigure(3, weight=2)
        self._build_charts(charts_container)

    def _build_year_to_population(self, parent: ttk.Frame) -> None:
        card = ttk.LabelFrame(parent, text="Calcular población para un año dado", style="Card.TLabelframe")
        card.pack(fill="both", expand=True)

        row = ttk.Frame(card)
        row.pack(fill="x", padx=10, pady=(10, 4))
        ttk.Label(row, text=f"Año (≥ {mdl.BASE_YEAR}):").pack(side="left")
        self.year_var = tk.StringVar(value=str(mdl.BASE_YEAR + 7))
        year_entry = ttk.Entry(row, textvariable=self.year_var, width=18)
        year_entry.pack(side="left", padx=(8, 0))

        btn = ttk.Button(card, text="Calcular población", command=self._on_calculate_population, style="Accent.TButton")
        btn.pack(anchor="w", padx=10, pady=6)

        self.population_result_var = tk.StringVar(value="")
        res = ttk.Label(card, textvariable=self.population_result_var, style="Result.TLabel")
        res.pack(fill="x", padx=10, pady=(0, 12))

    def _build_population_to_year(self, parent: ttk.Frame) -> None:
        card = ttk.LabelFrame(parent, text="Calcular año para alcanzar/superar una población objetivo", style="Card.TLabelframe")
        card.pack(fill="both", expand=True)

        row = ttk.Frame(card)
        row.pack(fill="x", padx=10, pady=(10, 4))
        ttk.Label(row, text="Objetivo (millones):").pack(side="left")
        self.target_var = tk.StringVar(value="4.0")
        target_entry = ttk.Entry(row, textvariable=self.target_var, width=18)
        target_entry.pack(side="left", padx=(8, 0))

        self.strict_var = tk.BooleanVar(value=False)
        strict_chk = ttk.Checkbutton(
            card,
            text="Exigir superar estrictamente (>)",
            variable=self.strict_var,
        )
        strict_chk.pack(anchor="w", padx=10, pady=2)

        btn = ttk.Button(card, text="Calcular año", command=self._on_calculate_year, style="Accent.TButton")
        btn.pack(anchor="w", padx=10, pady=6)

        self.year_result_var = tk.StringVar(value="")
        res = ttk.Label(card, textvariable=self.year_result_var, style="Result.TLabel")
        res.pack(fill="x", padx=10, pady=(0, 12))

    def _build_charts(self, parent: ttk.Frame) -> None:
        card = ttk.LabelFrame(parent, text="Gráficas", style="Card.TLabelframe")
        card.pack(fill="both", expand=True, padx=0, pady=(8, 0))

        if not MPL_AVAILABLE:
            ttk.Label(
                card,
                text=("Para visualizar gráficas, instale Matplotlib:\npip install matplotlib"),
                style="Hint.TLabel",
                justify="center",
            ).pack(fill="x", padx=12, pady=12)
            return

        nb = ttk.Notebook(card)
        nb.pack(fill="both", expand=True)

        tab_proj = ttk.Frame(nb)
        nb.add(tab_proj, text="Proyección por años")
        controls_proj = ttk.Frame(tab_proj)
        controls_proj.pack(fill="x", padx=12, pady=(10, 0))
        ttk.Label(controls_proj, text=f"Desde año (≥ {mdl.BASE_YEAR}):").pack(side="left")
        self.proj_start_var = tk.StringVar(value=str(mdl.BASE_YEAR))
        ttk.Entry(controls_proj, textvariable=self.proj_start_var, width=10).pack(side="left", padx=(6, 12))
        ttk.Label(controls_proj, text="Hasta año:").pack(side="left")
        self.proj_end_var = tk.StringVar(value=str(mdl.BASE_YEAR + 20))
        ttk.Entry(controls_proj, textvariable=self.proj_end_var, width=10).pack(side="left", padx=(6, 12))
        ttk.Button(controls_proj, text="Actualizar gráfica", command=self._draw_projection_chart, style="Accent.TButton").pack(side="left")

        self.fig_projection = Figure(figsize=(6.8, 3.2), dpi=100)
        self.ax_projection = self.fig_projection.add_subplot(111)
        self.canvas_projection = FigureCanvasTkAgg(self.fig_projection, master=tab_proj)
        self.canvas_projection.get_tk_widget().pack(fill="both", expand=True, padx=12, pady=12)

        tab_target = ttk.Frame(nb)
        nb.add(tab_target, text="Cruce con objetivo")
        controls_target = ttk.Frame(tab_target)
        controls_target.pack(fill="x", padx=12, pady=(10, 0))
        ttk.Label(controls_target, text="Usa el campo 'Objetivo (millones)' de la derecha y pulsa 'Calcular año'.").pack(side="left")
        ttk.Button(controls_target, text="Actualizar con objetivo", command=self._draw_target_chart, style="Accent.TButton").pack(side="right")

        self.fig_target = Figure(figsize=(6.8, 3.2), dpi=100)
        self.ax_target = self.fig_target.add_subplot(111)
        self.canvas_target = FigureCanvasTkAgg(self.fig_target, master=tab_target)
        self.canvas_target.get_tk_widget().pack(fill="both", expand=True, padx=12, pady=12)

        self._draw_projection_chart()
        self._draw_target_chart()

    def _draw_projection_chart(self) -> None:
        if not MPL_AVAILABLE:
            return
        try:
            start_year = int(self.proj_start_var.get().strip())
            end_year = int(self.proj_end_var.get().strip())
            if start_year < mdl.BASE_YEAR:
                raise ValueError(f"El año inicial debe ser ≥ {mdl.BASE_YEAR}.")
            if end_year < start_year:
                raise ValueError("El año final debe ser ≥ al inicial.")

            years = list(range(start_year, end_year + 1))
            populations_m = [mdl.compute_population_for_year(y) / 1_000_000.0 for y in years]

            self.ax_projection.clear()
            self.ax_projection.plot(years, populations_m, color="#2563EB", linewidth=2)
            self.ax_projection.scatter([years[0], years[-1]], [populations_m[0], populations_m[-1]], color="#1F2937")
            self.ax_projection.set_title("Proyección de población (millones)")
            self.ax_projection.set_xlabel("Año")
            self.ax_projection.set_ylabel("Población (millones)")
            self.ax_projection.grid(True, linestyle=":", alpha=0.5)
            self.fig_projection.tight_layout()
            self.canvas_projection.draw()
        except ValueError as exc:
            messagebox.showerror("Entrada inválida", str(exc))
        except Exception as exc:
            messagebox.showerror("Error", f"Ocurrió un error al graficar: {exc}")

    def _draw_target_chart(self) -> None:
        if not MPL_AVAILABLE:
            return
        try:
            target_str = self.target_var.get().strip().replace(",", ".")
            target_m = float(target_str) if target_str else None

            if target_m is not None and target_m > 0:
                year_cross = mdl.compute_year_to_reach_population(target_m, strictly_greater=bool(self.strict_var.get()))
                end_year = max(mdl.BASE_YEAR + 2, year_cross + 2)
            else:
                end_year = mdl.BASE_YEAR + 10

            years = list(range(mdl.BASE_YEAR, end_year + 1))
            populations_m = [mdl.compute_population_for_year(y) / 1_000_000.0 for y in years]

            self.ax_target.clear()
            self.ax_target.plot(years, populations_m, color="#10B981", linewidth=2)
            self.ax_target.set_title("Población y objetivo (millones)")
            self.ax_target.set_xlabel("Año")
            self.ax_target.set_ylabel("Población (millones)")
            self.ax_target.grid(True, linestyle=":", alpha=0.5)

            if target_m is not None and target_m > 0:
                self.ax_target.axhline(y=target_m, color="#DC2626", linestyle="--", linewidth=1.5, label=f"Objetivo: {target_m:g}M")
                year_cross = mdl.compute_year_to_reach_population(target_m, strictly_greater=bool(self.strict_var.get()))
                self.ax_target.axvline(x=year_cross, color="#F59E0B", linestyle=":", linewidth=1.5, label=f"Año: {year_cross}")
                p_cross_people = mdl.compute_population_for_year(year_cross)
                self.ax_target.scatter([year_cross], [p_cross_people / 1_000_000.0], color="#111827")
                self.ax_target.legend(loc="best")

            self.fig_target.tight_layout()
            self.canvas_target.draw()
        except ValueError as exc:
            messagebox.showerror("Entrada inválida", str(exc))
        except Exception as exc:
            messagebox.showerror("Error", f"Ocurrió un error al graficar: {exc}")

    def _on_calculate_population(self) -> None:
        try:
            year_str = self.year_var.get().strip()
            if not year_str:
                raise ValueError("Debe ingresar un año.")
            year = int(year_str)
            population_people = mdl.compute_population_for_year(year)
            formatted_millions = mdl.format_people_to_millions(population_people)
            self.population_result_var.set(f"Población estimada en {year}: {formatted_millions}")
            if MPL_AVAILABLE:
                try:
                    self.proj_start_var.set(str(mdl.BASE_YEAR))
                    self.proj_end_var.set(str(max(year, mdl.BASE_YEAR)))
                    self._draw_projection_chart()
                except Exception:
                    pass
        except ValueError as exc:
            messagebox.showerror("Entrada inválida", str(exc))
        except Exception as exc:
            messagebox.showerror("Error", f"Ocurrió un error: {exc}")

    def _on_calculate_year(self) -> None:
        try:
            target_str = self.target_var.get().strip().replace(",", ".")
            if not target_str:
                raise ValueError("Debe ingresar una población objetivo en millones.")
            target_millions = float(target_str)
            strictly = bool(self.strict_var.get())
            year = mdl.compute_year_to_reach_population(target_millions, strictly_greater=strictly)
            mode = ">" if strictly else "≥"
            self.year_result_var.set(f"Se alcanza con P {mode} {target_millions:g} millones en el año {year}.")
            if MPL_AVAILABLE:
                try:
                    self._draw_target_chart()
                except Exception:
                    pass
        except ValueError as exc:
            messagebox.showerror("Entrada inválida", str(exc))
        except Exception as exc:
            messagebox.showerror("Error", f"Ocurrió un error: {exc}")