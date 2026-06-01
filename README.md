# Descargar este código
Para descargar el código se puede utilizar o bien git, o bien la interfaz de github.

### Opción 1: usar git, por línea de comandos (recomendado)
  - Crear una carpeta, en cualquier ubicación preferida.
    Por ejemplo, dentro de `/home/al/fiuba/1c2025/modelos`, crear la carpeta `repo-modelos/`.
    **Todos los comandos siguientes (de esta sección y de las demás secciones) deben ejecutarse desde dentro de esa nueva carpeta `repo-modelos/`.**
  
  - Entrar a la nueva carpeta.
    - Se puede abrir un IDE (recomendado). Desde sus menúes elegir `Abrir carpeta` o similar y elegir esta nueva carpeta `repo-modelos/`. Desde sus menúes también se puede abrir un `Nuevo terminal` que abrirá ya dentro de esa misma carpeta.
  
    - Si no se quiere utilizar un IDE, se puede abrir una terminal, navegar hasta la carpeta en cuestión (en el ejemplo `cd /home/al/fiuba/1c2025/modelos/repo-modelos/`). Se recomienda usar un IDE.
  
  **Con esto se abrió una terminal (sea con o sin IDE) en la nueva carpeta. En dicha terminal, que ya tiene abierta la carpeta correcta, ejecutar los siguientes comandos (de esta sección y de las demás secciones).**
  
  - Clonar el repositorio:
    `git clone git@github.com:Aldy09/sw-modelos
.git .`
    Esto clona el repositorio, en la carpeta `repo-modelos/`.
  - Traer los últimos cambios (esto es útil para más adelante cuando haya que traer cambios nuevos, actualmente solo informará que Ya está actualizado):
    `git pull`
    
    El código ha sido descargado. Continuar con la siguiente sección.

### Opción 2: interfaz gráfica de Github
  - Clickear el botón verde llamado `<> Code` y luego la opción `Download ZIP`.
    Guardarlo en cualquier ubicación preferida, por ejemplo dentro de `/home/al/fiuba/1c2025/modelos`.
    Dar botón derecho al archivo y `Extraer` (o procedimiento necesario para extraer el .zip).
    Eso genererá una nueva carpeta llamada `sw-modelos-main/`. 
    
    **Todos los comandos siguientes (de esta sección y de las demás secciones) deben ejecutarse desde dentro de esa nueva carpeta `sw-modelos-main/`.**
    
    - Se puede abrir un IDE (recomendado). Desde sus menúes elegir `Abrir carpeta` o similar y elegir esta nueva carpeta `sw-modelos-main/`. Desde sus menúes también se puede abrir un `Nuevo terminal` que abrirá ya dentro de esa misma carpeta.
  
    - Si no se quiere utilizar un IDE, se puede abrir una terminal, navegar hasta la carpeta en cuestión (en el ejemplo `cd /home/al/fiuba/1c2025/modelos/sw-modelos-main/`). Se recomienda usar un IDE.
  
  **Con esto se abrió una terminal (sea con o sin IDE) en la nueva carpeta. En dicha terminal, que ya tiene abierta la carpeta correcta, ejecutar los comandos de las secciones siguientes.**

# Instalar dependencias y configurar filtro git
Luego de haber descargado e instalado `ILOG CPLEX Optimization Studio` de la página oficial de IBM, y de haber terminado de ejecutar la sección `Descargar este código`, seguir estos pasos.

- Crear un entorno python:

  `python -m venv .venv`

- Activarlo:

  `source .venv/bin/activate`

- Instalar dependencias:

  `pip install -r requirements.txt`


- Identificar la, llamémosla "carpeta_base", en la que se instaló ibm cplex.

  Para verificar, la carpeta es la que contiene a:

   ```
    concert  cpoptimizer  license  python       swidtag
    cplex    doc          opl      README.html  Uninstall
   ```

  Copiarse la ruta a la carpeta base, incluyendo a la carpeta_base. Llamémosla "ruta_base".

  (ej ruta_base: /home/al/otras_posibles_carpetas/[carpeta_base])

- Para poder utilizar ibm cplex:

  `./.venv/bin/python [ruta_base]/python/setup.py install`

- Para configurar un filtro para que git no agregue cambios de metadata de los notebooks (como la execution_count de las celdas) ni las imágenes generadas:

  `./configure_cleaning_for_git.sh` (recomendado)

  - Si en cambio se desea no conservar la metadata pero sí conservar las imágenes (ej plots) en los commits

    `./configure_cleaning_for_git_allow_images.sh`

  - Se recomienda no conservar las imágenes. De lo contrario cada vez que se vuelva a ejecutar un notebook, por más que no se haya hecho ningún cambio y el gráfico que se genere sea exactamente el mismo con exactamente los mismos datos, git lo interpreta como uno nuevo y committea sus bytes cada vez, quedando menos claros los diffs y poblando el history de cambios que en realidad no son cambios.

## Comentario sobre git
**Aclaración sobre comportamiento 'extraño' de git, que se debe al filtro configurado.**

El filtro de git configurado no modifica los notebooks en local, solo modifica la copia que usa internamente, pero los notebooks quedan intactos localmente.

Debido a cómo funcionan los filtros en git, lo que vemos es lo siguiente:
- abrimos un notebook que ya está committeado, no cambiamos absolutamente nada, lo ejecutamos tal cual está
- en `git status` veremos que existen cambios, porque cambió la metadata de execution_count de las celdas
- si se hace `git diff` ahí No se verán los cambios, esto es un comportamiento inusual, se debe a la comparación interna que hace git y cómo se aplican los filtros
- se puede hacer `git add` del notebook en cuestión, y luego de eso si se hace git status se verá que No hay cambios para committear, porque se aplicó el filtro y la metadata no se considera un cambio relevante.

# Ejecutar
Actualmente se cuenta con datos de prueba, modificables, en `data_and_model_construction/`.

Para ejecutar, se puede correr las celdas de los distintos notebooks, se puede iniciar basándose en `SOLVING EXAMPLE.ipynb`.

Para ejecutar el código que realiza los gráficos de valor marginal, costo de oportunidad, funcional y curva de oferta, se puede utilizar el notebook `ALL IN ONE USAGE EXAMPLE Problema5tipo2.ipynb`.

Aclaraciones:
- (Luego de modificar un archivo ".py", para ver los cambios reflejados desde un notebook se debe "Reiniciar kernel").
- La primera vez que se intente ejecutar, si es desde un ide, preguntará qué kernel se desea usar, elegir de la lista el correspondiente a ".venv".
- El gráfico de costo de oportunidad vs un rhs ('disponibilidad'), muestra en el eje vertical distintas cosas según el caso:
  - el costo de oportunidad del producto si el mismo no tenía demanda mínima,
  - el llamado 'costo de oportunidad encubierto' (VM de la demanda mínima) si el producto tenía demanda mínima.

# Traer cambios
- si se usó la opción 1 para descargar este código:
  `git pull`
- si se usó la popción 2: repetir el procedimiento de descarga.