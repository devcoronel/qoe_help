let mynode = document.getElementById("id-node");
let mydays = document.getElementById("id-days");
let load = document.getElementById("loading")
let table = document.getElementById("my_table")

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

	fetch("/sumario", {
		method: 'POST',
		body: formData
	})
		.then(response => response.json())
		.then(data => {
			if(data.data) {
				let elements = data.data[0]
				let dates = data.data[1]
				let days = data.data[2]
				//console.log(elements, dates, days)

				let tablehtml = '<table class="table table-hover" id="hourstable" data-excel-name="Horas_QoE_afectado" ><thead class="table-dark"><td onclick="sortTable(0)" class="header"><strong>Plano</strong></td>'
							
				for (let i in dates) {
					let a = parseInt(i)+1
					tablehtml += '<td onclick="sortTable('+ a +')" class="header"><strong>'+ dates[i] +'</strong></td>' 
				}
				tablehtml += '</thead><tbody>'
				
				for(let i in elements){
					// let n = parseInt(i) + 1
					let key = Object.keys(elements[i])
					let values = elements[i][key]

					tablehtml += '</td><td><a href="/detalle/'+ key + '/'+ days +'">'+ key +'</a></td>'

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
			console.log("There was an error")
			
		})
	}	
);
