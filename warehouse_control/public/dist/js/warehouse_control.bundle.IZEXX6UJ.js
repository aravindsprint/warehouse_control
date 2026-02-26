(() => {
  // ../warehouse_control/warehouse_control/public/js/warehouse_control.bundle.js
  frappe.provide("frappe.warehouse_control");
  frappe.warehouse_control = {
    check_status: function() {
      frappe.call({
        method: "frappe.client.get_value",
        args: {
          doctype: "Warehouse Control Settings",
          fieldname: "enable_app",
          filters: { name: "Warehouse Control Settings" }
        },
        callback: function(r) {
          if (r.message && !r.message.enable_app) {
            frappe.warehouse_control.hide_elements();
          }
        }
      });
    },
    hide_elements: function() {
      setTimeout(function() {
        $('.module-item:contains("Warehouse Control")').hide();
        $('[data-module="Warehouse Control"]').hide();
        $('.desktop-sidebar a:contains("Warehouse Control")').closest("li").hide();
        $('.module-view-link:contains("Warehouse Control")').closest(".module-item").hide();
        $(document).ajaxComplete(function(event, xhr, settings) {
          if (settings.url.includes("frappe.search")) {
            setTimeout(function() {
              $('.awesomplete li:contains("Warehouse Control")').hide();
            }, 100);
          }
        });
      }, 500);
    }
  };
  $(document).ready(function() {
    frappe.warehouse_control.check_status();
  });
  frappe.ready(function() {
    frappe.warehouse_control.check_status();
  });
})();
//# sourceMappingURL=warehouse_control.bundle.IZEXX6UJ.js.map
