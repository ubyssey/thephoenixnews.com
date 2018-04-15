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
      const
        elementOffset = element.data('offset'),
        elementHeight = element.height(),
        parentOffset = element.parent().offset().top,
        parentHeight = element.parent().height();

      if (parentHeight <= elementHeight) {
        return;
      }

      const
        hasClass = element.hasClass('js-sticky--fixed'),
        shouldStick = parentOffset - scrollTop < elementOffset,
        shouldFreeze = scrollTop + elementOffset + elementHeight >= parentOffset + parentHeight;

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
