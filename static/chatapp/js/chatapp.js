// timers
var hasNewMessagesTimer;
var hasNewChatsTimer;
var scrollDownMessagesTimer;
var scrollPosition = $('#conversation').scrollTop();

$(function(){
    $(".heading-compose").click(function() {
      $(".side-two").css({
        "left": "0"
      });
    });

    $(".newMessage-back").click(function() {
      $(".side-two").css({
        "left": "-100%"
      });
    });
});

function scrollDownMessages() {
  $('#conversation').scrollTop($('#conversation')[0].scrollHeight);
  clearTimeout(scrollDownMessagesTimer);
}

function openMessages(chaturl) {
  clearTimeout(hasNewMessagesTimer);

  $('#chat_messages').load(chaturl, function(data) {
    scrollDownMessagesTimer = setInterval(function() {
      scrollDownMessages();
    }, 100);
  });
}