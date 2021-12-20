const myform = document.getElementById("form_upload");
let alert = document.getElementById("alert")
let load = document.getElementById("load")
let make_question = false
function verify () {
	if (make_question == true){
		window.onbeforeunload = function(e) {
			return 'Please press the Logout button to logout.';
		};
	} else {
		window.onbeforeunload = null
	}
}

myform.addEventListener("submit", function (e) {
	e.preventDefault();

	const formData = new FormData(this);
	myform.reset()
	make_question = true
	verify()
	load.innerHTML = ''
    alert.innerHTML = `
	<div class="alert alert-primary alert-dismissible fade show" role="alert">
	<div class="row">
		<div class="col-2">
			<div class="spinner-border text-primary" role="status" >
			<span class="visually-hidden">Loading...</span>
			</div>
		</div>
		<div class="col-10"><strong><p style="text-align:center">Cargando: `+ formData.get('date') +`&nbsp&nbsp</p></strong></div>
		
		</div>
	</div>
	`

	fetch("/upload" , {
		method: 'POST',
		body: formData
	})
		.then(response => response.json())
		.then(data => {
			make_question = false
			verify()
            load.innerHTML = `
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
				<div class="alert alert-danger alert-dismissible fade show" role="alert">
				<strong>`+data.msg+`</strong>
				<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
				</div>
				`
			}
			
		})
		.catch(err => {
			alert.innerHTML = `
				<div class="alert alert-danger alert-dismissible fade show" role="alert">
				<strong>Ocurrió un error interno. Intente de nuevo</strong>
				<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
				</div>
				`
			load.innerHTML = `
            <button type="submit" class="btn btn-primary" style="padding-top: 0.2rem;">Subir data</button>
            `
		})
	}	
);