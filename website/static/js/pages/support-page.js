/**
 * Code for interaction in the support page
 */

'use strict';

var Raven = require('raven-js');
var $ = require('jquery');
var $osf = require('js/osfHelpers');

$(document).ready(function(){
    /**
     * Toggle individual item with jQuery
     * @param item {Object} jQuery object for the .support-item element
     * @param turnOff {Boolean} true if we are closing and open item
     * @private
     */
    function changeExpandState (item, turnOff) {
        var body = item.children('.support-body');
        var head = item.children('.support-head');
        var icon = head.children('.fa');
        if (turnOff){
            body.slideUp();
            icon.removeClass('fa-angle-down').addClass('fa-angle-right');
            item.removeClass('open').addClass('collapsed');
        } else {
            body.slideDown();
            icon.removeClass('fa-angle-right').addClass('fa-angle-down');
            item.removeClass('collapsed').addClass('open');
        }
    }

    /**
     * Resets the filter states for searching support items
     */
    function resetFilter () {
        $('.support-item').each(function() {
            var el = $(this);
            changeExpandState(el, true);
            el.removeClass('support-nomatch');
        });
        $('.support-filter').val('');
        $('.clear-search').removeClass('clear-active');
        searchItemIndex = 0;
    }

    var searchItemIndex = 0; // Index for which search result is now supposed to be in view; for prev and next buttons

    /**
     * Small utility function to ease scrolling into locations in the body
     * @param el {Object} jquery element object
     */
    function scrollTo (el) {
        var location = el ? el.offsetTop : 150; // Scroll to top if nothing given
        $('html, body').animate({
            scrollTop: location-150
        }, 500);
    }

    /**
     * Changes state of previous and next buttons based on whether there are available items to show.
     */
    function updatePrevNextStatus () {
        var openItems = $('.support-item.open');
        if (openItems[searchItemIndex + 1]){
            $('.search-next').removeClass('disabled');
        } else {
            $('.search-next').addClass('disabled');
        }
        if (openItems[searchItemIndex - 1]){
            $('.search-previous').removeClass('disabled');
        } else {
            $('.search-previous').addClass('disabled');
        }
    }

    // Toggle individual view when clicked on header
    $('.support-head').click(function(){
        var item = $(this).parent();
        changeExpandState(item, item.hasClass('open'));
    });

    $('.search-expand').click(function(){
        resetFilter();
        $('.support-item').each(function(){
            changeExpandState($(this));
        });
        updatePrevNextStatus();

    });

    $('.search-collapse').click(function(){
        resetFilter();
        $('.support-item').each(function(){
            changeExpandState($(this), true);
        });
        updatePrevNextStatus();
    });

    $('.search-up').click(function(){
        scrollTo();
    });
    $('.search-previous').click(function(){
        if(searchItemIndex > 0){
            var openItems = $('.support-item.open');
            var prevEl = openItems.get(searchItemIndex-1);
            scrollTo(prevEl);
            $(prevEl).addClass('search-selected');
            $(openItems.get(searchItemIndex)).removeClass('search-selected');
            searchItemIndex--;
        }
        updatePrevNextStatus();
    });
    $('.search-next').click(function(){
        var openItems = $('.support-item.open');
        var nextEl = openItems.get(searchItemIndex+1);
        if(nextEl){
            scrollTo(nextEl);
            $(nextEl).addClass('search-selected');
            $(openItems.get(searchItemIndex)).removeClass('search-selected');
            searchItemIndex++;
        }
        updatePrevNextStatus();
    });


    $('.clear-search').click(resetFilter);

    $('.support-filter').keyup(function(){
        var text = $(this).val().toLowerCase();
        if(text.length === 0){
            resetFilter();
        }
        $('.clear-search').addClass('clear-active');
        if (text.length < 2) {
            return;
        }
        var el;
        var content;
        $('.support-item').each(function(){
            el = $(this);
            content = el.text().toLowerCase();
            if (content.indexOf(text) !== -1) {
                changeExpandState(el);
                el.removeClass('support-nomatch');
            } else {
                changeExpandState(el, true);
                el.addClass('support-nomatch');
            }
        });
        updatePrevNextStatus();
    });

    function fixSearchLayer () {
        var topOffset = $(window).scrollTop();
        var searchLayer = $('.search-layer');
        if(topOffset > 100 && !searchLayer.hasClass('fixed-layer')){
            searchLayer.addClass('fixed-layer');
            $('.support-title').hide();
            $('.search-up').removeClass('disabled');
        }
        if(topOffset <= 100 && searchLayer.hasClass('fixed-layer')){
            searchLayer.removeClass('fixed-layer');
            $('.support-title').show();
            $('.search-up').addClass('disabled');
        }
    }

    // Handle fixing support search box on scroll
    $(window).scroll(fixSearchLayer);
    fixSearchLayer();
    updatePrevNextStatus();
});
