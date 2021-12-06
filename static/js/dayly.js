let load = document.getElementById("loading");
let table = document.getElementById("my_table");

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
				let dates = data.msg[1]

				let tablehtml = `
                <table class="table table-hover" id="daylytable" data-excel-name="Diario_`+ dates +`" >
                <thead class="table-dark">
                <td onclick="sortTable(0, 'daylytable')" class="header"><strong>Plano</strong></td>
				<td onclick="sortTable(1, 'hourstable')" class="header"><strong>QoE</strong></td>
				<td onclick="sortTable(2, 'hourstable')" class="header"><strong>Horas</strong></td>
				<td onclick="sortTable(3, 'hourstable')" class="header"><strong>Periodo</strong></td>
				<td onclick="sortTable(4, 'hourstable')" class="header"><strong>Cambios Modulación</strong></td>`
				tablehtml += '</thead><tbody>'
				
				for(let i in elements){
					// let n = parseInt(i) + 1
					let key = Object.keys(elements[i])
					let values = elements[i][key]

					tablehtml += '</td><td><a href="/detail/'+ key +'" target= "_blank">'+ key +'</a></td>'

					for(let j in values) {
						tablehtml += '<td>'+ values[j] +'</td>'
					}
				tablehtml += '</tr>'
						
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
