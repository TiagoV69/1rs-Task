Proyección de Población de Medellín

Características:

    Cálculo Predictivo: Estima la población para cualquier año futuro basado en parámetros iniciales.
    
    Cálculo de Hitos: Determina en qué año se alcanzará una población objetivo.

    Visualización de Datos: Genera gráficos dinámicos de la proyección poblacional y del cruce con objetivos, gracias a la integración con Matplotlib.

    Interfaz Gráfica Intuitiva: Construida con Tkinter para una fácil interacción del usuario.

 Estructura del Proyecto:

  El código está organizado de manera modular para separar responsabilidades, siguiendo las buenas prácticas de la ingeniería de software:

    main.py: El punto de entrada de la aplicación. Su única función es iniciar la interfaz.

    modelo.py: Contiene toda la lógica de negocio y los cálculos matemáticos puros. No tiene dependencias de la interfaz gráfica.

    vista.py: Define y construye toda la interfaz de usuario con Tkinter, incluyendo las ventanas, botones y gráficos.

  Instalación y Puesta en Marcha:

Para ejecutar este proyecto en tu máquina local, sigue estos pasos.

1. Requisitos Previos
Asegúrate de tener instalado Python 3.7 o una versión superior.

2. Guía de Instalación
  * Clona el repositorio en tu máquina local
  * Navega al directorio del proyecto
  * Como recomendación activa un entorno virtual para aislar las dependencias del proyecto
  * IMPORTANTE: Se requiere instalar la libreria de Matplotlib, sin esto las funciones de graficacion de la aplicación NO FUNCIONARAN si no esta instalada

  Cómo Ejecutar la Aplicación

    Una vez que hayas completado la instalación, puedes iniciar la aplicación ejecutando el archivo main.py:
