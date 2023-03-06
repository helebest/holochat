function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = jQuery.trim(cookies[i]);
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrfToken = getCookie('csrftoken');

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrfToken);
    }
  }
});

$(document).ready(function () {
  const messagesContainer = $("#chat-messages");
  function addMessage(message, isOutgoing) {
    const messageTypeClass = isOutgoing ? "outgoing-message" : "incoming-message";
    const messageElement = $("<div>", {class: "message " + messageTypeClass});
    const iconClass = isOutgoing ? "fas fa-user-circle outgoing-icon" : "fas fa-user-astronaut incoming-icon";
    const iconElement = $("<i>", {class: iconClass});
    if (isOutgoing) {
      messageElement.append($("<div>", {class: "message-content"})
          .append($("<div>", {class: "message-text"}).html(
              message.content + '<p>' + message.timestamp + '</p>')));
      messageElement.append(iconElement);
    } else {
      messageElement.append(iconElement);
      messageElement.append($("<div>", {class: "message-content"})
          .append($("<div>", {class: "message-text"}).html(
              message.content + '<p>' + message.timestamp + '</p>')));
    }
    messagesContainer.append(messageElement);
    messagesContainer.scrollTop(messagesContainer[0].scrollHeight);
  }
  function refreshChat() {
    $.get('/chatgpt_proxy/js_chat_hist', function (messages) {
      for (let i = 0; i < messages.length; i++) {
        const message = messages[i];
        if (message.role === 'assistant') {
          addMessage(message, false);
        } else {
          addMessage(message, true);
        }
      }
    });
  }

  // 处理表单提交事件来发送消息
  $("#message-form").submit(function (event) {
    event.preventDefault();
    let messageInput = $("#message-input");
    $("#message-input").prop('disabled', true);
    $("#message-submit").prop('disabled', true);
    let posting = $.post('/chatgpt_proxy/js_chat_send', {'messageInput': messageInput.val()})
    posting.done(function( data ) {
      messageInput.val("");
      refreshChat();
      $("#message-input").prop('disabled', false);
      $("#message-submit").prop('disabled', false);
    });
  });
  refreshChat();
});