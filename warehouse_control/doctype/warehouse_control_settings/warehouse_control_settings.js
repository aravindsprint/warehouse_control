frappe.ui.form.on('Warehouse Control Settings', {
    refresh: function(frm) {
        // Show current status
        let status = frm.doc.enable_app ? 'Enabled' : 'Disabled';
        let indicator = frm.doc.enable_app ? 'green' : 'red';
        
        frm.dashboard.add_indicator(__('App Status: {0}', [status]), indicator);
        
        // Add toggle button
        frm.add_custom_button(
            frm.doc.enable_app ? 'Disable App' : 'Enable App',
            function() {
                let new_value = frm.doc.enable_app ? 0 : 1;
                let action = new_value ? 'enable' : 'disable';
                
                frappe.confirm(
                    `Are you sure you want to ${action} the Warehouse Control app?`,
                    function() {
                        frm.set_value('enable_app', new_value);
                        frm.save();
                    }
                );
            }
        );
    },
    
    after_save: function(frm) {
        let msg = frm.doc.enable_app ? 'App enabled' : 'App disabled';
        frappe.show_alert({
            message: __(msg),
            indicator: frm.doc.enable_app ? 'green' : 'red'
        });
        
        // Refresh page after 2 seconds
        setTimeout(function() {
            window.location.reload();
        }, 2000);
    }
});
