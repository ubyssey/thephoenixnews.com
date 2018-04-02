require('../styles/main.scss')

var $ = require('jquery');

$(function() {

  var stickyElements = [];

  $('.js-sticky').each(function() {
    stickyElements.push($(this));
  });

  $(window).scroll(() => {
    const scrollTop = $(window).scrollTop();
    stickyElements.map(element => {
      const elementOffset = element.data('offset');
      const elementHeight = element.height();
      const parentOffset = element.parent().offset().top;
      const parentHeight = element.parent().height();
      const hasClass = element.hasClass('js-sticky--fixed');
      const shouldStick = parentOffset - scrollTop < elementOffset;
      const shouldFreeze = scrollTop + elementOffset + elementHeight >= parentOffset + parentHeight;

      if (shouldFreeze) {
        element.removeClass('js-sticky--fixed');
        element.addClass('js-sticky--frozen');
      } else if (shouldStick) {
        if (!hasClass) {
          element.removeClass('js-sticky--frozen');
          element.addClass('js-sticky--fixed');
          element.css('top', element.data('offset') + 'px');
        }
      } else if (hasClass) {
        element.removeClass('js-sticky--fixed');
      }
    });
  });

})
