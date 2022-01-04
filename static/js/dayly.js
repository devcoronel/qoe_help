let load = document.getElementById("loading");
let table = document.getElementById("div_dayly_table");
let statistics = document.getElementById("div_statistics")
let alert = document.getElementById("alert")
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
	myform.reset()

	fetch("/dayly" , {
		method: 'POST',
		body: formData
	})
		.then(response => response.json())
		.then(data => {
			if(typeof(data.msg) === 'object') {
				alert.innerHTML = ''
				let elements = data.msg[0]
				
				let tablehtml = `
				<div class="accordion accordion-flush" id="accordionFlushExample">
                    <div class="accordion-item" style="background-color: F2F5FA;">
                      <h2 class="accordion-header" id="flush-headingTwo">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseTwo" aria-expanded="false" aria-controls="flush-collapseTwo" style="background-color: EDF0F5;">
                            <div>
                                <h4 class="fw-bold">Tabla Diaria `+ formData.get('dayly_date') +`</h4>
                            </div>
                        </button>
                      </h2>
                      <div id="flush-collapseTwo" class="accordion-collapse collapse" aria-labelledby="flush-headingTwo" data-bs-parent="#accordionFlushExample">
                        <div class="accordion-body">
							<div style="display: flex ;justify-content: right;">
								<button id="daylybutton" class="btn btn-success" style="margin-bottom: 2rem;">Exportar</button>
							</div>
                            <div class="scrollmenu" style="border-radius:10px;">
							
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
				tablehtml += `</tbody></table>
				</div>
                        </div>
                      </div>
                    </div>
				</div>`
				
				load.innerHTML = ''
				table.innerHTML = tablehtml

				let body_statistics = `
				<hr>
                <br>
				<div class="row">
                    <div class="col-sm-10 col-md-9 col-9">
                        <h2 class="fw-bold"> <img src="../static/images/aboutme/i.png" width="35" class="pb-2">&nbspEstadística</h2>
                    </div>
                </div>
				<br>
				`
				statistics.innerHTML = body_statistics
				statistics.innerHTML += `
				<div class="row container">
                    <div class="col-3" style="background-color:#EBEDEF; border-radius: 1.5rem; margin: 0.5rem;">
						<pre style="padding:0.5rem">
Prioridad 1: QoE ≤ 70
Prioridad 2: 70 < QoE ≤ 80
Prioridad 3: Horas ≥ 3
Prioridad 4: Cambios de Modulación ≥ 1
Prioridad 5: No afectado en la fecha</pre>
                        <canvas id="canvas1"></canvas>
                    </div>
                    <div class="col-3" style="background-color:#EBEDEF; border-radius: 1.5rem; margin: 0.5rem;">
                        <canvas id="canvas2"></canvas>
                    </div>
                </div>`

				
				let dayly_table = document.getElementById("daylytable")
				let cell = dayly_table.getElementsByTagName("tr")
				let p1 = []
				let p2 = []
				let p3 = []
				let p4 = []
				let p5 = []

				let periodM = []
				let periodD = []
				let periodN = []
				let periodT = []
				let periodI = []
				let periodNo = []
				let periodMod = []

				for (let i = 1; i < cell.length; i++) {
					let priority = parseInt(cell[i].getElementsByTagName("td")[7].innerHTML)
					let period = cell[i].getElementsByTagName("td")[4].innerHTML

					if (priority == 1) {
						p1.push(priority)
					} else if (priority == 2) {
						p2.push(priority)
					} else if (priority == 3) {
						p3.push(priority)
					} else if (priority == 4) {
						p4.push(priority)
					} else if (priority == 5) {
						p5.push(priority)
					}

					if (period == 'MADRUGADA') {
						periodM.push(period)
					} else if (period == 'DIA') {
						periodD.push(period)
					} else if (period == 'NOCHE') {
						periodN.push(period)
					} else if (period == 'TODO EL DIA') {
						periodT.push(period)
					} else if (period == 'INTERMITENTE') {
						periodI.push(period)
					} else if (period == 'NO AFECTADO') {
						if (priority == 4){
							periodMod.push(period)
						} else{
							periodNo.push(period)
						}
					}
				}

				let p = [p1.length, p2.length, p3.length, p4.length, p5.length]

				let canvas1 = document.getElementById("canvas1").getContext("2d")
				var chart1 = new Chart(canvas1, {
					type: "bar",
					data: {
						labels: [1,2,3,4,5],
						datasets:[
							{
								label:"Prioridad",
								backgroundColor: [
									'rgba(231, 76, 60, 0.5)',
									'rgba(241, 196, 15, 0.5)',
									'rgba(88, 214, 141, 0.5)',
									'rgba(52, 152, 219, 0.5)',
									'rgba(189, 195, 199, 0.5)'
								],
								data: p
							}
						]
					},
					options: {
						scales: {
							y: {
								beginAtZero: true
							}
						}
					}
				})

				let canvas2 = document.getElementById("canvas2").getContext("2d")
				var chart2 = new Chart(canvas2, {
					type: "pie",
					data: {
						labels: [1,2,3,4,5],
						datasets:[
							{
								label: "Prioridad",
								backgroundColor: [
									'rgba(231, 76, 60, 0.5)',
									'rgba(241, 196, 15, 0.5)',
									'rgba(88, 214, 141, 0.5)',
									'rgba(52, 152, 219, 0.5)',
									'rgba(189, 195, 199, 0.5)'
								],
								data: p
							}
						]
					}
				})


				document.getElementById('daylybutton').addEventListener('click', function() {
					var table2excel = new Table2Excel();
					table2excel.export(document.querySelectorAll("#daylytable"), "Diario_"+ formData.get('dayly_date'));
				});
			}
			else{
				load.innerHTML = ''
				statistics.innerHTML = ''
				alert.innerHTML = `
				<div class="alert alert-danger alert-dismissible fade show" role="alert">
				<strong>`+ data.msg +`</strong>
				<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
				</div>
				`
			}
			
		})
		.catch(err => {
			console.log(err)
			load.innerHTML = ''
			statistics.innerHTML = ''
			alert.innerHTML = `
				<div class="alert alert-danger alert-dismissible fade show" role="alert">
				<strong>Ocurrió un error interno. Intente de nuevo</strong>
				<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
				</div>
				`
		})
	}	
);
