function submit_message(message) {
    $.post( "/send_message", {
        message: message
    }, handle_response);
	

    function handle_response(data) {
      // append the bot repsonse to the div
		if(`${data.result}` == "null"){
			console.log(`${data.result}`);
			$('.conversation-view').append(`
				<div class="chat-bubble">
					<span classs="chat-content">
						${data.message}
					</span>
				</div>
			`);
          // remove the loading indicator
			$( "#loading" ).remove();
		} else{
			$('.conversation-view').append(`
				<div class="chat-bubble">
					<span class="chat-content">
						${data.message}
					</span>
				</div>
				<div class="chat-bubble result">
					<span class="chat-content">
						${data.result}
					</span>
				</div>
			`);
          // remove the loading indicator
			$( "#loading" ).remove();
		
		}
	}
}
i = 0;
setInterval(function() {
    i = ++i % 4;
    $(".loading").text("Loading Detail Information " + Array(i+1).join("."));
}, 800);


$('#target').on('submit', function(e){
    e.preventDefault();
    var $input_message = $('#input_message');
    var $conversation_view = $('.conversation-view');

    const input_message = $input_message.val()
    // return if the user does not enter any text
    if (!input_message) {
      return
    }

    $conversation_view.append(`
        <div class="chat-bubble me">
            <span class="chat-content">
                ${input_message}
            </span>
        </div>
	`);
    // loading
    $conversation_view.append(`
        <div class="chat-bubble" id="loading">
            <span class="chat-content">
                <b>...</b>
            </span>
        </div>
	`);

        // clear the text input 
    $input_message.val('');

    var div = document.getElementsByClassName("conversation-view")[0];
    div.scrollTop = div.scrollHeight;

	console.log(input_message);
        // send the message
    submit_message(input_message);
});
