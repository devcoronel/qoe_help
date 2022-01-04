let load = document.getElementById("loading");
let table = document.getElementById("div_dayly_table");
let statistics = document.getElementById("div_statistics")
let alert = document.getElementById("alert")
const myform = document.getElementById("form_sumary");

myform.addEventListener("submit", function (e) {
	e.preventDefault();
	table.innerHTML = ''
	statistics.innerHTML = ''
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

					if (elements[i][2] < 70 && elements[i][2] >= 0) {
						tablehtml += `<td>1</td></tr>`
					} else if (elements[i][2] >= 70 && elements[i][2] < 80) {
						tablehtml += `<td>2</td></tr>`
					} else if (elements[i][3] >= 3) {
						tablehtml += `<td>3</td></tr>`
					} else if (elements[i][5] >= 2 && elements[i][3] >= 0) {
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
				<div class="row">
                    <div class="col-sm-10 col-md-9 col-9">
                        <h2 class="fw-bold"> <img src="../static/images/aboutme/i.png" width="35" class="pb-2">&nbspEstadística</h2>
                    </div>
                </div>
				`
				statistics.innerHTML = body_statistics
				statistics.innerHTML += `
				<div class="container">
				<div class="row container">
                    <div class="col-3 m-2" style="background-color:#EBEDEF; border-radius: 1.5rem;">
						<pre style="padding:0.5rem">
Prioridad 1: QoE < 70
Prioridad 2: 70 ≤ QoE < 80
Prioridad 3: Horas ≥ 3
Prioridad 4: Cambios de Modulación ≥ 2
Prioridad 5: No afectado en la fecha</pre>
                        <canvas id="canvas1"></canvas>
                    </div>
                    <div class="col-3 m-2" style="background-color:#EBEDEF; border-radius: 1.5rem;">
                        <canvas id="canvas2"></canvas>
                    </div>
					<div class="col-5 m-2" style="background-color:#EBEDEF; border-radius: 1.5rem;">
                        <canvas id="canvasA"></canvas>
                    </div>
				</div>
				</div>
				<div class="container">
				<div class="row container">
					<div class="col-3 m-2" style="background-color:#EBEDEF; border-radius: 1.5rem;">
						<pre style="padding:0.5rem">
MAD: Madrugada
DIA: Día
NOC: Noche
TED: Todo el día
INT: Intermitente
MOD: Cambios de Modulación ≥ 3
NAF: No afectado en la fecha</pre>
						<canvas id="canvas3"></canvas>
                    </div>
					<div class="col-3 m-2" style="background-color:#EBEDEF; border-radius: 1.5rem;">
                        <canvas id="canvas4"></canvas>
                    </div>
					<div class="col-5 m-2" style="background-color:#EBEDEF; border-radius: 1.5rem;">
                        <canvas id="canvasB"></canvas>
                    </div>
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

				let priorityList = [p1.length, p2.length, p3.length, p4.length, p5.length]
				let periodList = [periodM.length, periodD.length, periodN.length, periodT.length, periodI.length, periodMod.length, periodNo.length]

				let canvas1 = document.getElementById("canvas1").getContext("2d")
				var chart1 = new Chart(canvas1, {
					type: "bar",
					data: {
						labels: ["P1","P2","P3","P4","P5"],
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
								data: priorityList
							}
						]
					},
					options: {
						plugins:{
							labels:{
								render: 'value'
							}
						},
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
						labels: ["Prioridad 1","Prioridad 2","Prioridad 3","Prioridad 4","Prioridad 5"],
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
								data: priorityList
							}
						]
					},
					options:{
						plugins:{
							labels:{
								render: (context) => {
									const percentage = context.value / showData(chart2) *100
									return percentage.toFixed(0)+'%'
								},
								fontColor: '#fff',
								shadowColor: '#fff'
							},
						},

					},
				})
				function showData(chart){
					let totalsum = 0
					let i = 0
					for (i; i < chart.config.data.datasets[0].data.length; i++){
						if (chart.getDataVisibility(i) === true){
							totalsum += chart.config.data.datasets[0].data[i]
						}
					}
					return totalsum
				}

				let canvas3 = document.getElementById("canvas3").getContext("2d")
				var chart3 = new Chart(canvas3, {
					type: "bar",
					data: {
						labels: ["MAD", "DIA", "NOC", "TED", "INT", "MOD", "NAF"],
						datasets:[
							{
								label:"Periodo",
								backgroundColor: [
									'rgba(241, 196, 15, 0.5)', // amarillo
									'rgba(52, 152, 219, 0.5)', // azul
									'rgba(52, 73, 94, 0.5)', // azul oscuro
									'rgba(231, 76, 60, 0.5)', //rojo
									'rgba(88, 214, 141, 0.5)', // verde
									'rgba(142, 68, 173, 0.5)', // morado
									'rgba(189, 195, 199, 0.5)' // gris
								],
								data: periodList
							}
						]
					},
					options: {
						plugins:{
							labels:{
								render: 'value'
							}
						},
						scales: {
							y: {
								beginAtZero: true
							}
						}
					}
				})

				let canvas4 = document.getElementById("canvas4").getContext("2d")
				var chart4 = new Chart(canvas4, {
					type: "pie",
					data: {
						labels: ["Madrugada","Día","Noche","Todo el día","Intermitente", "Modulación", "No Afectado"],
						datasets:[
							{
								label: "Periodo",
								backgroundColor: [
									'rgba(241, 196, 15, 0.5)', // amarillo
									'rgba(52, 152, 219, 0.5)', // azul
									'rgba(52, 73, 94, 0.5)', // azul oscuro
									'rgba(231, 76, 60, 0.5)', //rojo
									'rgba(88, 214, 141, 0.5)', // verde
									'rgba(142, 68, 173, 0.5)', // morado
									'rgba(189, 195, 199, 0.5)' // gris
								],
								data: periodList
							}
						]
					},
					options:{
						plugins:{
							labels:{
								render: (context) => {
									const percentage = context.value / showData(chart4) *100
									return percentage.toFixed(0)+'%'
								},
								fontColor: '#fff',
								shadowColor: '#fff'
							},
						},

					},
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
