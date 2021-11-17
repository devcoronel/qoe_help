const myform = document.getElementById("form_upload");

myform.addEventListener("submit", function (e) {
	e.preventDefault();

	const formData = new FormData(this);

    document.getElementById("load").innerHTML = `
        <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
        </div>
        `
    document.getElementById("title").innerHTML = `
    <h2 class="fw-bold" style="text-align: center;"> <img src="{{ url_for('static', filename='images/aboutme/years.png') }}" width="35" class="pb-2">&nbsp{{title}}&nbsp<img src="{{ url_for('static', filename='images/aboutme/years.png') }}" width="35" class="pb-2"></h2>
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
            document.getElementById("title").innerHTML = `
            <h2 class="fw-bold" style="text-align: center;"> <img src="static/images/aboutme/check.png" width="35" class="pb-2">&nbspCarga de data&nbsp<img src="static/images/aboutme/check.png" width="35" class="pb-2"></h2>
            `
		})
		.catch(err => {
			console.log("There was an error")
			
		})
	}	
);