// Hide warehouse_control elements when app is disabled
frappe.provide('frappe.warehouse_control');

frappe.warehouse_control = {
    check_status: function() {
        frappe.call({
            method: 'frappe.client.get_value',
            args: {
                doctype: 'Warehouse Control Settings',
                fieldname: 'enable_app',
                filters: { name: 'Warehouse Control Settings' }
            },
            callback: function(r) {
                if (r.message && !r.message.enable_app) {
                    frappe.warehouse_control.hide_elements();
                }
            }
        });
    },
    
    hide_elements: function() {
        // Hide module from sidebar
        setTimeout(function() {
            $('.module-item:contains("Warehouse Control")').hide();
            $('[data-module="Warehouse Control"]').hide();
            $('.desktop-sidebar a:contains("Warehouse Control")').closest('li').hide();
            
            // Hide from module view
            $('.module-view-link:contains("Warehouse Control")').closest('.module-item').hide();
            
            // Hide from awesome bar results
            $(document).ajaxComplete(function(event, xhr, settings) {
                if (settings.url.includes('frappe.search')) {
                    // Let the original response handler run, then modify
                    setTimeout(function() {
                        $('.awesomplete li:contains("Warehouse Control")').hide();
                    }, 100);
                }
            });
        }, 500);
    }
};

// Run on page load
$(document).ready(function() {
    frappe.warehouse_control.check_status();
});

// Run after frappe is ready
frappe.ready(function() {
    frappe.warehouse_control.check_status();
});
