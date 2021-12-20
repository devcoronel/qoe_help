const myform = document.getElementById("form_status");
let alert = document.getElementById("alert")

myform.addEventListener("submit", function (e) {
	e.preventDefault();

	const formData = new FormData(this);
    myform.reset()
	fetch("/status" , {
		method: 'POST',
		body: formData
	})
		.then(response => response.json())
		.then(data => {
            if ((data.msg).slice(-5) == 'éxito') {
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
				<div class="alert alert-warning alert-dismissible fade show" role="alert">
				<strong>Ocurrió un error interno. Intente de nuevo</strong>
				<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
				</div>
				`
		})
	}	
);