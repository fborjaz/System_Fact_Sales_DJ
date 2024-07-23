# 🎁 Sistema de Gestión de Ventas 🏬

✨ **Descripción**

¡Bienvenido al proyecto **Sistema de Gestión de Ventas**! 🛒

El objetivo principal de este proyecto es desarrollar un sistema integral de gestión de ventas utilizando el paradigma de programación orientada a objetos (POO) en Python. El sistema está diseñado para permitir a las empresas registrar, administrar y analizar de manera eficiente toda la información relacionada con sus procesos de ventas, incluyendo productos, clientes, facturas y reportes. Este sistema no solo optimiza la gestión interna, sino que también proporciona herramientas analíticas para mejorar la toma de decisiones.

🚀 **Características Principales**

* **Productos:** 📦 Agrega, edita y elimina productos con facilidad. Incluye detalles como imágenes, descripciones, precios y stock.
* **Marcas:** 🏷️ Organiza tus productos por marcas reconocidas para una mejor gestión y visualización.
* **Proveedores:** 🤝 Mantén un registro completo de tus proveedores, con información de contacto y detalles relevantes.
* **Categorías:** 🗂️ Clasifica tus productos en categorías para facilitar la búsqueda y la organización.
* **Autenticación:** 🔐 Protege el acceso a las funciones de administración con un sistema seguro de registro e inicio de sesión.

🛠️ **Tecnologías Utilizadas**

*   **Backend:**
    *   **Django:** El potente framework web de Python que impulsa la aplicación.
    *   **PostgreSQL:** Base de datos robusta y eficiente para almacenar los datos de eventos y participantes.
*   **Frontend:**
    *   **HTML, CSS, JavaScript:** Lenguajes esenciales para construir la interfaz de usuario.
    *   **Font Awesome:** Biblioteca de iconos para añadir elementos visuales atractivos.
    *   **

## ⚙️ Cómo Ejecutar la Aplicación

**Prerrequisitos:**

*   **Python:** Asegúrate de tener Python instalado en tu sistema. Puedes descargarlo desde [https://www.python.org/](https://www.python.org/).
*   **PostgreSQL:** Descarga e instala PostgreSQL desde [https://www.postgresql.org/](https://www.postgresql.org/).
    *   **Configuración:**
        *   Crea una base de datos para el proyecto.
        *   Crea un usuario y otorga los permisos necesarios sobre la base de datos.
        *   Actualiza el archivo `settings.py` de Django con la información de conexión a tu base de datos:

            ```python
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME': 'tu_base_de_datos',  # Reemplaza con el nombre de tu base de datos
                    'USER': 'tu_usuario',        # Reemplaza con tu usuario de PostgreSQL
                    'PASSWORD': 'tu_contraseña',  # Reemplaza con tu contraseña
                    'HOST': 'localhost',
                    'PORT': '5432',
                }
            }
            ```

**Pasos:**

1.  **Clonar el repositorio:**

    ```bash
    git clone https://github.com/fborjaz/System_Fact_Sales_DJ.git
    cd proy_sales
    ```

2.  **Crear (o activar) un entorno virtual:**

    ```bash
    py -m venv .venv
    .venv\Scripts\activate  # Windows
    source venv/bin/activate  # macOS/Linux
    ```

3.  **Instalar las dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Aplicar las migraciones:**

    ```bash
    py manage.py makemigrations
    py manage.py migrate
    ```

5.  **Crear un superusuario:**

    ```bash
    py manage.py createsuperuser
    ```

6.  **Ejecutar el servidor de desarrollo:**

    ```bash
    py manage.py runserver
    ```

7.  **Acceder a la aplicación:**

    *   Abre tu navegador web y visita: [http://127.0.0.1:8000/](http://127.0.0.1:8000/) (para la interfaz principal)
    *   Accede al panel de administración: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) (utiliza las credenciales del superusuario).

## ¡Explora y disfruta de Sistema de Gestión de Ventas! 🧾
