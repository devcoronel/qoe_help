let url = window.location.href;
let split = url.split("/");
let route = split[split.length - 1]

if (route == "sumario") {
    let studies = document.getElementById("sumario");
    studies.innerHTML = `<a class="nav-link fw-bold" href="/sumario">Sumario</a>`;
} else if (route == "detalle") {
    let aboutme = document.getElementById("detalle");
    aboutme.innerHTML = `<a class="nav-link fw-bold" href="/detalle">Detalle</a>`;
} else {
    let proyects = document.getElementById("info");
    proyects.innerHTML = `<a class="nav-link fw-bold" href="/info">Info</a>`;
};