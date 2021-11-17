let url = window.location.href;
let split = url.split("/");
let route = split[split.length - 1]

if (route == "hours") {
    let hours = document.getElementById("hours");
    hours.innerHTML = `<a class="nav-link fw-bold" href="/hours">Hours</a>`;
} else if (route == "qoe") {
    let qoe = document.getElementById("qoe");
    qoe.innerHTML = `<a class="nav-link fw-bold" href="/qoe">QoE</a>`;
} else if (route == "info") {
    let info = document.getElementById("info");
    info.innerHTML = `<a class="nav-link fw-bold" href="/info">Info</a>`;
} else if (route == "upload") {
    let upload = document.getElementById("upload");
    upload.innerHTML = `<a class="nav-link fw-bold" href="/upload">Upload</a>`;
} else {
    let detail = document.getElementById("detail");
    detail.innerHTML = `<a class="nav-link fw-bold" href="/detail">Detail</a>`;
};