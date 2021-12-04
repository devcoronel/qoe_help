const myform = document.getElementById("form_upload");
let alert = document.getElementById("alert")

myform.addEventListener("submit", function (e) {
	e.preventDefault();

	const formData = new FormData(this);

    document.getElementById("load").innerHTML = `
        <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
        </div>
        `

	fetch("/upload" , {
		method: 'POST',
		body: formData
	})
		.then(response => response.json())
		.then(data => {
            document.getElementById("load").innerHTML = `
            <button type="submit" class="btn btn-primary" style="padding-top: 0.2rem;">Subir data</button>
            `
			if(data.msg == 'Carga subida con éxito'){
				alert.innerHTML = `
				<div class="alert alert-success alert-dismissible fade show" role="alert">
				<strong>`+data.msg+`</strong>
				<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
				</div>
				`
			} else {
				alert.innerHTML = `
				<div class="alert alert-warning alert-dismissible fade show" role="alert">
				<strong>`+data.msg+`</strong>
				<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
				</div>
				`
			}
			
		})
		.catch(err => {
			document.getElementById("load").innerHTML = ''
			console.log("There was an error")
			
		})
	}	
);