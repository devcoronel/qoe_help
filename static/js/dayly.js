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
                                <h4 class="fw-bold">Tabla Diaria `+ formData.get('dayly_date') +` - Región `+ formData.get('region') +`</h4>
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
				<td onclick="sortTable(3, 'daylytable')" class="header"><strong>CMs Afectados</strong></td>
				<td onclick="sortTable(4, 'daylytable')" class="header"><strong>CMs Estresados</strong></td>
				<td onclick="sortTable(5, 'daylytable')" class="header"><strong>Horas</strong></td>
				<td onclick="sortTable(6, 'daylytable')" class="header"><strong>Periodo</strong></td>
				<td onclick="sortTable(7, 'daylytable')" class="header"><strong>Cambio Modulación</strong></td>
				<td onclick="sortTable(8, 'daylytable')" class="header"><strong>Días</strong></td>
				<td onclick="sortTable(9, 'daylytable')" class="header"><strong>Prioridad</strong></td>`
				tablehtml += '</thead><tbody>'
				
				let cA = []
				let cB = []
				let cC = []
				let cD = []
				let cE = []

				let periodM = []
				let periodD = []
				let periodN = []
				let periodT = []
				let periodI = []
				let periodNo = []
				let periodMod = []

				let cA_greaterThan150 = []
				let cA_between50and150 = []
				let cA_between20and50 = []
				let cA_lessThan20 = []

				let cB_greaterThan150 = []
				let cB_between50and150 = []
				let cB_between20and50 = []
				let cB_lessThan20 = []

				let cC_greaterThan150 = []
				let cC_between50and150 = []
				let cC_between20and50 = []
				let cC_lessThan20 = []

				let cD_greaterThan150 = []
				let cD_between50and150 = []
				let cD_between20and50 = []
				let cD_lessThan20 = []
				
				for(let i in elements){

					tablehtml += `<tr>
					<td>`+ elements[i][0] +`</td>
					<td><a href="/detail/`+ elements[i][1] +`" target= "_blank">`+ elements[i][1] +`</a></td>
					<td>`+ elements[i][2] +`</td>
					<td>`+ elements[i][3] +`</td>
					<td>`+ elements[i][4] +`</td>
					<td>`+ elements[i][5] +`</td>
					<td>`+ elements[i][6] +`</td>
					<td>`+ elements[i][7] +`</td>
					<td>`+ elements[i][8] +`</td>`

					if (elements[i][2] < 70 && elements[i][2] >= 0) {
						cA.push(i)
						tablehtml += `<td> Con Afectación</td></tr>`
					} else if (elements[i][2] >= 70 && elements[i][2] < 80) {
						cC.push(i)
						tablehtml += `<td>Preventivo</td></tr>`
					} else if (elements[i][5] >= 3) {
						cB.push(i)
						tablehtml += `<td>Preventivo</td></tr>`
					} else if (elements[i][7] >= 2 && elements[i][5] >= 0) {
						cD.push(i)
						tablehtml += `<td>Preventivo</td></tr>`
					} else {
						cE.push(i)
						tablehtml += `<td>Monitoreo</td></tr>`
					}

					if (elements[i][6] == 'MADRUGADA') {
						periodM.push(i)
					} else if (elements[i][6] == 'DIA') {
						periodD.push(i)
					} else if (elements[i][6] == 'NOCHE') {
						periodN.push(i)
					} else if (elements[i][6] == 'TODO EL DIA') {
						periodT.push(i)
					} else if (elements[i][6] == 'INTERMITENTE') {
						periodI.push(i)
					} else if (elements[i][6] == 'NO AFECTADO') {
						if (elements[i][7] >= 2 && elements[i][5] >= 0) {
							periodMod.push(i)
						} else {
							periodNo.push(i)
						}
					}
				}

				for (let j in cA) {

					if(elements[cA[j]][3] > 150){
						cA_greaterThan150.push(cA[j])
					} else if(elements[cA[j]][3] > 50 && elements[cA[j]][3] <= 150){
						cA_between50and150.push(cA[j])
					} else if(elements[cA[j]][3] > 20 && elements[cA[j]][3] <= 50){
						cA_between20and50.push(cA[j])
					} else if(elements[cA[j]][3] <= 20){
						cA_lessThan20.push(cA[j])
					}
				}

				for (let k in cB) {

					if(elements[cB[k]][3] > 150){
						cB_greaterThan150.push(cB[k])
					} else if(elements[cB[k]][3] > 50 && elements[cB[k]][3] <= 150){
						cB_between50and150.push(cB[k])
					} else if(elements[cB[k]][3] > 20 && elements[cB[k]][3] <= 50){
						cB_between20and50.push(cB[k])
					} else if(elements[cB[k]][3] <= 20){
						cB_lessThan20.push(cB[k])
					}

				}
				for (let l in cC) {

					if(elements[cC[l]][3] > 150){
						cC_greaterThan150.push(cC[l])
					} else if(elements[cC[l]][3] > 50 && elements[cC[l]][3] <= 150){
						cC_between50and150.push(cC[l])
					} else if(elements[cC[l]][3] > 20 && elements[cC[l]][3] <= 50){
						cC_between20and50.push(cC[l])
					} else if(elements[cC[l]][3] <= 20){
						cC_lessThan20.push(cC[l])
					}

				}
				for (let m in cD) {
					
					if(elements[cD[m]][3] > 150){
						cD_greaterThan150.push(cD[m])
					} else if(elements[cD[m]][3] > 50 && elements[cD[m]][3] <= 150){
						cD_between50and150.push(cD[m])
					} else if(elements[cD[m]][3] > 20 && elements[cD[m]][3] <= 50){
						cD_between20and50.push(cD[m])
					} else if(elements[cD[m]][3] <= 20){
						cD_lessThan20.push(cD[m])
					}

				}

				let claseList = [cA.length, cB.length, cC.length, cD.length]
				let periodList = [periodM.length, periodD.length, periodN.length, periodT.length, periodI.length, periodMod.length]
				let sumPeriodPlanes = periodM.length + periodD.length + periodN.length + periodT.length + periodI.length + periodMod.length

				// console.log("qoe < 70: "+cA.length)
				// console.log("horas >= 3: "+cB.length)
				// console.log("qoe entre 70 y 80: "+cC.length)
				// console.log("modulacion: "+cD.length)
				// console.log("no afectado: "+cE.length)


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
                    <div class="col-4 m-2" style="background-color:#EBEDEF; border-radius: 1.5rem;">
						<h4 style="padding:0.5rem;text-align:center">Total Planos por Tipo de Afectación</h4>
                        <canvas id="canvas1"></canvas>
                    </div>
                    <div class="col-7 m-2" style="background-color:#EBEDEF; border-radius: 1.5rem;">
						<h4 style="padding:0.5rem;text-align:center">Total Planos por Periodo de Afectación</h4>
                        <canvas id="canvas2" style="padding:1rem"></canvas>
						<h6 style="padding:0.5rem;text-align:center">Total Planos = `+ sumPeriodPlanes +`</h6>
                    </div>
				</div>
				</div>
				<div class="container">
				<div class="row container">
					<div class="col-12" style="background-color:#EBEDEF; border-radius: 1.5rem;">
						<h4 style="padding:0.5rem;text-align:center">Tipo de Afectación por cantidad de Clientes Afectados</h4>
						<div id="impactedByTypeTable"></div>
					</div>
				</div>
				</hr>
				</div>`


				let canvas1 = document.getElementById("canvas1").getContext("2d")
				var chart1 = new Chart(canvas1, {
					type: "pie",
					data: {
						labels: ["QoE < 70","Horas ≥ 3","70 ≤ QoE < 80","Cambios de Mod ≥ 2"],
						datasets:[
							{
								backgroundColor: [
									'rgba(231, 76, 60, 0.5)',
									'rgba(230, 126, 34, 0.5)',
									'rgba(241, 196, 15, 0.5)',
									'rgba(88, 214, 141, 0.5)'
								],
								data: claseList
							}
						]
					},
					options:{
						plugins:{
							legend: {
								position: 'bottom'
							},
							labels:{
								render: (context) => {
									const percentage = context.value / showData(chart1) *100
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

				let canvas2 = document.getElementById("canvas2").getContext("2d")
				var chart2 = new Chart(canvas2, {
					type: "bar",
					data: {
						labels: ["MADRUGADA", "DIA", "NOCHE", "TODO EL DÍA", "INTERMITENTE", "MODULACIÓN"],
						datasets:[
							{
								label:"Periodo",
								backgroundColor: [
									'rgba(241, 196, 15, 0.5)', // amarillo
									'rgba(52, 152, 219, 0.5)', // azul
									'rgba(52, 73, 94, 0.5)', // azul oscuro
									'rgba(231, 76, 60, 0.5)', //rojo
									'rgba(142, 68, 173, 0.5)', // morado
									'rgba(88, 214, 141, 0.5)' // verde
									// 'rgba(189, 195, 199, 0.5)' // gris
								],
								data: periodList
							}
						]
					},
					options: {
						indexAxis: 'y',
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




				

				let impactedByTypeTable = document.getElementById("impactedByTypeTable")
				let impactedByTypeTableHTML = '<div class="scrollmenu" style="border-radius:10px;"><table class="table table-hover"><thead class="table-dark">'
				impactedByTypeTableHTML += `
				<tr>
					<td></td>
					<td></td>
					<td>Prioridad 1</td>
					<td>Prioridad 2</td>
					<td>Prioridad 3</td>
					<td>Prioridad 4</td>
					<td>Total General</td>
				</tr>
				<tr>
					<td>Estado de plano</td>
					<td>Estado</td>
					<td>150 < CMs Afectados</td>
					<td>50 < CMs Afectados ≤ 150</td>
					<td>20 < CMs Afectados ≤ 50</td>
					<td>CMs Afectados ≤ 20</td>
					<td></td>
				</tr>
				</thead>
				<tbody>
				<tr>
					<td rowspan="2">Con Afectación</td>
					<td>QoE < 70</td>
					<td>`+ cA_greaterThan150.length +`</td>
					<td>`+ cA_between50and150.length +`</td>
					<td>`+ cA_between20and50.length +`</td>
					<td>`+ cA_lessThan20.length +`</td>
					<td>`+ (cA_greaterThan150.length + cA_between50and150.length + cA_between20and50.length + cA_lessThan20.length) +`</td>
				</tr>
				<tr>
					<td>Horas ≥ 3</td>
					<td>`+ cB_greaterThan150.length +`</td>
					<td>`+ cB_between50and150.length +`</td>
					<td>`+ cB_between20and50.length +`</td>
					<td>`+ cB_lessThan20.length +`</td>
					<td>`+ (cB_greaterThan150.length + cB_between50and150.length + cB_between20and50.length + cB_lessThan20.length) +`</td>
				</tr>
				<tr>
					<td>Total</td>
					<td></td>
					<td>`+ (cA_greaterThan150.length + cB_greaterThan150.length) +`</td>
					<td>`+ (cA_between50and150.length + cB_between50and150.length) +`</td>
					<td>`+ (cA_between20and50.length + cB_between20and50.length) +`</td>
					<td>`+ (cA_lessThan20.length + cB_lessThan20.length) +`</td>
					<td>`+ (cA_greaterThan150.length + cA_between50and150.length + cA_between20and50.length + cA_lessThan20.length + cB_greaterThan150.length + cB_between50and150.length + cB_between20and50.length + cB_lessThan20.length) +`</td>
				</tr>

				<tr>
					<td rowspan="2">Preventivo</td>
					<td>70 ≤ QoE < 80</td>
					<td>`+ cC_greaterThan150.length +`</td>
					<td>`+ cC_between50and150.length +`</td>
					<td>`+ cC_between20and50.length +`</td>
					<td>`+ cC_lessThan20.length +`</td>
					<td>`+ (cC_greaterThan150.length + cC_between50and150.length + cC_between20and50.length + cC_lessThan20.length) +`</td>
				</tr>
				<tr>
					<td>Cambios de Modul ≥ 2</td>
					<td>`+ cD_greaterThan150.length +`</td>
					<td>`+ cD_between50and150.length +`</td>
					<td>`+ cD_between20and50.length +`</td>
					<td>`+ cD_lessThan20.length +`</td>
					<td>`+ (cD_greaterThan150.length + cD_between50and150.length + cD_between20and50.length + cD_lessThan20.length) +`</td>
				</tr>
				<tr>
					<td>Total</td>
					<td></td>
					<td>`+ (cC_greaterThan150.length + cD_greaterThan150.length) +`</td>
					<td>`+ (cC_between50and150.length + cD_between50and150.length) +`</td>
					<td>`+ (cC_between20and50.length + cD_between20and50.length) +`</td>
					<td>`+ (cC_lessThan20.length + cD_lessThan20.length) +`</td>
					<td>`+ (cC_greaterThan150.length + cC_between50and150.length + cC_between20and50.length + cC_lessThan20.length + cD_greaterThan150.length + cD_between50and150.length + cD_between20and50.length + cD_lessThan20.length) +`</td>
				</tr>
				<tr>
					<td>Total General</td>
					<td></td>
					<td>`+ (cA_greaterThan150.length + cB_greaterThan150.length + cC_greaterThan150.length + cD_greaterThan150.length) +`</td>
					<td>`+ (cA_between50and150.length + cB_between50and150.length + cC_between50and150.length + cD_between50and150.length) +`</td>
					<td>`+ (cA_between20and50.length + cB_between20and50.length + cC_between20and50.length + cD_between20and50.length) +`</td>
					<td>`+ (cA_lessThan20.length + cB_lessThan20.length + cC_lessThan20.length + cD_lessThan20.length) +`</td>
					<td>`+ (cA_greaterThan150.length + cB_greaterThan150.length + cC_greaterThan150.length + cD_greaterThan150.length + cA_between50and150.length + cB_between50and150.length + cC_between50and150.length + cD_between50and150.length + cA_between20and50.length + cB_between20and50.length + cC_between20and50.length + cD_between20and50.length + cA_lessThan20.length + cB_lessThan20.length + cC_lessThan20.length + cD_lessThan20.length) +`</td>
					
				</tr>
				</div>
				`
				
				//Clase A: QoE < 70
				// Clase B: Horas ≥ 3
				// Clase C: 70 ≤ QoE < 80
				// Clase D: Cambios de Modulación ≥ 2
				// Clase E: No afectado en la fecha

				impactedByTypeTable.innerHTML = impactedByTypeTableHTML

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
