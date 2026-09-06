// Elementos del DOM
const formulario = document.getElementById("formServicio");
const listaServicios = document.getElementById("listaServicios");
const mensaje = document.getElementById("mensaje");
const total = document.getElementById("total");
const spinner = document.getElementById("spinner");
const contenidoModal = document.getElementById("contenidoModal");

// Contador de registros
let contador = 0;

// Evento para registrar servicios
formulario.addEventListener("submit", function (e) {

    e.preventDefault();

    // Mostrar spinner
    spinner.classList.remove("d-none");

    // Obtener datos
    const nombre = document.getElementById("nombre").value.trim();
    const descripcion = document.getElementById("descripcion").value.trim();
    const categoria = document.getElementById("categoria").value;

    // Validaciones
    if (nombre === "" || descripcion === "" || categoria === "") {

        spinner.classList.add("d-none");

        mensaje.innerHTML = `
            <div class="alert alert-danger">
                Todos los campos son obligatorios.
            </div>
        `;

        return;
    }

    // Simular carga
    setTimeout(() => {

        spinner.classList.add("d-none");

        mensaje.innerHTML = `
            <div class="alert alert-success alert-dismissible fade show" role="alert">
                Servicio registrado correctamente.
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;

        // Crear card
        const columna = document.createElement("div");
        columna.className = "col-md-6 col-lg-4 mb-4";

        columna.innerHTML = `
            <div class="card shadow h-100">

                <div class="card-body">

                    <h5 class="card-title">${nombre}</h5>

                    <p class="card-text">
                        <strong>Descripción:</strong><br>
                        ${descripcion}
                    </p>

                    <span class="badge bg-success mb-3">
                        ${categoria}
                    </span>

                    <div class="d-flex gap-2">

                        <button class="btn btn-primary btn-sm ver">
                            Ver detalles
                        </button>

                        <button class="btn btn-danger btn-sm eliminar">
                            Eliminar
                        </button>

                    </div>

                </div>
            </div>
        `;

        listaServicios.appendChild(columna);

        contador++;
        total.textContent = contador;

        formulario.reset();

        // Botón eliminar
        columna.querySelector(".eliminar").addEventListener("click", function () {

            columna.remove();

            contador--;

            total.textContent = contador;

            mensaje.innerHTML = `
                <div class="alert alert-warning alert-dismissible fade show" role="alert">
                    Servicio eliminado correctamente.
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `;
        });

        // Botón ver detalles
        columna.querySelector(".ver").addEventListener("click", function () {

            contenidoModal.innerHTML = `
                <h4>${nombre}</h4>

                <hr>

                <p><strong>Descripción:</strong></p>

                <p>${descripcion}</p>

                <p><strong>Categoría:</strong> ${categoria}</p>
            `;

            const modal = new bootstrap.Modal(document.getElementById("modalInfo"));

            modal.show();

        });

    }, 800);

});