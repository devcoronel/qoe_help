let load = document.getElementById("loading");
let table = document.getElementById("mytable");

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

	fetch("/modulation" , {
		method: 'POST',
		body: formData
	})
		.then(response => response.json())
		.then(data => {
			if(typeof(data.msg) === 'object') {
				let elements = data.msg[0]
				let dates = data.msg[1]

				let tablehtml = `<table class="table table-hover" id="modulationtable" data-excel-name="Horas_QoE_afectado" ><thead class="table-dark"><td onclick="sortTable(0, 'modulationtable')" class="header"><strong>Plano</strong></td>`
							
				for (let i in dates) {
					let a = parseInt(i)+1
					tablehtml += `<td onclick="sortTable(`+ a +`, 'modulationtable')" class="header"><strong>`+ dates[i] +`</strong></td>`
				}
				tablehtml += '</thead><tbody>'
				
				for(let i in elements){
					tablehtml += '</td><td><a href="/detail/'+ elements[i][0] +'" target= "_blank">'+ elements[i][0] +'</a></td>'
					
					for (j in elements[i]) {
						if (j != 0) {
							tablehtml += '<td>'+ elements[i][j] +'</td>'
						}
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
