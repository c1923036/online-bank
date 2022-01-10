/*copyright Richard Milton 2011 - http://www.webweasel.co.uk/uk-bank-account-sort-code-jquery-plugin/example.html */
(function($) {

    $.fn.extend({

        sortCode: function(options) {

            var defaults = {
                boxwidth: 20,
                debug: false
            }

            var options = $.extend(defaults, options);
            var id = 0;

            return this.each(function() {

                var o = options,
                    $this = $(this),
                    thisName = $this.attr('name'),
                    spanClass = $this.attr('name') + '-break-sort-' + id,
                    errMess = false,
                    sc = $this.val();

                try {
                    if (typeof thisName == 'undefined') errMess = 'name attribute missing';
                    if ($('input[name=' + thisName + ']').length > 1) errMess = 'duplicate name attribute ' + thisName;
                    if (!errMess) {
                        $this.toggle(o.debug).after('<span class="' + spanClass + '"><input type="text">-<input type="text">-<input type="text"></span>');
                        $('.' + spanClass + '>input').attr('maxlength', '2').css('width', o.boxwidth + 'px').blur(function() {
                            $this.val($('.' + spanClass + '>input:eq(0)').val() + '' + $('.' + spanClass + '>input:eq(1)').val() + '' + $('.' + spanClass + '>input:eq(2)').val());
                        }).keydown(function(e) {
                            return (e.which == 9 || e.which == 8 || e.which == 46 || e.which >= 48 && e.which <= 57) || (e.which >= 96 && e.which <= 105);
                        }).keyup(function(e) {
                            if ((e.which >= 48 && e.which <= 57) || (e.which >= 96 && e.which <= 105)) {
                                if ($(this).val().length == 2 && $(this).next().length > 0) $(this).blur().next().select();
                            }
                        });
                        $('.' + spanClass + '>input:eq(0)').val(sc && sc != '' && sc.length >= 2 ? sc.substr(0, 2) : '');
                        $('.' + spanClass + '>input:eq(1)').val(sc && sc != '' && sc.length >= 4 ? sc.substr(2, 2) : '');
                        $('.' + spanClass + '>input:eq(2)').val(sc && sc != '' && sc.length >= 6 ? sc.substr(4, 2) : '');
                        id++;
                    }
                } catch (err) {
                    errMess = err + ' (check html syntax)';
                }
                if (errMess && o.debug) {
                    $this.after(' <strong>sortCode() plugin error:</strong> ' + errMess);
                }
            });
        }
    });
})(jQuery);