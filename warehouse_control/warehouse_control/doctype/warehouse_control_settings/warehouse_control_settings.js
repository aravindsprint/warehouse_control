frappe.ui.form.on('Warehouse Control Settings', {
    refresh: function(frm) {
        frm.set_intro(
            frm.doc.enable_app
                ? __('✓ Warehouse Control is currently ENABLED.')
                : __('⚠ Warehouse Control is currently DISABLED. All data is preserved.'),
            frm.doc.enable_app ? 'green' : 'orange'
        );
    },

    enable_app: function(frm) {
        frm.save();
    }
});