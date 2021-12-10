let load = document.getElementById("loading");
let table = document.getElementById("div_dayly_table");

const myform = document.getElementById("form_sumary");

myform.addEventListener("submit", function (e) {
	e.preventDefault();
	table.innerHTML = ''
	load.innerHTML = `
		<div class="spinner-border text-primary" role="status">
		<span class="visually-hidden">Loading...</span>
		</div>
	`
	const formData = new FormData(this);

	fetch("/dayly" , {
		method: 'POST',
		body: formData
	})
		.then(response => response.json())
		.then(data => {
			if(typeof(data.msg) === 'object') {
				let elements = data.msg[0]
				let today = data.msg[1]

				let tablehtml = `
                <table class="table table-hover" id="daylytable">
                <thead class="table-dark">
                <td onclick="sortTable(0, 'daylytable')" class="header"><strong>Plano</strong></td>
				<td onclick="sortTable(1, 'daylytable')" class="header"><strong>QoE</strong></td>
				<td onclick="sortTable(2, 'daylytable')" class="header"><strong>Horas</strong></td>
				<td onclick="sortTable(3, 'daylytable')" class="header"><strong>Periodo</strong></td>
				<td onclick="sortTable(4, 'daylytable')" class="header"><strong>Cambios Modulación</strong></td>
				<td onclick="sortTable(5, 'daylytable')" class="header"><strong>Días</strong></td>`
				tablehtml += '</thead><tbody>'
				
				for(let i in elements){

					tablehtml += `<tr><td><a href="/detail/`+ elements[i][0] +`" target= "_blank">`+ elements[i][0] +`</a></td>
					<td>`+ elements[i][1] +`</td>
					<td>`+ elements[i][2] +`</td>
					<td>`+ elements[i][3] +`</td>
					<td>`+ elements[i][4] +`</td>
					<td>`+ elements[i][5] +`</td></tr>`

				}
				tablehtml += '</tbody></table>'
				load.innerHTML = ''
				table.innerHTML = tablehtml

			}
			else{
				load.innerHTML = ''
				table.innerHTML = '<strong>'+ data.msg +'</strong>'
			}
			
		})
		.catch(err => {
			load.innerHTML = ''
			console.log("There was an error")
			
		})
	}	
);
