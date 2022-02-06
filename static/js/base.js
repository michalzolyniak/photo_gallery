$(function () {
    $('body').show();
    });

function makeFullScreen(e) {
         var target = e.srcElement || e.target;
         var divObj = target.parentElement.parentElement.parentElement.parentElement.querySelector('img')
           //Use the specification method before using prefixed versions
          if (divObj.requestFullscreen) {
            divObj.requestFullscreen();
          }
          else if (divObj.msRequestFullscreen) {
            divObj.msRequestFullscreen();
          }
          else if (divObj.mozRequestFullScreen) {
            divObj.mozRequestFullScreen();
          }
          else if (divObj.webkitRequestFullscreen) {
            divObj.webkitRequestFullscreen();
          } else {
            console.log("Fullscreen API is not supported");
          }
    };

function filter_user() {
        document.getElementById("select_user").submit();
    };

$(document).ready(function(){

          var multipleCancelButton = new Choices('#choices-multiple-remove-button', {
          removeItemButton: true,
          renderChoiceLimit:5
          });
      });