let table = document.getElementById("mytable");

function build(data) {
		if(typeof(data.msg[0]) === 'object') {
			let elements = data.msg[0]
			let dates = data.msg[1]

			let tablehtml = `<table class="table table-hover" id="modulationtable">
			<thead class="table-dark">
			<td onclick="sortTable(0, 'modulationtable')" class="header"><strong>CMTS</strong></td>
			<td onclick="sortTable(1, 'modulationtable')" class="header"><strong>Plano</strong></td>`
						
			for (let i in dates) {
				let a = parseInt(i)+2
				tablehtml += `<td onclick="sortTable(`+ a +`, 'modulationtable')" class="header"><strong>`+ dates[i] +`</strong></td>`
			}
			tablehtml += '</thead><tbody>'
			
			for(let i in elements){
				tablehtml += `<td>`+ elements[i][0] +`</td>
				<td><a href="/detail/`+ elements[i][1] +`" target= "_blank">`+ elements[i][1] +`</a></td>`
				
				for (j in elements[i]) {
					if (!(j == 0 || j == 1)) {
						tablehtml += '<td>'+ elements[i][j] +'</td>'
					}
				}
				
				tablehtml += '</tr>'
					
			}
			tablehtml += '</tbody></table>'
			table.innerHTML = tablehtml

		}
		else{
			table.innerHTML = '<strong>'+ data.msg +'</strong>'
		}
}