/**
 * Created by Sami on 2/05/2016.
 */

	$( document ).ready(function() {
		var loginForm = $("#loginForm");
		loginForm.submit(function(e) {
			//console.log("clicked " + $('input[name=password]').val());
			e.preventDefault();
			//var formData = loginForm.serialize();
			var token = $('input[name=csrfmiddlewaretoken]').val();
			var email = $('input[name=email]').val() == "" ? "null" : $('input[name=email]').val();
			var password = $('input[name=password]').val() == "" ? "null" : $('input[name=password]').val();
			//console.log(token + " : " + email + " : " + password);
			$.ajax({
				url:'/login/',
				type:'POST',
				//data:formData,
				data: {csrfmiddlewaretoken: token, email: email, password: password},
				success:function(data) {
					//console.log(data['error'].length);
					if (data['error'] != undefined) { //look if the error exists?
						$('#login-message').html(data['error']);
						//console.log(data['error']);
					} else { //no error?
						var newDoc = document.open();
						newDoc.write(data);
						newDoc.close();
					}
				},
				error: function (data) {
					console.log("error");
				}
			});
		});
		/*$('#facebook-login-btn').on('click', function() {
			console.log(document.URL);
			window.location = "/auth/facebook";
		});*/
		console.log("Login.js loaded succesfully.");
	});