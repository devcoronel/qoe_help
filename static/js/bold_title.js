let url = window.location.href;
let split = url.split("/");
let route = split[split.length - 1]

if (route == "analysis") {
    let analysis = document.getElementById("analysis");
    analysis.innerHTML = `<a class="nav-link fw-bold" href="/analysis">Análisis</a>`;
} else if (route == "addnode") {
    let addnode = document.getElementById("addnode");
    addnode.innerHTML = `<a class="nav-link fw-bold" href="/addnode">Agregar</a>`;
} else if (route == "priority") {
    let priority = document.getElementById("priority");
    priority.innerHTML = `<a class="nav-link fw-bold" href="/priority">Seguimiento</a>`;
}  else if (route == "upload") {
    let upload = document.getElementById("upload");
    upload.innerHTML = `<a class="nav-link fw-bold" href="/upload">Carga</a>`;
} else if (route == "modulation") {
    let modulation = document.getElementById("modulation");
    modulation.innerHTML = `<a class="nav-link fw-bold" href="/modulation">Modulación</a>`;
} else if (route == "dayly") {
    let dayly = document.getElementById("dayly");
    dayly.innerHTML = `<a class="nav-link fw-bold" href="/dayly">Diario</a>`;
} else if (route == "sampling") {
    let sampling = document.getElementById("sampling");
    sampling.innerHTML = `<a class="nav-link fw-bold" href="/sampling">Muestreo</a>`;
} else {
    let detail = document.getElementById("detail");
    detail.innerHTML = `<a class="nav-link fw-bold" href="/detail">Detalle</a>`;
};