$(function () {

  $(".js-upload-photos").click(function () {
    $("#fileupload").click();
  });

  $("#fileupload").fileupload({
    dataType: 'json',
      sequentialUploads: true,

      start: function (e) {
	  $("#modal-progress").modal("show");
      },

      stop: function (e) {
	  $("#modal-progress").modal("hide");
      },
      
      //limit the number of input files
      change: function (e, data) {
       	  if(data.files.length>=50){
	      console.log(data.files.length);
	      alert("Max 100 files are allowed");
	      return false;
	  }
      },

      progressall: function (e, data) {
	  var progress = parseInt(data.loaded / data.total * 100, 10);
	  var strProgress = progress + "%";
	  $(".progress-bar").css({"width": strProgress});
	  $(".progress-bar").text(strProgress);
      },

      done: function (e, data) {
	  if (data.result.is_valid) {
	      $("#gallery tbody").prepend(
		  "<tr><td><a href='" + data.result.url + "'>" + data.result.name + "</a></td></tr>"
	      )
	  }
      }

  });

});
