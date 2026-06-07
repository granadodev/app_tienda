# 🛒 App Gestión de Tienda

Una app web sencilla diseñada para la gestion de una tienda pequeña. Permite la gestión de inventario, ventas y un tipo de cuaderno de fiados.
---

## Características Principales

* **Pasarela de Ventas Inteligente (POS):**
    * **Buscadores interactivos en tiempo real (Live Search):** Selección de clientes y productos mediante menús flotantes dinámicos que agilizan el proceso de atención.
    * **Control total por teclado:** Navegación por los resultados con las flechas (Arriba/Abajo) y selección rápida con la tecla Enter para saltar automáticamente entre campos y añadir a la rejilla.
    * **Filtro de seguridad en Créditos:** El sistema valida el estado del cliente desde el backend; si un cliente está marcado como "No a Fiar" (Inactivo), no aparecerá en las opciones seleccionables de la pasarela de ventas para prevenir errores humanos.
    * **Transacciones atómicas:** Uso de `transaction.atomic()` en el servidor para asegurar que el descuento de stock y el registro del cobro se completen juntos, evitando datos corruptos.
* **Control de Inventario:**
    * Visualización limpia de productos registrados con su stock actual y unidades de medida.
    * Filtro de búsqueda instantáneo por nombre de producto desde el frontend.
    * **Descuento Lineal de Stock:** Control estricto de existencias que descuenta directamente las cantidades vendidas en cada transacción.
    * **Congelación de Precios:** Fijación automática del precio unitario del producto al momento de la venta para proteger el histórico contable ante futuros cambios de costos en el inventario.
* **Gestión de Clientes:**
    * Módulo organizado por estados dinámicos (Clientes Activos autorizados para fiar vs. Clientes "No a Fiar").
    * Búsqueda inteligente combinada que permite filtrar tanto por Nombre como por Teléfono.
* **Historial de Ventas Centralizado:**
    * Filtro avanzado integrado con Jinja y Django para clasificar los registros en tres secciones: Todas las ventas, Ventas en Efectivo (Consumidor Final) y Cuentas por Cobrar (Fiados).
    * Listado independiente de documentos (módulo de acumulación de saldos totales por cliente en desarrollo).

---

## Tecnologías Utilizadas

* **Backend:** Django 5.2 (Python 3.10)
* **Frontend:** Bootstrap 5, HTML5, JavaScript (ES6)
* **Base de Datos:** SQLite (Integrada de forma local)
* **Entorno de Desarrollo:** Anaconda (Conda Environments)

---

## Configuración Local

Sigue estos pasos para clonar el proyecto y ejecutarlo en tu máquina local utilizando tu entorno de Anaconda.

##Nota, los siguitntes pasos estan diseñados para usar el entorno de Conda. Si usted usa otro, tendra que adapar un poco los comandos.

### 1. Clonar el repositorio
Abre tu terminal o prompt de Anaconda y ejecuta:

```bash
git clone [https://github.com/granadodev/app-gestion-tienda.git](https://github.com/granadodev/app-gestion-tienda.git)
cd app-gestion-tienda
```



### 2. Activar tu entorno de Anaconda
Asegúrate de inicializar y activar el entorno virtual del proyecto:



###3. Preparar la Base de Datos (Migraciones)

Crea las tablas correspondientes en el archivo local de SQLite ejecutando las migraciones de Django:

```bash
#Hacer las migraciones
python manage.py makemigrations
python manage.py migrate


```



###4. Crear un Administrador (Opcional)

Si deseas acceder al panel de administración nativo de Django para gestionar usuarios, ejecuta:
```Bash

python manage.py createsuperuser
```



###5. Iniciar el Servidor de Desarrollo

Para correr el programa y empezar a utilizar la aplicación web, ejecuta el comando:

```Bash
python manage.py runserver
```

Una vez iniciado, abre tu navegador web e ingresa a la siguiente dirección:

```
http://localhost:8000/
```


###Estructura del Proyecto


Los modelos actuales del proyecto son:

    Product: Almacena la información de nombre, stock, unidad por la que se vende el producto y el precio por unidad (kilo, libra, etc).

    Customer: Almacena la información de contacto, fecha de registro y el interruptor booleano active que define si puede seguir pidiendo fiado.

    Sale: Documento principal de la venta que calcula de forma dinámica el monto total general invocando la propiedad @property def total_price mediante agregaciones (Sum).

    ProductSold: Modelo intermedio que extrae el precio oficial del inventario en su método save() y calcula de forma aislada los subtotales de cada artículo.









