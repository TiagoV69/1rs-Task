import tkinter as tk

# importamos el modulo de vista para tener la interfaz del ejercicio
from vista import PopulationApp 

# --- Punto de Entrada Principal ---
# OJITOOO: es el archivo principal que se debe ejecutar.
# Su responsabilidad es crear la ventana y la instancia de la aplicacion.

def main() -> None:
    """Configura y ejecuta la aplicación de Tkinter."""
    root = tk.Tk()

    # Mejora opcional de escala de DPI en Windows
    try:
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)
    except (ImportError, AttributeError):
        pass

    # Crea la aplicacion y la ejecuta
    app = PopulationApp(root)
    app.mainloop()


if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()