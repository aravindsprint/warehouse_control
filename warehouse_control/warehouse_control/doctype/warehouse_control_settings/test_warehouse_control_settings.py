import frappe
import unittest

class TestWarehouseControlSettings(unittest.TestCase):
    def setUp(self):
        self.settings = frappe.get_single('Warehouse Control Settings')
    
    def test_toggle_app(self):
        # Get initial state
        initial_state = self.settings.enable_app
        
        # Toggle off
        self.settings.enable_app = not initial_state
        self.settings.save()
        
        # Check modules
        modules = frappe.db.get_all('Module Def', 
            filters={'app_name': 'warehouse_control'},
            fields=['disabled'])
        
        for module in modules:
            self.assertEqual(module.disabled, self.settings.enable_app)
        
        # Restore original state
        self.settings.enable_app = initial_state
        self.settings.save()
    
    def test_module_count(self):
        modules = frappe.db.get_all('Module Def', 
            filters={'app_name': 'warehouse_control'})
        
        status = self.settings.get_app_status()
        self.assertEqual(status['total'], len(modules))
