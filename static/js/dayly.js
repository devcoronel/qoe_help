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
                <td onclick="sortTable(0, 'daylytable')" class="header"><strong>CMTS</strong></td>
                <td onclick="sortTable(1, 'daylytable')" class="header"><strong>Plano</strong></td>
				<td onclick="sortTable(2, 'daylytable')" class="header"><strong>QoE</strong></td>
				<td onclick="sortTable(3, 'daylytable')" class="header"><strong>Horas</strong></td>
				<td onclick="sortTable(4, 'daylytable')" class="header"><strong>Periodo</strong></td>
				<td onclick="sortTable(5, 'daylytable')" class="header"><strong>Cambios Modulación</strong></td>
				<td onclick="sortTable(6, 'daylytable')" class="header"><strong>Días</strong></td>
				<td onclick="sortTable(7, 'daylytable')" class="header"><strong>Prioridad</strong></td>`
				tablehtml += '</thead><tbody>'
				
				for(let i in elements){

					tablehtml += `<tr>
					<td>`+ elements[i][0] +`</td>
					<td><a href="/detail/`+ elements[i][1] +`" target= "_blank">`+ elements[i][1] +`</a></td>
					<td>`+ elements[i][2] +`</td>
					<td>`+ elements[i][3] +`</td>
					<td>`+ elements[i][4] +`</td>
					<td>`+ elements[i][5] +`</td>
					<td>`+ elements[i][6] +`</td>`

					if (elements[i][2] <= 70 && elements[i][2] >= 0) {
						tablehtml += `<td>1</td></tr>`
					} else if (elements[i][2] > 70 && elements[i][2] <= 80) {
						tablehtml += `<td>2</td></tr>`
					} else if (elements[i][3] >= 3) {
						tablehtml += `<td>3</td></tr>`
					} else if (elements[i][5] >= 1) {
						tablehtml += `<td>4</td></tr>`
					} else {
						tablehtml += `<td>5</td></tr>`
					}

				}
				tablehtml += `</tbody></table>`
				
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
