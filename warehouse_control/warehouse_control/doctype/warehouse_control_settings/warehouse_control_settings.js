frappe.ui.form.on('Warehouse Control Settings', {
    refresh: function(frm) {
        update_app_status(frm);
        update_module_list(frm);
        
        // Add toggle button
        frm.add_custom_button(
            __(frm.doc.enable_app ? 'Disable App' : 'Enable App'),
            function() {
                toggle_app(frm);
            },
            'primary'
        );
        
        // Add refresh button
        frm.add_custom_button(
            __('Refresh Status'),
            function() {
                update_app_status(frm);
                update_module_list(frm);
            },
            'btn-default'
        );
    },
    
    enable_app: function(frm) {
        // Auto-save when checkbox is toggled
        frm.save();
    }
});

function toggle_app(frm) {
    const new_status = !frm.doc.enable_app;
    
    frappe.call({
        method: 'warehouse_control.warehouse_control.doctype.warehouse_control_settings.warehouse_control_settings.toggle_app',
        args: {
            enable: new_status
        },
        callback: function(r) {
            if (r.message && r.message.status === 'success') {
                frm.reload_doc();
                
                // Show success message
                frappe.show_alert({
                    message: __(r.message.enabled ? '✓ App enabled successfully' : '✓ App disabled successfully'),
                    indicator: 'green'
                }, 5);
                
                // Clear cache and refresh after 2 seconds
                setTimeout(function() {
                    window.location.reload();
                }, 2000);
            }
        }
    });
}

function update_app_status(frm) {
    frappe.call({
        method: 'warehouse_control.warehouse_control.doctype.warehouse_control_settings.warehouse_control_settings.get_module_details',
        callback: function(r) {
            if (r.message) {
                const status = r.message;
                let status_html = '';
                
                if (frm.doc.enable_app) {
                    status_html = `
                        <div class="alert alert-success">
                            <h4><i class="fa fa-check-circle"></i> App is ENABLED</h4>
                            <p>Active Modules: ${status.active_count}</p>
                            <p>Inactive Modules: ${status.inactive_count}</p>
                        </div>
                    `;
                } else {
                    status_html = `
                        <div class="alert alert-warning">
                            <h4><i class="fa fa-exclamation-triangle"></i> App is DISABLED</h4>
                            <p>Total Modules: ${status.total}</p>
                            <p>All modules are currently inactive</p>
                        </div>
                    `;
                }
                
                frm.set_df_property('app_status_html', 'options', status_html);
                frm.refresh_field('app_status_html');
            }
        }
    });
}

function update_module_list(frm) {
    frappe.call({
        method: 'warehouse_control.warehouse_control.doctype.warehouse_control_settings.warehouse_control_settings.get_module_details',
        callback: function(r) {
            if (r.message) {
                const status = r.message;
                let modules_html = `
                    <table class="table table-bordered">
                        <thead>
                            <tr>
                                <th>Module Name</th>
                                <th>Status</th>
                                <th>Last Modified</th>
                            </tr>
                        </thead>
                        <tbody>
                `;
                
                // Add active modules
                status.active.forEach(function(module) {
                    modules_html += `
                        <tr class="success">
                            <td>${module.name}</td>
                            <td><span class="label label-success">Active</span></td>
                            <td>${module.modified}</td>
                        </tr>
                    `;
                });
                
                // Add inactive modules
                status.inactive.forEach(function(module) {
                    modules_html += `
                        <tr class="danger">
                            <td>${module.name}</td>
                            <td><span class="label label-danger">Inactive</span></td>
                            <td>${module.modified}</td>
                        </tr>
                    `;
                });
                
                modules_html += `
                        </tbody>
                    </table>
                `;
                
                frm.set_df_property('module_list_html', 'options', modules_html);
                frm.refresh_field('module_list_html');
            }
        }
    });
}
