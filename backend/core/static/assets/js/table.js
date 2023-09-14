var $table = $('#table')
var data2 = (document.getElementById("data").textContent === '') ?
		null : JSON.parse(document.getElementById("data").textContent);
const values = Object.values(data2)

var data = []
for (let i of values) { data.push(i); }


$(function () {
	$table.bootstrapTable({ data: data })

	$('#locale').change(function () {
		$table.bootstrapTable('refreshOptions', {
			locale: $(this).val()
		})
	})

})